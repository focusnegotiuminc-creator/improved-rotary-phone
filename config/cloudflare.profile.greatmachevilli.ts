export const greatMachevilliCloudflareProfile = {
  id: "greatmachevilli",
  ownerEmail: "thegreatmachevilli@icloud.com",
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
  ],
} as const;

export type GreatMachevilliCloudflareProfile = typeof greatMachevilliCloudflareProfile;
