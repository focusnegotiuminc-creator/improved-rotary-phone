import React, { useMemo, useState } from "react";
import { masterOsAgents, routeTask } from "../agents/recoding-architect";
import { connectorStatus } from "../connectors/registry";
import { focusCorpCloudflareProfile } from "../config/cloudflare.profile.focuscorp";
import { greatMachevilliCloudflareProfile } from "../config/cloudflare.profile.greatmachevilli";

export function CloudflareStatusDashboard({ env = {} }: { env?: Record<string, string | undefined> }) {
  const [task, setTask] = useState("");
  const route = useMemo(() => routeTask(task), [task]);
  const connectors = connectorStatus(env);
  const profiles = [greatMachevilliCloudflareProfile, focusCorpCloudflareProfile];

  return (
    <main className="min-h-screen bg-slate-950 text-slate-100 md:flex">
      <aside className="border-b border-slate-800 p-4 md:min-h-screen md:w-72 md:border-b-0 md:border-r">
        <h1 className="text-xl font-bold">Master OS</h1>
        <p className="text-sm text-slate-400">iPhone-friendly multi-agent command center</p>
        <nav className="mt-4 grid gap-2">
          {masterOsAgents.map((agent) => <span className="rounded-xl bg-slate-900 px-3 py-2 text-sm" key={agent}>{agent}</span>)}
        </nav>
      </aside>
      <section className="grid flex-1 gap-4 p-4">
        <section className="rounded-2xl border border-slate-800 bg-slate-900 p-4">
          <h2 className="text-lg font-semibold">Cloudflare profiles</h2>
          <div className="mt-3 grid gap-3 sm:grid-cols-2">
            {profiles.map((profile) => <article className="rounded-xl bg-slate-950 p-3" key={profile.id}><strong>{profile.id}</strong><p>{profile.ownerEmail}</p><p>Primary: Cloudflare Workers/Pages</p><p>Fallback: Vercel</p></article>)}
          </div>
        </section>
        <section className="rounded-2xl border border-slate-800 bg-slate-900 p-4">
          <h2 className="text-lg font-semibold">Connector status</h2>
          <div className="mt-3 grid gap-2 sm:grid-cols-2 lg:grid-cols-3">
            {connectors.map((connector) => <div className="rounded-xl bg-slate-950 p-3" key={connector.id}><span>{connector.ok ? "✅" : "⚠️"} {connector.id}</span><p className="text-xs text-slate-400">{connector.ok ? "configured" : `missing: ${connector.missing.join(", ")}`}</p></div>)}
          </div>
        </section>
        <section className="rounded-2xl border border-slate-800 bg-slate-900 p-4">
          <h2 className="text-lg font-semibold">Submit task / review / deployment / audit request</h2>
          <textarea className="mt-3 min-h-32 w-full rounded-xl bg-slate-950 p-3" value={task} onChange={(event) => setTask(event.target.value)} placeholder="Describe the task..." />
          {route.requiresConfirmation && <label className="mt-3 flex gap-2 text-amber-300"><input required type="checkbox" /> I confirm this deployment or destructive action.</label>}
          <p className="mt-3 text-sm text-slate-300">Route: {route.agent}</p>
        </section>
      </section>
    </main>
  );
}
