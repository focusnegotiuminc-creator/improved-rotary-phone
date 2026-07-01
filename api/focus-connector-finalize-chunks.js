const { json, readBody, requireAuth, github, getRepo, getFileSha } = require('./focus-connector-lib');

function safeName(value) {
  return String(value || '').replace(/[^a-zA-Z0-9._-]/g, '-').slice(0, 120);
}

async function readTextFile(owner, repo, path, branch) {
  const encoded = path.split('/').map(encodeURIComponent).join('/');
  const data = await github('GET', `/repos/${owner}/${repo}/contents/${encoded}?ref=${encodeURIComponent(branch)}`);
  return Buffer.from(String(data.content || '').replace(/\s/g, ''), 'base64').toString('utf8');
}

module.exports = async function handler(req, res) {
  if (req.method !== 'POST') return json(res, 405, { ok: false, error: 'POST required' });
  if (!requireAuth(req, res)) return;
  try {
    const body = await readBody(req);
    const { owner, repo } = getRepo(body);
    const branch = body.branch || 'main';
    const uploadId = safeName(body.uploadId);
    const targetPath = body.targetPath;
    const total = Number(body.total);
    const message = body.message || `Finalize upload ${targetPath}`;
    if (!uploadId || !targetPath || !total) return json(res, 400, { ok: false, error: 'uploadId, targetPath, and total are required' });

    let content = '';
    for (let i = 0; i < total; i++) {
      const chunkPath = `.focus-tmp/${uploadId}/${String(i).padStart(5, '0')}.b64`;
      content += await readTextFile(owner, repo, chunkPath, branch);
    }
    const bytes = Buffer.from(content, 'base64').length;
    if (!bytes) return json(res, 400, { ok: false, error: 'final content decoded to zero bytes' });

    const sha = await getFileSha(owner, repo, targetPath, branch);
    const encoded = targetPath.split('/').map(encodeURIComponent).join('/');
    const result = await github('PUT', `/repos/${owner}/${repo}/contents/${encoded}`, { message, content, branch, sha: sha || undefined });

    return json(res, 200, { ok: true, branch, targetPath, bytes, replaced: Boolean(sha), fileSha: result.content && result.content.sha, commit: result.commit && result.commit.sha });
  } catch (err) {
    return json(res, err.status || 500, { ok: false, error: err.message, details: err.data || null });
  }
};
