#!/bin/bash
# ═══════════════════════════════════════════════════════════════
# HYPERBOLIC TIME CHAMBER — One command. Everything online.
# ═══════════════════════════════════════════════════════════════

set -e
DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$DIR"

# ─── Colors ───────────────────────────────────────────────────
RED='\033[0;31m'
GREEN='\033[0;32m'
CYAN='\033[0;36m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo ""
echo -e "${CYAN}╔══════════════════════════════════════════════════════════════╗${NC}"
echo -e "${CYAN}║         HYPERBOLIC TIME CHAMBER                             ║${NC}"
echo -e "${CYAN}║         165 days. One machine. One mission.                 ║${NC}"
echo -e "${CYAN}╚══════════════════════════════════════════════════════════════╝${NC}"
echo ""

# ─── Stop command ─────────────────────────────────────────────
if [ "$1" = "stop" ]; then
    echo -e "${YELLOW}Shutting down...${NC}"
    docker compose down
    echo -e "${GREEN}All services stopped.${NC}"
    exit 0
fi

# ─── First-run setup ─────────────────────────────────────────
if [ ! -f ".env" ]; then
    echo -e "${YELLOW}First run detected. Creating .env from .env.example...${NC}"
    cp .env.example .env

    # Generate secrets automatically
    sed -i "s/CHANGE_ME_STRONG_PASSWORD/$(openssl rand -hex 16)/" .env
    sed -i "s/CHANGE_ME_RANDOM_STRING/$(openssl rand -hex 32)/" .env
    sed -i "s/CHANGE_ME_GHOST_ROOT/$(openssl rand -hex 16)/" .env
    sed -i "s/CHANGE_ME_GHOST_PASSWORD/$(openssl rand -hex 16)/" .env
    sed -i "s/CHANGE_ME_GENERATE_WITH_OPENSSL/$(openssl rand -hex 64)/g" .env
    # n8n key needs separate generation (the g flag above only hits the first CHANGE_ME pattern per line)
    grep -q "CHANGE_ME_GENERATE_WITH_OPENSSL" .env && \
        sed -i "s/CHANGE_ME_GENERATE_WITH_OPENSSL/$(openssl rand -hex 32)/" .env

    echo -e "${GREEN}.env created with generated secrets.${NC}"
    echo -e "${YELLOW}NOTE: You still need to fill in MM_WEBHOOK_* values after Mattermost setup.${NC}"
    echo -e "${YELLOW}NOTE: Fill in SMTP_* and API keys from ~/.fcc/.env if desired.${NC}"
    echo ""
fi

# ─── Pull and start everything ────────────────────────────────
echo -e "${CYAN}Starting all services...${NC}"
docker compose up -d --build 2>&1 | tail -5

# ─── Wait for PostgreSQL ──────────────────────────────────────
echo -e "${CYAN}Waiting for database...${NC}"
for i in $(seq 1 30); do
    if docker exec htc-postgres pg_isready -U milyfe >/dev/null 2>&1; then
        echo -e "${GREEN}Database ready.${NC}"
        break
    fi
    if [ "$i" -eq 30 ]; then
        echo -e "${YELLOW}Database still starting — continuing...${NC}"
    fi
    sleep 2
done

# ─── Check host Ollama ─────────────────────────────────────────
echo -e "${CYAN}Checking host Ollama...${NC}"
if curl -s --max-time 3 http://localhost:11434/api/tags >/dev/null 2>&1; then
    echo -e "${GREEN}Host Ollama is running.${NC}"
    # Pull qwen2.5:3b if not already available
    if ! curl -s http://localhost:11434/api/tags | grep -q "qwen2.5:3b"; then
        echo -e "${YELLOW}Pulling qwen2.5:3b...${NC}"
        curl -s http://localhost:11434/api/pull -d '{"name":"qwen2.5:3b"}' >/dev/null &
        echo -e "${YELLOW}Pull started in background.${NC}"
    fi
else
    echo -e "${RED}Host Ollama not running. Start it with: ollama serve${NC}"
fi

# ─── Health check all services ────────────────────────────────
echo ""
echo -e "${CYAN}═══════════════════════════════════════════════════════════════${NC}"
echo -e "${CYAN}  SERVICE STATUS${NC}"
echo -e "${CYAN}═══════════════════════════════════════════════════════════════${NC}"

check() {
    local name=$1
    local port=$2
    if curl -s --max-time 3 "http://localhost:$port" >/dev/null 2>&1; then
        printf "  ${GREEN}●${NC} %-25s → localhost:%-5s\n" "$name" "$port"
    else
        printf "  ${RED}○${NC} %-25s → localhost:%-5s ${YELLOW}(starting)${NC}\n" "$name" "$port"
    fi
}

check "Mattermost (Ops Hub)"    8065
check "SearXNG (Research)"      8080
check "n8n (Automation)"        5678
check "ntfy (Phone Alerts)"     9091
check "Ghost (Blog)"            2370
check "Mastodon (Social)"       3004
check "Listmonk (Email)"        9001
check "Owncast (Live Stream)"   8095
check "Uptime Kuma (Monitor)"   3012
check "Campaign API"            8200
check "Chamber Bot"             8066
check "Traefik (Proxy)"         8888

# ─── Campaign countdown ───────────────────────────────────────
echo ""
echo -e "${CYAN}═══════════════════════════════════════════════════════════════${NC}"
echo -e "${CYAN}  CAMPAIGN COUNTDOWN${NC}"
echo -e "${CYAN}═══════════════════════════════════════════════════════════════${NC}"

today=$(date +%s)
petition=$(date -d "2026-12-14" +%s 2>/dev/null || date -j -f "%Y-%m-%d" "2026-12-14" +%s 2>/dev/null)
qualifying=$(date -d "2027-01-11" +%s 2>/dev/null || date -j -f "%Y-%m-%d" "2027-01-11" +%s 2>/dev/null)
primary=$(date -d "2027-03-09" +%s 2>/dev/null || date -j -f "%Y-%m-%d" "2027-03-09" +%s 2>/dev/null)
office=$(date -d "2027-07-01" +%s 2>/dev/null || date -j -f "%Y-%m-%d" "2027-07-01" +%s 2>/dev/null)

if [ -n "$petition" ]; then
    days_petition=$(( (petition - today) / 86400 ))
    days_qualifying=$(( (qualifying - today) / 86400 ))
    days_primary=$(( (primary - today) / 86400 ))
    days_office=$(( (office - today) / 86400 ))

    printf "  Petition deadline:    ${YELLOW}%s days${NC} (Dec 14, 2026)\n" "$days_petition"
    printf "  Qualifying window:    ${YELLOW}%s days${NC} (Jan 11-15, 2027)\n" "$days_qualifying"
    printf "  Primary election:     ${YELLOW}%s days${NC} (Mar 9, 2027)\n" "$days_primary"
    printf "  Mayor takes office:   ${YELLOW}%s days${NC} (Jul 1, 2027)\n" "$days_office"
fi

echo ""
echo -e "${CYAN}═══════════════════════════════════════════════════════════════${NC}"
echo ""
echo -e "${GREEN}  The Hyperbolic Time Chamber is online.${NC}"
echo -e "${GREEN}  It never sleeps. It never stops. It never forgets.${NC}"
echo ""
echo -e "  Dashboard:      ${CYAN}http://localhost:8200${NC}"
echo -e "  Ops Hub:        ${CYAN}http://localhost:8065${NC}"
echo -e "  Automation:     ${CYAN}http://localhost:5678${NC}"
echo -e "  Blog:           ${CYAN}http://localhost:2370${NC}"
echo -e "  Live Stream:    ${CYAN}http://localhost:8095${NC}"
echo ""
echo -e "  Stop:           ${YELLOW}./start.sh stop${NC}"
echo ""
