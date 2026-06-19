import type { ReactNode } from "react";

export function Section({
  id,
  index,
  title,
  subtitle,
  children,
}: {
  id: string;
  index: string;
  title: string;
  subtitle?: string;
  children: ReactNode;
}) {
  return (
    <section id={id} className="scroll-mt-24 border-t border-border py-10 first:border-t-0">
      <header className="mb-6 flex items-start gap-4">
        <span className="mt-1 font-mono text-sm font-semibold text-accent">{index}</span>
        <div>
          <h2 className="text-pretty font-serif text-2xl font-semibold text-foreground md:text-3xl">
            {title}
          </h2>
          {subtitle ? (
            <p className="mt-2 max-w-2xl text-pretty leading-relaxed text-muted-foreground">
              {subtitle}
            </p>
          ) : null}
        </div>
      </header>
      <div className="pl-0 md:pl-9">{children}</div>
    </section>
  );
}

export function Card({
  title,
  children,
}: {
  title?: string;
  children: ReactNode;
}) {
  return (
    <div className="rounded-lg border border-border bg-card p-5 text-card-foreground shadow-sm">
      {title ? (
        <h3 className="mb-3 font-serif text-lg font-semibold text-foreground">{title}</h3>
      ) : null}
      {children}
    </div>
  );
}

export function KeyValue({ k, v }: { k: string; v: ReactNode }) {
  return (
    <div className="flex flex-col gap-0.5 border-b border-border/70 py-2 last:border-b-0 sm:flex-row sm:items-baseline sm:justify-between sm:gap-4">
      <dt className="text-sm font-medium text-muted-foreground">{k}</dt>
      <dd className="text-sm font-semibold text-foreground sm:text-right">{v}</dd>
    </div>
  );
}
