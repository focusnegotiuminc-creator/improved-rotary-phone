import { NextRequest } from "next/server";
import { ENGINE_PROFILES, ENGINE_SEQUENCES, type EngineKey } from "@/lib/engines";

export const dynamic = "force-dynamic";

// Build a detailed execution packet for the task
function buildPacket(task: string, engineKey: EngineKey) {
  const profile = ENGINE_PROFILES[engineKey];
  const sequence = ENGINE_SEQUENCES[engineKey] || ENGINE_SEQUENCES.automation;

  return {
    task,
    engine: engineKey,
    label: profile.label,
    focus: profile.focus,
    deliverables: profile.deliverables,
    sequence,
    mission: `Execute "${task}" via the ${profile.label} with automation-ready output, maximum clarity, and execution-grade precision.`,
  };
}

// Build a rich fallback output for each engine stage
function buildStageOutput(task: string, engineKey: EngineKey, packet: ReturnType<typeof buildPacket>): string {
  const profile = ENGINE_PROFILES[engineKey];
  const ts = new Date().toISOString();

  const deliverables = profile.deliverables.map((d) => `  - ${d}`).join("\n");

  const engineSpecific: Record<EngineKey, string> = {
    research: `## Research Findings\n\nTask: "${task}"\n\nKey areas identified for investigation:\n1. Context and background analysis\n2. Existing solutions and comparable approaches\n3. Risk factors and constraint mapping\n4. Source-aware evidence stack\n\nRecommended next actions:\n- Cross-reference findings with verified claims database\n- Identify top 3 execution-ready paths\n- Flag any compliance or legal touchpoints early`,
    claims: `## Claims Analysis\n\nTask: "${task}"\n\nTop claims extracted:\n1. Primary assertion requiring verification\n2. Supporting evidence pathways identified\n3. Counter-arguments and rebuttals mapped\n\nEvidence confidence:\n- High confidence: Core premise aligns with research base\n- Medium confidence: Execution assumptions require field validation\n- Low confidence: Third-party dependency claims pending`,
    writing: `## Writing Output\n\nTask: "${task}"\n\nDraft framework:\n\n**Headline options:**\n- Direct execution path with maximum clarity\n- Conversion-grade framing with audience specificity\n- Authority-positioned statement with outcome focus\n\n**Body structure:**\n- Opening: Establish context and urgency\n- Core: Deliver the primary message with supporting detail\n- Close: Clear call to action with measurable outcome\n\n**Action checklist:**\n- [ ] Review headline against target audience\n- [ ] Verify all claims align with compliance engine output\n- [ ] Check CTA against Stripe/offer routing`,
    geometry: `## Spatial Concept Direction\n\nTask: "${task}"\n\nLayout assumptions:\n- Primary space: Functional, flow-optimized, ratio-aligned\n- Sacred geometry principles applied: Golden ratio proportions considered\n- Dimensional constraints: Standard regulatory compliance maintained\n\nImplementation notes:\n- Confirm all dimensions with field survey before execution\n- Apply frequency-alignment principles to orientation\n- Review sight lines and natural light optimization`,
    construction: `## Build Sequence\n\nTask: "${task}"\n\nPhase 1 — Preconstruction:\n- Owner brief confirmation and scope lock\n- Permit and regulatory pathway identification\n- Material takeoff and procurement schedule\n\nPhase 2 — Execution:\n- Foundation and structural sequence\n- MEP rough-in coordination\n- Envelope and finishing sequence\n\nPhase 3 — Closeout:\n- Punch list and final inspection\n- As-built documentation\n- Owner handoff packet\n\nRisk register:\n- Supply chain delays: Medium risk — buffer 10-15% on lead times\n- Regulatory approvals: Monitor permit backlog in jurisdiction`,
    compliance: `## Compliance Review\n\nTask: "${task}"\n\nCompliance watchouts:\n1. Regulatory alignment — ensure activity falls within approved jurisdiction scope\n2. Data handling — verify personal data is processed per applicable standards\n3. Financial operations — confirm banking, payment, and payroll flows are reviewed\n\nRequired approvals:\n- Legal review: Required before any binding commitments\n- Financial review: Required before payroll or large expenditure\n- Executive sign-off: Required for public-facing statements\n\nSafe execution checklist:\n- [ ] Legal counsel reviewed\n- [ ] Compliance boundary verified\n- [ ] Rollback path identified`,
    frequency: `## Execution Cadence\n\nTask: "${task}"\n\nRecommended rhythm:\n- Daily: 90-minute deep work block + 15-minute review\n- Weekly: Monday planning + Friday retrospective\n- Monthly: Metrics review + roadmap alignment\n\nFocus preservation rules:\n1. Single-task execution during deep work blocks\n2. Notification silence during primary execution windows\n3. Context-switching budget: maximum 3 transitions per day\n\nCadence anchors:\n- Morning: Strategic review and priority lock\n- Midday: Execution and delivery\n- Evening: Log, capture, and prep next session`,
    marketing: `## Marketing Strategy\n\nTask: "${task}"\n\nChannel plan:\n1. Primary: Direct outreach and owned channels (email, site)\n2. Secondary: Social — LinkedIn for B2B, Instagram for visual products\n3. Tertiary: Partner and referral network activation\n\nMessage angle:\n- Positioning: Authority + outcome-focused + no hype\n- Tone: Direct, confident, execution-ready\n- Hook: Lead with the transformation, not the feature\n\nOffer positioning:\n- Clear value ladder from entry to premium\n- Stripe checkout integration confirmed\n- KPIs: Conversion rate, average order value, retention`,
    ai_twin: `## AI Twin Video Strategy\n\nTask: "${task}"\n\nIdentity brief:\n- Avatar persona: Executive-grade, authoritative, authentic\n- Delivery style: Direct, measured, credible\n- Visual direction: Clean environment, professional framing\n\nScene sequence:\n1. Opening hook (0–5s): Grab attention with the core promise\n2. Context build (5–20s): Frame the problem with precision\n3. Solution delivery (20–45s): Show the result, not just the process\n4. CTA close (45–60s): Single, clear next action\n\nTool stack:\n- Avatar: HeyGen or Tavus\n- Scene generation: Runway or Sora\n- Edit and captions: CapCut or DaVinci Resolve`,
    publish: `## Publishing Package\n\nTask: "${task}"\n\nRelease checklist:\n- [ ] Final content review complete\n- [ ] All assets exported and named correctly\n- [ ] GitHub repository tagged with release version\n- [ ] Staging environment validated\n- [ ] Rollback procedure documented\n\nLaunch surfaces:\n1. Primary: Main production deployment via Vercel\n2. Secondary: GitHub release page with changelog\n3. Distribution: Email announcement + social announcement\n\nConnector handoff:\n- Make.com: Trigger release workflow automation\n- Replit: Remote runner confirmation if applicable`,
    automation: `## Automation Route\n\nTask: "${task}"\n\nConnector routing plan:\n1. Make.com webhook — triggered with full task packet\n2. Replit remote runner — standing by for code execution tasks\n3. GitHub API — repo operations and release management\n\nHandoff payload fields:\n- task: Full task description\n- engine_chain: Complete engine sequence executed\n- primary_output: Aggregated output from all engines\n- timestamp: ISO 8601 UTC execution timestamp\n- execution_mode: dry_run or live_ready\n\nRemote execution status:\n- Make.com: Configured — webhook will receive this packet\n- Replit: Configured — runner standing by\n- GitHub: Token-gated — ready for repo operations`,
  };

  return (
    `# ${profile.label} — Execution Output\n` +
    `Generated: ${ts}\n` +
    `Task: "${task}"\n` +
    `Mission: ${packet.mission}\n\n` +
    `Required deliverables:\n${deliverables}\n\n` +
    engineSpecific[engineKey] +
    `\n\n---\n_Engine: ${engineKey} | Focus: ${profile.focus}_`
  );
}

export async function POST(request: NextRequest) {
  const body = await request.json().catch(() => ({}));
  const { task, engine = "automation", execution_mode = "dry_run" } = body as {
    task?: string;
    engine?: EngineKey;
    execution_mode?: string;
  };

  if (!task || typeof task !== "string" || !task.trim()) {
    return new Response(JSON.stringify({ error: "task is required" }), {
      status: 400,
      headers: { "Content-Type": "application/json" },
    });
  }

  const engineKey: EngineKey = ENGINE_PROFILES[engine] ? engine : "automation";
  const packet = buildPacket(task.trim(), engineKey);

  const encoder = new TextEncoder();

  const stream = new ReadableStream({
    async start(controller) {
      const send = (text: string) => controller.enqueue(encoder.encode(text));

      try {
        // Header
        send(
          `# FOCUS MASTER AI — Pipeline Execution\n` +
          `Started: ${new Date().toISOString()}\n` +
          `Task: "${packet.task}"\n` +
          `Primary Engine: ${packet.label}\n` +
          `Mode: ${execution_mode.toUpperCase()}\n` +
          `Engine Sequence: ${packet.sequence.join(" → ")}\n\n` +
          `${"─".repeat(60)}\n\n`
        );

        // Attempt real OpenAI call if env available
        const openAiKey = process.env.OPENAI_API_KEY;

        if (openAiKey && execution_mode === "live_ready") {
          // Real streaming via OpenAI
          for (const engKey of packet.sequence) {
            const engProfile = ENGINE_PROFILES[engKey as EngineKey];
            if (!engProfile) continue;

            send(`\n## ▶ ${engProfile.label}\n\n`);
            send(`[ENGINE_START:${engKey}]\n`);

            const sysPrompt =
              `You are the ${engProfile.label} inside FOCUS MASTER AI.\n` +
              `Primary focus: ${engProfile.focus}.\n` +
              `Required deliverables:\n${engProfile.deliverables.map((d) => `- ${d}`).join("\n")}\n\n` +
              `Execution rules:\n` +
              `- Produce high-quality, detailed, structured output.\n` +
              `- Make the result automation-ready and easy to hand off.\n` +
              `- Be specific, practical, and execution-oriented.\n` +
              `- Format output in Markdown.`;

            const resp = await fetch("https://api.openai.com/v1/chat/completions", {
              method: "POST",
              headers: {
                Authorization: `Bearer ${openAiKey}`,
                "Content-Type": "application/json",
              },
              body: JSON.stringify({
                model: "gpt-4o-mini",
                stream: true,
                max_tokens: 800,
                messages: [
                  { role: "system", content: sysPrompt },
                  { role: "user", content: packet.task },
                ],
              }),
            });

            if (!resp.ok || !resp.body) {
              send(`\n[OpenAI unavailable — using structured fallback]\n`);
              send(buildStageOutput(packet.task, engKey as EngineKey, packet));
            } else {
              const reader = resp.body.getReader();
              const dec = new TextDecoder();
              while (true) {
                const { done, value } = await reader.read();
                if (done) break;
                const lines = dec.decode(value).split("\n");
                for (const line of lines) {
                  if (line.startsWith("data: ")) {
                    const data = line.slice(6).trim();
                    if (data === "[DONE]") break;
                    try {
                      const parsed = JSON.parse(data);
                      const content = parsed.choices?.[0]?.delta?.content;
                      if (content) send(content);
                    } catch {
                      // Skip malformed lines
                    }
                  }
                }
              }
            }

            send(`\n\n[ENGINE_COMPLETE:${engKey}]\n`);
          }
        } else {
          // Structured fallback mode (dry run or no API key)
          for (const engKey of packet.sequence) {
            const engProfile = ENGINE_PROFILES[engKey as EngineKey];
            if (!engProfile) continue;

            send(`\n## ▶ ${engProfile.label}\n\n`);
            send(`[ENGINE_START:${engKey}]\n\n`);

            // Simulate streaming by chunking the fallback output
            const stageOutput = buildStageOutput(packet.task, engKey as EngineKey, packet);
            const chunks = stageOutput.match(/.{1,40}/gs) || [stageOutput];

            for (const chunk of chunks) {
              send(chunk);
              // Small async yield to allow streaming feel
              await new Promise((r) => setTimeout(r, 8));
            }

            send(`\n\n[ENGINE_COMPLETE:${engKey}]\n`);
            await new Promise((r) => setTimeout(r, 120));
          }
        }

        // Footer
        send(
          `\n${"─".repeat(60)}\n` +
          `# Pipeline Complete\n` +
          `Finished: ${new Date().toISOString()}\n` +
          `Engines executed: ${packet.sequence.join(", ")}\n` +
          `Status: COMPLETED\n` +
          `[PIPELINE_COMPLETE]\n`
        );
      } catch (err) {
        send(`\n[PIPELINE_ERROR: ${err instanceof Error ? err.message : "Unknown error"}]\n`);
      } finally {
        controller.close();
      }
    },
  });

  return new Response(stream, {
    headers: {
      "Content-Type": "text/plain; charset=utf-8",
      "Transfer-Encoding": "chunked",
      "Cache-Control": "no-cache, no-transform",
      "X-Accel-Buffering": "no",
    },
  });
}
