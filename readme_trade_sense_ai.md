# TradeSense AI

**Production-ready, real-time trading insight platform** — an end-to-end system combining streaming data ingestion, asynchronous processing, RAG-powered LLM analysis, and cloud-native deployment on AWS. This repository is designed to demonstrate advanced backend engineering, DevOps, and LLM integration skills.

---

## 🚀 Project Overview

TradeSense AI captures live market data, computes analytics, and generates human-readable trade opportunities and summaries using Retrieval-Augmented Generation (RAG) with LLMs. The system is event-driven, scalable, and hardened for production use.

Primary goals:

- Build a production-grade system that can be hosted on AWS (free-tier conscious)
- Showcase skills: FastAPI, Django (admin), MongoDB, Postgres (RDS), Redis, Celery, RabbitMQ, AWS (EC2, Lambda, API Gateway, S3), Kubernetes, ArgoCD, Jenkins, encryption, and LLM/RAG
- Maintain weekly public progress updates for portfolio and LinkedIn
- Learn deeply by implementing, deploying, and monitoring each component

---

## 🧩 Key Features

- Live market data ingestion (WebSocket / REST polling)
- Real-time analytics and alerting (Celery workers)
- LLM + RAG for AI-driven trade summaries and Q&A
- Secure storage (AES-256) for sensitive data
- CI/CD pipeline (Jenkins + ArgoCD) and GitOps deployment
- Monitoring (CloudWatch / Prometheus + Grafana) and logs
- Dev/prod parity with Docker, minikube/kind (local), and AWS deployment

---

## 📦 Tech Stack

**Backend:** FastAPI (microservices), Django (admin)

**Datastores:** MongoDB (document + vector), PostgreSQL (RDS), Redis (cache / vector), S3-compatible storage

**Messaging & Workers:** RabbitMQ (broker), Celery (tasks)

**AI / LLM:** Ollama (local) or Gemini/OpenAI (cloud), FAISS/Chroma/Redis-Vector for embeddings

**Infra & DevOps:** Docker, Kubernetes (minikube/kind or EKS), ArgoCD, Jenkins, Terraform (optional), LocalStack (for offline AWS emulation)

**Security:** JWT, AES-256 encryption, AWS KMS (optional)

**Monitoring:** Prometheus, Grafana, CloudWatch

---

## 📁 Repository Structure (Suggested)

```
tradesense-ai/
├── infra/                  # Terraform / ArgoCD manifests / Kubernetes charts
├── services/
│   ├── api/                # FastAPI service: ingestion, query endpoints
│   ├── analytics/          # Celery tasks, aggregations
│   ├── ai-insight/         # RAG + LLM orchestration (can be a Lambda-compatible service)
│   ├── admin/              # Django admin dashboard
│   └── alerting/           # Notification microservice (email/Slack)
├── docs/                   # Architecture diagrams, runbooks, designs
├── docker-compose.yml
├── k8s/                    # Kubernetes manifests for minikube / EKS
├── Jenkinsfile
├── README.md
└── scripts/                # helper scripts (db init, data loaders)
```

---

## 🔧 Quickstart — Local Development (Phase 1)

> Goal: Run the core services locally with Docker Compose: FastAPI, MongoDB, PostgreSQL, RabbitMQ, Redis, Celery worker.

1. Clone repository:

```bash
git clone https://github.com/<your-user>/tradesense-ai.git
cd tradesense-ai
```

2. Copy env template and adjust values:

```bash
cp .env.example .env
# edit .env to set SERVICE_PORTS, DB creds, LLM settings, JWT secret
```

3. Start services with Docker Compose:

```bash
docker-compose up --build
```

4. Initialize databases (scripts/db_init.sh) — run migrations and ensure Mongo indexes for embeddings.

5. Load sample market data (scripts/load_sample_data.py) to simulate live stream.

6. Access the API:

- FastAPI docs: `http://localhost:8000/docs`
- Django admin: `http://localhost:8001/admin` (create superuser via `scripts/create_admin.sh`)

---

## 🛠️ Phase 1 — Deliverables

- FastAPI service(s): `/ingest`, `/query`, `/health`
- Celery + RabbitMQ worker for background tasks (embedding generation, analytics)
- MongoDB schema & vector index setup
- Postgres schema for users, subscriptions, alerts
- Basic LLM + RAG integration (local Ollama or remote API key configurable)
- Docker Compose for local orchestration
- Unit tests for core logic and CI integration stub

---

## ☁️ Phase 2 — AWS Deployment (Free-tier mindful)

- EC2: fastapi + celery workers (t2.micro/t3.micro) or EKS for Kubernetes
- RDS: PostgreSQL (free-tier instance)
- MongoDB Atlas free-tier cluster
- S3: document storage and raw data
- Lambda + API Gateway: summary generator and lightweight endpoints
- CloudWatch: logs and basic metrics
- IAM roles and KMS for secrets

Security considerations and costs are in `docs/aws_cost_and_security.md`.

---

## 🔁 CI/CD & GitOps

- Jenkins pipeline builds Docker images and runs tests
- Push to private Docker registry (or GitHub Container Registry)
- ArgoCD watches repo and deploys to Kubernetes (minikube for local demo; EKS for prod)
- Optional: GitHub Actions can replace Jenkins for a zero-infra CI

---

## 🔐 Security & Ops

- Use JWT for API auth, with refresh tokens
- AES-256 for sensitive data at rest; keys managed via AWS KMS in prod
- Environment variables stored via AWS SSM / Secrets Manager in production
- Rate limiting using FastAPI middleware (limits per IP/api-key)
- Audit logs written to Postgres and S3

---

## 📈 Observability & Monitoring

- Expose Prometheus metrics in each service (`/metrics`)
- Grafana dashboards for latency, error rates, task queue depth
- CloudWatch for AWS-hosted components
- Alerts via SNS / Slack webhook on failures or high queue depth

---

## 📝 Weekly Update Template (for LinkedIn)

**Week X — TradeSense AI Update**

- What I built this week: _short summary_
- Key learnings: _what new tech / pitfalls_
- Screenshot or GIF: _API response, Grafana panel, deployment log_
- Link to repo: `https://github.com/<your-user>/tradesense-ai`

---

## ✅ Demo Script (for interviews)

1. Briefly present architecture diagram (docs/arch.png)
2. Show `docker-compose up` bringing services online
3. Run `scripts/load_sample_data.py` to simulate live feed
4. Query `/query` endpoint to generate an AI summary (show logs)
5. Show Celery dashboard/Flower or metrics for background tasks
6. Show Jenkins pipeline run or ArgoCD sync
7. Discuss how you would scale this to handle production traffic

---

## 🙌 Contributing

Contributions, issues, and feature requests are welcome. Please read `CONTRIBUTING.md` for details on coding standards and local setup.

---

## 📄 License

MIT License — see `LICENSE` file.

---

## 📞 Contact

Your Name — `your.email@example.com` | GitHub: `https://github.com/<your-user>` | LinkedIn: `https://linkedin.com/in/<your-user>`

---

_End of README — Proceed to Phase 1 scaffolding when ready._
