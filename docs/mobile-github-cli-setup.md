# Mobile GitHub Setup Guide

Purpose: finish PR #7 from iPhone or mobile browser, replace the pointer audio files with real MP3 binaries, merge the PR, and deploy.

## Recommended mobile route

Use GitHub Codespaces from Safari because it gives you a real Linux shell in the browser. Open the repository, tap Code, then Codespaces, then start a codespace.

## Login and clone

Run these in the Codespaces terminal or another trusted shell:

    gh auth login
    gh auth status
    gh auth setup-git
    git clone https://github.com/focusnegotiuminc-creator/improved-rotary-phone.git
    cd improved-rotary-phone
    git fetch origin focus-command-center-drive-import-2026-06-28
    git checkout focus-command-center-drive-import-2026-06-28

## Replace Flux and Crave audio files

Final audio paths:

    focus_ai/site/flux-crave/assets/audio/change-your-life-money.mp3
    focus_ai/site/flux-crave/assets/audio/be-your-menu.mp3

Remove known pointer files and add the real files:

    mkdir -p focus_ai/site/flux-crave/assets/audio
    git rm -f focus_ai/site/flux-crave/assets/flux-crave/audio/change-your-life-money.mp3 || true
    git rm -f focus_ai/site/flux-crave/assets/audio/change-your-life-money-real.mp3 || true

Then upload or copy the real MP3 files into the final audio folder using Codespaces upload, Working Copy, iCloud Drive, or the GitHub web editor.

Quality check:

    ls -lh focus_ai/site/flux-crave/assets/audio
    file focus_ai/site/flux-crave/assets/audio/*.mp3

Expected file sizes: roughly 6.6 MB for change-your-life-money and 12 MB for be-your-menu. If a file is only a few bytes, it is still a pointer file.

Commit and push:

    git add focus_ai/site/flux-crave/assets/audio
    git commit -m "Upload real Flux Crave MP3 binaries"
    git push origin focus-command-center-drive-import-2026-06-28

## Merge PR #7

    gh pr view 7 --json number,title,state,mergeable,reviewDecision,url --jq .
    gh pr checks 7 || true
    gh pr merge 7 --merge --delete-branch

## Review PR #6 before merging

    gh pr view 6 --json number,title,state,mergeable,reviewDecision,url --jq .
    gh pr diff 6

Merge PR #6 only after confirming it does not overwrite the new Focus Corp root homepage.

## Deploy

If Vercel is connected to GitHub, merging into main should deploy. Manual fallback:

    npm i -g vercel@latest
    vercel --prod

## GitHub UI only

Open GitHub app or Safari, go to the repository, open Pull Requests, open PR #7, check Files changed, tap Merge pull request, then delete branch.
