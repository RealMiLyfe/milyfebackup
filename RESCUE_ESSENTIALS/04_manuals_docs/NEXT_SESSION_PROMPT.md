# Next Session Prompt — Copy Everything Below the Line

---

Continue building MiLyfe Campaign Operations.

Context: The full audit is at hyperbolic-time-chamber/docs/ — read ULTIMATE_INTEGRATION_DESIGN.md and CAMPAIGN_OS_BUILD_PLAN.md.

The infrastructure is ALL built. 19 Docker containers running. 26 agents loaded. Campaign OS at :8200. 3D Office at :8787. Mayor site serving. Platform on Vercel.

NOTHING has produced real output yet. Fix that. Priority order:

1. Import all n8n workflows (5 JSON files in /workflows/) and get them running
2. Fix the morning brief to actually run at 6AM with working agents
3. Build the new SQLite tables (research_queue, verified_claims, etc.)
4. Build the new API endpoints (/research/queue, /research/verified, /intel/statements)
5. Get the SearXNG scheduled searches running (from searxng-target-list.md)
6. Publish the first Ghost blog post (use verified research from data/research/)
7. Post to Mastodon (first post — campaign announcement)
8. Configure Meilisearch to index campaign data
9. Build /illuminate page on mayor site
10. Add API auth to campaign-api write endpoints
11. Add Neo4j to Docker stack
12. Wire the content cascade (publish → Ghost + Postiz + Listmonk + Mastodon)

The machine is built. Make it produce.
