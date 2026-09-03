# MiLyfe Deployment Guide

## Local Development

### Prerequisites
- Node.js 20+
- Docker & Docker Compose
- Git

### Quick Start

```bash
# 1. Clone and install
cd milyfe-app
npm install --legacy-peer-deps

# 2. Start backend services
docker compose up -d

# 3. Pull LLM model (first time only, ~2GB)
docker exec milyfe-app-ollama-1 ollama pull llama3.2:3b

# 4. Start the app
npx expo start --web
```

### Accessing Services
| Service | URL | Purpose |
|---|---|---|
| MiLyfe App | http://localhost:8081 | The web app |
| Matrix Synapse | http://localhost:8008 | Messaging backend |
| Ollama | http://localhost:11434 | Local LLM |
| Temporal Web | http://localhost:8233 | Workflow monitoring |
| OpenFGA | http://localhost:8080 | Authorization |
| PostgreSQL | localhost:5432 | Database |

---

## Production Deployment (K3s)

### Infrastructure Requirements
- 3+ nodes (K3s lightweight Kubernetes)
- OpenTofu for infrastructure-as-code
- OpenBao for secrets management
- Woodpecker CI for builds
- Let's Encrypt for TLS

### Steps

```bash
# 1. Provision with OpenTofu
cd infrastructure/
tofu apply

# 2. Install K3s on nodes
curl -sfL https://get.k3s.io | sh -

# 3. Deploy MiLyfe
kubectl apply -f k8s/

# 4. Verify
kubectl get pods -n milyfe
```

### Security Checklist

- [ ] TLS on all endpoints (cert-manager + Let's Encrypt)
- [ ] CSP headers configured (nginx.conf)
- [ ] No secrets in environment variables (use OpenBao)
- [ ] Network policies restrict inter-service communication
- [ ] Image scanning in CI pipeline
- [ ] SBOM generated for every release
- [ ] No telemetry to third parties
- [ ] Backup encryption keys stored separately from data
- [ ] Incident response plan documented
- [ ] Place-level key rotation automated

---

## Environment Variables

```env
# Required
DATABASE_URL=postgres://milyfe:password@localhost:5432/milyfe
MATRIX_HOMESERVER_URL=http://localhost:8008
OLLAMA_URL=http://localhost:11434
TEMPORAL_ADDRESS=localhost:7233
OPENFGA_API_URL=http://localhost:8080

# Optional
MILYFE_STAGE=practice          # practice | live
MILYFE_PLACE=riverside         # Default place
MILYFE_LOG_LEVEL=info          # debug | info | warn | error
MILYFE_UBI_INTERVAL=604800000  # Weekly in ms (7 days)
MILYFE_UBI_AMOUNT=100          # Shares per delivery
```

---

## Monitoring

Use OpenTelemetry (not a proprietary APM):
- Traces: Jaeger
- Metrics: Prometheus + Grafana
- Logs: Loki
- Alerts: Alertmanager

**What to monitor:**
- Walking actions not settling (sync health)
- Stale resources (verification overdue)
- Safety escalations (response time)
- Offline devices not reconnecting
- Key rotation overdue
- UBI delivery failures
