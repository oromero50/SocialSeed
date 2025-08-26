import { createClient } from '@supabase/supabase-js'

// Debug: Check what environment variables are actually loaded
console.log('🔍 Environment Variables Debug:');
console.log('NEXT_PUBLIC_SUPABASE_URL:', process.env.NEXT_PUBLIC_SUPABASE_URL);
console.log('NEXT_PUBLIC_SUPABASE_ANON_KEY:', process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY);

const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL!
const supabaseAnonKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!

// Validate environment variables before creating client
if (!supabaseUrl || !supabaseAnonKey) {
  console.error('❌ Missing required Supabase environment variables:');
  console.error('URL:', supabaseUrl);
  console.error('Key:', supabaseAnonKey ? 'Present' : 'Missing');
  throw new Error('Missing Supabase environment variables. Check your .env file.');
}

// Create the Supabase client
export const supabase = createClient(supabaseUrl, supabaseAnonKey, {
  auth: {
    autoRefreshToken: true,
    persistSession: true,
    detectSessionInUrl: true
  }
})

// Test the connection immediately
console.log('🧪 Testing Supabase connection...');
(async () => {
  try {
    const result = await supabase.from('social_accounts').select('count').limit(1);
    if (result.error) {
      console.error('❌ Supabase connection failed:', result.error);
    } else {
      console.log('✅ Supabase connection successful!');
    }
  } catch (error: any) {
    console.error('❌ Supabase connection error:', error);
  }
})();

// Database types based on your schema
export interface SocialAccount {
  id: string
  platform: 'tiktok' | 'instagram' | 'twitter'
  username: string
  access_token: string
  phase: number
  health_score: number
  is_active: boolean
  created_at: string
  updated_at: string
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
