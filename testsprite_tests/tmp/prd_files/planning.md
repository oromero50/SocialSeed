# SocialSeed v2.0 - Technical Planning & Architecture Document

## 🏗️ System Architecture Overview

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                     SocialSeed v2.0 Platform                   │
├─────────────────────────────────────────────────────────────────┤
│  Frontend (Next.js + React + TypeScript)                       │
│  ├── Dashboard Component                                        │
│  ├── Account Management                                         │
│  ├── Approval Interface                                         │
│  ├── Analytics Dashboard                                        │
│  └── Real-time Monitoring                                       │
├─────────────────────────────────────────────────────────────────┤
│  Backend API (FastAPI + Python)                                │
│  ├── SocialSeedOrchestrator (Main Controller)                  │
│  ├── Phase Manager (3-Phase Safety System)                     │
│  ├── AI Service Provider (Multi-Provider)                      │
│  ├── Platform Services (TikTok/Instagram/Twitter)              │
│  ├── Traffic Light System (Risk Assessment)                    │
│  ├── Human Approval Workflow                                   │
│  ├── Behavioral Simulator                                       │
│  └── Authenticity Analyzer                                     │
├─────────────────────────────────────────────────────────────────┤
│  Data Layer                                                     │
│  ├── PostgreSQL (Supabase) - Primary Database                  │
│  ├── Redis (Upstash) - Caching & Session Management            │
│  └── Local Storage - Temporary Data & Logs                     │
├─────────────────────────────────────────────────────────────────┤
│  External Services                                              │
│  ├── AI Providers (DeepSeek → Groq → OpenAI → Anthropic)       │
│  ├── Social Platforms (TikTok, Instagram, Twitter APIs)        │
│  ├── Proxy Services (IPRoyal, SmartProxy, BrightData)          │
│  └── GitHub Integration (Repository Sync)                      │
└─────────────────────────────────────────────────────────────────┘
```

## 📁 Project Structure & Implementation

### Current Directory Structure
```
SocialSeed/
├── 🐍 backend/                     # Python FastAPI Backend
│   ├── main.py                     # ✅ Main application entry point
│   ├── phase_manager.py            # ✅ 3-phase safety system
│   ├── ai_service.py               # ✅ Multi-provider AI service
│   ├── database.py                 # ✅ PostgreSQL database manager
│   ├── authenticity_analyzer.py    # ✅ Account quality analysis
│   ├── behavioral_service.py       # ✅ Human behavior simulation
│   ├── tiktok_service.py           # ✅ TikTok platform integration
│   ├── instagram_service.py        # ✅ Instagram platform integration
│   ├── twitter_service.py          # ✅ Twitter platform integration
│   ├── proxy_service.py            # ✅ Proxy rotation management
│   ├── requirements.txt            # ✅ Python dependencies
│   ├── schema.sql                  # ✅ Database schema definition
│   ├── .env                        # ✅ Environment configuration
│   └── Dockerfile                  # ✅ Container configuration
├── ⚛️ frontend/                    # Next.js React Frontend
│   ├── components/
│   │   └── Dashboard.tsx           # ✅ Main dashboard component
│   ├── pages/
│   │   ├── index.tsx               # ✅ Home page
│   │   └── _app.tsx                # ✅ App wrapper
│   ├── lib/
│   │   └── supabase.ts             # ✅ Database client
│   ├── styles/
│   │   └── globals.css             # ✅ Global styles
│   ├── package.json                # ✅ Node.js dependencies
│   ├── tailwind.config.js          # ✅ Tailwind CSS config
│   ├── next.config.js              # ✅ Next.js configuration
│   ├── tsconfig.json               # ✅ TypeScript config
│   ├── .env.local                  # ✅ Frontend environment
│   └── Dockerfile                  # ✅ Container configuration
├── 🐳 Infrastructure/
│   ├── docker-compose.yml          # ✅ Service orchestration
│   └── start.sh                    # ✅ One-click startup script
├── 📊 logs/
│   └── deployment_progress.md      # ✅ Deployment tracking
├── 📚 Documentation/
│   ├── PRD.md                      # ✅ Product requirements
│   ├── planning.md                 # 🔄 This document
│   └── tasks.md                    # ⏳ Task management
└── 🔧 Configuration/
    ├── .env.example                # ✅ Environment template
    ├── .gitignore                  # ✅ Git exclusions
    └── README.md                   # ✅ Project overview
```

## 🚀 Backend Architecture Deep Dive

### Core Components

#### 1. **SocialSeedOrchestrator** (main.py)
**Purpose**: Central coordination system for all platform operations

**Key Responsibilities**:
- Initialize and manage all subsystems
- Route incoming requests to appropriate services
- Handle cross-cutting concerns (logging, error handling)
- Manage background task execution
- Coordinate phase transitions

**Current Implementation Status**: ✅ **COMPLETE**
```python
class SocialSeedOrchestrator:
    def __init__(self):
        # Core services initialization
        self.db = DatabaseManager()
        self.ai_service = AIServiceProvider()
        self.phase_manager = PhaseManager(self.db, self.ai_service)
        # ... platform services, monitoring, etc.
    
    async def execute_action(self, account_id, action_type, target_data):
        # Multi-step execution pipeline with safety checks
```

#### 2. **Phase Manager** (phase_manager.py)
**Purpose**: Implements the 3-phase safety progression system

**Phase Definitions**:
- **Phase 1 (Days 1-30)**: TikTok only, 50-100 actions/day, human approval required
- **Phase 2 (Days 31-60)**: TikTok + Instagram, 100-150 actions/day, selective approval
- **Phase 3 (Days 61+)**: All platforms, full automation, emergency approval only

**Current Implementation Status**: ✅ **COMPLETE**
```python
class PhaseManager:
    async def get_phase_config(self, account_id: str) -> PhaseConfig:
        # Dynamic configuration based on account age and performance
    
    async def assess_action_risk(self, account_id, action_type) -> RiskAssessment:
        # AI-powered risk evaluation with traffic light system
```

#### 3. **AI Service Provider** (ai_service.py)
**Purpose**: Multi-provider AI system with intelligent fallback

**Provider Hierarchy**:
1. **DeepSeek** (Primary): $0.00014/1K tokens - Cost optimized
2. **Groq** (Fallback): Fast inference, free tier
3. **OpenAI** (Fallback): Reliable, premium pricing
4. **Anthropic** (Emergency): High quality, premium pricing

**Current Implementation Status**: ✅ **COMPLETE**
```python
class AIServiceProvider:
    async def get_completion(self, prompt: str, provider: AIProvider = None):
        # Automatic failover between providers
        # Token usage tracking and cost optimization
```

#### 4. **Platform Services** (tiktok_service.py, instagram_service.py, twitter_service.py)
**Purpose**: Platform-specific automation implementations

**Common Interface**:
```python
class BasePlatformService:
    async def execute_action(self, account_id, action_type, target_data):
        # Platform-specific action execution
    
    async def get_health_status(self, account_id):
        # Account health monitoring
    
    async def simulate_human_behavior(self, action_type):
        # Natural timing and behavior patterns
```

**Platform-Specific Limits**:
- **TikTok**: 200 follows/day, 100 likes/day
- **Instagram**: 150 follows/day, 75 likes/day  
- **Twitter**: 400 follows/day, 200 likes/day

**Current Implementation Status**: ✅ **COMPLETE**

#### 5. **Database Manager** (database.py)
**Purpose**: PostgreSQL data access layer with connection pooling

**Key Features**:
- Async connection pooling for performance
- Comprehensive CRUD operations for all entities
- Health monitoring and reconnection logic
- Transaction management for data consistency

**Current Implementation Status**: ✅ **COMPLETE** (with recent fixes)
```python
class DatabaseManager:
    async def get_all_pending_approvals(self) -> List[Dict]:
        # Recently added method for approval workflow
    
    async def log_action(self, account_id, action_type, result):
        # Comprehensive action logging for analytics
```

### API Endpoints

#### Authentication & User Management
- `POST /auth/login` - User authentication
- `GET /users/profile` - User profile management
- `PUT /users/settings` - User preferences

#### Account Management  
- `GET /accounts` - List all connected accounts ✅
- `POST /accounts` - Add new social media account ✅
- `PUT /accounts/{id}` - Update account settings ✅
- `DELETE /accounts/{id}` - Remove account ✅
- `GET /accounts/{id}/health` - Account health status ✅

#### Action Management & Approval Workflow
- `GET /approvals/pending` - Pending approval requests ✅ **WORKING**
- `POST /approvals/{id}/approve` - Approve pending action ✅
- `POST /approvals/{id}/reject` - Reject pending action ✅
- `POST /actions/execute` - Execute approved action ✅
- `GET /actions/history` - Action history and logs ✅

#### Platform Health & Monitoring
- `GET /platform-health` - Overall platform status ✅ **NEEDS IMPLEMENTATION**
- `GET /health` - API health check ❌ **MISSING**
- `GET /metrics` - System performance metrics ✅

#### Analytics & Reporting
- `GET /analytics/growth/{account_id}` - Growth metrics ✅
- `GET /analytics/performance` - Action performance data ✅
- `GET /analytics/export` - Data export functionality ✅

## 🎨 Frontend Architecture Deep Dive

### Component Structure

#### 1. **Dashboard Component** (components/Dashboard.tsx)
**Purpose**: Main user interface for platform management

**Key Features**:
- Real-time account status monitoring
- Action approval interface
- Performance analytics visualization
- Account management (add/edit/delete)
- Emergency controls and settings

**Current Implementation Status**: ✅ **95% COMPLETE**
- [x] Account listing and management
- [x] Real-time status indicators
- [x] Action approval workflow
- [x] Analytics dashboard
- [x] Responsive design with Tailwind CSS
- [ ] Account creation form validation (needs testing)

#### 2. **Supabase Integration** (lib/supabase.ts)
**Purpose**: Database client and authentication

**Features**:
- Real-time data synchronization
- Secure authentication flows
- Connection testing and health monitoring

**Current Implementation Status**: ✅ **COMPLETE** (recently fixed)
- [x] Connection configuration
- [x] Authentication setup
- [x] Real-time subscriptions
- [x] Error handling and reconnection

#### 3. **Styling & UI Framework**
**Technology Stack**:
- **Tailwind CSS**: Utility-first styling
- **React Components**: Modular UI components
- **TypeScript**: Type safety and developer experience

**Current Implementation Status**: ✅ **COMPLETE**

### State Management

#### Local State (React useState/useEffect)
- Component-level state management
- Real-time data updates from Supabase
- Form handling and validation

#### Global State Strategy
- **Current**: Props drilling for shared state
- **Future**: Context API or Zustand for complex state

### Data Flow Architecture

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│  Dashboard  │───▶│  Supabase   │───▶│  Backend    │
│ Component   │    │   Client    │    │     API     │
└─────────────┘    └─────────────┘    └─────────────┘
       ▲                   ▲                   ▲
       │                   │                   │
       ▼                   ▼                   ▼
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│  Real-time  │    │  Database   │    │  Platform   │
│  Updates    │    │   Tables    │    │  Services   │
└─────────────┘    └─────────────┘    └─────────────┘
```

## 🗄️ Database Design & Schema

### Core Tables

#### **users** - User Account Management
```sql
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    subscription_tier VARCHAR(20) DEFAULT 'free',
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```

#### **social_accounts** - Connected Social Media Accounts
```sql
CREATE TABLE social_accounts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    platform VARCHAR(20) NOT NULL CHECK (platform IN ('tiktok', 'instagram', 'twitter')),
    username VARCHAR(100) NOT NULL,
    access_token TEXT, -- Encrypted
    current_phase VARCHAR(20) DEFAULT 'phase_1',
    health_score DECIMAL(3,2) DEFAULT 1.00,
    is_active BOOLEAN DEFAULT true,
    daily_action_limit INTEGER DEFAULT 50,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```

#### **actions** - Action Log and Approval Queue
```sql
CREATE TABLE actions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    account_id UUID REFERENCES social_accounts(id) ON DELETE CASCADE,
    action_type VARCHAR(50) NOT NULL,
    target_account VARCHAR(100),
    target_data JSONB,
    status VARCHAR(20) DEFAULT 'pending',
    risk_level VARCHAR(10) CHECK (risk_level IN ('green', 'yellow', 'red')),
    requires_approval BOOLEAN DEFAULT false,
    executed_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW(),
    approved_by UUID REFERENCES users(id),
    approval_reason TEXT
);
```

#### **targeting_criteria** - User-Defined Targeting Rules
```sql
CREATE TABLE targeting_criteria (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    account_id UUID REFERENCES social_accounts(id) ON DELETE CASCADE,
    name VARCHAR(100) NOT NULL,
    criteria JSONB NOT NULL, -- Hashtags, keywords, follower counts, etc.
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT NOW()
);
```

#### **health_metrics** - Account Health Monitoring
```sql
CREATE TABLE health_metrics (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    account_id UUID REFERENCES social_accounts(id) ON DELETE CASCADE,
    metric_type VARCHAR(50) NOT NULL,
    metric_value DECIMAL(10,2) NOT NULL,
    recorded_at TIMESTAMP DEFAULT NOW(),
    alert_threshold DECIMAL(10,2),
    INDEX idx_account_metric_time (account_id, metric_type, recorded_at)
);
```

#### **performance_stats** - Growth and Engagement Analytics
```sql
CREATE TABLE performance_stats (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    account_id UUID REFERENCES social_accounts(id) ON DELETE CASCADE,
    date DATE NOT NULL,
    followers_gained INTEGER DEFAULT 0,
    followers_lost INTEGER DEFAULT 0,
    actions_executed INTEGER DEFAULT 0,
    engagement_rate DECIMAL(5,2),
    reach INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(account_id, date)
);
```

### Database Indexes for Performance
```sql
-- Performance optimization indexes
CREATE INDEX idx_social_accounts_user_platform ON social_accounts(user_id, platform);
CREATE INDEX idx_actions_status_created ON actions(status, created_at);
CREATE INDEX idx_actions_account_date ON actions(account_id, created_at DESC);
CREATE INDEX idx_health_metrics_account_time ON health_metrics(account_id, recorded_at);
CREATE INDEX idx_performance_stats_account_date ON performance_stats(account_id, date DESC);
```

## 🔒 Security & Compliance Architecture

### Data Protection
- **Encryption at Rest**: All sensitive data encrypted in PostgreSQL
- **Token Security**: Social media tokens encrypted with AES-256
- **API Security**: JWT authentication with refresh tokens
- **Network Security**: HTTPS enforcement, CORS configuration

### Platform Compliance
- **Rate Limiting**: Respect platform API limits and terms
- **Behavioral Simulation**: Human-like patterns to avoid detection
- **Transparent Operation**: User consent for all automated actions
- **Emergency Controls**: Immediate stop capabilities

### Privacy & GDPR
- **Data Minimization**: Collect only necessary data
- **User Consent**: Explicit consent for data processing
- **Right to Deletion**: Complete data removal capabilities
- **Data Export**: User data portability

## 🚀 Deployment & Infrastructure Strategy

### Development Environment (Current)
- **Local Development**: Docker Compose orchestration
- **Database**: Supabase PostgreSQL (cloud)
- **Caching**: Redis container (local)
- **Services**: All services containerized

### Production Deployment (Planned)

#### Backend Deployment
- **Platform**: Railway.app
- **Configuration**: Environment-based deployment
- **Scaling**: Horizontal scaling based on load
- **Monitoring**: Built-in Railway metrics + custom logging

#### Frontend Deployment  
- **Platform**: Vercel
- **Build**: Automatic deployment from Git
- **CDN**: Global edge distribution
- **Analytics**: Vercel Analytics integration

#### Database & Caching
- **Database**: Supabase PostgreSQL (production)
- **Caching**: Upstash Redis (serverless)
- **Backups**: Automated daily backups
- **Monitoring**: Database performance metrics

### CI/CD Pipeline (To Be Implemented)

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   GitHub    │───▶│   GitHub    │───▶│  Railway/   │
│  Repository │    │   Actions   │    │   Vercel    │
└─────────────┘    └─────────────┘    └─────────────┘
       │                   │                   │
       ▼                   ▼                   ▼
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│    Code     │    │   Tests &   │    │ Production  │
│   Changes   │    │   Build     │    │ Deployment  │
└─────────────┘    └─────────────┘    └─────────────┘
```

#### Planned Pipeline Stages
1. **Code Push**: Trigger on main branch updates
2. **Testing**: Automated unit and integration tests
3. **Build**: Container builds for backend/frontend
4. **Deploy**: Automatic deployment to staging/production
5. **Monitoring**: Health checks and rollback capabilities

## 📊 Performance & Monitoring Strategy

### Backend Performance Targets
- **API Response Time**: < 200ms average
- **Database Query Time**: < 50ms average
- **Concurrent Users**: Support 1,000+ simultaneous users
- **Uptime**: 99.9% availability target

### Frontend Performance Targets
- **First Contentful Paint**: < 1.5s
- **Time to Interactive**: < 3s
- **Bundle Size**: < 1MB total
- **Lighthouse Score**: > 90

### Monitoring Stack

#### Application Monitoring
- **Logging**: Structured JSON logging with log levels
- **Error Tracking**: Comprehensive error capture and alerting
- **Performance Metrics**: API response times, database queries
- **User Analytics**: Feature usage and user behavior

#### Infrastructure Monitoring
- **System Health**: CPU, memory, disk usage
- **Network Monitoring**: Bandwidth, latency, errors
- **Database Performance**: Query performance, connection pooling
- **External Service Health**: AI providers, social platforms

### Alerting Strategy
- **Critical Alerts**: System downtime, data loss, security breaches
- **Warning Alerts**: Performance degradation, high error rates
- **Info Alerts**: Deployment notifications, usage milestones

## 🔄 Development Workflow & Git Strategy

### Branch Strategy
```
main (production) ──┬─── release/v2.1
                    ├─── develop ──┬─── feature/github-sync
                    │              ├─── feature/advanced-analytics  
                    │              └─── bugfix/dashboard-loading
                    └─── hotfix/critical-security-fix
```

### Development Process
1. **Feature Development**: Create feature branch from develop
2. **Testing**: Local testing with Docker Compose
3. **Code Review**: Pull request review process
4. **Integration**: Merge to develop branch
5. **Release**: Create release branch and deploy to staging
6. **Production**: Deploy to production after validation

### Code Quality Standards
- **TypeScript**: Strict type checking enabled
- **ESLint**: Code linting and formatting rules
- **Pytest**: Comprehensive backend testing
- **Jest**: Frontend unit and integration testing
- **Pre-commit Hooks**: Code quality checks before commits

## 🎯 Implementation Priorities & Next Steps

### Immediate Priorities (Next 7 Days)

#### 1. **Frontend Dashboard Completion** 🔥 **HIGH PRIORITY**
- [ ] Fix remaining TypeScript compilation issues
- [ ] Test and validate account creation functionality
- [ ] Verify real-time data updates from Supabase
- [ ] Implement error handling for failed API calls

#### 2. **GitHub Repository Synchronization** 🔥 **HIGH PRIORITY**
- [ ] Initialize GitHub repository with current codebase
- [ ] Set up automated deployment pipeline
- [ ] Configure remote development access
- [ ] Document deployment and development processes

#### 3. **Database Schema Deployment** 📊 **MEDIUM PRIORITY**
- [ ] Deploy complete schema to Supabase production
- [ ] Create initial test data for development
- [ ] Verify all database operations work correctly
- [ ] Set up database backup and recovery procedures

### Short-term Goals (Next 30 Days)

#### 1. **Production Deployment**
- [ ] Deploy backend to Railway with environment configuration
- [ ] Deploy frontend to Vercel with proper domain setup
- [ ] Configure production database and caching
- [ ] Set up monitoring and alerting systems

#### 2. **Feature Completion**
- [ ] Complete account creation and management workflows
- [ ] Implement comprehensive error handling
- [ ] Add advanced analytics and reporting features
- [ ] Complete AI-powered targeting optimization

#### 3. **Testing & Quality Assurance**
- [ ] Implement comprehensive test coverage
- [ ] Perform security audit and penetration testing
- [ ] Load testing and performance optimization
- [ ] User acceptance testing with beta users

### Long-term Roadmap (Next 90 Days)

#### 1. **Advanced Features**
- [ ] Mobile app development (React Native)
- [ ] Advanced AI features and personalization
- [ ] Enterprise features (team accounts, white-label)
- [ ] API documentation and developer portal

#### 2. **Market Expansion**
- [ ] Additional platform integrations (LinkedIn, Pinterest)
- [ ] International market support and localization
- [ ] Partnership and integration ecosystem
- [ ] Enterprise sales and institutional features

## 🛠️ Technology Stack Summary

### Backend Technologies
- **Language**: Python 3.11+
- **Framework**: FastAPI (async/await support)
- **Database**: PostgreSQL 14+ (via Supabase)
- **Caching**: Redis 7+ (via Upstash)
- **AI Providers**: DeepSeek, Groq, OpenAI, Anthropic
- **Containerization**: Docker + Docker Compose
- **Hosting**: Railway.app (planned)

### Frontend Technologies
- **Language**: TypeScript 5+
- **Framework**: Next.js 14+ (React 18+)
- **Styling**: Tailwind CSS 3+
- **Database Client**: Supabase JavaScript SDK
- **State Management**: React hooks (+ Context API)
- **Hosting**: Vercel (planned)

### Development Tools
- **Version Control**: Git + GitHub
- **Code Quality**: ESLint, Prettier, TypeScript strict mode
- **Testing**: Pytest (backend), Jest (frontend)
- **Monitoring**: Custom logging + external monitoring services
- **Documentation**: Markdown + auto-generated API docs

### External Services
- **Database**: Supabase PostgreSQL
- **Caching**: Upstash Redis
- **AI Services**: DeepSeek (primary), multiple fallbacks
- **Social Platforms**: TikTok, Instagram, Twitter APIs
- **Proxy Services**: IPRoyal, SmartProxy, BrightData (future)

---

**Document Version**: 1.0  
**Last Updated**: December 26, 2024  
**Next Review**: January 15, 2025  
**Document Owner**: Technical Architecture Team  
**Status**: Active - Implementation in Progress
