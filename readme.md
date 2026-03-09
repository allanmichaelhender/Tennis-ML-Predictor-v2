/tennis-predictor-v2
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI entry point & routes
│   ├── database/               # Database connection layer
│   │   ├── __init__.py
│   │   └── session.py          # Async engine & get_db dependency
│   ├── models/                 # SQLAlchemy 2.0 ORM Models
│   │   ├── __init__.py         # Exports Base, Player, Match for Alembic
│   │   ├── base.py             # Shared DeclarativeBase
│   │   ├── player.py           # Players table definition
│   │   └── match.py            # Matches table definition
│   ├── schemas/                # Pydantic v2 Data Validation
│   │   ├── __init__.py
│   │   ├── player.py           # Player validation & API response shapes
│   │   └── match.py            # Match validation & API response shapes
│   ├── ml/                     # Machine Learning Logic
│   │   ├── __init__.py
│   │   ├── encoder.py          # PyTorch LSTM (Player Form)
│   │   ├── predictor.py        # XGBoost (Final Classification)
│   │   └── validator.py        # Time-Aware Validation logic
│   └── services/               # Business Logic & ETL
│       ├── __init__.py
│       └── ingestion.py        # TML JSON-to-SQL Ingestion Service
├── migrations/                 # Alembic auto-generated migration scripts
├── tml-data/                   # Raw JSON/CSV files (Local storage)
├── alembic.ini                 # Alembic configuration (Async-enabled)
├── docker-compose.yml          # Infrastructure orchestration (DB, API, pgAdmin)
├── Dockerfile                  # API container recipe
├── requirements.txt            # Python dependencies (2026 Power Stack)
└── .env                        # Environment variables (DB_URL, API_KEYS)


src/
├── assets/            # Global CSS (index.css), logos, fonts
├── components/        # Reusable UI "Lego bricks"
│   ├── ui/            # Shadcn/UI primitives (Buttons, Cards, Inputs)
│   ├── lab/           # Specific to the Lab (EquityChart, StatCards)
│   └── dashboard/     # Specific to Live Feed (MatchRow, OddsDisplay)
├── hooks/             # Custom React hooks (useLabData, useLiveMatches)
├── layouts/           # Page shells (Sidebar, Navbar, MainLayout)
├── pages/             # Your actual route views (LabPage, DashboardPage)
├── services/          # API logic (api.ts - our Axios setup)
├── types/             # TS interfaces (lab.ts, dashboard.ts)
├── utils/             # Math/Formatting helpers (formatCurrency, calculateROI)
├── App.tsx            # Main router and app shell
└── main.tsx           # Entry point (the ReactDOM.render)