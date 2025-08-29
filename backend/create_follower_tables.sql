-- Additional tables for follower tracking and analytics

-- Follower snapshots for tracking changes over time
CREATE TABLE IF NOT EXISTS follower_snapshots (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    account_id UUID REFERENCES social_accounts(id) ON DELETE CASCADE,
    follower_count INTEGER DEFAULT 0,
    following_count INTEGER DEFAULT 0,
    engagement_rate DECIMAL(5,2) DEFAULT 0.00,
    snapshot_data JSONB, -- Complete follower/following list and analytics
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Unfollower events for "Who Unfriended Me" functionality
CREATE TABLE IF NOT EXISTS unfollower_events (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    account_id UUID REFERENCES social_accounts(id) ON DELETE CASCADE,
    unfollower_username VARCHAR(100) NOT NULL,
    unfollower_display_name VARCHAR(200),
    detected_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Growth analytics and insights
CREATE TABLE IF NOT EXISTS growth_analytics (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    account_id UUID REFERENCES social_accounts(id) ON DELETE CASCADE,
    period_start TIMESTAMP WITH TIME ZONE NOT NULL,
    period_end TIMESTAMP WITH TIME ZONE NOT NULL,
    followers_gained INTEGER DEFAULT 0,
    followers_lost INTEGER DEFAULT 0,
    net_growth INTEGER DEFAULT 0,
    engagement_rate DECIMAL(5,2) DEFAULT 0.00,
    growth_rate DECIMAL(5,2) DEFAULT 0.00,
    analytics_data JSONB, -- Detailed analytics and insights
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Follower details for tracking individual followers
CREATE TABLE IF NOT EXISTS follower_details (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    account_id UUID REFERENCES social_accounts(id) ON DELETE CASCADE,
    follower_username VARCHAR(100) NOT NULL,
    follower_display_name VARCHAR(200),
    follower_count INTEGER DEFAULT 0,
    following_count INTEGER DEFAULT 0,
    is_following BOOLEAN DEFAULT TRUE,
    first_seen TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    last_seen TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    unfollowed_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(account_id, follower_username)
);

-- Update social_accounts table with new columns for analytics
ALTER TABLE social_accounts 
ADD COLUMN IF NOT EXISTS follower_count INTEGER DEFAULT 0,
ADD COLUMN IF NOT EXISTS following_count INTEGER DEFAULT 0,
ADD COLUMN IF NOT EXISTS engagement_rate DECIMAL(5,2) DEFAULT 0.00,
ADD COLUMN IF NOT EXISTS last_sync TIMESTAMP WITH TIME ZONE,
ADD COLUMN IF NOT EXISTS metadata JSONB;

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_follower_snapshots_account_created ON follower_snapshots(account_id, created_at DESC);
CREATE INDEX IF NOT EXISTS idx_unfollower_events_account_detected ON unfollower_events(account_id, detected_at DESC);
CREATE INDEX IF NOT EXISTS idx_growth_analytics_account_period ON growth_analytics(account_id, period_start, period_end);
CREATE INDEX IF NOT EXISTS idx_follower_details_account_username ON follower_details(account_id, follower_username);
CREATE INDEX IF NOT EXISTS idx_follower_details_unfollowed ON follower_details(account_id, unfollowed_at) WHERE unfollowed_at IS NOT NULL;
