#!/usr/bin/env python3
"""
Setup script to create follower tracking tables in Supabase
"""
import asyncio
import asyncpg
import os
from pathlib import Path

async def setup_follower_tables():
    """Create follower tracking tables in Supabase"""
    
    # Supabase connection details
    supabase_url = "uvqpkcidjhjwbqxvnvqp.supabase.co"
    supabase_password = "SocialSeed2024!"
    database_url = f"postgresql://postgres:{supabase_password}@db.{supabase_url}:5432/postgres"
    
    try:
        print("🔄 Connecting to Supabase...")
        conn = await asyncpg.connect(database_url)
        
        # Read SQL file
        sql_file = Path(__file__).parent / "backend" / "create_follower_tables.sql"
        with open(sql_file, 'r') as f:
            sql_commands = f.read()
        
        print("📊 Creating follower tracking tables...")
        await conn.execute(sql_commands)
        
        print("✅ Follower tracking tables created successfully!")
        
        # Verify tables exist
        tables = await conn.fetch("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public' 
            AND table_name IN ('follower_snapshots', 'unfollower_events', 'growth_analytics', 'follower_details')
            ORDER BY table_name
        """)
        
        print("\n📋 Created tables:")
        for table in tables:
            print(f"  ✅ {table['table_name']}")
            
        await conn.close()
        print("\n🎉 Database setup complete!")
        
    except Exception as e:
        print(f"❌ Error setting up database: {e}")
        return False
        
    return True

if __name__ == "__main__":
    asyncio.run(setup_follower_tables())
