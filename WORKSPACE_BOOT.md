## FOCUS Master AI Workspace Boot

Primary workspace:

- `G:\My Drive\FOCUS_MASTER_AI_live`

How to use this workspace from another Codex/Desktop session:

1. Sign into the same Google account in Google Drive Desktop.
2. Make sure `G:\My Drive\FOCUS_MASTER_AI_live` is mounted on that machine.
3. Open Codex/Desktop and choose this folder as the workspace.
4. Work from this repo directly instead of creating a new copy.

Secrets/runtime:

- Repo-local secrets live in `.secrets/focus_master.env`
- The app runtime already checks this file automatically
- Do not paste API keys or passwords into chat

Recommended workflow:

- Pull latest changes first: `git pull`
- Work normally in this folder
- Commit and push changes back to GitHub when finished

Important:

- A chat alone cannot access your files unless the Codex app is opened on a device that has this Drive mounted.
- Google Drive gives file access; GitHub gives version history; both should be kept.
