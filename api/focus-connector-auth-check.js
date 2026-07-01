const { json, requireAuth } = require('./focus-connector-lib');

module.exports = async function handler(req, res) {
  if (!requireAuth(req, res)) return;
  return json(res, 200, {
    ok: true,
    authorized: true,
    service: 'github-binary-merge-connector'
  });
};
