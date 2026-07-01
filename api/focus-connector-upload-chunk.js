const { json, readBody, requireAuth, github, getRepo, getFileSha } = require('./focus-connector-lib');

function safeName(value) {
  return String(value || '').replace(/[^a-zA-Z0-9._-]/g, '-').slice(0, 120);
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
    const index = Number(body.index);
    const total = Number(body.total);
    const base64 = String(body.base64 || '').replace(/\s/g, '');
    if (!uploadId || !targetPath || !Number.isInteger(index) || !total || !base64) {
      return json(res, 400, { ok: false, error: 'uploadId, targetPath, index, total, and base64 are required' });
    }
    const chunkPath = `.focus-tmp/${uploadId}/${String(index).padStart(5, '0')}.b64`;
    const sha = await getFileSha(owner, repo, chunkPath, branch);
    const encoded = chunkPath.split('/').map(encodeURIComponent).join('/');
    const result = await github('PUT', `/repos/${owner}/${repo}/contents/${encoded}`, {
      message: `Store upload chunk ${index + 1} of ${total}`,
      content: Buffer.from(base64, 'utf8').toString('base64'),
      branch,
      sha: sha || undefined
    });
    return json(res, 200, { ok: true, branch, targetPath, uploadId, index, total, bytes: Buffer.from(base64, 'base64').length, chunkPath, commit: result.commit && result.commit.sha });
  } catch (err) {
    return json(res, err.status || 500, { ok: false, error: err.message, details: err.data || null });
  }
};
