from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd


DATA_PATH = Path(__file__).resolve().parents[3] / "data" / "generated_experiment_events.csv"


def generate_experiment_events(output_path: Path = DATA_PATH, seed: int = 42) -> pd.DataFrame:
    """Generate deterministic customer-level A/B test data."""
    rng = np.random.default_rng(seed)
    n_users = 48_000
    start_date = pd.Timestamp("2026-08-31")
    duration_days = 28

    assigned_variant = rng.choice(["control", "treatment"], size=n_users, p=[0.5, 0.5])
    acquisition_channels = rng.choice(
        ["paid_search", "organic", "email", "social", "affiliate"],
        size=n_users,
        p=[0.30, 0.25, 0.18, 0.17, 0.10],
    )
    device = rng.choice(["mobile", "desktop", "tablet"], size=n_users, p=[0.58, 0.34, 0.08])
    country = rng.choice(["US", "ZA", "GB", "CA", "AU"], size=n_users, p=[0.52, 0.18, 0.12, 0.10, 0.08])
    dates = start_date + pd.to_timedelta(rng.integers(0, duration_days, size=n_users), unit="D")

    channel_lift = pd.Series(acquisition_channels).map(
        {"paid_search": 0.006, "organic": 0.002, "email": 0.016, "social": -0.004, "affiliate": 0.000}
    ).to_numpy()
    device_lift = pd.Series(device).map({"mobile": -0.004, "desktop": 0.006, "tablet": -0.001}).to_numpy()
    base_probability = 0.083 + channel_lift + device_lift
    treatment_effect = np.where(assigned_variant == "treatment", 0.012, 0.0)
    conversion_probability = np.clip(base_probability + treatment_effect, 0.025, 0.18)
    converted = rng.binomial(1, conversion_probability)

    average_order_value = rng.lognormal(mean=3.78, sigma=0.42, size=n_users)
    revenue = np.where(converted == 1, average_order_value, 0.0)
    revenue *= np.where(assigned_variant == "treatment", 1.025, 1.0)

    session_minutes = rng.gamma(shape=2.6, scale=1.8, size=n_users)
    bounce_probability = np.clip(0.42 - converted * 0.20 + (device == "mobile") * 0.05, 0.05, 0.80)
    bounced = rng.binomial(1, bounce_probability)
    page_load_ms = rng.normal(1650, 340, size=n_users) + np.where(assigned_variant == "treatment", 45, 0)
    refund_probability = np.where(converted == 1, 0.025 + (assigned_variant == "treatment") * 0.002, 0.0)
    refunded = rng.binomial(1, refund_probability)

    data = pd.DataFrame(
        {
            "event_date": dates.date.astype(str),
            "user_id": [f"u_{idx:06d}" for idx in range(1, n_users + 1)],
            "variant": assigned_variant,
            "channel": acquisition_channels,
            "device": device,
            "country": country,
            "converted": converted,
            "revenue": np.round(revenue, 2),
            "session_minutes": np.round(session_minutes, 2),
            "bounced": bounced,
            "page_load_ms": np.round(page_load_ms.clip(650, 4200), 0).astype(int),
            "refunded": refunded,
        }
    )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    data.to_csv(output_path, index=False)
    return data


def load_or_generate_events(path: Path = DATA_PATH) -> pd.DataFrame:
    if path.exists():
        return pd.read_csv(path)
    return generate_experiment_events(path)
