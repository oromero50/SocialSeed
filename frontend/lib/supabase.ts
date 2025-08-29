import { createClient } from '@supabase/supabase-js'

// Debug: Check what environment variables are actually loaded
console.log('🔍 Environment Variables Debug:');
console.log('NEXT_PUBLIC_SUPABASE_URL:', process.env.NEXT_PUBLIC_SUPABASE_URL);
console.log('NEXT_PUBLIC_SUPABASE_ANON_KEY:', process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY);

const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL || 'http://localhost:8000'
const supabaseAnonKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY || 'dummy_key_for_development'

// Validate environment variables before creating client
if (!supabaseUrl || !supabaseAnonKey) {
  console.error('❌ Missing required Supabase environment variables:');
  console.error('URL:', supabaseUrl);
  console.error('Key:', supabaseAnonKey ? 'Present' : 'Missing');
  console.warn('⚠️ Using default development values for Supabase (not actually used in this app)');
}

// Create the Supabase client
export const supabase = createClient(supabaseUrl, supabaseAnonKey, {
  auth: {
    autoRefreshToken: true,
    persistSession: true,
    detectSessionInUrl: true
  }
})

// Test connection function (to be called when needed, not immediately)
export const testSupabaseConnection = async () => {
  try {
    console.log('🧪 Testing Supabase connection...');
    const result = await supabase.from('social_accounts').select('count').limit(1);
    if (result.error) {
      console.error('❌ Supabase connection failed:', result.error);
      return false;
    } else {
      console.log('✅ Supabase connection successful!');
      return true;
    }
  } catch (error: any) {
    console.error('❌ Supabase connection error:', error);
    return false;
  }
};

// Database types based on your schema
export interface SocialAccount {
  id: string
  platform: 'tiktok' | 'instagram' | 'twitter'
  username: string
  access_token?: string
  phase?: number
  health_score?: number
  is_active: boolean
  created_at: string
  updated_at?: string
  follower_count?: number
  following_count?: number
  engagement_rate?: number
  display_name?: string
  post_count?: number
  tweet_count?: number
  last_sync?: string
  growth_potential?: string
}

export interface AccountHealth {
  id: string
  account_id: string
  health_score: number
  rate_limit_status: string
  last_action_time: string
  created_at: string
}

export interface ActionHistory {
  id: string
  account_id: string
  action_type: string
  platform: string
  status: string
  created_at: string
}
