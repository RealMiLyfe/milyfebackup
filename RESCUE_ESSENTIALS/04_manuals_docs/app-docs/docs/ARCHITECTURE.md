# MiLyfe Architecture

## Overview

MiLyfe is a local-first, offline-capable community platform built with React Native/Expo. The architecture prioritizes: privacy, accessibility, human agency, and offline resilience.

## Tech Stack

| Layer | Technology | License |
|---|---|---|
| Runtime | React Native + Expo | MIT |
| Routing | Expo Router (file-based) | MIT |
| State | React Context + useReducer | — |
| Persistence | AsyncStorage + SQLite | MIT/Public Domain |
| Messaging | Matrix protocol (Synapse) | Apache-2.0 |
| AI | llama.cpp / Ollama (local) | MIT |
| Auth | WebAuthn / Passkeys | Web standard |
| Mesh | BLE + WiFi-Direct + LoRa | — |
| Deployment | Docker + K3s + Woodpecker CI | Apache-2.0 |

## Service Architecture

```
┌─────────────────────────────────────────────────────┐
│                    UI LAYER                           │
│  54 screens · 22 components · Expo Router            │
├─────────────────────────────────────────────────────┤
│                 MIDDLEWARE                            │
│  Action → MiScope → Persist → Notify → Sync         │
├───────────┬──────────┬──────────┬───────────────────┤
│ MiAction  │ MiScope  │ MiReceipt│  MiWalk           │
│ (envelope)│ (perms)  │ (proof)  │  (offline)        │
├───────────┼──────────┼──────────┼───────────────────┤
│ MiStage   │ MiSource │ MiAppeal │  MiModerate       │
│ (P vs L)  │ (fresh)  │ (due proc)│ (safety)         │
├───────────┼──────────┼──────────┼───────────────────┤
│ Ledger    │ Standing │ Messages │  Identity          │
│ ($MLY)    │ (facets) │ (Matrix) │  (WebAuthn)       │
├───────────┼──────────┼──────────┼───────────────────┤
│ Place     │ Notifs   │ Export   │  Onboarding       │
│ (jurisd.) │ (private)│ (always) │  (7 steps)        │
├───────────┴──────────┴──────────┴───────────────────┤
│              TRANSPORT / MESH                         │
│  Internet · BLE · WiFi-Direct · LoRa · DTN           │
├─────────────────────────────────────────────────────┤
│              PERSISTENCE                             │
│  SQLite (local) · AsyncStorage · Sync Engine         │
└─────────────────────────────────────────────────────┘
```

## Key Design Decisions

### Local-First
All data lives on the device. The server is optional for sync, not required for function.

### MiAction Protocol
Every consequential action is wrapped in a standard envelope carrying: actor, place, audience, state, approvals, consent, reversal rules, and appeal route. This is the foundation all services share.

### Permission Model (MiScope)
OpenFGA-style relationship graph + OPA-style policy evaluation. Answers "can this person do this thing?" with context (place, stage, age, emergency).

### Offline-First Money (MiWalk)
Reservations prevent double-spend. Conflicts require human review — the system never silently picks a winner for money, roles, or votes.

### Stage Isolation (MiStage)
Practice shares cannot become Live shares. The boundary is enforced at the service layer, not just UI.

## Directory Structure

```
milyfe-app/
├── app/                   # Expo Router screens (file-based routing)
│   ├── (tabs)/           # Main tab navigation
│   │   ├── pocket/      # Money screens
│   │   ├── learn/       # Education screens
│   │   ├── street/      # Resources & community
│   │   ├── voice/       # Governance
│   │   └── you/         # Profile, safety, settings
│   ├── auth/            # Signup & welcome
│   ├── keeper.tsx       # Admin workspace
│   └── youth.tsx        # Child mode
├── src/
│   ├── components/      # Reusable UI
│   │   ├── ui/         # Design system primitives
│   │   ├── layout/     # Responsive layouts
│   │   └── mi/         # Helper panel
│   ├── hooks/          # React hooks
│   ├── i18n/           # Translations (en, es, ar)
│   ├── services/       # Business logic (24 services)
│   ├── theme/          # Colors, typography, spacing
│   ├── types/          # TypeScript definitions
│   └── utils/          # Accessibility, print, focus, RTL
├── __tests__/          # Jest test suites (13 suites)
├── k8s/               # Kubernetes manifests
└── docs/              # Architecture documentation
```

## Getting Started

```bash
# Install dependencies
npm install --legacy-peer-deps

# Run web (development)
npx expo start --web

# Run TypeScript check
npx tsc --noEmit

# Run tests
npx jest

# Build for production
npx expo export --platform web

# Build Docker image
docker build -t milyfe-web .
```

## Design Laws (Non-Negotiable)

1. Five primary destinations; no module explosion
2. One account and profile; household/shop are layers
3. Practice money can never visually resemble live money
4. Helper messages are always labeled
5. Mi cannot send, spend, publish, vote, or change safety settings alone
6. Every public item shows freshness and source
7. Every sharing action shows audience before confirmation
8. Every serious action has an appeal or human review path
9. Export works even during a dispute
10. Accessibility blocks release
