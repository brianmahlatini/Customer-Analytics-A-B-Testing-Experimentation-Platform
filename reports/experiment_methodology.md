# Experiment Methodology Notes

## Hypothesis

The new marketing campaign landing page increases completed purchases versus the current page without harming customer-experience guardrails.

## Primary Metric

Conversion rate is the primary decision metric because the campaign is designed to increase completed purchases. The analysis uses a two-sided proportions z-test and reports absolute uplift, relative uplift, p-value, and a 95% confidence interval.

## Secondary Metric

Revenue per visitor is measured with a Welch two-sample t-test because the metric is continuous, skewed, and may have unequal variance across treatment and control groups.

## Guardrails

The dashboard tracks bounce rate, refund rate, and average page load time. These metrics are not the launch objective, but they help prevent shipping a treatment that improves conversion by creating operational or customer-experience risk.

## Sample Ratio Mismatch

The SRM check compares observed assignment counts with the expected 50/50 allocation using a chi-square goodness-of-fit test. A very small p-value would indicate assignment, logging, filtering, or exposure problems that should be investigated before interpreting uplift.

## Recommendation Logic

The generated recommendation launches the treatment only when the primary conversion result is statistically significant and revenue impact is positive.
