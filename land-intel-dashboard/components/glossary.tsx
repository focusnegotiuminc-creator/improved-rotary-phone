"use client";

import { useMemo, useState } from "react";
import { GLOSSARY, type GlossaryTerm } from "@/lib/content";

const NATURE_STYLE: Record<GlossaryTerm["nature"], string> = {
  legal: "bg-strong text-primary-foreground",
  historical: "bg-possible text-primary-foreground",
  symbolic: "bg-unknown text-primary-foreground",
  speculative: "bg-speculative text-primary-foreground",
};

export function Glossary() {
  const [query, setQuery] = useState("");
  const filtered = useMemo(() => {
    const q = query.trim().toLowerCase();
    if (!q) return GLOSSARY;
    return GLOSSARY.filter(
      (t) =>
        t.term.toLowerCase().includes(q) ||
        t.plain.toLowerCase().includes(q) ||
        t.legal.toLowerCase().includes(q),
    );
  }, [query]);

  return (
    <div>
      <label htmlFor="glossary-search" className="sr-only">
        Search land &amp; title terms
      </label>
      <input
        id="glossary-search"
        type="search"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        placeholder="Search terms (e.g. easement, trust, riparian)"
        className="mb-5 w-full rounded-lg border border-border bg-card px-4 py-3 text-base text-foreground outline-none placeholder:text-muted-foreground focus:border-primary"
      />
      <div className="grid grid-cols-1 gap-4 md:grid-cols-2">
        {filtered.map((t) => (
          <div
            key={t.term}
            className="rounded-lg border border-border bg-card p-4 text-card-foreground shadow-sm"
          >
            <div className="mb-2 flex items-center justify-between gap-2">
              <h3 className="font-serif text-lg font-semibold text-foreground">{t.term}</h3>
              <span
                className={`rounded-full px-2 py-0.5 text-[10px] font-semibold uppercase tracking-wide ${NATURE_STYLE[t.nature]}`}
              >
                {t.nature}
              </span>
            </div>
            <dl className="flex flex-col gap-2 text-sm">
              <div>
                <dt className="font-semibold text-muted-foreground">Black&apos;s Law-style</dt>
                <dd className="leading-relaxed text-foreground">{t.legal}</dd>
              </div>
              <div>
                <dt className="font-semibold text-muted-foreground">Plain English</dt>
                <dd className="leading-relaxed text-foreground">{t.plain}</dd>
              </div>
              <div>
                <dt className="font-semibold text-muted-foreground">Effect on land / title</dt>
                <dd className="leading-relaxed text-foreground">{t.land}</dd>
              </div>
            </dl>
          </div>
        ))}
        {filtered.length === 0 ? (
          <p className="text-sm text-muted-foreground">No terms match &ldquo;{query}&rdquo;.</p>
        ) : null}
      </div>
    </div>
  );
}
