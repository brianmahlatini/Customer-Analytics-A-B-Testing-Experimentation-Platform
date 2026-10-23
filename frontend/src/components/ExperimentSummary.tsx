import type { ExperimentConfig, ExperimentResults } from "../services/api";
import { MetricCard } from "./MetricCard";

type ExperimentSummaryProps = {
  config: ExperimentConfig;
  results: ExperimentResults;
};

const percent = new Intl.NumberFormat("en", { style: "percent", maximumFractionDigits: 2 });
const currency = new Intl.NumberFormat("en", { style: "currency", currency: "USD", maximumFractionDigits: 0 });

export function ExperimentSummary({ config, results }: ExperimentSummaryProps) {
  const srm = results.sample_ratio_mismatch;

  return (
    <section className="summary-band">
      <div className="summary-copy">
        <p className="eyebrow">Customer Analytics Experiment</p>
        <h1>{config.experiment_name}</h1>
        <p>{config.hypothesis}</p>
      </div>
      <div className="metric-grid">
        <MetricCard
          title="Recommendation"
          value={results.recommendation}
          detail={results.rationale}
          tone={results.recommendation === "Launch the treatment" ? "positive" : "warning"}
        />
        <MetricCard
          title="Conversion Lift"
          value={percent.format(results.conversion_test.relative_uplift)}
          detail={`${percent.format(results.conversion_test.absolute_uplift)} absolute uplift`}
          tone={results.conversion_test.is_significant ? "positive" : "warning"}
        />
        <MetricCard
          title="Monthly Revenue Impact"
          value={currency.format(results.business_impact.estimated_monthly_revenue_uplift)}
          detail={`${currency.format(results.business_impact.estimated_annual_revenue_uplift)} annualized`}
          tone="positive"
        />
        <MetricCard
          title="SRM Check"
          value={srm.has_sample_ratio_mismatch ? "Investigate" : "Passed"}
          detail={`p=${srm.p_value.toFixed(4)} | ${srm.control_count} / ${srm.treatment_count}`}
          tone={srm.has_sample_ratio_mismatch ? "warning" : "neutral"}
        />
      </div>
    </section>
  );
}
