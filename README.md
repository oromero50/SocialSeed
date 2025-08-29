# SocialSeed v2.0 🌱

**Enterprise-grade social media orchestration with phased safety approach**

SocialSeed is a comprehensive platform for managing and growing multiple social media accounts with AI-powered automation, safety monitoring, and analytics.

## ✨ Features

- 🎯 **Multi-Platform Support** - TikTok, Instagram, Twitter integration
- 🤖 **AI-Powered Automation** - LLM-driven content and engagement strategies  
- 📊 **Advanced Analytics** - Historical data tracking and growth insights
- 🔒 **OAuth Authentication** - Secure platform login flows
- 🛡️ **Safety-First Approach** - Phased deployment with health monitoring
- 📱 **Modern UI** - Clean, responsive dashboard interface

## 🚀 Quick Start

### Prerequisites

- Node.js 18+ 
- Python 3.9+
- Docker & Docker Compose
- TikTok Developer Account (for OAuth)

### Local Development

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/socialseed.git
   cd socialseed
   ```

2. **Environment Setup**
   ```bash
   cp .env.example .env
   # Fill in your API keys and database credentials
   ```

3. **Start with Docker**
   ```bash
   docker-compose up --build
   ```

4. **Access the application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Docs: http://localhost:8000/docs

### Manual Setup

#### Frontend
```bash
cd frontend
npm install
npm run dev
```

#### Backend
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## 🏗️ Architecture

```
SocialSeed/
├── frontend/          # Next.js React application
│   ├── components/    # Reusable UI components
│   ├── pages/        # Next.js pages and API routes
│   └── lib/          # Utilities and configurations
├── backend/          # FastAPI Python application  
│   ├── services/     # Business logic services
│   ├── migrations/   # Database migrations
│   └── main.py       # Application entry point
└── docker-compose.yml # Development environment
```

## 🔧 Configuration

### Environment Variables

**Frontend (.env.local)**
```bash
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_SUPABASE_URL=your_supabase_url
NEXT_PUBLIC_SUPABASE_ANON_KEY=your_supabase_key
```

**Backend (.env)**
```bash
# Database
DATABASE_URL=postgresql://user:pass@localhost:5432/socialseed
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_service_key

# TikTok OAuth
TIKTOK_CLIENT_ID=your_tiktok_client_id
TIKTOK_CLIENT_SECRET=your_tiktok_client_secret
TIKTOK_REDIRECT_URI=https://yourdomain.com/tiktok-callback

# Development
USE_MOCK_TIKTOK_OAUTH=true  # Set to false for production
```

## 🌐 Deployment

### Frontend (Vercel)
1. Connect your GitHub repository to Vercel
2. Set environment variables in Vercel dashboard
3. Deploy automatically on push to main branch

### Backend (Railway/Render)
1. Connect your GitHub repository 
2. Configure Docker deployment
3. Set production environment variables
4. Update frontend API_URL to point to backend

## 📱 Platform Integration

### TikTok Developer Setup
1. Apply at [developers.tiktok.com](https://developers.tiktok.com)
2. Create your app and get OAuth credentials
3. Configure redirect URIs for your domain
4. Add Login Kit and TikTok API products

### Development vs Production
- **Development**: Uses mock OAuth for testing
- **Production**: Requires real TikTok Developer credentials

## 🛠️ API Documentation

Interactive API documentation is available at:
- Development: http://localhost:8000/docs
- Production: https://your-backend-url.com/docs

### Key Endpoints

- `GET /tiktok/auth/login` - Initialize OAuth flow
- `GET /tiktok/auth/callback` - Handle OAuth callback  
- `POST /tiktok/auth/refresh` - Refresh access tokens
- `GET /analytics/{platform}/{username}` - Get account analytics

## 🔒 Security

- OAuth 2.0 with PKCE for secure authentication
- Environment-based configuration management
- Rate limiting and request validation
- CORS configuration for cross-origin requests

## 📊 Analytics & Monitoring

- Historical follower growth tracking
- Engagement rate analytics
- Account health monitoring
- Automated safety alerts

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- 📧 Email: support@socialseed.app
- 📖 Documentation: [docs.socialseed.app](https://docs.socialseed.app)
- 🐛 Issues: [GitHub Issues](https://github.com/yourusername/socialseed/issues)

---

**Built with ❤️ for the social media management community**