const GITHUB_API = 'https://api.github.com';

function json(res, status, body) {
  res.setHeader('content-type', 'application/json');
  res.status(status).json(body);
}

function getRepo(body = {}) {
  return {
    owner: body.owner || process.env.DEFAULT_OWNER || 'focusnegotiuminc-creator',
    repo: body.repo || process.env.DEFAULT_REPO || 'improved-rotary-phone'
  };
}

async function readBody(req) {
  if (req.body && typeof req.body === 'object') return req.body;
  if (typeof req.body === 'string' && req.body.trim()) return JSON.parse(req.body);
  const chunks = [];
  for await (const chunk of req) chunks.push(Buffer.from(chunk));
  const text = Buffer.concat(chunks).toString('utf8');
  return text ? JSON.parse(text) : {};
}

function requireAuth(req, res) {
  const expected = process.env.CONNECTOR_API_KEY;
  if (!expected) {
    json(res, 503, { ok: false, error: 'CONNECTOR_API_KEY is not configured on the deployment' });
    return false;
  }
  const received = req.headers['x-focus-connector-key'];
  if (received !== expected) {
    json(res, 401, { ok: false, error: 'Unauthorized connector request' });
    return false;
  }
  return true;
}

async function github(method, path, body) {
  const token = process.env.GITHUB_TOKEN;
  if (!token) throw new Error('GITHUB_TOKEN is not configured on the deployment');
  const response = await fetch(`${GITHUB_API}${path}`, {
    method,
    headers: {
      authorization: `Bearer ${token}`,
      accept: 'application/vnd.github+json',
      'content-type': 'application/json',
      'x-github-api-version': '2022-11-28',
      'user-agent': 'focus-github-connector'
    },
    body: body ? JSON.stringify(body) : undefined
  });
  const data = await response.json().catch(() => ({}));
  if (!response.ok) {
    const message = data.message || `GitHub request failed with ${response.status}`;
    const error = new Error(message);
    error.status = response.status;
    error.data = data;
    throw error;
  }
  return data;
}

async function getFileSha(owner, repo, filePath, branch) {
  try {
    const encoded = filePath.split('/').map(encodeURIComponent).join('/');
    const data = await github('GET', `/repos/${owner}/${repo}/contents/${encoded}?ref=${encodeURIComponent(branch)}`);
    return data.sha || null;
  } catch (err) {
    if (err.status === 404) return null;
    throw err;
  }
}

module.exports = { json, readBody, requireAuth, github, getRepo, getFileSha };
