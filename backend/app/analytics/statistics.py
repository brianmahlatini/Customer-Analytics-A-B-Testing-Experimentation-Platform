from __future__ import annotations

import numpy as np
import pandas as pd
from scipy import stats
from statsmodels.stats.proportion import confint_proportions_2indep, proportions_ztest


def _variant_frame(events: pd.DataFrame, variant: str) -> pd.DataFrame:
    return events.loc[events["variant"] == variant].copy()


def summarize_variants(events: pd.DataFrame) -> list[dict]:
    summary = []
    for variant, frame in events.groupby("variant"):
        visitors = len(frame)
        conversions = int(frame["converted"].sum())
        revenue = float(frame["revenue"].sum())
        summary.append(
            {
                "variant": variant,
                "visitors": visitors,
                "conversions": conversions,
                "conversion_rate": conversions / visitors,
                "total_revenue": revenue,
                "revenue_per_visitor": revenue / visitors,
                "average_order_value": revenue / conversions if conversions else 0.0,
                "bounce_rate": float(frame["bounced"].mean()),
                "refund_rate": float(frame["refunded"].mean()),
                "avg_page_load_ms": float(frame["page_load_ms"].mean()),
            }
        )
    return sorted(summary, key=lambda item: item["variant"])


def conversion_test(events: pd.DataFrame) -> dict:
    control = _variant_frame(events, "control")
    treatment = _variant_frame(events, "treatment")
    control_conversions = int(control["converted"].sum())
    treatment_conversions = int(treatment["converted"].sum())
    control_n = len(control)
    treatment_n = len(treatment)

    z_stat, p_value = proportions_ztest(
        [treatment_conversions, control_conversions],
        [treatment_n, control_n],
        alternative="two-sided",
    )
    ci_low, ci_high = confint_proportions_2indep(
        treatment_conversions,
        treatment_n,
        control_conversions,
        control_n,
        method="wald",
    )
    control_rate = control_conversions / control_n
    treatment_rate = treatment_conversions / treatment_n
    absolute_uplift = treatment_rate - control_rate
    relative_uplift = absolute_uplift / control_rate

    return {
        "metric": "conversion_rate",
        "control_value": control_rate,
        "treatment_value": treatment_rate,
        "absolute_uplift": absolute_uplift,
        "relative_uplift": relative_uplift,
        "confidence_interval_low": float(ci_low),
        "confidence_interval_high": float(ci_high),
        "p_value": float(p_value),
        "test_statistic": float(z_stat),
        "is_significant": bool(p_value < 0.05),
    }


def revenue_test(events: pd.DataFrame) -> dict:
    control = _variant_frame(events, "control")["revenue"].to_numpy()
    treatment = _variant_frame(events, "treatment")["revenue"].to_numpy()
    t_stat, p_value = stats.ttest_ind(treatment, control, equal_var=False)

    difference = treatment.mean() - control.mean()
    control_var = control.var(ddof=1)
    treatment_var = treatment.var(ddof=1)
    standard_error = np.sqrt(control_var / len(control) + treatment_var / len(treatment))
    df_num = (control_var / len(control) + treatment_var / len(treatment)) ** 2
    df_den = ((control_var / len(control)) ** 2 / (len(control) - 1)) + (
        (treatment_var / len(treatment)) ** 2 / (len(treatment) - 1)
    )
    degrees_freedom = df_num / df_den
    margin = stats.t.ppf(0.975, degrees_freedom) * standard_error
    relative_uplift = difference / control.mean()

    return {
        "metric": "revenue_per_visitor",
        "control_value": float(control.mean()),
        "treatment_value": float(treatment.mean()),
        "absolute_uplift": float(difference),
        "relative_uplift": float(relative_uplift),
        "confidence_interval_low": float(difference - margin),
        "confidence_interval_high": float(difference + margin),
        "p_value": float(p_value),
        "test_statistic": float(t_stat),
        "is_significant": bool(p_value < 0.05),
    }


def guardrail_metrics(events: pd.DataFrame) -> list[dict]:
    metrics = []
    for column, label in [
        ("bounce_rate", "bounce_rate"),
        ("refund_rate", "refund_rate"),
        ("avg_page_load_ms", "avg_page_load_ms"),
    ]:
        summaries = {item["variant"]: item for item in summarize_variants(events)}
        control_value = summaries["control"][column]
        treatment_value = summaries["treatment"][column]
        delta = treatment_value - control_value
        metrics.append(
            {
                "metric": label,
                "control_value": control_value,
                "treatment_value": treatment_value,
                "absolute_delta": delta,
                "relative_delta": delta / control_value if control_value else 0.0,
                "status": "watch" if label == "avg_page_load_ms" and delta > 100 else "pass",
            }
        )
    return metrics


def business_impact(events: pd.DataFrame, monthly_visitors: int = 180_000) -> dict:
    revenue = revenue_test(events)
    monthly_incremental_revenue = revenue["absolute_uplift"] * monthly_visitors
    annual_incremental_revenue = monthly_incremental_revenue * 12
    return {
        "monthly_visitors": monthly_visitors,
        "incremental_revenue_per_visitor": revenue["absolute_uplift"],
        "estimated_monthly_revenue_uplift": monthly_incremental_revenue,
        "estimated_annual_revenue_uplift": annual_incremental_revenue,
    }


def experiment_results(events: pd.DataFrame) -> dict:
    conversion = conversion_test(events)
    revenue = revenue_test(events)
    impact = business_impact(events)
    recommendation = (
        "Launch the treatment"
        if conversion["is_significant"] and revenue["absolute_uplift"] > 0
        else "Do not launch yet"
    )
    rationale = (
        "The treatment improves the primary conversion metric with positive revenue impact."
        if recommendation == "Launch the treatment"
        else "The observed lift is not strong enough relative to uncertainty and business risk."
    )

    return {
        "hypothesis": "A redesigned campaign landing page increases completed purchases versus the current page.",
        "primary_metric": "conversion_rate",
        "secondary_metric": "revenue_per_visitor",
        "variant_summary": summarize_variants(events),
        "conversion_test": conversion,
        "revenue_test": revenue,
        "guardrails": guardrail_metrics(events),
        "business_impact": impact,
        "recommendation": recommendation,
        "rationale": rationale,
    }
