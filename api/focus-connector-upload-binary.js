const { json, readBody, requireAuth, github, getRepo, getFileSha } = require('./focus-connector-lib');

module.exports = async function handler(req, res) {
  if (req.method !== 'POST') return json(res, 405, { ok: false, error: 'POST required' });
  if (!requireAuth(req, res)) return;

  try {
    const body = await readBody(req);
    const { owner, repo } = getRepo(body);
    const branch = body.branch || 'main';
    const path = body.path;
    const message = body.message || `Upload binary ${path}`;
    if (!path) return json(res, 400, { ok: false, error: 'path is required' });
    if (!body.base64) return json(res, 400, { ok: false, error: 'base64 is required' });

    const base64 = String(body.base64).replace(/^data:.*?;base64,/, '').replace(/\s/g, '');
    const bytes = Buffer.from(base64, 'base64').length;
    if (!bytes) return json(res, 400, { ok: false, error: 'base64 decoded to zero bytes' });

    const sha = await getFileSha(owner, repo, path, branch);
    const encoded = path.split('/').map(encodeURIComponent).join('/');
    const result = await github('PUT', `/repos/${owner}/${repo}/contents/${encoded}`, {
      message,
      content: base64,
      branch,
      sha: sha || undefined
    });

    return json(res, 200, {
      ok: true,
      owner,
      repo,
      branch,
      path,
      bytes,
      replaced: Boolean(sha),
      fileSha: result.content && result.content.sha,
      commit: result.commit && result.commit.sha
    });
  } catch (err) {
    return json(res, err.status || 500, { ok: false, error: err.message, details: err.data || null });
  }
};
