import { CONFIDENCE_LABELS, type Confidence } from "@/lib/content";

const COLOR: Record<Confidence, string> = {
  verified: "bg-verified",
  strong: "bg-strong",
  likely: "bg-likely",
  possible: "bg-possible",
  speculative: "bg-speculative",
  unknown: "bg-unknown",
};

export function ConfidenceBadge({
  level,
  withTooltip = true,
}: {
  level: Confidence;
  withTooltip?: boolean;
}) {
  const meta = CONFIDENCE_LABELS[level];
  return (
    <span
      title={withTooltip ? meta.blurb : undefined}
      className={`inline-flex items-center gap-1.5 rounded-full px-2.5 py-0.5 text-xs font-medium text-primary-foreground ${COLOR[level]}`}
    >
      <span className="h-1.5 w-1.5 rounded-full bg-primary-foreground/80" aria-hidden />
      {meta.label}
    </span>
  );
}
