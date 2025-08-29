# SocialSeed v2.0 🚀

**Enterprise Social Media Orchestration with Phased Safety Approach**

A sophisticated, enterprise-grade social media automation platform designed for solopreneurs and businesses that prioritizes account safety through intelligent phased deployment and human-in-the-loop approval systems.

## ✨ Features

### 🛡️ **Phased Safety System**
- **Phase 1 (Days 1-30)**: Ultra-conservative TikTok-only operations
- **Phase 2 (Days 31-60)**: Controlled scaling with Instagram integration
- **Phase 3 (Days 61+)**: Full multi-platform operation with hybrid AI/human management

### 🤖 **AI-Powered Intelligence**
- **DeepSeek Primary**: Cost-optimized AI provider ($0.00014/1K tokens)
- **Multi-Provider Fallback**: Groq, Anthropic, OpenAI for redundancy
- **Authenticity Analysis**: AI-powered account verification
- **Risk Assessment**: Real-time action risk evaluation

### 📊 **Real-Time Monitoring**
- **Traffic Light System**: Green/Yellow/Red risk indicators
- **Platform Health Dashboard**: Live status monitoring
- **Human Approval Workflow**: Manual review for high-risk actions
- **Performance Analytics**: Growth metrics and trend analysis

### 🔄 **Multi-Platform Support**
- **TikTok**: Primary platform (200 follows/day limit)
- **Instagram**: Secondary platform (150 follows/day limit)
- **Twitter**: Tertiary platform (400 follows/day limit)

### 🚀 **Scalability Features**
- **Proxy Rotation**: IPRoyal, SmartProxy, BrightData support
- **Rate Limiting**: Platform-specific safety thresholds
- **Behavioral Simulation**: Human-like action patterns
- **Graceful Degradation**: Automatic fallback systems

## 🏗️ Architecture

```
SocialSeed v2.0
├── Backend (FastAPI + Python)
│   ├── Phase Manager
│   ├── AI Service Provider
│   ├── Platform Services (TikTok, Instagram, Twitter)
│   ├── Database Manager (PostgreSQL)
│   ├── Proxy Service
│   └── Behavioral Simulator
├── Frontend (Next.js + React)
│   ├── Dashboard
│   ├── Approval Queue
│   ├── Analytics
│   └── Settings
└── Infrastructure
    ├── Docker Compose
    ├── PostgreSQL
    └── Redis
```

## 🚀 Quick Start

### 1. **Clone Repository**
```bash
git clone https://github.com/oromero50/SocialSeed.git
cd SocialSeed
```

### 2. **Environment Setup**
```bash
# Copy environment template
cp backend/.env.example backend/.env

# Edit with your API keys
nano backend/.env
```

### 3. **Docker Deployment**
```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f
```

### 4. **Access Applications**
- **Dashboard**: http://localhost:3000
- **API**: http://localhost:8000
- **Database**: localhost:5432
- **Redis**: localhost:6379

## 🔑 Required Services

### **Essential (Free Tier)**
- **Supabase**: Database hosting
- **DeepSeek**: AI service (primary)
- **Vercel**: Frontend hosting
- **Upstash Redis**: Caching

### **Recommended ($5/month)**
- **Railway**: Backend hosting
- **IPRoyal**: Proxy rotation ($75/month when scaling)

## 📊 Cost Breakdown

| Service | Cost | Tier |
|---------|------|------|
| Supabase | $0 | Free |
| DeepSeek | ~$2 | Pay-per-use |
| Railway | $5 | Basic |
| Vercel | $0 | Free |
| Redis | $0 | Free |
| **Total** | **~$7** | **Basic Setup** |

*With proxies: +$75/month for enterprise scaling*

## 🎯 Phase Deployment Guide

### **Phase 1: Foundation (Days 1-30)**
- ✅ TikTok platform only
- ✅ 5 follows/hour maximum
- ✅ Human approval for ALL yellow/red flags
- ✅ Build authentic baseline
- ✅ Zero account bans target

### **Phase 2: Controlled Scaling (Days 31-60)**
- ✅ Add Instagram platform
- ✅ 15 follows/hour on TikTok, 10 on Instagram
- ✅ Moderate risk tolerance
- ✅ LLM-optimized targeting
- ✅ <5 consecutive errors target

### **Phase 3: Full Operation (Days 61+)**
- ✅ All platforms active
- ✅ 25 follows/hour maximum
- ✅ Hybrid human/AI management
- ✅ Continuous optimization
- ✅ Sustainable growth rates

## 🛠️ Development

### **Backend Development**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

### **Frontend Development**
```bash
cd frontend
npm install
npm run dev
```

### **Database Management**
```bash
# Initialize schema
psql $DATABASE_URL -f backend/schema.sql

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

## 📈 Monitoring & Analytics

### **Dashboard Metrics**
- Account health scores
- Phase progression status
- Pending approvals queue
- Platform health indicators
- Traffic light system alerts

### **Health Endpoints**
- `GET /platform-health`: Platform status
- `GET /dashboard/{user_id}`: User analytics
- `GET /approvals/pending`: Approval queue

## 🔒 Security Features

- **JWT Authentication**: Secure API access
- **Rate Limiting**: Platform-specific thresholds
- **Proxy Rotation**: IP address management
- **Human Approval**: Manual review for risky actions
- **Audit Logging**: Complete action history

## 🚨 Troubleshooting

### **Common Issues**
- **Database Connection**: Check Supabase credentials
- **AI Service Errors**: Verify API keys and quotas
- **Rate Limiting**: Check platform health dashboard
- **Authentication**: Ensure JWT secret is set

### **Support Resources**
- **Logs**: `tail -f logs/socialseed.log`
- **Health Check**: `GET /platform-health`
- **Database Status**: `GET /dashboard/{user_id}`

## 📚 API Documentation

### **Core Endpoints**
```
POST /accounts/create          # Create new account
GET  /accounts/{id}           # Get account details
POST /actions/execute          # Execute social media action
GET  /approvals/pending       # Get pending approvals
POST /approvals/{id}/approve  # Approve action
GET  /platform-health         # Platform health status
GET  /dashboard/{user_id}     # User dashboard data
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- **Documentation**: [COMPLETE_SETUP_GUIDE.md](COMPLETE_SETUP_GUIDE.md)
- **Issues**: GitHub Issues
- **Discussions**: GitHub Discussions

---

**Ready to scale your social media presence safely? Start with Phase 1 and build your foundation! 🚀**

*Built with ❤️ for entrepreneurs who value both growth and account safety.*
