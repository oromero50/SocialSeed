# SocialSeed v2.0 - Complete Setup Instructions
# Enterprise Social Media Orchestration with Phased Safety Approach

## 🚀 QUICK START GUIDE

### 1. CREATE REQUIRED SERVICE ACCOUNTS

**Essential Services (Create these first):**

1. **Supabase** (Database) - FREE TIER
   - Go to: https://supabase.com
   - Create project, get connection string
   - Copy to `DATABASE_URL` in .env

2. **DeepSeek** (AI - Primary) - $0.00014/1K tokens  
   - Go to: https://platform.deepseek.com
   - Create API key
   - Copy to `DEEPSEEK_API_KEY` in .env

3. **Railway** (Backend Hosting) - $5/month
   - Go to: https://railway.app  
   - Connect GitHub repo
   - Deploy backend service

4. **Vercel** (Frontend Hosting) - FREE TIER
   - Go to: https://vercel.com
   - Connect GitHub repo
   - Deploy frontend

5. **Upstash Redis** (Caching) - FREE TIER
   - Go to: https://upstash.com
   - Create Redis database
   - Copy connection string to `REDIS_URL`

**Optional for Later:**
- IPRoyal (Proxies) - $1.80/GB when ready to scale

### 2. CURSOR AI IMPLEMENTATION

**Copy all files into Cursor project:**

```bash
# Create project structure
mkdir socialseed-v2
cd socialseed-v2

# Backend files
mkdir backend
# Copy these files to backend/:
- updated_main.py -> main.py
- phase_manager.py  
- authenticity_analyzer.py
- behavioral_service.py
- ai_service.py
- tiktok_service.py
- proxy_service.py
- updated_schema.sql -> schema.sql
- updated_requirements.txt -> requirements.txt
- .env.example

# Frontend files  
mkdir frontend
# Copy these files to frontend/:
- package.json
- All React components for dashboard

# Configuration
- docker-compose.yml
- Dockerfile.backend
```

### 3. ENVIRONMENT SETUP

**Create .env file:**
```bash
cp .env.example .env
# Fill in your API keys and database credentials
```

**Install dependencies:**
```bash
# Backend
cd backend
pip install -r requirements.txt

# Frontend  
cd ../frontend
npm install
```

### 4. DATABASE SETUP

**Initialize database:**
```bash
# Run the schema
psql $DATABASE_URL -f schema.sql

# Or using Python
python -c "
import asyncio
from database import DatabaseManager
async def setup(): 
    db = DatabaseManager()
    await db.initialize()
asyncio.run(setup())
"
```

### 5. PLATFORM SETUP

**TikTok (Primary Platform):**
- Rate limit: 200 follows/day
- Get API access through TikTok Developer Program
- Phase 1: 60% of automation resources

**Instagram (Secondary):**  
- Rate limit: 150 follows/day
- Phase 2+: 30% of automation resources
- Use unofficial API (instagrapi)

**Twitter (Tertiary):**
- Rate limit: 400 follows/day (premium)
- Phase 3: 10% of automation resources
- Twitter Developer Account required

### 6. PHASE DEPLOYMENT

**Phase 1 (Days 1-30): Ultra-Conservative**
- TikTok ONLY
- 5 follows/hour maximum
- Human approval for ALL yellow/red flags  
- Build authentic baseline

**Phase 2 (Days 31-60): Controlled Scaling**
- Add Instagram
- 15 follows/hour on TikTok, 10 on Instagram
- Moderate risk tolerance
- LLM-optimized targeting

**Phase 3 (Days 61+): Full Operation**
- All platforms active
- 25 follows/hour maximum
- Hybrid human/AI management
- Continuous optimization

### 7. LAUNCH SEQUENCE

**Start Backend:**
```bash
cd backend
python main.py
# Runs on http://localhost:8000
```

**Start Frontend:**
```bash
cd frontend  
npm run dev
# Runs on http://localhost:3000
```

**Verify Services:**
- Dashboard: http://localhost:3000
- API Health: http://localhost:8000/platform-health
- Approval Queue: http://localhost:8000/approvals/pending

### 8. DAILY OPERATIONS

**Monitor Dashboard:**
- Account health scores
- Phase progression status
- Pending approvals queue
- Platform health indicators
- Traffic light system alerts

**Human Approval Tasks:**
- Review yellow/red flagged actions
- Approve/reject risky interactions
- Monitor authenticity scores
- Adjust safety thresholds

**Scaling Checklist:**
- Add proxies when budget allows ($75/month)
- Upgrade hosting as user base grows  
- Add more AI providers for redundancy
- Implement additional platforms

### 9. COST OPTIMIZATION

**Current Costs (No Proxies):**
- Supabase: $0/month (free tier)
- DeepSeek AI: ~$2/month  
- Railway: $5/month
- Vercel: $0/month (free tier)
- Redis: $0/month (free tier)
**Total: ~$7/month**

**With Proxies (When Ready):**
- Add IPRoyal: +$75/month
- Upgrade hosting: +$10/month  
**Total: ~$92/month**

### 10. TROUBLESHOOTING

**Common Issues:**
- Database connection: Check Supabase credentials
- AI service errors: Verify API keys and quotas
- Rate limiting: Check platform health dashboard
- Authentication: Ensure JWT secret is set

**Support Resources:**
- Check logs: `tail -f logs/socialseed.log`
- Health endpoint: GET /platform-health
- Database status: GET /dashboard/{user_id}

## 🎯 SUCCESS METRICS

**Phase 1 Goals:**
- Zero account bans
- >0.01 engagement rate
- <0.3 risk score maintained

**Phase 2 Goals:**  
- Successful Instagram integration
- 2x follower growth rate
- <5 consecutive errors

**Phase 3 Goals:**
- Full multi-platform operation
- Sustainable growth rates
- Human-AI hybrid efficiency

---

**Ready to build? Start with step 1 and work through each section systematically. The system is designed for solopreneurs but scales to enterprise levels.**
