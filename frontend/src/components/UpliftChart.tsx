import Plot from "react-plotly.js";
import type { TestResult, VariantSummary } from "../services/api";

type UpliftChartProps = {
  conversion: TestResult;
  revenue: TestResult;
  variants: VariantSummary[];
};

const percent = new Intl.NumberFormat("en", { style: "percent", maximumFractionDigits: 2 });

export function UpliftChart({ conversion, revenue, variants }: UpliftChartProps) {
  return (
    <section className="chart-grid">
      <div className="panel">
        <div className="panel-heading">
          <p className="eyebrow">Primary Metric</p>
          <h2>Conversion Rate by Variant</h2>
        </div>
        <Plot
          data={[
            {
              type: "bar",
              x: variants.map((variant) => variant.variant),
              y: variants.map((variant) => variant.conversion_rate),
              marker: { color: ["#245953", "#D96C2C"] },
              text: variants.map((variant) => percent.format(variant.conversion_rate)),
              textposition: "auto",
            },
          ]}
          layout={{
            autosize: true,
            height: 320,
            margin: { l: 52, r: 24, t: 20, b: 44 },
            paper_bgcolor: "rgba(0,0,0,0)",
            plot_bgcolor: "rgba(0,0,0,0)",
            yaxis: { tickformat: ".1%", gridcolor: "#e7ece9" },
            xaxis: { fixedrange: true },
            showlegend: false,
          }}
          config={{ displayModeBar: false, responsive: true }}
          className="plot"
        />
      </div>
      <div className="panel">
        <div className="panel-heading">
          <p className="eyebrow">Uncertainty</p>
          <h2>Uplift and 95% Confidence Intervals</h2>
        </div>
        <Plot
          data={[
            {
              type: "scatter",
              mode: "markers",
              x: [conversion.absolute_uplift, revenue.absolute_uplift],
              y: ["Conversion", "Revenue / Visitor"],
              error_x: {
                type: "data",
                symmetric: false,
                array: [
                  conversion.confidence_interval_high - conversion.absolute_uplift,
                  revenue.confidence_interval_high - revenue.absolute_uplift,
                ],
                arrayminus: [
                  conversion.absolute_uplift - conversion.confidence_interval_low,
                  revenue.absolute_uplift - revenue.confidence_interval_low,
                ],
              },
              marker: { color: "#D96C2C", size: 13 },
            },
          ]}
          layout={{
            autosize: true,
            height: 320,
            margin: { l: 118, r: 32, t: 20, b: 44 },
            paper_bgcolor: "rgba(0,0,0,0)",
            plot_bgcolor: "rgba(0,0,0,0)",
            xaxis: { zeroline: true, zerolinecolor: "#1d2b2a", gridcolor: "#e7ece9" },
            yaxis: { fixedrange: true },
            showlegend: false,
          }}
          config={{ displayModeBar: false, responsive: true }}
          className="plot"
        />
      </div>
    </section>
  );
}
