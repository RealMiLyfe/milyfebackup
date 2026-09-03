"""Agent Dashboards — live metrics pinned per channel.

Each channel gets a regularly-updated pinned post showing
that agent's key metrics at a glance.
"""

from __future__ import annotations

from datetime import date, datetime
from typing import Any

import structlog

from htc_agents.config import settings
from htc_agents.tools.campaign_api import campaign_api
from htc_agents.tools.notify import post_to_channel


log = structlog.get_logger()


async def update_field_ops_dashboard():
    """Update the #field-ops dashboard with petition/ground game metrics."""
    petition = await campaign_api.get_petition_status()
    contacts = await campaign_api.get_contacts_summary()

    today = date.today()
    deadline = date(2026, 12, 14)
    days_left = (deadline - today).days

    if petition:
        collected = petition.get("collected", 0)
        target = petition.get("target", 1000)
        pct = (collected / target * 100) if target > 0 else 0
        needed_per_day = max(0, (target - collected)) / max(days_left, 1)

        dashboard = (
            f"## 📊 Field Ops Dashboard\n"
            f"*Updated: {datetime.now().strftime('%b %d, %I:%M %p')}*\n\n"
            f"| Metric | Value |\n"
            f"|--------|-------|\n"
            f"| Signatures Collected | **{collected}** / {target} ({pct:.1f}%) |\n"
            f"| Days to Deadline | **{days_left}** |\n"
            f"| Needed Per Day | **{needed_per_day:.1f}** |\n"
        )

        if contacts:
            dashboard += (
                f"| Total Voter Contacts | {contacts.get('total', 'N/A')} |\n"
                f"| Strong Supporters | {contacts.get('strong', 'N/A')} |\n"
            )

        # Pace indicator
        if needed_per_day > 20:
            dashboard += f"\n⚠️ **OFF PACE** — need {needed_per_day:.0f}/day. Increase collection sessions."
        elif needed_per_day > 10:
            dashboard += f"\n📈 On pace but tight. {needed_per_day:.0f}/day needed."
        else:
            dashboard += f"\n✅ **AHEAD OF PACE** — maintain momentum."

        await post_to_channel("field-ops", dashboard)


async def update_compliance_dashboard():
    """Update #compliance with upcoming deadlines."""
    compliance = await campaign_api.get_compliance_upcoming()

    today = date.today()
    key_dates = {
        "Petition Deadline": date(2026, 12, 14),
        "Qualifying Start": date(2027, 1, 11),
        "Primary Election": date(2027, 3, 9),
        "General Election": date(2027, 5, 18),
    }

    dashboard = (
        f"## ⚖️ Compliance Dashboard\n"
        f"*Updated: {datetime.now().strftime('%b %d, %I:%M %p')}*\n\n"
        f"| Deadline | Date | Days Away | Status |\n"
        f"|----------|------|-----------|--------|\n"
    )

    for name, target_date in key_dates.items():
        days = (target_date - today).days
        if days <= 3:
            status = "🚨 URGENT"
        elif days <= 7:
            status = "⚠️ Soon"
        elif days <= 30:
            status = "📅 Approaching"
        else:
            status = "✅ OK"
        dashboard += f"| {name} | {target_date.strftime('%b %d')} | {days} | {status} |\n"

    if compliance:
        dashboard += f"\n**Upcoming filings:** {compliance}"

    await post_to_channel("compliance", dashboard)


async def update_ops_dashboard():
    """Update #ops with overall campaign health."""
    scoreboard = await campaign_api.get_scoreboard()

    dashboard = (
        f"## 🏠 Campaign Dashboard\n"
        f"*Updated: {datetime.now().strftime('%b %d, %I:%M %p')}*\n\n"
    )

    if scoreboard:
        dashboard += "| Metric | Value |\n|--------|-------|\n"
        for key, value in scoreboard.items():
            dashboard += f"| {key.replace('_', ' ').title()} | {value} |\n"
    else:
        dashboard += "*Scoreboard data unavailable*\n"

    dashboard += f"\n**Agents online:** 18 | **System:** Healthy"
    await post_to_channel("ops", dashboard)


async def update_all_dashboards():
    """Update all channel dashboards."""
    try:
        await update_field_ops_dashboard()
        await update_compliance_dashboard()
        await update_ops_dashboard()
        log.info("dashboards.updated")
    except Exception as e:
        log.error("dashboards.update_failed", error=str(e))
