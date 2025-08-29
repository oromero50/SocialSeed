# SocialSeed v2.0
## Budget-Optimized Multi-Platform Social Media Orchestrator

🎯 **TikTok Priority** • 📱 **Instagram Ready** • 🐦 **Twitter Support** • 🤖 **AI-Powered**

---

## Table of Contents

### Strategy & Architecture
- Executive Summary & Philosophy
- TikTok-First Strategy
- Multi-Platform Roadmap
- Cost Analysis & Budget

### Technical Implementation
- Project Structure & Setup
- Database Schema Design
- Backend API Implementation
- Frontend Dashboard

### Platform Integration
- TikTok Bot Implementation
- Instagram Integration
- Twitter Automation
- Safety & Monitoring

### Deployment & Scaling
- Proxy-Ready Infrastructure
- AI Provider Integration
- Deployment Strategy
- Growth & Monetization

---

## Executive Summary

### Project Vision

SocialSeed v2.0 is a cost-effective social media orchestration platform designed specifically for solopreneurs. It creates and manages authentic personas across multiple platforms to organically grow communities and promote products/services.

**Key Differentiators:**
- TikTok-first approach for maximum organic reach
- No initial proxy costs ($0 startup vs $75+/month)
- AI-powered content and persona generation
- Proxy-ready infrastructure for future scaling
- Multi-platform coordination and cross-promotion

### Business Impact

**Expected ROI Timeline:**
- **Month 1-2:** Foundation ($0 cost)
- **Month 3-4:** Growth (10K+ followers)
- **Month 5-6:** Monetization ($1K+/month)
- **Month 7+:** Scale ($5K+/month)

### Why This Approach Works

Traditional social media growth services focus on fake engagement. SocialSeed focuses on building genuine communities through intelligent automation that mimics authentic human behavior.

**✅ Authentic Growth** - Real followers, genuine engagement
**⚖️ Platform Compliant** - No ToS violations, ban-safe
**💰 Cost Effective** - $0 startup, scale as you grow

---

## TikTok-First Platform Strategy

### Why TikTok First?

#### 📈 Higher Rate Limits
- **TikTok:** 200 follows/day, 500 likes/day
- **Instagram:** 150 follows/day, 300 likes/day

#### ⚡ Algorithm Advantages
- Content-first discovery (vs follower-based)
- Viral potential regardless of follower count
- Less sophisticated bot detection
- Mobile-native behavior patterns

#### 🚀 Growth Potential
- 500-2000 followers/day possible safely
- Higher engagement rates
- Cross-platform promotion opportunities
- Trend-jacking for massive reach

### Multi-Platform Integration

**🎯 TikTok PRIMARY** - Content creation hub, viral growth engine
*Timeline: Month 1-2*

**📸 Instagram SECONDARY** - Professional presence, cross-promotion target
*Timeline: Month 2-3*

**🐦 Twitter/X SUPPORT** - Thought leadership, community building
*Timeline: Month 3-4*

### Growth Funnel Strategy

1. **Create** - Viral TikTok content
2. **Grow** - Build TikTok following
3. **Cross-Promote** - Drive to other platforms
4. **💰 Monetize** - Convert to customers

---

## Cost Analysis & Budget Optimization

### Traditional vs SocialSeed Costs

#### 📊 Phase 1: Foundation
**$0/month**
- No proxies required
- Free AI credits
- Supabase free tier
- Vercel free hosting
*Months 1-2*

#### 📈 Phase 2: Growth
**$20-50/month**
- Basic AI credits
- Optional budget proxies
- Upgraded hosting
- Mobile data for rotation
*Months 3-4*

#### 🚀 Phase 3: Scale
**$100-200/month**
- Residential proxies
- Premium AI models
- Professional hosting
- Advanced analytics
*Months 5+*

### Budget Optimization Strategies

**Cost-Saving Techniques:**
- Start with free AI provider credits
- Use mobile hotspot rotation instead of proxies
- Leverage free hosting tiers
- Gradual scaling based on revenue
- Open-source alternatives for all tools

**Revenue Optimization:**
- Build personal brand before monetizing
- Cross-platform audience growth
- Multiple revenue streams
- Early validation before scaling
- Community-driven growth

---

## Project Structure & Setup

### Technology Stack

#### 🔧 Backend
- Python 3.11+ with FastAPI
- Supabase (PostgreSQL + Auth)
- Celery + Redis for task queues
- AI provider integrations

#### 🎨 Frontend
- Next.js 14 + TypeScript
- Tailwind CSS + Shadcn/ui
- Zustand for state management
- TanStack Query for API calls

#### 🤖 Automation
- Selenium + undetected-chrome
- Platform-specific APIs where available
- Proxy-ready infrastructure
- Mobile-first automation

### Directory Structure

```
socialseed/
├── backend/
│   ├── app/
│   │   ├── core/
│   │   │   ├── persona_factory.py
│   │   │   ├── growth_engine.py
│   │   │   ├── content_orchestrator.py
│   │   │   └── safety_monitor.py
│   │   ├── platforms/
│   │   │   ├── tiktok/
│   │   │   │   ├── tiktok_bot.py
│   │   │   │   ├── tiktok_api.py
│   │   │   │   └── tiktok_utils.py
│   │   │   ├── instagram/
│   │   │   └── twitter/
│   │   ├── services/
│   │   │   ├── proxy_manager.py
│   │   │   ├── ai_service.py
│   │   │   └── account_manager.py
│   │   ├── api/
│   │   │   ├── personas.py
│   │   │   ├── accounts.py
│   │   │   └── campaigns.py
│   │   └── tasks/
│   │       ├── growth_tasks.py
│   │       └── content_tasks.py
├── frontend/
│   ├── src/
│   │   ├── app/
│   │   │   ├── dashboard/
│   │   │   ├── personas/
│   │   │   └── campaigns/
│   │   ├── components/
│   │   ├── hooks/
│   │   └── services/
├── config/
│   ├── personas/
│   ├── platforms/
│   └── ai_providers.yaml
└── docs/
```

---

## Database Schema Design

### Core Tables

```sql
-- Personas Table
CREATE TABLE personas (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    category VARCHAR(100) NOT NULL,
    niche VARCHAR(100) NOT NULL,
    personality_traits JSONB,
    communication_style JSONB,
    content_themes JSONB,
    target_audience JSONB,
    growth_strategy JSONB,
    ai_character_prompt TEXT,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Social Accounts Table 
CREATE TABLE social_accounts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    persona_id UUID REFERENCES personas(id),
    platform VARCHAR(50) NOT NULL,
    username VARCHAR(255) NOT NULL,
    email VARCHAR(255),
    password_encrypted TEXT,
    proxy_id UUID REFERENCES proxies(id),
    account_metrics JSONB,
    daily_limits JSONB,
    safety_score INTEGER DEFAULT 100,
    status VARCHAR(50) DEFAULT 'active',
    created_at TIMESTAMP DEFAULT NOW(),
    last_activity TIMESTAMP
);
```

### Proxy & Analytics Tables

```sql
-- Proxies Table (Future-Ready)
CREATE TABLE proxies (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    ip_address VARCHAR(45),
    port INTEGER,
    username VARCHAR(255),
    password_encrypted TEXT,
    country VARCHAR(10),
    provider VARCHAR(100),
    status VARCHAR(50) DEFAULT 'inactive',
    assigned_accounts INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Actions Log Table
CREATE TABLE actions_log (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    account_id UUID REFERENCES social_accounts(id),
    action_type VARCHAR(50) NOT NULL,
    target_username VARCHAR(255),
    success BOOLEAN,
    response_data JSONB,
    performed_at TIMESTAMP DEFAULT NOW()
);
```

### Database Design Principles

**Scalability Features:**
- UUID primary keys for distributed systems
- JSONB for flexible schema evolution
- Indexed foreign keys for performance
- Soft deletes for data recovery

**Future-Proofing:**
- Proxy table ready but unused initially
- Platform-agnostic account structure
- Extensible metrics and settings
- Audit trail for all actions

---

## AI Provider Integration

### Provider-Agnostic Architecture

```python
# backend/services/ai_service.py
class AIService:
    def __init__(self):
        self.providers = {}
        self.default_provider = None
        self.model_routing = {
            "persona_creation": {
                "preferred": ["anthropic", "openai"],
                "fallback": ["deepseek", "groq"]
            },
            "content_generation": {
                "preferred": ["anthropic", "google"],
                "fallback": ["openai", "deepseek"]
            },
            "quick_responses": {
                "preferred": ["groq", "deepseek"],
                "fallback": ["openai", "anthropic"]
            }
        }
    
    async def generate_completion(self, 
                                task_type: str,
                                messages: List[AIMessage],
                                preferred_provider: str = None):
        provider = self._select_provider(task_type, preferred_provider)
        return await provider.generate_completion(messages)
```

### Cost Optimization

**💰 Budget Providers**
- DeepSeek: $0.00014/1K tokens
- Groq: $0.00059/1K tokens
- OpenAI: $0.01/1K tokens

**🔄 Smart Routing**
- Use DeepSeek for bulk content
- Use Groq for quick responses
- Use premium models for personas
- Automatic fallback on failures

### AI Configuration Setup

```yaml
# config/ai_providers.yaml
ai_providers:
  deepseek:
    api_key: "${DEEPSEEK_API_KEY}"
    base_url: "https://api.deepseek.com/v1"
    enabled: true
    priority: 1  # Cheapest for bulk operations
    models:
      default: "deepseek-chat"
  
  groq:
    api_key: "${GROQ_API_KEY}"
    base_url: "https://api.groq.com/openai/v1"
    enabled: true
    priority: 2  # Fastest for quick responses
    models:
      default: "llama3-70b-8192"
  
  openai:
    api_key: "${OPENAI_API_KEY}"
    enabled: false  # Disabled initially to save costs
    priority: 3
    models:
      default: "gpt-4o-mini"
```

---

## TikTok Bot Implementation

### No-Proxy Safe Configuration

```python
# backend/platforms/tiktok/tiktok_bot.py
class TikTokBot:
    def __init__(self, account_data: Dict, persona: Dict):
        self.account = account_data
        self.persona = persona
        
        # No-proxy safe limits (conservative start)
        self.limits = {
            "daily_follows": 60,        # Start conservative
            "daily_likes": 150,         # TikTok allows more
            "daily_comments": 15,       # Limited commenting
            "daily_video_views": 300,   # Binge-watching normal
            "session_duration": 45,     # Shorter sessions
            "follow_speed_min": 45,     # Slower without proxies
            "like_speed_min": 8         # Natural liking speed
        }
    
    async def no_proxy_safety_mode(self):
        """Extra safety measures for no-proxy operation"""
        
        # Extended delays between actions
        self.limits["follow_speed_min"] = 120  # 2 minutes
        self.limits["session_duration"] = 30   # 30 min max
        
        # Add random breaks
        if random.random() < 0.3:  # 30% chance
            break_duration = random.randint(1800, 3600)  # 30-60 min
            await asyncio.sleep(break_duration)
```

### Mobile-First Automation

```python
async def initialize_mobile_simulation(self):
    """Mobile-first TikTok automation"""
    
    options = uc.ChromeOptions()
    
    # Mobile user agents
    mobile_agents = [
        "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X)",
        "Mozilla/5.0 (Android 13; Mobile; rv:109.0)"
    ]
    
    options.add_argument(f'--user-agent={random.choice(mobile_agents)}')
    
    # Mobile viewport
    mobile_viewports = [(375, 667), (414, 896), (390, 844)]
    width, height = random.choice(mobile_viewports)
    
    self.driver = uc.Chrome(options=options)
    self.driver.set_window_size(width, height)
    
    # Mobile touch simulation
    await self._setup_mobile_behaviors()
```

### Trend-Following Algorithm

```python
async def discover_trending_content(self) -> List[Dict]:
    """Discover trending content for engagement"""
    
    trending_data = []
    
    # Method 1: Trending hashtags
    hashtags = await self._get_trending_hashtags()
    
    for hashtag in hashtags[:10]:
        videos = await self._get_hashtag_videos(hashtag, limit=20)
        
        for video in videos:
            if self._should_engage_with_video(video):
                trending_data.append({
                    "type": "hashtag_video",
                    "hashtag": hashtag,
                    "creator": video["creator"],
                    "engagement_score": video["likes"] + video["shares"]
                })
    
    # Method 2: For You Page scraping
    fyp_videos = await self._scrape_fyp_content(limit=50)
    trending_data.extend(fyp_videos)
    
    return sorted(trending_data, 
                 key=lambda x: x["engagement_score"], 
                 reverse=True)[:100]
```

### Authentic Engagement

```python
async def engage_authentically(self, target_data: Dict):
    """Engage with content authentically"""
    
    engagement_plan = await self.ai_service.generate_engagement_plan(
        persona=self.persona,
        target_data=target_data,
        platform="tiktok"
    )
    
    for action in engagement_plan["actions"]:
        if action["type"] == "follow":
            # Natural profile viewing before following
            await self._view_profile_naturally(target_data["creator"])
            await asyncio.sleep(random.uniform(5, 15))
            
            success = await self._follow_user(target_data["creator"])
            if success:
                self.daily_actions["follows"] += 1
        
        elif action["type"] == "like_videos":
            for video_id in action["video_ids"]:
                await self._like_video_naturally(video_id)
                await asyncio.sleep(random.uniform(3, 8))
        
        elif action["type"] == "comment":
            comment_text = await self.ai_service.generate_comment(
                self.persona, target_data["video_content"]
            )
            await self._post_comment(target_data["video_id"], comment_text)
        
        # Wait between different action types
        await asyncio.sleep(random.uniform(30, 120))
```

---

## Proxy-Ready Infrastructure

### Current: No-Proxy Mode

```python
# backend/services/proxy_manager.py
class ProxyManager:
    def __init__(self):
        self.proxy_enabled = settings.USE_PROXIES
        self.proxy_providers = {}
    
    async def get_proxy_for_account(self, account_id: str) -> Optional[Dict]:
        """Get proxy configuration for account"""
        
        if not self.proxy_enabled:
            # No-proxy mode with extra safety
            return await self._no_proxy_config(account_id)
        
        # Future proxy logic here
        return await self._get_residential_proxy(account_id)
    
    async def _no_proxy_config(self, account_id: str) -> Dict:
        """Ultra-conservative no-proxy configuration"""
        
        return {
            "proxy": None,
            "safety_multiplier": 2.0,  # Double all delays
            "conservative_limits": True,
            "extended_breaks": True,
            "mobile_rotation_suggested": True,
            "max_daily_sessions": 3,
            "session_gap_hours": 4
        }
```

### Future: Proxy Integration

```python
async def _get_residential_proxy(self, account_id: str) -> Dict:
    """Get residential proxy when enabled"""
    
    # Select provider based on budget and requirements
    if self.budget_mode:
        provider = "iproyal"  # $7/month
        proxy = await self._get_budget_proxy(provider)
    else:
        provider = "smartproxy"  # $75/month
        proxy = await self._get_premium_proxy(provider)
    
    return {
        "proxy": proxy,
        "provider": provider,
        "rotation_schedule": "daily",
        "health_check_interval": 3600,  # 1 hour
        "failover_enabled": True
    }

async def enable_proxy_mode(self, budget_tier: str):
    """Enable proxy mode when ready to scale"""
    
    self.proxy_enabled = True
    
    if budget_tier == "budget":
        # Initialize budget proxy providers
        await self._setup_budget_proxies()
    elif budget_tier == "premium":
        # Initialize premium proxy providers
        await self._setup_premium_proxies()
    
    # Update all account configurations
    await self._migrate_accounts_to_proxy_mode()
```

### Proxy Migration Strategy

**▶️ Phase 1: Start Free** - No proxies, conservative limits
**→ Phase 2: Budget Proxies** - $7-15/month, shared proxies  
**→ Phase 3: Premium Scale** - $75+/month, dedicated proxies

---

## Multi-Platform Integration

### Platform Orchestration Engine

```python
# backend/core/growth_engine.py
class MultiPlatformOrchestrator:
    def __init__(self):
        self.platforms = {
            "tiktok": TikTokBot,
            "instagram": InstagramBot,
            "twitter": TwitterBot
        }
        self.cross_promotion_engine = CrossPromotionEngine()
    
    async def orchestrate_daily_growth(self, persona_id: str):
        """Coordinate growth activities across all platforms"""
        
        persona = await self.get_persona(persona_id)
        accounts = await self.get_persona_accounts(persona_id)
        
        # Phase-based platform activation
        active_platforms = self._get_active_platforms_for_phase(persona.phase)
        
        for platform in active_platforms:
            platform_accounts = [acc for acc in accounts if acc.platform == platform]
            
            for account in platform_accounts:
                # Execute platform-specific growth
                growth_task = await self._create_platform_growth_task(
                    platform, account, persona.growth_strategy
                )
                
                # Schedule with natural delays
                celery_app.send_task(
                    f'growth.{platform}_daily_task',
                    args=[account.id, growth_task],
                    countdown=random.randint(300, 1800)  # 5-30 min delay
                )
        
        # Cross-platform promotion
        await self._schedule_cross_promotion(persona_id)
    
    def _get_active_platforms_for_phase(self, phase: int) -> List[str]:
        """Return active platforms based on growth phase"""
        
        platform_activation = {
            1: ["tiktok"],                           # Focus on TikTok
            2: ["tiktok", "instagram"],              # Add Instagram
            3: ["tiktok", "instagram", "twitter"]    # Full platform suite
        }
        
        return platform_activation.get(phase, ["tiktok"])
```

### Platform-Specific Strategies

| Platform | Focus | Growth Rate | Content | Timing | Automation |
|----------|--------|-------------|---------|---------|------------|
| **TikTok** | Viral content creation | 100-500 followers/day | Trend-based videos | Peak engagement hours | Follow trending creators |
| **Instagram** | Professional presence | 50-200 followers/day | Curated feed posts | Morning and evening | Hashtag targeting |
| **Twitter** | Thought leadership | 20-100 followers/day | Text-based insights | Business hours | Tweet engagement |

### Cross-Platform Synergy

```python
# Cross-promotion automation
async def execute_cross_promotion(self, persona_id: str):
    """Execute cross-platform promotion strategy"""
    
    persona_accounts = await self.get_persona_accounts(persona_id)
    
    # TikTok → Instagram promotion
    tiktok_account = next(acc for acc in persona_accounts if acc.platform == "tiktok")
    instagram_account = next(acc for acc in persona_accounts if acc.platform == "instagram")
    
    if tiktok_account and instagram_account:
        # Share TikTok highlights on Instagram Stories
        viral_tiktoks = await self._get_viral_content(tiktok_account.id)
        
        for video in viral_tiktoks[:3]:  # Top 3 viral videos
            instagram_story = await self._create_instagram_story_from_tiktok(video)
            await self._post_instagram_story(instagram_account.id, instagram_story)
    
    # Instagram → Twitter promotion 
    if instagram_account:
        twitter_account = next(acc for acc in persona_accounts if acc.platform == "twitter")
        
        if twitter_account:
            # Tweet about Instagram posts
            recent_posts = await self._get_recent_instagram_posts(instagram_account.id)
            
            for post in recent_posts[:2]:  # Top 2 posts
                tweet = await self.ai_service.create_promotion_tweet(persona, post)
                await self._post_tweet(twitter_account.id, tweet)
```

---

## Safety & Monitoring System

### No-Proxy Safety Measures

```python
# backend/core/safety_monitor.py
class NoProxySafetyMonitor:
    def __init__(self):
        self.risk_thresholds = {
            "daily_action_limit": 0.6,    # 60% of platform limit
            "hourly_velocity": 8,         # Max 8 actions/hour
            "session_duration": 30,       # 30 min max sessions
            "consecutive_days": 5,        # Max 5 days straight
            "success_rate_min": 0.8       # 80% success required
        }
    
    async def assess_no_proxy_risk(self, account_id: str) -> Dict:
        """Enhanced risk assessment for no-proxy operation"""
        
        recent_actions = await self._get_recent_actions(account_id, hours=24)
        account_data = await self._get_account_data(account_id)
        
        risk_factors = {
            "velocity_risk": self._calculate_velocity_risk(recent_actions),
            "pattern_risk": self._detect_suspicious_patterns(recent_actions),
            "success_rate_risk": self._calculate_success_rate_decline(recent_actions),
            "account_age_protection": self._calculate_age_protection(account_data),
            "platform_behavior_deviation": self._detect_unnatural_behavior(recent_actions)
        }
        
        # No-proxy accounts need extra conservative scoring
        risk_score = self._calculate_conservative_risk_score(risk_factors)
        
        if risk_score > 0.5:  # Lower threshold for no-proxy
            await self._trigger_safety_pause(account_id)
        
        return {
            "risk_score": risk_score,
            "recommendations": self._generate_safety_recommendations(risk_factors),
            "immediate_actions": self._determine_safety_actions(risk_score)
        }
```

### Behavioral Pattern Analysis

```python
async def analyze_human_behavior_deviation(self, account_id: str) -> Dict:
    """Analyze deviation from human-like behavior"""
    
    behavior_metrics = await self._collect_behavior_metrics(account_id)
    
    # Human behavior indicators
    human_patterns = {
        "action_timing_variance": 0.8,              # High variance = human
        "session_length_distribution": "normal",     # Bell curve
        "break_frequency": "irregular",              # Irregular breaks
        "interaction_depth": "variable",             # Some deep, some shallow
        "content_preference_evolution": True         # Interests evolve
    }
    
    deviations = []
    
    # Check timing patterns
    if behavior_metrics["timing_variance"] < 0.3:
        deviations.append({
            "type": "timing_too_regular",
            "severity": "medium",
            "recommendation": "Add more randomization to action timing"
        })
    
    # Check session patterns
    if behavior_metrics["session_consistency"] > 0.9:
        deviations.append({
            "type": "session_too_consistent", 
            "severity": "high",
            "recommendation": "Vary session lengths and frequencies"
        })
    
    # Check interaction depth
    if behavior_metrics["shallow_interactions"] > 0.8:
        deviations.append({
            "type": "interactions_too_shallow",
            "severity": "medium", 
            "recommendation": "Add deeper content engagement"
        })
    
    return {
        "deviation_score": len(deviations) / 10,  # Normalize
        "deviations": deviations,
        "human_behavior_score": self._calculate_human_score(behavior_metrics)
    }
```

### Automated Safety Responses

**⚠️ Risk Level: High**
- Immediate pause all automation
- Send alert to user dashboard
- Enforce 24-48 hour cooldown
- Reset behavioral patterns
- Require manual review before restart

**🔶 Risk Level: Medium**
- Reduce automation limits by 50%
- Increase delays between actions
- Add more human simulation
- Monitor closely for 48 hours
- Gradually return to normal limits

---

## Frontend Dashboard Implementation

### Dashboard Components

```tsx
// frontend/src/components/Dashboard.tsx
import { useState, useEffect } from 'react';
import { PersonaGrid } from './PersonaGrid';
import { PlatformMetrics } from './PlatformMetrics';
import { SafetyAlerts } from './SafetyAlerts';

export const Dashboard = () => {
    const [personas, setPersonas] = useState([]);
    const [metrics, setMetrics] = useState({});
    const [alerts, setAlerts] = useState([]);

    return (
        <div className="min-h-screen bg-gray-50">
            {/* Header */}
            <div className="bg-white shadow">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                    <div className="py-6">
                        <h1 className="text-3xl font-bold text-gray-900">
                            SocialSeed Dashboard
                        </h1>
                        <p className="text-gray-600">
                            Manage your organic social media growth
                        </p>
                    </div>
                </div>
            </div>

            {/* Safety Alerts */}
            <SafetyAlerts alerts={alerts} />

            {/* Metrics Overview */}
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
                <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
                    <div className="bg-white p-6 rounded-lg shadow">
                        <h3 className="text-lg font-medium">Total Followers</h3>
                        <p className="text-3xl font-bold text-blue-600">
                            {metrics.totalFollowers || 0}
                        </p>
                    </div>
                    <div className="bg-white p-6 rounded-lg shadow">
                        <h3 className="text-lg font-medium">Active Accounts</h3>
                        <p className="text-3xl font-bold text-green-600">
                            {metrics.activeAccounts || 0}
                        </p>
                    </div>
                    <div className="bg-white p-6 rounded-lg shadow">
                        <h3 className="text-lg font-medium">Safety Score</h3>
                        <p className="text-3xl font-bold text-yellow-600">
                            {metrics.safetyScore || 100}%
                        </p>
                    </div>
                </div>

                {/* Platform Performance */}
                <PlatformMetrics />

                {/* Persona Management */}
                <PersonaGrid personas={personas} />
            </div>
        </div>
    );
};
```

### Real-Time Monitoring

```tsx
// frontend/src/components/SafetyMonitor.tsx
import { useEffect, useState } from 'react';
import { useWebSocket } from '@/hooks/useWebSocket';

export const SafetyMonitor = ({ accountId }) => {
    const [safetyData, setSafetyData] = useState(null);
    const { data, isConnected } = useWebSocket(`/ws/safety/${accountId}`);

    useEffect(() => {
        if (data) {
            setSafetyData(data);
        }
    }, [data]);

    const getRiskColor = (riskLevel) => {
        switch (riskLevel) {
            case 'low':
                return 'text-green-600 bg-green-100';
            case 'medium':
                return 'text-yellow-600 bg-yellow-100';
            case 'high':
                return 'text-red-600 bg-red-100';
            default:
                return 'text-gray-600 bg-gray-100';
        }
    };

    return (
        <div className="bg-white p-4 rounded-lg shadow">
            <div className="flex justify-between items-center mb-4">
                <h3 className="text-lg font-medium">Safety Monitor</h3>
                <div className={`px-2 py-1 rounded text-sm ${
                    isConnected ? 'bg-green-100 text-green-600' : 'bg-red-100 text-red-600'
                }`}>
                    {isConnected ? 'Connected' : 'Disconnected'}
                </div>
            </div>

            {safetyData && (
                <div>
                    <div className="flex justify-between items-center mb-2">
                        <div className={`px-3 py-1 rounded text-sm ${
                            getRiskColor(