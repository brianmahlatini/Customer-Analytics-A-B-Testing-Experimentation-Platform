from app.data.generator import generate_experiment_events
from app.ml.uplift import ml_experiment_insights


def test_ml_insights_include_experiment_appropriate_models(tmp_path):
    data = generate_experiment_events(tmp_path / "events.csv")
    insights = ml_experiment_insights(data)

    model_names = {model["algorithm"] for model in insights["models"]}

    assert "LogisticRegression" in model_names
    assert "T-Learner" in model_names
    assert len(insights["top_uplift_segments"]) > 0
    assert insights["targeting_recommendation"]["top_500_average_revenue_uplift"] > 0
