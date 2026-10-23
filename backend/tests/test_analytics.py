import pandas as pd

from app.analytics.quality import sample_ratio_mismatch
from app.analytics.statistics import conversion_test, experiment_results
from app.data.generator import generate_experiment_events


def test_generated_experiment_has_expected_variants(tmp_path):
    data = generate_experiment_events(tmp_path / "events.csv")

    assert set(data["variant"].unique()) == {"control", "treatment"}
    assert len(data) == 48_000
    assert data["user_id"].is_unique


def test_conversion_test_returns_uplift(tmp_path):
    data = generate_experiment_events(tmp_path / "events.csv")
    result = conversion_test(data)

    assert result["metric"] == "conversion_rate"
    assert result["treatment_value"] > result["control_value"]
    assert result["confidence_interval_low"] < result["absolute_uplift"] < result["confidence_interval_high"]


def test_sample_ratio_mismatch_passes_for_balanced_data():
    events = pd.DataFrame({"variant": ["control"] * 1000 + ["treatment"] * 1002})
    result = sample_ratio_mismatch(events)

    assert result["has_sample_ratio_mismatch"] is False


def test_experiment_results_contains_recommendation(tmp_path):
    data = generate_experiment_events(tmp_path / "events.csv")
    result = experiment_results(data)

    assert result["primary_metric"] == "conversion_rate"
    assert "recommendation" in result
