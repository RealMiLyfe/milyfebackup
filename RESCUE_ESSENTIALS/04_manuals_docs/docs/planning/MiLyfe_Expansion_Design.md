# MiLyfe Platform — Major Expansion Design Document

**Date:** August 21, 2026  
**Status:** Design Phase — No Code Yet  
**Current Platform:** 64 routes, 16 apps, live at milyfe-platform.vercel.app  

---

## CRITICAL GAPS IDENTIFIED (Missing From Design)

Before the expansion features — these are holes between what EXISTS today and what the design assumes is there:

### Database Tables That Don't Exist Yet (Routes exist, no tables backing them):
| Feature | Routes Exist | DB Tables | Status |
|---------|-------------|-----------|--------|
| Housing board | `/housing` | ❌ None | Page works client-only or is a stub |
| Rideshare | `/rideshare` | ❌ None | Same |
| Jobs/Career | `/career`, `/jobs` | ❌ No jobs, resumes, applications tables | Same |
| MiLearn courses | `/learn`, `/learn/create` | ❌ No courses, modules, progress tables | Same |
| MiFamily | `/family` | ❌ No families, events, budgets tables | Same |
| Business Hub | `/business` | ❌ No businesses table | Same |
| MiGuild | `/guild` | ❌ No guild_members, guild_tasks, conflicts tables | Same |
| Safety/Walk | `/safety`, `/safety/walk` | ❌ None | Same |
| Notifications | `/notifications` | ❌ No notifications table | Same |
| Support | `/support` | ❌ None | Same |
| Feed/Social | `/feed` | ❌ No posts, comments, reactions tables | Same |
| Media content | `/media` | ❌ No media_content, radio_stations, media_likes tables | Same |
| Proposals/Governance | `/govern` | ❌ No proposals, proposal_votes tables | Same |

**Impact:** These pages likely store everything client-side or use hard-coded data. Before expanding, we need a FULL database migration to back all existing routes.

### Missing Shared Infrastructure:
| System | Status | Needed For |
|--------|--------|------------|
| Notification delivery (push/email/SMS) | ❌ Not built | Everything |
| File upload pipeline (beyond basic Supabase) | Minimal | Media, recordings, shop images |
| Background job system | ❌ Not built | Decay, UBI, notifications, AI |
| Content moderation pipeline | ❌ Not built | Social, forum, recordings |
| Real-time event bus | Partial (Supabase Realtime) | Cross-app notifications |
| Testing infrastructure | ❌ Zero tests | Platform reliability |
| CI/CD beyond Vercel auto-deploy | ❌ Not built | Multi-repo coordination |
| API versioning | ❌ Not built | Developer platform |

### Missing Connections Between Today's Features and Expansion:
| Today's Feature | Expansion Gap |
|----------------|--------------|
| Offline queue (Dexie) | No sync conflict resolution — what if user submits offline AND online changes? |
| Voice navigation | Doesn't connect to Mi AI — should be unified voice interface |
| Standing system | Not enforced anywhere yet — gated features exist in code but no UI shows locks |
| Global search | Only searches static index — needs to search DB content (posts, listings, courses) |
| TTS | Only in Rights — should be platform-wide accessibility feature |
| Channels | No connection to MiSocial — channels should BE social creator pages |
| Rate limiting | In-memory only — resets on every deploy (Vercel cold starts) |
| Analytics (PostHog) | No actual events being tracked yet — just pageviews |

---

## ADDITIONAL SYSTEMS MISSING FROM DESIGN (Gaps Found)

### 22. Full Database Migration (Priority: CRITICAL)
All existing page routes need proper Supabase tables. This is the foundation before ANY expansion.

### 23. Notification System (Push + Email + In-App)
| Channel | Tech | Use Case |
|---------|------|----------|
| In-app | Supabase Realtime | All notifications |
| Push | Web Push API + service worker | Urgent alerts |
| Email | Resend API | Digests, account alerts |
| SMS | Twilio (later) | Emergency broadcast, 2FA |

### 24. Content Moderation Pipeline
- AI pre-screening (text: toxicity, images: NSFW)
- Community flagging → queue → review (human or jury)
- Auto-action on high-confidence violations
- Appeal workflow
- Needed by: Forum, Social, Marketplace, Recordings, Media

### 25. Unified File/Media Pipeline
- Upload → process (compress, thumbnail, transcode) → CDN
- Video transcoding for different qualities
- Image optimization (WebP, resize)
- Document scanning/OCR
- Storage strategy: Supabase Storage now → Cloudflare R2 at scale

### 26. Background Job System
- Vercel Cron (current: UBI + decay)
- Need: Notification digests, content moderation queue, search indexing, analytics aggregation, standing recalculation, media transcoding
- Solution: Upstash QStash or Inngest

### 27. User Onboarding Flow (Expansion)
Current onboarding exists but doesn't:
- Set up digital twin
- Choose interests (for algorithm)
- Connect to neighborhood
- Verify identity (optional, for higher trust)
- Complete first actions (checkin, report, vote)

### 28. Reputation & Trust Web
Standing is individual — missing:
- Mutual endorsements (LinkedIn-style)
- Trust graph (who trusts who — affects delegation weight)
- Business reputation (tied to owner's standing)
- Neighborhood reputation (aggregate of residents)

### 29. $MLY Tokenomics Dashboard
People need to understand the full economy:
- Total supply, circulation, burned, in treasury
- Velocity (how fast MLY moves)
- Top earning actions, top spending categories
- Inflation/deflation rate
- Projections: "At current rate, your $MLY will be worth..."

### 30. Accessibility Expansion
Built today: TTS, font/contrast. Missing:
- Screen reader optimization (ARIA roles throughout)
- Keyboard navigation for all interfaces
- High contrast mode (proper theme, not just toggle)
- Reduced motion mode (exists but not enforced)
- Cognitive accessibility: Simple language mode, step-by-step guides
- Audio descriptions for visual content

### 31. Privacy & Data Sovereignty
Users own their data — needs:
- Data export (exists at `/profile/export` but may be incomplete)
- Account deletion (full GDPR-style erasure)
- Data portability (standard format export)
- Consent management (granular opt-in/out)
- Encryption at rest for vault documents
- Zero-knowledge proofs for identity verification

### 32. Interoperability / Federation
For future growth:
- ActivityPub support (federate with Mastodon/Threads)
- RSS feeds for public content
- ICAL export for events/calendars
- OpenID Connect as identity provider
- Webhook subscriptions for external services

### 33. Gamification Framework
Exists in pieces (standing, streaks, MLY rewards). Missing unified:
- Achievement badges (first post, first sale, first vote, etc.)
- Weekly/monthly challenges
- Leaderboards (neighborhood, all-platform)
- Seasonal events/campaigns
- Team challenges (neighborhoods compete)

### 34. Communication Expansion
MiConnect has DMs. Missing:
- Voice calls (WebRTC)
- Video calls (WebRTC)
- Group video (for study groups, family, guild meetings)
- Screen sharing
- Voice messages
- Walkie-talkie mode (push-to-talk for guild patrols)

### 35. Payment & Financial Rails
$MLY is internal and stays internal. MiLyfe uses **no third-party payment
processor — ever** (no Stripe, PayPal, Braintree, or any gateway). The community
IS the financial system: value is earned through participation and exchanged
peer-to-peer through the $MLY wallet and community treasury.
- Any real-world bridge (if the community ever chooses one) is a peer-to-peer /
  community exchange desk, not a corporate processor.
- Business invoicing: Generate invoices in MLY
- Splits: Split bills among group members
- Recurring payments: Subscriptions, rent, allowances (all in $MLY)
- Tax reporting: Annual MLY earnings statement

---

## Table of Contents

1. [Emergency Broadcast System](#1-emergency-broadcast-system)
2. [MiNews — World News Feed](#2-minews--world-news-feed)
3. [MiAcademia — R&D + Community Education](#3-miacademia--rd--community-education)
4. [Community Knowledge Base (Wiki)](#4-community-knowledge-base-wiki)
5. [MiForum — Reddit-Style Community Pages](#5-miforum--reddit-style-community-pages)
6. [MiSocial — Full Social Media App](#6-misocial--full-social-media-app)
7. [MiTwin — Digital Twin + Avatar](#7-mitwin--digital-twin--avatar)
8. [MiNav — Interactive Maps & Navigation](#8-minav--interactive-maps--navigation)
9. [MiAuto — Automobile Integration](#9-miauto--automobile-integration)
10. [MiDev — Developer Platform Expansion](#10-midev--developer-platform-expansion)
11. [Mi AI — Expanded Intelligence](#11-mi-ai--expanded-intelligence)
12. [Auto-Scaling Infrastructure](#12-auto-scaling-infrastructure)
13. [MiLearn — Real Courses & Libraries](#13-milearn--real-courses--libraries)
14. [Community Recording & Reward System](#14-community-recording--reward-system)
15. [Consequence & Accountability System](#15-consequence--accountability-system)
16. [MiConstitution — Interactive App](#16-miconstitution--interactive-app)
17. [Transparency Dashboards](#17-transparency-dashboards)
18. [MiMarket — Expanded Marketplace](#18-mimarket--expanded-marketplace)
19. [MiCity Expansion — GitHub-Style Civic Ops](#19-micity-expansion--github-style-civic-ops)
20. [Admin AI + People Dashboards](#20-admin-ai--people-dashboards)
21. [Repo Strategy & GitHub Organization](#21-repo-strategy--github-organization)

---

## 1. Emergency Broadcast System

**Purpose:** Allow verified community leaders (Level 5 standing) to send priority notifications to geographic zones during emergencies.

**Architecture:**
- Broadcast types: Weather, Safety, Infrastructure, Health, Community
- Geo-fencing: Target by zip code, neighborhood, or radius
- Channels: Push notification, in-app banner, SMS (for opted-in users)
- Verification: Only Level 5 standing OR admin-approved can broadcast
- Rate limit: 1 broadcast per user per 6 hours (prevents abuse)
- Acknowledge system: Users confirm they saw the alert

**Data Model:**
```
broadcasts: id, sender_id, type, severity (info/warning/critical), 
            title, body, geo_zone, radius_miles, acknowledged_count,
            expires_at, created_at
broadcast_acks: broadcast_id, user_id, acked_at
```

**Repo:** Part of main `MiLyfe-Platform` (it's a feature, not a standalone app)

---

## 2. MiNews — World News Feed

**Purpose:** Curated world news relevant to MiLyfe's mission — civic engagement, community economics, social justice, tech for good, local Jacksonville news.

**Architecture:**
- Aggregation: RSS feeds from verified sources + community-submitted links
- Categories: Local (Jax), National, World, Tech, Economy, Justice, Community Wins
- AI curation: Mi AI summarizes articles, flags relevance
- Community interaction: Upvote, discuss, share to MiForum
- NO original journalism — aggregation + commentary only
- Source transparency: Always link to original, show publication bias score

**Data Model:**
```
news_articles: id, source_url, source_name, title, summary, 
              ai_summary, category, relevance_score, image_url,
              published_at, submitted_by, upvotes, comments_count
news_sources: id, name, url, rss_feed, bias_rating, category, active
news_comments: id, article_id, user_id, content, likes, created_at
```

**Repo:** `MiLyfe-Platform` (integrated as `/news` route group)

---

## 3. MiAcademia — R&D + Community Education

**Purpose:** Bridge between MiLearn (courses) and actual research. Community-driven R&D labs, study groups, academic papers, research proposals funded by $MLY.

**Architecture:**
- Research Labs: Community members propose and join research projects
- Study Groups: Real-time collaborative learning (video + shared docs)
- Paper Library: Open-access papers relevant to community development
- Grants: Propose research, community votes to fund with $MLY pool
- Mentorship: Pair researchers with community experts
- Certifications: Verifiable credentials issued on completion

**Data Model:**
```
research_projects: id, title, description, lead_id, status, 
                   funding_goal, funding_raised, category, members[]
study_groups: id, name, topic, schedule, max_members, meeting_url
academic_papers: id, title, authors, abstract, pdf_url, doi, 
                 category, submitted_by, citations
research_grants: id, project_id, amount, status, voter_count
```

**Repo:** `MiLyfe-Academia` (separate repo — complex enough to warrant isolation)

---

## 4. Community Knowledge Base (Wiki)

**Purpose:** Community-edited wiki for local knowledge — how things work, resource directories, FAQs, procedures, history.

**Architecture:**
- MediaWiki-style but simpler: Markdown-based pages
- Version history: Full edit trail, rollback capability
- Categories: How-To, Resources, History, Policies, FAQ, Neighborhoods
- Moderation: Community flagging + standing-gated editing (Level 2+ to edit)
- Search: Full-text search with vector embeddings for semantic lookup
- Templates: Standardized page formats (Business profile, Neighborhood guide, etc.)

**Data Model:**
```
wiki_pages: id, slug, title, content_md, category, created_by, 
            last_edited_by, version, locked, views
wiki_revisions: id, page_id, editor_id, content_md, diff, 
                edit_summary, created_at
wiki_categories: id, name, description, parent_id, icon
```

**Repo:** `MiLyfe-Platform` (integrated as `/wiki` route group)

---

## 5. MiForum — Reddit-Style Community Pages

**Purpose:** Subreddit-style spaces where communities, neighborhoods, and interest groups can self-organize discussions.

**Architecture:**
- Spaces: Anyone Level 2+ can create (like subreddits)
- Posts: Text, link, image, poll
- Voting: Upvote/downvote with $MLY-weighted standing
- Moderation: Space creators + elected mods, community-flagging
- Flair/Tags: Custom per-space
- Sort: Hot, New, Top (day/week/month/all)
- Cross-posting between spaces
- Karma system tied to community standing

**Data Model:**
```
forum_spaces: id, name, slug, description, banner_url, rules,
              creator_id, member_count, created_at
forum_posts: id, space_id, author_id, type (text/link/image/poll),
             title, body, url, image_url, upvotes, downvotes,
             comment_count, pinned, created_at
forum_comments: id, post_id, parent_id, author_id, body, 
               upvotes, downvotes, depth, created_at
forum_memberships: space_id, user_id, role (member/mod/creator)
forum_votes: id, post_id/comment_id, user_id, direction (up/down)
```

**Repo:** `MiLyfe-Forum` (standalone — this will get big fast)

---

## 6. MiSocial — Full Social Media App

**Purpose:** Build out the existing feed into a proper social platform — profiles, stories, reels, DMs, follows, algorithmic + chronological feeds.

**Architecture:**
- Profile pages: Bio, posts, media, activity, followers/following
- Stories: 24hr disappearing content (photo/video + text)
- Reels/Shorts: Short-form video (15-60 sec)
- Feed algorithms: Chronological (default) + "For You" (engagement-based)
- Follows: Follow users, spaces, hashtags
- Hashtags: Trending, community-specific
- Reactions: Beyond likes — ❤️ 🔥 💪 🤝 👑 (community-themed)
- Content moderation: AI + community flagging + consequences

**Integration with existing:**
- Merges current `/feed` into full social experience
- MiMedia becomes the "upload studio" for MiSocial content
- MiConnect DMs stay as the messaging layer

**Data Model:**
```
social_profiles: user_id, bio, website, banner_url, 
                 followers_count, following_count, post_count
follows: id, follower_id, following_id, created_at
stories: id, user_id, media_url, type, text_overlay, 
         views, expires_at, created_at
reels: id, user_id, video_url, thumbnail_url, caption, 
       hashtags[], likes, views, shares, duration
hashtags: id, tag, post_count, trending_score
```

**Repo:** `MiLyfe-Social` (standalone app — potentially the largest sub-system)

---

## 7. MiTwin — Digital Twin + Avatar

**Purpose:** Each user gets a digital twin — an AI-powered avatar that represents them, can act on their behalf (with permissions), and provides personalized insights.

**Architecture:**
- Avatar creation: Customizable 3D/2D avatar (face, body, style)
- Digital twin AI: Learns user preferences, can draft messages, suggest actions
- Representation: Avatar appears in forums, social, profiles
- Automation: "Twin mode" — twin can auto-accept guild tasks, auto-vote on delegated proposals
- Dashboard: Twin shows you patterns about yourself (spending, health, social activity)
- NFT-ready: Avatar exportable as profile asset

**Tech Stack:**
- Avatar: Ready Player Me SDK or custom Three.js/React Three Fiber
- AI: Personal fine-tuned model based on user interaction history
- Storage: Avatar assets in Supabase Storage, preferences in user profile

**Data Model:**
```
digital_twins: user_id, avatar_config (JSON), ai_personality,
               automation_settings, active, created_at
twin_actions: id, twin_id, action_type, payload, executed_at, 
              approved_by_user
twin_insights: id, twin_id, insight_type, data (JSON), 
               generated_at
avatar_assets: id, user_id, asset_type, file_url, metadata
```

**Repo:** `MiLyfe-Twin` (separate — heavy 3D/AI workload)

---

## 8. MiNav — Interactive Maps & Navigation

**Purpose:** Waze-style community navigation — real-time traffic, hazards, community points of interest, walking routes, transit.

**Architecture:**
- Map engine: MapLibre GL (open-source) or Mapbox
- Layers: Traffic, transit, hazards, businesses, events, issues, guild patrol zones
- Community reports: Road hazards, police checkpoints, construction, flooding
- Turn-by-turn: Walking, driving, transit directions
- Transit: JTA GTFS real-time feed integration
- Points of Interest: MiLyfe businesses, events, resources
- Safety overlay: Well-lit paths, "walk with me" routes, crime heat map
- ETA sharing: Share arrival time with family/friends

**Data Model:**
```
map_reports: id, user_id, type (hazard/police/construction/flood),
             lat, lng, description, upvotes, expires_at, created_at
map_routes: id, user_id, origin, destination, mode, waypoints,
            distance, duration, saved
transit_stops: id, name, lat, lng, routes[], next_arrivals[]
poi_pins: id, type, name, lat, lng, data (JSON), source
```

**Tech Stack:**
- MapLibre GL JS for rendering
- Turf.js for geo calculations
- JTA GTFS-RT for real-time transit
- Supabase Realtime for live hazard updates

**Repo:** `MiLyfe-Nav` (separate — mapping is a complex domain)

---

## 9. MiAuto — Automobile Integration

**Purpose:** Everything car-related for the community — ride management, maintenance tracking, car-sharing, insurance co-op, EV charging, parking.

**Architecture:**
- Vehicle Registry: Users register vehicles, track maintenance
- Maintenance Tracker: Oil changes, inspections, reminders
- Community Garage: Find trusted local mechanics (from MiBusiness directory)
- Car Share: Turo-style community car sharing (pay with $MLY)
- Gas/EV Tracker: Find cheapest gas or available chargers
- Insurance Co-op: Community collective bargaining for insurance rates
- Parking: Report/find free parking spots
- Merge with existing Rideshare: Rideshare becomes a feature within MiAuto

**Data Model:**
```
vehicles: id, owner_id, make, model, year, color, plate, 
          mileage, type (gas/ev/hybrid), status
maintenance_records: id, vehicle_id, type, mileage, cost, 
                     provider_id, notes, next_due, created_at
car_shares: id, vehicle_id, owner_id, hourly_rate, daily_rate,
            available_from, available_to, rules, status
parking_spots: id, reporter_id, lat, lng, type (free/metered/lot),
               available, reported_at, expires_at
ev_chargers: id, name, lat, lng, connector_type, status, 
             price_per_kwh, network
```

**Repo:** `MiLyfe-Auto` (separate — automotive is a vertical)

---

## 10. MiDev — Developer Platform Expansion

**Purpose:** Make MiLyfe a true developer ecosystem — APIs, SDKs, plugins, bounties, open-source contributions, developer profiles.

**Architecture:**
- Developer Portal: API docs, SDK downloads, sandbox environment
- App Store: Third-party apps/plugins for MiLyfe (vetted by community)
- Bounty Board: $MLY-funded feature requests and bug bounties
- Contribution Tracking: GitHub-integrated contribution scoring
- Developer Profiles: Portfolio, contributions, reputation, skills
- Hackathons: Community-organized coding events
- SDKs: JavaScript, Python, React Native
- Webhooks: Subscribe to platform events
- OAuth: "Sign in with MiLyfe" for third-party apps

**Data Model:**
```
developer_apps: id, developer_id, name, description, 
                api_key, oauth_config, status, downloads
app_reviews: id, app_id, user_id, rating, review, created_at
bounties: id, title, description, reward_mly, status, 
          posted_by, claimed_by, github_issue_url
contributions: id, developer_id, type, repo, pr_url, 
               merged, reward_mly, created_at
hackathons: id, title, description, start_at, end_at, 
            prize_pool, submissions_count
```

**Repo:** `MiLyfe-Dev-Portal` (separate — developer-facing infrastructure)

---

## 11. Mi AI — Expanded Intelligence

**Purpose:** Evolve Mi from a simple assistant into a platform-wide intelligence layer.

**Architecture:**
- Personal AI: Each user's Mi learns their patterns and preferences
- Community AI: Aggregated (anonymized) insights for governance decisions
- Content AI: Auto-moderation, spam detection, content categorization
- Recommendation Engine: Suggest courses, jobs, connections, events
- Natural Language Actions: "Mi, send $5 to Maria" — execute platform actions via chat
- Voice AI: Full conversational mode (not just navigation commands)
- Multi-modal: Accept images (report issues by photo), documents (scan legal papers)
- Agents: Mi spawns specialized sub-agents (Legal Mi, Health Mi, Finance Mi)

**Expanded capabilities:**
- RAG (Retrieval Augmented Generation) over community knowledge base
- Function calling for platform actions (send MLY, create post, file report)
- Memory: Persistent conversation context per user
- Proactive: Mi reaches out ("You haven't checked in for 3 days, everything okay?")

**Tech Stack:**
- Groq (fast inference, current) + local Ollama fallback
- LangChain/LangGraph for agent orchestration
- Supabase pgvector for embeddings/RAG
- Edge Functions for real-time AI features

**Repo:** `MiLyfe-AI` (separate — AI infrastructure is its own system)

---

## 12. Auto-Scaling Infrastructure

**Purpose:** Prepare the platform for 10K → 100K → 1M users without manual intervention.

**Architecture:**
- Current: Vercel (auto-scales serverless functions)
- Database: Supabase Pro tier (connection pooling, read replicas)
- CDN: Vercel Edge Network (already active)
- Media: Cloudflare R2 or Supabase Storage with CDN
- Rate limiting: Move from in-memory to Upstash Redis (distributed)
- Queue system: Upstash QStash for async jobs (email, notifications, AI)
- Monitoring: Sentry (errors) + PostHog (analytics) + Checkly (uptime)
- Load testing: k6 scripts for API endpoints

**Scaling triggers:**
- 1K users: Current infra holds fine
- 10K users: Add Redis caching, Supabase Pro, Upstash rate limiter
- 100K users: Database read replicas, CDN for all media, queue workers
- 1M users: Multi-region, dedicated Postgres, microservices split

**Repo:** `MiLyfe-Infrastructure` (IaC — Terraform/Pulumi configs)

---

## 13. MiLearn — Real Courses & Libraries

**Purpose:** Replace placeholder courses with real, substantive educational content.

**Default Course Library (20+ courses):**

**Legal & Rights:**
1. Know Your Rights: Complete Guide (10 modules)
2. Tenant Rights in Florida (8 modules)
3. Police Encounters: What to Do (6 modules)
4. Small Claims Court: Step by Step (7 modules)
5. Immigration Rights Basics (8 modules)

**Financial:**
6. $MLY Economics: How Community Currency Works (5 modules)
7. Building Credit from Zero (8 modules)
8. Starting a Business with $0 (10 modules)
9. Crypto & Digital Assets for Beginners (7 modules)
10. Tax Basics for Gig Workers (6 modules)

**Digital:**
11. Digital Literacy: Protect Yourself Online (8 modules)
12. Building Your First Website (10 modules)
13. Data Privacy: What They Know About You (6 modules)
14. AI Literacy: Understanding Machine Learning (7 modules)

**Civic:**
15. How Local Government Actually Works (8 modules)
16. Community Organizing 101 (10 modules)
17. Running for Local Office (7 modules)
18. Grant Writing for Community Projects (8 modules)

**Health:**
19. Mental Health First Aid (8 modules)
20. Nutrition on a Budget (6 modules)
21. CPR & First Aid Certification (5 modules)

**Career:**
22. Interview Skills That Actually Work (6 modules)
23. Remote Work: Getting Started (7 modules)
24. Freelancing & Self-Employment (9 modules)

**Life Skills:**
25. Conflict Resolution & De-escalation (7 modules)
26. Co-Parenting Communication (6 modules)
27. Home Repair Basics (10 modules)

**Repo:** Course content goes in `MiLyfe-Platform` as seed data; authoring tool in `MiLyfe-Academia`

---

## 14. Community Recording & Reward System

**Purpose:** Citizens who record community-relevant events (infrastructure issues, safety concerns, community wins) get rewarded AND the footage goes to appropriate personnel.

**Architecture:**
- Quick Record: One-tap recording from any screen
- Auto-categorize: AI analyzes footage and suggests category
- Routing: Based on category, routes to:
  - Infrastructure → City maintenance queue (public)
  - Safety → Community safety board (moderated)
  - Police encounter → MiRights log (private, user-controlled)
  - Community win → MiSocial feed (public)
  - Emergency → Emergency broadcast + 911 suggestion
- Rewards: $MLY based on contribution value (voted by community)
- Privacy controls: Blur faces option, restrict access, delete after X days
- Legal protection: Clear disclaimer — recordings are user's property

**Consequences for misuse:**
- False reports: Standing reduction
- Harassment via recording: Account restriction
- Doxxing/targeting: Immediate suspension + community tribunal
- Copyright violations: Content removal + warning

**Data Model:**
```
community_recordings: id, recorder_id, video_url, category,
                      ai_category_suggestion, status (pending/routed/rewarded),
                      routed_to, reward_mly, privacy_level,
                      faces_blurred, lat, lng, created_at
recording_reviews: id, recording_id, reviewer_id, 
                   action (approve/reject/flag), reason, created_at
```

**Repo:** `MiLyfe-Platform` (integrated feature)

---

## 15. Consequence & Accountability System

**Purpose:** Real consequences for platform misuse. Not authoritarian — community-driven, transparent, proportional.

**Architecture:**

**Offense Tiers:**
- Tier 1 (Warning): Spam, minor policy violation → Warning + 24hr feature restriction
- Tier 2 (Restriction): Harassment, false reports → 7-day feature lock + standing reduction
- Tier 3 (Suspension): Doxxing, hate speech, scams → 30-day suspension + community tribunal review
- Tier 4 (Ban): Repeated Tier 3, illegal activity → Permanent ban (appealable after 6 months)

**Mechanisms:**
- Community flagging: Any user can flag content
- AI pre-screening: Auto-detect obvious violations
- Community jury: Random selection of Level 3+ users for Tier 3+ cases
- Appeals: Written appeal reviewed by different jury
- Transparency: All enforcement actions logged (anonymized) in transparency dashboard
- Standing impact: Violations reduce standing (can be rebuilt over time)
- $MLY consequences: Fines deducted from balance for economic harm

**Data Model:**
```
violations: id, user_id, type, tier, description, evidence_urls[],
            reported_by, reviewed_by, status, action_taken,
            standing_penalty, mly_penalty, appeal_status, created_at
community_juries: id, violation_id, jurors[], verdict, 
                  reasoning, voted_at
appeals: id, violation_id, user_id, statement, 
         reviewed_by_jury, outcome, created_at
user_restrictions: user_id, type, reason, starts_at, ends_at
```

**Repo:** `MiLyfe-Platform` (core moderation system)

---

## 16. MiConstitution — Interactive App

**Purpose:** The constitution deserves its own dedicated app experience, not just a page within MiRights.

**Architecture:**
- Full document viewer with table of contents navigation
- Amendment proposals: Community can propose amendments
- Ratification process: Supermajority (67%) vote to amend
- History: Timeline of all amendments and their vote results
- Annotated version: Community commentary on each article
- Interactive scenarios: "What does this mean in practice?" walkthroughs
- Multilingual: Full constitution in all supported languages
- Audio: Full TTS reading of entire document (already built)
- Comparison: Side-by-side original vs. proposed amendments
- Governance simulator: "If this amendment passes, here's what changes"

**Data Model:**
```
constitution_articles: id, number, title, content_md, 
                       effective_date, status (active/amended/repealed)
constitution_amendments: id, article_id, proposed_by, 
                         proposal_text, rationale, status,
                         votes_for, votes_against, required_votes,
                         voting_ends_at, ratified_at
constitution_annotations: id, article_id, user_id, 
                          annotation, position, likes
```

**Repo:** `MiLyfe-Platform` (expanded `/constitution` route group)

---

## 17. Transparency Dashboards

**Purpose:** Full platform transparency — finances, moderation, governance, algorithms, all visible to the community.

**Dashboards:**
1. **Financial:** Total $MLY in circulation, daily UBI distributed, total burned, treasury balance
2. **Moderation:** Violations this month, actions taken (anonymized), appeal outcomes
3. **Governance:** Active proposals, participation rate, delegation stats, amendment history
4. **Platform Health:** Uptime, error rate, active users, growth
5. **Community Impact:** Issues resolved, $MLY circulated locally, courses completed, jobs filled
6. **AI Transparency:** What Mi knows, what data is collected, algorithm explanations
7. **Development:** Open PRs, bounties active, roadmap progress, contributor stats

**Architecture:**
- Real-time data from Supabase materialized views
- Charts: Recharts (already in stack)
- Public access: No login required for transparency data
- Export: CSV/JSON export for citizen auditing
- Alerts: Community can set alerts for anomalies

**Repo:** `MiLyfe-Platform` (integrated as `/transparency` route group)

---

## 18. MiMarket — Expanded Marketplace

**Purpose:** Merge current MiShop + housing + rideshare into a unified marketplace with on-demand services, classifieds, and B2B.

**Architecture:**

**Sections:**
- **Shop:** Physical goods (existing)
- **Services:** On-demand services (cleaning, repair, tutoring, etc.)
- **Classifieds:** Free/for-sale items, lost & found, giveaways
- **Housing:** Rentals, roommates, sublets (existing)
- **Auto:** Vehicles for sale, parts, services (ties into MiAuto)
- **Jobs/Gigs:** Short-term $MLY-paid work (existing)
- **B2B:** Business-to-business services and bulk orders

**On-Demand features:**
- Request a service → matched to available providers
- Real-time provider tracking (like Uber)
- Scheduled vs. immediate
- Provider ratings and portfolio
- Escrow: $MLY held until job confirmed complete
- Dispute resolution: Community mediation

**Data Model:**
```
marketplace_listings: id, seller_id, type (product/service/classified/housing/auto),
                      title, description, price, price_type (fixed/hourly/negotiable),
                      category, subcategory, images[], location, 
                      status, views, created_at
service_requests: id, requester_id, category, description, 
                  budget, urgency (asap/scheduled), scheduled_at,
                  matched_provider_id, status, created_at
escrow_holds: id, buyer_id, seller_id, listing_id, amount, 
              status (held/released/disputed), created_at
```

**Repo:** `MiLyfe-Market` (separate — marketplace is complex enough)

---

## 19. MiCity Expansion — GitHub-Style Civic Ops

**Purpose:** Transform MiCity from "report issues" to a full civic operations platform — like GitHub but for city maintenance and improvement.

**Architecture:**

**GitHub-style features:**
- **Issues:** Already exist — expand with labels, assignees, milestones
- **Projects:** Kanban boards for neighborhood improvement campaigns
- **Pull Requests (Proposals):** Propose a fix → community reviews → approved → funded → executed
- **Branches (Initiatives):** Long-running improvement efforts with multiple issues
- **Releases (Milestones):** Celebrate completed projects
- **Stars (Upvotes):** Prioritize issues by community interest
- **Forks (Templates):** Copy successful projects to other neighborhoods

**Citizen/Business Repair Program:**
- Verified citizens/businesses can claim city repair tasks
- Qualification: Pass basic training course (via MiLearn)
- Tasks: Pothole patching, trash pickup, graffiti removal, light replacement
- Verification: Before/after photos, GPS confirmation
- Payment: $MLY from city improvement fund (community-pooled)
- Legal protection: Waiver system, insurance requirement for major work
- Tiers: Level 1 (cleanup), Level 2 (minor repair), Level 3 (major repair, requires license)

**Data Model:**
```
civic_projects: id, name, description, neighborhood, 
                creator_id, status (planning/active/completed),
                budget, spent, milestone_count, issue_count
civic_milestones: id, project_id, title, description, 
                  due_date, status, issues[]
civic_repair_claims: id, issue_id, claimer_id, claimer_type (citizen/business),
                     tier, before_photo, after_photo, gps_verified,
                     reward_mly, status (claimed/in_progress/verified/paid)
repair_certifications: user_id, tier, course_completed, 
                       insurance_verified, active
```

**Repo:** `MiLyfe-Civic` (separate — civic ops platform)

---

## 20. Admin AI + People Dashboards

**Purpose:** Leave admin board for AI management. Give people proper dashboards for their lives.

**AI Admin Dashboard (admin only):**
- AI performance metrics (response time, accuracy, user satisfaction)
- Content moderation queue
- System health monitoring
- Feature flags and A/B tests
- User reports and escalations

**People Dashboards:**
- **My Dashboard:** Personal stats, $MLY flow, standing progress, upcoming events
- **Family Dashboard:** Shared calendar, budget, member status (from MiFamily)
- **Business Dashboard:** Sales, reviews, inventory, customers (from Business Hub)
- **Guild Dashboard:** Patrol stats, earnings, tasks, conflict resolution
- **Developer Dashboard:** Apps, API usage, bounties, contributions
- **Neighborhood Dashboard:** Local issues, events, businesses, safety stats

**Repo:** `MiLyfe-Platform` (dashboards are views on existing data)

---

## 21. Repo Strategy & GitHub Organization

**GitHub Organization:** `RealMiLyfe`

### Recommended Repository Structure:

| Repo | Description | Priority | Complexity |
|------|-------------|----------|------------|
| `MiLyfe-Platform` | Core platform (current) — expands with emergency broadcast, wiki, constitution, recordings, consequences, transparency, dashboards | Already exists | High |
| `MiLyfe-Social` | Full social media (profiles, stories, reels, follows, feed algorithms) | High | Very High |
| `MiLyfe-Forum` | Reddit-style community spaces | High | High |
| `MiLyfe-Market` | Unified marketplace (shop + services + classifieds + on-demand) | High | High |
| `MiLyfe-Civic` | GitHub-style civic ops, repair program | High | High |
| `MiLyfe-Nav` | Maps, navigation, transit, Waze-style reports | Medium | High |
| `MiLyfe-AI` | AI infrastructure (agents, RAG, function calling, memory) | High | Very High |
| `MiLyfe-Twin` | Digital twin system (avatars, personal AI, automation) | Medium | Very High |
| `MiLyfe-Auto` | Automobile platform (vehicles, maintenance, sharing) | Medium | Medium |
| `MiLyfe-Academia` | R&D, study groups, papers, grants | Medium | Medium |
| `MiLyfe-Dev-Portal` | Developer ecosystem (APIs, SDK, bounties, app store) | Medium | High |
| `MiLyfe-Infrastructure` | IaC, scaling configs, deployment | High | Medium |
| `MiLyfe-Mobile` | React Native wrapper for PWA + native features | Medium | Medium |
| `MiLyfe-Docs` | Public documentation, API docs, contribution guides | High | Low |

### Shared Packages (npm workspace or turborepo):

| Package | Purpose |
|---------|---------|
| `@milyfe/ui` | Shared UI components (buttons, cards, inputs) |
| `@milyfe/auth` | Authentication utilities |
| `@milyfe/mly` | $MLY transaction utilities |
| `@milyfe/i18n` | Translations |
| `@milyfe/types` | Shared TypeScript types |

### Tech Stack Per Repo:

- **Frontend:** Next.js 14 + Tailwind + Radix UI
- **Backend:** Supabase (DB + Auth + Storage + Realtime + Edge Functions)
- **AI:** Groq/OpenAI + LangChain + pgvector
- **Maps:** MapLibre GL JS
- **3D/Avatar:** React Three Fiber + Ready Player Me
- **Mobile:** React Native (Expo) wrapping web views + native modules
- **Infra:** Vercel + Supabase + Upstash Redis + Cloudflare R2

---

## Build Order (Recommended)

### Phase 0 — Foundation Fix (Week 1) ⚠️ CRITICAL
*Nothing else works without this.*
1. Full database migration (tables for ALL 53 existing routes)
2. Notification system (in-app + push + email via Resend)
3. Background job system (Upstash QStash)
4. Content moderation pipeline (AI + flagging + queue)
5. Migrate rate limiting to Redis (Upstash)
6. Wire up standing enforcement (actually lock features)
7. Wire up PostHog events across all existing pages
8. Connect voice nav to Mi AI (unified voice interface)

### Phase 1 — Foundation Expansion (Weeks 2-4)
9. Emergency Broadcast (in Platform)
10. Consequence & Accountability System (in Platform)
11. Transparency Dashboards (in Platform)
12. MiConstitution interactive app (in Platform)
13. Community Recording & Reward system (in Platform)
14. Real courses seeded (25+ courses with actual content)
15. Knowledge Base / Wiki (in Platform)
16. Gamification framework (badges, challenges, leaderboards)
17. $MLY Tokenomics dashboard (in Platform)

### Phase 2 — Social & Community (Weeks 5-7)
18. MiForum (new repo)
19. MiSocial (new repo — merges existing /feed)
20. MiNews (in Platform)
21. Communication expansion (voice/video calls via WebRTC)
22. MiAcademia R&D (new repo)

### Phase 3 — Marketplace & Civic (Weeks 8-10)
23. MiMarket unified marketplace (new repo — absorbs shop, housing, rideshare)
24. MiCity GitHub-style expansion (new repo)
25. MiNav maps & navigation (new repo)
26. MiAuto (new repo)
27. Payment rails ($MLY ↔ USD bridge)

### Phase 4 — Advanced Intelligence (Weeks 11-14)
28. Mi AI expansion (new repo — agents, RAG, function calling)
29. MiDev Portal (new repo)
30. MiTwin digital twin (new repo)
31. Unified file/media pipeline
32. Privacy & data sovereignty tools

### Phase 5 — Scale & Distribution (Weeks 15-18)
33. Auto-scaling infrastructure
34. React Native mobile app
35. ActivityPub federation
36. Accessibility audit & expansion
37. Security audit
38. Performance optimization
39. Beta → Public launch prep

---

## Environment Variables Needed

```env
# Existing
NEXT_PUBLIC_SUPABASE_URL=
NEXT_PUBLIC_SUPABASE_ANON_KEY=
SUPABASE_SERVICE_ROLE_KEY=
GROQ_API_KEY=
UBI_CRON_SECRET=

# New (add as features are built)
NEXT_PUBLIC_SENTRY_DSN=
SENTRY_ORG=
SENTRY_PROJECT=
NEXT_PUBLIC_POSTHOG_KEY=
NEXT_PUBLIC_POSTHOG_HOST=
NEXT_PUBLIC_MAPLIBRE_KEY=
UPSTASH_REDIS_URL=
UPSTASH_REDIS_TOKEN=
RESEND_API_KEY=
JTA_GTFS_API_KEY=
READY_PLAYER_ME_APP_ID=
```

---

## Decision Points (Need Your Input)

### Architecture Decisions:
1. **Social media algorithm:** Pure chronological or include "For You" AI-ranked feed?
2. **Digital twin AI:** How autonomous should it be? Auto-vote? Auto-post?
3. **Marketplace escrow:** Who arbitrates disputes — AI, community jury, or both?
4. **City repair legal:** Partner with actual city government or operate independently?
5. **Forum moderation:** Elected mods, standing-based, or AI-first?
6. **Revenue model:** $MLY-only or eventually support USD transactions too?
7. **Mobile:** PWA-only or dedicated native app (React Native)?
8. **Open source:** Fully open or some components proprietary?

### New Decisions (From Gap Analysis):
9. **Database: real data or stubs?** Many pages currently work without real tables. Do you want ALL tables built before expansion, or build them as you expand each feature?
10. **Federation:** Should MiSocial posts federate to Mastodon/Threads via ActivityPub? This would give you free distribution but adds complexity.
11. **Voice/Video calls:** Build custom WebRTC or use a service (Twilio, Daily.co, LiveKit)?
12. **Cash bridge:** MiLyfe uses no third-party payment processor, ever. $MLY is earned through participation and exchanged peer-to-peer. If a real-world bridge is ever needed, it is a community-run peer-to-peer exchange, never a corporate gateway.
13. **Identity verification:** How far do you go? Just email? Phone? Government ID? Biometric? This affects trust levels and what people can do.
14. **AI hosting:** Stay on Groq free tier, or invest in dedicated AI (fine-tuned models, RAG infrastructure)? Budget question.
15. **Multi-city:** Is MiLyfe Jacksonville-only forever, or should architecture support multiple cities (each with their own governance, businesses, etc.)?
16. **Data ownership:** Do users truly own their data (can export, delete, take elsewhere)? This is a philosophical AND technical choice.

---

*This document is the design foundation. No code until design is approved. Each repo should start with its own README, data model, and API spec before implementation begins.*
