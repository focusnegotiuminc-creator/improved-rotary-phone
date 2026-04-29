# Tailscale Hardening Review

Generated: 2026-04-28T23:20:00+00:00

## Current posture

- Tailnet device: `msi`
- Tailnet URL: `https://msi.tail894763.ts.net`
- Private console origin: `http://127.0.0.1:8000`
- Tailscale service: running
- MagicDNS: enabled
- Tailnet Lock: enabled
- Trusted signing keys:
  - `tlpub:43db145f6ab8e366b6caa2ac9a114c2f2a478f7526174810479199d181f1ee43` (MSI)
  - `tlpub:8713bbc6eea977df1b6acdd7b8b4dc0c97304fe1d51695f4069ff04dcb37c6c0` (iPhone `masteroftime`)

## Findings addressed

1. Public Funnel exposure was removed from the private console lane
2. The private console now stays on a tailnet-only `tailscale serve` path
3. The MSI no longer accepts peer-advertised routes
4. Tailnet Lock is enabled and healthy
5. A second trusted signing node was added for recovery redundancy

## Applied changes

- Bound the Flask private console to `127.0.0.1` by default instead of `0.0.0.0`
- Disabled public Funnel exposure
- Kept tailnet-only `tailscale serve` for `https://msi.tail894763.ts.net/`
- Set Tailscale to unattended mode on Windows
- Disabled accepting peer-advertised routes on this MSI
- Added the iPhone `masteroftime` as a second trusted Tailnet Lock signer

## Verified after hardening

- `tailscale serve status` shows `tailnet only`
- `tailscale funnel status` shows no public Funnel exposure for the console
- `tailscale debug prefs` shows:
  - `RouteAll: false`
  - `RunSSH: false`
  - `RunWebClient: false`
  - `ForceDaemon: true`
- Private console health endpoint responds at:
  - `http://127.0.0.1:8000/health`
  - `https://msi.tail894763.ts.net/health`
- Tailnet Lock reports `Enabled: true`
- Tailnet Lock trusted key count is `2`
- `tailscale lock log` records the `add-key` event for the iPhone trusted signer
- `tailscale ping masteroftime.tail894763.ts.net` succeeds

## Device access policy review

- Current devices visible in the tailnet include:
  - `msi`
  - `masteroftime` (iPhone)
  - `moto-g-64gb---2025-xt2513v`
  - two offline MacBook nodes
- This pass intentionally scoped the private console lane to the MSI and iPhone only
- Recommended admin-policy follow-up:
  - restrict MSI private-console access to your personal devices only
  - remove or expire stale devices that no longer need tailnet access
  - avoid broad owner-wide access if a narrower ACL or tag policy is available

## Subnet and Funnel design review

- No subnet routes are being advertised from this MSI
- This machine remains a device endpoint, not a subnet router
- Funnel is not appropriate for the private console because it would publish the node on the public internet
- Tailnet-only Serve is the correct design for MSI-to-iPhone private console access

## Least-privilege exposure review

- Keep:
  - `RunSSH: false`
  - `RunWebClient: false`
  - `RouteAll: false`
- Keep the private console bound to loopback and expose it only through Tailscale Serve
- Do not turn on `shields-up` for this use case because it would block the incoming tailnet access you want

## Recovery posture

- Tailnet Lock disablement material is stored only in the private secret store and GitHub repo secrets
- The MSI remains a trusted signing node
- The iPhone now provides second-signer redundancy for tailnet recovery and trusted-key changes

## Operational helper

- Use [start_private_console_tailscale.ps1](/G:/My%20Drive/FOCUS_MASTER_AI_live/scripts/start_private_console_tailscale.ps1) to relaunch the private console and reapply the hardened Tailscale lane if needed
