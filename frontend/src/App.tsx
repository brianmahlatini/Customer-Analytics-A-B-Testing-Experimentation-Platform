import { useEffect, useState } from "react";
import FlaskConical from "lucide-react/dist/esm/icons/flask-conical.js";
import { ExperimentSummary } from "./components/ExperimentSummary";
import { GuardrailTable } from "./components/GuardrailTable";
import { MlInsightsPanel } from "./components/MlInsightsPanel";
import { ResultsTable } from "./components/ResultsTable";
import { SampleSizePanel } from "./components/SampleSizePanel";
import { UpliftChart } from "./components/UpliftChart";
import {
  fetchExperimentConfig,
  fetchExperimentResults,
  fetchMlInsights,
  type ExperimentConfig,
  type ExperimentResults,
  type MlInsights,
} from "./services/api";
import "./styles/app.css";

export default function App() {
  const [config, setConfig] = useState<ExperimentConfig | null>(null);
  const [results, setResults] = useState<ExperimentResults | null>(null);
  const [mlInsights, setMlInsights] = useState<MlInsights | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  async function loadDashboard() {
    setLoading(true);
    setError(null);
    try {
      const [configPayload, resultsPayload, mlPayload] = await Promise.all([
        fetchExperimentConfig(),
        fetchExperimentResults(),
        fetchMlInsights(),
      ]);
      setConfig(configPayload);
      setResults(resultsPayload);
      setMlInsights(mlPayload);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Could not load dashboard data.");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    loadDashboard();
  }, []);

  if (loading) {
    return (
      <main className="app-shell app-shell--center">
        <span className="loading-ring" aria-hidden="true" />
        <p>Loading experiment dashboard...</p>
      </main>
    );
  }

  if (error || !config || !results || !mlInsights) {
    return (
      <main className="app-shell app-shell--center">
        <FlaskConical size={30} aria-hidden="true" />
        <h1>Dashboard data unavailable</h1>
        <p>{error}</p>
        <button onClick={loadDashboard} type="button">
          Retry
        </button>
      </main>
    );
  }

  return (
    <main className="app-shell">
      <ExperimentSummary config={config} results={results} />
      <SampleSizePanel config={config} />
      <UpliftChart conversion={results.conversion_test} revenue={results.revenue_test} variants={results.variant_summary} />
      <ResultsTable results={results} />
      <MlInsightsPanel insights={mlInsights} />
      <GuardrailTable guardrails={results.guardrails} qualityChecks={results.quality_checks} />
    </main>
  );
}
