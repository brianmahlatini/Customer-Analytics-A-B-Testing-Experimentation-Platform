import type { MlInsights } from "../services/api";

type MlInsightsPanelProps = {
  insights: MlInsights;
};

const percent = new Intl.NumberFormat("en", { style: "percent", maximumFractionDigits: 2 });
const currency = new Intl.NumberFormat("en", { style: "currency", currency: "USD", maximumFractionDigits: 2 });

export function MlInsightsPanel({ insights }: MlInsightsPanelProps) {
  return (
    <section className="panel">
      <div className="panel-heading">
        <div>
          <p className="eyebrow">Machine Learning</p>
          <h2>Uplift Modeling and Targeting</h2>
        </div>
      </div>
      <div className="ml-grid">
        {insights.models.map((model) => (
          <article className="ml-card" key={model.algorithm}>
            <strong>{model.algorithm}</strong>
            <p>{model.purpose}</p>
            <div className="ml-stats">
              {model.holdout_auc !== undefined && <span>AUC {model.holdout_auc.toFixed(3)}</span>}
              {model.conversion_probability_mae !== undefined && (
                <span>CVR MAE {model.conversion_probability_mae.toFixed(3)}</span>
              )}
              {model.revenue_mae !== undefined && <span>Revenue MAE {currency.format(model.revenue_mae)}</span>}
            </div>
          </article>
        ))}
      </div>
      <div className="recommendation-strip">
        <div>
          <span>Top 500 predicted conversion uplift</span>
          <strong>{percent.format(insights.targeting_recommendation.top_500_average_conversion_uplift)}</strong>
        </div>
        <div>
          <span>Top 500 predicted revenue uplift</span>
          <strong>{currency.format(insights.targeting_recommendation.top_500_average_revenue_uplift)}</strong>
        </div>
        <p>{insights.targeting_recommendation.policy}</p>
      </div>
      <div className="table-wrap">
        <table>
          <thead>
            <tr>
              <th>Channel</th>
              <th>Device</th>
              <th>Country</th>
              <th>Customers</th>
              <th>Predicted CVR Uplift</th>
              <th>Predicted Revenue Uplift</th>
            </tr>
          </thead>
          <tbody>
            {insights.top_uplift_segments.map((segment) => (
              <tr key={`${segment.channel}-${segment.device}-${segment.country}`}>
                <td>{segment.channel}</td>
                <td>{segment.device}</td>
                <td>{segment.country}</td>
                <td>{segment.customers.toLocaleString()}</td>
                <td>{percent.format(segment.predicted_conversion_uplift)}</td>
                <td>{currency.format(segment.predicted_revenue_uplift)}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </section>
  );
}
