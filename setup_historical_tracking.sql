-- Complete Database Setup for SocialSeed v2.0
-- This script sets up historical tracking tables and fixes system_config issues

-- =====================================================
-- 1. HISTORICAL TRACKING TABLES
-- =====================================================

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

-- =====================================================
-- 2. CREATE INDEXES FOR PERFORMANCE
-- =====================================================

CREATE INDEX IF NOT EXISTS idx_follower_history_account_created ON follower_history(account_id, created_at DESC);
CREATE INDEX IF NOT EXISTS idx_engagement_history_account_created ON engagement_history(account_id, created_at DESC);
CREATE INDEX IF NOT EXISTS idx_content_history_account_created ON content_history(account_id, created_at DESC);

-- =====================================================
-- 3. FIX SYSTEM_CONFIG TABLE (for settings to work)
-- =====================================================

-- Create system_config table if it doesn't exist
CREATE TABLE IF NOT EXISTS system_config (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    config_key VARCHAR(255) NOT NULL UNIQUE,
    config_value TEXT,
    description TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create index for system_config
CREATE INDEX IF NOT EXISTS idx_system_config_key ON system_config(config_key);

-- =====================================================
-- 4. ENABLE ROW LEVEL SECURITY
-- =====================================================

-- Enable RLS for historical tracking tables
ALTER TABLE follower_history ENABLE ROW LEVEL SECURITY;
ALTER TABLE engagement_history ENABLE ROW LEVEL SECURITY;
ALTER TABLE content_history ENABLE ROW LEVEL SECURITY;

-- Enable RLS for system_config
ALTER TABLE system_config ENABLE ROW LEVEL SECURITY;

-- =====================================================
-- 5. CREATE RLS POLICIES
-- =====================================================

-- Policies for historical tracking tables
CREATE POLICY "Allow all operations on follower_history" ON follower_history FOR ALL USING (true);
CREATE POLICY "Allow all operations on engagement_history" ON engagement_history FOR ALL USING (true);
CREATE POLICY "Allow all operations on content_history" ON content_history FOR ALL USING (true);

-- Policies for system_config
CREATE POLICY "Allow all operations on system_config" ON system_config FOR ALL USING (true);

-- =====================================================
-- 6. GRANT PERMISSIONS
-- =====================================================

-- Grant permissions to authenticated users
GRANT ALL ON follower_history TO authenticated;
GRANT ALL ON engagement_history TO authenticated;
GRANT ALL ON content_history TO authenticated;
GRANT ALL ON system_config TO authenticated;

-- =====================================================
-- 7. INSERT SAMPLE DATA (OPTIONAL)
-- =====================================================

-- Insert sample follower history for testing
-- Uncomment and modify these lines after you have accounts in social_accounts table
/*
INSERT INTO follower_history (account_id, follower_count, following_count, post_count, created_at) VALUES
-- Replace 'YOUR_ACCOUNT_ID' with actual UUID from your social_accounts table
-- (SELECT id FROM social_accounts WHERE username = 'oromero0' LIMIT 1), 150, 200, 25, NOW() - INTERVAL '7 days'),
-- (SELECT id FROM social_accounts WHERE username = 'oromero0' LIMIT 1), 175, 220, 28, NOW() - INTERVAL '3 days'),
-- (SELECT id FROM social_accounts WHERE username = 'oromero0' LIMIT 1), 200, 250, 30, NOW());

-- Insert sample engagement history
INSERT INTO engagement_history (account_id, likes_count, comments_count, shares_count, created_at) VALUES
-- (SELECT id FROM social_accounts WHERE username = 'oromero0' LIMIT 1), 45, 12, 8, NOW() - INTERVAL '7 days'),
-- (SELECT id FROM social_accounts WHERE username = 'oromero0' LIMIT 1), 52, 15, 10, NOW() - INTERVAL '3 days'),
-- (SELECT id FROM social_accounts WHERE username = 'oromero0' LIMIT 1), 60, 18, 12, NOW());
*/

-- =====================================================
-- 8. VERIFICATION QUERIES
-- =====================================================

-- Check if tables were created successfully
SELECT 
    table_name,
    CASE 
        WHEN table_name IN ('follower_history', 'engagement_history', 'content_history', 'system_config') 
        THEN '✅ Created' 
        ELSE '❌ Missing' 
    END as status
FROM information_schema.tables 
WHERE table_name IN ('follower_history', 'engagement_history', 'content_history', 'system_config')
AND table_schema = 'public';

-- Check RLS status
SELECT 
    schemaname,
    tablename,
    rowsecurity
FROM pg_tables 
WHERE tablename IN ('follower_history', 'engagement_history', 'content_history', 'system_config');
