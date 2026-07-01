const { json, readBody, requireAuth, github, getRepo, getFileSha } = require('./focus-connector-lib');

module.exports = async function handler(req, res) {
  if (req.method !== 'POST') return json(res, 405, { ok: false, error: 'POST required' });
  if (!requireAuth(req, res)) return;

  try {
    const body = await readBody(req);
    const { owner, repo } = getRepo(body);
    const branch = body.branch || 'main';
    const path = body.path;
    const message = body.message || `Delete ${path}`;
    if (!path) return json(res, 400, { ok: false, error: 'path is required' });

    const sha = await getFileSha(owner, repo, path, branch);
    if (!sha) return json(res, 404, { ok: false, error: 'file not found', path, branch });

    const encoded = path.split('/').map(encodeURIComponent).join('/');
    const result = await github('DELETE', `/repos/${owner}/${repo}/contents/${encoded}`, {
      message,
      sha,
      branch
    });

    return json(res, 200, {
      ok: true,
      owner,
      repo,
      branch,
      path,
      commit: result.commit && result.commit.sha
    });
  } catch (err) {
    return json(res, err.status || 500, { ok: false, error: err.message, details: err.data || null });
  }
};
