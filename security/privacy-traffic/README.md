# Private Browsing + Traffic Visibility Playbook

Purpose: observe traffic from your own machine/app testing environment so you can understand where app/browser traffic goes and identify unexpected monitoring, installs, or interference.

## Boundaries

Use only on devices, browsers, domains, and accounts you own or are authorized to test. Do not intercept other people's traffic or credentials.

## Practical setup

1. Use a dedicated browser profile for Flux & Crave / Focus testing.
2. Use a reputable VPN only when you need network privacy from the local network/ISP; remember the VPN provider can see metadata.
3. Use browser DevTools Network tab for web-app requests.
4. Use OS-level checks for active connections and DNS cache.
5. For deeper lab testing, use Wireshark or mitmproxy only on your own test device with explicit trust/certificate setup.
6. Keep store-account, social-account, and banking sessions out of packet-capture/decryption experiments unless absolutely necessary.

## What to watch

- Unexpected third-party domains.
- Calls to unknown analytics/ad networks.
- Repeated failed certificate/DNS attempts.
- Installers, browser extensions, or startup services you did not authorize.
- Traffic leaving when no app/browser action is happening.

## Recommended reporting

Capture:

- Timestamp.
- App/browser action performed.
- Destination host/IP.
- Process name.
- Whether request is expected.
- Follow-up action: allow, block, investigate, remove extension/app.
