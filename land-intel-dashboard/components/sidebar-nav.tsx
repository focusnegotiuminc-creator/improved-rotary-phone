"use client";

import { useState } from "react";

export type NavItem = { id: string; index: string; label: string };

export function SidebarNav({ items }: { items: NavItem[] }) {
  const [open, setOpen] = useState(false);

  return (
    <>
      {/* Mobile toggle */}
      <button
        type="button"
        onClick={() => setOpen((v) => !v)}
        className="fixed bottom-4 right-4 z-40 inline-flex h-12 min-w-12 items-center justify-center gap-2 rounded-full bg-primary px-5 text-sm font-semibold text-primary-foreground shadow-lg lg:hidden"
        aria-expanded={open}
        aria-controls="section-nav"
      >
        {open ? "Close" : "Contents"}
      </button>

      <nav
        id="section-nav"
        aria-label="Report sections"
        className={`${
          open ? "block" : "hidden"
        } fixed inset-0 z-30 overflow-y-auto bg-background/98 p-6 pt-20 lg:sticky lg:top-0 lg:block lg:h-screen lg:max-h-screen lg:w-72 lg:shrink-0 lg:overflow-y-auto lg:border-r lg:border-border lg:bg-card/40 lg:p-6 lg:pt-8`}
      >
        <p className="mb-4 font-mono text-xs uppercase tracking-widest text-accent">
          Investigation Index
        </p>
        <ol className="flex flex-col gap-1">
          {items.map((item) => (
            <li key={item.id}>
              <a
                href={`#${item.id}`}
                onClick={() => setOpen(false)}
                className="flex items-start gap-3 rounded-md px-3 py-2 text-sm text-foreground transition-colors hover:bg-muted"
              >
                <span className="font-mono text-xs text-muted-foreground">{item.index}</span>
                <span className="leading-snug">{item.label}</span>
              </a>
            </li>
          ))}
        </ol>
      </nav>
    </>
  );
}
