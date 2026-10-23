import type { GuardrailMetric, QualityCheck } from "../services/api";

type GuardrailTableProps = {
  guardrails: GuardrailMetric[];
  qualityChecks: QualityCheck[];
};

const percent = new Intl.NumberFormat("en", { style: "percent", maximumFractionDigits: 2 });

export function GuardrailTable({ guardrails, qualityChecks }: GuardrailTableProps) {
  return (
    <section className="split-grid">
      <div className="panel">
        <div className="panel-heading">
          <p className="eyebrow">Guardrails</p>
          <h2>Customer Experience Metrics</h2>
        </div>
        <div className="table-wrap">
          <table>
            <thead>
              <tr>
                <th>Metric</th>
                <th>Control</th>
                <th>Treatment</th>
                <th>Delta</th>
                <th>Status</th>
              </tr>
            </thead>
            <tbody>
              {guardrails.map((metric) => (
                <tr key={metric.metric}>
                  <td>{metric.metric}</td>
                  <td>{metric.control_value.toFixed(metric.metric.includes("ms") ? 0 : 4)}</td>
                  <td>{metric.treatment_value.toFixed(metric.metric.includes("ms") ? 0 : 4)}</td>
                  <td>{metric.metric.includes("rate") ? percent.format(metric.relative_delta) : metric.absolute_delta.toFixed(0)}</td>
                  <td>
                    <span className={`pill ${metric.status === "pass" ? "pill--pass" : "pill--watch"}`}>
                      {metric.status}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
      <div className="panel">
        <div className="panel-heading">
          <p className="eyebrow">Data Quality</p>
          <h2>Experiment Integrity Checks</h2>
        </div>
        <div className="quality-list">
          {qualityChecks.map((check) => (
            <div className="quality-item" key={check.check}>
              <span className={`pill ${check.status === "pass" ? "pill--pass" : "pill--watch"}`}>{check.status}</span>
              <div>
                <strong>{check.check}</strong>
                <p>{check.details}</p>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
