export type VariantSummary = {
  variant: string;
  visitors: number;
  conversions: number;
  conversion_rate: number;
  total_revenue: number;
  revenue_per_visitor: number;
  average_order_value: number;
  bounce_rate: number;
  refund_rate: number;
  avg_page_load_ms: number;
};

export type TestResult = {
  metric: string;
  control_value: number;
  treatment_value: number;
  absolute_uplift: number;
  relative_uplift: number;
  confidence_interval_low: number;
  confidence_interval_high: number;
  p_value: number;
  test_statistic: number;
  is_significant: boolean;
};

export type GuardrailMetric = {
  metric: string;
  control_value: number;
  treatment_value: number;
  absolute_delta: number;
  relative_delta: number;
  status: string;
};

export type QualityCheck = {
  check: string;
  status: string;
  details: string;
};

export type ExperimentResults = {
  hypothesis: string;
  primary_metric: string;
  secondary_metric: string;
  variant_summary: VariantSummary[];
  conversion_test: TestResult;
  revenue_test: TestResult;
  guardrails: GuardrailMetric[];
  business_impact: {
    monthly_visitors: number;
    incremental_revenue_per_visitor: number;
    estimated_monthly_revenue_uplift: number;
    estimated_annual_revenue_uplift: number;
  };
  recommendation: string;
  rationale: string;
  quality_checks: QualityCheck[];
  sample_ratio_mismatch: {
    control_count: number;
    treatment_count: number;
    expected_control: number;
    expected_treatment: number;
    chi_square: number;
    p_value: number;
    has_sample_ratio_mismatch: boolean;
  };
};

export type ExperimentConfig = {
  experiment_name: string;
  hypothesis: string;
  primary_metric: string;
  secondary_metrics: string[];
  guardrail_metrics: string[];
  sample_size_plan: {
    baseline_conversion_rate: number;
    minimum_detectable_effect: number;
    alpha: number;
    power: number;
    visitors_per_day: number;
    sample_size_per_group: number;
    total_sample_size: number;
    estimated_duration_days: number;
  };
};

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000";

async function request<T>(path: string): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${path}`);
  if (!response.ok) {
    throw new Error(`API request failed: ${response.status}`);
  }
  return response.json();
}

export function fetchExperimentResults() {
  return request<ExperimentResults>("/experiment/results");
}

export function fetchExperimentConfig() {
  return request<ExperimentConfig>("/experiment/config");
}
