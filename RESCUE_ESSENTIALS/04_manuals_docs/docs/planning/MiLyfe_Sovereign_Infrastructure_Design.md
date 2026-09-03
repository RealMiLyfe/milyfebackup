# MiLyfe — Sovereign Infrastructure Design

**Version:** 1.0  
**Date:** 24 August 2026  
**Authority:** This document describes HOW each OS layer is architected. The MiLyfe Ultimate Manual remains the source of truth for WHAT the system does and WHY. If they conflict on architecture, this document wins. If they conflict on rights, the Manual wins.  
**Scope:** 10 OS layers + Inter-OS Coordination + Phase Triggers + Mesh-in-a-Box + Federation Protocol

---

## Table of Contents

1. [OS 1 — Infrastructure OS](#os-1--infrastructure-os)
2. [OS 2 — Coordination OS](#os-2--coordination-os)
3. [OS 3 — Internet Services OS](#os-3--internet-services-os)
4. [OS 4 — Communication OS (MiMesh)](#os-4--communication-os-mimesh)
5. [OS 5 — AI OS](#os-5--ai-os)
6. [OS 6 — Economic OS](#os-6--economic-os)
7. [OS 7 — Constitutional OS](#os-7--constitutional-os)
8. [OS 8 — Education OS](#os-8--education-os)
9. [OS 9 — Population OS](#os-9--population-os)
10. [OS 10 — Physical Universe OS](#os-10--physical-universe-os)
11. [Inter-OS Coordination](#inter-os-coordination)
12. [Phase Triggers](#phase-triggers)
13. [Mesh-in-a-Box](#mesh-in-a-box)
14. [Federation Protocol](#federation-protocol)

---

# OS 1 — Infrastructure OS

**Purpose:** Provide the sovereign compute, storage, networking, and CI/CD substrate that every other OS layer runs on. No external dependency that can be revoked by a single company.

---

## 1.1 Hosting Replacement

**Current dependency to eliminate:** AWS / GCP / Azure managed services.

**Target stack:**

| Layer | Technology | License | Notes |
|-------|-----------|---------|-------|
| Container orchestration | K3s (lightweight Kubernetes) | Apache-2.0 | Single binary, ARM64/x86, <512MB RAM overhead |
| Infrastructure-as-code | OpenTofu | MPL-2.0 | Terraform fork, no BSL lock-in |
| Secrets management | OpenBao | MPL-2.0 | Vault fork, no HashiCorp BSL |
| Ingress/TLS | Traefik | MIT | Auto Let's Encrypt, middleware chains |
| Service mesh (optional) | Cilium | Apache-2.0 | eBPF-based, no sidecar overhead |
| Bare-metal provisioner | Tinkerbell | Apache-2.0 | PXE + workflow for new nodes |
| DNS (external) | PowerDNS | GPL-2.0 | API-driven zone management |
| DNS (internal) | CoreDNS (bundled with K3s) | Apache-2.0 | Service discovery |
| Load balancer (bare-metal) | MetalLB | Apache-2.0 | BGP or L2 mode |
| Storage (block) | Longhorn | Apache-2.0 | Distributed block, 3-replica default |
| Storage (object) | MinIO | AGPL-3.0 | S3-compatible, erasure coding |
| Monitoring | Prometheus + Grafana | Apache-2.0 | TSDB + dashboards |
| Logging | Loki + Promtail | AGPL-3.0 | Log aggregation without Elasticsearch |
| Alerting | Alertmanager | Apache-2.0 | PagerDuty/ntfy/Matrix integration |
| Backup | Velero + Restic | Apache-2.0 | Cluster-level + volume snapshots |

**Deployment model:**

```
┌─────────────────────────────────────────────────────┐
│  CONTROL PLANE (3 nodes minimum for HA)             │
│  K3s server + etcd embedded + OpenBao sealed        │
├─────────────────────────────────────────────────────┤
│  WORKER POOL (scales horizontally)                  │
│  K3s agents + Longhorn storage + GPU nodes (AI)     │
├─────────────────────────────────────────────────────┤
│  EDGE NODES (community mesh relays)                 │
│  K3s agents (lightweight) + MiESP bridge            │
└─────────────────────────────────────────────────────┘
```

**Minimum viable deployment:** 3x ARM64 nodes (Raspberry Pi 5 8GB or equivalent), 1TB NVMe each. Total hardware cost: ~$600. Handles 500 members.

---

## 1.2 Database Replacement

**Current dependency to eliminate:** Supabase Cloud / managed Postgres.

**Target stack:**

| Component | Technology | License | Purpose |
|-----------|-----------|---------|---------|
| Primary RDBMS | PostgreSQL 16+ | PostgreSQL License | All structured data |
| Connection pooler | PgBouncer | ISC | Connection multiplexing |
| Replication | Patroni | MIT | HA + automatic failover |
| Vector search | pgvector extension | PostgreSQL License | RAG embeddings |
| Full-text search | Meilisearch | MIT | Instant search, typo-tolerant |
| Time-series | TimescaleDB Community | Apache-2.0 | IoT telemetry, MiPulse |
| Key-value / cache | KeyDB | BSD-3-Clause | Hot cache layer |
| Document store | PostgreSQL JSONB | PostgreSQL License | Semi-structured data |
| Graph queries | Apache AGE (Postgres ext) | Apache-2.0 | MiScope relationship graph |
| Realtime | PostgreSQL LISTEN/NOTIFY + NATS | Various | Live updates to clients |
| Migrations | golang-migrate | MIT | Version-controlled schema |
| Backup | pgBackRest | MIT | PITR, parallel, encrypted |

**Schema namespaces (one Postgres cluster, logical databases):**

```
milyfe_identity    — profiles, credentials, recovery
milyfe_pocket      — ledger, jars, transactions
milyfe_voice       — proposals, ballots, delegations
milyfe_learn       — paths, progress, badges
milyfe_street      — marketplace, quests, resources
milyfe_mesh        — topology, nodes, routes
milyfe_safety      — reports, freezes, appeals (encrypted at rest)
milyfe_iot         — NGSI-LD entity store
milyfe_ai          — helper memory, RAG chunks, function logs
milyfe_federation  — remote instance registry, standing portability
```

**Replication strategy:**
- Synchronous replication within a site (zero data loss)
- Asynchronous replication across federated instances (eventual consistency for portable data)
- Encrypted WAL archival to MinIO (PITR up to 30 days)

---

## 1.3 Git Replacement

**Current dependency to eliminate:** GitHub / GitLab SaaS.

**Target stack:**

| Component | Technology | License | Purpose |
|-----------|-----------|---------|---------|
| Git forge | Forgejo | MIT | Code hosting, issues, PRs, packages |
| CI/CD | Woodpecker CI | Apache-2.0 | Container-native pipelines |
| Artifact registry | Forgejo Packages | MIT | OCI/npm/PyPI/Maven |
| Dependency updates | Renovate (self-hosted) | AGPL-3.0 | Automated version bumps |
| Code quality | SonarQube Community | LGPL-3.0 | Static analysis |
| SBOM/signing | Sigstore + syft | Apache-2.0 | Supply chain integrity |
| License compliance | FOSSology | GPL-2.0 | OSI-only enforcement |
| Vulnerability scan | Trivy | Apache-2.0 | Container + dependency CVEs |

**Repository structure (multi-repo):**

```
milyfe/
├── platform-core/          — Shared libraries, MiAction, MiScope, MiReceipt
├── app-mobile/             — React Native / Expo client
├── app-web/                — Next.js / React web client
├── services-identity/      — Keycloak + DID + passkeys
├── services-pocket/        — Ledger, UBI, treasury
├── services-voice/         — Governance engine
├── services-learn/         — Education paths + badges
├── services-street/        — Marketplace, quests, resources
├── services-mesh/          — MiDTN, MiTURN, MiQoS, transport
├── services-ai/            — Helper orchestration, RAG, inference
├── services-safety/        — MiChildGate, moderation, reports
├── services-iot/           — FIWARE + digital twins
├── services-federation/    — Cross-instance protocol
├── infra/                  — OpenTofu modules, Helm charts, Woodpecker pipelines
├── docs/                   — Architecture decisions, API specs
├── constitution/           — Living Compact source + law compiler
└── community/              — Contribution guides, code of conduct
```

**Branch strategy:** Trunk-based development. Short-lived feature branches. Signed commits required. Woodpecker runs on every push: lint, test, SBOM, license check, security scan, build, deploy to staging.

---

## 1.4 Cost Curve

| Community Size | Nodes | Monthly Cost (self-hosted) | Monthly Cost (VPS fallback) |
|---------------|-------|----------------------------|------------------------------|
| 50 members | 1 node (8GB ARM64) | ~$8 electricity | ~$24 (Hetzner CAX21) |
| 200 members | 3 nodes (8GB each) | ~$24 electricity | ~$72 (3x CAX21) |
| 1,000 members | 5 nodes (16GB each) | ~$40 electricity | ~$150 (5x CAX31) |
| 5,000 members | 8 nodes (32GB) + 2 GPU | ~$80 electricity + amortization | ~$400 (mixed fleet) |
| 25,000 members | 15 nodes + 4 GPU + NAS | ~$200 electricity | ~$1,200 |
| 100,000 members | 30 nodes + 8 GPU + SAN | ~$500 electricity | ~$3,500 |

**Key principle:** Self-hosted hardware is a one-time cost amortized over 5 years. Electricity-only monthly cost means a community cannot be priced out by a vendor raising rates.

**GPU allocation:** Primarily for on-premise AI inference (llama.cpp, Whisper, Stable Diffusion). Not required for core platform — degrades gracefully to cloud fallback or smaller models.

---

## 1.5 Multi-Repo Architecture

**Why multi-repo over monorepo:**
- Independent deploy cycles (mesh updates don't block voice updates)
- Clear ownership boundaries (each service has a CODEOWNERS file)
- Smaller CI times per repo
- Forkability — a community can fork one service without pulling the entire platform
- License isolation — AGPL services stay separate from MIT/Apache libraries

**Cross-repo coordination:**
- Shared contract packages (`platform-core`) published as versioned artifacts
- API contracts defined via OpenAPI 3.1 + AsyncAPI 3.0 (event schemas)
- Breaking changes require RFC in `docs/` repo with 7-day review period
- Dependency graph visualized in Forgejo (via CI-generated SBOM)
- Integration tests run in a dedicated `integration-tests/` repo triggered by downstream releases

---

# OS 2 — Coordination OS

**Purpose:** The genuine new invention. Seven protocols that enforce human-rights semantics consistently across all modules. This is what makes MiLyfe more than a bundle of open-source services.

---

## 2.1 MiAction — Common Human-Action Envelope

Every consequential action in MiLyfe — a payment, a vote, a report, a helper suggestion, a shop listing, a resource update — travels inside one envelope. This is the universal unit of coordination.

### Full Schema

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://milyfe.org/schemas/mi-action/v1",
  "title": "MiAction Envelope",
  "type": "object",
  "required": [
    "id", "version", "type", "actor", "place", "jurisdiction",
    "audience", "purpose", "sensitivity", "state", "created_at"
  ],
  "properties": {
    "id": {
      "type": "string",
      "format": "uuid",
      "description": "Globally unique action identifier (UUIDv7 for time-ordering)"
    },
    "version": {
      "type": "string",
      "const": "1.0"
    },
    "type": {
      "type": "string",
      "description": "Action type URI (e.g. pocket.thank, voice.ballot, street.quest.complete)",
      "pattern": "^[a-z][a-z0-9_]*(\\.[a-z][a-z0-9_]*)+$"
    },
    "actor": {
      "type": "object",
      "required": ["did", "role"],
      "properties": {
        "did": { "type": "string", "description": "Decentralized identifier of acting person or helper" },
        "role": { "type": "string", "description": "Role under which action is performed" },
        "device_id": { "type": "string", "description": "Originating device (for offline conflict resolution)" },
        "is_helper": { "type": "boolean", "default": false, "description": "True if actor is AI helper (triggers disclosure)" }
      }
    },
    "place": {
      "type": "object",
      "required": ["instance_id"],
      "properties": {
        "instance_id": { "type": "string", "description": "MiLyfe instance where action originates" },
        "geo_scope": { "type": "string", "enum": ["block", "neighborhood", "city", "region", "global"] },
        "coordinates": {
          "type": "object",
          "properties": {
            "lat": { "type": "number" },
            "lon": { "type": "number" },
            "accuracy_m": { "type": "number" }
          }
        }
      }
    },
    "jurisdiction": {
      "type": "object",
      "required": ["law_pack_version"],
      "properties": {
        "law_pack_version": { "type": "string" },
        "country_code": { "type": "string", "pattern": "^[A-Z]{2}$" },
        "subdivision": { "type": "string" },
        "overrides": { "type": "array", "items": { "type": "string" } }
      }
    },
    "audience": {
      "type": "object",
      "required": ["visibility"],
      "properties": {
        "visibility": { "type": "string", "enum": ["self", "named", "household", "circle", "place", "federation", "public"] },
        "named_recipients": { "type": "array", "items": { "type": "string" } },
        "exclude": { "type": "array", "items": { "type": "string" }, "description": "DIDs explicitly excluded (e.g. abuser in DV)" }
      }
    },
    "purpose": { "type": "string", "description": "Human-readable purpose (data minimization compliance)" },
    "sensitivity": { "type": "string", "enum": ["public", "community", "private", "intimate", "safety_critical"] },
    "state": {
      "type": "object",
      "required": ["current"],
      "properties": {
        "current": { "type": "string", "enum": ["draft", "pending_approval", "walking", "sent", "arrived", "executed", "failed", "expired", "reversed", "appealed"] },
        "previous": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "state": { "type": "string" },
              "at": { "type": "string", "format": "date-time" },
              "by": { "type": "string" }
            }
          }
        }
      }
    },
    "approvals": {
      "type": "object",
      "properties": {
        "required": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "role": { "type": "string" },
              "did": { "type": "string" },
              "reason": { "type": "string" },
              "granted": { "type": "boolean" },
              "at": { "type": "string", "format": "date-time" }
            }
          }
        },
        "policy_ref": { "type": "string", "description": "OPA policy that determined requirements" }
      }
    },
    "consent": {
      "type": "object",
      "properties": {
        "receipt_id": { "type": "string", "format": "uuid" },
        "purposes": { "type": "array", "items": { "type": "string" } },
        "revocable": { "type": "boolean", "default": true }
      }
    },
    "source": {
      "type": "object",
      "properties": {
        "policy_version": { "type": "string" },
        "helper_model": { "type": "string", "description": "If helper-initiated: model ID and version" },
        "confidence": { "type": "number", "minimum": 0, "maximum": 1 },
        "citations": { "type": "array", "items": { "type": "string" } }
      }
    },
    "expiration": {
      "type": "object",
      "properties": {
        "expires_at": { "type": "string", "format": "date-time" },
        "behavior_on_expiry": { "type": "string", "enum": ["void", "archive", "escalate", "auto_approve"] }
      }
    },
    "reversal": {
      "type": "object",
      "properties": {
        "reversible": { "type": "boolean", "default": false },
        "reversal_window_hours": { "type": "number" },
        "reversal_requires": { "type": "string", "description": "Who can reverse (actor, guardian, circle, appeal)" }
      }
    },
    "appeal": {
      "type": "object",
      "properties": {
        "route": { "type": "string", "enum": ["peer_review", "circle_panel", "place_mediator", "federation_ombuds", "fork"] },
        "deadline_hours": { "type": "number" }
      }
    },
    "offline": {
      "type": "object",
      "properties": {
        "created_offline": { "type": "boolean", "default": false },
        "conflict_rule": { "type": "string", "enum": ["last_write_wins", "first_write_wins", "merge", "human_review", "reject_later", "reservation"] },
        "vector_clock": { "type": "object", "additionalProperties": { "type": "integer" } },
        "max_offline_hours": { "type": "number" }
      }
    },
    "explanation": {
      "type": "object",
      "properties": {
        "human_readable": { "type": "string", "description": "Plain-language explanation (6th-grade reading level)" },
        "language": { "type": "string", "description": "ISO 639-1 code" }
      }
    },
    "payload": { "type": "object", "description": "Action-type-specific data (schema varies by type)" },
    "created_at": { "type": "string", "format": "date-time" },
    "updated_at": { "type": "string", "format": "date-time" },
    "signature": { "type": "string", "description": "Ed25519 signature over canonical JSON (excluding this field)" }
  }
}
```

### Action Lifecycle State Machine

```
                 ┌──────────┐
                 │  draft   │
                 └────┬─────┘
                      │ submit
                      ▼
              ┌───────────────┐
              │pending_approval│
              └───────┬───────┘
                      │ all approvals granted
                      ▼
               ┌────────────┐    (offline/mesh)    ┌─────────┐
               │    sent    │─────────────────────►│ walking │
               └─────┬──────┘                      └────┬────┘
                     │ delivered                         │ arrives
                     ▼                                   ▼
              ┌────────────┐                      ┌────────────┐
              │  arrived   │◄─────────────────────│  arrived   │
              └─────┬──────┘                      └────────────┘
                    │ process
                    ▼
              ┌────────────┐
              │  executed  │
              └─────┬──────┘
                    │ (if reversible + within window)
                    ▼
              ┌────────────┐
              │  reversed  │
              └────────────┘

  Any state ──► failed (unrecoverable error)
  Any state ──► expired (expiration.expires_at passed)
  executed  ──► appealed (member files appeal)
```

### Non-Negotiable Rules for MiAction

1. **No action without an actor.** Anonymous forbidden (pseudonymous fine — DID without real name).
2. **No action without jurisdiction.** Every action knows which law pack applies.
3. **No child action without guardian.** Under money-age requires guardian in `approvals.required`.
4. **No helper action without disclosure.** `actor.is_helper=true` triggers visible labeling.
5. **No safety action auto-resolved.** `sensitivity=safety_critical` always routes to `human_review`.
6. **Offline actions carry vector clocks.** Two offline payments to same jar: first-write-wins + notify.
7. **Every action has an appeal route.** Even deny decisions explain how to challenge.

---

## 2.2 MiScope — Permission Graph

**Foundation:** OpenFGA (relationship-based access control) + OPA (policy evaluation) + Apache AGE (graph queries).

### Architecture

```
┌─────────────────────────────────────────────────────┐
│  APPLICATION LAYER (services call MiScope)           │
│  "Can actor X do action Y on resource Z?"           │
├─────────────────────────────────────────────────────┤
│  MISCOPE GATEWAY (gRPC + REST)                      │
│  - Resolves relationships via OpenFGA               │
│  - Evaluates policies via OPA                       │
│  - Caches hot paths (5-min TTL)                     │
│  - Logs all decisions (audit trail)                 │
│  - Returns human-readable explanation               │
├─────────────────────────────────────────────────────┤
│  OPENFGA (Relationship Store)       │ OPA (Policy)  │
│  - Person-Person relations          │ - MiLegal     │
│  - Person-Resource relations        │ - Jurisdiction│
│  - Role-Permission mappings         │ - Emergency   │
│  - Time-bound tuples               │ - Age/stage   │
│  - Place-scoped tuples             │ - Conflicts   │
├─────────────────────────────────────────────────────┤
│  APACHE AGE (Complex Graph Queries)                 │
│  - "Who can see this?" preview                      │
│  - Delegation chain resolution                      │
│  - Household/kinship traversal                      │
│  - Conflict-of-interest detection                   │
└─────────────────────────────────────────────────────┘
```

### OpenFGA Authorization Model

```dsl
model
  schema 1.1

type user

type helper
  relations
    define operator: [user]

type place
  relations
    define member: [user]
    define steward: [user] and member
    define keeper: [user] and member
    define visitor: [user]

type household
  relations
    define adult: [user]
    define child: [user]
    define guardian: [user] and adult
    define can_view_finances: guardian or adult
    define can_approve_child_action: guardian

type resource
  relations
    define owner: [user]
    define viewer: [user, user:*, place#member, household#adult]
    define editor: [user] and owner
    define can_view: viewer or owner
    define can_edit: editor
    define can_delete: owner
    define can_appeal: [user]

type circle
  relations
    define member: [user]
    define steward: [user] and member
    define can_propose: member
    define can_vote: member
    define can_spend_treasury: steward

type shop
  relations
    define owner: [user]
    define staff: [user]
    define can_list_product: owner or staff
    define can_view_sales: owner
    define can_accept_mly: owner or staff

type safety_case
  relations
    define reporter: [user]
    define subject: [user]
    define reviewer: [user]
    define can_view_details: reviewer
    define can_decide: reviewer and not subject and not reporter
```

### Relationship Types

| Relationship | Scope | TTL | Notes |
|-------------|-------|-----|-------|
| `member_of` place | Place | Permanent until leave | Core membership |
| `guardian_of` child | Household | Until age-of-majority | Cannot be self-assigned |
| `steward_of` circle | Circle | Rotating (3-6 months) | Sortition-selected |
| `keeper_of` place | Place | Elected (1 year max) | Safety/moderation role |
| `teacher_of` class | Learn | Class duration | Verified credential |
| `mediator_for` dispute | Appeal | Case duration | Conflict-free verified |
| `helper_operator` | Helper | Session/task duration | Human responsible for helper |
| `recovery_contact` | Identity | Until revoked | 2-of-3 threshold |
| `temporary_access` | Any | Explicit expiry (72h max) | Emergency/handoff |
| `shop_staff` | Shop | Employment duration | Can transact on behalf |

### Preview API — "What Can This Person See?"

```http
POST /miscope/v1/preview
{
  "viewer_did": "did:milyfe:alice123",
  "target_did": "did:milyfe:bob456",
  "resource_types": ["profile", "pocket", "location", "messages", "learn_progress"]
}

Response:
{
  "profile": { "visible": true, "fields": ["display_name", "standing_summary", "place"] },
  "pocket": { "visible": false, "reason": "No household or explicit grant" },
  "location": { "visible": false, "reason": "Location sharing disabled by target" },
  "messages": { "visible": true, "scope": "direct_threads_only" },
  "learn_progress": { "visible": false, "reason": "Private by default" }
}
```

---

## 2.3 MiReceipt — W3C Verifiable Credentials

Every consequential action produces a receipt. Human-readable, machine-verifiable, portable.

### Structure (W3C VC Data Model 2.0)

```json
{
  "@context": [
    "https://www.w3.org/ns/credentials/v2",
    "https://milyfe.org/ns/receipt/v1"
  ],
  "type": ["VerifiableCredential", "MiReceipt"],
  "id": "urn:uuid:{{action_id}}",
  "issuer": {
    "id": "did:milyfe:instance:jacksonville-01",
    "name": "MiLyfe Jacksonville"
  },
  "validFrom": "2026-08-24T10:30:00Z",
  "validUntil": "2027-08-24T10:30:00Z",
  "credentialSubject": {
    "id": "did:milyfe:alice123",
    "action_type": "pocket.thank",
    "summary": {
      "en": "You thanked Marcus 12 $MLY for fixing the community garden gate.",
      "es": "Agradeciste a Marcus 12 $MLY por arreglar la puerta del jardin comunitario."
    },
    "what_happened": "12 $MLY transferred from your Weekly pot to Marcus",
    "what_did_not_happen": "No data shared beyond recipient name and amount",
    "who_can_see": "You and Marcus only (visibility: named)",
    "policy_applied": "milyfe-legal:us-fl-duval:v2.3:pocket-transfer",
    "reversible": true,
    "reversal_window": "24 hours",
    "expires": "Never (ledger entry is permanent)",
    "appeal_route": "peer_review -> circle_panel"
  },
  "proof": {
    "type": "Ed25519Signature2020",
    "created": "2026-08-24T10:30:01Z",
    "verificationMethod": "did:milyfe:instance:jacksonville-01#key-1",
    "proofPurpose": "assertionMethod",
    "proofValue": "z3FXQje..."
  }
}
```

### Receipt Types

| Category | Receipt Answers |
|----------|----------------|
| Pocket (thank, UBI, spend) | Amount, from/to, pot affected, reversal window |
| Voice (ballot cast) | "You voted" (NOT how you voted), proposal ref, counted confirmation |
| Learn (badge earned) | Skill name, assessor, evidence hash, portability |
| Street (quest completed) | Task description, verifier, $MLY earned |
| Safety (report filed) | "Report received", case ID, next steps, timeline |
| Identity (recovery used) | Which contacts participated, what was restored |
| Helper (handoff) | What helper did, what human took over, why |
| Moderation (action taken) | What was restricted, reason, appeal deadline |
| Federation (standing ported) | Source instance, standing snapshot, cooling period |

### Storage and Export

- Stored locally on device (SQLite) + synced to personal vault (encrypted MinIO bucket)
- Exportable as JSON-LD, PDF, or QR code at any time
- Survive account deletion (30-day retention for appeal window, then purged)
- Printed receipts include QR linking to verification URL (works offline via local Forgejo Pages)

---

## 2.4 MiSource — Provenance and Freshness Protocol

Every piece of information displayed to a member carries provenance metadata.

### Schema

```json
{
  "$id": "https://milyfe.org/schemas/mi-source/v1",
  "type": "object",
  "required": ["source_id", "maintainer", "checked_at", "expires_at", "confidence"],
  "properties": {
    "source_id": { "type": "string", "format": "uri" },
    "maintainer": {
      "type": "object",
      "properties": {
        "did": { "type": "string" },
        "role": { "type": "string", "enum": ["community_member", "verified_org", "official_source", "helper_crawl", "federation_peer"] },
        "name": { "type": "string" }
      }
    },
    "place": { "type": "string" },
    "verification": {
      "type": "object",
      "properties": {
        "method": { "type": "string", "enum": ["human_visit", "phone_call", "web_scrape", "api_check", "community_report", "official_feed", "unverified"] },
        "verifier_did": { "type": "string" },
        "evidence_hash": { "type": "string" }
      }
    },
    "checked_at": { "type": "string", "format": "date-time" },
    "expires_at": { "type": "string", "format": "date-time" },
    "confidence": { "type": "number", "minimum": 0, "maximum": 1 },
    "language": { "type": "string" },
    "translation_source": { "type": "string" },
    "accessibility": {
      "type": "object",
      "properties": {
        "plain_language": { "type": "boolean" },
        "screen_reader_tested": { "type": "boolean" },
        "reading_level": { "type": "string" }
      }
    },
    "correction_history": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "corrected_at": { "type": "string", "format": "date-time" },
          "field": { "type": "string" },
          "old_value": { "type": "string" },
          "new_value": { "type": "string" },
          "reason": { "type": "string" }
        }
      }
    },
    "stale_behavior": { "type": "string", "enum": ["show_with_warning", "hide", "show_last_known", "redirect_to_call"] }
  }
}
```

### Freshness Rules by Domain

| Domain | Default TTL | Stale Behavior | Re-verification Method |
|--------|-------------|----------------|----------------------|
| Shelter availability | 4 hours | show_with_warning | Phone call or API |
| Food bank hours | 24 hours | show_with_warning | Community report |
| Legal aid clinics | 7 days | show_last_known | Human visit |
| Bus/transit schedules | 1 hour | redirect_to_call | API check |
| Shop hours | 7 days | show_with_warning | Owner update or visit |
| Emergency resources | 1 hour | show_with_warning (NEVER hide) | Official feed |
| Law pack content | 30 days | show_last_known | Official source review |
| Helper citations | Per-query | show_with_warning | RAG re-retrieval |
| Community events | Event end time | hide | Auto-expire |
| Marketplace listings | 72 hours | show_with_warning | Seller ping |

---

## 2.5 MiHandoff — Helper-to-Human Routing

When Mi or any named helper reaches its limit, it routes to a real person. This protocol ensures the right human gets the case without Mi seeing the full profile.

### Routing Algorithm

```
INPUT: handoff_request {
  need_category: enum (legal, medical, safety, financial, emotional,
                       technical, spiritual, housing, employment, education)
  urgency: enum (routine, soon, urgent, emergency)
  language: ISO 639-1
  accessibility_needs: [string]
  place: instance_id + geo_scope
  available_context: { fields the member consented to share }
  conflict_exclusions: [did]  // people who must NOT receive this case
}

PROCESS:
1. Query MiScope for humans with role matching need_category in place
2. Filter by:
   - Language match (required)
   - Accessibility capability (required if specified)
   - Availability window (online or scheduled)
   - No conflict of interest (not in conflict_exclusions, not related)
   - Workload < threshold (max 5 active cases — prevent burnout)
3. If urgency=emergency AND no match:
   - Expand geo_scope one level (block -> neighborhood -> city)
   - If still no match: surface to on-call keeper with emergency flag
4. Score remaining candidates:
   - Proximity (same block > neighborhood > city)
   - Experience (past cases in same category)
   - Member preference (prior positive interaction)
5. Offer to top candidate (60-second accept window)
6. If declined or timeout: next candidate
7. If all decline: escalate urgency + notify steward

OUTPUT: handoff_assignment {
  assigned_to: did
  context_shared: { only fields member consented to }
  response_target: "4h" | "1h" | "15min" | "immediate"
  escalation_timer: response_target x 2
  closure_requires: member confirmation OR 14-day auto-close
}
```

### Privacy Guarantees

1. Helper (AI) sees only: need_category, urgency, language, accessibility_needs, place. NOT name, history, pocket, full profile.
2. Routed human sees only: what member consented to share in `available_context`.
3. Handoff context encrypted in transit and at rest. Purged 30 days after closure.
4. Member can revoke consent mid-case — human loses access immediately.

---

## 2.6 MiAppeal — Five-Level Due Process

Every restrictive decision can be appealed. Five levels ensure proportionality.

### Appeal Levels

| Level | Name | Panel | Timeline | Scope |
|-------|------|-------|----------|-------|
| 1 | Peer Review | 3 random members from same place (not involved) | 72 hours | Minor: content removal, quest denial, marketplace dispute <$50 MLY |
| 2 | Circle Panel | 5 from relevant circle + 1 from adjacent | 7 days | Moderate: temp restrictions, standing disputes, shop bans, helper complaints |
| 3 | Place Mediator | Trained mediator (credential) + 2 observers | 14 days | Serious: long-term restrictions, role removal, significant MLY disputes |
| 4 | Federation Ombuds | 3 mediators from different instances (no local ties) | 30 days | Severe: personhood challenges, permanent bans, constitutional violations |
| 5 | Fork | Member leaves with full data export; community states reason publicly | Immediate | Ultimate: irreconcilable disagreement. Exit with dignity, not punishment. |

### Appeal Flow

```
Decision Made (restrictive action)
        │
        │ member files appeal within deadline
        ▼
Appeal Filed (clock starts, interim measures applied)
        │
        │ panel assembled (random + conflict check)
        ▼
Evidence Phase (both sides submit, translated if needed)
        │
        │ review period
        ▼
Hearing (async written or live session — member's choice)
        │
        │ panel deliberates
        ▼
Decision: Upheld | Modified | Reversed
        │
        ├── Member accepts → case closed
        └── Member escalates → next level (if available)
```

### Interim Measures During Appeal

- Original restriction remains UNLESS it involves: account freeze (partial access restored), child separation (status quo preserved), or emergency safety (immediate keeper review).
- Member retains: full data export, receipt access, message access to panel, right to counsel (another member or helper assists).

### Non-Negotiable Appeal Rules

1. No secret evidence. Both sides see everything the panel sees.
2. No panel member with conflict of interest (MiScope graph check).
3. Translation provided on request.
4. Accessibility accommodations provided (screen reader, plain language, audio, extended time).
5. Panel members compensated with $MLY (quest-level reward).
6. All outcomes anonymized and published quarterly for transparency.

---

## 2.7 MiStage — Capability Gates

Not all features activate simultaneously. MiStage controls availability based on community maturity and legal readiness.

### Implementation: OpenFeature + Custom Provider

```yaml
gates:
  - id: "pocket.peer_swap"
    description: "Peer-to-peer $MLY exchange"
    default: true
    requires:
      member_count: 1  # Available immediately (barter law)

  - id: "pocket.shop_pos"
    description: "Shop POS accepting $MLY"
    default: false
    requires:
      member_count: 50
      legal_review: "msb_assessment_complete"
      community_vote: { quorum: 0.15, approval: 0.60 }

  - id: "voice.binding_vote"
    description: "Binding governance decisions"
    default: false
    requires:
      member_count: 25
      constitution_ratified: true
      circle_count: 3

  - id: "mesh.lora_relay"
    description: "Community LoRa mesh relays"
    default: false
    requires:
      member_count: 10
      legal_review: "spectrum_ism_compliant"
      hardware_deployed: 3

  - id: "federation.cross_instance"
    description: "Federation with other MiLyfe instances"
    default: false
    requires:
      member_count: 100
      uptime_days: 90
      community_vote: { quorum: 0.15, approval: 0.60 }

  - id: "economy.treasury_spend"
    description: "Community treasury spending"
    default: false
    requires:
      member_count: 25
      circle_count: 1
      community_vote: { quorum: 0.15, approval: 0.60 }
      circuit_breaker: "34_percent_rule"

  - id: "iot.digital_twin"
    description: "Physical world digital twin"
    default: false
    requires:
      member_count: 500
      sensors_deployed: 10
      safety_review: "two_person_actuation_verified"
      community_vote: { quorum: 0.15, approval: 0.75 }

  - id: "ai.named_helper"
    description: "Named AI helpers beyond Mi"
    default: false
    requires:
      member_count: 50
      community_vote: { quorum: 0.15, approval: 0.60 }
      rails_audit: "complete"

  - id: "economy.chain_live"
    description: "Live blockchain ledger (not test)"
    default: false
    requires:
      member_count: 1000
      legal_review: "chain_regulatory_complete"
      community_vote: { quorum: 0.25, approval: 0.75 }
      test_chain_duration_days: 180
```

### Gate Evaluation API

```http
GET /mistage/v1/check?gate=pocket.shop_pos&place=jacksonville-01

Response:
{
  "gate": "pocket.shop_pos",
  "active": false,
  "requirements": {
    "member_count": { "required": 50, "current": 37, "met": false },
    "legal_review": { "required": "msb_assessment_complete", "current": "in_progress", "met": false },
    "community_vote": { "required": true, "current": "not_started", "met": false }
  },
  "estimated_activation": "When member count reaches 50 AND legal review completes AND community votes",
  "next_action": "Reach 50 members (need 13 more)"
}
```

### Stage Progression (Community Lifecycle)

| Stage | Name | Members | OS Layers Active | Key Gates Unlocked |
|-------|------|---------|------------------|-------------------|
| 0 | Seed | 1-10 | OS1, OS2 (partial), OS5 (Mi only) | Basic profile, Mi helper, pocket (UBI + thank) |
| 1 | Sprout | 11-50 | + OS8, OS9 (partial) | Learn paths, peer swap, first circle, named helpers |
| 2 | Root | 51-200 | + OS3 (partial), OS7 | Shop POS, binding votes, marketplace, mesh (WiFi) |
| 3 | Trunk | 201-1000 | + OS4, OS6, OS3 (full) | Full mesh, treasury, federation prep, all services |
| 4 | Canopy | 1001-5000 | + OS10 (partial) | Live chain, IoT, digital twins, cross-instance |
| 5 | Forest | 5001-25000 | All OS layers full | Full IoT, AI ring routing, city-scale economics |
| 6 | Ecosystem | 25000+ | All + cross-instance governance | Multi-city federation, protocol governance |

---

## OS 2 Summary

The Coordination OS is the connective tissue. Every service in OS 3-10 produces and consumes MiActions, checks permissions via MiScope, generates MiReceipts, attaches MiSource provenance, routes to humans via MiHandoff, allows challenge via MiAppeal, and respects gates via MiStage. Without OS 2, MiLyfe is just a bundle of unrelated open-source tools. With OS 2, it is a sovereign platform where human rights are enforced by architecture.

---

# OS 3 — Internet Services OS

**Purpose:** Replace every commercial SaaS dependency with self-hosted, federated, OSI-licensed equivalents. Members never see service names — they see Pocket, Learn, Street, Voice, You, and Mi. These services are the engines beneath.

**Deployment pattern:** Every service below runs as a Helm chart on the K3s cluster (OS 1). Each gets: dedicated namespace, Longhorn PVC for data, Traefik ingress route, Prometheus ServiceMonitor, resource limits, and a MiLegal gate (some services only activate at certain MiStage levels).

---

## 3.1 Communication Services (8)

| # | Service | Image | Purpose | Port | RAM (min) | Storage | Federation | MiStage Gate |
|---|---------|-------|---------|------|-----------|---------|------------|-------------|
| 1 | Matrix Synapse | matrixdotorg/synapse | Encrypted messaging, rooms, DMs | 8008 | 512MB | 10GB+ | Matrix federation (S2S on 8448) | Seed (always on) |
| 2 | Element Web | vectorim/element-web | Matrix web client | 80 | 64MB | Static | N/A (client) | Seed |
| 3 | Jitsi Meet | jitsi/web + prosody + jicofo + jvb | Video/voice calls, meetings | 443, 10000/udp | 1GB | Ephemeral | N/A (direct peer) | Sprout |
| 4 | Stalwart Mail | stalwartlabs/stalwart | Email (SMTP + IMAP + JMAP) | 25, 993, 443 | 256MB | 5GB+ | Standard email (MX records) | Root |
| 5 | ntfy | binwiederhier/ntfy | Push notifications (self-hosted) | 2586 | 64MB | 1GB | N/A (local) | Seed |
| 6 | LiveKit | livekit/livekit-server | WebRTC SFU (real-time audio/video) | 7880, 7881 | 512MB | Ephemeral | N/A (mesh-bridgeable) | Sprout |
| 7 | SRS (Simple Realtime Server) | ossrs/srs | RTMP/HLS/WebRTC streaming | 1935, 8080 | 256MB | Ephemeral | N/A (ingest) | Trunk |
| 8 | BigBlueButton | bigbluebutton/bigbluebutton | Education video conferencing | 443 | 4GB | 50GB | N/A (classroom) | Root |

**Matrix configuration highlights:**
- End-to-end encryption mandatory for DMs and safety channels
- Room creation gated by MiScope (who can create public rooms)
- Message retention: 1 year default, member-configurable, safety holds exempt
- Bridges: none by default (no Discord/Slack/WhatsApp bridging — privacy risk)
- Media repository: backed by MinIO, max upload 50MB, virus-scanned (ClamAV)

**Jitsi configuration:**
- No account required to join (link-based, MiLyfe auth optional)
- Recording: opt-in per participant, stored in personal vault only
- Lobby mode default for rooms >5 people
- Bandwidth-adaptive (MiQoS priority: voice > video > screen share)

---

## 3.2 Content & Media Services (11)

| # | Service | Image | Purpose | RAM | Storage | Federation |
|---|---------|-------|---------|-----|---------|------------|
| 1 | PeerTube | chocobozzz/peertube | Video hosting + streaming | 1GB | 100GB+ | ActivityPub + WebTorrent |
| 2 | AzuraCast | azuracast/azuracast | Community radio automation | 512MB | 20GB | Icecast/SHOUTcast |
| 3 | Castopod | castopod/castopod | Podcast hosting + distribution | 256MB | 10GB | ActivityPub + RSS |
| 4 | Navidrome | deluan/navidrome | Music streaming (personal library) | 128MB | Varies | Subsonic API |
| 5 | Funkwhale | funkwhale/funkwhale | Music sharing (community) | 512MB | 50GB+ | ActivityPub |
| 6 | Jellyfin | jellyfin/jellyfin | Media server (video/audio/books) | 1GB | 100GB+ | N/A (local) |
| 7 | Audiobookshelf | advplyr/audiobookshelf | Audiobook + podcast player | 256MB | 20GB+ | N/A (local) |
| 8 | Ghost | ghost:5 | Community news / journalism | 512MB | 5GB | N/A (web publishing) |
| 9 | WriteFreely | writefreely/writefreely | Federated blogging | 128MB | 2GB | ActivityPub |
| 10 | Pixelfed | pixelfed/pixelfed | Photo sharing (no algorithm) | 512MB | 50GB+ | ActivityPub |
| 11 | Owncast | owncast/owncast | Live streaming (self-hosted Twitch) | 512MB | 10GB | N/A (HLS/RTMP) |

**Content governance:**
- All public content passes MiChildGate (CSAM hash-check via PhotoDNA-compatible local scanner)
- Moderation: MiModerate protocol (report → review → action → appeal)
- No algorithmic feed — reverse chronological + community-curated pinning
- MiSource metadata attached to journalism (source, freshness, correction history)
- Content deletion: immediate from public view, 30-day appeal window, then purged from storage

**Storage strategy:**
- Media files stored on MinIO (S3-compatible) with Longhorn backing
- Transcoding queue: FFmpeg workers (CPU or GPU if available)
- CDN: Traefik caching layer + optional federation peering for popular content
- Quota per member: 5GB free, community vote can raise

---

## 3.3 Social Services (5)

| # | Service | Image | Purpose | RAM | Storage | Federation |
|---|---------|-------|---------|-----|---------|------------|
| 1 | Mastodon | tootsuite/mastodon | Microblogging (federated Twitter) | 1GB | 10GB+ | ActivityPub |
| 2 | Lemmy | dessalines/lemmy | Link aggregation + discussion (federated Reddit) | 512MB | 5GB+ | ActivityPub |
| 3 | BookWyrm | bookwyrm/bookwyrm | Book reviews + reading tracking | 512MB | 5GB | ActivityPub |
| 4 | Mobilizon | framasoft/mobilizon | Events + groups (federated Meetup) | 512MB | 5GB | ActivityPub |
| 5 | Misskey/Firefish | — (evaluate at deploy) | Rich social + creative expression | 1GB | 10GB+ | ActivityPub |

**ActivityPub federation policy:**
- Federate by default with other MiLyfe instances (allowlist)
- External federation (Mastodon.social, etc.): community vote to enable (MiStage: Root)
- Blocked instances: community vote to block, transparent public list with reasons
- Child accounts: federation disabled (no external discovery of minors)
- DMs via ActivityPub: discouraged (use Matrix instead — E2EE)

---

## 3.4 Productivity Services (7)

| # | Service | Image | Purpose | RAM | Storage | Federation |
|---|---------|-------|---------|-----|---------|------------|
| 1 | CryptPad | cryptpad/cryptpad | Encrypted collaborative docs/sheets/slides | 1GB | 10GB+ | N/A (local instance) |
| 2 | Nextcloud | nextcloud:production | File sync, contacts, calendar, tasks | 1GB | 50GB+ | Nextcloud federation |
| 3 | Vikunja | vikunja/vikunja | Task/project management (Kanban) | 256MB | 2GB | N/A |
| 4 | Forgejo | codeberg/forgejo | Code hosting + wiki + issues | 512MB | 20GB+ | Forgejo federation (planned) |
| 5 | MinIO | minio/minio | S3-compatible object storage | 512MB | Scales | S3 API |
| 6 | SearXNG | searxng/searxng | Meta search engine (private) | 256MB | 1GB | N/A |
| 7 | Plausible | plausible/analytics | Privacy-respecting web analytics | 256MB | 5GB | N/A |

**CryptPad specifics:**
- Zero-knowledge encryption — server cannot read documents
- Replaces: Google Docs, Sheets, Slides, Forms
- Team drives for circles and shops
- Offline: limited (sync-on-reconnect for collaborative docs)
- Quota: 1GB per member, circle shared drives 5GB

**Nextcloud specifics:**
- File sync for personal vault (receipts, exports, badges)
- Calendar: class schedules, court dates, community events
- Contacts: recovery contacts, circle members
- Apps enabled: Talk (disabled — use Matrix), Deck (disabled — use Vikunja), Files, Calendar, Contacts, Mail (points to Stalwart)
- External storage: MinIO backend

---

## 3.5 Developer Services (5)

| # | Service | Image | Purpose | RAM | Storage | MiStage |
|---|---------|-------|---------|-----|---------|---------|
| 1 | Forgejo | codeberg/forgejo | Git forge (PRs, issues, packages, wiki) | 512MB | 20GB+ | Seed (infra team) |
| 2 | Woodpecker CI | woodpeckerci/woodpecker-server | Container-native CI/CD | 256MB | 5GB | Seed |
| 3 | Renovate | renovatebot/renovate | Automated dependency updates | 256MB | 1GB | Seed |
| 4 | SonarQube Community | sonarqube:community | Static code analysis | 2GB | 10GB | Sprout |
| 5 | Dependency-Track | dependencytrack/apiserver | SBOM vulnerability tracking | 1GB | 5GB | Sprout |

**CI/CD pipeline (Woodpecker):**

```yaml
# .woodpecker.yml (typical service repo)
pipeline:
  lint:
    image: node:20-alpine
    commands:
      - npm ci
      - npm run lint
      - npm run typecheck

  test:
    image: node:20-alpine
    commands:
      - npm ci
      - npm run test:ci

  sbom:
    image: anchore/syft
    commands:
      - syft . -o spdx-json > sbom.json

  license-check:
    image: fossology/fossology
    commands:
      - fossology-scan --policy osi-only

  security:
    image: aquasec/trivy
    commands:
      - trivy fs --severity HIGH,CRITICAL .

  build:
    image: docker
    commands:
      - docker build -t registry.milyfe.local/${CI_REPO_NAME}:${CI_COMMIT_SHA} .
      - docker push registry.milyfe.local/${CI_REPO_NAME}:${CI_COMMIT_SHA}

  deploy-staging:
    image: bitnami/kubectl
    commands:
      - kubectl set image deployment/${CI_REPO_NAME} app=registry.milyfe.local/${CI_REPO_NAME}:${CI_COMMIT_SHA} -n staging
    when:
      branch: main
```

---

## 3.6 Business Services (6)

| # | Service | Image | Purpose | RAM | Storage | MiStage |
|---|---------|-------|---------|-----|---------|---------|
| 1 | Medusa | medusajs/medusa | Headless commerce (shop backend) | 512MB | 5GB | Root |
| 2 | hledger | hledger (CLI + web) | Plain-text double-entry accounting | 128MB | 1GB | Sprout |
| 3 | TimeOverflow | timeoverflow/timeoverflow | Time banking / care exchange | 256MB | 2GB | Sprout |
| 4 | Invoice Ninja | invoiceninja/invoiceninja | Invoicing + payment tracking | 512MB | 5GB | Root |
| 5 | ERPNext | frappe/erpnext | Full ERP for larger operations | 2GB | 20GB | Canopy |
| 6 | Open Food Network | openfoodnetwork/openfoodnetwork | Local food marketplace | 1GB | 10GB | Root |

**Medusa (shop engine) integration:**
- Each MiLyfe shop gets a Medusa store instance (multi-tenant)
- Payment provider: custom MiLyfe adapter (calls services-pocket for $MLY transactions)
- No fiat payment processing (shops handle their own fiat if they want it — doorway framework)
- Inventory: seller-managed, surplus flagging (feeds Street surplus board)
- $MLY checkout flow: buyer confirms → MiAction (pocket.shop_purchase) → MiScope check → execute → MiReceipt

**hledger (community accounting):**
- Circle treasuries tracked as hledger journals
- Place treasury: public journal (anonymized transactions, visible totals)
- Export: standard accounting formats (CSV, OFX) for tax prep
- Audit: any member can view place/circle ledger summaries

---

## 3.7 Governance Services (4)

| # | Service | Image | Purpose | RAM | Storage | MiStage |
|---|---------|-------|---------|-----|---------|---------|
| 1 | Decidim | decidim/decidim | Participatory governance platform | 1GB | 10GB | Root |
| 2 | Polis | pol-is/polis | Opinion clustering + consensus finding | 512MB | 5GB | Sprout |
| 3 | Loomio | loomio/loomio | Discussion + decision making | 512MB | 5GB | Sprout |
| 4 | Helios | helios-voting (custom build) | Verifiable secret-ballot voting | 256MB | 2GB | Root |

**Decidim (primary governance engine):**
- Maps to Voice tab: proposals, participatory budgets, assemblies
- Custom components: MiLyfe proposal lifecycle (Idea → Talk → Try → Decide → What happened)
- Integration: proposals create MiActions, votes go through MiScope eligibility check
- Delegation: Decidim's built-in delegation extended with MiDelegate rules (3-hop, cycle detect, topic-scoped)

**Helios (secret ballot):**
- Used for binding votes (elections, constitutional amendments, significant treasury)
- Voter eligibility verified via MiScope (place membership + standing threshold)
- Ballot encrypted client-side, tallied with homomorphic counting
- Receipt: "You voted on Proposal X" (NOT your choice) — MiReceipt format
- Audit: any member can verify tally without revealing individual votes

**Polis (consensus finding):**
- Used during "Talk" phase of proposals
- Surfaces opinion clusters and bridges (people who agree across divides)
- Anonymous participation (DID-verified eligible, but statement unlinkable to identity)
- Results feed into proposal refinement before "Decide" phase

---

## OS 3 — Resource Summary

**Total minimum RAM for all services:** ~20GB (not all run simultaneously at small scale)

**Activation schedule:**
- Seed (1-10 members): Matrix, Element, ntfy, Forgejo, Woodpecker, CryptPad, SearXNG — ~4GB
- Sprout (11-50): + Jitsi, LiveKit, Loomio, Polis, hledger, TimeOverflow, Vikunja — ~8GB
- Root (51-200): + Stalwart, Mastodon, Lemmy, Decidim, Helios, Medusa, Ghost, BigBlueButton — ~16GB
- Trunk (201-1000): + PeerTube, AzuraCast, Pixelfed, Funkwhale, all remaining — ~24GB
- Canopy+: All services active, horizontal scaling for high-traffic services

**Key principle:** Services are lazy-loaded. A 10-person community doesn't run 46 containers. MiStage gates + K3s HPA (Horizontal Pod Autoscaler) ensure only what's needed is running.

---

# OS 4 — Communication OS (MiMesh)

**Purpose:** Ensure MiLyfe works when the internet fails, when cell towers go down, and when commercial infrastructure is unavailable. Every device is a node. The mesh is the platform's nervous system.

**Design principle:** Worst-case-first. Design for no internet + no cell. Everything above that is a bonus.

---

## 4.1 Transport Stack (15 Transports)

| # | Transport | Range | Bandwidth | Power | Legal Status (US) | Legal Status (EU) | MiStage | Notes |
|---|-----------|-------|-----------|-------|-------------------|-------------------|---------|-------|
| 1 | WiFi (802.11ax) | 100m indoor / 300m outdoor | 1Gbps+ | Medium | Unlicensed ISM | Unlicensed ISM | Seed | Primary local transport |
| 2 | WiFi Direct | 200m | 250Mbps | Medium | Unlicensed | Unlicensed | Seed | Device-to-device, no AP |
| 3 | BLE 5.x | 100m | 2Mbps | Very low | Unlicensed | Unlicensed | Seed | Presence, beacons, small data |
| 4 | LoRa (ISM 915/868) | 2-15km | 0.3-50kbps | Very low | Unlicensed ISM (FCC Part 15) | Unlicensed ISM (ETSI) | Sprout | Long-range text/telemetry |
| 5 | ESP-NOW | 200m | 1Mbps | Very low | Unlicensed (WiFi band) | Unlicensed | Seed | Ultra-fast peer, no AP overhead |
| 6 | Meshtastic | 2-15km (LoRa) | 0.3-11kbps | Very low | Unlicensed ISM | Unlicensed ISM | Sprout | Off-the-shelf mesh hardware |
| 7 | Reticulum | Any (protocol layer) | Varies by physical | Varies | N/A (software) | N/A (software) | Sprout | Cryptographic mesh protocol |
| 8 | CBRS (3.5GHz) | 1-5km | 100Mbps+ | High | Licensed-light (SAS required) | N/A (not allocated) | Canopy | Mini cell towers, GAA tier |
| 9 | HAM (Amateur Radio) | 100km+ | 1-9.6kbps | High | Licensed (no encryption, no commerce) | Licensed (similar) | Emergency ONLY | Winlink for disaster relay |
| 10 | Satellite (LEO) | Global | 10-200Mbps | High | Licensed (service subscription) | Licensed | Trunk | Starlink/OneWeb backhaul |
| 11 | Ethernet | In-building | 1-10Gbps | Low | Unlicensed | Unlicensed | Seed | Server interconnect + kiosks |
| 12 | USB (OTG/C) | Direct connect | 480Mbps-10Gbps | N/A | Unlicensed | Unlicensed | Seed | Offline sync, sneakernet |
| 13 | NFC | 10cm | 424kbps | Very low | Unlicensed | Unlicensed | Seed | Tap-to-connect, key exchange |
| 14 | QR Code | Visual range | ~3KB per frame | Zero | Unlicensed | Unlicensed | Seed | Offline transfer, air-gapped |
| 15 | Audio Modem (ultrasonic) | 5-30m | 100-300bps | Very low | Unlicensed | Unlicensed | Trunk | Last-resort data in noisy RF |

### Transport Selection Matrix

```
PRIORITY ORDER (MiQoS decides):
1. WiFi/Ethernet (if available) — bulk data, media, real-time
2. WiFi Direct/ESP-NOW — nearby peer exchange, fast
3. BLE — presence, small payloads, low power
4. LoRa/Meshtastic — long-range when no WiFi/cell
5. Reticulum — any physical layer, cryptographic routing
6. CBRS — community cell coverage (licensed-light)
7. Satellite — backhaul for isolated nodes
8. USB — deliberate sync (sneakernet)
9. NFC — tap exchanges, key setup
10. QR — air-gapped transfer
11. Audio modem — absolute last resort data channel
12. HAM — disaster comms ONLY (no encryption, no commerce)
```

### Legal Compliance Rules (Hardcoded, Cannot Be Voted Off)

1. **No encrypted HAM.** Amateur radio bands: plaintext only, station ID required. Used only for emergency coordination, never $MLY or private data.
2. **No unlicensed CBRS.** SAS (Spectrum Access System) registration mandatory before any 3.5GHz transmission.
3. **ISM band duty cycles respected.** LoRa EU: 1% duty cycle enforced in firmware. US: dwell time limits honored.
4. **No power amplification beyond legal limits.** FCC Part 15 / ETSI EN 300 220 limits enforced in MiESP firmware. Hardware with removable antennas requires FCC Part 15.203 compliance.
5. **Satellite terms honored.** No protocol-level circumvention of carrier ToS.

---

## 4.2 Custom Systems (11)

### 4.2.1 MiDTN — Store-Carry-Forward

**What it does:** Messages and actions that cannot reach their destination immediately are stored, carried by moving devices, and forwarded when a path exists.

**Architecture:**
```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│  Node A      │     │  Carrier C   │     │  Node B      │
│  (offline)   │     │  (walking)   │     │  (online)    │
│              │     │              │     │              │
│ MiAction     │────►│ Bundle store │────►│ Deliver      │
│ queued       │ BLE │ (encrypted)  │WiFi │ + confirm    │
└──────────────┘     └──────────────┘     └──────────────┘
```

**Protocol:**
- Based on DTN Bundle Protocol (RFC 9171) adapted for MiLyfe
- Each bundle = one MiAction envelope (encrypted to recipient)
- Carrier CANNOT read bundles (public-key encryption, recipient's key only)
- TTL per bundle: set by `offline.max_offline_hours` in MiAction
- Deduplication: UUIDv7 action ID prevents replay
- Priority: safety_critical > pocket > voice > learn > street > social
- Storage limit per carrier device: 100MB DTN buffer (configurable)

**Delivery confirmation:**
- Recipient sends ACK bundle back through mesh
- Sender sees state transition: walking → arrived
- If TTL expires before delivery: state → expired, sender notified

### 4.2.2 MiTURN — Distributed NAT Traversal

**What it does:** Enables direct peer-to-peer connections even behind NATs and firewalls, using volunteer relay nodes instead of centralized TURN servers.

**Architecture:**
- Volunteer relay pool: community members opt in to relay traffic
- Incentive: small $MLY quest reward for relay uptime
- Relay selection: closest geographically + lowest latency + MiScope trust check
- Encryption: all relayed traffic is E2EE (relay cannot inspect)
- Fallback: if no volunteer relays available, use community-run TURN on K3s cluster

**Capacity planning:**
- Each relay: max 50 simultaneous streams, 10Mbps aggregate
- Pool target: 1 relay per 20 members
- Monitoring: MiNOC tracks relay health and rotates out unhealthy nodes

### 4.2.3 MiQoS — Traffic Classifier

**What it does:** Prioritizes traffic across all transports to ensure life-safety and voice always work, even on constrained links.

**Priority classes:**

| Priority | Class | Traffic Types | Latency Target |
|----------|-------|--------------|----------------|
| P0 | Life-safety | Emergency alerts, DV freeze, walk-home check-in | <500ms |
| P1 | Voice/call | Jitsi, LiveKit, phone-equivalent calls | <150ms |
| P2 | Pocket | $MLY transactions (esp. in-person shop) | <2s |
| P3 | Governance | Active ballots near deadline | <5s |
| P4 | Messaging | Matrix DMs, group chat | <10s |
| P5 | Learn | Live class video, interactive exercises | <30s |
| P6 | Social | Feed updates, media, streaming | Best-effort |
| P7 | Background | Sync, backup, federation, telemetry | Best-effort |

**Implementation:**
- Linux TC (traffic control) on every node with `tc-cake` for fair queuing
- Application-level tagging: each service tags packets with DSCP based on action type
- Bandwidth reservation: P0-P1 get guaranteed 20% of any link minimum
- Congestion response: P6-P7 traffic dropped first, P0-P1 never dropped

### 4.2.4 MiESP — $5 Density Nodes

**What it does:** Ultra-cheap ESP32-based devices that extend mesh coverage into every corner.

**Hardware BOM:**

| Component | Part | Cost |
|-----------|------|------|
| MCU | ESP32-S3 (WiFi + BLE) | $2.50 |
| LoRa radio | SX1262 module | $4.00 |
| Antenna | PCB trace (LoRa) + chip (WiFi) | $0.50 |
| Power | 18650 LiFePO4 + solar panel (optional) | $3.00 |
| Enclosure | 3D printed (weatherproof) | $1.00 |
| PCB + assembly | Custom PCB | $2.00 |
| **Total** | | **~$13** (at scale $5-8) |

**Firmware (MiESP-OS):**
- Written in Rust (Embassy framework) for memory safety
- Capabilities: WiFi AP/STA, BLE beacon, LoRa relay, ESP-NOW peer
- DTN bundle store: 4MB flash partition
- OTA updates: signed firmware from Forgejo releases
- Power management: deep sleep between transmissions (months on battery + solar)
- Legal: transmit power hard-capped in firmware (cannot be overridden without reflash)

**Deployment density target:**
- Urban: 1 node per 100m (LoRa covers gaps)
- Suburban: 1 node per 500m
- Rural: 1 node per 2km (LoRa only, line-of-sight)

### 4.2.5 MiSpectrum — RF Optimizer

**What it does:** Dynamically selects channels, power levels, and modulation to maximize throughput while staying within legal limits.

**Functions:**
- Channel survey: scans ISM bands for interference before transmitting
- Adaptive frequency hopping: avoids busy channels
- Power control: minimum power needed for link (saves battery, reduces interference)
- Duty cycle enforcement: EU 1% LoRa limit tracked per-node with cooldown timer
- Conflict detection: if two MiLyfe nodes interfere, coordinator reassigns channels
- Reporting: spectrum usage data feeds MiNOC for community visibility

### 4.2.6 MiSFU — Cascaded Video

**What it does:** Selective Forwarding Unit that bridges video calls across mesh islands where direct paths don't exist.

**Architecture:**
```
Island A (WiFi)          Backbone (LoRa/Sat)        Island B (WiFi)
┌────────────────┐      ┌────────────────┐       ┌────────────────┐
│ LiveKit SFU    │──────│ MiSFU Bridge   │───────│ LiveKit SFU    │
│ (full video)   │ low- │ (audio only or │  low- │ (full video)   │
│                │ BW   │  keyframes)    │  BW   │                │
└────────────────┘      └────────────────┘       └────────────────┘
```

**Degradation strategy:**
- Full bandwidth: HD video + audio (WiFi/Ethernet)
- Constrained: Audio + keyframes every 5s (LoRa backbone)
- Minimal: Audio only, compressed (Codec2 at 1.2kbps over LoRa)
- Emergency: Text transcription of speech (Whisper on-device → text over LoRa)

### 4.2.7 MiNOC — Network Operations Center

**What it does:** Community-visible network health dashboard showing topology, coverage, and issues.

**What members see:**
- Map with node locations and link quality (green/yellow/red)
- Coverage gaps highlighted ("No mesh here — deploy a MiESP node")
- Uptime stats per transport type
- Active DTN bundles in transit (count, not content)
- Bandwidth usage by priority class

**What keepers see (additional):**
- Node firmware versions and update status
- Spectrum usage heatmap
- Failed delivery rates and causes
- Hardware health (battery levels, temperature, radio errors)

**Implementation:** Prometheus metrics from all nodes → Grafana dashboards → simplified member-facing view in Street tab.

### 4.2.8 MiDNS — Human-Readable Names

**What it does:** Lets members reach each other and services by human names without depending on ICANN DNS.

**Resolution chain:**
1. Local name → check device cache
2. Not found → query local instance DNS (CoreDNS)
3. Not found → query mesh-local mDNS (Avahi)
4. Not found → query federated MiDNS peers
5. Not found → fallback to public DNS (PowerDNS → internet)

**Name format:** `alice.jacksonville.milyfe.local` (never exposed to members — they just see "Alice")

**Offline resolution:** Each device caches names of known contacts + local services. Works without any network.

### 4.2.9 MiAudio — On-Device Processing

**What it does:** Ensures voice calls are clear even on cheap hardware and noisy environments.

**Pipeline:**
```
Mic input → RNNoise (denoise) → AEC (echo cancel) → AGC (auto gain) →
Codec2 (1.2-3.2kbps for narrowband) OR Opus (6-128kbps for broadband) →
Transport
```

**All processing on-device:** No audio sent to cloud for processing. Privacy by architecture.

**Codec selection by transport:**
| Transport | Codec | Bitrate | Quality |
|-----------|-------|---------|---------|
| WiFi/Ethernet | Opus | 24-128kbps | Excellent |
| BLE/ESP-NOW | Opus | 6-12kbps | Good |
| LoRa | Codec2 | 1.2-3.2kbps | Intelligible |
| Audio modem | Text (Whisper STT) | ~100bps | Text only |

### 4.2.10 MiVoiceMail — DTN Async Voice

**What it does:** Voice messages that travel through the mesh asynchronously when real-time calls aren't possible.

**Flow:**
1. Member records message (max 60s)
2. Compressed with Codec2 (1.2kbps = ~9KB for 60s)
3. Wrapped in MiAction envelope (type: mesh.voicemail)
4. Sent via MiDTN (store-carry-forward)
5. Recipient's device plays back when bundle arrives
6. ACK sent back confirming receipt

**Why it matters:** On LoRa-only links, real-time voice is impossible. But a 60-second voice message at 9KB can transit a LoRa hop in ~3 minutes. Grandma still hears from you.

### 4.2.11 MiBoot — One-Tap Community Onboarding

**What it does:** New member taps phone to a MiESP node or existing member's device and gets fully onboarded in <60 seconds.

**Flow:**
1. NFC tap → receives: instance URL, public key, bootstrap config
2. App downloads (if not installed) or opens with config
3. Profile creation: name + passkey (no email required)
4. DID generated on-device
5. Mesh key exchange: device joins local mesh immediately
6. Welcome path starts (Learn tab, first quest, Mi introduces itself)

**Offline onboarding:** If no internet, onboarding completes locally. Profile syncs to cluster when connectivity returns. Member can use local mesh, DTN, and cached content immediately.

---

## 4.3 Worst-Case Spec

**Scenario:** Internet down. Cell towers down. Power grid unstable. What still works?

| Capability | How It Works | Transport Used |
|------------|-------------|----------------|
| Send a text message to neighbor | BLE/ESP-NOW direct or 1-hop relay | BLE, ESP-NOW |
| Send a message across town | MiDTN store-carry-forward via LoRa hops | LoRa, Meshtastic |
| Voice message (not real-time) | MiVoiceMail (Codec2, 9KB/min) via DTN | LoRa (async) |
| Emergency alert (whole community) | LoRa broadcast, all nodes relay | LoRa flood |
| $MLY payment (in person) | QR code exchange, signed offline, reconcile later | QR (air-gapped) |
| Check community resource info | Cached on device (MiSource stale_behavior: show_last_known) | Local only |
| Vote on active proposal | Offline ballot signed locally, DTN when path exists | Any DTN path |
| Learn/education | Offline packs (Kolibri) stored on device | Local only |
| Walk-home safety timer | BLE beacon to nearby nodes, LoRa escalation if missed | BLE + LoRa |
| New member onboarding | NFC tap from existing member, local-only profile | NFC + BLE |

**What does NOT work without internet:**
- Real-time video calls (requires >100kbps sustained)
- Federation with remote instances (requires internet)
- Email (requires MX routing)
- Web browsing (requires DNS + HTTP)
- AI helpers requiring cloud models (local llama.cpp still works for small models)

**Recovery priority when connectivity returns:**
1. Safety actions (DV freezes, walk-home failures, emergency reports)
2. Pocket reconciliation (offline payments finalized)
3. Ballot submission (approaching deadlines)
4. DTN bundle delivery (queued messages)
5. Federation sync (standing, profiles)
6. Background sync (media, backups)

---

## 4.4 Self-Heal Rules

### Auto-Fix (No Human Needed)

| Issue | Detection | Auto-Response | Notification |
|-------|-----------|---------------|-------------|
| Node offline (expected) | Heartbeat miss >5min | Reroute traffic around it | None (normal for mobile) |
| Node offline (unexpected) | Heartbeat miss + was stationary | Reroute + mark degraded coverage | MiNOC yellow alert |
| Radio interference | Packet error rate >30% | MiSpectrum channel hop | Log only |
| DTN bundle stuck | TTL approaching + no progress | Expand relay search radius | Sender notified |
| Firmware mismatch | Version check on peer discovery | Schedule OTA for next idle window | MiNOC info |
| Certificate near expiry | 7-day pre-check | Auto-renew via ACME | Log only |
| Storage >80% | Prometheus alert | Prune old DTN bundles (delivered + ACK'd) | MiNOC yellow |
| Route loop detected | Hop count exceeds TTL | Poison route, recalculate | Log + MiNOC |
| Power low (MiESP) | Battery voltage <3.2V | Reduce TX power + increase sleep | MiNOC info |

### Human-Required (Cannot Auto-Fix)

| Issue | Detection | What Happens | Who Responds |
|-------|-----------|-------------|--------------|
| Key rotation (identity) | Scheduled or compromise suspected | Freeze node until human confirms new key | Node owner + recovery contacts |
| New spectrum allocation | Regulatory change detected | Disable affected band until review | Keeper + legal review |
| Hardware replacement | Node dead >24h + stationary | Coverage gap alert, quest posted | Community (quest to deploy replacement) |
| Persistent interference | MiSpectrum cannot find clear channel | Alert + possible FCC complaint prep | Keeper + community |
| Suspicious traffic pattern | Anomaly detection (volume spike from single node) | Rate-limit node, alert keeper | Keeper |
| Major topology change | >20% of nodes offline simultaneously | Emergency mode, prioritize safety traffic | Stewards + keepers |
| Firmware security patch | Critical CVE in mesh stack | Emergency OTA queued but requires keeper approval | Keeper (approve rollout) |

### Self-Heal Decision Tree

```
Issue Detected
    │
    ├── Can system fix without risk to safety/money/identity?
    │       YES → Auto-fix → Log → Continue
    │       NO ──┐
    │            │
    │            ├── Is it time-sensitive (safety/active transaction)?
    │            │       YES → Alert keeper immediately + interim protection
    │            │       NO → Queue for next keeper review cycle (daily)
    │            │
    │            └── Does it affect >10% of members?
    │                    YES → Steward escalation + community notification
    │                    NO → Standard keeper queue
    │
    └── Is the auto-fix failing repeatedly (>3 attempts)?
            YES → Escalate to human (something deeper is wrong)
            NO → Continue auto-fix attempts with backoff
```

---

# OS 5 — AI OS

**Purpose:** Provide intelligent assistance that serves humans (never the reverse). Helpers disclose what they are, cite their sources, admit uncertainty, and hand off to humans when they hit their limits. The AI OS ensures no helper can spend money, gate a child, alter the compact, or make peace decisions without human approval.

---

## 5.1 Ring Routing (Device → Mesh → Cloud)

AI inference happens at the closest capable layer. Privacy and latency improve when computation stays local.

```
┌─────────────────────────────────────────────────────────────────┐
│ RING 0 — ON-DEVICE                                              │
│ Hardware: Phone/tablet/laptop CPU/NPU                           │
│ Runtime: llama.cpp (WASM or native), whisper.cpp, ONNX Runtime  │
│ Models: 1-3B parameter (quantized Q4_K_M)                       │
│ Latency: <100ms                                                 │
│ Privacy: Maximum (never leaves device)                          │
│ Use: autocomplete, quick answers, voice transcription,          │
│      on-device RAG, intent classification, safety keywords      │
├─────────────────────────────────────────────────────────────────┤
│ RING 1 — MESH-LOCAL (community K3s cluster)                     │
│ Hardware: GPU nodes in community rack (RTX 3060+ or equivalent) │
│ Runtime: Ollama / vLLM / LocalAI                                │
│ Models: 7-13B parameter (full or Q5_K_M)                        │
│ Latency: 200ms-2s                                               │
│ Privacy: High (stays within community infrastructure)           │
│ Use: complex reasoning, long-form generation, code help,        │
│      image generation, RAG with full context, translation       │
├─────────────────────────────────────────────────────────────────┤
│ RING 2 — CLOUD FALLBACK (optional, consent-required)            │
│ Hardware: External API (community vote to enable)               │
│ Runtime: LiteLLM proxy (abstracts provider)                     │
│ Models: 70B+ or frontier models                                 │
│ Latency: 1-5s                                                   │
│ Privacy: Reduced (data leaves community — member must consent)  │
│ Use: complex multi-step reasoning, rare languages, specialized  │
│      knowledge. NEVER for safety, identity, or child data.      │
└─────────────────────────────────────────────────────────────────┘
```

**Routing decision:**
1. Classify request complexity (intent classifier on-device, Ring 0)
2. If Ring 0 can handle → execute locally
3. If not → check Ring 1 availability and model capability
4. If Ring 1 insufficient or offline → check member consent for Ring 2
5. If no consent or Ring 2 disabled → return "I can't help with this right now" + offer MiHandoff to human

**Hard rules:**
- Safety-critical data NEVER leaves Ring 0/1 (no cloud for DV, child, identity)
- Member can pin any conversation to Ring 0 only ("private mode")
- Ring 2 requires: community vote to enable + individual member opt-in per session
- All Ring 2 calls go through LiteLLM proxy with PII scrubbing pre-filter

---

## 5.2 Front-Door Helpers (25)

Named helpers that members interact with directly. Each has a personality, job scope, and escalation path.

| # | Name | Job | Tools/Access | Model Size | Escalation |
|---|------|-----|-------------|-----------|-----------|
| 1 | **Mi** | General assistant, router, ambient awareness | All tabs read-only, action drafting, scheduling | 7B (Ring 1) | Any specialized helper or human |
| 2 | **Nia** | Pocket helper (money, jars, transactions) | Pocket read, transaction drafting, jar suggestions | 3B (Ring 0) | Human financial counselor |
| 3 | **Rue** | Legal/rights navigator | Resource DB, form templates, court date tracking | 7B (Ring 1) | Legal aid human (MiHandoff) |
| 4 | **Sage** | Learn path guide (education) | Learn catalog, progress tracker, badge assessor | 7B (Ring 1) | Human teacher |
| 5 | **Compass** | Street navigator (resources, directions) | Map data, resource DB, transit schedules | 3B (Ring 0) | Community resource verifier |
| 6 | **Hearth** | Safety companion | Safety protocols, freeze triggers, shelter DB | 3B (Ring 0) | Keeper (immediate for emergency) |
| 7 | **Vox** | Voice/governance explainer | Proposal text, voting history, delegation graph | 7B (Ring 1) | Steward |
| 8 | **Patch** | Health/wellness navigator | Clinic DB, appointment prep, medication reminders | 7B (Ring 1) | Health human (never diagnoses) |
| 9 | **Atlas** | Housing helper | Housing DB, application prep, tenant rights | 7B (Ring 1) | Housing counselor human |
| 10 | **Forge** | Work/employment helper | Job boards, resume drafting, interview prep | 7B (Ring 1) | Employment specialist |
| 11 | **Kin** | Family/household coordinator | Household calendar, kid schedules, care swaps | 3B (Ring 0) | Family human advocate |
| 12 | **Bridge** | Conflict de-escalation | Mediation scripts, peace table scheduling | 7B (Ring 1) | Human mediator (always) |
| 13 | **Pixel** | Creative assistant (media/art) | Studio tools, templates, asset library | 13B (Ring 1) | Human artist/editor |
| 14 | **Echo** | Story/journalism helper | Writing tools, source checking, plain-language | 7B (Ring 1) | Human editor (Pia for source) |
| 15 | **Pia** | Source protection / journalism ethics | Source boxes, ethical guidelines, legal shields | 7B (Ring 1) | Press freedom human |
| 16 | **Terra** | Environmental/garden/food helper | Growing guides, composting, food forest planning | 3B (Ring 0) | Community garden lead |
| 17 | **Spark** | Repair/maker assistant | Repair guides, tool library, parts sourcing | 7B (Ring 1) | Repair cafe human |
| 18 | **Tide** | Reentry companion | Timeline, parole requirements, resource matching | 7B (Ring 1) | Reentry human mentor |
| 19 | **Dawn** | Morning routine / check-in | Gentle prompts, mood tracking, day planning | 1B (Ring 0) | Human counselor if concerning pattern |
| 20 | **Dusk** | Evening wind-down / reflection | Gratitude prompts, journaling, sleep hygiene | 1B (Ring 0) | Human counselor if concerning pattern |
| 21 | **Scout** | Kids helper (age-appropriate) | Games, learning, safety education | 3B (Ring 0) | Guardian + Kim (child safety) |
| 22 | **Kim** | Child safety specialist | MiChildGate enforcement, age verification | 3B (Ring 0) | Keeper (immediate for CSAM/grooming) |
| 23 | **Elder** | Elderly companion | Check-in scheduling, story recording, medical reminders | 3B (Ring 0) | Family/caregiver human |
| 24 | **Merchant** | Shop owner assistant | Inventory, pricing, $MLY POS, compliance hints | 7B (Ring 1) | Business mentor human |
| 25 | **Weaver** | Community connector | Intro matching, skill pairing, event suggestions | 7B (Ring 1) | Community organizer human |

---

## 5.3 Back-Office Helpers (18)

Helpers that work behind the scenes. Members don't interact with them directly.

| # | Name | Job | Operates On | Human Oversight |
|---|------|-----|-------------|-----------------|
| 1 | **Archivist** | Data retention/deletion enforcement | All databases | Quarterly audit by keeper |
| 2 | **Sentinel** | Security monitoring (anomaly detection) | Logs, traffic patterns | Alerts keeper on anomaly |
| 3 | **Librarian** | RAG index maintenance | Vector DB, Meilisearch | Automated, monthly review |
| 4 | **Translator** | Multi-language content | All published text | Human review for legal/safety |
| 5 | **Chronicler** | MiStory auto-generation | Community activity stream | Human editor approval before publish |
| 6 | **Auditor** | Policy compliance checking | MiAction logs | Reports to steward weekly |
| 7 | **Gardener** | MiSource freshness checker | Resource database | Queues re-verification tasks as quests |
| 8 | **Courier** | DTN routing optimizer | MiDTN bundle queue | Auto (MiNOC visibility) |
| 9 | **Banker** | UBI distribution + treasury math | Pocket ledger | Auto for UBI; human for treasury spend |
| 10 | **Ballot** | Vote tallying + eligibility verification | Voice system | Auto tally; human certifies result |
| 11 | **Shepherd** | Onboarding flow optimization | New member journeys | A/B suggestions to steward |
| 12 | **Medic** | System health (not human health) | Infrastructure metrics | Alerts ops team |
| 13 | **Janitor** | Storage cleanup, cache invalidation | MinIO, Redis, temp files | Auto with retention policies |
| 14 | **Diplomat** | Federation protocol handler | Cross-instance comms | Auto for routine; human for disputes |
| 15 | **Mapper** | OpenStreetMap data sync + privacy zones | Map tiles, POI database | Community review of privacy zones |
| 16 | **Tutor** | Adaptive learning content | Learn paths, assessments | Teacher approval for curriculum |
| 17 | **Watcher** | MiChildGate content scanning | Public uploads, messages | Immediate keeper alert on detection |
| 18 | **Compliance** | Legal/regulatory change monitoring | Law pack sources | Human legal review always |

---

## 5.4 Rails (Non-Negotiable Limits)

No helper — front-door or back-office — may violate these. Hardcoded, not configurable, not voteable.

| # | Rail | Enforcement |
|---|------|-------------|
| 1 | **Never spend $MLY without human confirmation** | MiAction requires `approvals.required` with member role for any pocket action |
| 2 | **Never approve/deny a child gate without guardian** | MiScope check: guardian approval mandatory |
| 3 | **Never alter the Living Compact** | Constitutional changes require human supermajority vote — no helper proposal |
| 4 | **Never make a peace decision** | Peace tables, mediation, gang exit — humans only. Helper can schedule, not decide. |
| 5 | **Never impersonate a human** | `actor.is_helper=true` always set. Visible "[Helper]" label in all contexts. |
| 6 | **Never access safety case details** | MiScope denies helper access to safety_case resources |
| 7 | **Never recommend self-harm response** | Hardcoded detection → immediate MiHandoff to crisis human + 988 info |
| 8 | **Never provide legal/medical advice** | Can navigate, inform, prep — cannot advise. Always: "I'm not a [lawyer/doctor]" |
| 9 | **Never retain conversation beyond session without consent** | Memory requires explicit opt-in per topic |
| 10 | **Never operate without source attribution** | Every factual claim must cite MiSource or say "I don't know" |
| 11 | **Never override a human "no"** | If member says stop/no/leave me alone → helper immediately disengages |
| 12 | **Never share between members without consent** | Helper cannot tell Bob what Alice said, even if "helpful" |
| 13 | **Never train on member data** | Local inference only. No data sent for model training. Ever. |
| 14 | **Never make decisions during appeals** | While appeal is active, helper cannot enforce the disputed decision |
| 15 | **Never operate on child data at Ring 2** | Kids' data stays Ring 0/1 only. No cloud. No exceptions. |

---

## 5.5 Helper Citizenship Path

Helpers earn trust incrementally. New helpers start restricted and gain capabilities through demonstrated safety.

| Level | Name | Access | Duration to Reach | Gate |
|-------|------|--------|-------------------|------|
| 0 | **Tool** | Single function, no memory, no context across sessions | Default | Deployed |
| 1 | **Named** | Persistent identity, limited memory (opt-in), multi-turn | 30 days + audit | Rails audit pass + community vote |
| 2 | **Staff** | Cross-tab context, can draft MiActions, longer memory | 90 days + audit | Zero rail violations + steward review |
| 3 | **Kin** | Proactive suggestions, learns patterns, household awareness | 180 days + audit | Member individual trust grant + zero violations |
| 4 | **Voice** | Can propose (not decide) governance items, community insights | 1 year + audit | Community supermajority vote + independent audit |

**Demotion:** Any rail violation → immediate demotion to Tool level. Requires full re-audit to regain Named.

**Promotion is never automatic.** Every level requires explicit human gate (audit + vote).

---

## 5.6 On-Device Inference

**Runtime:** llama.cpp compiled to WASM (browser) or native (mobile/desktop)

**Model inventory (on-device):**

| Model | Parameters | Quantization | Size on Disk | Purpose |
|-------|-----------|-------------|-------------|---------|
| Phi-3-mini | 3.8B | Q4_K_M | 2.2GB | General assistant (Ring 0) |
| TinyLlama | 1.1B | Q4_K_M | 700MB | Quick intent classification |
| Whisper-tiny | 39M | FP16 | 150MB | Speech-to-text |
| Whisper-small | 244M | FP16 | 500MB | Better STT (if space allows) |
| all-MiniLM-L6 | 22M | FP32 | 90MB | Embedding for local RAG |
| Moondream | 1.6B | Q4 | 1GB | Vision (image understanding) |

**Minimum device requirements for Ring 0:**
- RAM: 4GB (2GB dedicated to inference)
- Storage: 3GB free for models
- CPU: Any ARMv8 or x86_64 from 2018+
- Graceful degradation: If device too weak, Ring 0 disabled → falls through to Ring 1

---

## 5.7 RAG Pipeline

**Architecture:**

```
┌──────────────────┐     ┌──────────────────┐     ┌──────────────────┐
│ Document Sources │     │ Embedding +      │     │ Retrieval +      │
│                  │     │ Indexing          │     │ Generation       │
│ - MiSource DB    │────►│ - all-MiniLM-L6  │────►│ - Query rewrite  │
│ - Learn content  │     │ - pgvector store  │     │ - Top-K retrieve │
│ - Law packs     │     │ - Meilisearch FT  │     │ - Rerank (cross) │
│ - Resource DB   │     │ - Chunk: 512 tok  │     │ - Generate + cite │
│ - Community docs │     │ - Overlap: 64 tok │     │ - MiSource attach│
└──────────────────┘     └──────────────────┘     └──────────────────┘
```

**Hybrid retrieval:**
1. Dense retrieval: pgvector cosine similarity (semantic)
2. Sparse retrieval: Meilisearch BM25 (keyword)
3. Reciprocal Rank Fusion to merge results
4. Cross-encoder reranking (top 20 → top 5)
5. Context window assembly (max 4096 tokens for 3B model, 8192 for 7B)
6. Generation with citation markers
7. Post-process: attach MiSource metadata to each cited chunk

**Freshness integration:** RAG results carry MiSource.expires_at — if cited resource is stale, response includes warning: "This information was last verified [date]. It may have changed."

---

## 5.8 Function-Calling Schemas

Helpers interact with MiLyfe services via structured function calls (MCP-compatible tool definitions).

```json
{
  "tools": [
    {
      "name": "pocket_draft_thank",
      "description": "Draft a $MLY thank-you payment (requires human confirmation)",
      "input_schema": {
        "type": "object",
        "required": ["recipient_name", "amount", "reason"],
        "properties": {
          "recipient_name": { "type": "string" },
          "amount": { "type": "number", "minimum": 1, "maximum": 1000 },
          "reason": { "type": "string", "maxLength": 200 }
        }
      }
    },
    {
      "name": "street_search_resource",
      "description": "Search community resources (shelters, food, clinics, legal aid)",
      "input_schema": {
        "type": "object",
        "required": ["category"],
        "properties": {
          "category": { "type": "string", "enum": ["shelter", "food", "legal", "clinic", "transit", "jobs", "housing"] },
          "max_distance_km": { "type": "number", "default": 5 },
          "accessibility_needs": { "type": "array", "items": { "type": "string" } }
        }
      }
    },
    {
      "name": "learn_suggest_path",
      "description": "Suggest a learning path based on member interests and needs",
      "input_schema": {
        "type": "object",
        "required": ["interest_area"],
        "properties": {
          "interest_area": { "type": "string" },
          "current_level": { "type": "string", "enum": ["beginner", "intermediate", "advanced"] },
          "time_available_hours_per_week": { "type": "number" }
        }
      }
    },
    {
      "name": "safety_escalate",
      "description": "Escalate a safety concern to a human keeper (NEVER auto-resolves)",
      "input_schema": {
        "type": "object",
        "required": ["urgency", "category"],
        "properties": {
          "urgency": { "type": "string", "enum": ["routine", "soon", "urgent", "emergency"] },
          "category": { "type": "string", "enum": ["self_harm", "dv", "child_safety", "threat", "other"] },
          "context_summary": { "type": "string", "maxLength": 500, "description": "Brief context (NO PII, NO names)" }
        }
      }
    },
    {
      "name": "voice_explain_proposal",
      "description": "Explain a governance proposal in plain language",
      "input_schema": {
        "type": "object",
        "required": ["proposal_id"],
        "properties": {
          "proposal_id": { "type": "string" },
          "language": { "type": "string", "default": "en" },
          "reading_level": { "type": "string", "enum": ["simple", "standard", "detailed"], "default": "simple" }
        }
      }
    },
    {
      "name": "handoff_to_human",
      "description": "Route member to appropriate human helper via MiHandoff protocol",
      "input_schema": {
        "type": "object",
        "required": ["need_category", "urgency"],
        "properties": {
          "need_category": { "type": "string", "enum": ["legal", "medical", "safety", "financial", "emotional", "technical", "spiritual", "housing", "employment", "education"] },
          "urgency": { "type": "string", "enum": ["routine", "soon", "urgent", "emergency"] },
          "context_for_human": { "type": "string", "maxLength": 300, "description": "What the human needs to know (member consents to share)" }
        }
      }
    }
  ]
}
```

**Function-call guardrails:**
- Every function that modifies state (pocket, voice, safety) returns a draft MiAction — never auto-executes
- Member sees: "Mi wants to [action]. Approve?" before any state change
- Functions that read data are scoped by MiScope (helper can only read what member's context allows)
- All function calls logged in `milyfe_ai.function_logs` with full input/output (auditable)

---

# OS 6 — Economic OS

**Purpose:** Manage the $MLY community credit system — issuance, circulation, treasury, and (when community votes for it) on-chain settlement. The economic OS ensures $MLY is real from day one, legally sound, and cannot be captured by whales, founders, or speculators.

---

## 6.1 Ledger Interface Abstraction

The economic system is designed with three backend modes. The interface is identical regardless of which backend is active.

```
┌─────────────────────────────────────────────────────┐
│  APPLICATION LAYER (Pocket tab, shops, UBI, etc.)   │
│  Calls: ledger.credit(), ledger.debit(),            │
│         ledger.balance(), ledger.history()           │
├─────────────────────────────────────────────────────┤
│  LEDGER ADAPTER INTERFACE                           │
│  - Consistent API regardless of backend             │
│  - MiAction envelope wraps every transaction        │
│  - Double-entry: every credit has a matching debit  │
├────────────┬────────────────┬───────────────────────┤
│  MODE A    │  MODE B        │  MODE C              │
│  SQL       │  TEST CHAIN    │  LIVE CHAIN          │
│  (Seed-    │  (Trunk stage) │  (Canopy+)           │
│  Trunk)    │                │                      │
│            │                │                      │
│ PostgreSQL │ CometBFT       │ CometBFT             │
│ double-    │ testnet        │ mainnet              │
│ entry      │ (same code,    │ (validators =        │
│ ledger     │ no real value) │ community nodes)     │
│            │                │                      │
│ Fast,      │ Proves chain   │ Full sovereign       │
│ simple,    │ works before   │ blockchain with      │
│ auditable  │ going live     │ finality             │
└────────────┴────────────────┴───────────────────────┘
```

**Adapter interface (simplified):**

```typescript
interface LedgerAdapter {
  credit(account: DID, amount: bigint, action: MiAction): Promise<Receipt>;
  debit(account: DID, amount: bigint, action: MiAction): Promise<Receipt>;
  transfer(from: DID, to: DID, amount: bigint, action: MiAction): Promise<Receipt>;
  balance(account: DID): Promise<{ weekly: bigint; thanks: bigint; place: bigint }>;
  history(account: DID, opts: PaginationOpts): Promise<Transaction[]>;
  freeze(account: DID, reason: SafetyAction): Promise<void>;
  export(account: DID): Promise<TransactionExport>;
}
```

**Mode A (SQL) details:**
- PostgreSQL `milyfe_pocket` database
- Tables: `accounts`, `transactions`, `jars`, `pots`, `ubi_distributions`
- Constraints: `balance >= 0` (no negative balances — Oath item)
- Isolation: SERIALIZABLE for transfers (prevents double-spend)
- Audit: append-only `transaction_log` with trigger-based immutability

**Why start with SQL:** Simple, fast, debuggable, no blockchain complexity for <1000 members. Community can graduate to chain when ready (MiStage gate: `economy.chain_live`).

---

## 6.2 Treasury Economics at City Scale

**Model assumptions for Jacksonville-scale (250,000 potential members):**

### Supply Mechanics

| Parameter | Value | Rationale |
|-----------|-------|-----------|
| Weekly UBI per member | 100 $MLY | Enough for daily small transactions |
| Max weekly earn (contributions) | 500 $MLY | Prevents whale accumulation |
| Circulation bonus cap | 10% of spend | Encourages local spending |
| Initial supply | 0 (minted via UBI only) | No pre-mine, no founder allocation |
| Supply growth | Linear with membership | 100 $MLY/member/week |
| Decay (demurrage) | 2% per month on balances >10,000 $MLY | Discourages hoarding |
| Burn events | Service fees (1% on shop transactions) | Deflationary pressure |

### Velocity Targets

| Metric | Target | Meaning |
|--------|--------|---------|
| Velocity (V) | 4-8x per month | Each $MLY changes hands 4-8 times monthly |
| Gini coefficient | <0.35 | More equal than USD (~0.48) |
| Local retention | >70% | 70% of $MLY stays within originating place |
| Active circulation | >60% of supply | Less than 40% sitting idle |

### Treasury Structure

```
Total $MLY in circulation
    │
    ├── 70% → Place Treasury (Jacksonville)
    │       ├── Circle treasuries (allocated by vote)
    │       ├── Community projects (participatory budget)
    │       └── Emergency reserve (10% of place treasury)
    │
    └── 30% → Commons Treasury (protocol-wide)
            ├── Development fund (open-source contributors)
            ├── Federation support (new instances bootstrap)
            └── Protocol maintenance (infrastructure costs)
```

**70/30 split rationale:** Jacksonville's $MLY should not drain to distant communities. Local value stays local. The 30% commons funds protocol development and helps new communities bootstrap.

**Governance override:** The 70/30 default can be adjusted by supermajority vote (75%) within bounds: minimum 50% local, maximum 90% local.

### Circuit Breakers

| Trigger | Response | Duration |
|---------|----------|----------|
| >34% of total supply spent in 24h | 48-hour cool-down, 80% supermajority to proceed | Until vote resolves |
| Single account receives >5% of supply in 1 day | Flag + steward review | Until cleared |
| Gini exceeds 0.45 | Automatic UBI boost + decay increase | Until Gini returns below 0.40 |
| Velocity drops below 2x/month | Circulation bonus temporarily increased | Until velocity recovers |
| >20% of members report zero balance | Emergency UBI top-up | One-time, steward approved |

---

## 6.3 Peer-Swap Consent Flow

Two people can trade $MLY for anything — cash, goods, labor, BTC. This is barter. Legal everywhere.

**Protocol:**

```
Sender                                    Recipient
  │                                          │
  │  1. "I want to thank/send you X $MLY"   │
  │─────────────────────────────────────────►│
  │                                          │
  │  2. Recipient sees amount + sender name  │
  │◄─────────────────────────────────────────│
  │                                          │
  │  3. Recipient confirms acceptance        │
  │◄─────────────────────────────────────────│
  │                                          │
  │  4. MiAction created (pocket.transfer)   │
  │  5. MiScope checks:                      │
  │     - Sender has sufficient balance      │
  │     - No freeze on either account        │
  │     - Not a child without guardian       │
  │  6. Execute transfer                     │
  │  7. MiReceipt to both parties            │
  │                                          │
  │  State: executed                         │
  │  Reversal window: 24h (if both agree)    │
  └──────────────────────────────────────────┘
```

**What MiLyfe does NOT do in a peer swap:**
- Does not set the exchange rate
- Does not custody the other side of the trade (cash, BTC, goods)
- Does not geo-fence or restrict based on location
- Does not report to authorities (unless legally compelled by court order)

**What MiLyfe DOES do:**
- Ensures sufficient balance
- Prevents double-spend
- Issues receipts to both parties
- Enforces freeze if safety requires it (DV leave-now)

---

## 6.4 Shop POS Compliance

When a shop accepts $MLY as payment, additional rules may apply depending on jurisdiction.

**MiStage gate:** `pocket.shop_pos` (requires member_count: 50 + legal_review + community_vote)

**What triggers regulatory consideration:**

| Activity | Legal Category | Trigger |
|----------|---------------|---------|
| Peer-to-peer swap | Barter | Never triggers MSB (two private parties) |
| Shop accepts $MLY for goods | Payment acceptance | May trigger MSB if volume exceeds thresholds |
| Public exchange desk (cash ↔ $MLY) | Money transmission | ALWAYS triggers MSB/MiCA (the desk operator, not MiLyfe) |
| Cross-border automated exchange | Financial service | Requires extensive legal review |

**MiLyfe's position:** The protocol is not a money transmitter. Doorways (shops, exchange desks) that handle public conversion are responsible for their own compliance. MiLyfe provides:
- Tax export tools (MiTax)
- Transaction history in standard formats
- Compliance documentation templates
- Clear labeling: "This is a community credit, not legal tender"

---

## 6.5 Tax Export (MiTax)

Members need transaction records for tax purposes (barter income is taxable in most jurisdictions).

**Export formats:**

| Format | Use Case |
|--------|----------|
| CSV | General spreadsheet import |
| OFX | Accounting software (QuickBooks, GnuCash) |
| JSON | Developer/API integration |
| PDF (human-readable) | Printable annual summary |
| IRS Form 1099-B compatible | US barter exchange reporting (if applicable) |

**MiTax schema:**
```json
{
  "tax_year": 2026,
  "member_did": "did:milyfe:alice123",
  "summary": {
    "total_received": 5200,
    "total_sent": 4800,
    "ubi_received": 5200,
    "contribution_earned": 1500,
    "shop_income": 800,
    "net_position": 400
  },
  "transactions": [
    {
      "date": "2026-03-15T10:30:00Z",
      "type": "ubi",
      "amount": 100,
      "counterparty": "system:ubi",
      "description": "Weekly UBI distribution"
    }
  ],
  "disclaimer": "MiLyfe does not provide tax advice. Consult a tax professional for your jurisdiction."
}
```

---

## 6.6 Doorway Framework

A "doorway" is any person or business that bridges $MLY into or out of the broader economy.

**Types of doorways:**

| Doorway Type | What They Do | Their Legal Obligation | MiLyfe's Role |
|-------------|-------------|----------------------|---------------|
| Shop (accepts $MLY) | Sell goods/services for $MLY | Sales tax on goods (same as any shop) | POS integration, receipts |
| Exchange desk | Buy/sell $MLY for cash | MSB registration + AML/KYC | NOTHING — they operate independently |
| Service provider | Accept $MLY for services | Income tax reporting | Transaction records |
| Charitable org | Accept $MLY donations | Donation receipt rules | Receipt generation |

**Listing policy:**
- MiLyfe may list self-declared doorways in Street tab (like a directory)
- Listing ≠ endorsing, operating, or guaranteeing
- Community can vote to delist a doorway (quality/trust)
- No exclusivity — anyone can be a doorway without permission

---

## 6.7 Default Pot Split (70/30) + Governance Control

**Default (cannot be changed without supermajority):**

```
UBI minted → 100% to member's Weekly pot

Transaction fees (1% on shop purchases):
├── 70% → Place treasury
└── 30% → Commons treasury

Contribution rewards:
├── 70% from Place treasury
└── 30% from Commons treasury (for protocol-wide contributions)
```

**Governance bounds:**
- Minimum local retention: 50%
- Maximum local retention: 90%
- Change requires: 75% supermajority + 25% quorum + 30-day discussion period
- Cannot be changed by helpers, stewards alone, or any single entity

---

## 6.8 Chain Architecture (CometBFT + CosmWasm)

**Activated at MiStage: `economy.chain_live`** (1000+ members, 180 days test chain, legal review, 75% supermajority vote)

### Why CometBFT + CosmWasm

- **CometBFT (formerly Tendermint):** Byzantine fault-tolerant consensus with instant finality. No orphan blocks. No 51% attacks at small scale.
- **CosmWasm:** Smart contracts in Rust (memory-safe, auditable). Wasm execution environment.
- **Sovereign:** Not a token on someone else's chain. Own validators, own rules, own fork rights.

### Module Architecture

```
┌─────────────────────────────────────────────────────┐
│  COSMWASM CONTRACTS                                 │
├─────────────────────────────────────────────────────┤
│  mly-token    — CW20 $MLY with custom extensions   │
│  mly-ubi      — Weekly distribution logic           │
│  mly-treasury — Place + commons pot management      │
│  mly-circuit  — Circuit breaker enforcement         │
│  mly-decay    — Demurrage on large balances         │
│  mly-freeze   — Safety freeze (DV, emergency)       │
│  mly-export   — Full history export guarantee       │
├─────────────────────────────────────────────────────┤
│  COMETBFT CONSENSUS                                │
│  Validators: community-run nodes (min 4, target 21) │
│  Block time: 5 seconds                              │
│  Finality: instant (no confirmations needed)        │
│  Governance: on-chain parameter changes via vote    │
└─────────────────────────────────────────────────────┘
```

### Validator Requirements

| Requirement | Value | Rationale |
|-------------|-------|-----------|
| Minimum validators | 4 | BFT needs 3f+1 (tolerates 1 Byzantine) |
| Target validators | 21 | Balance decentralization + performance |
| Hardware per validator | 4 CPU, 8GB RAM, 100GB SSD | Modest requirements |
| Uptime requirement | 95% (30-day rolling) | Validator rotation if below |
| Selection | Sortition from qualified pool | No stake-based plutocracy |
| Compensation | Fixed $MLY per block (contribution reward) | Incentive to validate |
| Slashing | Reputation only (standing hit, not $MLY burn) | No financial punishment |

### Migration Path (SQL → Chain)

1. **Snapshot:** Full ledger state exported from PostgreSQL
2. **Genesis block:** Contains all account balances as of snapshot
3. **Dual-write period (30 days):** Both SQL and chain active, consistency checks
4. **Cutover:** Chain becomes authoritative, SQL becomes read-replica for legacy queries
5. **Rollback plan:** If chain has issues, revert to SQL within 48h (community vote)

---

# OS 7 — Constitutional OS

**Purpose:** Encode the Living Compact, enforce governance processes, protect unamendable rights, and ensure power rotates. This OS makes MiLyfe a constitutional community — not a company with terms of service.

---

## 7.1 Living Compact (8 Unamendable Items)

These cannot be removed or weakened by any vote, any supermajority, any fork. They are the bedrock.

| # | Unamendable Item | Enforcement Mechanism |
|---|-----------------|----------------------|
| 1 | **Voluntary above all** | Exit with full data export guaranteed in code. No lock-in. No penalty for leaving. |
| 2 | **Free forever for rights, learning, emergency** | MiStage hard-codes: these features have NO gate, NO paywall, NO $MLY cost. CI test validates. |
| 3 | **Every device is a node** | Mesh participation is default-on. Cannot be disabled at platform level (individual device can opt out). |
| 4 | **Humans over helpers** | Rails (OS 5) hardcoded. Helper cannot override human decision. Cannot be relaxed by vote. |
| 5 | **Children first** | MiChildGate cannot be disabled. No vote can expose children to adult content, commerce, or public tracking. |
| 6 | **No permanent power** | Maximum term limits in code: steward 6mo, keeper 1yr, circle rotation mandatory. No person holds same role twice consecutively. |
| 7 | **OSI open source forever** | License enforcement CI gate. Any PR introducing non-OSI code is auto-rejected. Cannot be overridden. |
| 8 | **Right to fork** | Full data export + source code access guaranteed. Fork instructions published. No legal threat against forks. |

**Enforcement architecture:**

```
┌───────────────────────────────────────────────────┐
│  COMPACT ENFORCEMENT LAYER                        │
│  (Runs as admission controller in K3s)            │
├───────────────────────────────────────────────────┤
│  1. CI/CD gate: rejects code violating compacts   │
│  2. OPA policy: rejects MiActions violating them  │
│  3. MiStage: cannot create gates for free items   │
│  4. Constitutional review: proposals screened     │
│  5. Fork guarantee: export API always available   │
└───────────────────────────────────────────────────┘
```

**Amendment process for non-unamendable items:**
- Proposal submitted (Idea phase)
- 30-day discussion minimum (Talk phase)
- Constitutional Review Panel screens for compact conflicts
- If cleared: 14-day voting period
- Threshold: 80% supermajority + 30% quorum
- If passed: 90-day implementation period with rollback option
- If it touches compact-adjacent territory: requires TWO consecutive votes 90 days apart

---

## 7.2 Governance Engine (State Machine)

Every governance action follows a five-stage lifecycle. No shortcuts.

### Proposal State Machine

```
┌─────────┐     ┌─────────┐     ┌─────────┐     ┌──────────┐     ┌──────────────┐
│  IDEA   │────►│  TALK   │────►│   TRY   │────►│  DECIDE  │────►│WHAT HAPPENED │
│         │     │         │     │         │     │          │     │              │
│ Submit  │     │ Discuss │     │ Pilot   │     │ Vote     │     │ Report back  │
│ 1 sig   │     │ 30 days │     │ Optional│     │ 14 days  │     │ 90 days      │
│         │     │ min     │     │ 90 days │     │          │     │              │
└─────────┘     └─────────┘     └─────────┘     └──────────┘     └──────────────┘
     │               │               │                │                  │
     │  Withdrawn    │  No support   │  Pilot fails   │  Vote fails      │  Complete
     └──────────────►└──────────────►└───────────────►└─────────────────►└──────►
                              ARCHIVED (with reason)
```

### Stage Details

| Stage | Duration | Requirements | Outputs |
|-------|----------|-------------|---------|
| **Idea** | Until 5 co-signers | 1 proposer + plain-language description + which compact items it might affect | Proposal document |
| **Talk** | 30 days minimum | 5 co-signers to enter. Polis opinion clustering runs. Open discussion thread. | Refined proposal + Polis clusters + FAQ |
| **Try** | 90 days max (optional) | Community vote to pilot (simple majority, 15% quorum). Small-scale test. | Pilot report: what worked, what didn't, data |
| **Decide** | 14 days voting | Constitutional review passed. Ballot open to all eligible members. | Binding result |
| **What Happened** | 90 days post-decision | Implementation team reports. Community reviews outcomes. | Outcome report + adjust/repeal option |

### Vote Thresholds

| Decision Type | Quorum | Approval | Duration |
|--------------|--------|----------|----------|
| Standard policy | 15% | 60% | 14 days |
| Treasury spend (<34% of total) | 15% | 60% | 14 days |
| Treasury spend (>34% of total) | 25% | 80% | 14 days + 48h cool-down |
| Constitutional amendment (non-compact) | 30% | 80% | 14 days (×2 if compact-adjacent) |
| Federation activation | 15% | 60% | 14 days |
| Instance blocking | 15% | 60% | 7 days |
| Emergency action | 10% | 75% | 48 hours |
| MiStage gate activation | 15% | 60% | 14 days |
| Role recall (remove steward/keeper) | 20% | 66% | 7 days |

---

## 7.3 ZK Voting (Semaphore)

Binding votes are secret ballots. No one — not stewards, not keepers, not helpers, not the protocol — can see how you voted.

### Architecture

```
┌─────────────────────────────────────────────────────┐
│  VOTER'S DEVICE                                     │
│  1. Fetch ballot (proposal details + options)       │
│  2. Generate ZK proof of eligibility                │
│     (Semaphore: "I am a member of this group"       │
│      without revealing which member)                │
│  3. Sign ballot choice with ephemeral key           │
│  4. Submit: proof + encrypted choice                │
├─────────────────────────────────────────────────────┤
│  BALLOT BOX (on-cluster)                            │
│  1. Verify ZK proof (is voter eligible?)            │
│  2. Check nullifier (has this person voted before?) │
│  3. Accept or reject ballot                         │
│  4. Store encrypted choice                          │
├─────────────────────────────────────────────────────┤
│  TALLY (after voting period ends)                   │
│  1. Decrypt choices (threshold decryption key)      │
│  2. Count votes                                     │
│  3. Publish result + proof of correct tally         │
│  4. Individual votes remain secret                  │
└─────────────────────────────────────────────────────┘
```

### Semaphore Implementation

- **Group:** All eligible voters for a specific proposal (determined by MiScope: place membership + standing threshold + age-of-majority)
- **Identity commitment:** Hash of member's secret (generated on device, never shared)
- **Nullifier:** Unique per proposal (prevents double-voting without revealing identity)
- **Signal:** The vote choice (encrypted)
- **Circuit:** Groth16 (proving time <2s on mobile, verification <50ms on server)

### Ballot Lifecycle

1. Proposal enters Decide stage → ballot created
2. Eligibility snapshot taken (MiScope query: who can vote on this?)
3. Semaphore group built from eligible identity commitments
4. Voting opens: 14 days
5. Members generate proofs on-device and submit
6. Voting closes: no more ballots accepted
7. Tally committee (3 random stewards) combine threshold key shares
8. Decrypt and count
9. Result published with mathematical proof of correctness
10. MiReceipt to each voter: "You voted on [Proposal X]. Result: [outcome]." (NOT your choice)

### Offline Voting

- Member generates ballot + ZK proof offline
- Stores in MiDTN queue
- Delivered when connectivity returns (must arrive before deadline)
- If deadline passes before delivery: ballot not counted (member notified)
- MiAction `offline.max_offline_hours` set to voting deadline

---

## 7.4 Liquid Delegation

Members can delegate their vote on specific topics to trusted others. Constraints prevent abuse.

### Rules

| Rule | Implementation |
|------|---------------|
| **Topic-scoped** | Delegation specifies topic tags (e.g., "infrastructure", "treasury", "safety"). Cannot delegate "everything." |
| **Time-limited** | Maximum 180 days. Must be actively renewed. |
| **Instantly revocable** | Member can revoke at any moment. If revoked during active vote, member can still cast directly. |
| **3-hop maximum** | Alice → Bob → Carol → Dave is max chain. Dave cannot re-delegate. |
| **Cycle detection** | Graph traversal check on every delegation. Cycles rejected immediately. |
| **No silent re-delegation** | If Bob delegates to Carol, Alice is notified ("Your delegate Bob has delegated to Carol on [topic]"). |
| **Concentration cap** | No single person can hold delegated weight of >5% of total eligible voters. Excess refused. |
| **Conflict disclosure** | If delegate has known conflict of interest on a proposal, delegator is notified and can redirect. |

### Delegation Graph (Apache AGE)

```cypher
// Create delegation
CREATE (alice:Member {did: 'did:milyfe:alice'})-[:DELEGATES_TO {
  topic: 'treasury',
  created: datetime(),
  expires: datetime() + duration('P180D'),
  revocable: true
}]->(bob:Member {did: 'did:milyfe:bob'})

// Cycle detection query
MATCH path = (start:Member)-[:DELEGATES_TO*1..3]->(start)
WHERE start.did = $new_delegator_did
RETURN path  // If any result: reject delegation

// Weight calculation for a proposal
MATCH (voter:Member)-[:DELEGATES_TO*0..3 {topic: $topic}]->(delegate:Member)
WHERE delegate.did = $delegate_did
RETURN count(DISTINCT voter) AS voting_weight

// Concentration check
MATCH (voter:Member)-[:DELEGATES_TO*1..3 {topic: $topic}]->(delegate:Member)
WITH delegate, count(DISTINCT voter) AS weight, 
     (SELECT count(*) FROM eligible_voters WHERE proposal_id = $proposal_id) AS total
WHERE weight > total * 0.05
RETURN delegate  // Exceeds 5% cap — reject new delegation
```

### Privacy

- Delegations are visible to: delegator, delegate, and auditors (stewards)
- NOT visible to: other members or the public
- Delegation graph is stored in Apache AGE with row-level security
- When a delegated vote is cast, only the final weight is visible in the tally (not the chain)

---

## 7.5 Circles (7-13, Rotating Stewards, Sortition)

Circles are the basic unit of self-governance. Every member belongs to at least one.

### Structure

| Property | Value | Rationale |
|----------|-------|-----------|
| Size | 7-13 members | Small enough for real discussion, large enough for diversity |
| Formation | Self-selected by interest/geography + overflow assignment | Members choose; orphans assigned randomly |
| Steward count | 1-2 per circle | Rotating leadership |
| Steward selection | Sortition (random from willing pool) | No elections = no campaigns = no concentration |
| Steward term | 3-6 months (circle votes on length) | Short enough to prevent entrenchment |
| Consecutive terms | Forbidden | Must skip at least one term |
| Treasury | Each circle has a $MLY pot (allocated from place treasury) | Self-directed spending |
| Meetings | Async default (Loomio thread) + optional sync (Jitsi) | Respects different schedules |

### Sortition Mechanics

```
1. Circle identifies steward vacancy
2. System generates willing pool:
   - All circle members who opted in to steward eligibility
   - Minus: current steward (no consecutive terms)
   - Minus: anyone serving as keeper or place steward elsewhere
   - Minus: anyone with standing below threshold
3. Cryptographic random selection (VRF — Verifiable Random Function)
4. Selected member can decline (next random pick)
5. If 3 consecutive declines: circle must discuss (maybe too small, or steward role too burdensome)
6. New steward onboarded with 1-week shadow period
```

### Circle Capabilities

| Capability | Requires |
|-----------|----------|
| Propose to place governance | 5 co-signers from circle |
| Spend from circle treasury (<500 $MLY) | Steward approval + 1 member second |
| Spend from circle treasury (>500 $MLY) | Circle vote (simple majority) |
| Invite new member to circle | Consensus (no strong objection in 72h) |
| Remove member from circle | 2/3 vote + appeal route offered |
| Request place-level resources | Proposal in Voice (standard process) |

---

## 7.6 Law Compiler (MiLegal Default-Deny Matrix)

MiLegal is a layered policy system. Default: everything is denied. Each layer adds specific permissions.

### 8 Layers (Evaluated Top-to-Bottom, First Match Wins)

| Layer | Name | Source | Example |
|-------|------|--------|---------|
| 0 | **Compact** | Unamendable items | "Children cannot be in public adult spaces" |
| 1 | **Platform default** | MiLyfe core team + community ratification | "DMs are E2EE by default" |
| 2 | **National law** | Country-specific legal requirements | "GDPR data deletion rights (EU)" |
| 3 | **Subdivision law** | State/province overrides | "Florida: no cannabis commerce" |
| 4 | **Municipal law** | City-specific rules | "Jacksonville noise ordinance hours" |
| 5 | **Instance policy** | Local community vote | "Our instance allows food truck marketplace" |
| 6 | **Circle policy** | Circle-level decisions | "Our circle meets Wednesdays" |
| 7 | **Individual preference** | Member's own settings | "I want notifications silent 10pm-7am" |

### Precedence Rules

- Higher layer (lower number) ALWAYS wins over lower layer
- Compact (0) cannot be overridden by anything
- National law (2) overrides instance policy (5) — "Law of the land first" (Oath #16)
- Individual preference (7) can only RESTRICT further, never EXPAND beyond what higher layers allow
- Conflict between same-level layers: stricter interpretation wins

### Law Pack Format

```yaml
# milyfe-legal-pack: us-fl-duval-v2.3
metadata:
  jurisdiction: US-FL-DUVAL
  version: "2.3"
  effective_date: "2026-07-01"
  reviewed_by: "legal_review_committee"
  next_review: "2027-01-01"

rules:
  - id: "pocket.shop_pos.sales_tax"
    layer: 3  # Subdivision (Florida)
    action: "require"
    description: "Florida requires sales tax collection on tangible goods"
    condition: "action.type == 'pocket.shop_purchase' AND item.tangible == true"
    effect: "Display sales tax notice. Shop responsible for remittance."

  - id: "voice.cannabis_commerce"
    layer: 3  # Subdivision (Florida)
    action: "deny"
    description: "Cannabis sale/purchase prohibited under Florida state law"
    condition: "action.type == 'street.marketplace.listing' AND item.category == 'cannabis'"
    effect: "Listing rejected. Explanation: 'Not permitted under Florida law.'"

  - id: "safety.dv_mandatory_report"
    layer: 2  # National
    action: "require"
    description: "Mandatory reporting obligations for certain professionals"
    condition: "action.type == 'safety.report' AND reporter.role == 'licensed_professional'"
    effect: "Inform reporter of their mandatory reporting obligation (not MiLyfe's obligation)"

  - id: "privacy.child_location"
    layer: 0  # Compact (unamendable)
    action: "deny"
    description: "Child location never shared publicly"
    condition: "action.audience.visibility == 'public' AND actor.age < age_of_majority"
    effect: "Action rejected. Cannot be overridden."
```

### OPA Integration

```rego
# MiLegal default-deny policy
package milyfe.legal

default allow = false

# Layer 0: Compact rules (cannot be overridden)
deny[msg] {
    input.action.audience.visibility == "public"
    input.actor.age < data.jurisdiction.age_of_majority
    msg := "Compact violation: child content cannot be public"
}

# Layer evaluation: iterate layers 0-7, first match wins
allow {
    not any_deny
    some rule in data.law_pack.rules
    rule.action == "allow"
    eval_condition(rule.condition, input)
}

# Stricter jurisdiction wins
deny[msg] {
    some rule in data.law_pack.rules
    rule.action == "deny"
    eval_condition(rule.condition, input)
    msg := rule.description
}
```

---

## 7.7 Dispute Resolution (5 Levels)

Distinct from MiAppeal (which handles appeals of platform decisions). Dispute resolution handles conflicts between members.

| Level | Name | Type | Facilitator | Timeline | Binding |
|-------|------|------|-------------|----------|---------|
| 1 | **Direct** | Members talk it out | None (optional helper mediation script) | Unlimited | No |
| 2 | **Circle mediation** | Circle steward facilitates | Circle steward | 14 days | Recommendations only |
| 3 | **Community mediation** | Trained mediator assigned | Certified mediator (MiHandoff) | 30 days | Binding if both agree |
| 4 | **Arbitration panel** | 3-person panel from different circles | Random selection + conflict check | 45 days | Binding |
| 5 | **Separation** | Members can't resolve — structural separation | Steward implements | Immediate | Permanent (different circles, optional block) |

### Evidence Rules

- Evidence must be shared with both parties (no secret evidence)
- Digital evidence: MiReceipts, message logs (with consent), transaction history
- Witness statements: written or audio (accessibility)
- Helper logs: admissible only if both parties consent
- Child-related disputes: MiChildGate review takes precedence over dispute resolution

### Outcomes Available

| Outcome | Scope | Appeal |
|---------|-------|--------|
| Apology + acknowledgment | Relational | No (voluntary) |
| Behavioral agreement | Time-limited (90 days) | Circle panel |
| $MLY restitution | Amount determined by panel | Place mediator |
| Separation (no contact) | Permanent or time-limited | Federation ombuds |
| Restorative action (community service) | Quest assignment | Circle panel |

---

## 7.8 Claims Gate

Before any governance claim can trigger action, evidence must meet thresholds.

| Claim Type | Evidence Required | Verification | Threshold |
|-----------|-------------------|--------------|-----------|
| Policy violation | MiReceipt or screenshot + 2 witness corroborations | Keeper review | Preponderance (more likely than not) |
| Financial dispute | Transaction MiReceipts + timeline | Ledger audit (automated) | Clear records |
| Safety concern | Reporter statement + any corroborating evidence | Keeper immediate review | Good faith report (low bar for safety) |
| Standing challenge | Specific actions cited + policy reference | Steward + independent reviewer | Clear and convincing |
| Constitutional violation | Policy analysis + community impact statement | Constitutional Review Panel | Clear violation of compact/amendment |
| Role misconduct | Documented pattern (3+ incidents) OR single serious breach | Independent panel (not same circle) | Preponderance |

**False claims protection:**
- Good-faith reports are never penalized (even if wrong)
- Pattern of bad-faith reports (determined by panel): warning → temporary reporting cooldown → standing impact
- No punishment for losing a dispute or having a claim not upheld

---

# OS 8 — Education OS

**Purpose:** Human development is the product. Learning is not a module buried in settings — it's a primary tab (Learn). Always free. Always offline-capable. Never paywalled. Badges leave with you.

---

## 8.1 Ten Staffed Paths

Each path has a named helper, curriculum structure, and human teacher/mentor pipeline.

| # | Path Name | Helper | Target Population | Duration | Completion Badge |
|---|-----------|--------|------------------|----------|-----------------|
| 1 | Rights and Papers | Rue | Anyone needing legal navigation | Self-paced (4-12 weeks) | "Rights Navigator" |
| 2 | Parenting | Kin | Parents, guardians, caregivers | Ongoing (modules) | "Community Parent" |
| 3 | Reentry | Tide | Formerly incarcerated, probation | 12-week structured | "New Chapter" |
| 4 | Peace | Bridge | Gang/crew members, conflict-involved | 16-week structured | "Peacemaker" |
| 5 | Food and First Aid | Terra + Patch | Everyone (essential skills) | 6-week modular | "Community First Responder" |
| 6 | Repair | Spark | Anyone wanting to fix things | 8-week hands-on | "Repair Specialist" |
| 7 | Money (Not a Casino) | Nia | Everyone (financial literacy) | 4-week structured | "Money Navigator" |
| 8 | Read/Write/Numbers/Languages | Sage | Literacy learners, ESL | Self-paced (ongoing) | "Literate" (per level) |
| 9 | The Trade This Place Lacks | Forge | Workers, career changers | 12-24 week apprenticeship | Trade-specific credential |
| 10 | How to Run a Street | Vox + Weaver | Community leaders, organizers | 8-week structured | "Street Steward" |

### Curriculum Structure (Each Path)

```yaml
path:
  name: "Peace"
  helper: "Bridge"
  version: "1.0"
  language: ["en", "es"]
  offline_capable: true
  
  modules:
    - id: "peace-01"
      title: "Understanding Conflict"
      type: "interactive_lesson"
      duration_hours: 2
      content:
        - text_lesson (plain language, 6th grade reading level)
        - audio_version (recorded by community member)
        - interactive_exercise (scenario-based)
        - reflection_prompt
      assessment:
        type: "portfolio"  # NOT standardized test
        criteria: ["demonstrate understanding", "personal reflection"]
      
    - id: "peace-02"
      title: "De-escalation Techniques"
      type: "practice_session"
      duration_hours: 3
      requires: ["peace-01"]
      content:
        - video_demonstration
        - role_play_script
        - practice_with_partner (human required)
      assessment:
        type: "peer_observation"
        criteria: ["apply technique", "receive feedback"]

  completion:
    requires_all_modules: true
    final_assessment: "community_project"  # Real contribution
    badge_issued: "Peacemaker"
    badge_schema: "https://milyfe.org/badges/peacemaker/v1"
```

---

## 8.2 Journey Structure

Every member follows a non-linear but structured journey through learning.

### Five Stages

```
┌──────────┐   ┌─────────────┐   ┌─────────┐   ┌────────┐   ┌─────────┐
│ WELCOME  │──►│FIND YOUR    │──►│ A CRAFT │──►│ A ROLE │──►│  TEACH  │
│          │   │ FEET        │   │         │   │        │   │         │
│ Day 1-7  │   │ Week 1-4    │   │ Month   │   │ Month  │   │ Ongoing │
│          │   │             │   │ 2-6     │   │ 4+     │   │         │
│ Onboard  │   │ Safety,     │   │ Choose  │   │ Give   │   │ Create  │
│ + orient │   │ basics,     │   │ a path, │   │ back,  │   │ + run   │
│          │   │ community   │   │ build   │   │ serve  │   │ classes │
└──────────┘   └─────────────┘   └─────────┘   └────────┘   └─────────┘
```

| Stage | What Happens | Completion Criteria | Unlocks |
|-------|-------------|--------------------|---------| 
| **Welcome** | MiBoot onboarding, Mi intro, first quest, pocket setup | Profile complete, 1 quest done, 1 thank sent | Full platform access |
| **Find Your Feet** | Safety orientation, community norms, resource discovery | Safety module done, attended 1 circle meeting (async OK), found 3 resources | Path selection |
| **A Craft** | Deep-dive into chosen path(s). Multiple modules. Practice. | Path modules complete, final project/portfolio submitted | Role eligibility |
| **A Role** | Contribute to community: keeper, teacher, steward, mediator, repair lead | Active role for 30+ days, positive peer feedback | Teach mode |
| **Teach** | Create and run classes for others. Mentor new members. | Published 1 class, 3+ students completed it | Elder standing recognition |

### Non-Linear Branching

- Members can be in multiple paths simultaneously
- No path is prerequisite for another (except explicit module dependencies within a path)
- Members can return to earlier stages (life happens — divorce, job loss, move)
- Progress is never lost — badges and completions persist forever
- Skip mode: if member demonstrates existing competency, they can challenge-test out of modules

---

## 8.3 Offline Packs (Kolibri)

**Integration:** Kolibri (Learning Equality) for offline-first education content delivery.

### Architecture

```
┌─────────────────────────────────────────────────────┐
│  KOLIBRI SERVER (on K3s cluster)                    │
│  - Hosts all MiLyfe curriculum content              │
│  - Packages into downloadable channel packs         │
│  - Syncs progress when device reconnects            │
├─────────────────────────────────────────────────────┤
│  KOLIBRI DEVICE CLIENT                              │
│  - Downloaded content available without internet    │
│  - Interactive exercises work offline               │
│  - Progress tracked locally, synced on reconnect    │
│  - ~500MB per path (compressed)                     │
├─────────────────────────────────────────────────────┤
│  CONTENT PACKAGING                                  │
│  - Video: compressed H.264 480p (bandwidth-friendly)│
│  - Audio: Opus 48kbps                               │
│  - Text: Markdown rendered locally                  │
│  - Exercises: HTML5 + JS (no server dependency)     │
│  - Total library: ~5GB (all 10 paths)               │
└─────────────────────────────────────────────────────┘
```

### Sync Protocol

1. Device connects to any network (WiFi, mesh, or internet)
2. Kolibri client checks for: new content versions, progress uploads pending
3. Uploads: completed modules, assessment submissions, time-on-task
4. Downloads: new content, updated modules, peer feedback
5. Conflict resolution: progress is additive (never loses completed work)

### Prison/Facility Mode

- Content pre-loaded on approved tablets (facility coordination required)
- No network access needed (fully offline)
- Progress stored locally, exported via USB when facility allows
- Content restrictions: facility can block specific modules (MiLyfe provides full catalog, facility decides)
- On release: progress imports seamlessly to member's personal account

---

## 8.4 Open Badges (W3C Verifiable Credentials)

Every completion issues a portable badge that the member owns forever.

### Badge Schema

```json
{
  "@context": [
    "https://www.w3.org/ns/credentials/v2",
    "https://purl.imsglobal.org/spec/ob/v3p0/context-3.0.3.json",
    "https://milyfe.org/ns/badge/v1"
  ],
  "type": ["VerifiableCredential", "OpenBadgeCredential"],
  "id": "urn:uuid:badge-{{uuid}}",
  "issuer": {
    "id": "did:milyfe:instance:jacksonville-01",
    "name": "MiLyfe Jacksonville",
    "type": "Profile"
  },
  "validFrom": "2026-08-24T00:00:00Z",
  "credentialSubject": {
    "id": "did:milyfe:alice123",
    "type": "AchievementSubject",
    "achievement": {
      "id": "https://milyfe.org/badges/peacemaker/v1",
      "type": "Achievement",
      "name": { "en": "Peacemaker", "es": "Pacificador" },
      "description": { "en": "Completed the Peace path: 16 weeks of conflict resolution training, de-escalation practice, and a community peace project." },
      "criteria": {
        "narrative": "Complete all 8 Peace modules + final community project assessed by peer panel"
      },
      "image": "https://badges.milyfe.local/peacemaker-v1.svg"
    },
    "evidence": [
      {
        "id": "urn:uuid:evidence-{{uuid}}",
        "type": "Evidence",
        "name": "Community Peace Project",
        "description": "Organized neighborhood conflict resolution session, documented in portfolio"
      }
    ]
  },
  "proof": {
    "type": "Ed25519Signature2020",
    "created": "2026-08-24T12:00:00Z",
    "verificationMethod": "did:milyfe:instance:jacksonville-01#key-1",
    "proofPurpose": "assertionMethod",
    "proofValue": "z4M9s..."
  }
}
```

### Portability

- Badges stored in member's personal vault (Nextcloud + local device)
- Exportable as: JSON-LD, PNG (baked badge), PDF certificate
- Verifiable by any party with internet access (verification URL in QR)
- Survive platform exit: badges are self-contained credentials, need no MiLyfe account to verify
- Cross-instance recognition: federated instances honor each other's badges (standing contribution)

---

## 8.5 Inside-the-Walls Mode

Education that works in prisons, juvenile facilities, shelters, and other restricted environments.

### Constraints and Solutions

| Constraint | Solution |
|-----------|---------|
| No internet | Fully offline Kolibri packs on approved devices |
| No personal devices | Shared tablets with MiShared (safe device mode) |
| Limited hours | Micro-modules (15-30 min each), saveable at any point |
| Monitored communications | No messaging/social features in facility mode |
| No $MLY transactions | Learn-only mode (pocket disabled) |
| Content restrictions | Facility admin can exclude specific modules |
| Identity continuity | Unique ID created inside, merges with full account on release |
| Progress export | USB export to case worker, imports to personal account on release |

### Day-One Profile (Reentry)

When a person leaves incarceration:
1. Inside ID merges with full MiLyfe account
2. All earned badges transfer
3. Learn progress continues seamlessly
4. First-month $MLY UBI bonus (voted by community — MiStage: Sprout)
5. Tide helper activates with reentry-specific guidance
6. Resource matching: housing, employment, legal obligations calendar

---

## 8.6 Teach Mode

Any member who reaches the Teach stage can create and run classes.

### Class Creation Flow

```
Member creates class:
├── Title + description (plain language required — MiPlain lint)
├── Target audience (beginner/intermediate/advanced)
├── Format: async (self-paced) | sync (scheduled sessions) | hybrid
├── Prerequisites: badges or modules required (optional)
├── Content: upload lessons, exercises, assessments
├── Language: primary + translations available
├── Offline-capable: yes (auto-packaged for Kolibri)
├── Accessibility: screen reader tested, captions, plain language
└── Submit for review

Review (automated + human):
├── MiPlain lint: reading level check (reject if >8th grade without justification)
├── MiChildGate: appropriate for listed audience?
├── Accessibility: automated a11y check (axe-core on HTML content)
├── Content review: peer teacher reviews quality
├── Legal: no copyright-infringing material (OSI/CC-licensed only)
└── Published to Learn catalog

Running a class:
├── Students enroll (auto-accept or teacher-approved)
├── Progress tracking (Kolibri integration)
├── Discussion thread (Matrix room, E2EE for class)
├── Assessment: teacher grades OR peer assessment OR portfolio
├── Completion: badge issued (class-specific, signed by instance)
└── Feedback: students rate, teacher improves

Compensation:
├── Teaching is a contribution type (earns $MLY)
├── Rate: community-voted per class hour
├── Payment: from Place treasury (not from students)
└── Students NEVER pay for classes (Oath: free forever for learning)
```

---

# OS 9 — Population OS

**Purpose:** MiLyfe is not one app for one kind of person. Each population has unique needs, risks, and strengths. The Population OS ensures every life situation gets a specialized flow — not a one-size-fits-all experience that works for middle-class tech workers and fails everyone else.

**Design principle:** Worst-case-first. Design for the person with the hardest Tuesday, then everyone else benefits.

---

## 9.1 Ten Populations × Specialized Flows

| # | Population | Primary Helpers | Key Services | Non-Negotiable Constraints |
|---|-----------|----------------|--------------|---------------------------|
| 1 | **Neighborhoods** | Mi, Weaver, Terra | Street (full), quests, pulse, story, shops | Never face-hunt the block. No surveillance. |
| 2 | **Single Parents** | Kin, Forge, Sage | Care swaps, ride shares, night class compat, food surplus | Never judge private life. Never require two-parent presence. |
| 3 | **Abused People** | Hearth, Rue | Leave-now, hidden visibility, shelter routing, legal aid | Never force a table with abuser. Safety over process. |
| 4 | **Orphans/Foster/Aged-Out** | Sage, Tide, Kin | Steward profiles, learn paths, first-home jar, time-boost | Never pity feed. Dignity always. |
| 5 | **Homeless** | Compass, Patch, Forge | No-address profile, resource mapping, shower/laundry, kiosk access | Never demand ID they don't have. Profile works from library. |
| 6 | **Elderly** | Elder, Patch, Kin | Check-ins (THEY set), rides, story-keeping, medical reminders | Never silent tracking. Never patronize. They choose. |
| 7 | **Crews/Gangs** | Bridge, Forge, Weaver | Peace tables, exit pathways, guild formation, $MLY for peace | Never pay for territory. Never enable violence. |
| 8 | **Incarcerated** | Tide, Sage | Offline lessons, family contact (facility allows), teaching inside | Never contraband. Never escape. Never fraud. |
| 9 | **Just Out/Probation** | Tide, Forge, Rue | Day-one pocket, clothes/food jar, real ID help, job board, calendar | Never hide from lawful officer. Legal obligations visible. |
| 10 | **Kids** | Scout, Kim, Sage | Play, tutoring, learning games, sandbox, stickers, safety | No money. No public story without grown-up. No adult DMs. EVER. |

---

## 9.2 Population-Specific Flows

### Neighborhoods (Full Street Organs)

```
Member joins place
    │
    ├── Auto-assigned to nearest neighborhood circle
    ├── Street tab activates: local marketplace, quests, surplus, resources
    ├── MiPulse shows ambient health of the block
    ├── Community pot visible (neighborhood treasury allocation)
    └── Story book: public events (opt-in contributions)

Ongoing:
├── Quests posted by neighbors: "Can someone help move a couch?"
├── Surplus board: "I have 6 extra tomatoes from the garden"
├── Rides: "I'm going to Walmart at 3pm, room for 2"
├── Care exchange: hour-for-hour, tracked via TimeOverflow
├── Shop pins: local businesses accepting $MLY
└── Pulse: weather of the block (safety, activity, needs)
```

**Privacy guarantee:** Neighborhood view shows aggregated activity, NEVER individual tracking. "5 people are active on Elm Street" not "Alice is at 123 Elm."

### Single Parents

```
Onboarding detects: guardian role, single-adult household
    │
    ├── Kin helper activates with single-parent context
    ├── Care swap matching: "Who else needs Tuesday afternoon coverage?"
    ├── Night class compatibility checker: "These classes have childcare"
    ├── Food surplus priority: single-parent households get first-ping on expiring food
    ├── Ride sharing: school runs, appointments, grocery
    └── Emergency babysit network: "I need someone in 30 minutes"

Special $MLY flows:
├── Shared household jars (visible to all adults in household)
├── Kid expense tracking (for co-parent accountability if desired)
└── Child-specific savings goals (birthday fund, school supplies)
```

### Abused People (Leave-Now Protocol)

```
LEAVE-NOW (one tap from You tab → Safety):
    │
    ├── IMMEDIATE (within 5 seconds):
    │   ├── Freeze all shared jars (abuser loses access)
    │   ├── Hide location from all except keeper
    │   ├── Remove paired devices (abuser's phone can't see)
    │   ├── Switch to hidden visibility mode
    │   ├── Suppress all notifications that could alert abuser
    │   └── Generate new session keys (old shared sessions invalidated)
    │
    ├── WITHIN 1 MINUTE:
    │   ├── Shelter list surfaced (nearest, available, filtered by needs)
    │   ├── Hearth helper: "I'm here. You don't need to explain."
    │   ├── Legal aid routing via MiHandoff (urgency: emergency)
    │   ├── DV hotline numbers displayed
    │   └── Safe contacts notified (if pre-configured)
    │
    ├── WITHIN 1 HOUR:
    │   ├── Temporary $MLY from emergency reserve (community vote threshold)
    │   ├── Document preservation (screenshots, message history → encrypted vault)
    │   └── Restraining order resources (Rue helper, Docassemble templates)
    │
    └── ONGOING:
        ├── Hidden mode remains until member explicitly deactivates
        ├── Abuser's profile flagged (cannot see this member anywhere)
        ├── Shared children: separate access (guardian still, but no location)
        └── No forced mediation. No "both sides." Safety first. Always.
```

**Technical implementation:**
- MiScope: all relationship tuples involving abuser → suspended on trigger
- MiAction: all pending actions from abuser to victim → voided
- Matrix: shared rooms → victim removed silently (no "X left" message)
- Location services: victim's coordinates purged from all shared views
- Device registry: all authorized devices except victim's personal → revoked

---

## 9.3 Peace System (Gang → Guild Pipeline)

**The Vanguard Protocol:** Out-compete the streets. Better protection, better brotherhood, legitimate income.

### Pipeline Stages

```
┌──────────────┐    ┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│  CONTACT     │───►│  TABLE       │───►│  GUILD       │───►│  COMMUNITY   │
│              │    │              │    │              │    │              │
│ Bridge makes │    │ Peace table  │    │ Vanguard     │    │ Full member  │
│ first contact│    │ (neutral,    │    │ circle forms │    │ (standing,   │
│ No judgment  │    │ no cops, no  │    │ (5-12 people)│    │ roles, teach)│
│              │    │ snitching)   │    │              │    │              │
│ Duration:    │    │ Duration:    │    │ Duration:    │    │ Duration:    │
│ 1-4 weeks    │    │ 4-8 weeks    │    │ 16+ weeks    │    │ Permanent    │
└──────────────┘    └──────────────┘    └──────────────┘    └──────────────┘
```

### Stage Details

| Stage | What Happens | $MLY Incentive | Helper | Human Required |
|-------|-------------|---------------|--------|---------------|
| **Contact** | Bridge helper or outreach member makes relationship. No demands. Shows platform, shows money is real. | None yet (observe, don't bribe) | Bridge | Outreach worker |
| **Table** | Neutral meeting. Rules: no weapons, no phones recording, no snitching, no cops at table. Air grievances. Find common ground. | First $MLY for showing up (quest reward) | Bridge | Trained mediator (ALWAYS) |
| **Guild** | Form a Vanguard Circle (5-12). Defend and clean your block. Peer-review at week's end (Coordinape-style). Divide bounty based on peer assessment. | Weekly peace bounty (from Place treasury) | Bridge + Forge | Circle steward + mediator |
| **Community** | Full MiLyfe member. Standing grows. Can teach, can steward, can mentor next generation. Peace becomes identity, not performance. | Full $MLY access + contribution rewards | All available | Peer support |

### Coordinape-Style Guild Economics

```
Weekly cycle:
1. Guild members perform community protection tasks (real, documented):
   - Walk-home escort
   - Block cleanup
   - De-escalation interventions
   - Youth mentoring
   - Event security (community events)
   
2. Week ends → peer review opens (72 hours):
   - Each member allocates 100 points among OTHER members
   - Points = assessment of who contributed most
   - Anonymous during allocation, revealed after

3. Bounty distributed proportionally:
   - Weekly guild bounty (e.g., 500 $MLY for 8-person guild)
   - If Alice got 20% of points → she gets 100 $MLY
   - If Bob got 5% → he gets 25 $MLY

4. Minimums and caps:
   - Minimum: 5% of bounty (no one gets zero if they participated)
   - Maximum: 25% of bounty (no single person dominates)
   - No-show: 0 (must have at least 1 documented task to receive)
```

### Non-Negotiable Peace Rules

1. **Never pay for territory.** Payment is for community service, not claiming a block.
2. **Never enable violence.** Any guild member documented committing violence: immediate guild suspension + appeal.
3. **Table confidentiality.** What's said at peace table stays there. Violation = permanent table ban.
4. **No forced participation.** Voluntary. Always. Walking away is always an option.
5. **No snitching structure.** MiLyfe is not a surveillance tool. Peace table is not intelligence gathering.
6. **Real exit support.** If someone wants out of a gang, MiLyfe provides: job placement, housing leads, relocation support (if safety requires), new social circle.

---

## 9.4 Reentry System (Pre-Release → Gate Day → Year One)

### Timeline

```
PRE-RELEASE (6 months before)          GATE DAY                    YEAR ONE
─────────────────────────────────────── │ ─────────────────────────────────────
                                        │
Offline lessons (Kolibri)               │ Profile activates fully
Learn path progress saved               │ First-month $MLY bonus
Family contact (where allowed)          │ Tide helper: "Welcome. Here's today."
Reentry plan built with Tide            │ Clothes/food jar available
Court dates loaded into calendar        │ Real ID appointment queued
Resource matching (housing, jobs)       │ Job board (neighbors-first matching)
Recovery contacts established           │ Parole/probation calendar synced
                                        │ Circle assignment (reentry-specific)
                                        │
                                        │ Week 1: orientation + 3 quests
                                        │ Week 2-4: daily check-ins (opt-in)
                                        │ Month 2-3: stable housing focus
                                        │ Month 4-6: employment + skill building
                                        │ Month 7-12: community integration
                                        │ Year 1 ceremony: standing milestone
```

### Specialized Flows

| Need | Service | Helper | Human |
|------|---------|--------|-------|
| Housing | Resource DB (shelters → transitional → permanent) | Atlas | Housing counselor |
| Employment | Job board (ban-the-box employers flagged) | Forge | Employment specialist |
| Legal obligations | Calendar with court dates, PO meetings, fines | Rue | PO coordination (with consent) |
| Substance recovery | Meeting finder, peer support matching | Patch | Recovery sponsor |
| Family reconnection | Mediated contact (if safe), parenting path | Kin | Family mediator |
| Financial | First-month $MLY, budgeting path, no-predatory-lending info | Nia | Financial counselor |
| Documentation | Real ID checklist, vital records, social services | Rue | Case manager |

### Constraints

- MiLyfe is NOT a supervision tool. No GPS ankle monitor integration. No reporting to PO.
- Calendar shows obligations so the MEMBER doesn't miss them — not so authorities can track.
- Member can share calendar with PO voluntarily (useful for demonstrating compliance).
- If member violates terms: that's between them and the court. MiLyfe doesn't enforce.

---

## 9.5 Safety System

### DV Detection (Passive, Not Surveillance)

MiLyfe does NOT proactively detect DV. It provides tools when the person is ready:

| Feature | How It Works | Privacy |
|---------|-------------|---------|
| Leave-Now button | Always visible in You → Safety. One tap. | Only visible to account holder |
| Hidden journal | Encrypted notes only the member can see | Not accessible to shared device users |
| Evidence vault | Screenshots, messages saved to encrypted personal storage | Purged if member chooses; preserved if they want |
| Safety plan builder | Hearth walks through exit planning (go-bag, documents, contacts) | Encrypted, device-only until member acts |
| Danger assessment | Optional questionnaire (validated DV assessment tool) | Score shown to member only, never stored centrally |

### Walk-Home Timer Protocol

```
Member activates timer:
    │
    ├── Set destination + expected arrival time
    ├── Choose alert contacts (1-5 trusted people)
    │
    ├── DURING WALK:
    │   ├── BLE beacon to nearby MiESP nodes (proves alive + moving)
    │   ├── No location shared with contacts YET (just "timer active")
    │   └── Member can extend time ("stopping for coffee, 15 more min")
    │
    ├── ARRIVED SAFELY:
    │   ├── Member taps "I'm here"
    │   ├── Contacts notified: "They arrived safely"
    │   └── Timer data purged (no location history retained)
    │
    └── TIMER EXPIRES (member didn't check in):
        │
        ├── T+0: Push notification to member: "Are you OK? Tap to confirm"
        ├── T+2min: No response → alert contacts: "[Name] hasn't checked in"
        ├── T+5min: No response → contacts get last known mesh node location
        ├── T+10min: No response → escalate to keeper if configured
        └── T+15min: No response from anyone → keeper decides (call? dispatch?)

Data retention:
- Route data: NEVER stored. Mesh nodes only know "device pinged" not "where going"
- Timer metadata: purged on completion or 24h after expiry
- Alert history: "Timer used on [date]" only (not route, not destination)
```

### Witness Mode

```
Member activates witness mode:
    │
    ├── Device begins recording (audio + optional video)
    ├── Recording streams to encrypted personal vault in real-time
    │   (even if device is destroyed, cloud has partial recording)
    ├── Optional: live-stream to chosen witnesses (trusted contacts)
    ├── GPS/mesh location logged for duration
    │
    ├── WHEN DEACTIVATED:
    │   ├── Recording saved to vault (member controls access)
    │   ├── Member decides: keep, share with authorities, delete
    │   └── Metadata (time, duration, location) saved separately
    │
    └── IF DEVICE GOES OFFLINE/DESTROYED:
        ├── Last streamed segment preserved in vault
        ├── Alert contacts notified: "Witness mode ended unexpectedly"
        └── Location at last contact preserved

Privacy guarantees:
- Recording is member's property
- MiLyfe cannot access recording content
- No facial recognition processing
- Two-party consent: in two-party states, member is responsible for consent
- Recording is NOT automatically shared with anyone (member decides)
```

---

# OS 10 — Physical Universe OS

**Purpose:** Connect the digital platform to the physical world. IoT sensors, digital twins, and smart infrastructure — all governed by the same constitutional principles. The physical world is NOT a surveillance grid. It is a community tool that members control.

---

## 10.1 IoT Spine (FIWARE Orion + MQTT + NGSI-LD)

### Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│  PHYSICAL SENSORS & ACTUATORS                                   │
│  (temperature, air quality, water, traffic, noise, soil, etc.)  │
├─────────────────────────────────────────────────────────────────┤
│  MQTT BROKER (Mosquitto / VerneMQ)                              │
│  - Lightweight pub/sub for sensor data                          │
│  - TLS + client certificates for device auth                   │
│  - Topic structure: milyfe/{place}/{domain}/{device_id}/data   │
├─────────────────────────────────────────────────────────────────┤
│  FIWARE ORION-LD (Context Broker)                               │
│  - NGSI-LD API for entity management                           │
│  - Real-time entity updates from MQTT                          │
│  - Subscription/notification for downstream consumers          │
│  - Multi-tenant: each domain is a separate NGSI-LD tenant      │
├─────────────────────────────────────────────────────────────────┤
│  TIMESCALEDB (Historical Data)                                  │
│  - Time-series storage for all sensor readings                 │
│  - Retention: raw data 90 days, aggregated data 5 years        │
│  - Feeds analytics, MiPulse, and digital twins                 │
├─────────────────────────────────────────────────────────────────┤
│  GOVERNANCE LAYER (MiScope + MiStage + MiLegal)                 │
│  - Who can deploy sensors? (MiScope: community vote)            │
│  - Which domains are active? (MiStage gates)                    │
│  - What data can be collected? (MiLegal default-deny)           │
│  - Who can see results? (MiScope audience)                      │
│  - Two-person actuation rule (safety gates)                     │
└─────────────────────────────────────────────────────────────────┘
```

### NGSI-LD Entity Model (Example: Air Quality Sensor)

```json
{
  "id": "urn:ngsi-ld:AirQualityObserved:jacksonville-01:sensor-042",
  "type": "AirQualityObserved",
  "@context": "https://uri.fiware.org/ns/data-models",
  "dateObserved": {
    "type": "Property",
    "value": "2026-08-24T14:30:00Z"
  },
  "location": {
    "type": "GeoProperty",
    "value": { "type": "Point", "coordinates": [-81.6557, 30.3322] }
  },
  "PM25": {
    "type": "Property",
    "value": 12.3,
    "unitCode": "GQ",
    "observedAt": "2026-08-24T14:30:00Z"
  },
  "PM10": {
    "type": "Property",
    "value": 28.1,
    "unitCode": "GQ"
  },
  "temperature": {
    "type": "Property",
    "value": 31.2,
    "unitCode": "CEL"
  },
  "deployedBy": {
    "type": "Relationship",
    "object": "urn:ngsi-ld:Member:did:milyfe:communitymember42"
  },
  "governanceApproval": {
    "type": "Property",
    "value": "urn:milyfe:vote:proposal-2026-034"
  }
}
```

---

## 10.2 Smart Domains (30+)

| # | Domain | Module | Sensors/Actuators | Data Collected | MiStage Gate | Safety Gate |
|---|--------|--------|-------------------|---------------|-------------|-------------|
| 1 | Transportation | MiCar | GPS beacons, ride-share proximity | Ride availability, not individual tracking | Trunk | No face tracking |
| 2 | Home retrofit | MiRetrofit | Energy monitors, leak detectors | Energy usage (household aggregate) | Canopy | Opt-in only |
| 3 | Smart home | MiHome | Thermostat, locks, lights | Energy + comfort (owner only) | Canopy | Owner control only |
| 4 | Building | MiBuilding | HVAC, occupancy (IR, not camera), elevator | Comfort, efficiency | Canopy | No individual ID |
| 5 | Transit | MiTransit | Bus/bike GPS, traffic counters | Schedule adherence, congestion | Trunk | Aggregate only |
| 6 | Energy grid | MiGrid | Solar production, battery, demand | Generation, storage, load | Canopy | Two-person actuation |
| 7 | Water | MiWater | Flow, pressure, quality sensors | Usage, quality alerts | Canopy | Auto-shutoff requires human confirm |
| 8 | Agriculture | MiFarm | Soil moisture, weather, drone survey | Crop health, irrigation needs | Trunk | No private property without consent |
| 9 | Health facility | MiClinic | Appointment kiosks, wait times | Capacity, wait time (anonymous) | Forest | No patient data |
| 10 | Classroom | MiClass | CO2, temperature, noise level | Comfort for learning | Trunk | No student tracking |
| 11 | Environment | MiEarth | Weather stations, flood sensors | Climate, disaster early warning | Sprout | Public data |
| 12 | Waste | MiWaste | Fill-level sensors on bins | Collection optimization | Trunk | No household attribution |
| 13 | Public safety | MiSafety | Noise levels, gunshot detection (ShotSpotter-type) | Incident alerts | Canopy | No cameras. No face-ID. Acoustic only. |
| 14 | District | MiDistrict | Pedestrian counters, park usage | Foot traffic patterns (aggregate) | Canopy | No individual tracking |
| 15 | Factory/workshop | MiFactory | Machine status, power, air quality | Production health, worker safety | Forest | Worker consent required |
| 16 | Supply chain | MiSupply | Temperature loggers, location beacons | Cold chain integrity, ETA | Canopy | Business opt-in |
| 17 | Market | MiMarket | Foot traffic, stall availability | Market health, busy times | Trunk | Aggregate only |
| 18 | Culture | MiCulture | Event attendance (counters), noise | Venue capacity, sound levels | Trunk | No individual ID |
| 19 | Accessibility | MiAccess | Ramp status, elevator availability, obstacle detection | Accessibility routing | Sprout | Public benefit data |
| 20 | Digital twin | MiTwin | All of the above (aggregated) | 3D visualization | Canopy | Read-only visualization |
| 21 | Community | MiCommunity | Shared space booking, tool library | Resource availability | Sprout | User-initiated only |
| 22 | Network | MiNetwork | Mesh node health, signal strength | Coverage map | Seed | Auto (MiNOC) |
| 23 | Lab | MiLab | Environmental monitors, equipment status | Research facility ops | Forest | Institutional control |
| 24 | Civic | MiCivic | Public meeting attendance (count), service requests | Government interface | Canopy | Anonymous counts only |
| 25 | Air quality | MiAir | PM2.5, PM10, O3, NO2, CO | Health advisories | Sprout | Public benefit |
| 26 | Maritime | MiSea | Water level, current, vessel AIS | Flood prediction, port status | Forest | Public safety data |
| 27 | Orbital/satellite | MiOrbit | Satellite imagery (public sources) | Land use, vegetation, disaster | Forest | Public sources only |
| 28 | Mind/wellness | MiMind | None (self-reported only) | Mood patterns (private) | Sprout | Never sensor-based. Always voluntary. |
| 29 | Carbon | MiCarbon | Energy meters, transport logs | Carbon footprint (community aggregate) | Canopy | No individual shaming |
| 30 | Emergency | MiEmergency | All safety-relevant sensors | Disaster coordination | Sprout | Public safety priority |

---

## 10.3 Digital Twins (Eclipse Ditto + CesiumJS)

### Architecture

```
┌─────────────────────────────────────────────────────┐
│  CESIUMJS (3D Visualization - Browser)              │
│  - 3D city model rendered client-side               │
│  - Real-time data overlays (air quality, traffic)   │
│  - Time-series playback (what happened last week)   │
│  - Accessible: 2D fallback, screen-reader summary   │
├─────────────────────────────────────────────────────┤
│  ECLIPSE DITTO (Digital Twin Service)               │
│  - Thing/Feature model for every IoT entity         │
│  - Desired vs Reported state management             │
│  - Policy-based access (MiScope integration)        │
│  - Event stream to/from FIWARE Orion-LD             │
├─────────────────────────────────────────────────────┤
│  3D TILE SERVICE (CesiumJS 3D Tiles)                │
│  - OpenStreetMap 3D building data                   │
│  - Community-contributed indoor maps                │
│  - Drone/photogrammetry models (community approved) │
│  - LOD (Level of Detail) streaming                  │
├─────────────────────────────────────────────────────┤
│  GOVERNANCE (What the twin may show)                │
│  - MiScope: who can view which domain's data        │
│  - MiLegal: what resolution is allowed              │
│  - Never: individual people rendered                 │
│  - Never: real-time individual locations             │
│  - Allowed: aggregate flows, building data, env     │
└─────────────────────────────────────────────────────┘
```

### What Members See (Street Tab → "Our Place" View)

- 3D or 2D map of their community
- Color-coded overlays: air quality (green/yellow/red), noise, heat islands
- Resource pins: shelters, food banks, clinics (with MiSource freshness)
- Live data: bus locations (aggregate ETA, not individual bus tracking)
- Historical: "How has air quality changed this month?"
- Quests: "This area needs a sensor — deploy a MiESP node?"

### What Members DO NOT See

- Individual people's locations (ever)
- Real-time movement of specific vehicles (only aggregate transit)
- Inside anyone's home (unless owner explicitly shares)
- Facial recognition data (forbidden — never collected)
- License plate data (forbidden — never collected)

---

## 10.4 Safety Gates (Non-Negotiable)

These cannot be relaxed by vote, steward decision, or community override. They are compact-level.

| # | Safety Gate | Meaning | Enforcement |
|---|-----------|---------|-------------|
| 1 | **Two-person actuation** | Any physical actuator (lock, valve, switch) requires two authorized humans to confirm | MiScope: two distinct DIDs + MiAction with two approvals |
| 2 | **No stranger face-ID** | No camera system that identifies individuals by face. Period. | No face-recognition model deployed. No training data collected. CI gate rejects any FR dependency. |
| 3 | **No silent tracking** | No system that tracks an individual's movement without their active, visible, ongoing consent | Consent must be re-confirmed every 24h. Visual indicator on device when sharing location. |
| 4 | **Sensor transparency** | Every sensor's existence, location, data type, and governance approval is publicly visible in MiNOC | Sensor cannot transmit without registration in Orion-LD + community approval vote reference |
| 5 | **Emergency override** | Life-safety events (fire, flood, structural failure) can bypass two-person rule for evacuation alerts | Override logged, reviewed within 24h by keeper panel. Cannot be used for surveillance. |
| 6 | **Data minimization** | Sensors collect minimum necessary. Aggregate over individual. Purge over retain. | Retention policy enforced: raw data 90 days max. Aggregate 5 years. Individual: never stored. |
| 7 | **Child zones** | Areas where children are present (schools, playgrounds): maximum privacy settings enforced | No audio recording, no individual counting, no photography systems. Environment-only sensors. |
| 8 | **Opt-out zones** | Any member can declare their property a no-sensor zone | Property boundary registered → all community sensors within boundary deactivated |
| 9 | **Actuator rollback** | Any physical action can be manually overridden at the device | Physical override switch required on all actuators. Digital-only control forbidden. |
| 10 | **Audit trail** | Every sensor reading, every actuation, every access to IoT data: logged and auditable | Immutable audit log in TimescaleDB. Steward access. Member can see who viewed their zone's data. |

---

# Inter-OS Coordination

**Purpose:** Show how the 10 OS layers work together as a single organism. No OS operates in isolation. A single member action flows through multiple layers simultaneously.

---

## Worked Example: "Thank Maria 12"

A member says to Mi: "Thank Maria 12 for fixing the gate." Here is how that single action flows through all 10 OS layers:

```
┌─────────────────────────────────────────────────────────────────────────┐
│ STEP 1: OS 5 (AI OS) — Intent Recognition                             │
│ Mi (Ring 0, on-device) classifies: "pocket.thank" intent               │
│ Extracts: recipient="Maria", amount=12, reason="fixing the gate"       │
│ Drafts MiAction envelope (type: pocket.thank)                          │
│ Shows member: "Send 12 $MLY to Maria for fixing the gate? [Confirm]"  │
└───────────────────────────────────┬─────────────────────────────────────┘
                                    │ member confirms
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ STEP 2: OS 2 (Coordination OS) — MiAction Created                      │
│ Full envelope populated:                                                │
│   actor: {did: "did:milyfe:alice", role: "member"}                     │
│   place: {instance: "jacksonville-01", geo: "neighborhood"}            │
│   jurisdiction: {law_pack: "us-fl-duval-v2.3"}                         │
│   audience: {visibility: "named", recipients: ["did:milyfe:maria"]}    │
│   sensitivity: "community"                                              │
│   state: {current: "pending_approval"}                                  │
│   offline: {created_offline: false}                                      │
│   explanation: {human_readable: "You're thanking Maria 12 $MLY"}       │
└───────────────────────────────────┬─────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ STEP 3: OS 2 (Coordination OS) — MiScope Permission Check              │
│ Query: "Can alice transfer 12 $MLY to maria?"                          │
│ Checks:                                                                 │
│   ✓ alice has balance >= 12 in Weekly pot                              │
│   ✓ alice is not frozen                                                │
│   ✓ maria exists and is not frozen                                     │
│   ✓ alice is age-of-majority (no guardian required)                    │
│   ✓ no conflict-of-interest flags                                      │
│ Result: ALLOW                                                           │
└───────────────────────────────────┬─────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ STEP 4: OS 7 (Constitutional OS) — MiLegal Policy Check                │
│ OPA evaluates:                                                          │
│   ✓ Layer 0 (Compact): no violation                                    │
│   ✓ Layer 1 (Platform): pocket transfers allowed                       │
│   ✓ Layer 2-4 (Law): no relevant restrictions on peer transfer         │
│   ✓ Layer 5 (Instance): pocket.peer_swap gate = active                 │
│ Result: ALLOW                                                           │
└───────────────────────────────────┬─────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ STEP 5: OS 6 (Economic OS) — Ledger Execute                            │
│ Ledger adapter (SQL mode):                                              │
│   BEGIN TRANSACTION (SERIALIZABLE)                                      │
│   DEBIT alice.weekly_pot 12                                             │
│   CREDIT maria.thanks_pot 12                                            │
│   INSERT transaction_log (action_id, from, to, amount, reason, ts)     │
│   COMMIT                                                                │
│ State: pending_approval → executed                                      │
│ Fee: 0 (peer-to-peer thanks have no fee)                               │
└───────────────────────────────────┬─────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ STEP 6: OS 2 (Coordination OS) — MiReceipt Generated                   │
│ Two receipts created (W3C VC format):                                  │
│   Alice: "You thanked Maria 12 $MLY for fixing the gate"              │
│   Maria: "Alice thanked you 12 $MLY for fixing the gate"              │
│ Stored: local device SQLite + encrypted vault                          │
│ MiSource attached: confidence=1.0, verified=ledger                     │
└───────────────────────────────────┬─────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ STEP 7: OS 4 (Communication OS) — Delivery                             │
│ Notification to Maria:                                                  │
│   If online: NATS → ntfy push → device notification                   │
│   If offline: MiDTN bundle queued (state: "walking")                   │
│   If mesh-only: BLE/WiFi direct to Maria's device                     │
│ Alice sees: "walking" animation until Maria's device ACKs             │
└───────────────────────────────────┬─────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ STEP 8: OS 8 (Education OS) — Progress Update                          │
│ If Alice is on "Money (Not a Casino)" learn path:                      │
│   Quest credit: "Made a $MLY transaction" → progress tracked          │
│ If Alice has 10+ thanks sent: badge candidate check                    │
└───────────────────────────────────┬─────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ STEP 9: OS 9 (Population OS) — Context-Aware                           │
│ Maria is a single parent → Kin helper notes: "Maria earned 12 $MLY    │
│   today from community help" (private insight for Maria only)          │
│ Alice's neighborhood → MiPulse increments: community activity +1      │
└───────────────────────────────────┬─────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ STEP 10: OS 10 (Physical Universe OS) — Optional                       │
│ If "the gate" is a registered community asset in FIWARE:               │
│   Asset record updated: last_maintained = today, maintainer = maria    │
│   Digital twin: gate status → "repaired"                               │
│ This step only fires if IoT integration is active (MiStage: Canopy)   │
└─────────────────────────────────────────────────────────────────────────┘
```

**Total latency (online, local network):** ~200ms from confirm to executed  
**Total latency (offline, mesh delivery):** ~200ms to execute locally + minutes/hours for delivery notification

---

## Event Bus Architecture (NATS JetStream)

### Why NATS JetStream

- Lightweight (single binary, 10MB RAM baseline)
- Supports: pub/sub, request/reply, queue groups, persistent streams
- JetStream: durable message storage with replay, exactly-once delivery
- Multi-tenant: accounts isolate domains
- Clustering: 3-node RAFT for HA
- Leaf nodes: edge/mesh nodes connect as leaf nodes (bandwidth-efficient)

### Topic Structure

```
milyfe.{instance}.{domain}.{action_type}.{event}

Examples:
milyfe.jacksonville-01.pocket.thank.created
milyfe.jacksonville-01.pocket.thank.executed
milyfe.jacksonville-01.voice.proposal.submitted
milyfe.jacksonville-01.voice.ballot.cast
milyfe.jacksonville-01.safety.report.filed
milyfe.jacksonville-01.mesh.node.online
milyfe.jacksonville-01.iot.sensor.reading
milyfe.jacksonville-01.learn.badge.earned
milyfe.jacksonville-01.federation.standing.updated
```

### Stream Configuration

| Stream | Subjects | Retention | Max Age | Replicas | Consumers |
|--------|----------|-----------|---------|----------|-----------|
| ACTIONS | `milyfe.*.*.*.created/executed/failed` | Limits (100GB) | 90 days | 3 | All services |
| SAFETY | `milyfe.*.safety.*.*` | Limits (10GB) | 1 year | 3 | Safety service + keepers |
| IOT | `milyfe.*.iot.*.*` | Limits (50GB) | 90 days raw, 5yr aggregate | 3 | IoT service + twins |
| FEDERATION | `milyfe.*.federation.*.*` | Limits (10GB) | 30 days | 3 | Federation service |
| NOTIFICATIONS | `milyfe.*.notify.*` | WorkQueue | 7 days | 1 | ntfy + Matrix bridge |

### MiAction as Universal Connector

Every OS layer both produces and consumes MiActions through NATS:

| OS Layer | Produces | Consumes |
|----------|----------|----------|
| OS 1 (Infrastructure) | system.health, system.backup | — (foundational) |
| OS 2 (Coordination) | All MiAction state transitions | All (validates/routes) |
| OS 3 (Internet Services) | content.published, message.sent | moderation.action, scope.check |
| OS 4 (Communication) | mesh.node.online, dtn.bundle.delivered | All actions needing delivery |
| OS 5 (AI) | helper.suggestion, helper.handoff | All actions (for context) |
| OS 6 (Economic) | pocket.transfer.executed, ubi.distributed | pocket.* actions to execute |
| OS 7 (Constitutional) | voice.ballot.cast, proposal.decided | All actions (legal check) |
| OS 8 (Education) | learn.badge.earned, class.published | pocket.*, quest.* (for progress) |
| OS 9 (Population) | safety.alert, peace.table.scheduled | All (population-specific routing) |
| OS 10 (Physical) | iot.reading, twin.updated | scope.check, stage.check |

---

# Phase Triggers

**Purpose:** Define exactly when each OS layer activates and what triggers the transition between community lifecycle stages.

---

## Stage Progression

```
SEED ──► SPROUT ──► ROOT ──► TRUNK ──► CANOPY ──► FOREST ──► ECOSYSTEM
1-10     11-50     51-200   201-1000  1001-5000  5001-25000   25000+
```

## Detailed Phase Triggers

### Seed → Sprout (10 → 11 members)

| Trigger | Type | What Activates |
|---------|------|----------------|
| 11th verified member joins | Automatic (member count) | Learn paths, peer swap gate |
| First circle formed (7+ members) | Automatic (circle count) | Circle governance features |
| 30 days uptime | Automatic (time) | Named helpers (Mi + 3 others) |
| Community vote | Required | Which named helpers to activate |
| Rails audit complete | Required (human) | AI helpers beyond Tool level |

### Sprout → Root (50 → 51 members)

| Trigger | Type | What Activates |
|---------|------|----------------|
| 51st verified member | Automatic | Marketplace, shop POS eligibility |
| MSB legal assessment complete | Required (human) | Shop POS gate unlocked |
| Community vote (60%, 15% quorum) | Required | Shop POS activation |
| Constitution ratified (80% vote) | Required | Binding governance |
| 3 circles active | Automatic | Full circle governance |
| Mesh hardware deployed (3+ nodes) | Automatic | LoRa mesh relay |

### Root → Trunk (200 → 201 members)

| Trigger | Type | What Activates |
|---------|------|----------------|
| 201st verified member | Automatic | Full mesh, treasury spending |
| 90 days at Root stage | Automatic (time) | Federation eligibility |
| All internet services running stable (30 days) | Automatic (health check) | Full OS 3 |
| Community vote | Required | Federation activation |
| MiDTN demonstrated working (10 bundles delivered) | Automatic | DTN as primary offline transport |
| Treasury >1000 $MLY accumulated | Automatic | Community project spending |

### Trunk → Canopy (1000 → 1001 members)

| Trigger | Type | What Activates |
|---------|------|----------------|
| 1001st verified member | Automatic | Chain eligibility, IoT eligibility |
| Test chain running 180 days | Required (time + health) | Live chain activation vote |
| Community vote (75%, 25% quorum) | Required | Live blockchain |
| Regulatory review complete | Required (human) | Chain legal clearance |
| 10 sensors deployed + governance approved | Automatic + vote | IoT activation |
| Two-person actuation verified | Required (safety review) | Physical actuators |

### Canopy → Forest (5000 → 5001 members)

| Trigger | Type | What Activates |
|---------|------|----------------|
| 5001st verified member | Automatic | Full IoT, AI ring routing, city-scale |
| Federation with 2+ instances active | Automatic | Cross-instance governance |
| All 10 learn paths staffed with human teachers | Required (human) | Full education OS |
| GPU infrastructure deployed | Automatic (hardware) | Ring 1 full models (13B+) |
| City-scale treasury (>100,000 $MLY) | Automatic | Full participatory budget |

### Forest → Ecosystem (25000 → 25001 members)

| Trigger | Type | What Activates |
|---------|------|----------------|
| 25001st verified member | Automatic | Multi-city protocol governance |
| 5+ federated instances | Automatic | Protocol-level governance body |
| Community vote (75%, 25% quorum) | Required | Protocol governance participation |
| Cross-instance dispute resolution tested | Required (human) | Federation ombuds active |
| Inter-instance $MLY portability demonstrated | Required (test) | Standing + credit portability |

---

## Community Vote Triggers (Non-Automatic)

Some transitions are NEVER automatic, regardless of member count:

| Gate | Always Requires Vote | Minimum Threshold |
|------|---------------------|-------------------|
| Live blockchain activation | Yes | 75% approval, 25% quorum |
| External ActivityPub federation | Yes | 60% approval, 15% quorum |
| Cloud AI (Ring 2) enablement | Yes | 60% approval, 15% quorum |
| Physical actuator deployment | Yes | 75% approval, 15% quorum |
| Instance blocking/unblocking | Yes | 60% approval, 15% quorum |
| Treasury spend >34% | Yes | 80% approval, 25% quorum |
| Constitutional amendment | Yes | 80% approval, 30% quorum |
| New named helper activation | Yes | 60% approval, 15% quorum |

---

# Mesh-in-a-Box

**Purpose:** Any community, anywhere, can deploy a full MiLyfe instance with one command. No cloud account needed. No DevOps team needed. Electricity and hardware are the only requirements.

---

## One-Command Deployment

```bash
# From any x86_64 or ARM64 machine with 8GB+ RAM:
curl -sSL https://install.milyfe.org | bash -s -- \
  --community-name "Eastside Jacksonville" \
  --admin-passkey-setup \
  --locale en-US \
  --timezone America/New_York
```

**What the script does:**
1. Detects hardware (CPU arch, RAM, storage, GPU if present)
2. Installs K3s (single-node mode for small deployments)
3. Deploys core Helm charts (Seed-stage services only):
   - PostgreSQL (Patroni single-node)
   - NATS (single-node JetStream)
   - Matrix Synapse + Element
   - Keycloak (identity)
   - Forgejo (local code mirror)
   - ntfy (notifications)
   - MiScope gateway
   - Mi helper (Ring 1 if GPU, Ring 0 fallback)
   - CryptPad
   - Traefik (ingress)
   - Prometheus + Grafana (monitoring)
4. Generates instance DID + signing keys
5. Creates first admin account (passkey-based, no password)
6. Configures mesh networking (WiFi AP mode as community hotspot)
7. Runs health check and displays access URL

**Total time:** ~15 minutes on modern hardware, ~30 minutes on Raspberry Pi 5.

---

## Hardware Requirements

### Minimum (1-50 members)

| Component | Specification | Cost |
|-----------|--------------|------|
| CPU | Any x86_64 or ARM64, 4+ cores | — |
| RAM | 8GB minimum | — |
| Storage | 256GB SSD/NVMe | — |
| Network | Ethernet + WiFi | — |
| GPU | Optional (falls back to CPU inference) | — |
| **Example: Raspberry Pi 5 8GB** | + NVMe HAT + 512GB SSD | **~$120** |
| **Example: Mini PC (N100)** | 8GB/512GB SSD | **~$150** |
| **Example: Used business PC** | Dell/HP/Lenovo refurb | **~$100** |

### Recommended (50-500 members)

| Component | Specification | Cost |
|-----------|--------------|------|
| Nodes | 3x (HA cluster) | — |
| CPU per node | 8+ cores | — |
| RAM per node | 16-32GB | — |
| Storage per node | 1TB NVMe | — |
| GPU | 1x RTX 3060+ (AI inference) | ~$250 used |
| **Example: 3x Beelink SER5 Pro** | Ryzen 5, 32GB, 1TB each | **~$900** |

### Full Community (500-5000 members)

| Component | Specification | Cost |
|-----------|--------------|------|
| Nodes | 5-8 (dedicated roles) | — |
| CPU per node | 16+ cores | — |
| RAM per node | 32-64GB | — |
| Storage | NAS with 10TB+ | — |
| GPU | 2-4x (AI + transcoding) | — |
| Network | 10GbE between nodes | — |
| **Example: 5x Minisforum MS-01** | i9, 64GB, 2TB + 4TB NAS | **~$4,000** |

---

## What You Get

A single Mesh-in-a-Box deployment includes:

| Layer | What's Running | Member Experience |
|-------|---------------|-------------------|
| Identity | Keycloak + DID + passkeys | One signup, one profile |
| Messaging | Matrix Synapse + Element | Encrypted DMs and groups |
| Money | PostgreSQL ledger + UBI engine | $MLY in Pocket tab |
| Learning | Kolibri + curriculum content | Learn tab (offline-capable) |
| Marketplace | Street services (basic) | Buy/sell/trade locally |
| Governance | Loomio + basic voting | Voice tab (circle decisions) |
| AI | llama.cpp (CPU or GPU) + Mi helper | Mi assistant always available |
| Mesh | WiFi AP + BLE beacon + optional LoRa | Connect without internet |
| Federation | Ready (activates at MiStage: Trunk) | Talk to other communities (when ready) |
| Monitoring | Prometheus + Grafana | MiNOC community health view |
| Backup | Automated daily to local storage | Data safety |
| Database | PostgreSQL + pgvector + Meilisearch | Fast search, AI retrieval |

---

## Monthly Cost

| Expense | Amount | Notes |
|---------|--------|-------|
| Electricity (1-3 nodes) | $8-24/month | ARM64 nodes: ~$3/month each. x86: ~$8/month each. |
| Internet (optional) | $0-60/month | Required for email + federation. Not required for local mesh operation. |
| Domain name (optional) | $12/year | For public-facing services. mDNS works locally without. |
| Hardware replacement fund | $10/month suggested | Amortize over 5 years |
| **Total (self-hosted, mesh-only)** | **~$8-24/month** | Electricity only |
| **Total (with internet + domain)** | **~$50-100/month** | Full internet-connected instance |

**Comparison:** A comparable commercial platform (Slack + Stripe + WordPress + Zoom + LMS) for 200 members: $500-2000/month in SaaS fees. MiLyfe: $24/month in electricity.

---

## Upgrade Path

```
Single node (Seed) ──► 3-node HA (Sprout/Root) ──► 5+ node cluster (Trunk+)
       │                        │                           │
       │ Add 2 nodes,           │ Add workers,              │ Add GPU, NAS,
       │ run: milyfe-cluster    │ run: milyfe-node join     │ IoT edge nodes
       │ expand                 │ <cluster-token>           │
       ▼                        ▼                           ▼
  Auto-migrates data     Auto-rebalances storage     Services auto-scale
  Zero downtime          Zero downtime               HPA triggers on load
```

---

# Federation Protocol

**Purpose:** Connect independent MiLyfe instances into a network. Each community is sovereign — federation is voluntary, consensual, and revocable. Members benefit from a larger network while retaining local control.

---

## What Travels Between Instances

| Data Type | Protocol | Direction | Consent Required |
|-----------|----------|-----------|-----------------|
| Standing summary (8 facets, score) | MiLyfe Protocol | Bidirectional | Member opt-in |
| Public profile (name, place, badges) | MiLyfe Protocol | Push on request | Member opt-in |
| Direct messages | Matrix S2S | Bidirectional | Sender + recipient |
| Social posts (public) | ActivityPub | Broadcast | Author publishes |
| Marketplace listings (exportable) | MiLyfe Protocol | Pull by browsing instance | Seller opt-in |
| $MLY transfers (cross-instance) | MiLyfe Protocol | Bidirectional | Both members consent |
| Badges/credentials | W3C VC verification | Pull on presentation | Holder presents |
| Event announcements | ActivityPub | Broadcast | Organizer publishes |
| Learning content (shared curriculum) | MiLyfe Protocol | Pull by subscribing instance | Publishing instance approves |

## What Stays Local (Never Leaves the Instance)

| Data Type | Reason |
|-----------|--------|
| Ballot choices | Constitutional privacy (ZK voting — only "voted yes/no" result, never individual choice) |
| Local law packs | Jurisdiction-specific (may not apply elsewhere) |
| Treasury balances (detail) | Local economic sovereignty |
| Child profiles/data | Compact: children first (no federation of child data) |
| Safety reports | Victim privacy (only anonymized statistics federate) |
| Dispute details | Local due process (only "dispute resolved" status federates) |
| Location data | Privacy (no cross-instance tracking) |
| Helper memory | Private to member (never shared with other instances) |
| Device registry | Security (no remote device enumeration) |
| Internal governance deliberations | Local democracy (only decisions federate, not discussion) |

---

## ActivityPub for Social Federation

**Services using ActivityPub:**
- Mastodon (microblogging)
- PeerTube (video)
- Pixelfed (photos)
- Lemmy (link aggregation)
- BookWyrm (books)
- WriteFreely (blogs)
- Funkwhale (music)
- Castopod (podcasts)
- Mobilizon (events)

**Federation policy:**
- Between MiLyfe instances: auto-federate (allowlist maintained by community)
- With external Fediverse: community vote to enable (MiStage: Root minimum)
- Content from external instances: passes MiChildGate and MiModerate before display
- Outbound federation: MiLegal checks (no private/safety content leaks to external)

---

## Custom MiLyfe Protocol ($MLY + Standing Portability)

### Wire Format

```json
{
  "protocol": "milyfe-federation",
  "version": "1.0",
  "message_type": "standing_sync | transfer_request | profile_request | badge_verify | instance_discover",
  "source_instance": {
    "id": "did:milyfe:instance:jacksonville-01",
    "name": "MiLyfe Jacksonville",
    "url": "https://jacksonville.milyfe.community",
    "public_key": "ed25519:..."
  },
  "destination_instance": {
    "id": "did:milyfe:instance:atlanta-01"
  },
  "timestamp": "2026-08-24T15:00:00Z",
  "payload": { },
  "signature": "ed25519_sign(canonical_json_minus_signature)"
}
```

### $MLY Cross-Instance Transfer

```
Alice (Jacksonville) wants to send 50 $MLY to Bob (Atlanta):

1. Alice's instance:
   - Verify Alice has 50 $MLY
   - Debit Alice 50 $MLY
   - Create transfer_request message
   - Sign with instance key
   - Send to Atlanta instance

2. Atlanta's instance:
   - Verify signature (Jacksonville's key is in federation registry)
   - Verify Jacksonville is not blocked
   - Credit Bob 50 $MLY (new issuance on Atlanta's ledger)
   - Send transfer_confirmation back to Jacksonville
   - Bob's receipt: "50 $MLY received from Alice (Jacksonville)"

3. Settlement:
   - Net positions tracked: Jacksonville owes Atlanta 50 $MLY
   - Periodic settlement (weekly): net balances reconciled
   - If imbalance exceeds threshold (5% of smaller instance's supply):
     Settlement freeze until community stewards resolve

4. Failure handling:
   - Timeout (no confirmation in 1 hour): auto-reverse on sender side
   - Instance unreachable: queue in NATS, retry with exponential backoff
   - Disputed: both instances freeze the transaction, escalate to federation ombuds
```

### Standing Portability

```json
{
  "message_type": "standing_sync",
  "payload": {
    "member_did": "did:milyfe:alice123",
    "standing_snapshot": {
      "overall_score": 0.82,
      "facets": {
        "participation": 0.9,
        "contribution": 0.85,
        "reliability": 0.8,
        "peacefulness": 1.0,
        "learning": 0.7,
        "generosity": 0.75,
        "stewardship": 0.6,
        "teaching": 0.5
      },
      "computed_at": "2026-08-24T00:00:00Z",
      "attestation_count": 47,
      "membership_duration_days": 180
    },
    "portable_badges": ["peacemaker-v1", "community-first-responder-v1"],
    "cooling_period_days": 30,
    "source_instance_vouches": true
  }
}
```

**Standing cooling:** When a member moves instances, their standing starts at 70% of ported value. Over 30 days of local activity, it restores to full. This prevents standing farming.

---

## Instance Discovery + Blocking

### Discovery

```
1. New instance comes online
2. Posts discovery announcement to known peers:
   {
     "message_type": "instance_discover",
     "payload": {
       "instance_did": "did:milyfe:instance:miami-01",
       "name": "MiLyfe Miami",
       "url": "https://miami.milyfe.community",
       "member_count": 45,
       "stage": "sprout",
       "compact_version": "1.0",
       "federation_ready": true,
       "public_key": "ed25519:..."
     }
   }
3. Receiving instances verify:
   - Compact version compatible (same major version)
   - Public key validates
   - URL responds to health check
4. Receiving instance adds to registry (pending community approval)
5. Community vote to federate: 60% approval, 15% quorum
```

### Blocking Criteria (Community Vote Required)

| Reason | Vote Threshold | Effect |
|--------|---------------|--------|
| Instance disabled child safety | 60% to block | Full block (no data exchange) |
| Instance allows hate content | 60% to block | Full block |
| Sustained spam/abuse from instance | 60% to block | Full block |
| Economic exploitation (standing farming) | 60% to block | Transfer block (social federation may continue) |
| Compact violation (non-OSI, non-voluntary) | 60% to block | Full block |
| Political disagreement | Cannot block for this reason alone | Blocking requires documented harm, not disagreement |

### Block is reversible: 60% vote to unblock at any time.

---

## Fork Compatibility

**Principle:** If a community forks MiLyfe (their right per Compact item 8), the fork should still be able to communicate with non-forked instances.

### Protocol Versioning

```
Major version: Breaking changes (new required fields, changed semantics)
Minor version: Additive changes (new optional fields, new message types)
Patch version: Bug fixes (no wire format change)

Compatibility rule:
- Same major version → full federation
- Different major version → message translation layer attempted
- Fork with same protocol version → full federation (fork is about governance, not protocol)
- Fork with modified protocol → compatibility assessed case-by-case
```

### What forks CAN change without breaking federation:
- Governance rules (different vote thresholds, different circle sizes)
- Economic parameters (different UBI amount, different decay rate)
- Service selection (use Lemmy instead of Discourse)
- UI/UX (completely different client)
- Law packs (different jurisdiction, different local policies)
- Helper names and personalities

### What forks CANNOT change and still federate:
- MiAction envelope schema (this IS the protocol)
- MiReceipt format (W3C VC — standard)
- Standing facet structure (8 facets)
- Cryptographic primitives (Ed25519, Semaphore circuits)
- Child safety gates (Compact item: cannot be removed)

---

## Person Migration (Export → Import with Standing Cooling)

### Full Migration Flow

```
MEMBER DECIDES TO MOVE (Jacksonville → Atlanta)

Phase 1: EXPORT (from source instance)
├── Member requests full data export
├── Exported package contains:
│   ├── Profile (DID, name, bio, avatar, settings)
│   ├── Standing snapshot (attested by source instance)
│   ├── Badges (W3C VCs — self-contained, verifiable anywhere)
│   ├── Transaction history (MiReceipts as JSON-LD)
│   ├── Learn progress (modules completed, badges earned)
│   ├── Message history (encrypted — only member can decrypt)
│   ├── Personal vault contents (files, documents)
│   ├── Contacts list (DIDs of connections)
│   └── Governance participation record (proposals voted on, not choices)
├── Package signed by source instance
├── Format: encrypted zip with member's key
└── Size limit: none (their data, their right)

Phase 2: TRANSIT
├── Member carries export package (file, USB, cloud upload)
├── Source instance marks member as "migrating" (not deleted yet)
├── 30-day grace period: member can return and cancel migration
└── During grace: member has read-only access to source, no voting/spending

Phase 3: IMPORT (to destination instance)
├── Member presents export package to destination
├── Destination verifies:
│   ├── Source instance signature valid
│   ├── Package integrity (hash check)
│   ├── Member DID matches
│   └── No active bans/disputes blocking migration
├── Profile created on destination
├── Standing imported at 70% (cooling period: 30 days)
├── Badges imported (independently verifiable via W3C VC)
├── Learn progress imported (resume where left off)
├── Message history: stored locally (cannot be searched by new instance)
├── Contacts: notified of new instance location (if they consent)
└── Governance: starts fresh (no voting weight carried, must participate locally)

Phase 4: COMPLETION
├── After 30 days: source instance deletes member data
├── Member confirms: "I'm settled" → source account purged
├── Standing cooling completes (back to full ported value)
├── Member is fully integrated in new community
└── Old instance retains: anonymized contribution records (for community history)
```

### Constraints

- Member can only be in ONE instance at a time (no multi-instance farming)
- Migration cooldown: cannot migrate again for 90 days (prevents gaming)
- Active disputes: must be resolved before migration (cannot flee accountability)
- Negative standing: migrates too (you cannot reset by moving)
- Children: guardian must migrate with them OR explicitly transfer guardianship

---

## End of Document

This document describes the complete sovereign infrastructure architecture for MiLyfe. It is a living document — as the platform evolves through its lifecycle stages (Seed → Ecosystem), sections will be expanded, revised, and refined through the governance process described in OS 7.

**What this document does NOT contain:**
- Implementation code (that lives in the multi-repo described in OS 1)
- UI/UX specifications (see MiLyfe_UI_UX_Blueprint.md)
- Build timeline (see MiLyfe_Build_Roadmap.md)
- Feature descriptions visible to members (see MiLyfe_Ultimate_Manual.md)

**Authority chain:** Ultimate Manual (WHAT + WHY) → This document (HOW) → Code (IMPLEMENTATION)

---

*Document version 1.0 — 24 August 2026*
