# 🚀 TradeSense AI

**TradeSense AI** is a production-grade, real-time trading analytics platform that leverages modern web technologies, microservices architecture, and Artificial Intelligence to provide actionable market insights.

![Dashboard Preview](https://via.placeholder.com/800x400?text=TradeSense+AI+Dashboard)

---

## 🌟 Key Features

### 1. Real-Time Market Data ⚡

- **Live Feed**: Real-time trade ingestion and broadcasting via WebSockets.
- **Crypto Integration**: Seamless integration with **CoinGecko API** for live cryptocurrency prices and metadata.
- **Low Latency**: Optimized Redis Pub/Sub architecture for instant data delivery to the frontend.

### 2. AI-Powered Insights 🧠

- **LLM Integration**: Utilizes Large Language Models (OpenAI/Gemini) to generate daily market summaries and sentiment analysis.
- **RAG Pipeline**: Retrieval-Augmented Generation to ground AI insights in actual trade data.
- **Smart Summaries**: Automated generation of "Day in Review" summaries for tracked assets.

### 3. Advanced Analytics 📊

- **Historical Querying**: Efficient retrieval of historical trade data using MongoDB and PostgreSQL.
- **Visualizations**: Interactive charts and metric cards for price trends, volume, and volatility.
- **Technical Indicators**: (Planned) RSI, MACD, and Moving Averages.

### 4. Modern User Interface 🎨

- **Glassmorphism Design**: Premium, dark-themed UI with modern aesthetics.
- **Responsive**: Fully responsive layout for desktop, tablet, and mobile.
- **Interactive**: Dynamic components with animations and real-time state updates.

---

## 🏗️ Technology Stack

### Frontend

- **Framework**: React 18 + TypeScript + Vite
- **Styling**: Vanilla CSS (CSS Variables, Flexbox/Grid)
- **State Management**: React Hooks
- **Communication**: Axios (REST), Native WebSockets
- **Containerization**: Nginx (Alpine)

### Backend

- **API Gateway**: FastAPI (Python 3.10+)
- **Task Queue**: Celery + RabbitMQ
- **Real-time**: Redis Pub/Sub
- **Database**:
  - **MongoDB**: Document store for trade logs and unstructured data.
  - **PostgreSQL**: Relational store for user data and structured records.
  - **Redis**: Caching and message broker.
- **AI/ML**: OpenAI API / Google Gemini, LangChain (planned).

### Infrastructure

- **Docker**: Full containerization of all services.
- **Docker Compose**: Orchestration for local development.
- **CI/CD**: (Planned) GitHub Actions for automated testing and deployment.

---

## 📂 Project Structure

```
tradesense-ai/
├── frontend/                 # React + TypeScript Frontend
│   ├── src/
│   │   ├── components/       # Reusable UI components (Navbar, Cards)
│   │   ├── pages/            # Main route pages (Dashboard, Analytics, Insights)
│   │   ├── services/         # API clients and WebSocket logic
│   │   └── ...
│   ├── Dockerfile            # Frontend production build
│   └── ...
├── services/
│   ├── api/                  # FastAPI Backend Service
│   │   ├── app/
│   │   │   ├── routes/       # API Endpoints (ingest, query, market, insights)
│   │   │   ├── models/       # Pydantic & DB Models
│   │   │   ├── core/         # Config & DB connections
│   │   │   └── integrations/ # External APIs (CoinGecko, etc.)
│   │   └── ...
│   ├── worker/               # Celery Worker Service
│   │   ├── tasks.py          # Background tasks (LLM generation, data sync)
│   │   └── ...
│   └── ml/                   # (Planned) Machine Learning Service
├── docker-compose.yml        # Service orchestration
└── .vscode/                  # VS Code debug configurations
```

---

## 🚀 Getting Started

### Prerequisites

- Docker & Docker Compose
- Node.js 18+ (for local frontend dev)
- Python 3.10+ (for local backend dev)

### Quick Start (Docker)

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/yourusername/tradesense-ai.git
    cd tradesense-ai
    ```

2.  **Start all services:**

    ```bash
    docker-compose up -d --build
    ```

3.  **Access the application:**
    - **Frontend**: [http://localhost:3000](http://localhost:3000)
    - **API Docs**: [http://localhost:8000/docs](http://localhost:8000/docs)
    - **Flower (Celery Monitor)**: [http://localhost:5556](http://localhost:5556)

### Local Debugging (VS Code)

A `.vscode/launch.json` is provided for debugging.

1.  **Start Infrastructure**: Run databases and queues via Docker:
    ```bash
    docker-compose up -d mongo postgres redis rabbitmq
    ```
2.  **Backend**: Select **"Python: FastAPI"** in VS Code Debug tab and hit F5.
3.  **Frontend**: Run `npm run dev` in `frontend/` directory, then select **"Chrome: Frontend"** in VS Code Debug tab.

---

## 🗺️ Roadmap & Remaining Tasks

We are building towards a comprehensive AI trading platform. Here is what's left to do:

### Phase 1: Foundation (✅ Completed)

- [x] Basic microservices architecture (API, Worker, DBs).
- [x] Real-time data ingestion pipeline.
- [x] Modern React Frontend with Dashboard.
- [x] Basic LLM integration for summaries.

### Phase 2: Market Data & Intelligence (🚧 In Progress)

- [x] CoinGecko API Integration (Free Tier).
- [ ] **Alpha Vantage Integration**: Add stock market data support.
- [ ] **Data Caching**: Implement Redis caching for external API calls to respect rate limits.
- [ ] **Background Sync**: Create periodic tasks to keep market data fresh.

### Phase 3: AI & Predictions (📅 Next)

- [ ] **Price Prediction Model**: Train an LSTM model on historical data to predict next-day closing prices.
- [ ] **MCP Server**: Implement a **Model Context Protocol** server to allow external LLMs (like Claude Desktop) to interact with TradeSense data directly.
- [ ] **Sentiment Analysis**: Analyze news headlines to gauge market sentiment.

### Phase 4: Production Readiness

- [ ] **Authentication**: Add User Auth (OAuth2/JWT) to save personalized watchlists.
- [ ] **Deployment**: Terraform scripts for AWS deployment (ECS/Fargate).
- [ ] **Testing**: Comprehensive unit and integration tests (Pytest + Jest).

---

## 🤝 Contributing

Contributions are welcome! Please fork the repository and submit a Pull Request.

## 📄 License

MIT License
