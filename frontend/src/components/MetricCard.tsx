import ArrowUpRight from "lucide-react/dist/esm/icons/arrow-up-right.js";
import BadgeCheck from "lucide-react/dist/esm/icons/badge-check.js";
import CircleAlert from "lucide-react/dist/esm/icons/circle-alert.js";

type MetricCardProps = {
  title: string;
  value: string;
  detail: string;
  tone?: "positive" | "neutral" | "warning";
};

export function MetricCard({ title, value, detail, tone = "neutral" }: MetricCardProps) {
  const Icon = tone === "warning" ? CircleAlert : tone === "positive" ? ArrowUpRight : BadgeCheck;

  return (
    <article className={`metric-card metric-card--${tone}`}>
      <div className="metric-card__icon">
        <Icon size={18} aria-hidden="true" />
      </div>
      <div>
        <p>{title}</p>
        <strong>{value}</strong>
        <span>{detail}</span>
      </div>
    </article>
  );
}
