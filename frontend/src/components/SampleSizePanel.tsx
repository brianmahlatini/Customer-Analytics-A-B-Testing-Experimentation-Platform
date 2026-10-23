import type { ExperimentConfig } from "../services/api";

type SampleSizePanelProps = {
  config: ExperimentConfig;
};

const percent = new Intl.NumberFormat("en", { style: "percent", maximumFractionDigits: 1 });
const number = new Intl.NumberFormat("en");

export function SampleSizePanel({ config }: SampleSizePanelProps) {
  const plan = config.sample_size_plan;

  return (
    <section className="panel sample-panel">
      <div className="panel-heading">
        <p className="eyebrow">Power Planning</p>
        <h2>Sample Size and Duration</h2>
      </div>
      <div className="sample-grid">
        <div>
          <span>Baseline conversion</span>
          <strong>{percent.format(plan.baseline_conversion_rate)}</strong>
        </div>
        <div>
          <span>Minimum detectable effect</span>
          <strong>{percent.format(plan.minimum_detectable_effect)}</strong>
        </div>
        <div>
          <span>Power</span>
          <strong>{percent.format(plan.power)}</strong>
        </div>
        <div>
          <span>Sample per group</span>
          <strong>{number.format(plan.sample_size_per_group)}</strong>
        </div>
        <div>
          <span>Total sample</span>
          <strong>{number.format(plan.total_sample_size)}</strong>
        </div>
        <div>
          <span>Estimated duration</span>
          <strong>{plan.estimated_duration_days} days</strong>
        </div>
      </div>
    </section>
  );
}
