from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import mean_absolute_error, roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler


CATEGORICAL_FEATURES = ["channel", "device", "country", "weekday", "is_weekend"]
NUMERIC_FEATURES = ["experiment_day"]


def _feature_frame(events: pd.DataFrame) -> pd.DataFrame:
    features = events.copy()
    dates = pd.to_datetime(features["event_date"])
    features["weekday"] = dates.dt.day_name()
    features["is_weekend"] = dates.dt.dayofweek.isin([5, 6]).astype(int).astype(str)
    features["experiment_day"] = (dates - dates.min()).dt.days
    return features[CATEGORICAL_FEATURES + NUMERIC_FEATURES]


def _preprocessor() -> ColumnTransformer:
    return ColumnTransformer(
        transformers=[
            ("categorical", OneHotEncoder(handle_unknown="ignore"), CATEGORICAL_FEATURES),
            ("numeric", StandardScaler(), NUMERIC_FEATURES),
        ]
    )


def _classification_pipeline(model) -> Pipeline:
    return Pipeline([("preprocess", _preprocessor()), ("model", model)])


def _regression_pipeline(model) -> Pipeline:
    return Pipeline([("preprocess", _preprocessor()), ("model", model)])


def response_propensity_model(events: pd.DataFrame) -> dict:
    x = _feature_frame(events)
    y = events["converted"].astype(int)
    x_train, x_test, y_train, y_test = train_test_split(
        x,
        y,
        test_size=0.25,
        random_state=42,
        stratify=y,
    )
    model = _classification_pipeline(LogisticRegression(max_iter=800, class_weight="balanced"))
    model.fit(x_train, y_train)
    probabilities = model.predict_proba(x_test)[:, 1]

    return {
        "algorithm": "LogisticRegression",
        "purpose": "Predict baseline conversion propensity for covariate-adjusted customer analytics.",
        "target": "converted",
        "features": CATEGORICAL_FEATURES + NUMERIC_FEATURES,
        "holdout_auc": float(roc_auc_score(y_test, probabilities)),
    }


def treatment_uplift_models(events: pd.DataFrame) -> tuple[dict, pd.DataFrame]:
    x = _feature_frame(events)
    treatment_mask = events["variant"] == "treatment"
    control_mask = events["variant"] == "control"

    conversion_control = _classification_pipeline(
        RandomForestClassifier(
            n_estimators=120,
            max_depth=7,
            min_samples_leaf=80,
            random_state=42,
            class_weight="balanced_subsample",
            n_jobs=-1,
        )
    )
    conversion_treatment = _classification_pipeline(
        RandomForestClassifier(
            n_estimators=120,
            max_depth=7,
            min_samples_leaf=80,
            random_state=43,
            class_weight="balanced_subsample",
            n_jobs=-1,
        )
    )
    revenue_control = _regression_pipeline(
        RandomForestRegressor(
            n_estimators=140,
            max_depth=8,
            min_samples_leaf=70,
            random_state=44,
            n_jobs=-1,
        )
    )
    revenue_treatment = _regression_pipeline(
        RandomForestRegressor(
            n_estimators=140,
            max_depth=8,
            min_samples_leaf=70,
            random_state=45,
            n_jobs=-1,
        )
    )

    conversion_control.fit(x.loc[control_mask], events.loc[control_mask, "converted"])
    conversion_treatment.fit(x.loc[treatment_mask], events.loc[treatment_mask, "converted"])
    revenue_control.fit(x.loc[control_mask], events.loc[control_mask, "revenue"])
    revenue_treatment.fit(x.loc[treatment_mask], events.loc[treatment_mask, "revenue"])

    control_conversion_probability = conversion_control.predict_proba(x)[:, 1]
    treatment_conversion_probability = conversion_treatment.predict_proba(x)[:, 1]
    control_revenue_prediction = revenue_control.predict(x)
    treatment_revenue_prediction = revenue_treatment.predict(x)

    scored = events[["user_id", "variant", "channel", "device", "country"]].copy()
    scored["predicted_control_conversion"] = control_conversion_probability
    scored["predicted_treatment_conversion"] = treatment_conversion_probability
    scored["predicted_conversion_uplift"] = treatment_conversion_probability - control_conversion_probability
    scored["predicted_control_revenue"] = control_revenue_prediction
    scored["predicted_treatment_revenue"] = treatment_revenue_prediction
    scored["predicted_revenue_uplift"] = treatment_revenue_prediction - control_revenue_prediction

    conversion_mae = float(
        np.mean(
            np.abs(
                np.where(treatment_mask, treatment_conversion_probability, control_conversion_probability)
                - events["converted"].to_numpy()
            )
        )
    )
    revenue_mae = float(
        mean_absolute_error(
            events["revenue"],
            np.where(treatment_mask, treatment_revenue_prediction, control_revenue_prediction),
        )
    )

    metadata = {
        "algorithm": "T-Learner",
        "conversion_base_estimator": "RandomForestClassifier",
        "revenue_base_estimator": "RandomForestRegressor",
        "purpose": "Estimate customer-level conditional average treatment effects for conversion and revenue.",
        "features": CATEGORICAL_FEATURES + NUMERIC_FEATURES,
        "conversion_probability_mae": conversion_mae,
        "revenue_mae": revenue_mae,
    }
    return metadata, scored


def uplift_segments(scored: pd.DataFrame) -> list[dict]:
    grouped = (
        scored.groupby(["channel", "device", "country"], as_index=False)
        .agg(
            customers=("user_id", "count"),
            predicted_conversion_uplift=("predicted_conversion_uplift", "mean"),
            predicted_revenue_uplift=("predicted_revenue_uplift", "mean"),
        )
        .query("customers >= 100")
        .sort_values(["predicted_revenue_uplift", "predicted_conversion_uplift"], ascending=False)
        .head(10)
    )
    return grouped.to_dict(orient="records")


def model_recommendations(scored: pd.DataFrame) -> dict:
    high_uplift = scored.sort_values("predicted_revenue_uplift", ascending=False).head(500)
    low_uplift = scored.sort_values("predicted_revenue_uplift", ascending=True).head(500)

    return {
        "best_targeting_rule": "Prioritize segments with positive predicted conversion and revenue uplift.",
        "top_500_average_conversion_uplift": float(high_uplift["predicted_conversion_uplift"].mean()),
        "top_500_average_revenue_uplift": float(high_uplift["predicted_revenue_uplift"].mean()),
        "bottom_500_average_conversion_uplift": float(low_uplift["predicted_conversion_uplift"].mean()),
        "bottom_500_average_revenue_uplift": float(low_uplift["predicted_revenue_uplift"].mean()),
        "policy": "Launch broadly if A/B test is significant; use uplift segments for campaign targeting and personalization.",
    }


def ml_experiment_insights(events: pd.DataFrame) -> dict:
    propensity = response_propensity_model(events)
    uplift_model, scored = treatment_uplift_models(events)

    return {
        "models": [propensity, uplift_model],
        "top_uplift_segments": uplift_segments(scored),
        "targeting_recommendation": model_recommendations(scored),
    }
