-- Simplified SocialSeed Schema for Supabase
-- Tables that match the backend expectations

-- Users table (simplified)
CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    full_name VARCHAR(255),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Social accounts table (matches backend expectations)
CREATE TABLE IF NOT EXISTS social_accounts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    platform VARCHAR(50) NOT NULL, -- 'tiktok', 'instagram', 'twitter'
    username VARCHAR(255) NOT NULL,
    display_name VARCHAR(255),
    
    -- Account metrics
    followers_count INTEGER DEFAULT 0,
    following_count INTEGER DEFAULT 0,
    posts_count INTEGER DEFAULT 0,
    
    -- Account status
    is_active BOOLEAN DEFAULT true,
    health_score DECIMAL(3,2) DEFAULT 1.00,
    current_phase VARCHAR(20) DEFAULT 'phase_1',
    daily_action_limit INTEGER DEFAULT 50,
    
    -- Authentication
    access_token TEXT,
    
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    
    UNIQUE(user_id, platform, username)
);

-- Actions table (for backend compatibility)
CREATE TABLE IF NOT EXISTS actions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    account_id UUID REFERENCES social_accounts(id) ON DELETE CASCADE,
    action_type VARCHAR(50) NOT NULL, -- follow, unfollow, like, comment
    platform VARCHAR(50) NOT NULL,
    target_account VARCHAR(255),
    status VARCHAR(20) DEFAULT 'pending', -- pending, completed, failed
    created_at TIMESTAMP DEFAULT NOW(),
    executed_at TIMESTAMP
);

-- Insert a default user for testing
INSERT INTO users (id, email, full_name) VALUES 
('550e8400-e29b-41d4-a716-446655440000', 'test@socialseed.com', 'Test User')
ON CONFLICT (id) DO NOTHING;

-- Create indexes for performance
CREATE INDEX IF NOT EXISTS idx_social_accounts_user_platform ON social_accounts(user_id, platform);
CREATE INDEX IF NOT EXISTS idx_social_accounts_status ON social_accounts(is_active);
CREATE INDEX IF NOT EXISTS idx_actions_status ON actions(status);
CREATE INDEX IF NOT EXISTS idx_actions_account ON actions(account_id);

