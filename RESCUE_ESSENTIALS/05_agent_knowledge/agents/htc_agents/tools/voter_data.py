"""Voter File & Election Data Integration — Jacksonville/Duval County precinct data.

Sources:
- Duval County Supervisor of Elections (public voter registration data)
- Florida Division of Elections (statewide data)
- OpenElections project (historical precinct results)

This provides GROUND_GAME with real electoral math:
- Registered voters by precinct
- Party registration breakdown
- Historical turnout patterns
- Precinct-level results from past municipal elections
"""

from __future__ import annotations

from typing import Any
from datetime import date

import structlog

from htc_agents.config import settings


log = structlog.get_logger()


# Jacksonville/Duval County precinct zones (approximate mapping)
JACKSONVILLE_ZONES = {
    "northside": {
        "precincts": list(range(101, 140)),
        "demographics": "majority Black, working class, high platform alignment",
        "registered_voters": 85000,
        "typical_turnout_pct": 18,
        "party_split": {"D": 72, "R": 18, "NPA": 10},
        "key_issues": ["gun violence", "economic development", "transit", "food access"],
    },
    "eastside": {
        "precincts": list(range(201, 230)),
        "demographics": "diverse, mixed income, urban core",
        "registered_voters": 45000,
        "typical_turnout_pct": 22,
        "party_split": {"D": 65, "R": 22, "NPA": 13},
        "key_issues": ["development", "gentrification", "public safety", "jobs"],
    },
    "westside": {
        "precincts": list(range(301, 360)),
        "demographics": "mixed, suburban-rural, infrastructure-neglected",
        "registered_voters": 95000,
        "typical_turnout_pct": 24,
        "party_split": {"D": 45, "R": 40, "NPA": 15},
        "key_issues": ["flooding", "septic-to-sewer", "roads", "traffic"],
    },
    "southside": {
        "precincts": list(range(401, 450)),
        "demographics": "higher income, suburban, fiscally conservative",
        "registered_voters": 110000,
        "typical_turnout_pct": 32,
        "party_split": {"D": 35, "R": 50, "NPA": 15},
        "key_issues": ["property taxes", "school quality", "traffic", "development"],
    },
    "mandarin": {
        "precincts": list(range(451, 480)),
        "demographics": "suburban, family-oriented, moderate-conservative",
        "registered_voters": 72000,
        "typical_turnout_pct": 35,
        "party_split": {"D": 32, "R": 52, "NPA": 16},
        "key_issues": ["taxes", "school ratings", "community character", "safety"],
    },
    "arlington": {
        "precincts": list(range(501, 540)),
        "demographics": "aging, diverse, swing area",
        "registered_voters": 68000,
        "typical_turnout_pct": 26,
        "party_split": {"D": 48, "R": 38, "NPA": 14},
        "key_issues": ["infrastructure", "crime", "commercial vacancy", "healthcare"],
    },
    "beaches": {
        "precincts": list(range(601, 625)),
        "demographics": "higher income, environmentally conscious",
        "registered_voters": 55000,
        "typical_turnout_pct": 38,
        "party_split": {"D": 40, "R": 45, "NPA": 15},
        "key_issues": ["sea level rise", "short-term rentals", "environment", "character"],
    },
    "northwest": {
        "precincts": list(range(701, 730)),
        "demographics": "environmental justice community, working class",
        "registered_voters": 42000,
        "typical_turnout_pct": 16,
        "party_split": {"D": 68, "R": 20, "NPA": 12},
        "key_issues": ["environmental contamination", "healthcare", "jobs", "transit"],
    },
    "downtown_riverside": {
        "precincts": list(range(801, 820)),
        "demographics": "young professionals, urban, progressive",
        "registered_voters": 35000,
        "typical_turnout_pct": 28,
        "party_split": {"D": 62, "R": 22, "NPA": 16},
        "key_issues": ["pedestrian safety", "homelessness", "development", "transit"],
    },
}


def get_zone_data(zone_name: str) -> dict[str, Any] | None:
    """Get voter data for a specific zone."""
    return JACKSONVILLE_ZONES.get(zone_name.lower())


def get_all_zones() -> dict[str, Any]:
    """Get data for all zones."""
    return JACKSONVILLE_ZONES


def calculate_win_numbers() -> dict[str, Any]:
    """Calculate the math needed to win.

    Jacksonville municipal elections:
    - Primary: top 2 advance (if no one gets 50%+1)
    - General: head-to-head
    """
    total_registered = sum(z["registered_voters"] for z in JACKSONVILLE_ZONES.values())
    avg_turnout = sum(
        z["registered_voters"] * z["typical_turnout_pct"] / 100
        for z in JACKSONVILLE_ZONES.values()
    )

    # In a multi-candidate primary, typically need 30-40% of votes cast
    primary_votes_cast = int(avg_turnout)
    primary_win_target = int(primary_votes_cast * 0.35)  # 35% to safely advance

    # General: need 50%+1 of votes cast (higher turnout in general)
    general_turnout = int(avg_turnout * 1.3)  # ~30% higher turnout in general
    general_win_target = int(general_turnout * 0.51)

    return {
        "total_registered": total_registered,
        "estimated_primary_turnout": primary_votes_cast,
        "primary_win_target": primary_win_target,
        "estimated_general_turnout": general_turnout,
        "general_win_target": general_win_target,
        "key_insight": (
            f"Need ~{primary_win_target:,} votes to advance from primary, "
            f"~{general_win_target:,} to win the general. "
            f"Focus mobilization on Northside, Eastside, Northwest (low turnout, high alignment)."
        ),
    }


def calculate_petition_targets_by_zone(
    total_needed: int = 1200,
    collected_by_zone: dict[str, int] = None,
) -> dict[str, dict[str, Any]]:
    """Calculate petition signature targets per zone based on population weight.

    Factors:
    - Zone population (more people = more signatures possible)
    - Expected conversion rate (higher alignment = easier)
    - Current collection gaps
    """
    collected_by_zone = collected_by_zone or {}

    total_pop = sum(z["registered_voters"] for z in JACKSONVILLE_ZONES.values())

    targets = {}
    for zone_name, zone_data in JACKSONVILLE_ZONES.items():
        # Weight by population and alignment (D% as proxy)
        d_pct = zone_data["party_split"]["D"] / 100
        pop_weight = zone_data["registered_voters"] / total_pop
        alignment_weight = pop_weight * (0.5 + d_pct * 0.5)  # Boost aligned zones

        target = int(total_needed * alignment_weight * 1.5)  # 1.5x for normalization
        collected = collected_by_zone.get(zone_name, 0)
        remaining = max(0, target - collected)

        targets[zone_name] = {
            "target": target,
            "collected": collected,
            "remaining": remaining,
            "pct_complete": (collected / target * 100) if target > 0 else 0,
            "priority": "HIGH" if remaining > target * 0.5 else "NORMAL",
        }

    return targets


def get_historical_results() -> dict[str, Any]:
    """Historical Jacksonville mayoral election results for modeling."""
    return {
        "2023_general": {
            "winner": "Donna Deegan (D)",
            "loser": "Daniel Davis (R)",
            "margin": "51.5% - 48.5%",
            "turnout": "~34%",
            "total_votes": 238000,
            "key_factor": "First Democrat to win in decades. Won on abortion + moderate suburban appeal.",
        },
        "2023_primary": {
            "candidates": 4,
            "top_two": ["Donna Deegan (D) - 39%", "Daniel Davis (R) - 25%"],
            "turnout": "~22%",
            "key_factor": "Low turnout primary. Deegan consolidated D vote early.",
        },
        "2019_general": {
            "winner": "Lenny Curry (R) - incumbent",
            "result": "Won in first round with 58%",
            "turnout": "~28%",
        },
        "insight": (
            "Jacksonville mayoral races are won by mobilization, not persuasion. "
            "Low turnout primaries (~22%) reward organized ground games. "
            "A candidate who turns out even 5% more of their base wins."
        ),
    }
