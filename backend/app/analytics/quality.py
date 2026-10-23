from __future__ import annotations

import pandas as pd
from scipy.stats import chisquare


def sample_ratio_mismatch(events: pd.DataFrame, expected_ratio: tuple[float, float] = (0.5, 0.5)) -> dict:
    counts = events["variant"].value_counts().reindex(["control", "treatment"], fill_value=0)
    total = counts.sum()
    expected = [total * expected_ratio[0], total * expected_ratio[1]]
    statistic, p_value = chisquare(counts.to_numpy(), f_exp=expected)

    return {
        "control_count": int(counts["control"]),
        "treatment_count": int(counts["treatment"]),
        "expected_control": round(expected[0], 2),
        "expected_treatment": round(expected[1], 2),
        "chi_square": round(float(statistic), 4),
        "p_value": round(float(p_value), 6),
        "has_sample_ratio_mismatch": bool(p_value < 0.001),
    }


def data_quality_checks(events: pd.DataFrame) -> list[dict]:
    checks = []
    checks.append(
        {
            "check": "Missing values",
            "status": "pass" if int(events.isna().sum().sum()) == 0 else "fail",
            "details": f"{int(events.isna().sum().sum())} missing cells",
        }
    )
    duplicate_users = int(events["user_id"].duplicated().sum())
    checks.append(
        {
            "check": "Duplicate user assignments",
            "status": "pass" if duplicate_users == 0 else "fail",
            "details": f"{duplicate_users} duplicate user IDs",
        }
    )
    invalid_revenue = int(((events["converted"] == 0) & (events["revenue"] > 0)).sum())
    checks.append(
        {
            "check": "Revenue consistency",
            "status": "pass" if invalid_revenue == 0 else "fail",
            "details": f"{invalid_revenue} non-converters with revenue",
        }
    )
    variants = sorted(events["variant"].unique().tolist())
    checks.append(
        {
            "check": "Variant labels",
            "status": "pass" if variants == ["control", "treatment"] else "fail",
            "details": ", ".join(variants),
        }
    )
    return checks
