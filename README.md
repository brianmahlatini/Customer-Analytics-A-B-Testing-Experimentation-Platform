# Customer Analytics & A/B Testing Experimentation Platform

A senior-level full-stack statistics, causal inference, and machine learning project that determines whether a new marketing campaign, website change, or sales strategy actually improves business outcomes. The platform plans experiments, generates customer-level A/B test data, analyzes treatment and control groups, checks experiment integrity, estimates uplift, applies appropriate uplift modeling algorithms, and presents a clear launch recommendation.

## Features

- Synthetic customer-level A/B experiment data generation with acquisition channel, device, country, conversion, revenue, bounce, refund, and page-load metrics
- Measurable hypothesis definition with primary, secondary, and guardrail metrics
- Sample size and experiment duration calculation using statistical power analysis
- Treatment and control analysis using proportions z-tests, Welch revenue tests, p-values, and 95% confidence intervals
- Absolute uplift, relative uplift, conversion lift, revenue-per-visitor lift, and estimated monthly and annual revenue impact
- Sample-ratio mismatch detection using chi-square goodness-of-fit testing
- Data-quality checks for missing values, duplicate user assignments, invalid revenue, and variant labels
- Machine learning layer with conversion propensity modeling and T-learner uplift modeling
- Segment-level CATE ranking for high-uplift customer targeting
- FastAPI backend for experiment configuration, power planning, results, events, and ML insights
- React TypeScript dashboard for statistical significance, confidence intervals, guardrails, uplift, and targeting recommendations
- PostgreSQL schema and reporting methodology notes

## Tech Stack

### Statistics, Causal Inference, and Machine Learning

- Python
- pandas
- NumPy
- SciPy
- statsmodels
- scikit-learn

### Backend

- FastAPI
- Uvicorn
- pytest

### Frontend

- React
- TypeScript
- Vite
- Plotly
- Lucide React

### Database and Reporting

- PostgreSQL schema
- SQL
- Docker Compose
- Experiment methodology notes

## Project Structure

```text
.
|-- backend/
|   |-- app/
|   |   |-- main.py
|   |   |-- analytics/
|   |   |   |-- quality.py
|   |   |   |-- sample_size.py
|   |   |   |-- statistics.py
|   |   |-- data/
|   |   |   |-- generator.py
|   |   |-- ml/
|   |   |   |-- uplift.py
|   |-- scripts/
|   |   |-- generate_data.py
|   |-- tests/
|   |   |-- test_analytics.py
|   |   |-- test_api.py
|   |   |-- test_ml.py
|   |-- requirements.txt
|-- data/
|   |-- generated_experiment_events.csv
|-- frontend/
|   |-- src/
|   |   |-- App.tsx
|   |   |-- main.tsx
|   |   |-- components/
|   |   |   |-- ExperimentSummary.tsx
|   |   |   |-- GuardrailTable.tsx
|   |   |   |-- MetricCard.tsx
|   |   |   |-- MlInsightsPanel.tsx
|   |   |   |-- ResultsTable.tsx
|   |   |   |-- SampleSizePanel.tsx
|   |   |   |-- UpliftChart.tsx
|   |   |-- services/
|   |   |   |-- api.ts
|   |   |-- styles/
|   |   |   |-- app.css
|   |-- package.json
|   |-- tsconfig.json
|-- infra/
|   |-- docker-compose.yml
|   |-- schema.sql
|-- reports/
|   |-- experiment_methodology.md
|-- .gitignore
|-- pytest.ini
|-- README.md
```

## Experiment Design

### Business Question

Does a redesigned marketing campaign landing page increase purchases compared with the current page?

### Hypothesis

The new campaign landing page increases completed purchases without harming customer-experience guardrails.

### Primary Metric

`conversion_rate`

```text
conversions / assigned_visitors
```

### Secondary Metric

`revenue_per_visitor`

```text
total_revenue / assigned_visitors
```

### Guardrail Metrics

- Bounce rate
- Refund rate
- Average page load time

## Dataset

The data generator creates a deterministic customer-level experiment dataset with:

- Customer assignment: user ID, variant, exposure date
- Customer profile: acquisition channel, device, country
- Conversion outcome: binary purchase flag
- Revenue outcome: purchase revenue, zero for non-converters
- Engagement signal: session duration and bounce flag
- Guardrail signals: page-load time and refund flag

Latest generated dataset:

| Rows | Control Users | Treatment Users | Allocation | Date Range |
| ---: | ---: | ---: | --- | --- |
| 48,000 | 23,850 | 24,150 | 50/50 target | 2026-08-31 to 2026-09-27 |

## Features X

The ML uplift layer uses only pre-treatment or assignment-time features:

- Acquisition channel
- Device type
- Country
- Weekday
- Weekend flag
- Experiment day

Outcome fields such as conversion, revenue, refunds, bounce, and page-load results are excluded from model features to avoid leakage.

## Target y

Primary experiment target:

```text
converted = 1 when the assigned user completes a purchase
converted = 0 otherwise
```

Secondary business target:

```text
revenue = customer revenue generated after assignment
```

## Statistical Tests

The platform analyzes the A/B test with:

- Two-proportion z-test for conversion-rate difference
- Welch two-sample t-test for revenue-per-visitor difference
- 95% confidence intervals for uplift uncertainty
- Chi-square goodness-of-fit test for sample-ratio mismatch
- Data-quality checks before interpreting results

Latest statistical result:

| Metric | Control | Treatment | Absolute Uplift | Relative Uplift | p-value | 95% CI |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| Conversion rate | 8.65% | 10.09% | 1.44 pp | 16.60% | 0.00000007 | 0.92 pp to 1.96 pp |
| Revenue / visitor | $4.12 | $4.99 | $0.88 | 21.37% | 0.0000000006 | $0.60 to $1.16 |

Sample-ratio mismatch result:

| Control Count | Treatment Count | Expected Split | SRM p-value | Status |
| ---: | ---: | --- | ---: | --- |
| 23,850 | 24,150 | 50/50 | 0.1709 | Passed |

Estimated revenue impact:

| Monthly Visitors | Incremental Revenue / Visitor | Monthly Revenue Uplift | Annual Revenue Uplift |
| ---: | ---: | ---: | ---: |
| 180,000 | $0.88 | $158,324 | $1,899,889 |

Recommendation:

```text
Launch the treatment.
```

## ML Design

The machine learning layer is designed for experimentation and causal decision support, not generic prediction.

### Models Used

- LogisticRegression baseline conversion propensity model
- RandomForestClassifier T-learner for conversion uplift
- RandomForestRegressor T-learner for revenue uplift
- Segment aggregation for high-uplift targeting recommendations

### Why These Algorithms Fit

- Logistic Regression is interpretable and works well as a baseline conversion propensity model.
- T-learners are appropriate for A/B testing because they model treatment and control outcomes separately, then estimate customer-level conditional average treatment effects.
- Random Forest models capture non-linear segment interactions across channel, device, country, and time.
- Segment aggregation turns individual uplift estimates into practical campaign-targeting recommendations.

Latest ML run:

| Model | Purpose | Metric |
| --- | --- | ---: |
| LogisticRegression | Baseline conversion propensity | Holdout AUC: 0.515 |
| T-Learner with RandomForestClassifier | Conversion uplift estimation | Probability MAE: 0.492 |
| T-Learner with RandomForestRegressor | Revenue uplift estimation | Revenue MAE: $8.19 |

Top predicted uplift segments:

| Channel | Device | Country | Customers | Predicted CVR Uplift | Predicted Revenue Uplift |
| --- | --- | --- | ---: | ---: | ---: |
| email | desktop | AU | 242 | 4.33% | $3.34 |
| email | desktop | ZA | 504 | 5.43% | $2.44 |
| paid_search | desktop | AU | 397 | 4.92% | $2.31 |

## Local Setup

### 1. Backend

```bash
python -m pip install -r backend/requirements.txt
python backend/scripts/generate_data.py
uvicorn app.main:app --app-dir backend --reload
```

Backend API:

```text
http://localhost:8000/health
```

### 2. Frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend dashboard:

```text
http://localhost:5173
```

Set `VITE_API_BASE_URL` if the backend runs on a different host or port.

### 3. Optional PostgreSQL

```bash
docker compose -f infra/docker-compose.yml up -d
```

## API Endpoints

```text
GET /health
GET /experiment/config
GET /experiment/power
GET /experiment/results
GET /experiment/ml-insights
GET /experiment/events?limit=500
```

The experiment results response includes:

- Hypothesis and primary metric
- Variant summaries
- Conversion statistical test
- Revenue statistical test
- Guardrail metrics
- Sample-ratio mismatch check
- Data-quality checks
- Estimated business impact
- Launch recommendation

The ML insights response includes:

- Model names and model purposes
- Propensity model quality
- Uplift model quality
- Top uplift segments
- Targeting recommendation

## Dashboard

The React dashboard presents:

- Recommendation summary
- Conversion and revenue uplift
- Estimated monthly and annual revenue impact
- Power and sample-size plan
- Conversion-rate chart
- Confidence interval chart
- Statistical results table
- ML uplift model summaries
- Top predicted uplift segments
- Guardrail metrics
- Data-quality checks

## Regenerating Data

Run:

```bash
python backend/scripts/generate_data.py
```

This regenerates:

- Synthetic customer-level experiment data
- Treatment and control assignments
- Conversion outcomes
- Revenue outcomes
- Engagement and guardrail metrics

## Testing

Run backend tests:

```bash
pytest
```

Run frontend production build:

```bash
cd frontend
npm run build
```

## Repository

Owner: brianmahlatini

Repository: Customer-Analytics-A-B-Testing-Experimentation-Platform

GitHub: Customer-Analytics-A-B-Testing-Experimentation-Platform
