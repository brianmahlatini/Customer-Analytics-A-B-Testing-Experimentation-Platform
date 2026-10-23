# Customer Analytics & A/B Testing Experimentation Platform

A senior-level statistics and causal inference project that determines whether a new marketing campaign, website change, or sales strategy improves business outcomes. The platform generates synthetic customer experiment data, plans sample size and duration, analyzes treatment versus control groups, checks experiment integrity, and presents a clear launch recommendation with business impact.

## Features

- Synthetic customer-level A/B experiment data with acquisition channels, devices, countries, conversions, revenue, bounce events, refunds, and page-load guardrails
- Measurable hypothesis and primary metric definition for conversion-rate improvement
- Sample size and experiment-duration planning using statistical power analysis
- Treatment and control analysis using proportions z-tests, Welch revenue tests, p-values, and 95% confidence intervals
- Machine learning uplift modeling with conversion propensity, T-learner CATE estimation, and high-uplift segment discovery
- Absolute uplift, relative uplift, conversion lift, revenue-per-visitor lift, and estimated monthly and annual revenue impact
- Sample-ratio mismatch detection using chi-square goodness-of-fit testing
- Data-quality checks for missing values, duplicate assignments, invalid revenue, and variant labels
- FastAPI backend serving experiment configuration, power calculations, generated events, and statistical results
- React TypeScript dashboard with Plotly visualizations for significance, confidence intervals, guardrails, and recommendation
- PostgreSQL schema and reporting methodology notes

## Tech Stack

### Statistics and Analytics

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

### Database and Infrastructure

- PostgreSQL
- SQL
- Docker Compose

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
|   |-- requirements.txt
|-- frontend/
|   |-- src/
|   |   |-- App.tsx
|   |   |-- main.tsx
|   |   |-- components/
|   |   |-- services/
|   |   |-- styles/
|   |-- package.json
|   |-- tsconfig.json
|-- infra/
|   |-- docker-compose.yml
|   |-- schema.sql
|-- reports/
|   |-- experiment_methodology.md
|-- data/
|   |-- .gitkeep
|-- .gitignore
|-- README.md
|-- pytest.ini
```

## Experiment Design

### Business Question

Does a redesigned marketing campaign landing page increase purchases compared with the current page?

### Hypothesis

The new campaign landing page increases completed purchases without harming guardrail metrics.

### Primary Metric

`conversion_rate`

This is calculated as:

```text
conversions / assigned_visitors
```

### Secondary Metric

`revenue_per_visitor`

This is calculated as:

```text
total_revenue / assigned_visitors
```

### Guardrail Metrics

- Bounce rate
- Refund rate
- Average page load time

## Generated Dataset

The data generator creates a deterministic synthetic experiment dataset.

| Field | Description |
| --- | --- |
| `event_date` | Date of user exposure |
| `user_id` | Unique assigned user |
| `variant` | Control or treatment |
| `channel` | Acquisition channel |
| `device` | User device type |
| `country` | Country segment |
| `converted` | Binary purchase outcome |
| `revenue` | Purchase revenue, zero for non-converters |
| `session_minutes` | Session engagement |
| `bounced` | Binary bounce outcome |
| `page_load_ms` | Page load performance guardrail |
| `refunded` | Binary refund guardrail |

Latest generated design:

| Rows | Variants | Allocation | Date Range |
| ---: | --- | --- | --- |
| 48,000 | control, treatment | 50/50 target | 2026-08-31 to 2026-09-27 |

## Statistical Methods

### Sample Size Planning

The platform calculates sample size for a two-sided conversion-rate test using:

- Baseline conversion rate
- Minimum detectable effect
- Alpha level
- Desired power
- Expected visitors per day

Default plan:

| Baseline CVR | MDE | Alpha | Power | Visitors / Day |
| ---: | ---: | ---: | ---: | ---: |
| 8.3% | 1.0 pp | 0.05 | 80% | 1,700 |

### Conversion Test

The primary analysis compares treatment and control conversion rates using a two-proportion z-test. The output includes:

- Control conversion rate
- Treatment conversion rate
- Absolute uplift
- Relative uplift
- 95% confidence interval
- p-value
- Statistical significance flag

### Revenue Test

Revenue per visitor is analyzed using Welch's t-test. The output includes:

- Control revenue per visitor
- Treatment revenue per visitor
- Incremental revenue per visitor
- Relative revenue uplift
- 95% confidence interval
- p-value

### Sample-Ratio Mismatch

The SRM check uses a chi-square goodness-of-fit test against the expected 50/50 allocation. A failed SRM check indicates the experiment assignment or logging pipeline should be investigated before interpreting the result.

## Machine Learning Design

The ML layer is designed for experimentation and causal decision support, not generic prediction.

| Algorithm | Role | Why it fits |
| --- | --- | --- |
| Logistic Regression | Conversion propensity model | Provides an interpretable baseline response model using pre-treatment covariates |
| Random Forest T-Learner | Conversion uplift model | Estimates conditional average treatment effect by comparing predicted treatment and control conversion probabilities |
| Random Forest T-Learner | Revenue uplift model | Estimates incremental revenue per customer for targeting and personalization |
| Segment aggregation | Uplift segment discovery | Ranks channel, device, and country combinations by predicted conversion and revenue lift |

Only pre-treatment assignment features are used for ML targeting: channel, device, country, weekday, weekend flag, and experiment day. Outcome and post-treatment guardrail fields are excluded from uplift features to avoid leakage.

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

| Endpoint | Description |
| --- | --- |
| `GET /health` | API health check |
| `GET /experiment/config` | Hypothesis, metrics, guardrails, and sample-size plan |
| `GET /experiment/power` | Dynamic sample-size calculation |
| `GET /experiment/results` | Experiment results, tests, SRM, guardrails, and recommendation |
| `GET /experiment/ml-insights` | ML model summaries, uplift segments, and targeting recommendation |
| `GET /experiment/events?limit=500` | Generated customer-level event sample |

## Dashboard

The React dashboard presents:

- Experiment recommendation
- Conversion uplift
- Estimated monthly and annual revenue uplift
- Sample-ratio mismatch result
- Power and duration plan
- Conversion-rate chart
- Confidence interval chart
- Statistical results table
- ML uplift model summaries
- Top predicted uplift segments
- Guardrail metrics table
- Data-quality checks

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
