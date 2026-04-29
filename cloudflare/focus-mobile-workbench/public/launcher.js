(() => {
  const REMOTE_URL = "https://focus-mobile-workbench.thefocuscorp.workers.dev/app";
  const TAILNET_URL = "https://msi.tail894763.ts.net/private-console";
  const remoteLink = document.getElementById("remote-link");
  const openLink = document.getElementById("open-console");
  const openRemote = document.getElementById("open-remote");
  const copyButton = document.getElementById("copy-link");
  const statusLine = document.getElementById("status-line");
  const statusDetail = document.getElementById("status-detail");
  const directLink = document.getElementById("direct-link");

  if (openRemote) {
    openRemote.setAttribute("href", REMOTE_URL);
  }

  if (openLink) {
    openLink.setAttribute("href", TAILNET_URL);
  }

  if (remoteLink) {
    remoteLink.textContent = REMOTE_URL;
  }

  if (directLink) {
    directLink.textContent = TAILNET_URL;
  }

  const isiPhone = /iPhone|iPad|iPod/i.test(navigator.userAgent);
  const inStandalone = window.matchMedia?.("(display-mode: standalone)")?.matches || window.navigator.standalone;

  function setStatus(title, detail) {
    if (statusLine) statusLine.textContent = title;
    if (statusDetail) statusDetail.textContent = detail;
  }

  async function copyLink() {
    try {
      await navigator.clipboard.writeText(REMOTE_URL);
      setStatus("Remote link copied", "Paste it anywhere on iPhone if you want the public workbench path too.");
    } catch (_error) {
      setStatus("Copy didn’t complete", "Use the remote path shown below and copy it manually if needed.");
    }
  }

  function handoff() {
    setStatus("Opening remote workbench", "Handing off to the Cloudflare-hosted private console path.");
    window.location.href = REMOTE_URL;
  }

  if (copyButton) {
    copyButton.addEventListener("click", copyLink);
  }

  if (isiPhone && inStandalone) {
    setStatus("Home Screen launcher ready", "This shortcut is installed. Opening the remote workbench now.");
    window.setTimeout(handoff, 450);
    return;
  }

  if (isiPhone) {
    setStatus(
      "iPhone detected",
      "Tap Open remote workbench now, or add this page to your Home Screen for one-tap use later."
    );
    return;
  }

  setStatus(
    "Launcher is live",
    "This page is optimized for iPhone. Use the Home Screen install flow there for one-tap opening."
  );
})();
