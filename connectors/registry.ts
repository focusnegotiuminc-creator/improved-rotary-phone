declare const process: { env: Record<string, string | undefined> };
import { CloudflareConnector } from "./cloudflare";

export const connectorRegistry = {
  cloudflare: new CloudflareConnector(),
  github: { id: "github", requiredEnv: ["GITHUB_TOKEN"] },
  googleDrive: { id: "google-drive", requiredEnv: ["GOOGLE_DRIVE_CLIENT_ID", "GOOGLE_DRIVE_CLIENT_SECRET"] },
  vercel: { id: "vercel", requiredEnv: ["VERCEL_TOKEN"] },
  gmail: { id: "gmail", requiredEnv: ["GMAIL_CLIENT_ID", "GMAIL_CLIENT_SECRET"] },
  calendar: { id: "calendar", requiredEnv: ["GOOGLE_CALENDAR_CLIENT_ID", "GOOGLE_CALENDAR_CLIENT_SECRET"] },
} as const;

export type ConnectorId = keyof typeof connectorRegistry;

export function connectorStatus(env: Record<string, string | undefined> = process.env) {
  return Object.entries(connectorRegistry).map(([id, connector]) => {
    const requiredEnv = "requiredEnv" in connector ? connector.requiredEnv : ["CLOUDFLARE_API_TOKEN"];
    const missing = requiredEnv.filter((key) => !env[key]);
    return { id, ok: missing.length === 0, missing };
  });
}
