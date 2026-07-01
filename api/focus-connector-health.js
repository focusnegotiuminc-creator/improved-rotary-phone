module.exports = async function handler(req, res) {
  res.setHeader('content-type', 'application/json');
  res.status(200).json({
    ok: true,
    service: 'github-binary-merge-connector',
    routes: [
      '/health',
      '/github/upload-binary',
      '/github/delete-file',
      '/github/merge-pr'
    ],
    configured: {
      githubToken: Boolean(process.env.GITHUB_TOKEN),
      connectorKey: Boolean(process.env.CONNECTOR_API_KEY),
      defaultOwner: process.env.DEFAULT_OWNER || 'focusnegotiuminc-creator',
      defaultRepo: process.env.DEFAULT_REPO || 'improved-rotary-phone'
    }
  });
};
