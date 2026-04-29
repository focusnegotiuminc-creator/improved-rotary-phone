(() => {
  const TARGET_URL = "https://msi.tail894763.ts.net/private-console";
  const openLink = document.getElementById("open-console");
  const copyButton = document.getElementById("copy-link");
  const statusLine = document.getElementById("status-line");
  const statusDetail = document.getElementById("status-detail");
  const directLink = document.getElementById("direct-link");

  if (openLink) {
    openLink.setAttribute("href", TARGET_URL);
  }

  if (directLink) {
    directLink.textContent = TARGET_URL;
  }

  const isiPhone = /iPhone|iPad|iPod/i.test(navigator.userAgent);
  const inStandalone = window.matchMedia?.("(display-mode: standalone)")?.matches || window.navigator.standalone;

  function setStatus(title, detail) {
    if (statusLine) statusLine.textContent = title;
    if (statusDetail) statusDetail.textContent = detail;
  }

  async function copyLink() {
    try {
      await navigator.clipboard.writeText(TARGET_URL);
      setStatus("Direct link copied", "Paste it anywhere on iPhone if you want the raw tailnet URL too.");
    } catch (_error) {
      setStatus("Copy didn’t complete", "Use the direct path shown below and copy it manually if needed.");
    }
  }

  function handoff() {
    setStatus("Opening private console", "Handing off to the Tailscale route on your MSI.");
    window.location.href = TARGET_URL;
  }

  if (copyButton) {
    copyButton.addEventListener("click", copyLink);
  }

  if (isiPhone && inStandalone) {
    setStatus("Home Screen launcher ready", "This shortcut is installed. Opening the private console now.");
    window.setTimeout(handoff, 450);
    return;
  }

  if (isiPhone) {
    setStatus(
      "iPhone detected",
      "Tap Open private console now, or add this page to your Home Screen for one-tap use later."
    );
    return;
  }

  setStatus(
    "Launcher is live",
    "This page is optimized for iPhone. Use the Home Screen install flow there for one-tap opening."
  );
})();
