-- Historical Tracking Tables for SocialSeed v2.0
-- These tables store historical data for analytics and growth tracking

-- Table to track follower counts over time
CREATE TABLE IF NOT EXISTS follower_history (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    account_id UUID NOT NULL REFERENCES social_accounts(id) ON DELETE CASCADE,
    follower_count INTEGER NOT NULL,
    following_count INTEGER NOT NULL,
    post_count INTEGER NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    -- Index for efficient queries
    CONSTRAINT fk_follower_history_account FOREIGN KEY (account_id) REFERENCES social_accounts(id)
);

-- Table to track engagement metrics over time
CREATE TABLE IF NOT EXISTS engagement_history (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    account_id UUID NOT NULL REFERENCES social_accounts(id) ON DELETE CASCADE,
    likes_count INTEGER NOT NULL DEFAULT 0,
    comments_count INTEGER NOT NULL DEFAULT 0,
    shares_count INTEGER NOT NULL DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    -- Index for efficient queries
    CONSTRAINT fk_engagement_history_account FOREIGN KEY (account_id) REFERENCES social_accounts(id)
);

-- Table to track content performance over time
CREATE TABLE IF NOT EXISTS content_history (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    account_id UUID NOT NULL REFERENCES social_accounts(id) ON DELETE CASCADE,
    post_id VARCHAR(255), -- External post ID from social platform
    post_type VARCHAR(50), -- 'video', 'image', 'story', etc.
    likes_count INTEGER NOT NULL DEFAULT 0,
    comments_count INTEGER NOT NULL DEFAULT 0,
    shares_count INTEGER NOT NULL DEFAULT 0,
    reach_count INTEGER NOT NULL DEFAULT 0,
    impressions_count INTEGER NOT NULL DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    -- Index for efficient queries
    CONSTRAINT fk_content_history_account FOREIGN KEY (account_id) REFERENCES social_accounts(id)
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_follower_history_account_created ON follower_history(account_id, created_at DESC);
CREATE INDEX IF NOT EXISTS idx_engagement_history_account_created ON engagement_history(account_id, created_at DESC);
CREATE INDEX IF NOT EXISTS idx_content_history_account_created ON content_history(account_id, created_at DESC);

-- Insert sample data for testing (optional)
-- This will help you see the analytics working immediately

-- Sample follower history for your TikTok account
INSERT INTO follower_history (account_id, follower_count, following_count, post_count, created_at) VALUES
-- You'll need to replace 'YOUR_ACCOUNT_ID' with the actual UUID from your social_accounts table
-- (SELECT id FROM social_accounts WHERE username = 'oromero0' LIMIT 1), 150, 200, 25, NOW() - INTERVAL '7 days'),
-- (SELECT id FROM social_accounts WHERE username = 'oromero0' LIMIT 1), 175, 220, 28, NOW() - INTERVAL '3 days'),
-- (SELECT id FROM social_accounts WHERE username = 'oromero0' LIMIT 1), 200, 250, 30, NOW());

-- Sample engagement history
INSERT INTO engagement_history (account_id, likes_count, comments_count, shares_count, created_at) VALUES
-- (SELECT id FROM social_accounts WHERE username = 'oromero0' LIMIT 1), 45, 12, 8, NOW() - INTERVAL '7 days'),
-- (SELECT id FROM social_accounts WHERE username = 'oromero0' LIMIT 1), 52, 15, 10, NOW() - INTERVAL '3 days'),
-- (SELECT id FROM social_accounts WHERE username = 'oromero0' LIMIT 1), 60, 18, 12, NOW());

-- Enable Row Level Security (RLS) for security
ALTER TABLE follower_history ENABLE ROW LEVEL SECURITY;
ALTER TABLE engagement_history ENABLE ROW LEVEL SECURITY;
ALTER TABLE content_history ENABLE ROW LEVEL SECURITY;

-- Create RLS policies (adjust based on your user management system)
-- For now, allow all operations (you can restrict this later)
CREATE POLICY "Allow all operations on follower_history" ON follower_history FOR ALL USING (true);
CREATE POLICY "Allow all operations on engagement_history" ON engagement_history FOR ALL USING (true);
CREATE POLICY "Allow all operations on content_history" ON content_history FOR ALL USING (true);

-- Grant permissions to authenticated users
GRANT ALL ON follower_history TO authenticated;
GRANT ALL ON engagement_history TO authenticated;
GRANT ALL ON content_history TO authenticated;
