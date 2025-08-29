-- SocialSeed v2.0 - Historical Data Tables Migration
-- Creates tables for comprehensive TikTok analytics and growth tracking

-- User Profile History Table
CREATE TABLE IF NOT EXISTS user_profile_history (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES auth.users(id),
    platform TEXT NOT NULL DEFAULT 'tiktok',
    username TEXT NOT NULL,
    display_name TEXT,
    follower_count INTEGER DEFAULT 0,
    following_count INTEGER DEFAULT 0,
    like_count BIGINT DEFAULT 0,
    video_count INTEGER DEFAULT 0,
    avatar_url TEXT,
    bio TEXT,
    is_verified BOOLEAN DEFAULT FALSE,
    is_private BOOLEAN DEFAULT FALSE,
    extracted_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    extraction_method TEXT DEFAULT 'api', -- 'playwright', 'api', 'mobile'
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    -- Ensure we don't duplicate data for same user/time
    UNIQUE(user_id, username, platform, DATE_TRUNC('hour', extracted_at))
);

-- Follower List History Table  
CREATE TABLE IF NOT EXISTS follower_history (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    source_user_id UUID REFERENCES auth.users(id),
    source_username TEXT NOT NULL,
    follower_username TEXT NOT NULL,
    follower_user_id TEXT,
    follower_display_name TEXT,
    follower_avatar_url TEXT,
    is_verified BOOLEAN DEFAULT FALSE,
    extracted_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    status TEXT DEFAULT 'active', -- 'active', 'new', 'lost'
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    -- Prevent duplicate followers in same extraction batch
    UNIQUE(source_username, follower_username, DATE_TRUNC('day', extracted_at))
);

-- Video Metrics History Table
CREATE TABLE IF NOT EXISTS video_metrics_history (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES auth.users(id),
    username TEXT NOT NULL,
    video_id TEXT NOT NULL,
    description TEXT,
    view_count BIGINT DEFAULT 0,
    like_count INTEGER DEFAULT 0,
    comment_count INTEGER DEFAULT 0,
    share_count INTEGER DEFAULT 0,
    engagement_rate DECIMAL(5,2) DEFAULT 0,
    video_url TEXT,
    thumbnail_url TEXT,
    duration INTEGER DEFAULT 0,
    video_created_at TIMESTAMP WITH TIME ZONE,
    extracted_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    -- Prevent duplicate video metrics for same extraction time
    UNIQUE(video_id, DATE_TRUNC('hour', extracted_at))
);

-- Growth Analytics Summary Table
CREATE TABLE IF NOT EXISTS growth_analytics (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES auth.users(id),
    platform TEXT NOT NULL DEFAULT 'tiktok',
    username TEXT NOT NULL,
    period_start TIMESTAMP WITH TIME ZONE,
    period_end TIMESTAMP WITH TIME ZONE,
    followers_start INTEGER DEFAULT 0,
    followers_end INTEGER DEFAULT 0,
    followers_gained INTEGER DEFAULT 0,
    followers_lost INTEGER DEFAULT 0,
    net_growth INTEGER DEFAULT 0,
    growth_rate DECIMAL(5,2) DEFAULT 0,
    avg_daily_growth DECIMAL(8,2) DEFAULT 0,
    engagement_rate_avg DECIMAL(5,2) DEFAULT 0,
    total_videos INTEGER DEFAULT 0,
    total_views BIGINT DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    -- Prevent duplicate analytics for same period
    UNIQUE(user_id, username, platform, period_start, period_end)
);

-- Follower Changes Tracking Table
CREATE TABLE IF NOT EXISTS follower_changes (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES auth.users(id),
    username TEXT NOT NULL,
    change_type TEXT NOT NULL, -- 'gained', 'lost'
    follower_username TEXT NOT NULL,
    follower_display_name TEXT,
    detected_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Performance Indexes
CREATE INDEX IF NOT EXISTS idx_profile_history_user_time ON user_profile_history(user_id, username, extracted_at DESC);
CREATE INDEX IF NOT EXISTS idx_profile_history_platform ON user_profile_history(platform, username);
CREATE INDEX IF NOT EXISTS idx_follower_history_source_time ON follower_history(source_username, extracted_at DESC);
CREATE INDEX IF NOT EXISTS idx_follower_history_user ON follower_history(source_user_id);
CREATE INDEX IF NOT EXISTS idx_video_metrics_username_time ON video_metrics_history(username, extracted_at DESC);
CREATE INDEX IF NOT EXISTS idx_growth_analytics_user_platform ON growth_analytics(user_id, platform, username);
CREATE INDEX IF NOT EXISTS idx_follower_changes_user_time ON follower_changes(user_id, username, detected_at DESC);

-- Row Level Security (RLS) Policies
-- Users can only access their own data

-- Profile History RLS
ALTER TABLE user_profile_history ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can view own profile history" ON user_profile_history
    FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own profile history" ON user_profile_history
    FOR INSERT WITH CHECK (auth.uid() = user_id);

-- Follower History RLS
ALTER TABLE follower_history ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can view own follower history" ON follower_history
    FOR SELECT USING (auth.uid() = source_user_id);

CREATE POLICY "Users can insert own follower history" ON follower_history
    FOR INSERT WITH CHECK (auth.uid() = source_user_id);

-- Video Metrics RLS
ALTER TABLE video_metrics_history ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can view own video metrics" ON video_metrics_history
    FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own video metrics" ON video_metrics_history
    FOR INSERT WITH CHECK (auth.uid() = user_id);

-- Growth Analytics RLS
ALTER TABLE growth_analytics ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can view own growth analytics" ON growth_analytics
    FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own growth analytics" ON growth_analytics
    FOR INSERT WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update own growth analytics" ON growth_analytics
    FOR UPDATE USING (auth.uid() = user_id);

-- Follower Changes RLS
ALTER TABLE follower_changes ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can view own follower changes" ON follower_changes
    FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own follower changes" ON follower_changes
    FOR INSERT WITH CHECK (auth.uid() = user_id);

-- Functions for analytics calculations
CREATE OR REPLACE FUNCTION calculate_engagement_rate(
    likes INTEGER,
    comments INTEGER,
    shares INTEGER,
    views BIGINT
)
RETURNS DECIMAL(5,2) AS $$
BEGIN
    IF views > 0 THEN
        RETURN ROUND(((likes + comments + shares)::DECIMAL / views) * 100, 2);
    ELSE
        RETURN 0;
    END IF;
END;
$$ LANGUAGE plpgsql;

-- Function to get growth rate between two dates
CREATE OR REPLACE FUNCTION get_growth_rate(
    p_user_id UUID,
    p_username TEXT,
    p_start_date TIMESTAMP WITH TIME ZONE,
    p_end_date TIMESTAMP WITH TIME ZONE
)
RETURNS TABLE(
    followers_start INTEGER,
    followers_end INTEGER,
    growth_absolute INTEGER,
    growth_rate DECIMAL(5,2),
    days_period INTEGER
) AS $$
DECLARE
    start_followers INTEGER;
    end_followers INTEGER;
    days_diff INTEGER;
BEGIN
    -- Get follower count at start date
    SELECT follower_count INTO start_followers
    FROM user_profile_history
    WHERE user_id = p_user_id 
      AND username = p_username
      AND extracted_at >= p_start_date
    ORDER BY extracted_at ASC
    LIMIT 1;

    -- Get follower count at end date
    SELECT follower_count INTO end_followers
    FROM user_profile_history
    WHERE user_id = p_user_id 
      AND username = p_username
      AND extracted_at <= p_end_date
    ORDER BY extracted_at DESC
    LIMIT 1;

    -- Calculate days between dates
    days_diff := EXTRACT(DAYS FROM p_end_date - p_start_date);

    -- Return calculated values
    followers_start := COALESCE(start_followers, 0);
    followers_end := COALESCE(end_followers, 0);
    growth_absolute := followers_end - followers_start;
    
    IF followers_start > 0 THEN
        growth_rate := ROUND((growth_absolute::DECIMAL / followers_start) * 100, 2);
    ELSE
        growth_rate := 0;
    END IF;
    
    days_period := GREATEST(days_diff, 1);
    
    RETURN NEXT;
END;
$$ LANGUAGE plpgsql;

-- Create a view for easy analytics access
CREATE OR REPLACE VIEW user_growth_summary AS
SELECT 
    h.user_id,
    h.username,
    h.platform,
    h.follower_count,
    h.following_count,
    h.like_count,
    h.extracted_at,
    LAG(h.follower_count) OVER (
        PARTITION BY h.user_id, h.username 
        ORDER BY h.extracted_at
    ) as previous_followers,
    h.follower_count - LAG(h.follower_count) OVER (
        PARTITION BY h.user_id, h.username 
        ORDER BY h.extracted_at
    ) as followers_change,
    ROW_NUMBER() OVER (
        PARTITION BY h.user_id, h.username 
        ORDER BY h.extracted_at DESC
    ) as recency_rank
FROM user_profile_history h
ORDER BY h.user_id, h.username, h.extracted_at DESC;

-- Grant necessary permissions
GRANT SELECT ON user_growth_summary TO authenticated;
GRANT EXECUTE ON FUNCTION calculate_engagement_rate TO authenticated;
GRANT EXECUTE ON FUNCTION get_growth_rate TO authenticated;

-- Comment the tables
COMMENT ON TABLE user_profile_history IS 'Historical tracking of user profile metrics across platforms';
COMMENT ON TABLE follower_history IS 'Complete follower lists with timestamps for change detection';
COMMENT ON TABLE video_metrics_history IS 'Historical video performance metrics and engagement data';
COMMENT ON TABLE growth_analytics IS 'Calculated growth metrics and trends over time periods';
COMMENT ON TABLE follower_changes IS 'Real-time tracking of follower gains and losses';

-- Migration complete
SELECT 'Historical analytics tables created successfully' as status;
