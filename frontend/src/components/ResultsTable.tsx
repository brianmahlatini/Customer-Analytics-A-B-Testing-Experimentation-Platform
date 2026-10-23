import type { ExperimentResults } from "../services/api";

type ResultsTableProps = {
  results: ExperimentResults;
};

const percent = new Intl.NumberFormat("en", { style: "percent", maximumFractionDigits: 2 });
const currency = new Intl.NumberFormat("en", { style: "currency", currency: "USD", maximumFractionDigits: 2 });

function metricFormatter(metric: string, value: number) {
  if (metric.includes("conversion")) return percent.format(value);
  if (metric.includes("revenue")) return currency.format(value);
  return value.toFixed(4);
}

export function ResultsTable({ results }: ResultsTableProps) {
  const tests = [results.conversion_test, results.revenue_test];

  return (
    <section className="panel">
      <div className="panel-heading">
        <p className="eyebrow">Statistical Tests</p>
        <h2>Effect Size, Significance, and Confidence</h2>
      </div>
      <div className="table-wrap">
        <table>
          <thead>
            <tr>
              <th>Metric</th>
              <th>Control</th>
              <th>Treatment</th>
              <th>Absolute Uplift</th>
              <th>Relative Uplift</th>
              <th>95% CI</th>
              <th>p-value</th>
              <th>Decision</th>
            </tr>
          </thead>
          <tbody>
            {tests.map((test) => (
              <tr key={test.metric}>
                <td>{test.metric}</td>
                <td>{metricFormatter(test.metric, test.control_value)}</td>
                <td>{metricFormatter(test.metric, test.treatment_value)}</td>
                <td>{metricFormatter(test.metric, test.absolute_uplift)}</td>
                <td>{percent.format(test.relative_uplift)}</td>
                <td>
                  {metricFormatter(test.metric, test.confidence_interval_low)} to{" "}
                  {metricFormatter(test.metric, test.confidence_interval_high)}
                </td>
                <td>{test.p_value.toFixed(5)}</td>
                <td>
                  <span className={`pill ${test.is_significant ? "pill--pass" : "pill--watch"}`}>
                    {test.is_significant ? "Significant" : "Uncertain"}
                  </span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </section>
  );
}
