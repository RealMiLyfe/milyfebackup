"""Mattermost bot integration — full-featured campaign operations hub.

Modules:
    main — Bot plugin, channel routing, threaded conversations
    chains — Multi-agent pipelines with handoffs
    scheduler — Daily rhythm cron tasks (morning brief, opponent scans, etc.)
    workflows — Approval workflows, feedback, knowledge ingestion, interrupts
    simulation — Autonomous debate drills, crisis tabletops, content sprints
    integrations — Ghost, Listmonk, Mastodon, SearXNG enhanced
    dashboards — Live metrics per channel
"""

from htc_agents.bot.main import create_bot

__all__ = ["create_bot"]
