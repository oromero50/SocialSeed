-- Complete Database Setup for SocialSeed v2.0
-- This script sets up all necessary tables including historical tracking

-- ========================================
-- 1. HISTORICAL TRACKING TABLES
-- ========================================

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

-- ========================================
-- 2. ENSURE SYSTEM_CONFIG TABLE EXISTS
-- ========================================

-- Create system_config table if it doesn't exist
CREATE TABLE IF NOT EXISTS system_config (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    config_key VARCHAR(255) UNIQUE NOT NULL,
    config_value TEXT,
    description TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- ========================================
-- 3. CREATE INDEXES FOR PERFORMANCE
-- ========================================

-- Historical tracking indexes
CREATE INDEX IF NOT EXISTS idx_follower_history_account_created ON follower_history(account_id, created_at DESC);
CREATE INDEX IF NOT EXISTS idx_engagement_history_account_created ON engagement_history(account_id, created_at DESC);
CREATE INDEX IF NOT EXISTS idx_content_history_account_created ON content_history(account_id, created_at DESC);

-- System config indexes
CREATE INDEX IF NOT EXISTS idx_system_config_key ON system_config(config_key);

-- ========================================
-- 4. ENABLE ROW LEVEL SECURITY
-- ========================================

-- Historical tracking tables
ALTER TABLE follower_history ENABLE ROW LEVEL SECURITY;
ALTER TABLE engagement_history ENABLE ROW LEVEL SECURITY;
ALTER TABLE content_history ENABLE ROW LEVEL SECURITY;

-- System config table
ALTER TABLE system_config ENABLE ROW LEVEL SECURITY;

-- ========================================
-- 5. CREATE RLS POLICIES
-- ========================================

-- Historical tracking policies
CREATE POLICY "Allow all operations on follower_history" ON follower_history FOR ALL USING (true);
CREATE POLICY "Allow all operations on engagement_history" ON engagement_history FOR ALL USING (true);
CREATE POLICY "Allow all operations on content_history" ON content_history FOR ALL USING (true);

-- System config policies
CREATE POLICY "Allow all operations on system_config" ON system_config FOR ALL USING (true);

-- ========================================
-- 6. GRANT PERMISSIONS
-- ========================================

-- Historical tracking tables
GRANT ALL ON follower_history TO authenticated;
GRANT ALL ON engagement_history TO authenticated;
GRANT ALL ON content_history TO authenticated;

-- System config table
GRANT ALL ON system_config TO authenticated;

-- ========================================
-- 7. INSERT SAMPLE DATA (OPTIONAL)
-- ========================================

-- Insert default system configuration
INSERT INTO system_config (config_key, config_value, description) VALUES
('default_safety_level', '"Moderate"', 'Default safety level for new accounts'),
('default_action_delay', '15', 'Default action delay in minutes'),
('default_auto_approval', 'true', 'Default auto-approval setting')
ON CONFLICT (config_key) DO NOTHING;

-- ========================================
-- 8. VERIFICATION QUERIES
-- ========================================

-- Check if tables were created successfully
SELECT 
    table_name,
    CASE 
        WHEN table_name IN ('follower_history', 'engagement_history', 'content_history', 'system_config') 
        THEN '✅ Created' 
        ELSE '❌ Missing' 
    END as status
FROM information_schema.tables 
WHERE table_schema = 'public' 
    AND table_name IN ('follower_history', 'engagement_history', 'content_history', 'system_config');

-- Check table structures
SELECT 
    table_name,
    column_name,
    data_type,
    is_nullable
FROM information_schema.columns 
WHERE table_schema = 'public' 
    AND table_name IN ('follower_history', 'engagement_history', 'content_history', 'system_config')
ORDER BY table_name, ordinal_position;
