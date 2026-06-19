import { NextResponse } from "next/server";

export const dynamic = "force-dynamic";

export async function GET() {
  return NextResponse.json({
    service: "FOCUS MASTER AI Pipeline",
    status: "online",
    version: "2.0.0",
    timestamp: new Date().toISOString(),
    engines: [
      "research", "claims", "writing", "geometry",
      "construction", "compliance", "frequency",
      "marketing", "ai_twin", "publish", "automation"
    ],
    connectors: [
      { name: "OpenAI", status: process.env.OPENAI_API_KEY ? "configured" : "fallback_mode" },
      { name: "GitHub", status: process.env.GITHUB_TOKEN ? "configured" : "not_configured" },
      { name: "Make.com", status: process.env.MAKE_WEBHOOK_URL ? "configured" : "not_configured" },
      { name: "Replit", status: process.env.REPLIT_ENDPOINT ? "configured" : "not_configured" },
    ],
    companies: ["Focus Negotium Inc", "Royal Lee Construction Solutions LLC", "Focus Records LLC"],
  });
}
