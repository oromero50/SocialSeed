# TikTok Data Extraction Suite Integration Plan
# SocialSeed v2.0 - Historical Metrics & Analytics

## 🎯 INTEGRATION OVERVIEW

We're integrating the comprehensive TikTok Data Extraction Suite into SocialSeed to enable:
- **Historical follower/following tracking** with precise numbers
- **Engagement metrics analysis** over time
- **Follower list changes detection** (new/lost followers)
- **Growth analytics dashboard** with trend visualization
- **Automated data collection** with multiple extraction methods

## 📊 SUPABASE SCHEMA UPDATES

### New Tables for Historical Tracking

```sql
-- User Profile History Table
CREATE TABLE user_profile_history (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES auth.users(id),
    platform TEXT NOT NULL DEFAULT 'tiktok',
    username TEXT NOT NULL,
    display_name TEXT,
    follower_count INTEGER,
    following_count INTEGER,
    like_count BIGINT,
    video_count INTEGER,
    avatar_url TEXT,
    bio TEXT,
    is_verified BOOLEAN DEFAULT FALSE,
    is_private BOOLEAN DEFAULT FALSE,
    extracted_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    extraction_method TEXT DEFAULT 'api', -- 'playwright', 'api', 'mobile'
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Follower List History Table  
CREATE TABLE follower_history (
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
    UNIQUE(source_username, follower_username, extracted_at)
);

-- Video Metrics History Table
CREATE TABLE video_metrics_history (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES auth.users(id),
    username TEXT NOT NULL,
    video_id TEXT NOT NULL,
    description TEXT,
    view_count BIGINT,
    like_count INTEGER,
    comment_count INTEGER,
    share_count INTEGER,
    engagement_rate DECIMAL(5,2),
    video_url TEXT,
    thumbnail_url TEXT,
    duration INTEGER,
    video_created_at TIMESTAMP WITH TIME ZONE,
    extracted_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(video_id, extracted_at)
);

-- Growth Analytics Summary Table
CREATE TABLE growth_analytics (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES auth.users(id),
    platform TEXT NOT NULL DEFAULT 'tiktok',
    username TEXT NOT NULL,
    period_start TIMESTAMP WITH TIME ZONE,
    period_end TIMESTAMP WITH TIME ZONE,
    followers_start INTEGER,
    followers_end INTEGER,
    followers_gained INTEGER,
    followers_lost INTEGER,
    net_growth INTEGER,
    growth_rate DECIMAL(5,2),
    avg_daily_growth DECIMAL(8,2),
    engagement_rate_avg DECIMAL(5,2),
    total_videos INTEGER,
    total_views BIGINT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(user_id, username, period_start, period_end)
);

-- Indexes for Performance
CREATE INDEX idx_profile_history_username ON user_profile_history(username);
CREATE INDEX idx_profile_history_extracted_at ON user_profile_history(extracted_at);
CREATE INDEX idx_follower_history_source ON follower_history(source_username);
CREATE INDEX idx_follower_history_extracted_at ON follower_history(extracted_at);
CREATE INDEX idx_video_metrics_username ON video_metrics_history(username);
CREATE INDEX idx_growth_analytics_user ON growth_analytics(user_id, username);
```

## 🔧 BACKEND INTEGRATION

### 1. TikTok Extractor Service (backend/services/tiktok_extractor.py)

```python
"""
TikTok Data Extraction Service with Supabase Integration
Combines the three extraction methods with historical storage
"""

import asyncio
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import logging
from supabase import create_client, Client
from .tiktok_suite import TikTokDataExtractor, TikTokPlaywrightExtractor

class TikTokExtractorService:
    def __init__(self, supabase_client: Client):
        self.supabase = supabase_client
        self.extractor = TikTokDataExtractor()
        self.logger = logging.getLogger(__name__)
    
    async def extract_and_store_profile(self, user_id: str, username: str, 
                                      method: str = 'api', ms_token: str = None) -> Dict[str, Any]:
        """Extract profile data and store in Supabase"""
        try:
            # Setup extractor based on method
            if method == 'playwright':
                client = self.extractor.setup_playwright_method(headless=True)
                async with client as browser:
                    await browser.setup_browser()
                    profile_data = await self.extractor.extract_complete_profile(
                        username=username, method='playwright'
                    )
            elif method == 'api':
                api_client = self.extractor.setup_api_method(ms_token=ms_token)
                await api_client.setup()
                profile_data = await self.extractor.extract_complete_profile(
                    username=username, method='api'
                )
            
            if profile_data and 'error' not in profile_data:
                # Store in Supabase
                result = self.supabase.table('user_profile_history').insert({
                    'user_id': user_id,
                    'platform': 'tiktok',
                    'username': username,
                    'display_name': profile_data.get('display_name'),
                    'follower_count': profile_data.get('follower_count', 0),
                    'following_count': profile_data.get('following_count', 0),
                    'like_count': profile_data.get('like_count', 0),
                    'video_count': profile_data.get('video_count', 0),
                    'avatar_url': profile_data.get('avatar_url'),
                    'bio': profile_data.get('bio'),
                    'is_verified': profile_data.get('is_verified', False),
                    'is_private': profile_data.get('is_private', False),
                    'extraction_method': method
                }).execute()
                
                # Calculate growth if previous data exists
                await self._calculate_growth_metrics(user_id, username)
                
                return {
                    'success': True,
                    'data': profile_data,
                    'stored_id': result.data[0]['id'] if result.data else None
                }
            
            return {'error': 'Failed to extract profile data'}
            
        except Exception as e:
            self.logger.error(f"Profile extraction error: {str(e)}")
            return {'error': str(e)}
    
    async def extract_and_store_followers(self, user_id: str, username: str,
                                        limit: int = 100, method: str = 'playwright') -> Dict[str, Any]:
        """Extract follower list and detect changes"""
        try:
            if method == 'playwright':
                client = self.extractor.setup_playwright_method(headless=True)
                async with client as browser:
                    await browser.setup_browser()
                    social_data = await self.extractor.extract_followers_following(
                        username=username, method='playwright', followers_limit=limit
                    )
            
            followers = social_data.get('followers', [])
            
            if followers:
                # Get previous follower list for comparison
                previous_followers = self._get_latest_followers(username)
                
                # Detect changes
                changes = self._detect_follower_changes(previous_followers, followers)
                
                # Store new follower data
                for follower in followers:
                    self.supabase.table('follower_history').insert({
                        'source_user_id': user_id,
                        'source_username': username,
                        'follower_username': follower.get('username'),
                        'follower_user_id': follower.get('user_id'),
                        'follower_display_name': follower.get('display_name'),
                        'follower_avatar_url': follower.get('avatar_url'),
                        'is_verified': follower.get('is_verified', False),
                        'status': 'active'
                    }).execute()
                
                return {
                    'success': True,
                    'followers_extracted': len(followers),
                    'changes': changes
                }
            
            return {'error': 'No followers extracted'}
            
        except Exception as e:
            self.logger.error(f"Follower extraction error: {str(e)}")
            return {'error': str(e)}
    
    async def _calculate_growth_metrics(self, user_id: str, username: str):
        """Calculate and store growth analytics"""
        try:
            # Get last 30 days of data
            thirty_days_ago = datetime.now() - timedelta(days=30)
            
            result = self.supabase.table('user_profile_history').select('*').eq(
                'user_id', user_id
            ).eq('username', username).gte(
                'extracted_at', thirty_days_ago.isoformat()
            ).order('extracted_at', desc=False).execute()
            
            if len(result.data) >= 2:
                first_record = result.data[0]
                last_record = result.data[-1]
                
                followers_start = first_record['follower_count']
                followers_end = last_record['follower_count']
                net_growth = followers_end - followers_start
                
                period_days = (
                    datetime.fromisoformat(last_record['extracted_at']) - 
                    datetime.fromisoformat(first_record['extracted_at'])
                ).days
                
                if period_days > 0:
                    avg_daily_growth = net_growth / period_days
                    growth_rate = (net_growth / followers_start * 100) if followers_start > 0 else 0
                    
                    # Store growth analytics
                    self.supabase.table('growth_analytics').upsert({
                        'user_id': user_id,
                        'username': username,
                        'period_start': first_record['extracted_at'],
                        'period_end': last_record['extracted_at'],
                        'followers_start': followers_start,
                        'followers_end': followers_end,
                        'net_growth': net_growth,
                        'growth_rate': round(growth_rate, 2),
                        'avg_daily_growth': round(avg_daily_growth, 2)
                    }).execute()
            
        except Exception as e:
            self.logger.error(f"Growth calculation error: {str(e)}")
    
    def get_growth_analytics(self, user_id: str, username: str, days: int = 30) -> Dict[str, Any]:
        """Get growth analytics for dashboard"""
        try:
            start_date = datetime.now() - timedelta(days=days)
            
            result = self.supabase.table('growth_analytics').select('*').eq(
                'user_id', user_id
            ).eq('username', username).gte(
                'period_start', start_date.isoformat()
            ).order('period_end', desc=True).limit(1).execute()
            
            if result.data:
                return {
                    'success': True,
                    'analytics': result.data[0]
                }
            
            return {'error': 'No growth data available'}
            
        except Exception as e:
            return {'error': str(e)}
    
    def get_historical_chart_data(self, user_id: str, username: str, days: int = 30) -> Dict[str, Any]:
        """Get data for growth charts"""
        try:
            start_date = datetime.now() - timedelta(days=days)
            
            result = self.supabase.table('user_profile_history').select(
                'extracted_at, follower_count, following_count, like_count'
            ).eq('user_id', user_id).eq('username', username).gte(
                'extracted_at', start_date.isoformat()
            ).order('extracted_at', desc=False).execute()
            
            return {
                'success': True,
                'chart_data': result.data
            }
            
        except Exception as e:
            return {'error': str(e)}
```

### 2. API Endpoints (backend/main.py additions)

```python
@app.post("/tiktok/extract-profile")
async def extract_tiktok_profile(request: TikTokExtractRequest):
    """Extract and store TikTok profile data"""
    extractor_service = TikTokExtractorService(supabase)
    
    result = await extractor_service.extract_and_store_profile(
        user_id=request.user_id,
        username=request.username,
        method=request.method,
        ms_token=request.ms_token
    )
    
    return result

@app.post("/tiktok/extract-followers")
async def extract_tiktok_followers(request: TikTokFollowersRequest):
    """Extract and analyze follower changes"""
    extractor_service = TikTokExtractorService(supabase)
    
    result = await extractor_service.extract_and_store_followers(
        user_id=request.user_id,
        username=request.username,
        limit=request.limit,
        method=request.method
    )
    
    return result

@app.get("/tiktok/analytics/{user_id}/{username}")
async def get_tiktok_analytics(user_id: str, username: str, days: int = 30):
    """Get growth analytics for dashboard"""
    extractor_service = TikTokExtractorService(supabase)
    
    analytics = extractor_service.get_growth_analytics(user_id, username, days)
    chart_data = extractor_service.get_historical_chart_data(user_id, username, days)
    
    return {
        'analytics': analytics,
        'chart_data': chart_data
    }
```

## 🎨 FRONTEND ANALYTICS DASHBOARD

### Enhanced Account Manager with Historical Metrics

```typescript
// frontend/components/HistoricalAnalytics.tsx
interface HistoricalAnalyticsProps {
  userId: string;
  username: string;
  platform: string;
}

const HistoricalAnalytics: React.FC<HistoricalAnalyticsProps> = ({ userId, username, platform }) => {
  const [analyticsData, setAnalyticsData] = useState(null);
  const [chartData, setChartData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [timeRange, setTimeRange] = useState(30);

  useEffect(() => {
    fetchAnalytics();
  }, [timeRange]);

  const fetchAnalytics = async () => {
    try {
      const response = await fetch(`/api/tiktok/analytics/${userId}/${username}?days=${timeRange}`);
      const data = await response.json();
      
      setAnalyticsData(data.analytics);
      setChartData(data.chart_data);
    } catch (error) {
      console.error('Analytics fetch error:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <div>Loading analytics...</div>;

  return (
    <div className="space-y-6">
      {/* Time Range Selector */}
      <div className="flex space-x-4">
        {[7, 30, 90].map(days => (
          <button
            key={days}
            onClick={() => setTimeRange(days)}
            className={`px-4 py-2 rounded ${timeRange === days ? 'bg-blue-500 text-white' : 'bg-gray-200'}`}
          >
            {days} days
          </button>
        ))}
      </div>

      {/* Growth Metrics Cards */}
      {analyticsData && (
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          <MetricCard
            title="Followers Gained"
            value={analyticsData.followers_gained || 0}
            change={`+${analyticsData.growth_rate || 0}%`}
            positive={analyticsData.net_growth > 0}
          />
          <MetricCard
            title="Daily Average Growth"
            value={Math.round(analyticsData.avg_daily_growth || 0)}
            suffix="per day"
          />
          <MetricCard
            title="Net Growth"
            value={analyticsData.net_growth || 0}
            positive={analyticsData.net_growth > 0}
          />
          <MetricCard
            title="Growth Rate"
            value={`${analyticsData.growth_rate || 0}%`}
            positive={analyticsData.growth_rate > 0}
          />
        </div>
      )}

      {/* Growth Chart */}
      <div className="bg-white p-6 rounded-lg shadow">
        <h3 className="text-lg font-semibold mb-4">Follower Growth Over Time</h3>
        <ResponsiveContainer width="100%" height={300}>
          <LineChart data={chartData}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="extracted_at" />
            <YAxis />
            <Tooltip />
            <Line type="monotone" dataKey="follower_count" stroke="#8884d8" strokeWidth={2} />
            <Line type="monotone" dataKey="following_count" stroke="#82ca9d" strokeWidth={2} />
          </LineChart>
        </ResponsiveContainer>
      </div>

      {/* Engagement Trends */}
      <div className="bg-white p-6 rounded-lg shadow">
        <h3 className="text-lg font-semibold mb-4">Engagement Trends</h3>
        <ResponsiveContainer width="100%" height={200}>
          <AreaChart data={chartData}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="extracted_at" />
            <YAxis />
            <Tooltip />
            <Area type="monotone" dataKey="like_count" stackId="1" stroke="#ffc658" fill="#ffc658" />
          </AreaChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
};
```

## 🔄 AUTOMATED DATA COLLECTION

### Background Tasks (backend/tasks/data_collection.py)

```python
import asyncio
from datetime import datetime, timedelta
from celery import Celery
from ..services.tiktok_extractor import TikTokExtractorService

# Setup Celery for background tasks
celery_app = Celery('socialseed', broker='redis://localhost:6379')

@celery_app.task
def collect_daily_metrics():
    """Automated daily data collection for all active accounts"""
    # Get all active TikTok accounts
    accounts = supabase.table('social_accounts').select('*').eq('platform', 'tiktok').eq('is_active', True).execute()
    
    for account in accounts.data:
        try:
            # Extract profile data
            asyncio.run(extract_profile_task(account))
            
            # Extract followers (weekly)
            if datetime.now().weekday() == 0:  # Monday
                asyncio.run(extract_followers_task(account))
                
        except Exception as e:
            logger.error(f"Collection error for {account['username']}: {str(e)}")

async def extract_profile_task(account):
    """Extract profile data for a single account"""
    extractor_service = TikTokExtractorService(supabase)
    
    result = await extractor_service.extract_and_store_profile(
        user_id=account['user_id'],
        username=account['username'],
        method='api'  # Use API method for automated collection
    )
    
    return result
```

## 📅 IMPLEMENTATION TIMELINE

### Week 1: Core Integration
- [ ] Copy TikTok extraction suite to `backend/services/`
- [ ] Create Supabase schema with historical tables
- [ ] Implement `TikTokExtractorService` class
- [ ] Add basic API endpoints for data extraction

### Week 2: Frontend Analytics
- [ ] Create `HistoricalAnalytics` component
- [ ] Integrate charts with Recharts library
- [ ] Add analytics to Account Manager
- [ ] Implement real-time data refresh

### Week 3: Automation & Polish
- [ ] Set up automated data collection with Celery
- [ ] Add follower change detection
- [ ] Implement growth trend analysis
- [ ] Add export functionality for historical data

### Week 4: Testing & Optimization
- [ ] Test all three extraction methods
- [ ] Optimize database queries and indexes
- [ ] Add error handling and retry logic
- [ ] Performance testing with rate limiting

## 🔧 CONFIGURATION UPDATES

### Environment Variables (.env)
```bash
# TikTok Integration
TIKTOK_MS_TOKEN_DEFAULT=your_default_ms_token
TIKTOK_RATE_LIMIT_MIN=2.0
TIKTOK_RATE_LIMIT_MAX=5.0
PLAYWRIGHT_HEADLESS=true

# Celery (for background tasks)
CELERY_BROKER_URL=redis://localhost:6379
CELERY_RESULT_BACKEND=redis://localhost:6379

# Supabase (enhanced for historical data)
SUPABASE_HISTORICAL_RETENTION_DAYS=365
```

This integration plan provides:
1. **Complete historical tracking** of follower/following counts
2. **Follower list change detection** (new/lost followers)
3. **Automated daily data collection** 
4. **Rich analytics dashboard** with growth charts
5. **Three extraction methods** for reliability
6. **Scalable Supabase storage** with proper indexing

The system will enable users to track their TikTok growth over time, identify trends, and understand their audience changes in detail.
