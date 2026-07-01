import express from 'express';
import multer from 'multer';
import { Octokit } from '@octokit/rest';
import { z } from 'zod';

const app = express();
const upload = multer({ storage: multer.memoryStorage(), limits: { fileSize: 95 * 1024 * 1024 } });

app.use(express.json({ limit: '100mb' }));

const env = z.object({
  GITHUB_TOKEN: z.string().min(1),
  CONNECTOR_API_KEY: z.string().min(16).optional(),
  DEFAULT_OWNER: z.string().default('focusnegotiuminc-creator'),
  DEFAULT_REPO: z.string().default('improved-rotary-phone'),
  VERCEL_TOKEN: z.string().optional(),
  VERCEL_PROJECT_ID: z.string().optional(),
  VERCEL_TEAM_ID: z.string().optional()
}).parse(process.env);

const octokit = new Octokit({ auth: env.GITHUB_TOKEN });

function requireKey(req, res, next) {
  if (!env.CONNECTOR_API_KEY) return next();
  const given = req.header('x-focus-connector-key') || req.query.key;
  if (given !== env.CONNECTOR_API_KEY) {
    return res.status(401).json({ ok: false, error: 'Unauthorized connector request' });
  }
  return next();
}

function repoParams(body = {}) {
  return {
    owner: body.owner || env.DEFAULT_OWNER,
    repo: body.repo || env.DEFAULT_REPO
  };
}

async function getFileSha({ owner, repo, path, branch }) {
  try {
    const existing = await octokit.repos.getContent({ owner, repo, path, ref: branch });
    if (Array.isArray(existing.data)) return null;
    return existing.data.sha;
  } catch (err) {
    if (err.status === 404) return null;
    throw err;
  }
}

app.get('/health', (_req, res) => {
  res.json({ ok: true, service: 'github-binary-merge-connector' });
});

app.post('/github/upload-binary', requireKey, upload.single('file'), async (req, res) => {
  try {
    const body = req.body || {};
    const { owner, repo } = repoParams(body);
    const branch = body.branch || 'main';
    const path = body.path;
    const message = body.message || `Upload binary ${path}`;

    if (!path) return res.status(400).json({ ok: false, error: 'path is required' });

    let buffer;
    if (req.file?.buffer) {
      buffer = req.file.buffer;
    } else if (body.base64) {
      buffer = Buffer.from(body.base64, 'base64');
    } else {
      return res.status(400).json({ ok: false, error: 'multipart file or base64 is required' });
    }

    const sha = await getFileSha({ owner, repo, path, branch });
    const result = await octokit.repos.createOrUpdateFileContents({
      owner,
      repo,
      path,
      branch,
      message,
      sha: sha || undefined,
      content: buffer.toString('base64')
    });

    res.json({
      ok: true,
      owner,
      repo,
      branch,
      path,
      bytes: buffer.length,
      sha: result.data.content?.sha,
      commit: result.data.commit.sha,
      url: result.data.content?.html_url || result.data.commit.html_url
    });
  } catch (err) {
    res.status(err.status || 500).json({ ok: false, error: err.message, status: err.status });
  }
});

app.post('/github/delete-file', requireKey, async (req, res) => {
  try {
    const { owner, repo } = repoParams(req.body);
    const branch = req.body.branch || 'main';
    const path = req.body.path;
    const message = req.body.message || `Delete ${path}`;
    if (!path) return res.status(400).json({ ok: false, error: 'path is required' });
    const sha = await getFileSha({ owner, repo, path, branch });
    if (!sha) return res.status(404).json({ ok: false, error: 'file not found' });
    const result = await octokit.repos.deleteFile({ owner, repo, path, branch, message, sha });
    res.json({ ok: true, owner, repo, branch, path, commit: result.data.commit.sha });
  } catch (err) {
    res.status(err.status || 500).json({ ok: false, error: err.message, status: err.status });
  }
});

app.post('/github/merge-pr', requireKey, async (req, res) => {
  try {
    const { owner, repo } = repoParams(req.body);
    const pull_number = Number(req.body.pull_number);
    const merge_method = req.body.merge_method || 'merge';
    if (!pull_number) return res.status(400).json({ ok: false, error: 'pull_number is required' });
    const pr = await octokit.pulls.get({ owner, repo, pull_number });
    if (pr.data.state !== 'open') {
      return res.status(409).json({ ok: false, error: `PR is ${pr.data.state}` });
    }
    const merged = await octokit.pulls.merge({
      owner,
      repo,
      pull_number,
      merge_method,
      commit_title: req.body.commit_title,
      commit_message: req.body.commit_message
    });
    res.json({ ok: true, owner, repo, pull_number, merged: merged.data.merged, sha: merged.data.sha, message: merged.data.message });
  } catch (err) {
    res.status(err.status || 500).json({ ok: false, error: err.message, status: err.status });
  }
});

app.post('/vercel/deploy', requireKey, async (req, res) => {
  try {
    if (!env.VERCEL_TOKEN || !env.VERCEL_PROJECT_ID) {
      return res.status(400).json({ ok: false, error: 'VERCEL_TOKEN and VERCEL_PROJECT_ID are required' });
    }
    const url = new URL('https://api.vercel.com/v13/deployments');
    if (env.VERCEL_TEAM_ID) url.searchParams.set('teamId', env.VERCEL_TEAM_ID);
    const response = await fetch(url, {
      method: 'POST',
      headers: { Authorization: `Bearer ${env.VERCEL_TOKEN}`, 'Content-Type': 'application/json' },
      body: JSON.stringify({
        name: req.body.name || env.DEFAULT_REPO,
        project: env.VERCEL_PROJECT_ID,
        target: req.body.target || 'production',
        gitSource: req.body.gitSource
      })
    });
    const data = await response.json();
    res.status(response.status).json({ ok: response.ok, status: response.status, data });
  } catch (err) {
    res.status(500).json({ ok: false, error: err.message });
  }
});

const port = Number(process.env.PORT || 8787);
app.listen(port, () => console.log(`github-binary-merge-connector listening on ${port}`));
