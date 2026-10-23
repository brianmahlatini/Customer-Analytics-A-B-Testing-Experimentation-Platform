from __future__ import annotations

from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware

from app.analytics.quality import data_quality_checks, sample_ratio_mismatch
from app.analytics.sample_size import calculate_conversion_sample_size
from app.analytics.statistics import experiment_results
from app.data.generator import load_or_generate_events


app = FastAPI(
    title="Customer Analytics & A/B Testing Experimentation API",
    version="1.0.0",
    description="Statistical testing, power planning, data quality checks, and uplift estimation for A/B tests.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "service": "experimentation-api"}


@app.get("/experiment/config")
def experiment_config() -> dict:
    plan = calculate_conversion_sample_size()
    return {
        "experiment_name": "Campaign Landing Page Checkout Lift Test",
        "hypothesis": "The new campaign landing page increases completed purchases without harming guardrail metrics.",
        "primary_metric": "conversion_rate",
        "secondary_metrics": ["revenue_per_visitor", "average_order_value"],
        "guardrail_metrics": ["bounce_rate", "refund_rate", "avg_page_load_ms"],
        "sample_size_plan": plan.__dict__,
    }


@app.get("/experiment/power")
def experiment_power(
    baseline_conversion_rate: float = Query(0.083, gt=0, lt=1),
    minimum_detectable_effect: float = Query(0.01, gt=0, lt=1),
    alpha: float = Query(0.05, gt=0, lt=1),
    power: float = Query(0.80, gt=0, lt=1),
    visitors_per_day: int = Query(1700, gt=0),
) -> dict:
    return calculate_conversion_sample_size(
        baseline_conversion_rate=baseline_conversion_rate,
        minimum_detectable_effect=minimum_detectable_effect,
        alpha=alpha,
        power=power,
        visitors_per_day=visitors_per_day,
    ).__dict__


@app.get("/experiment/results")
def results() -> dict:
    events = load_or_generate_events()
    payload = experiment_results(events)
    payload["quality_checks"] = data_quality_checks(events)
    payload["sample_ratio_mismatch"] = sample_ratio_mismatch(events)
    return payload


@app.get("/experiment/events")
def events(limit: int = Query(500, gt=0, le=5000)) -> list[dict]:
    data = load_or_generate_events()
    return data.head(limit).to_dict(orient="records")
