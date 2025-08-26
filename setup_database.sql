-- SocialSeed v2.0 Database Setup
-- Run this in your Supabase SQL Editor

-- Enable necessary extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Users table
CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email VARCHAR(255) UNIQUE NOT NULL,
    username VARCHAR(100) UNIQUE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Social accounts table
CREATE TABLE IF NOT EXISTS social_accounts (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    platform VARCHAR(50) NOT NULL CHECK (platform IN ('tiktok', 'instagram', 'twitter')),
    username VARCHAR(255) NOT NULL,
    access_token TEXT NOT NULL,
    refresh_token TEXT,
    phase INTEGER DEFAULT 1 CHECK (phase >= 1 AND phase <= 3),
    health_score INTEGER DEFAULT 100 CHECK (health_score >= 0 AND health_score <= 100),
    is_active BOOLEAN DEFAULT true,
    last_action_time TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(platform, username)
);

-- Phase progressions table
CREATE TABLE IF NOT EXISTS phase_progressions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    account_id UUID REFERENCES social_accounts(id) ON DELETE CASCADE,
    from_phase INTEGER NOT NULL,
    to_phase INTEGER NOT NULL,
    progression_date TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    reason TEXT,
    approved_by UUID REFERENCES users(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Account health logs table
CREATE TABLE IF NOT EXISTS account_health_logs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    account_id UUID REFERENCES social_accounts(id) ON DELETE CASCADE,
    health_score INTEGER NOT NULL CHECK (health_score >= 0 AND health_score <= 100),
    rate_limit_status VARCHAR(50) DEFAULT 'normal',
    last_action_time TIMESTAMP WITH TIME ZONE,
    notes TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Approval requests table
CREATE TABLE IF NOT EXISTS approval_requests (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    account_id UUID REFERENCES social_accounts(id) ON DELETE CASCADE,
    action_type VARCHAR(100) NOT NULL,
    target_identifier VARCHAR(255),
    risk_score DECIMAL(3,2) CHECK (risk_score >= 0 AND risk_score <= 1),
    status VARCHAR(50) DEFAULT 'pending' CHECK (status IN ('pending', 'approved', 'rejected')),
    requested_by UUID REFERENCES users(id),
    reviewed_by UUID REFERENCES users(id),
    review_notes TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Safety assessments table
CREATE TABLE IF NOT EXISTS safety_assessments (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    account_id UUID REFERENCES social_accounts(id) ON DELETE CASCADE,
    assessment_type VARCHAR(100) NOT NULL,
    risk_score DECIMAL(3,2) CHECK (risk_score >= 0 AND risk_score <= 1),
    ai_provider VARCHAR(100),
    assessment_data JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Platform health table
CREATE TABLE IF NOT EXISTS platform_health (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    platform VARCHAR(50) NOT NULL,
    status VARCHAR(50) DEFAULT 'healthy' CHECK (status IN ('healthy', 'warning', 'critical')),
    health_score INTEGER DEFAULT 100 CHECK (health_score >= 0 AND health_score <= 100),
    last_check TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    error_count INTEGER DEFAULT 0,
    rate_limit_status VARCHAR(50) DEFAULT 'normal',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Action history table
CREATE TABLE IF NOT EXISTS action_history (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    account_id UUID REFERENCES social_accounts(id) ON DELETE CASCADE,
    action_type VARCHAR(100) NOT NULL,
    platform VARCHAR(50) NOT NULL,
    target_identifier VARCHAR(255),
    status VARCHAR(50) DEFAULT 'pending' CHECK (status IN ('pending', 'completed', 'failed', 'cancelled')),
    risk_score DECIMAL(3,2) CHECK (risk_score >= 0 AND risk_score <= 1),
    execution_time TIMESTAMP WITH TIME ZONE,
    response_data JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Behavior sessions table
CREATE TABLE IF NOT EXISTS behavior_sessions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    account_id UUID REFERENCES social_accounts(id) ON DELETE CASCADE,
    session_start TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    session_end TIMESTAMP WITH TIME ZONE,
    behavior_pattern VARCHAR(50) DEFAULT 'moderate' CHECK (behavior_pattern IN ('conservative', 'moderate', 'aggressive')),
    actions_performed INTEGER DEFAULT 0,
    breaks_taken INTEGER DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Campaigns table
CREATE TABLE IF NOT EXISTS campaigns (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    target_platforms VARCHAR(50)[],
    start_date TIMESTAMP WITH TIME ZONE,
    end_date TIMESTAMP WITH TIME ZONE,
    status VARCHAR(50) DEFAULT 'draft' CHECK (status IN ('draft', 'active', 'paused', 'completed')),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Campaign accounts table
CREATE TABLE IF NOT EXISTS campaign_accounts (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    campaign_id UUID REFERENCES campaigns(id) ON DELETE CASCADE,
    account_id UUID REFERENCES social_accounts(id) ON DELETE CASCADE,
    role VARCHAR(100),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Target accounts table
CREATE TABLE IF NOT EXISTS target_accounts (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    campaign_id UUID REFERENCES campaigns(id) ON DELETE CASCADE,
    platform VARCHAR(50) NOT NULL,
    username VARCHAR(255) NOT NULL,
    targeting_criteria JSONB,
    priority INTEGER DEFAULT 1 CHECK (priority >= 1 AND priority <= 5),
    status VARCHAR(50) DEFAULT 'pending' CHECK (status IN ('pending', 'targeted', 'engaged', 'converted')),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Trending content table
CREATE TABLE IF NOT EXISTS trending_content (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    platform VARCHAR(50) NOT NULL,
    content_type VARCHAR(100),
    hashtags TEXT[],
    engagement_metrics JSONB,
    trending_score DECIMAL(5,2),
    discovered_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- System configuration table
CREATE TABLE IF NOT EXISTS system_config (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    config_key VARCHAR(255) UNIQUE NOT NULL,
    config_value TEXT,
    description TEXT,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Insert default system configuration
INSERT INTO system_config (config_key, config_value, description) VALUES
('phase_1_duration_days', '30', 'Duration of Phase 1 (TikTok only)'),
('phase_2_duration_days', '30', 'Duration of Phase 2 (TikTok + Instagram)'),
('phase_3_duration_days', 'unlimited', 'Duration of Phase 3 (All platforms)'),
('max_daily_actions_per_account', '50', 'Maximum daily actions per social account'),
('risk_threshold_auto_pause', '0.7', 'Risk score threshold to auto-pause account'),
('ai_provider_primary', 'deepseek', 'Primary AI service provider'),
('ai_provider_fallback', 'groq,anthropic,openai,google', 'Fallback AI service providers'),
('behavior_pattern_default', 'moderate', 'Default behavior pattern for new accounts')
ON CONFLICT (config_key) DO NOTHING;

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_social_accounts_user_id ON social_accounts(user_id);
CREATE INDEX IF NOT EXISTS idx_social_accounts_platform ON social_accounts(platform);
CREATE INDEX IF NOT EXISTS idx_social_accounts_phase ON social_accounts(phase);
CREATE INDEX IF NOT EXISTS idx_action_history_account_id ON action_history(account_id);
CREATE INDEX IF NOT EXISTS idx_action_history_created_at ON action_history(created_at);
CREATE INDEX IF NOT EXISTS idx_approval_requests_status ON approval_requests(status);
CREATE INDEX IF NOT EXISTS idx_platform_health_platform ON platform_health(platform);

-- Create updated_at trigger function
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Apply updated_at triggers
CREATE TRIGGER update_social_accounts_updated_at BEFORE UPDATE ON social_accounts
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_approval_requests_updated_at BEFORE UPDATE ON approval_requests
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_platform_health_updated_at BEFORE UPDATE ON platform_health
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_campaigns_updated_at BEFORE UPDATE ON campaigns
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Insert sample data for testing
INSERT INTO users (email, username) VALUES
('admin@socialseed.com', 'admin')
ON CONFLICT (email) DO NOTHING;

-- Insert sample platform health data
INSERT INTO platform_health (platform, status, health_score) VALUES
('tiktok', 'healthy', 95),
('instagram', 'healthy', 88),
('twitter', 'warning', 72)
ON CONFLICT (platform) DO UPDATE SET
    status = EXCLUDED.status,
    health_score = EXCLUDED.health_score,
    updated_at = NOW();
