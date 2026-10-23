from __future__ import annotations

from dataclasses import dataclass

from statsmodels.stats.power import NormalIndPower
from statsmodels.stats.proportion import proportion_effectsize


@dataclass(frozen=True)
class SampleSizePlan:
    baseline_conversion_rate: float
    minimum_detectable_effect: float
    alpha: float
    power: float
    visitors_per_day: int
    sample_size_per_group: int
    total_sample_size: int
    estimated_duration_days: int


def calculate_conversion_sample_size(
    baseline_conversion_rate: float = 0.083,
    minimum_detectable_effect: float = 0.01,
    alpha: float = 0.05,
    power: float = 0.80,
    visitors_per_day: int = 1700,
) -> SampleSizePlan:
    treatment_rate = baseline_conversion_rate + minimum_detectable_effect
    effect_size = proportion_effectsize(baseline_conversion_rate, treatment_rate)
    analysis = NormalIndPower()
    per_group = analysis.solve_power(
        effect_size=effect_size,
        alpha=alpha,
        power=power,
        ratio=1.0,
        alternative="two-sided",
    )
    sample_size_per_group = int(per_group) + 1
    total_sample_size = sample_size_per_group * 2
    estimated_duration_days = int((total_sample_size + visitors_per_day - 1) / visitors_per_day)

    return SampleSizePlan(
        baseline_conversion_rate=baseline_conversion_rate,
        minimum_detectable_effect=minimum_detectable_effect,
        alpha=alpha,
        power=power,
        visitors_per_day=visitors_per_day,
        sample_size_per_group=sample_size_per_group,
        total_sample_size=total_sample_size,
        estimated_duration_days=estimated_duration_days,
    )
