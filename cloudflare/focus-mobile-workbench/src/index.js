import { stacks, templates, toolBridges } from "./catalog.js";

const COOKIE_NAME = "focus_workbench_session";

function json(data, status = 200, headers = {}) {
  return new Response(JSON.stringify(data), {
    status,
    headers: {
      "content-type": "application/json; charset=utf-8",
      "cache-control": "no-store",
      ...headers,
    },
  });
}

function readCookies(request) {
  return Object.fromEntries(
    (request.headers.get("cookie") || "")
      .split(";")
      .map((part) => part.trim())
      .filter(Boolean)
      .map((part) => {
        const [key, ...rest] = part.split("=");
        return [key, rest.join("=")];
      })
  );
}

function toBase64Url(bytes) {
  const text = String.fromCharCode(...bytes);
  return btoa(text).replace(/\+/g, "-").replace(/\//g, "_").replace(/=+$/g, "");
}

function fromBase64Url(value) {
  const normalized = value.replace(/-/g, "+").replace(/_/g, "/");
  const padded = normalized + "=".repeat((4 - (normalized.length % 4 || 4)) % 4);
  return Uint8Array.from(atob(padded), (char) => char.charCodeAt(0));
}

async function sha256(text) {
  return new Uint8Array(await crypto.subtle.digest("SHA-256", new TextEncoder().encode(text)));
}

function safeEqual(a, b) {
  if (a.length !== b.length) return false;
  let diff = 0;
  for (let index = 0; index < a.length; index += 1) {
    diff |= a[index] ^ b[index];
  }
  return diff === 0;
}

async function sign(payload, secret) {
  const key = await crypto.subtle.importKey(
    "raw",
    new TextEncoder().encode(secret),
    { name: "HMAC", hash: "SHA-256" },
    false,
    ["sign"]
  );
  const signature = await crypto.subtle.sign("HMAC", key, new TextEncoder().encode(payload));
  return toBase64Url(new Uint8Array(signature));
}

async function verifyPassword(password, env) {
  const expected = env.PRIVATE_APP_PASSWORD || "";
  if (!expected) return false;
  const [providedHash, expectedHash] = await Promise.all([sha256(password), sha256(expected)]);
  return safeEqual(providedHash, expectedHash);
}

async function createSessionCookie(env) {
  const secret = env.APP_SESSION_SECRET || env.PRIVATE_APP_PASSWORD || "focus-mobile-workbench";
  const payload = JSON.stringify({
    ts: Date.now(),
    nonce: crypto.randomUUID(),
  });
  const encoded = toBase64Url(new TextEncoder().encode(payload));
  const signature = await sign(encoded, secret);
  return `${encoded}.${signature}`;
}

async function hasValidSession(request, env) {
  const token = readCookies(request)[COOKIE_NAME];
  if (!token) return false;
  const [payload, signature] = token.split(".");
  if (!payload || !signature) return false;
  const secret = env.APP_SESSION_SECRET || env.PRIVATE_APP_PASSWORD || "focus-mobile-workbench";
  const expected = await sign(payload, secret);
  return safeEqual(new TextEncoder().encode(signature), new TextEncoder().encode(expected));
}

function chooseStack(stackId) {
  return stacks.find((stack) => stack.id === stackId) || stacks[0];
}

function buildFallbackRun(body) {
  const stack = chooseStack(body.stackId);
  const selectedTools = (body.toolIds || [])
    .map((toolId) => toolBridges.find((tool) => tool.id === toolId))
    .filter(Boolean);

  const runbook = [
    `# ${stack.label}`,
    "",
    `Mission: ${body.prompt || "No mission entered."}`,
    "",
    "## Objective",
    stack.objective,
    "",
    "## Engine sequence",
    ...stack.engines.map((engine, index) => `${index + 1}. ${engine}`),
    "",
    "## Selected bridges",
    ...(selectedTools.length
      ? selectedTools.map((tool) => `- ${tool.label}: ${tool.role}`)
      : ["- No bridge cards selected; use the stack defaults."]),
    "",
    "## Operator next actions",
    "- Review the mission wording and confirm the stack is appropriate.",
    "- Attach any links, files, or prompt context before the next run.",
    "- Use this output as the briefing note for the next execution step.",
    "",
    "## Workspace note",
    body.documentText ? body.documentText.slice(0, 900) : "No active workspace document was sent with this run.",
  ].join("\n");

  return {
    id: crypto.randomUUID(),
    createdAt: new Date().toISOString(),
    mode: "fallback",
    provider: "fallback",
    model: "deterministic-runbook",
    stack,
    output: runbook,
  };
}

function outputTextFromResponses(data) {
  if (typeof data.output_text === "string" && data.output_text.trim()) {
    return data.output_text;
  }
  const blocks = [];
  for (const item of data.output || []) {
    for (const content of item.content || []) {
      if (content.type === "output_text" && content.text) {
        blocks.push(content.text);
      }
    }
  }
  return blocks.join("\n\n").trim();
}

async function runWithOpenAI(body, env) {
  const stack = chooseStack(body.stackId);
  const prompt = [
    `You are Focus Mobile Workbench, a private operator assistant for internal business execution.`,
    `Stay within authorized business operations and do not help with policy bypass, payroll tampering, credential exposure, or public-site leakage of private systems.`,
    `Stack: ${stack.label}`,
    `Objective: ${stack.objective}`,
    `Engines: ${stack.engines.join(", ")}`,
    "",
    `Mission: ${body.prompt || "No mission entered."}`,
    "",
    `Workspace document:`,
    body.documentText || "No workspace document attached.",
  ].join("\n");

  const response = await fetch("https://api.openai.com/v1/responses", {
    method: "POST",
    headers: {
      "content-type": "application/json",
      authorization: `Bearer ${env.OPENAI_API_KEY}`,
    },
    body: JSON.stringify({
      model: env.OPENAI_MODEL || env.DEFAULT_OPENAI_MODEL || "gpt-4.1-mini",
      input: prompt,
    }),
  });

  if (!response.ok) {
    const errorText = await response.text();
    throw new Error(`OpenAI run failed: ${response.status} ${errorText}`);
  }

  const data = await response.json();
  return {
    id: crypto.randomUUID(),
    createdAt: new Date().toISOString(),
    mode: "live",
    provider: "openai",
    model: env.OPENAI_MODEL || env.DEFAULT_OPENAI_MODEL || "gpt-4.1-mini",
    stack,
    output: outputTextFromResponses(data) || "The model returned an empty response.",
  };
}

async function handleLogin(request, env) {
  const body = await request.json().catch(() => ({}));
  if (!(await verifyPassword(body.password || "", env))) {
    return json({ ok: false, error: "Invalid passphrase." }, 401);
  }
  const token = await createSessionCookie(env);
  return json(
    { ok: true },
    200,
    {
      "set-cookie": `${COOKIE_NAME}=${token}; HttpOnly; Secure; SameSite=Strict; Path=/; Max-Age=43200`,
    }
  );
}

function handleLogout() {
  return json(
    { ok: true },
    200,
    {
      "set-cookie": `${COOKIE_NAME}=; HttpOnly; Secure; SameSite=Strict; Path=/; Max-Age=0`,
    }
  );
}

async function handleApi(request, env) {
  const url = new URL(request.url);

  if (url.pathname === "/api/session" && request.method === "POST") {
    return handleLogin(request, env);
  }

  if (url.pathname === "/api/session" && request.method === "DELETE") {
    return handleLogout();
  }

  if (!(await hasValidSession(request, env))) {
    return json({ ok: false, error: "Authentication required." }, 401);
  }

  if (url.pathname === "/api/status") {
    return json({
      ok: true,
      app: {
        name: env.APP_NAME || "Focus Mobile Workbench",
        version: "0.1.0",
        posture: "private",
      },
      providers: [
        { id: "fallback", label: "Fallback Planner", configured: true },
        { id: "openai", label: "OpenAI", configured: Boolean(env.OPENAI_API_KEY) },
      ],
      stacks,
      toolBridges,
      templates,
    });
  }

  if (url.pathname === "/api/run" && request.method === "POST") {
    const body = await request.json().catch(() => ({}));
    if (!String(body.prompt || "").trim()) {
      return json({ ok: false, error: "A mission prompt is required." }, 400);
    }

    try {
      const run =
        body.provider === "openai" && env.OPENAI_API_KEY
          ? await runWithOpenAI(body, env)
          : buildFallbackRun(body);
      return json({ ok: true, run });
    } catch (error) {
      return json({ ok: false, error: error instanceof Error ? error.message : "Run failed." }, 500);
    }
  }

  return json({ ok: false, error: "Not found." }, 404);
}

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    if (url.pathname.startsWith("/api/")) {
      return handleApi(request, env);
    }

    if (url.pathname === "/" || url.pathname === "/app") {
      return env.ASSETS.fetch(new Request(new URL("/index.html", request.url), request));
    }

    return env.ASSETS.fetch(request);
  },
};
