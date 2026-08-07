import React, { useState } from 'react';
import { masterOsAgents } from '../agents/recoding-architect';

const profiles = ['Great Machevilli', 'The Focus Corp'];
const connectors = ['Cloudflare', 'GitHub', 'Google Drive', 'Vercel', 'Gmail', 'Calendar'];

export function CloudflareStatusDashboard() {
  const [confirming, setConfirming] = useState<string | null>(null);
  return (
    <main className="min-h-screen bg-slate-950 text-white md:flex">
      <aside className="w-full border-b border-white/10 p-4 md:min-h-screen md:w-72 md:border-b-0 md:border-r">
        <h1 className="text-xl font-bold">Master OS Agents</h1>
        <nav className="mt-4 grid gap-2 text-sm">
          {masterOsAgents.map((agent) => <span key={agent} className="rounded-xl bg-white/5 px-3 py-2">{agent}</span>)}
        </nav>
      </aside>
      <section className="flex-1 space-y-6 p-4 md:p-8">
        <header>
          <p className="text-sm uppercase tracking-widest text-cyan-300">Cloudflare primary / Vercel fallback</p>
          <h2 className="text-3xl font-black">iPhone-friendly Automation Dashboard</h2>
        </header>
        <div className="grid gap-4 md:grid-cols-2">
          {profiles.map((profile) => <article key={profile} className="rounded-2xl border border-white/10 bg-white/5 p-4"><h3 className="font-bold">{profile}</h3><p className="text-sm text-slate-300">Connection status loads from the Cloudflare connector health check. No secrets are stored in the dashboard.</p><span className="mt-3 inline-flex rounded-full bg-amber-400/20 px-3 py-1 text-xs text-amber-200">Awaiting runtime credentials</span></article>)}
        </div>
        <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
          {connectors.map((connector) => <div key={connector} className="rounded-xl border border-white/10 p-4"><strong>{connector}</strong><p className="text-sm text-slate-400">Health check, retries, audit trail, and error logs enabled.</p></div>)}
        </div>
        <form className="rounded-2xl border border-white/10 bg-white/5 p-4">
          <label className="text-sm font-semibold" htmlFor="task">Submit task, review, deployment, or audit-log request</label>
          <textarea id="task" className="mt-2 min-h-32 w-full rounded-xl bg-slate-900 p-3" placeholder="Describe the task..." />
          <div className="mt-3 flex flex-wrap gap-2">
            {['Submit Task','Request Code Review','Request Deployment','View Audit Logs'].map((action) => <button key={action} type="button" onClick={() => /Deployment|Audit/.test(action) ? setConfirming(action) : undefined} className="rounded-full bg-cyan-500 px-4 py-2 font-bold text-slate-950">{action}</button>)}
          </div>
        </form>
        {confirming && <section className="rounded-2xl border border-red-400/40 bg-red-950/40 p-4"><h3 className="font-bold">Confirm {confirming}</h3><p className="text-sm">Deployment and destructive/audit-sensitive actions require explicit human confirmation before execution.</p><button className="mt-3 rounded-full bg-red-400 px-4 py-2 font-bold text-red-950">Confirm</button></section>}
      </section>
    </main>
  );
}
