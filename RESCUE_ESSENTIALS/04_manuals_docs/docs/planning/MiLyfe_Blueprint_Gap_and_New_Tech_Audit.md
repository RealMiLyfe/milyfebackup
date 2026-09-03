# MiLyfe — Cross-Blueprint Gap & New-Technology Audit

**Compared:** `MiLyfe_COMPLETE.md` and `MiLyfe_UI_UX_Blueprint.md`  
**Date:** August 18, 2026  
**Purpose:** Identify what is still unspecified, what can be assembled from existing open-source systems, and what MiLyfe genuinely needs to create.

---

# 1. Overall finding

The two blueprints now describe the **vision, rights, daily experience, safety posture, architecture, screens, edge cases, and open-source foundation** unusually well.

The largest remaining gap is not another member-facing feature. It is the **trustworthy coordination layer between the interface and all the existing systems**.

Today the documents say things such as:

- “Only these people can see this.”
- “This action is still walking.”
- “A human must decide.”
- “This resource was verified recently.”
- “This role expires.”
- “This person may appeal.”
- “The same profile works after moving.”
- “A stricter jurisdiction wins.”

Existing projects can perform parts of those promises, but no single existing project enforces them consistently across identity, Pocket, learning, Street, Voice, safety, shops, helpers, mesh, shared devices, and offline use.

**The key invention MiLyfe needs is a common human-action protocol—not another general social network, wallet, LMS, or AI framework.**

---

# 2. What does not need to be invented

MiLyfe should assemble and brand these beneath its experience rather than rebuilding them:

| Capability | Existing foundation is sufficient | MiLyfe’s work |
|---|---|---|
| Web/mobile runtime | React, React Native, Expo | Common MiLyfe experience and accessibility rules |
| Accessible primitives | React Aria or Radix; native platform controls | MiLyfe design system and human testing |
| Identity cryptography | DIDKit, Aries, WebAuthn/passkeys, hardware keys | Plain identity and recovery orchestration |
| General authentication | Keycloak/Authentik/SuperTokens where appropriate | One-profile UX and local/offline bridge |
| Messaging | Matrix plus DTN/Reticulum/Meshtastic layers | Audience, child, safety, and delivery-state rules |
| Learning | Kolibri, Moodle, Open edX, Open Badges | One learning journey and place-needs matching |
| Maps | OpenStreetMap and MapLibre | Privacy zones, resource freshness, offline packs |
| Governance discussion | Decidim, Loomio, Polis | MiLyfe proposal lifecycle and plain-language wrapper |
| Verifiable voting | Helios/MACI/Snapshot components where suitable | Local eligibility, delegation, stages, receipts, appeals |
| Commerce/operations | ERPNext, Saleor, UniCenta, Open Food Network | Small-shop mode and `$MLY` stage rules |
| Forms/legal packets | Docassemble | Local source/date labels and human handoff |
| AI runtime | llama.cpp, Ollama, LocalAI, governance toolkits | Mi rails, disclosure, memory, citations, handoff |
| Policy evaluation | OPA | Signed MiLegal packs and human-readable explanations |
| Infrastructure | Forgejo, K3s, OpenTofu, OpenBao, Woodpecker | MiGit packaging, safe defaults, and operations |
| Accessibility testing | axe-core, Playwright, Storybook | Manual testing with disabled people |
| Security scanning | OSV-Scanner, Dependency-Check, SBOM/Sigstore tools | MiCompat admission and release policy |

These are engines. They are not the member product.

---

# 3. New technology MiLyfe should build

Only capabilities that close a cross-platform hole deserve a new Mi name. The following are genuine gaps rather than decorative brands.

## P0 — Required for a safe first product

## 3.1 MiAction — common human-action protocol

**Hole:** Every module currently invents its own draft, approval, consent, send, offline, expiry, review, and appeal behavior.

**Build:** A common action envelope used by Pocket, Voice, Story, safety, shops, identity, roles, and Mi.

Every action carries:

- Actor and role
- Place and jurisdiction
- Intended audience
- Purpose
- Data sensitivity
- Draft/sent/walking/arrived/failed state
- Required human approvals
- Consent receipt
- Source and policy version
- Expiration
- Reversal rules
- Appeal route
- Offline conflict rule
- Human-readable explanation

**Why existing tools are insufficient:** Workflow engines can move tasks, policy engines can allow/deny, and ledgers can record events; none supplies MiLyfe’s complete human-rights semantics across all modules.

**Member-visible result:** Screens consistently say what happened, who can see it, whether it moved, who must agree, when it ends, and how to challenge it.

## 3.2 MiScope — relationship, permission, and consent graph

**Hole:** The UI blueprint requires a detailed permission matrix, but the underlying architecture has no single cross-module authorization model for household, child, shop, recovery, teacher, keeper, mediator, auditor, helper, and temporary roles.

**Build:** A purpose-bound permission graph with:

- Person-to-person and person-to-place relationships
- Object-level audiences
- Time-limited roles
- Required second-person approvals
- Youth assent plus guardian permission
- Emergency exceptions
- Conflict-of-interest markers
- Revocation and appeal
- “What can this person see?” preview
- Local/offline policy cache

**Foundation:** OPA can evaluate rules; relationship-based authorization projects can store parts of the graph. MiScope is the MiLyfe-specific model and explanation layer.

## 3.3 MiReceipt — understandable proof of every consequential action

**Hole:** Cryptographic receipts, policy logs, consent records, votes, and offline sends are currently separate concepts.

**Build:** One human-readable receipt format for:

- Thanks and jar movements
- Private-ballot participation
- Story publication and removal
- Consent
- Role assignment
- Recovery request
- Helper-to-human handoff
- Report/moderation decision
- Data access
- Export/leave

A receipt answers: **What happened? What did not happen? Who can see it? Which policy applied? Can it be undone? When does it expire? How do I appeal?**

MiReceipt should be portable, printable, translatable, cryptographically verifiable where useful, and understandable without exposing keys or ballot choices.

## 3.4 MiWalk — offline action and conflict engine

**Hole:** MiDTN transports data, but transport does not resolve the meaning of two conflicting offline actions.

**Build:** A cross-module offline state machine for:

- Pocket movements
- Ballots near a deadline
- Role changes
- Block/report actions
- Resource updates
- Child and safety settings
- Recovery requests
- Shop sales/refunds
- Story additions/removals

It defines what may occur offline, reservation rules, ordering, expiry, reconciliation, user notification, and mandatory human review.

**Critical distinction:** MiDTN answers “How does the message travel?” MiWalk answers “What does the product do when the delayed actions disagree?”

## 3.5 MiSource — provenance, freshness, and correction protocol

**Hole:** The UX promises reliable shelters, food, legal links, shops, classes, law packs, helper citations, and public facts. The architecture does not define one freshness system.

**Build:** A provenance envelope containing:

- Source and responsible maintainer
- Place/jurisdiction
- Verification method
- Checked date
- Expiration
- Confidence
- Language/translation source
- Accessibility status
- Correction history
- Safe behavior when stale

MiSource must feed Street, Search, Mi, Rue, Learn, shop pages, law packs, and emergency resources.

## 3.6 MiHandoff — helper-to-human case routing

**Hole:** “Ask a person” appears throughout the UX, but no shared technology routes the request safely.

**Build:** A local-first handoff layer that matches:

- Need and urgency
- Human role and license where required
- Language
- Accessibility
- Place/jurisdiction
- Availability
- Conflicts of interest
- Minimum necessary context
- Consent to share
- Response target
- Escalation and closure

It must work without giving Mi or a universal admin access to the member’s full profile.

## 3.7 MiAppeal — due-process and correction engine

**Hole:** Appeals are promised for personhood, moderation, place bans, helper actions, shop disputes, standing scars, and money reviews, but they have no unified process.

**Build:** A reusable case flow with:

- Notice and reason
- Evidence available to each side
- Translation/accessibility support
- Reviewer independence
- Conflict disclosure
- Time limits
- Interim restrictions
- Member response
- Decision and remedy
- Escalation
- Retention/forgetting rule
- Export during the case

This is not a court. It is association-level due process and correction.

## 3.8 MiShared — safe shared-device and kiosk shell

**Hole:** Shared-device safety is specified in UX but is not an ordinary feature of identity, messaging, maps, helpers, or learning platforms.

**Build:** A device mode coordinating:

- Neutral notifications
- No sensitive search history
- Per-person local vault separation
- Safe session clearing
- Kiosk timeout and handoff
- Download destination warnings
- Read-aloud privacy
- Cached location removal
- Panic freeze
- Recovery without exposing another member
- Child/adult switching without shared secrets

This should be a shell used by all modules, not separate settings in each one.

## P1 — Required before Practice Town becomes broad

## 3.9 MiPlaceShift — portable profile and jurisdiction transition

**Hole:** The blueprints promise that a person can visit, live across places, move, retain selected badges, cool local standing, and receive different lawful features.

**Build:** A transition protocol that previews and applies:

- Old/new place membership
- Law-pack differences
- Money-stage differences
- Voice eligibility
- Pending offline actions
- Resource and learning packs
- Household split moves
- Selected portable attestations
- Local standing cooling
- Data residency and replication

It must avoid silently geo-locking a person or claiming that a peer payment is controlled by the app.

## 3.10 MiKinship — household, guardian, care, and separation graph

**Hole:** MiScope can authorize, but family/care relationships have special lifecycle and safety needs.

**Build:** A domain layer for:

- Household membership
- Guardian and youth relationships
- Youth assent
- Temporary/foster caregivers
- Adult dependents
- Shared devices and jars
- Separation and abuse-safe split
- Incapacity and death
- Age transitions
- Conflicting lawful orders

This should not create a “head of household” superuser.

## 3.11 MiModerate — federated safety and moderation protocol

**Hole:** Matrix, ActivityPub, forums, Street, Story, shops, classes, and Voice all moderate differently.

**Build:** A common report/block/restrict/appeal interface with:

- Cross-surface blocking
- Child-safety priority
- Immediate-threat separation
- Evidence minimization
- Local/community scope
- Federation notices
- Proportional actions
- Independent appeal through MiAppeal
- Public transparency statistics with privacy thresholds

Public illegal-content duties and private encrypted communications remain technically and legally distinct.

## 3.12 MiDelegate — constrained civic delegation

**Hole:** Existing liquid-voting tools do not necessarily implement MiLyfe’s topic-specific, expiring, privacy-preserving, concentration-aware delegation.

**Build:** Delegation with:

- Topic and place scope
- Expiry
- Immediate revocation
- No silent re-delegation
- Conflict disclosures
- Privacy-preserving concentration warnings
- Proof the delegate acted without revealing a secret vote
- Accessible offline-aware deadline behavior

## 3.13 MiStage — Practice versus Live capability assurance

**Hole:** A configuration flag alone is too weak to prevent Practice shares, sample court papers, simulated decisions, or test resources from being mistaken for live systems.

**Build:** A signed capability manifest and persistent stage presentation used by every screen, receipt, export, notification, map, shop till, and API boundary.

MiStage fails closed when components disagree. It should make it technically difficult—not merely stylistically discouraged—to move Practice objects into Live.

## 3.14 MiNotify — privacy-aware notification router

**Hole:** Safety, legal deadlines, money, messages, child activity, and shared devices require different lock-screen exposure and delivery urgency.

**Build:** A policy-bound router that understands sensitivity, device ownership, recipient role, local/offline path, quiet hours, neutral preview, acknowledgement, escalation, and expiry.

It prevents each module from leaking sensitive meaning through notification text.

## 3.15 MiRender — one content package across app, print, SMS, voice, and offline

**Hole:** The UX promises accessible non-app channels, but ordinary content systems do not preserve the same source, freshness, audience, and safety meaning across all formats.

**Build:** A structured content renderer for:

- App/web
- Printable packets
- Screen reader/read-aloud
- SMS summaries
- Voice/IVR prompts
- Low-bandwidth voice mail
- Kiosk
- Offline lesson/resource packs

A MiSource record and MiReceipt meaning must survive every rendering.

## P2 — Important for scale and long-term ownership

## 3.16 MiUXKit — enforceable human-interface system

**Hole:** The blueprint defines design laws, but a normal component library does not enforce MiPlain language, child rules, audience labels, stage badges, helper disclosure, and offline truth.

**Build:** A design system and content contract containing:

- Accessible components and states
- Mandatory audience/source/stage patterns
- MiPlain checks
- RTL and large-text behavior
- Dark/high-contrast themes
- Crisis patterns
- Story and child-safe patterns
- Shared-device behavior
- Printable equivalents

This is a custom layer above React Aria/React Native—not a replacement for them.

## 3.17 MiScenario — rights and failure simulator

**Hole:** MiSandbox simulates proposals, but the full system needs repeatable human-impact simulations.

**Build:** Scenario packs that test:

- Abusive recovery person
- Child contacted by unknown adult
- Conflicting offline money
- Stale shelter information
- Helper hallucinated deadline
- Place-law change
- Captured keeper group
- Shared-device leak
- Screen-reader destructive action
- Partial network failure
- Practice/Live contamination

It should validate policy, UI states, role rules, notifications, receipts, and appeals together before release.

## 3.18 MiLifecycle — retention, migration, and deletion coordinator

**Hole:** MiArchive names retention versus forgetting, but no cross-system lifecycle engine is specified.

**Build:** A data-purpose registry and coordinator that knows:

- Why each data item exists
- Device/place/commons location
- Retention period
- Legal hold
- Consent withdrawal
- Story removal
- Account departure
- Death/stewardship
- Backup and replica deletion
- Export format and version
- Schema migration

It orchestrates existing storage systems without pretending every public or peer-held copy can be erased.

## 3.19 MiCompat UX profile

**Hole:** MiCompat checks software licenses, but “safe GitHub” also requires maturity, privacy, accessibility, maintenance, and replacement readiness.

**Expand MiCompat** rather than create another brand. Each dependency receives:

- Exact version and license
- Transitive-license result
- Security-policy status
- Known critical vulnerabilities
- Maintainer/activity signal
- Telemetry/network behavior
- Accessibility impact
- Offline impact
- Data categories touched
- Replacement plan
- Last human review

“OSI-OK” alone must not mean “approved for a child, wallet, or safety flow.”

---

# 4. Important specifications still missing from both blueprints

These are not necessarily new technology. They are decisions and operational artifacts that must exist before implementation.

## 4.1 Filled role-and-permission matrix

The UX blueprint says this is required but does not yet contain the actual object-by-role matrix. This should be completed before detailed wireframes because permissions change screen layout and available actions.

## 4.2 Canonical content and event model

The documents list event names, but do not fully define shared objects and lifecycle states for:

Person · Place · Household · Role · Relationship · Audience · Consent · Source · Resource · Message · Action · Receipt · Case · Appeal · Lesson · Class · Shop · Item · Jar · Proposal · Ballot · Story · Pulse condition · Device · Export.

Without a canonical model, each open-source integration will describe the same human differently.

## 4.3 Actual service blueprints

The UI blueprint requires backstage maps but does not yet contain the filled maps for recovery, leave-now, personhood, child report, human handoff, offline Pocket, shop dispute, and binding proposal.

## 4.4 Human operating model

The platform still needs named answers for:

- Who verifies shelters and legal resources?
- Who responds when “I need a person” is selected?
- Who may review a child report?
- Who funds after-hours coverage?
- Who handles an appeal if all local reviewers conflict?
- What happens when no qualified human exists locally?
- What response times are honest?

Software cannot manufacture available humans.

## 4.5 Data-classification and retention table

Every object needs classification, storage location, encryption, audience, replication, retention, export, deletion, legal-hold, and incident rules.

## 4.6 Federation and fork compatibility

“People can fork” is promised, but the documents need a user-level answer to:

- Can two forks still message?
- How does a person move between them?
- What happens to `$MLY`, receipts, standing, and consent?
- How are harmful or incompatible instances blocked?
- Which protocol versions interoperate?
- Who tells the user that a fork changed a right?

## 4.7 Recovery when the whole place fails

Device recovery is described. Place-level recovery is not complete. Define what happens if a local instance disappears, keepers collude, signing keys are lost, or the place is physically destroyed.

## 4.8 Hardware and radio interaction design

The architecture contains extensive device and mesh technology, but the member experience for adding, sharing, repairing, retiring, transferring, and safely disposing of a node is not designed.

## 4.9 Economic abuse and coercion patterns

Add explicit UX policy for forced transfers, household financial control, employer pressure to accept `$MLY`, vote buying, peace-reward coercion, shop collusion, and predatory public doorways.

## 4.10 Model and content update governance

The blueprints need a visible path for changed helper models, changed law packs, withdrawn learning content, translation corrections, and security updates—especially when an old offline device reconnects after months.

## 4.11 Accessibility ownership

Accessibility is a release blocker, but the operating model must define who has stop-ship authority, how disabled reviewers are compensated, and how local forks are prevented from silently weakening core access patterns.

## 4.12 Brand architecture at scale

The documents contain many `Mi*` names. Member UI intentionally hides most of them. A registry should mark every name as:

- Member-facing
- Role-facing
- Builder-facing
- Protocol/internal
- Retired/alias

Without this, new technology names will recreate the module explosion the UX is designed to avoid.

---

# 5. Recommended consolidation

Do not expose all new technology names to members. Organize them internally into four planes:

## Human plane

MiAction · MiReceipt · MiAppeal · MiHandoff · MiUXKit

## Trust plane

MiScope · MiSource · MiStage · MiCompat · MiLifecycle

## Continuity plane

MiWalk · MiShared · MiPlaceShift · MiNotify · MiRender

## Community plane

MiKinship · MiModerate · MiDelegate · MiScenario

Members still see only:

**Pocket · Learn · Street · Voice · You · Mi**

The new names belong in MiGit, architecture diagrams, and builder documentation—not the primary interface.

---

# 6. Build priority

## Before first interactive prototype

1. Fill the role-and-permission matrix.
2. Define canonical objects, audiences, and states.
3. Specify MiAction, MiScope, and MiReceipt.
4. Fill the recovery and leave-now service blueprints.
5. Establish MiUXKit component/content contracts.

## Before Lab with multiple people

6. Build MiShared basics.
7. Build MiSource for local resources.
8. Build MiHandoff with at least one real human path.
9. Build MiWalk for messages and non-money actions.
10. Build MiAppeal minimum viable case flow.

## Before Practice Town

11. Extend MiWalk to Pocket and ballots.
12. Build MiStage and Practice/Live isolation.
13. Build MiModerate and child-safety routing.
14. Build MiPlaceShift and MiKinship lifecycle flows.
15. Build MiScenario integrated rights/failure tests.
16. Fill the federation and place-failure plan.

## Before Live transferable `$MLY`

17. Independent legal and security review.
18. Economic coercion and dispute tests.
19. Complete reversible/irreversible receipt language.
20. Offline double-action resolution tested with real low-connectivity users.
21. Doorway/shop compliance and predatory-ramp reporting.
22. Place-level key and continuity recovery drill.

---

# 7. Free, OSI-open-source GitHub foundation for the new systems

## 7.1 Admission rule

“Premium” here means **mature, high-quality, self-hostable, and suitable for serious evaluation**—not a paid edition. Every project below has a free OSI-licensed foundation at the time of this audit. This is a candidate register, not a permanent safety certification.

Before adoption, MiCompat must verify the **exact commit, exact package, transitive licenses, security advisories, telemetry, accessibility, maintenance, and replacement path**. A repository may change its license or move features into a non-OSI directory later.

### Status labels

- **DEFAULT** — first project to prototype
- **ALTERNATE** — credible substitute or specialist component
- **ADAPTER** — useful beneath MiLyfe but not the product model
- **EVALUATE** — promising, but requires stronger review or has licensing/packaging boundaries
- **DO NOT DEFAULT** — technically relevant but mixed, non-OSI, retired, or unsuitable for a core promise

No GitHub repository is “safe forever.” Safety comes from the admission gate, pinned releases, testing, signing, updates, incident response, and human review.

---

## 7.2 MiAction — action envelopes and workflow

| Status | Project | GitHub | License | Best use in MiLyfe |
|---|---|---|---|---|
| DEFAULT | Temporal | [temporalio/temporal](https://github.com/temporalio/temporal) | MIT | Durable action workflows, retries, timers, human wait states |
| DEFAULT | Open Policy Agent | [open-policy-agent/opa](https://github.com/open-policy-agent/opa) | Apache-2.0 | Policy decisions on each action |
| DEFAULT | CloudEvents specification | [cloudevents/spec](https://github.com/cloudevents/spec) | Apache-2.0 | Standard event envelope beneath MiAction |
| DEFAULT | JSON Schema | [json-schema-org/json-schema-spec](https://github.com/json-schema-org/json-schema-spec) | Academic/permissive specification terms; verify | Validate portable action objects |
| ALTERNATE | Flowable | [flowable/flowable-engine](https://github.com/flowable/flowable-engine) | Apache-2.0 | BPMN/DMN human workflow where visual process modeling helps |
| ALTERNATE | NATS Server | [nats-io/nats-server](https://github.com/nats-io/nats-server) | Apache-2.0 | Lightweight event transport |
| ALTERNATE | Apache Kafka | [apache/kafka](https://github.com/apache/kafka) | Apache-2.0 | Large-scale ordered event streams |
| ADAPTER | OpenTelemetry | [open-telemetry/opentelemetry-specification](https://github.com/open-telemetry/opentelemetry-specification) | Apache-2.0 | Operational traces without storing private action content |
| ADAPTER | AsyncAPI | [asyncapi/spec](https://github.com/asyncapi/spec) | Apache-2.0 | Document event contracts |

**Build rather than adopt:** MiAction’s rights, audience, consent, approval, expiry, reversibility, offline, and appeal schema. Temporal or Flowable runs the workflow; it does not define the human promise.

---

## 7.3 MiScope and MiKinship — authorization, relationships, consent

| Status | Project | GitHub | License | Best use in MiLyfe |
|---|---|---|---|---|
| DEFAULT | OpenFGA | [openfga/openfga](https://github.com/openfga/openfga) | Apache-2.0 | Relationship-based permissions; official material identifies it as free and Apache-2.0 |
| DEFAULT | OPA | [open-policy-agent/opa](https://github.com/open-policy-agent/opa) | Apache-2.0 | Purpose, place, legal, child, and stage policy |
| ALTERNATE | SpiceDB | [authzed/spicedb](https://github.com/authzed/spicedb) | Apache-2.0 | High-assurance relationship permissions and consistency |
| ALTERNATE | Ory Keto | [ory/keto](https://github.com/ory/keto) | Apache-2.0 | Zanzibar-style relationship authorization |
| ALTERNATE | Cerbos | [cerbos/cerbos](https://github.com/cerbos/cerbos) | Apache-2.0 | Application authorization with policy-as-code |
| ALTERNATE | Casbin | [casbin/casbin](https://github.com/casbin/casbin) | Apache-2.0 | Embedded RBAC/ABAC where a service is too heavy |
| ALTERNATE | Cedar | [cedar-policy/cedar](https://github.com/cedar-policy/cedar) | Apache-2.0 | Formally structured application authorization policies |
| ADAPTER | OPAL | [permitio/opal](https://github.com/permitio/opal) | Apache-2.0 | Distribute policy data to OPA/Cedar; recheck current repository boundaries |
| ADAPTER | Keycloak | [keycloak/keycloak](https://github.com/keycloak/keycloak) | Apache-2.0 | Authentication, OIDC, WebAuthn, sessions; official repository remains Apache-2.0 |

**Selection:** Start with **OpenFGA + OPA**. Evaluate SpiceDB if strict relationship-consistency requirements justify additional operational complexity.

**Build rather than adopt:** MiLyfe relationship vocabulary, youth assent, guardian limitations, abuse-safe separation, temporary care, role expiry, visibility previews, and appeals.

---

## 7.4 MiReceipt — credentials, signatures, transparency, portable proof

| Status | Project | GitHub | License | Best use in MiLyfe |
|---|---|---|---|---|
| DEFAULT | TrustBloc VCS | [trustbloc/vcs](https://github.com/trustbloc/vcs) | Apache-2.0 | Issue and verify W3C Verifiable Credentials; official repository states Apache-2.0 |
| DEFAULT | in-toto | [in-toto/in-toto](https://github.com/in-toto/in-toto) | Apache-2.0 | Signed supply/action attestations and provenance concepts |
| DEFAULT | Sigstore Cosign | [sigstore/cosign](https://github.com/sigstore/cosign) | Apache-2.0 | Sign and verify release/action artifacts |
| ALTERNATE | Veramo | [decentralized-identity/veramo](https://github.com/decentralized-identity/veramo) | Apache-2.0 | JavaScript DID/VC framework |
| ALTERNATE | Hyperledger Aries Cloud Agent Python | [openwallet-foundation/acapy](https://github.com/openwallet-foundation/acapy) | Apache-2.0 | Credential exchange and DIDComm; verify current foundation/repository path |
| ALTERNATE | DIDKit | [spruceid/didkit](https://github.com/spruceid/didkit) | Apache-2.0 / MIT components; verify exact crate | DID and credential operations on devices |
| ALTERNATE | immudb | [codenotary/immudb](https://github.com/codenotary/immudb) | Apache-2.0 | Tamper-evident append-only records where required |
| ADAPTER | Trillian | [google/trillian](https://github.com/google/trillian) | Apache-2.0 | Verifiable transparency log |
| ADAPTER | Rekor | [sigstore/rekor](https://github.com/sigstore/rekor) | Apache-2.0 | Transparency log for public artifacts—not private member actions |

**Build rather than adopt:** The MiReceipt human-readable format and its privacy rules. Do not put health, child, abuse, location, private ballot choice, or private-message content in a public transparency log.

---

## 7.5 MiWalk — local-first data and offline reconciliation

| Status | Project | GitHub | License | Best use in MiLyfe |
|---|---|---|---|---|
| DEFAULT | Automerge | [automerge/automerge](https://github.com/automerge/automerge) | MIT | Local-first CRDT state with change history; repository was active in August 2026 |
| DEFAULT | SQLite | [sqlite/sqlite](https://github.com/sqlite/sqlite) | Public domain | Reliable device-local structured storage |
| DEFAULT | PouchDB | [pouchdb/pouchdb](https://github.com/pouchdb/pouchdb) | Apache-2.0 | Browser/device document storage and CouchDB replication |
| DEFAULT | Apache CouchDB | [apache/couchdb](https://github.com/apache/couchdb) | Apache-2.0 | Replication endpoint for appropriate non-secret documents |
| ALTERNATE | Yjs | [yjs/yjs](https://github.com/yjs/yjs) | MIT | Collaborative text and structured shared editing |
| ALTERNATE | Loro | [loro-dev/loro](https://github.com/loro-dev/loro) | MIT | Local-first CRDT evaluation; newer than Yjs/Automerge |
| ALTERNATE | WatermelonDB | [Nozbe/WatermelonDB](https://github.com/Nozbe/WatermelonDB) | MIT | React Native local database patterns |
| ALTERNATE | RxDB core | [pubkey/rxdb](https://github.com/pubkey/rxdb) | Apache-2.0 core | Reactive local database; audit premium/plugin boundaries before use |
| ADAPTER | Syncthing | [syncthing/syncthing](https://github.com/syncthing/syncthing) | MPL-2.0 | User-controlled file synchronization, not transactional Pocket state |
| ADAPTER | Eclipse zenoh | [eclipse-zenoh/zenoh](https://github.com/eclipse-zenoh/zenoh) | EPL-2.0 / Apache-2.0 components; verify | Edge/offline data movement across constrained networks |

Research comparing current CRDT options describes Yjs, Automerge, and Loro as MIT-licensed and actively maintained. Automerge’s official repository describes its purpose as local-first persistence and synchronization.

**Never allow a generic CRDT to resolve money, guardianship, moderation, or a binding ballot automatically.** MiWalk must classify mergeable, rejectable, reservable, expiring, and human-review actions.

---

## 7.6 MiSource — provenance, freshness, lineage, correction

| Status | Project | GitHub | License | Best use in MiLyfe |
|---|---|---|---|---|
| DEFAULT | OpenLineage | [OpenLineage/OpenLineage](https://github.com/OpenLineage/OpenLineage) | Apache-2.0 | Provenance/lineage event vocabulary |
| DEFAULT | OpenMetadata | [open-metadata/OpenMetadata](https://github.com/open-metadata/OpenMetadata) | Apache-2.0 | Context catalog, ownership, quality, lineage; official repository confirms Apache-2.0 |
| DEFAULT | in-toto | [in-toto/in-toto](https://github.com/in-toto/in-toto) | Apache-2.0 | Signed provenance |
| ALTERNATE | DataHub | [datahub-project/datahub](https://github.com/datahub-project/datahub) | Apache-2.0 | Large-scale metadata catalog and ownership |
| ALTERNATE | Apache Atlas | [apache/atlas](https://github.com/apache/atlas) | Apache-2.0 | Metadata governance and classification |
| ALTERNATE | Marquez | [MarquezProject/marquez](https://github.com/MarquezProject/marquez) | Apache-2.0 | OpenLineage reference backend |
| ADAPTER | frictionless-py | [frictionlessdata/frictionless-py](https://github.com/frictionlessdata/frictionless-py) | MIT | Validate tabular resource packages |
| ADAPTER | Great Expectations | [great-expectations/great_expectations](https://github.com/great-expectations/great_expectations) | Apache-2.0 | Data-quality expectations; inspect current package boundaries |
| ADAPTER | Schematron | [Schematron/schematron](https://github.com/Schematron/schematron) | MIT | Rule validation for structured documents |

**Build rather than adopt:** Street-resource freshness, emergency expiry, translator/source labels, safe stale behavior, member correction, and place/jurisdiction semantics.

---

## 7.7 MiHandoff and MiAppeal — human support and cases

| Status | Project | GitHub | License | Best use in MiLyfe |
|---|---|---|---|---|
| DEFAULT | Zammad | [zammad/zammad](https://github.com/zammad/zammad) | AGPL-3.0 | Mature self-hosted case/help desk; official repository confirms AGPLv3 and foundation ownership |
| DEFAULT | Temporal | [temporalio/temporal](https://github.com/temporalio/temporal) | MIT | Durable timers, escalations, independent review, expiry |
| DEFAULT | Matrix Synapse | [element-hq/synapse](https://github.com/element-hq/synapse) | AGPL-3.0 | Consent-based member/human support rooms |
| ALTERNATE | FreeScout | [freescout-helpdesk/freescout](https://github.com/freescout-helpdesk/freescout) | AGPL-3.0 | Lighter shared inbox; review modules individually |
| ALTERNATE | osTicket | [osTicket/osTicket](https://github.com/osTicket/osTicket) | GPL-2.0 | Simple, mature ticketing |
| ALTERNATE | GLPI | [glpi-project/glpi](https://github.com/glpi-project/glpi) | GPL-3.0 | Cases plus service/asset operations; official repo includes a security policy |
| ALTERNATE | Request Tracker | [bestpractical/rt](https://github.com/bestpractical/rt) | GPL-2.0 | Mature request and escalation tracking |
| ADAPTER | Jitsi Meet | [jitsi/jitsi-meet](https://github.com/jitsi/jitsi-meet) | Apache-2.0 | Human video handoff when bandwidth allows |
| ADAPTER | BigBlueButton | [bigbluebutton/bigbluebutton](https://github.com/bigbluebutton/bigbluebutton) | LGPL-3.0 | Accessible group/class support rooms |
| DO NOT DEFAULT | Chatwoot whole repository | [chatwoot/chatwoot](https://github.com/chatwoot/chatwoot) | MIT core plus separately licensed enterprise directory | High-quality core, but not license-pure as a whole; use only after a directory/package-level MiCompat review |

**Selection:** Zammad for case handling plus Temporal for MiLyfe-specific workflow. Do not expose a generic help-desk interface to members.

---

## 7.8 MiShared — authentication, local vaults, kiosk safety

| Status | Project | GitHub | License | Best use in MiLyfe |
|---|---|---|---|---|
| DEFAULT | Keycloak | [keycloak/keycloak](https://github.com/keycloak/keycloak) | Apache-2.0 | OIDC, sessions, WebAuthn, identity federation |
| DEFAULT | SimpleWebAuthn | [MasterKale/SimpleWebAuthn](https://github.com/MasterKale/SimpleWebAuthn) | MIT | Passkey/WebAuthn support in React/web surfaces |
| DEFAULT | libsodium | [jedisct1/libsodium](https://github.com/jedisct1/libsodium) | ISC | Local encryption primitives |
| DEFAULT | age | [FiloSottile/age](https://github.com/FiloSottile/age) | BSD-3-Clause | Simple encrypted exports and recovery files |
| ALTERNATE | WebAuthn4J | [webauthn4j/webauthn4j](https://github.com/webauthn4j/webauthn4j) | Apache-2.0 | Java WebAuthn verification |
| ALTERNATE | SQLCipher | [sqlcipher/sqlcipher](https://github.com/sqlcipher/sqlcipher) | BSD-style | Encrypted SQLite storage; verify build/distribution terms |
| ADAPTER | KeePassXC | [keepassxreboot/keepassxc](https://github.com/keepassxreboot/keepassxc) | GPL-2.0/3.0 components | Advanced user-held secrets and paper-recovery workflows |
| ADAPTER | Vaultwarden | [dani-garcia/vaultwarden](https://github.com/dani-garcia/vaultwarden) | AGPL-3.0 | Self-hosted credential vault where operationally appropriate |
| ADAPTER | Apache Guacamole | [apache/guacamole-server](https://github.com/apache/guacamole-server) | Apache-2.0 | Controlled remote support; never silent access |

**Build rather than adopt:** Neutral notifications, session-clearing contract, child/adult separation, per-person cache boundaries, panic freeze, kiosk handoff, and readable privacy warnings.

---

## 7.9 MiPlaceShift — federation, portability, and resilient transfer

| Status | Project | GitHub | License | Best use in MiLyfe |
|---|---|---|---|---|
| DEFAULT | Matrix Synapse | [element-hq/synapse](https://github.com/element-hq/synapse) | AGPL-3.0 | Federated rooms and portable communication concepts |
| DEFAULT | ActivityPub specification | [w3c/activitypub](https://github.com/w3c/activitypub) | W3C document license/code terms; verify implementation use | Federation vocabulary |
| DEFAULT | Syncthing | [syncthing/syncthing](https://github.com/syncthing/syncthing) | MPL-2.0 | User-controlled transfer of files/packs |
| ALTERNATE | GoToSocial | [superseriousbusiness/gotosocial](https://github.com/superseriousbusiness/gotosocial) | AGPL-3.0 | Lightweight ActivityPub server patterns |
| ALTERNATE | Mastodon | [mastodon/mastodon](https://github.com/mastodon/mastodon) | AGPL-3.0 | Mature federation and instance moderation patterns |
| ADAPTER | IPFS Kubo | [ipfs/kubo](https://github.com/ipfs/kubo) | Apache-2.0 / MIT dual | Content-addressed public or encrypted user-controlled packages |
| ADAPTER | rclone | [rclone/rclone](https://github.com/rclone/rclone) | MIT | Export/transfer across user-selected storage |
| ADAPTER | restic | [restic/restic](https://github.com/restic/restic) | BSD-2-Clause | Encrypted backups |
| ADAPTER | Velero | [vmware-tanzu/velero](https://github.com/vmware-tanzu/velero) | Apache-2.0 | Place-service backup and disaster recovery |

**Build rather than adopt:** Cross-place rights preview, law-pack change, standing cooling, household split, pending-action handling, and fork-compatibility receipts.

---

## 7.10 MiModerate — reporting, blocking, safety, privacy-preserving review

| Status | Project | GitHub | License | Best use in MiLyfe |
|---|---|---|---|---|
| DEFAULT | Matrix Synapse | [element-hq/synapse](https://github.com/element-hq/synapse) | AGPL-3.0 | Room permissions, federation, moderation hooks |
| DEFAULT | Draupnir | [the-draupnir-project/Draupnir](https://github.com/the-draupnir-project/Draupnir) | AFL-3.0 | Matrix moderation tooling; review permissions carefully |
| DEFAULT | Microsoft Presidio | [microsoft/presidio](https://github.com/microsoft/presidio) | MIT | PII detection/redaction assistance; never automatic truth judgment |
| ALTERNATE | Mastodon | [mastodon/mastodon](https://github.com/mastodon/mastodon) | AGPL-3.0 | Federated report and instance-policy patterns |
| ALTERNATE | GoToSocial | [superseriousbusiness/gotosocial](https://github.com/superseriousbusiness/gotosocial) | AGPL-3.0 | Smaller federated moderation surface |
| ALTERNATE | Discourse | [discourse/discourse](https://github.com/discourse/discourse) | GPL-2.0 | Mature discussion moderation and trust patterns; do not reuse global scoring |
| ADAPTER | ClamAV | [Cisco-Talos/clamav](https://github.com/Cisco-Talos/clamav) | GPL-2.0 | Scan uploaded public/support files for malware |
| ADAPTER | YARA | [VirusTotal/yara](https://github.com/VirusTotal/yara) | BSD-3-Clause | Defensive content/file pattern matching |
| ADAPTER | PhotoStructure's BlurHash implementation family | [woltapp/blurhash](https://github.com/woltapp/blurhash) | MIT | Safer obscured previews; not moderation itself |

**Build rather than adopt:** One cross-surface block, victim-centered reporting, child routing, emergency separation, independent appeal, proportionate scope, and privacy-threshold transparency.

---

## 7.11 MiDelegate and Voice integrity

| Status | Project | GitHub | License | Best use in MiLyfe |
|---|---|---|---|---|
| DEFAULT | Decidim | [decidim/decidim](https://github.com/decidim/decidim) | AGPL-3.0 | Participatory-process and proposal patterns |
| DEFAULT | Helios Server | [benadida/helios-server](https://github.com/benadida/helios-server) | Apache-2.0 | Verifiable private election backend |
| DEFAULT | Helios Booth | [benadida/helios-booth](https://github.com/benadida/helios-booth) | GPL-3.0-or-later | Independent ballot booth |
| ALTERNATE | Loomio | [loomio/loomio](https://github.com/loomio/loomio) | AGPL-3.0 | Deliberation and collaborative decisions |
| ALTERNATE | Polis | [compdemocracy/polis](https://github.com/compdemocracy/polis) | AGPL-3.0 | Large-group opinion sensemaking |
| ALTERNATE | Snapshot | [snapshot-labs/snapshot](https://github.com/snapshot-labs/snapshot) | MIT | Off-chain voting components; audit wallet/chain assumptions |
| EVALUATE | MACI protocol | [privacy-scaling-explorations/maci](https://github.com/privacy-scaling-explorations/maci) | MIT | Coercion-resistant voting research/implementation; platform wrapper found in search is retired, so use only the maintained protocol after audit |
| ADAPTER | Apache Superset | [apache/superset](https://github.com/apache/superset) | Apache-2.0 | Public aggregate outcomes, not secret-ballot processing |

**Build rather than adopt:** Topic-scoped delegation, expiry, instant revocation, no silent re-delegation, privacy-preserving concentration warnings, local eligibility, and plain-language stage/history UI.

---

## 7.12 MiStage — Practice/Live isolation and controlled release

| Status | Project | GitHub | License | Best use in MiLyfe |
|---|---|---|---|---|
| DEFAULT | OpenFeature | [open-feature/spec](https://github.com/open-feature/spec) | Apache-2.0 | Vendor-neutral capability/feature evaluation interface |
| DEFAULT | Flipt | [flipt-io/flipt](https://github.com/flipt-io/flipt) | GPL-3.0 | Self-hosted feature flags; verify current license/version |
| DEFAULT | TUF | [theupdateframework/python-tuf](https://github.com/theupdateframework/python-tuf) | Apache-2.0 / BSD components | Signed capability and update metadata |
| ALTERNATE | Unleash | [Unleash/unleash](https://github.com/Unleash/unleash) | AGPL-3.0-or-later in current repository | Mature feature management; current GitHub result reports AGPL, not the older Apache assumption |
| ALTERNATE | GrowthBook | [growthbook/growthbook](https://github.com/growthbook/growthbook) | MIT core; verify package boundaries | Feature flags and controlled experiments without manipulative engagement tests |
| ADAPTER | Conftest | [open-policy-agent/conftest](https://github.com/open-policy-agent/conftest) | Apache-2.0 | Test stage/configuration policies in CI |
| ADAPTER | Cosign | [sigstore/cosign](https://github.com/sigstore/cosign) | Apache-2.0 | Sign manifests and releases |

**Build rather than adopt:** The MiStage manifest, fail-closed cross-service checks, persistent member presentation, export/notification markings, and absolute prohibition on Practice-to-Live contamination.

---

## 7.13 MiNotify — private, local-first notifications

| Status | Project | GitHub | License | Best use in MiLyfe |
|---|---|---|---|---|
| DEFAULT | ntfy | [binwiederhier/ntfy](https://github.com/binwiederhier/ntfy) | Apache-2.0 in current 2026 project reporting; verify tag | Self-hosted HTTP/WebSocket push |
| DEFAULT | Apprise | [caronc/apprise](https://github.com/caronc/apprise) | BSD-2-Clause | Route to many notification transports |
| DEFAULT | Gotify | [gotify/server](https://github.com/gotify/server) | MIT | Lightweight self-hosted push server |
| ALTERNATE | Novu | [novuhq/novu](https://github.com/novuhq/novu) | MIT-reported core; audit repository boundaries | Workflow, digest, preferences, and channel orchestration |
| ALTERNATE | Ntfy Android | [binwiederhier/ntfy-android](https://github.com/binwiederhier/ntfy-android) | GPL-2.0 | Android client patterns |
| ADAPTER | Matrix | [element-hq/synapse](https://github.com/element-hq/synapse) | AGPL-3.0 | Encrypted in-app alerts and acknowledgements |

**Build rather than adopt:** Sensitivity classification, neutral lock-screen previews, shared-device policy, acknowledgement/escalation, expiry, child rules, and MiScope enforcement.

---

## 7.14 MiRender — app, print, translation, speech, and low-bandwidth formats

| Status | Project | GitHub | License | Best use in MiLyfe |
|---|---|---|---|---|
| DEFAULT | Pandoc | [jgm/pandoc](https://github.com/jgm/pandoc) | GPL-2.0-or-later | Convert structured content to many document formats |
| DEFAULT | WeasyPrint | [Kozea/WeasyPrint](https://github.com/Kozea/WeasyPrint) | BSD-3-Clause | Accessible print/PDF rendering; official project confirms BSD |
| DEFAULT | Piper | [rhasspy/piper](https://github.com/rhasspy/piper) | MIT | Local text-to-speech; verify maintained fork/model licenses |
| DEFAULT | LibreTranslate | [LibreTranslate/LibreTranslate](https://github.com/LibreTranslate/LibreTranslate) | AGPL-3.0 | Self-hosted machine translation, visibly labeled |
| DEFAULT | Argos Translate | [argosopentech/argos-translate](https://github.com/argosopentech/argos-translate) | MIT | Offline translation engine and packages; verify each model license |
| ALTERNATE | Whisper | [openai/whisper](https://github.com/openai/whisper) | MIT | Local speech-to-text; audit model/data limitations |
| ALTERNATE | Coqui TTS | [coqui-ai/TTS](https://github.com/coqui-ai/TTS) | MPL-2.0 | Speech synthesis; verify activity and model licenses |
| ADAPTER | Docassemble | [jhpyle/docassemble](https://github.com/jhpyle/docassemble) | MIT | Guided legal/information packet generation |
| ADAPTER | BrailleBlaster | [aphtech/brailleblaster](https://github.com/aphtech/brailleblaster) | LGPL-2.1 | Braille-ready educational and rights materials |
| ADAPTER | liblouis | [liblouis/liblouis](https://github.com/liblouis/liblouis) | GPL-3.0/LGPL components; verify | Braille translation |

**Build rather than adopt:** One structured Mi content package preserving audience, source, freshness, stage, safety wording, receipt meaning, and correction route across every rendering.

---

## 7.15 MiUXKit — accessible React and React Native design foundation

| Status | Project | GitHub | License | Best use in MiLyfe |
|---|---|---|---|---|
| DEFAULT | React Aria / Spectrum | [adobe/react-spectrum](https://github.com/adobe/react-spectrum) | Apache-2.0 | Accessible web behavior and hooks |
| DEFAULT | Expo | [expo/expo](https://github.com/expo/expo) | MIT core; dependencies vary | Universal React Native runtime; official repo confirms MIT source |
| DEFAULT | Storybook | [storybookjs/storybook](https://github.com/storybookjs/storybook) | MIT | Component states, review, docs, and visual testing |
| DEFAULT | Style Dictionary | [amzn/style-dictionary](https://github.com/amzn/style-dictionary) | Apache-2.0 | Shared design tokens across platforms |
| DEFAULT | axe-core | [dequelabs/axe-core](https://github.com/dequelabs/axe-core) | MPL-2.0 | Automated accessibility checks |
| DEFAULT | Playwright | [microsoft/playwright](https://github.com/microsoft/playwright) | Apache-2.0 | Browser, keyboard, viewport, and offline testing |
| ALTERNATE | Radix Primitives | [radix-ui/primitives](https://github.com/radix-ui/primitives) | MIT | Headless web components if React Aria is not selected |
| ALTERNATE | React Native Paper | [callstack/react-native-paper](https://github.com/callstack/react-native-paper) | MIT | Accessible native component base; fully restyle for MiLyfe |
| ALTERNATE | Tamagui core | [tamagui/tamagui](https://github.com/tamagui/tamagui) | MIT core; verify cloud/pro packages | Cross-platform styling/component primitives |
| ADAPTER | i18next | [i18next/i18next](https://github.com/i18next/i18next) | MIT | Localization and pluralization |
| ADAPTER | FormatJS | [formatjs/formatjs](https://github.com/formatjs/formatjs) | MIT | Locale-aware date, number, and message formatting |
| ADAPTER | Lucide | [lucide-icons/lucide](https://github.com/lucide-icons/lucide) | ISC | Open icon foundation |
| ADAPTER | Pa11y | [pa11y/pa11y](https://github.com/pa11y/pa11y) | LGPL-3.0 | Accessibility test automation |
| ADAPTER | React Hook Form | [react-hook-form/react-hook-form](https://github.com/react-hook-form/react-hook-form) | MIT | Accessible long-form state when paired with Mi patterns |
| ADAPTER | TanStack Query | [TanStack/query](https://github.com/TanStack/query) | MIT | Cached server state and connection transitions |

**Selection:** React Aria for web behavior, native platform semantics through Expo/React Native, and a custom MiUXKit visual/content layer. Do not mix multiple full UI kits.

---

## 7.16 MiScenario — integrated rights, policy, resilience, and UX tests

| Status | Project | GitHub | License | Best use in MiLyfe |
|---|---|---|---|---|
| DEFAULT | Playwright | [microsoft/playwright](https://github.com/microsoft/playwright) | Apache-2.0 | End-to-end, device, network, accessibility, and screenshot scenarios |
| DEFAULT | Cucumber JS | [cucumber/cucumber-js](https://github.com/cucumber/cucumber-js) | MIT | Human-readable acceptance scenarios |
| DEFAULT | Conftest | [open-policy-agent/conftest](https://github.com/open-policy-agent/conftest) | Apache-2.0 | Policy tests in CI |
| DEFAULT | LitmusChaos | [litmuschaos/litmus](https://github.com/litmuschaos/litmus) | Apache-2.0 | Infrastructure and network failure experiments |
| ALTERNATE | k6 | [grafana/k6](https://github.com/grafana/k6) | AGPL-3.0 | Load and reliability tests |
| ALTERNATE | Schemathesis | [schemathesis/schemathesis](https://github.com/schemathesis/schemathesis) | MIT | Property-based API testing |
| ALTERNATE | Hypothesis | [HypothesisWorks/hypothesis](https://github.com/HypothesisWorks/hypothesis) | MPL-2.0 | Generate edge cases for state and policy functions |
| ADAPTER | Toxiproxy | [Shopify/toxiproxy](https://github.com/Shopify/toxiproxy) | MIT | Simulate slow, failed, and unstable connections |
| ADAPTER | Pumba | [alexei-led/pumba](https://github.com/alexei-led/pumba) | Apache-2.0 | Container network/process failure testing |
| ADAPTER | OWASP ZAP | [zaproxy/zaproxy](https://github.com/zaproxy/zaproxy) | Apache-2.0 | Defensive web security testing |

MiScenario must combine UI, policy, role graph, event state, offline reconciliation, notifications, receipts, and appeals—not run these tools in isolation.

---

## 7.17 MiLifecycle — classification, retention, export, deletion, and recovery

| Status | Project | GitHub | License | Best use in MiLyfe |
|---|---|---|---|---|
| DEFAULT | OpenMetadata | [open-metadata/OpenMetadata](https://github.com/open-metadata/OpenMetadata) | Apache-2.0 | Data ownership, classification, lineage, policies |
| DEFAULT | Apache NiFi | [apache/nifi](https://github.com/apache/nifi) | Apache-2.0 | Controlled data movement and lifecycle workflows |
| DEFAULT | Velero | [vmware-tanzu/velero](https://github.com/vmware-tanzu/velero) | Apache-2.0 | Cluster backup/restore |
| DEFAULT | restic | [restic/restic](https://github.com/restic/restic) | BSD-2-Clause | Encrypted repository backups |
| ALTERNATE | DataHub | [datahub-project/datahub](https://github.com/datahub-project/datahub) | Apache-2.0 | Enterprise-scale catalog/classification |
| ALTERNATE | Apache Atlas | [apache/atlas](https://github.com/apache/atlas) | Apache-2.0 | Data governance and classifications |
| ALTERNATE | BorgBackup | [borgbackup/borg](https://github.com/borgbackup/borg) | BSD-3-Clause | Deduplicated encrypted backups |
| ADAPTER | rclone | [rclone/rclone](https://github.com/rclone/rclone) | MIT | User-selected export destination |
| ADAPTER | age | [FiloSottile/age](https://github.com/FiloSottile/age) | BSD-3-Clause | Encrypt portable export packages |
| ADAPTER | Microsoft Presidio | [microsoft/presidio](https://github.com/microsoft/presidio) | MIT | Assist data discovery/redaction; human review required |
| ADAPTER | MinIO | [minio/minio](https://github.com/minio/minio) | AGPL-3.0 | Object storage; recheck current community distribution and compatibility |

**Build rather than adopt:** Purpose registry, consent withdrawal, peer/public-copy limits, death/stewardship, place/fork migration, retention conflict, deletion verification, and member-readable lifecycle receipts.

---

## 7.18 Expanded MiCompat — license, SBOM, vulnerability, provenance, and policy

| Status | Project | GitHub | License | Best use in MiLyfe |
|---|---|---|---|---|
| DEFAULT | ScanCode Toolkit | [aboutcode-org/scancode-toolkit](https://github.com/aboutcode-org/scancode-toolkit) | Apache-2.0 | Deep license/copyright/package detection |
| DEFAULT | OSS Review Toolkit | [oss-review-toolkit/ort](https://github.com/oss-review-toolkit/ort) | Apache-2.0 | End-to-end dependency and license compliance |
| DEFAULT | Syft | [anchore/syft](https://github.com/anchore/syft) | Apache-2.0 | Generate CycloneDX/SPDX SBOMs |
| DEFAULT | Grype | [anchore/grype](https://github.com/anchore/grype) | Apache-2.0 | Scan SBOMs/images for vulnerabilities |
| DEFAULT | Trivy | [aquasecurity/trivy](https://github.com/aquasecurity/trivy) | Apache-2.0 in current official/project reporting; verify tag | Vulnerability, secret, IaC, license, container scanning |
| DEFAULT | OSV-Scanner | [google/osv-scanner](https://github.com/google/osv-scanner) | Apache-2.0 | Ecosystem-aware vulnerability scanning and remediation |
| DEFAULT | Dependency-Track | [DependencyTrack/dependency-track](https://github.com/DependencyTrack/dependency-track) | Apache-2.0 | Continuous portfolio SBOM monitoring |
| DEFAULT | GUAC | [guacsec/guac](https://github.com/guacsec/guac) | Apache-2.0 | Graph software supply-chain metadata |
| DEFAULT | Cosign | [sigstore/cosign](https://github.com/sigstore/cosign) | Apache-2.0 | Sign images, binaries, and attestations |
| DEFAULT | in-toto | [in-toto/in-toto](https://github.com/in-toto/in-toto) | Apache-2.0 | Supply-chain layout and attestations |
| ALTERNATE | OWASP Dependency-Check | [dependency-check/DependencyCheck](https://github.com/dependency-check/DependencyCheck) | Apache-2.0 | NVD/CPE-focused dependency scanning |
| ALTERNATE | FOSSology | [fossology/fossology](https://github.com/fossology/fossology) | GPL-2.0 | Formal license clearing and audit workflow |
| ALTERNATE | ORT + ClearlyDefined | [clearlydefined/curated-data](https://github.com/clearlydefined/curated-data) | CC-BY-4.0 data | Curated package licensing metadata |
| ADAPTER | CycloneDX CLI | [CycloneDX/cyclonedx-cli](https://github.com/CycloneDX/cyclonedx-cli) | Apache-2.0 | SBOM validation, merging, conversion |
| ADAPTER | SPDX tools | [spdx/tools-python](https://github.com/spdx/tools-python) | Apache-2.0 | SPDX document processing |
| ADAPTER | OpenSSF Scorecard | [ossf/scorecard](https://github.com/ossf/scorecard) | Apache-2.0 | Repository security-practice signals—not a safety verdict |
| ADAPTER | Scorecard Monitor | [ossf/scorecard-monitor](https://github.com/ossf/scorecard-monitor) | Apache-2.0 | Monitor dependency score changes |
| ADAPTER | Renovate | [renovatebot/renovate](https://github.com/renovatebot/renovate) | AGPL-3.0 | Automated dependency-update proposals; human merge required |
| ADAPTER | Dependabot Core | [dependabot/dependabot-core](https://github.com/dependabot/dependabot-core) | MIT | Dependency update logic |
| ADAPTER | Gitleaks | [gitleaks/gitleaks](https://github.com/gitleaks/gitleaks) | MIT | Secret scanning |
| ADAPTER | Semgrep Community | [semgrep/semgrep](https://github.com/semgrep/semgrep) | LGPL-2.1 for engine; rules vary | Static analysis; verify rule licenses and product boundaries |
| ADAPTER | CodeQL CLI/bundles | [github/codeql](https://github.com/github/codeql) | Mixed open-source licenses by component; inspect | Security analysis only after exact component review |

Current 2026 comparisons identify Trivy, Grype, OSV-Scanner, Dependency-Check, Syft, and Dependency-Track as leading free open-source SCA tools, with Apache-2.0 reported for the principal projects. Use multiple tools because none covers licenses, SBOM, vulnerabilities, secrets, provenance, maintenance, accessibility, and privacy alone.

### Required MiCompat pipeline

1. Scan source and packages with ScanCode/ORT.
2. Generate signed CycloneDX and SPDX SBOMs with Syft/CycloneDX tooling.
3. Scan vulnerabilities with OSV-Scanner plus Grype or Trivy.
4. Monitor deployed SBOMs in Dependency-Track.
5. Sign releases and attestations with Cosign/in-toto.
6. Store supply-chain relationships in GUAC where scale justifies it.
7. Apply the OSI allowlist and MiLyfe child/privacy/accessibility profiles.
8. Require human approval for exceptions and time-limit every waiver.

---

## 7.19 Projects explicitly excluded from the default body

| Project/category | Reason |
|---|---|
| HashiCorp Terraform, Vault, Consul current BSL editions | BSL is not OSI; use OpenTofu, OpenBao, and etcd/CoreDNS/Traefik |
| Sentry current BSL distribution | Not OSI for MiLyfe’s default; use GlitchTip plus Grafana/OpenTelemetry |
| n8n Sustainable Use License | Not OSI; use Activepieces, Node-RED, or Temporal after exact-version review |
| PowerSync | Current licensing includes competitive-use restrictions; not OSI-pure for the default |
| Camunda 8 core distribution | Current licensing is not a clean all-OSI default; use Temporal or Flowable |
| Chatwoot enterprise directory | Proprietary/source-available boundary in the same repository; do not ingest blindly |
| Authentik enterprise directory | MIT core exists, but repository/product includes enterprise boundaries; Keycloak is the cleaner default |
| Retired MACI Platform wrapper | Official search result states the platform is no longer maintained; only evaluate the actively maintained MACI protocol |
| Retired Walt.id VC-Lib | Official repository states it is sunset; use maintained Walt.id components or TrustBloc/Veramo |
| Any “awesome list” entry without exact license and security review | Listed does not mean maintained, secure, accessible, or OSI-clean |
| Proprietary cloud analytics/session replay | Conflicts with self-hosting and sensitive-page privacy |
| Generic crypto-wallet templates | Encourage investment UX and do not satisfy MiAction/MiReceipt/child/offline rules |

---

## 7.20 Recommended minimal stack—avoid unnecessary complexity

MiLyfe should not install every candidate. The smallest credible foundation to prototype the new coordination layer is:

| Need | Initial selection |
|---|---|
| Workflow/actions | Temporal + CloudEvents |
| Relationship permissions | OpenFGA |
| Policy/legal/stage checks | OPA + Conftest |
| Identity/session | Keycloak + WebAuthn |
| Receipts/attestations | TrustBloc VCS + in-toto/Cosign concepts |
| Device/local state | SQLite + Automerge; PouchDB/CouchDB only where replication fits |
| Provenance/freshness | OpenLineage vocabulary + a small MiSource service; OpenMetadata when scale requires |
| Human cases | Zammad behind a custom MiHandoff/MiAppeal UI |
| Communication | Matrix Synapse + MiDTN adapters |
| Notifications | ntfy + Apprise |
| Documents/access | Pandoc + WeasyPrint + Piper/Argos where needed |
| UI foundation | React Aria + Expo/React Native + Storybook + Style Dictionary |
| Tests | Playwright + Cucumber + Conftest + LitmusChaos |
| Supply chain | ScanCode + ORT + Syft + OSV-Scanner + Grype/Trivy + Dependency-Track + Cosign |

Everything else remains an alternate until a proven requirement appears.

---

# 8. Final assessment

MiLyfe does **not** need to create another wallet, map, chat server, LMS, voting platform, AI runtime, cloud, or general workflow engine.

It needs to create the layer existing tools do not provide:

> **A rights-aware, local-first, offline-capable human-action system that carries audience, consent, source, role, stage, approval, expiry, receipt, conflict, and appeal consistently across a person’s whole life.**

If only three new systems are designed first, they should be:

1. **MiAction** — what a consequential action means
2. **MiScope** — who may see or do what, why, and until when
3. **MiReceipt** — what happened, what did not, and how the person can challenge it

MiWalk, MiSource, MiHandoff, and MiAppeal follow immediately because they make the promises work offline, keep information trustworthy, connect people to real humans, and prevent power from becoming permanent.

That coordination layer is the genuinely new technical contribution in the current MiLyfe work.