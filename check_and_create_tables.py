#!/usr/bin/env python3
"""
Check existing tables and create only the missing ones
"""
import asyncio
import asyncpg
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

async def check_and_create_tables():
    """Check what tables exist and create missing ones"""
    try:
        # Parse DATABASE_URL
        database_url = os.getenv('DATABASE_URL')
        if not database_url:
            print("❌ DATABASE_URL not found in environment")
            return False
            
        print(f"🔗 Connecting to database...")
        
        # Connect to database
        conn = await asyncpg.connect(database_url)
        
        print("🔍 Checking existing tables...")
        
        # Check what tables exist
        existing_tables = await conn.fetch("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
        """)
        
        table_names = [row['table_name'] for row in existing_tables]
        print(f"📋 Existing tables: {table_names}")
        
        # Check if users table exists and what columns it has
        if 'users' in table_names:
            print("👤 Users table exists, checking structure...")
            user_columns = await conn.fetch("""
                SELECT column_name, is_nullable, column_default
                FROM information_schema.columns 
                WHERE table_name = 'users' AND table_schema = 'public'
            """)
            print("📋 Users table columns:")
            for col in user_columns:
                print(f"   - {col['column_name']} (nullable: {col['is_nullable']})")
        
        # Create social_accounts table if it doesn't exist
        if 'social_accounts' not in table_names:
            print("📝 Creating social_accounts table...")
            await conn.execute("""
                CREATE TABLE social_accounts (
                    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                    user_id UUID,
                    platform VARCHAR(50) NOT NULL,
                    username VARCHAR(255) NOT NULL,
                    display_name VARCHAR(255),
                    followers_count INTEGER DEFAULT 0,
                    following_count INTEGER DEFAULT 0,
                    posts_count INTEGER DEFAULT 0,
                    is_active BOOLEAN DEFAULT true,
                    health_score DECIMAL(3,2) DEFAULT 1.00,
                    current_phase VARCHAR(20) DEFAULT 'phase_1',
                    daily_action_limit INTEGER DEFAULT 50,
                    access_token TEXT,
                    created_at TIMESTAMP DEFAULT NOW(),
                    updated_at TIMESTAMP DEFAULT NOW(),
                    UNIQUE(platform, username)
                );
            """)
            print("✅ social_accounts table created")
        else:
            print("✅ social_accounts table already exists")
        
        # Create actions table if it doesn't exist
        if 'actions' not in table_names:
            print("📝 Creating actions table...")
            await conn.execute("""
                CREATE TABLE actions (
                    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                    account_id UUID,
                    action_type VARCHAR(50) NOT NULL,
                    platform VARCHAR(50) NOT NULL,
                    target_account VARCHAR(255),
                    status VARCHAR(20) DEFAULT 'pending',
                    created_at TIMESTAMP DEFAULT NOW(),
                    executed_at TIMESTAMP
                );
            """)
            print("✅ actions table created")
        else:
            print("✅ actions table already exists")
        
        # Test the tables we need
        print("🧪 Testing essential tables...")
        accounts_count = await conn.fetchval("SELECT COUNT(*) FROM social_accounts") 
        actions_count = await conn.fetchval("SELECT COUNT(*) FROM actions")
        
        print(f"📊 Tables ready:")
        print(f"   - social_accounts: {accounts_count} records") 
        print(f"   - actions: {actions_count} records")
        
        await conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    asyncio.run(check_and_create_tables())

