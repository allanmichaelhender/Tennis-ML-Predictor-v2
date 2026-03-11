# 🎾 Vantage Point: AI-Powered Tennis Analytics

**Vantage Point** is a platform that uses AI to predict outcomes in professional tennis. By combining **PyTorch Neural Networks** and **XGBoost** models, the system processes historical ATP/WTA data to generate real-time win probabilities and identify value against live bookmaker odds.

## 🚀 Key Features
- **Hybrid ML Inference**: Combines PyTorch and XGBoost models for accurate probability forecasting.
- **Automated Data Pipeline**: Real-time fixture syncing and market data ingestion.
- **Production-Grade Infrastructure**: Uses Docker Compose for containerized deployment, Nginx for reverse proxy, and SSL/TLS security.
- **Real-Time Dashboard**: A React UI with dynamic polling hooks and interactive Recharts data visualizations.

## 🛠️ Tech Stack

### Backend & AI
- **Framework**: FastAPI (Asynchronous Python 3.11+)
- **ML/DL**: PyTorch, XGBoost, scikit-learn, Pandas, NumPy
- **Database**: PostgreSQL with **SQLAlchemy** (ORM) and **Alembic** (Migrations)
- **Async Driver**: **Asyncpg** for non-blocking database I/O
- **Production Server**: Gunicorn with Uvicorn workers

### Frontend
- **Framework**: React 18, Vite, TypeScript
- **Styling**: Tailwind CSS
- **Visualisation**: Recharts (Model Calibration & Equity tracking)

### DevOps & Cloud
- **Infrastructure**: Google Cloud Platform (GCP) Compute Engine
- **Orchestration**: Docker & Docker Compose
- **Proxy/Web Server**: Nginx
- **Security**: Certbot (Let's Encrypt SSL/TLS)

## 🏗️ Architecture
Vantage Point uses a decoupled, containerized architecture:
1.  **`tennis_api`**: A FastAPI service for ML inference and data orchestration.
2.  **`tennis_db`**: A PostgreSQL 16 instance with persistent data volumes.
3.  **`tennis_proxy`**: Nginx acts as a reverse proxy and static asset host.
4.  **`tennis_pgadmin`**: A secure database management interface.

## 🔧 Getting Started

### Prerequisites
- Docker & Docker Compose
- Python 3.10+
- Google Gemini API Key

### Installation & Setup
1.  **Clone the Repository**:
    ```bash
    git clone https://github.com
    cd Vantage-Point-ML
    ```

2.  **Configure Environment**: Create a `.env` file in the root.
    ```env
    DATABASE_URL=postgresql+asyncpg://postgres:password@db:5432/tennis_db
    GEMINI_API_KEY=your_key_here
    THE_ODDS_API_KEY=your_key_here
    ```

3.  **Deploy with Docker**:
    ```bash
    docker-compose up -d --build
    ```

4.  **Initialize Database**:
    ```bash
    docker-compose exec tennis_api alembic upgrade head
    docker-compose exec tennis_api python app/services/data/master_sync.py
    ```

## 📊 Model Performance
The current **XGBoost + PyTorch NN** model is trained on a curated dataset of over 50,000 matches, focusing on surface-specific Elo ratings and rolling performance metrics (Serve/Return/Break Point conversion).

```
/Backend
├── app/
│   ├── main.py                 # FastAPI entry point & routes
│   ├── api/                    # Api logic
│   │   ├── deps.py             # API key and get database logic
│   │   ├── Endpoints/          # Endpoints directory
│   ├── core/                   # Core logic, e.g. ratelimit setup
│   ├── database/               # Database connection layer
│   │   └── session.py          # Async engine
│   ├── models/                 # SQLAlchemy ORM Models
│   ├── schemas/                # Pydantic Data Validation Schemas
│   ├── tml-data/               # Raw JSON/CSV files with historic match and odds data
│   ├── sevices/                # Collating all ML, LLM, Ingestion, etc. files
│   │   ├── data/               # Data ingestion and LLM logic
│   │   ├── ml/                 # ML files - feature engine and inference
│   │   └── quant/              # Code for running and quantifying model results
├── migrations/                 # Alembic auto-generated migration scripts
├── alembic.ini                 # Alembic configuration 
├── docker-compose.yml          # Infrastructure orchestration (DB, API, pgAdmin, etc.)
├── Dockerfile                  # API container recipe
├── requirements.txt            # Python dependencies 
└── .env                        # Environment variables 

/Frontend
src/
├── components/        # Reusable UI
│   ├── lab/           # Specific to the Lab (EquityChart, StatCards)
│   └── dashboard/     # Specific to Dashboard (MatchCard, PredictModal)
├── hooks/             # Custom React hooks (usePerformance, useLiveMatches)
├── pages/             # Route views (LabPage, DashboardPage)
├── services/          # API logic (api.ts / Axios setup)
├── types/             # TS interfaces
├── utils/             # Math/Formatting helpers
├── App.tsx            # Main router
└── main.tsx           # Entry point

```