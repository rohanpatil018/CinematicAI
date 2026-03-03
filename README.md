<p align="center">
  <h1 align="center">🎬 CineMatch AI</h1>
  <p align="center">
    <strong>AI-Powered Movie Intelligence SaaS Platform</strong>
  </p>
  <p align="center">
    Discover movies that actually match your soul — with hybrid AI recommendations, real-time streaming availability, and a cinematic DNA profile unique to you.
  </p>
  <p align="center">
    <a href="#features"><img src="https://img.shields.io/badge/Features-8-gold?style=for-the-badge" alt="Features" /></a>
    <a href="#tech-stack"><img src="https://img.shields.io/badge/Stack-React%20%2B%20FastAPI-blue?style=for-the-badge" alt="Stack" /></a>
    <a href="#license"><img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" alt="License" /></a>
    <a href="#"><img src="https://img.shields.io/badge/Version-1.0.0-orange?style=for-the-badge" alt="Version" /></a>
  </p>
</p>

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Architecture](#architecture)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Backend Setup](#backend-setup)
  - [Frontend Setup](#frontend-setup)
  - [Docker Setup](#docker-setup)
- [Environment Variables](#environment-variables)
- [API Reference](#api-reference)
- [Project Structure](#project-structure)
- [Recommendation Engine](#recommendation-engine)
- [Screenshots](#screenshots)
- [Contributing](#contributing)
- [License](#license)

---

## Overview

**CineMatch AI** is a full-stack movie intelligence platform that combines advanced machine learning with an elegant, cinema-themed UI to deliver hyper-personalized movie recommendations. Unlike traditional recommendation systems, CineMatch uses a **hybrid scoring engine** that blends content-based filtering (TF-IDF), collaborative filtering, and semantic vector search (FAISS) — all enhanced by a context-aware **Vibe Engine** that adapts to your mood, time of day, and preferences.

Whether you're looking for a hidden gem for a solo night, the perfect group movie with friends, or just want to understand your cinematic taste on a deeper level, CineMatch has you covered.

---

## Features

| Feature | Description |
|---|---|
| 🤖 **Hybrid AI Recommendations** | Multi-signal scoring: `0.4 × Content + 0.4 × Collaborative + 0.2 × Preference`, boosted by mood and context |
| 🌊 **Vibe Engine** | Context-aware suggestions based on mood (chill, thrilled, romantic, etc.) with genre weight multipliers |
| 🔍 **Semantic Search** | Natural language movie search powered by FAISS + Sentence Transformers (`all-MiniLM-L6-v2`) |
| 🧬 **Cinematic DNA Profile** | Unique taste fingerprint with radar charts, taste evolution tracking, and archetype classification |
| 💎 **Hidden Gems Detector** | Surfaces critically-loved films with low popularity using a weighted `HGS` formula |
| 👥 **Watch Together** | Group compatibility scoring with shared favorites, compromise picks, and alternating suggestions |
| 📺 **Live Streaming Availability** | Real-time platform availability via TMDB API across Netflix, Prime, Disney+, Hotstar, and more |
| 🛡️ **Admin Dashboard** | Platform analytics, user management, and API usage monitoring |

---

## Tech Stack

### Frontend — `cinematch-ai/`

| Technology | Purpose |
|---|---|
| **React 18** | UI framework with functional components and hooks |
| **TypeScript** | Type-safe development |
| **Vite** | Lightning-fast build tool and dev server |
| **Tailwind CSS 3** | Utility-first styling with custom cinema-gold design tokens |
| **shadcn/ui** | Radix-based accessible component library |
| **TanStack Query** | Server state management and data fetching |
| **React Router v6** | Client-side routing with nested layouts |
| **Recharts** | Data visualization for DNA profiles and analytics |
| **Lucide React** | Modern icon library |
| **Vitest** | Unit testing framework |

### Backend — `cinematch-backend/`

| Technology | Purpose |
|---|---|
| **FastAPI** | High-performance async Python API framework |
| **SQLAlchemy 2.0** | Async ORM with PostgreSQL/SQLite support |
| **PostgreSQL 16** | Primary production database |
| **Redis 7** | Caching layer with configurable TTLs |
| **FAISS** | Facebook's vector similarity search for semantic queries |
| **Sentence Transformers** | Text embeddings via `all-MiniLM-L6-v2` model |
| **scikit-learn** | TF-IDF vectorization and cosine similarity |
| **Pydantic v2** | Data validation and serialization |
| **APScheduler** | Background task scheduling |
| **SlowAPI** | Rate limiting middleware |
| **Docker** | Containerized deployment |

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        FRONTEND (React + Vite)                  │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌───────────────────┐  │
│  │ Landing  │ │Dashboard │ │ Discover │ │  DNA Profile      │  │
│  └──────────┘ └──────────┘ └──────────┘ └───────────────────┘  │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌───────────────────┐  │
│  │ Results  │ │Hidden    │ │ Watch    │ │  Admin Dashboard  │  │
│  │          │ │Gems      │ │ Together │ │                   │  │
│  └──────────┘ └──────────┘ └──────────┘ └───────────────────┘  │
└────────────────────────────┬────────────────────────────────────┘
                             │ HTTP / REST
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    BACKEND (FastAPI)                             │
│                                                                 │
│  ┌─── Routers ──────────────────────────────────────────────┐   │
│  │  auth │ users │ movies │ recommendations │ social │ admin│   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                 │
│  ┌─── Services (Business Logic) ────────────────────────────┐   │
│  │  RecommendationEngine  │  SemanticSearchService          │   │
│  │  DNAService            │  HiddenGemService               │   │
│  │  CompatibilityService  │  StreamingService               │   │
│  │  CacheService          │                                 │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                 │
│  ┌─── Middleware ───────────────────────────────────────────┐   │
│  │  CORS  │  Rate Limiting  │  Request Counter  │  Auth    │   │
│  └──────────────────────────────────────────────────────────┘   │
└────────┬──────────────┬──────────────┬──────────────────────────┘
         │              │              │
         ▼              ▼              ▼
   ┌──────────┐  ┌──────────┐  ┌──────────────┐
   │PostgreSQL│  │  Redis   │  │ FAISS Index  │
   │  (Data)  │  │ (Cache)  │  │  (Vectors)   │
   └──────────┘  └──────────┘  └──────────────┘
```

---

## Getting Started

### Prerequisites

- **Node.js** ≥ 18.x and **npm** ≥ 9.x
- **Python** ≥ 3.12
- **PostgreSQL** 16+ (or SQLite for development)
- **Redis** 7+ (optional, gracefully degrades)
- **Docker** & **Docker Compose** (optional, for containerized setup)

### Backend Setup

```bash
# 1. Navigate to backend directory
cd cinematch-backend

# 2. Create and activate virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS/Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set up environment variables
cp .env.example .env
# Edit .env with your TMDB API key and database credentials

# 5. Run the development server
uvicorn app.main:app --reload --port 8000
```

The API will be available at `http://localhost:8000` with interactive docs at `http://localhost:8000/docs`.

### Frontend Setup

```bash
# 1. Navigate to frontend directory
cd cinematch-ai

# 2. Install dependencies
npm install

# 3. Start the development server
npm run dev
```

The app will be available at `http://localhost:5173`.

### Docker Setup

For a fully containerized environment with PostgreSQL and Redis:

```bash
cd cinematch-backend

# Build and start all services
docker-compose up --build
```

This starts four services:

| Service | Port | Description |
|---|---|---|
| `cinematch-api` | `8000` | FastAPI application (4 workers) |
| `cinematch-worker` | — | Background streaming alert worker |
| `cinematch-postgres` | `5432` | PostgreSQL 16 Alpine |
| `cinematch-redis` | `6379` | Redis 7 Alpine |

---

## Environment Variables

Create a `.env` file in `cinematch-backend/` based on `.env.example`:

| Variable | Description | Default |
|---|---|---|
| `DATABASE_URL` | PostgreSQL async connection string | `postgresql+asyncpg://...` |
| `REDIS_URL` | Redis connection string | `redis://localhost:6379/0` |
| `JWT_SECRET_KEY` | Secret for JWT token generation | *(change in production)* |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | JWT access token lifetime | `30` |
| `REFRESH_TOKEN_EXPIRE_DAYS` | JWT refresh token lifetime | `7` |
| `TMDB_API_KEY` | [TMDB API](https://www.themoviedb.org/settings/api) key for streaming data | *(required)* |
| `EMBEDDING_MODEL` | Sentence transformer model name | `all-MiniLM-L6-v2` |
| `FAISS_INDEX_PATH` | Path to FAISS vector index | `./data/faiss_index.bin` |
| `RATE_LIMIT_PER_MINUTE` | API rate limit per user | `60` |
| `CORS_ORIGINS` | Allowed frontend origins (JSON array) | `["http://localhost:5173"]` |

---

## API Reference

All API endpoints are prefixed with `/api/v1`. Interactive documentation is available at `/docs` (Swagger UI) and `/redoc` when `DEBUG=true`.

### Authentication

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/auth/register` | Create a new user account |
| `POST` | `/auth/login` | Obtain JWT access + refresh tokens |
| `POST` | `/auth/refresh` | Refresh an expired access token |

### Movies & Recommendations

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/movies/` | List movies with filtering and pagination |
| `GET` | `/movies/{id}` | Get movie details with streaming availability |
| `GET` | `/movies/search` | Search movies by title or natural language |
| `POST` | `/recommendations/` | Get AI recommendations (mood, context-aware) |
| `GET` | `/recommendations/hidden-gems` | Discover hidden gems |

### User Profile & Social

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/users/me` | Get current user profile |
| `PUT` | `/users/me` | Update user preferences |
| `GET` | `/users/me/dna` | Get cinematic DNA profile |
| `POST` | `/social/compatibility` | Calculate watch-together compatibility |

### Admin

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/admin/stats` | Platform analytics and stats |
| `GET` | `/admin/users` | User management |

### Health

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/health` | Health check for Docker and load balancers |

---

## Project Structure

```
Movie-Engine/
├── cinematch-ai/                   # Frontend (React + TypeScript)
│   ├── public/                     # Static assets
│   ├── src/
│   │   ├── assets/                 # Images and media
│   │   ├── components/
│   │   │   ├── layout/             # AppLayout, Sidebar
│   │   │   ├── ui/                 # shadcn/ui components (49 components)
│   │   │   ├── MovieCard.tsx       # Movie card with match badge
│   │   │   ├── MoodSelector.tsx    # Vibe engine mood selector
│   │   │   ├── DashboardLayout.tsx # Dashboard layout wrapper
│   │   │   └── NavLink.tsx         # Navigation link component
│   │   ├── hooks/                  # Custom React hooks
│   │   ├── lib/                    # Utility functions
│   │   ├── pages/
│   │   │   ├── Landing.tsx         # Marketing landing page
│   │   │   ├── Login.tsx           # Authentication
│   │   │   ├── Signup.tsx          # Registration
│   │   │   ├── Dashboard.tsx       # Main dashboard
│   │   │   ├── DashboardHome.tsx   # Dashboard home view
│   │   │   ├── Discover.tsx        # Movie discovery
│   │   │   ├── Results.tsx         # Recommendation results
│   │   │   ├── DNAProfile.tsx      # Cinematic DNA page
│   │   │   ├── HiddenGems.tsx      # Hidden gems explorer
│   │   │   ├── WatchTogether.tsx   # Group watch mode
│   │   │   └── AdminDashboard.tsx  # Admin analytics
│   │   ├── test/                   # Test files
│   │   ├── App.tsx                 # Root component + routing
│   │   ├── main.tsx                # Entry point
│   │   └── index.css               # Tailwind + design tokens
│   ├── tailwind.config.ts          # Tailwind configuration
│   ├── vite.config.ts              # Vite configuration
│   └── package.json
│
├── cinematch-backend/              # Backend (FastAPI + Python)
│   ├── app/
│   │   ├── core/
│   │   │   ├── config.py           # Pydantic settings
│   │   │   ├── database.py         # SQLAlchemy async engine
│   │   │   ├── security.py         # JWT + password hashing
│   │   │   └── rate_limit.py       # SlowAPI rate limiter
│   │   ├── models/
│   │   │   ├── user.py             # User model
│   │   │   ├── movie.py            # Movie model
│   │   │   ├── rating.py           # Rating model
│   │   │   ├── subscription.py     # Subscription tiers
│   │   │   └── streaming_alert.py  # Streaming alerts
│   │   ├── routers/
│   │   │   ├── auth.py             # Auth endpoints
│   │   │   ├── users.py            # User endpoints
│   │   │   ├── movies.py           # Movie endpoints
│   │   │   ├── recommendations.py  # Recommendation endpoints
│   │   │   ├── social.py           # Social/compatibility endpoints
│   │   │   └── admin.py            # Admin endpoints
│   │   ├── schemas/
│   │   │   ├── auth.py             # Auth request/response models
│   │   │   ├── user.py             # User schemas
│   │   │   ├── recommendation.py   # Recommendation schemas
│   │   │   ├── dna.py              # DNA profile schemas
│   │   │   └── streaming.py        # Streaming schemas
│   │   ├── services/
│   │   │   ├── recommendation_engine.py  # Hybrid AI engine
│   │   │   ├── semantic_search.py        # FAISS + embeddings
│   │   │   ├── dna_service.py            # Cinematic DNA builder
│   │   │   ├── hidden_gem_service.py     # Hidden gem scorer
│   │   │   ├── compatibility_service.py  # Watch-together logic
│   │   │   ├── streaming_service.py      # TMDB streaming data
│   │   │   └── cache_service.py          # Redis cache wrapper
│   │   ├── background/
│   │   │   ├── scheduler.py              # APScheduler jobs
│   │   │   └── streaming_alert_worker.py # Streaming alert worker
│   │   └── main.py                 # FastAPI app + lifespan
│   ├── data/                       # ML model data (FAISS index, TF-IDF)
│   ├── Dockerfile                  # Production container
│   ├── docker-compose.yml          # Multi-service orchestration
│   ├── requirements.txt            # Python dependencies
│   └── .env.example                # Environment template
│
└── docs/
    └── screenshots/                # Application screenshots
```

---

## Recommendation Engine

CineMatch's recommendation engine uses a **hybrid scoring approach** that combines three signals:

### Scoring Formula

```
final_score = (0.4 × content_score) + (0.4 × collab_score) + (0.2 × preference_score)
```

After computing the base score, two contextual multipliers are applied:

- **Mood Boost** — Multiplies genre weights based on mood (e.g., `chill → Comedy ×1.3, Animation ×1.2`)
- **Context Boost** — Keyword-to-genre mapping (e.g., `"space" → Sci-Fi`, `"dark" → Thriller, Crime, Horror`)

### Signal Breakdown

| Signal | Weight | Method |
|---|---|---|
| **Content-Based** | 40% | TF-IDF cosine similarity between movie metadata |
| **Collaborative** | 40% | User-based filtering from ratings of similar users |
| **Preference** | 20% | Learned genre + director preferences from user history |

### Hidden Gem Score (HGS)

```
HGS = (imdb_rating × 0.35) + (rt_score × 0.25) + (content_sim × 0.25) - (popularity × 0.15)
```

Only surfaces movies with `vote_count < 100,000` and `rating > 7.5`.

---

## Screenshots

> *Screenshots will be added here as the application evolves. Place them in `docs/screenshots/`.*

---

## Contributing

Contributions are welcome! Here's how to get started:

1. **Fork** the repository
2. **Create a feature branch** — `git checkout -b feature/amazing-feature`
3. **Commit your changes** — `git commit -m "Add amazing feature"`
4. **Push to the branch** — `git push origin feature/amazing-feature`
5. **Open a Pull Request**

### Development Guidelines

- Follow existing code patterns and naming conventions
- Write tests for new features (Vitest for frontend, pytest for backend)
- Use conventional commit messages
- Ensure ESLint passes for frontend changes
- Add type hints for all Python functions

---

## License

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for details.

---

<p align="center">
  <strong>Built with ❤️ and AI</strong>
  <br />
  <sub>Stop scrolling. Start watching.</sub>
</p>
