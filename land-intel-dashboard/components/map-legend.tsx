import { MAP_LEGEND } from "@/lib/content";

export function MapLegend() {
  return (
    <div className="grid grid-cols-1 gap-5 lg:grid-cols-2">
      {MAP_LEGEND.map((group) => (
        <div
          key={group.group}
          className="rounded-lg border border-border bg-card p-5 text-card-foreground shadow-sm"
        >
          <h3 className="mb-3 font-serif text-lg font-semibold text-foreground">
            {group.group}
          </h3>
          <ul className="flex flex-col">
            {group.items.map((item) => (
              <li
                key={item.name}
                className="flex items-start gap-3 border-b border-border/60 py-2.5 last:border-b-0"
              >
                <span
                  className="mt-0.5 inline-flex h-7 w-12 shrink-0 items-center justify-center rounded border border-border bg-muted font-mono text-xs text-foreground"
                  aria-hidden
                >
                  {item.symbol}
                </span>
                <div className="min-w-0">
                  <p className="flex flex-wrap items-center gap-2 text-sm font-semibold text-foreground">
                    {item.name}
                    <span className="rounded bg-muted px-1.5 py-0.5 font-mono text-[10px] uppercase tracking-wide text-muted-foreground">
                      {item.kind}
                    </span>
                  </p>
                  <p className="text-sm leading-relaxed text-muted-foreground">
                    {item.meaning}
                  </p>
                </div>
              </li>
            ))}
          </ul>
        </div>
      ))}
    </div>
  );
}
