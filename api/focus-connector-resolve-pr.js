const { json, readBody, requireAuth, github, getRepo } = require('./focus-connector-lib');

async function listAllPullFiles(owner, repo, pullNumber) {
  const files = [];
  for (let page = 1; page <= 10; page++) {
    const batch = await github('GET', `/repos/${owner}/${repo}/pulls/${pullNumber}/files?per_page=100&page=${page}`);
    files.push(...batch);
    if (batch.length < 100) break;
  }
  return files;
}

function flattenTree(tree) {
  const map = new Map();
  for (const item of tree.tree || []) map.set(item.path, item);
  return map;
}

module.exports = async function handler(req, res) {
  if (req.method !== 'POST') return json(res, 405, { ok: false, error: 'POST required' });
  if (!requireAuth(req, res)) return;

  try {
    const body = await readBody(req);
    const { owner, repo } = getRepo(body);
    const pullNumber = Number(body.pull_number || body.pr || 7);
    const baseBranch = body.base || 'main';
    const replacementBranch = body.branch || `focus-pr-${pullNumber}-resolved-${Date.now()}`;
    const mergeMethod = body.merge_method || 'merge';

    const pr = await github('GET', `/repos/${owner}/${repo}/pulls/${pullNumber}`);
    const baseRef = await github('GET', `/repos/${owner}/${repo}/git/ref/heads/${encodeURIComponent(baseBranch)}`);
    const baseSha = baseRef.object.sha;
    const baseCommit = await github('GET', `/repos/${owner}/${repo}/git/commits/${baseSha}`);
    const baseTreeSha = baseCommit.tree.sha;

    const prTree = await github('GET', `/repos/${owner}/${repo}/git/trees/${pr.head.sha}?recursive=1`);
    const prTreeMap = flattenTree(prTree);
    const files = await listAllPullFiles(owner, repo, pullNumber);

    const tree = [];
    for (const file of files) {
      if (file.status === 'removed') {
        tree.push({ path: file.filename, mode: '100644', type: 'blob', sha: null });
        continue;
      }
      const item = prTreeMap.get(file.filename);
      if (!item || item.type !== 'blob' || !item.sha) continue;
      tree.push({ path: file.filename, mode: item.mode || '100644', type: 'blob', sha: item.sha });
    }

    if (!tree.length) return json(res, 400, { ok: false, error: 'No changed files found to rebuild' });

    const newTree = await github('POST', `/repos/${owner}/${repo}/git/trees`, { base_tree: baseTreeSha, tree });
    const newCommit = await github('POST', `/repos/${owner}/${repo}/git/commits`, {
      message: body.commit_message || `Resolve PR #${pullNumber} by applying branch changes onto ${baseBranch}`,
      tree: newTree.sha,
      parents: [baseSha]
    });

    try {
      await github('POST', `/repos/${owner}/${repo}/git/refs`, {
        ref: `refs/heads/${replacementBranch}`,
        sha: newCommit.sha
      });
    } catch (err) {
      if (err.status !== 422) throw err;
      await github('PATCH', `/repos/${owner}/${repo}/git/refs/heads/${encodeURIComponent(replacementBranch)}`, {
        sha: newCommit.sha,
        force: true
      });
    }

    const replacementPr = await github('POST', `/repos/${owner}/${repo}/pulls`, {
      title: body.title || `Resolved: ${pr.title}`,
      head: replacementBranch,
      base: baseBranch,
      body: body.body || `Rebuilds PR #${pullNumber} on top of the current ${baseBranch} branch to bypass merge conflicts while preserving the PR changed files.`
    });

    const merge = await github('PUT', `/repos/${owner}/${repo}/pulls/${replacementPr.number}/merge`, {
      merge_method: mergeMethod,
      commit_title: body.merge_title || `Merge resolved PR #${pullNumber}`,
      commit_message: body.merge_message || `Merged clean replacement PR #${replacementPr.number}.`
    });

    return json(res, 200, {
      ok: true,
      original_pull_number: pullNumber,
      replacement_pull_number: replacementPr.number,
      replacement_branch: replacementBranch,
      changed_files: files.length,
      commit: newCommit.sha,
      merged: merge.merged,
      merge_sha: merge.sha,
      message: merge.message
    });
  } catch (err) {
    return json(res, err.status || 500, { ok: false, error: err.message, details: err.data || null });
  }
};
