CREATE TABLE IF NOT EXISTS experiments (
    experiment_id SERIAL PRIMARY KEY,
    experiment_name TEXT NOT NULL,
    hypothesis TEXT NOT NULL,
    primary_metric TEXT NOT NULL,
    started_at DATE NOT NULL,
    ended_at DATE NOT NULL,
    status TEXT NOT NULL CHECK (status IN ('planned', 'running', 'completed', 'launched', 'stopped'))
);

CREATE TABLE IF NOT EXISTS experiment_events (
    event_date DATE NOT NULL,
    user_id TEXT PRIMARY KEY,
    experiment_id INTEGER REFERENCES experiments(experiment_id),
    variant TEXT NOT NULL CHECK (variant IN ('control', 'treatment')),
    channel TEXT NOT NULL,
    device TEXT NOT NULL,
    country TEXT NOT NULL,
    converted INTEGER NOT NULL CHECK (converted IN (0, 1)),
    revenue NUMERIC(12, 2) NOT NULL,
    session_minutes NUMERIC(8, 2) NOT NULL,
    bounced INTEGER NOT NULL CHECK (bounced IN (0, 1)),
    page_load_ms INTEGER NOT NULL,
    refunded INTEGER NOT NULL CHECK (refunded IN (0, 1))
);

CREATE INDEX IF NOT EXISTS idx_experiment_events_variant ON experiment_events(variant);
CREATE INDEX IF NOT EXISTS idx_experiment_events_date ON experiment_events(event_date);
CREATE INDEX IF NOT EXISTS idx_experiment_events_channel ON experiment_events(channel);

CREATE OR REPLACE VIEW experiment_variant_summary AS
SELECT
    variant,
    COUNT(*) AS visitors,
    SUM(converted) AS conversions,
    AVG(converted::NUMERIC) AS conversion_rate,
    SUM(revenue) AS total_revenue,
    AVG(revenue) AS revenue_per_visitor,
    AVG(bounced::NUMERIC) AS bounce_rate,
    AVG(refunded::NUMERIC) AS refund_rate,
    AVG(page_load_ms) AS avg_page_load_ms
FROM experiment_events
GROUP BY variant;
