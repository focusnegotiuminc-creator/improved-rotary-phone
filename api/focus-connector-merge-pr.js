const { json, readBody, requireAuth, github, getRepo } = require('./focus-connector-lib');

module.exports = async function handler(req, res) {
  if (req.method !== 'POST') return json(res, 405, { ok: false, error: 'POST required' });
  if (!requireAuth(req, res)) return;

  try {
    const body = await readBody(req);
    const { owner, repo } = getRepo(body);
    const pullNumber = Number(body.pull_number || body.pr || body.number);
    const mergeMethod = body.merge_method || 'merge';
    if (!pullNumber) return json(res, 400, { ok: false, error: 'pull_number is required' });
    if (!['merge', 'squash', 'rebase'].includes(mergeMethod)) {
      return json(res, 400, { ok: false, error: 'merge_method must be merge, squash, or rebase' });
    }

    const result = await github('PUT', `/repos/${owner}/${repo}/pulls/${pullNumber}/merge`, {
      merge_method: mergeMethod,
      commit_title: body.commit_title,
      commit_message: body.commit_message
    });

    return json(res, 200, {
      ok: true,
      owner,
      repo,
      pull_number: pullNumber,
      merged: result.merged,
      sha: result.sha,
      message: result.message
    });
  } catch (err) {
    return json(res, err.status || 500, { ok: false, error: err.message, details: err.data || null });
  }
};
