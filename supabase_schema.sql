-- Supabase Schema for The Break-down Breakdown
-- Run this in the Supabase SQL Editor

-- Field Reports Table (anonymous survey responses)
CREATE TABLE field_reports (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    
    -- Survey responses
    call_volume INTEGER CHECK (call_volume BETWEEN 1 AND 5),
    parts_lead_time INTEGER CHECK (parts_lead_time BETWEEN 1 AND 60),
    trying_to_hire BOOLEAN,
    hiring_difficulty INTEGER CHECK (hiring_difficulty BETWEEN 1 AND 5),
    business_sentiment INTEGER CHECK (business_sentiment BETWEEN 1 AND 5),
    region TEXT,
    company_size TEXT,
    
    -- Metadata (no identifying info)
    month TEXT  -- e.g., "2025-12"
);

-- Index for querying by month
CREATE INDEX idx_field_reports_month ON field_reports(month);
CREATE INDEX idx_field_reports_region ON field_reports(region);

-- Email Subscribers Table (stored separately from survey data)
CREATE TABLE email_subscribers (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    email TEXT UNIQUE NOT NULL,
    subscribed BOOLEAN DEFAULT TRUE
);

-- Indicator Cache Table (for FRED data caching)
CREATE TABLE indicator_cache (
    id TEXT PRIMARY KEY,  -- e.g., "UMCSENT"
    value NUMERIC,
    fetched_at TIMESTAMPTZ DEFAULT NOW()
);

-- Monthly Index Snapshots (historical record)
CREATE TABLE index_snapshots (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    month TEXT UNIQUE NOT NULL,  -- e.g., "2025-12"
    score NUMERIC NOT NULL,
    
    -- Component scores for transparency
    economic_score NUMERIC,
    industry_score NUMERIC,
    field_score NUMERIC,
    
    -- Snapshot of key metrics
    report_count INTEGER,
    metrics JSONB,
    
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Row Level Security (RLS)
-- Enable RLS on all tables
ALTER TABLE field_reports ENABLE ROW LEVEL SECURITY;
ALTER TABLE email_subscribers ENABLE ROW LEVEL SECURITY;
ALTER TABLE indicator_cache ENABLE ROW LEVEL SECURITY;
ALTER TABLE index_snapshots ENABLE ROW LEVEL SECURITY;

-- Policies: Allow anonymous inserts for field reports
CREATE POLICY "Allow anonymous field report submissions"
ON field_reports FOR INSERT
TO anon
WITH CHECK (true);

-- Policies: Allow reading aggregated data (not individual reports)
-- Note: We'll use edge functions or server-side queries for aggregation
CREATE POLICY "Allow reading index snapshots"
ON index_snapshots FOR SELECT
TO anon
USING (true);

-- Policies: Allow email signup
CREATE POLICY "Allow email signup"
ON email_subscribers FOR INSERT
TO anon
WITH CHECK (true);

-- View for aggregated monthly metrics (safe to expose)
CREATE VIEW monthly_metrics AS
SELECT 
    month,
    COUNT(*) as report_count,
    ROUND(AVG(call_volume)::numeric, 2) as avg_call_volume,
    ROUND(AVG(parts_lead_time)::numeric, 1) as avg_parts_lead_time,
    ROUND(AVG(business_sentiment)::numeric, 2) as avg_business_sentiment,
    ROUND(AVG(hiring_difficulty) FILTER (WHERE hiring_difficulty IS NOT NULL)::numeric, 2) as avg_hiring_difficulty
FROM field_reports
GROUP BY month
HAVING COUNT(*) >= 10;  -- Only show when 10+ responses for privacy

-- Regional metrics view (only when enough data)
CREATE VIEW regional_metrics AS
SELECT 
    month,
    region,
    COUNT(*) as report_count,
    ROUND(AVG(call_volume)::numeric, 2) as avg_call_volume,
    ROUND(AVG(business_sentiment)::numeric, 2) as avg_business_sentiment
FROM field_reports
GROUP BY month, region
HAVING COUNT(*) >= 10;  -- Privacy threshold

