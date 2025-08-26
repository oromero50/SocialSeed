-- SocialSeed v2.0 - Updated Database Schema
-- Supports phased approach, traffic light system, and human-in-the-loop approvals

-- Users and Authentication
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(255),
    subscription_tier VARCHAR(50) DEFAULT 'free',
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    is_active BOOLEAN DEFAULT true,
    settings JSONB DEFAULT '{}'
);

-- Social Media Accounts with Phase Support
CREATE TABLE social_accounts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    platform VARCHAR(50) NOT NULL, -- 'tiktok', 'instagram', 'twitter'
    username VARCHAR(255) NOT NULL,
    display_name VARCHAR(255),
    bio TEXT,
    profile_picture_url VARCHAR(500),

    -- Account Metrics
    followers_count INTEGER DEFAULT 0,
    following_count INTEGER DEFAULT 0,
    posts_count INTEGER DEFAULT 0,
    engagement_rate DECIMAL(5,4) DEFAULT 0.0000,

    -- Phase Management
    current_phase VARCHAR(20) DEFAULT 'phase_1',
    phase_started_at TIMESTAMP DEFAULT NOW(),
    phase_progression_locked BOOLEAN DEFAULT false,

    -- Account Health
    status VARCHAR(20) DEFAULT 'active', -- active, paused, warning, banned
    risk_score DECIMAL(3,2) DEFAULT 0.00,
    consecutive_errors INTEGER DEFAULT 0,
    last_action_at TIMESTAMP,
    last_error_at TIMESTAMP,

    -- Authentication Data
    access_token TEXT,
    refresh_token TEXT,
    token_expires_at TIMESTAMP,
    cookies JSONB,
    session_data JSONB,

    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),

    UNIQUE(user_id, platform, username)
);

-- Phase Progression History
CREATE TABLE phase_progressions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    account_id UUID REFERENCES social_accounts(id) ON DELETE CASCADE,
    from_phase VARCHAR(20) NOT NULL,
    to_phase VARCHAR(20) NOT NULL,
    progression_type VARCHAR(30) DEFAULT 'automatic', -- automatic, manual, forced
    reason TEXT,
    metrics_at_progression JSONB,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Account Health Monitoring
CREATE TABLE account_health_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    account_id UUID REFERENCES social_accounts(id) ON DELETE CASCADE,

    -- Health Metrics
    followers_count INTEGER,
    following_count INTEGER,
    posts_count INTEGER,
    engagement_rate DECIMAL(5,4),
    follow_ratio DECIMAL(8,2),

    -- Risk Assessment
    risk_score DECIMAL(3,2),
    risk_factors JSONB,
    authenticity_score DECIMAL(3,2),

    -- Platform Response
    avg_response_time_ms INTEGER,
    error_rate DECIMAL(3,2),
    rate_limit_hits INTEGER,

    created_at TIMESTAMP DEFAULT NOW()
);

-- Human Approval Workflow
CREATE TABLE approval_requests (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    account_id UUID REFERENCES social_accounts(id) ON DELETE CASCADE,

    -- Request Details
    action_type VARCHAR(50) NOT NULL, -- follow, unfollow, like, comment, etc.
    target_data JSONB NOT NULL,
    risk_level VARCHAR(10) NOT NULL, -- green, yellow, red

    -- Risk Assessment
    risk_score DECIMAL(3,2),
    reasoning TEXT,
    recommendation TEXT,
    flags JSONB,

    -- Approval Status
    status VARCHAR(20) DEFAULT 'pending', -- pending, approved, rejected, expired
    requested_at TIMESTAMP DEFAULT NOW(),
    reviewed_at TIMESTAMP,
    reviewer_id UUID REFERENCES users(id),
    review_notes TEXT,

    -- Auto-expiration
    expires_at TIMESTAMP DEFAULT (NOW() + INTERVAL '24 hours'),

    created_at TIMESTAMP DEFAULT NOW()
);

-- Traffic Light System Logs
CREATE TABLE safety_assessments (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    account_id UUID REFERENCES social_accounts(id) ON DELETE CASCADE,

    -- Action Context
    action_type VARCHAR(50) NOT NULL,
    target_username VARCHAR(255),
    target_platform VARCHAR(50),

    -- Risk Assessment Results
    risk_level VARCHAR(10) NOT NULL,
    authenticity_score DECIMAL(3,2),
    confidence DECIMAL(3,2),
    reasoning TEXT,

    -- LLM Analysis
    llm_provider VARCHAR(50),
    llm_response JSONB,
    analysis_duration_ms INTEGER,

    -- Decision Outcome
    action_taken VARCHAR(50), -- proceed, pause, request_approval, reject
    human_override BOOLEAN DEFAULT false,

    created_at TIMESTAMP DEFAULT NOW()
);

-- Platform Health Monitoring
CREATE TABLE platform_health (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    platform VARCHAR(50) NOT NULL,

    -- Response Metrics
    avg_response_time_ms INTEGER,
    success_rate DECIMAL(5,4),
    rate_limit_count INTEGER DEFAULT 0,
    error_count INTEGER DEFAULT 0,

    -- Health Status
    status VARCHAR(20) DEFAULT 'healthy', -- healthy, degraded, down
    consecutive_errors INTEGER DEFAULT 0,
    last_error_at TIMESTAMP,
    last_rate_limit_at TIMESTAMP,

    -- Time Window
    window_start TIMESTAMP DEFAULT NOW(),
    window_end TIMESTAMP DEFAULT (NOW() + INTERVAL '1 hour'),

    created_at TIMESTAMP DEFAULT NOW()
);

-- Action Execution History
CREATE TABLE action_history (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    account_id UUID REFERENCES social_accounts(id) ON DELETE CASCADE,

    -- Action Details
    action_type VARCHAR(50) NOT NULL,
    target_username VARCHAR(255),
    target_user_id VARCHAR(255),
    target_platform VARCHAR(50),

    -- Execution Context
    phase VARCHAR(20),
    risk_assessment_id UUID REFERENCES safety_assessments(id),
    approval_request_id UUID REFERENCES approval_requests(id),

    -- Behavioral Context
    delay_before_action INTEGER, -- seconds
    delay_reasoning TEXT,
    was_in_burst BOOLEAN DEFAULT false,
    session_action_count INTEGER,

    -- Results
    status VARCHAR(20) NOT NULL, -- success, failed, rate_limited, blocked
    response_code INTEGER,
    response_time_ms INTEGER,
    error_message TEXT,

    -- Timing
    scheduled_at TIMESTAMP,
    executed_at TIMESTAMP DEFAULT NOW(),
    created_at TIMESTAMP DEFAULT NOW()
);

-- Behavioral Session Tracking
CREATE TABLE behavior_sessions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    account_id UUID REFERENCES social_accounts(id) ON DELETE CASCADE,

    -- Session Metadata
    session_start TIMESTAMP DEFAULT NOW(),
    session_end TIMESTAMP,
    pattern_type VARCHAR(20), -- conservative, moderate, aggressive

    -- Activity Metrics
    total_actions INTEGER DEFAULT 0,
    successful_actions INTEGER DEFAULT 0,
    failed_actions INTEGER DEFAULT 0,

    -- Behavioral Metrics
    avg_delay_seconds INTEGER,
    break_count INTEGER DEFAULT 0,
    total_break_duration INTEGER DEFAULT 0, -- seconds
    burst_count INTEGER DEFAULT 0,

    -- Quality Metrics
    authenticity_score DECIMAL(3,2),
    detection_risk DECIMAL(3,2),

    created_at TIMESTAMP DEFAULT NOW()
);

-- Campaign Management with Phase Support
CREATE TABLE campaigns (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,

    -- Campaign Details
    name VARCHAR(255) NOT NULL,
    description TEXT,
    status VARCHAR(20) DEFAULT 'draft', -- draft, active, paused, completed

    -- Phase Configuration
    allowed_phases JSONB DEFAULT '["phase_1", "phase_2", "phase_3"]',
    min_phase_required VARCHAR(20) DEFAULT 'phase_1',

    -- Targeting
    platforms JSONB NOT NULL, -- ["tiktok", "instagram", "twitter"]
    target_hashtags JSONB,
    target_keywords JSONB,
    target_demographics JSONB,

    -- Safety Settings
    max_risk_level VARCHAR(10) DEFAULT 'yellow',
    require_human_approval BOOLEAN DEFAULT false,
    authenticity_threshold DECIMAL(3,2) DEFAULT 0.50,

    -- Scheduling
    start_date DATE,
    end_date DATE,
    active_hours JSONB, -- {"start": 8, "end": 22}
    timezone VARCHAR(50) DEFAULT 'UTC',

    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Campaign Account Assignments
CREATE TABLE campaign_accounts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    campaign_id UUID REFERENCES campaigns(id) ON DELETE CASCADE,
    account_id UUID REFERENCES social_accounts(id) ON DELETE CASCADE,

    -- Account-specific Settings
    daily_action_limit INTEGER DEFAULT 50,
    hourly_action_limit INTEGER DEFAULT 10,
    weight DECIMAL(3,2) DEFAULT 1.00, -- Resource allocation weight

    -- Status
    status VARCHAR(20) DEFAULT 'active',
    assigned_at TIMESTAMP DEFAULT NOW(),

    UNIQUE(campaign_id, account_id)
);

-- Target Account Analysis
CREATE TABLE target_accounts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    -- Account Identity
    platform VARCHAR(50) NOT NULL,
    username VARCHAR(255) NOT NULL,
    user_id VARCHAR(255),
    display_name VARCHAR(255),

    -- Profile Data
    bio TEXT,
    followers_count INTEGER,
    following_count INTEGER,
    posts_count INTEGER,
    verified BOOLEAN DEFAULT false,
    has_profile_picture BOOLEAN DEFAULT true,

    -- Authenticity Analysis
    authenticity_score DECIMAL(3,2),
    authenticity_level VARCHAR(20), -- genuine, likely_genuine, suspicious, likely_bot, definite_bot
    confidence DECIMAL(3,2),
    red_flags JSONB,
    green_flags JSONB,

    -- Analysis Metadata
    analyzed_at TIMESTAMP DEFAULT NOW(),
    analyzer_version VARCHAR(20),
    needs_reanalysis BOOLEAN DEFAULT false,

    -- Interaction History
    last_interacted_at TIMESTAMP,
    interaction_count INTEGER DEFAULT 0,
    successful_interactions INTEGER DEFAULT 0,

    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),

    UNIQUE(platform, username)
);

-- Content Trend Monitoring
CREATE TABLE trending_content (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    platform VARCHAR(50) NOT NULL,

    -- Content Details
    content_type VARCHAR(50), -- hashtag, keyword, topic, sound
    content_value VARCHAR(255) NOT NULL,
    category VARCHAR(100),

    -- Trend Metrics
    volume INTEGER DEFAULT 0,
    growth_rate DECIMAL(5,2),
    engagement_rate DECIMAL(5,4),
    trend_score DECIMAL(5,2),

    -- Trend Status
    status VARCHAR(20) DEFAULT 'emerging', -- emerging, trending, peak, declining, dead
    first_detected TIMESTAMP DEFAULT NOW(),
    peak_detected TIMESTAMP,

    -- Recommendation
    recommended_for_phases JSONB DEFAULT '["phase_2", "phase_3"]',
    risk_level VARCHAR(10) DEFAULT 'green',

    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),

    UNIQUE(platform, content_type, content_value)
);

-- System Configuration
CREATE TABLE system_config (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    key VARCHAR(100) UNIQUE NOT NULL,
    value JSONB NOT NULL,
    description TEXT,
    category VARCHAR(50),
    updated_by UUID REFERENCES users(id),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Insert default configuration
INSERT INTO system_config (key, value, description, category) VALUES 
('phase_settings', '{
    "phase_1": {
        "duration_days": 30,
        "max_follows_per_hour": 5,
        "max_likes_per_hour": 10,
        "platforms": ["tiktok"],
        "risk_threshold": 0.3
    },
    "phase_2": {
        "duration_days": 30,
        "max_follows_per_hour": 15,
        "max_likes_per_hour": 25,
        "platforms": ["tiktok", "instagram"],
        "risk_threshold": 0.5
    },
    "phase_3": {
        "duration_days": null,
        "max_follows_per_hour": 25,
        "max_likes_per_hour": 40,
        "platforms": ["tiktok", "instagram", "twitter"],
        "risk_threshold": 0.7
    }
}', 'Phase progression settings', 'phases'),

('ai_providers', '{
    "primary": "deepseek",
    "fallback": ["groq", "anthropic", "openai", "google"],
    "rate_limits": {
        "deepseek": 1000,
        "groq": 500,
        "anthropic": 100,
        "openai": 200,
        "google": 300
    }
}', 'AI service provider configuration', 'ai'),

('safety_thresholds', '{
    "authenticity_minimum": {
        "phase_1": 0.7,
        "phase_2": 0.5,
        "phase_3": 0.3
    },
    "risk_escalation": {
        "yellow_threshold": 0.4,
        "red_threshold": 0.7,
        "auto_pause_threshold": 0.9
    }
}', 'Safety and risk thresholds', 'safety');

-- Indexes for Performance
CREATE INDEX idx_social_accounts_user_platform ON social_accounts(user_id, platform);
CREATE INDEX idx_social_accounts_phase ON social_accounts(current_phase);
CREATE INDEX idx_social_accounts_status ON social_accounts(status);

CREATE INDEX idx_approval_requests_status ON approval_requests(status);
CREATE INDEX idx_approval_requests_account ON approval_requests(account_id);
CREATE INDEX idx_approval_requests_expires ON approval_requests(expires_at);

CREATE INDEX idx_action_history_account_time ON action_history(account_id, executed_at);
CREATE INDEX idx_action_history_status ON action_history(status);

CREATE INDEX idx_safety_assessments_account_time ON safety_assessments(account_id, created_at);
CREATE INDEX idx_safety_assessments_risk_level ON safety_assessments(risk_level);

CREATE INDEX idx_target_accounts_platform_username ON target_accounts(platform, username);
CREATE INDEX idx_target_accounts_authenticity ON target_accounts(authenticity_level);
CREATE INDEX idx_target_accounts_needs_reanalysis ON target_accounts(needs_reanalysis);

CREATE INDEX idx_platform_health_platform_window ON platform_health(platform, window_start, window_end);

-- Updated triggers for timestamp maintenance
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_social_accounts_updated_at BEFORE UPDATE ON social_accounts FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_campaigns_updated_at BEFORE UPDATE ON campaigns FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_target_accounts_updated_at BEFORE UPDATE ON target_accounts FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_trending_content_updated_at BEFORE UPDATE ON trending_content FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
