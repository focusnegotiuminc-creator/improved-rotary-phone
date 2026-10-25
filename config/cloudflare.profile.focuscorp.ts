export const focusCorpCloudflareProfile = {
  id: "focuscorp",
  ownerEmail: "theFocusCorp@proton.me",
  supportedEmails: [
    "theFocusCorp@proton.me",
    "Focusnegotiuminc@gmail.com",
    "fninc@proton.me",
    "rlcsolutions@proton.me",
  ],
  accountEnv: "CLOUDFLARE_ACCOUNT_ID",
  zoneEnv: "CLOUDFLARE_ZONE_ID",
  projectNameEnv: "CLOUDFLARE_PROJECT_NAME",
  deploymentTarget: "cloudflare-workers-pages",
  fallbackTarget: "vercel",
  requiredEnv: [
    "CLOUDFLARE_API_TOKEN",
    "CLOUDFLARE_ACCOUNT_ID",
    "CLOUDFLARE_ZONE_ID",
    "CLOUDFLARE_PROJECT_NAME",
    "CLOUDFLARE_KV_NAMESPACE_ID",
    "CLOUDFLARE_D1_DATABASE_ID",
    "CLOUDFLARE_R2_BUCKET",
  ],
} as const;

export type FocusCorpCloudflareProfile = typeof focusCorpCloudflareProfile;
