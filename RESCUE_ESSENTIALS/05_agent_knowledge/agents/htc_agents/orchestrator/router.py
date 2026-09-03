"""Intent router — classifies incoming messages and routes to the correct agent."""

from __future__ import annotations

import re
from typing import Any

import structlog

from htc_agents.orchestrator.state import AgentRole, TaskPriority


log = structlog.get_logger()


# Prefix-based routing (explicit user intent from ROLES.md)
PREFIX_ROUTES = {
    # COMMANDER
    "strategy": AgentRole.COMMANDER,
    "strategy:": AgentRole.COMMANDER,
    "commander": AgentRole.COMMANDER,
    # SCOUT
    "research": AgentRole.SCOUT,
    "research:": AgentRole.SCOUT,
    "scout": AgentRole.SCOUT,
    "intel": AgentRole.SCOUT,
    "intel:": AgentRole.SCOUT,
    # STORYTELLER
    "write": AgentRole.STORYTELLER,
    "write:": AgentRole.STORYTELLER,
    "content": AgentRole.STORYTELLER,
    "draft": AgentRole.STORYTELLER,
    "storyteller": AgentRole.STORYTELLER,
    # SCOUT (rapid)
    "rapid": AgentRole.SCOUT,
    "rapid:": AgentRole.SCOUT,
    "breaking": AgentRole.SCOUT,
    # SENTINEL
    "compliance": AgentRole.SENTINEL,
    "legal": AgentRole.SENTINEL,
    "sentinel": AgentRole.SENTINEL,
    "filing": AgentRole.SENTINEL,
    # CONNECTOR
    "volunteer": AgentRole.CONNECTOR,
    "volunteers": AgentRole.CONNECTOR,
    "outreach": AgentRole.CONNECTOR,
    "connector": AgentRole.CONNECTOR,
    # BUILDER
    "platform": AgentRole.BUILDER,
    "builder": AgentRole.BUILDER,
    "demo": AgentRole.BUILDER,
    "feature": AgentRole.BUILDER,
    # GUARDIAN
    "health": AgentRole.GUARDIAN,
    "status": AgentRole.GUARDIAN,
    "guardian": AgentRole.GUARDIAN,
    "repair": AgentRole.GUARDIAN,
    # ANALYST
    "metrics": AgentRole.ANALYST,
    "performance": AgentRole.ANALYST,
    "analyst": AgentRole.ANALYST,
    "retrospective": AgentRole.ANALYST,
    "retro": AgentRole.ANALYST,
    # DEBATE_COACH
    "debate": AgentRole.DEBATE_COACH,
    "spar": AgentRole.DEBATE_COACH,
    "drill": AgentRole.DEBATE_COACH,
    "simulate": AgentRole.DEBATE_COACH,
    "coach": AgentRole.DEBATE_COACH,
    # FUNDRAISER
    "fundraise": AgentRole.FUNDRAISER,
    "fundraiser": AgentRole.FUNDRAISER,
    "donors": AgentRole.FUNDRAISER,
    "donate": AgentRole.FUNDRAISER,
    "money": AgentRole.FUNDRAISER,
    # SCHEDULER
    "schedule": AgentRole.SCHEDULER,
    "calendar": AgentRole.SCHEDULER,
    "scheduler": AgentRole.SCHEDULER,
    "today": AgentRole.SCHEDULER,
    "tomorrow": AgentRole.SCHEDULER,
    "where": AgentRole.SCHEDULER,
    # POLLSTER
    "pulse": AgentRole.POLLSTER,
    "sentiment": AgentRole.POLLSTER,
    "pollster": AgentRole.POLLSTER,
    "trending": AgentRole.POLLSTER,
    # MEDIA_COACH
    "press": AgentRole.MEDIA_COACH,
    "media": AgentRole.MEDIA_COACH,
    "interview": AgentRole.MEDIA_COACH,
    "reporter": AgentRole.MEDIA_COACH,
    # OPPO_TRACKER
    "oppo": AgentRole.OPPO_TRACKER,
    "opposition": AgentRole.OPPO_TRACKER,
    "donor": AgentRole.OPPO_TRACKER,
    "tracker": AgentRole.OPPO_TRACKER,
    # GROUND_GAME
    "precinct": AgentRole.GROUND_GAME,
    "doors": AgentRole.GROUND_GAME,
    "canvass": AgentRole.GROUND_GAME,
    "ground": AgentRole.GROUND_GAME,
    "turf": AgentRole.GROUND_GAME,
    "petition": AgentRole.GROUND_GAME,
    # CRISIS_MANAGER
    "crisis": AgentRole.CRISIS_MANAGER,
    "attack": AgentRole.CRISIS_MANAGER,
    "defend": AgentRole.CRISIS_MANAGER,
    "damage": AgentRole.CRISIS_MANAGER,
    # SPEECHWRITER
    "speech": AgentRole.SPEECHWRITER,
    "keynote": AgentRole.SPEECHWRITER,
    "remarks": AgentRole.SPEECHWRITER,
    "townhall": AgentRole.SPEECHWRITER,
    "stump": AgentRole.SPEECHWRITER,
    # COALITION_BUILDER
    "coalition": AgentRole.COALITION_BUILDER,
    "endorsement": AgentRole.COALITION_BUILDER,
    "churches": AgentRole.COALITION_BUILDER,
    "unions": AgentRole.COALITION_BUILDER,
    "organizations": AgentRole.COALITION_BUILDER,
}

# Keyword patterns for intent classification when no prefix match
KEYWORD_PATTERNS = {
    AgentRole.COMMANDER: [
        r"priorit", r"big picture", r"overall strategy",
        r"campaign direction", r"what should.*focus",
        r"morning brief", r"next step", r"campaign plan",
    ],
    AgentRole.SCOUT: [
        r"news", r"breaking",
        r"just announced", r"what happened", r"responded",
        r"jacksonville.*news", r"city council", r"jea",
    ],
    AgentRole.STORYTELLER: [
        r"write.*post", r"draft.*post", r"linkedin", r"tweet", r"blog",
        r"email blast", r"social media",
        r"how.*say", r"content", r"narrative",
    ],
    AgentRole.SENTINEL: [
        r"deadline", r"filing", r"compliance", r"legal", r"finance report",
        r"disclosure", r"regulation", r"election law", r"fec",
    ],
    AgentRole.CONNECTOR: [
        r"volunteer", r"sign.*up", r"recruit",
        r"event", r"rally", r"meetup", r"organize",
    ],
    AgentRole.BUILDER: [
        r"platform", r"milyfe.*app", r"how does.*work", r"feature",
        r"demo", r"architecture", r"standing", r"design law",
    ],
    AgentRole.GUARDIAN: [
        r"service.*down", r"not working", r"restart", r"health check",
        r"container", r"docker", r"server", r"error", r"crash",
    ],
    AgentRole.ANALYST: [
        r"metric", r"growth", r"compare",
        r"last week", r"progress", r"retrospective",
        r"what.*working", r"improve", r"kpi",
    ],
    AgentRole.DEBATE_COACH: [
        r"debate", r"spar", r"mock", r"practice.*answer",
        r"how.*respond.*to", r"score.*answer", r"drill",
        r"what.*they.*say", r"attack.*line", r"prepare.*for",
    ],
    AgentRole.FUNDRAISER: [
        r"fundrais", r"donat", r"donor", r"money",
        r"contribution", r"house party", r"ask.*email",
        r"finance limit", r"small dollar", r"raise.*fund",
    ],
    AgentRole.SCHEDULER: [
        r"schedule", r"calendar", r"today", r"tomorrow",
        r"this week", r"where should.*be", r"time.*block",
        r"what.*time", r"best.*location", r"plan.*day",
    ],
    AgentRole.POLLSTER: [
        r"sentiment", r"pulse", r"trending", r"talking about",
        r"public opinion", r"what.*people.*think",
        r"issue.*track", r"neighborhood.*care", r"hot.*issue",
    ],
    AgentRole.MEDIA_COACH: [
        r"press", r"media", r"interview", r"reporter",
        r"press release", r"pitch.*story", r"earned media",
        r"tv", r"radio", r"podcast", r"op.?ed",
    ],
    AgentRole.OPPO_TRACKER: [
        r"deegan.*donor", r"opponent.*network", r"pac",
        r"who.*fund", r"endorsement.*chain", r"voting record",
        r"accountability", r"promise.*broke", r"dark money",
    ],
    AgentRole.GROUND_GAME: [
        r"precinct", r"door.*knock", r"canvass", r"turf",
        r"signature.*gap", r"voter file", r"petition.*target",
        r"win number", r"turnout", r"zone",
    ],
    AgentRole.CRISIS_MANAGER: [
        r"crisis", r"attack.*on.*us", r"hit piece", r"defend",
        r"they.*saying", r"bad press", r"damage control",
        r"respond.*to.*attack", r"counter.*narrative",
    ],
    AgentRole.SPEECHWRITER: [
        r"speech", r"keynote", r"remarks", r"town hall.*open",
        r"elevator pitch", r"stump", r"2.minute", r"30.second",
        r"debate answer", r"closing.*statement",
    ],
    AgentRole.COALITION_BUILDER: [
        r"coalition", r"endorsement", r"church", r"union",
        r"organization", r"association", r"partnership",
        r"institutional", r"naacp", r"chamber.*commerce",
    ],
}

# Priority keywords
URGENT_KEYWORDS = [
    r"urgent", r"breaking", r"just announced", r"right now",
    r"immediately", r"asap", r"rapid response", r"attack",
]

HIGH_KEYWORDS = [
    r"deadline", r"today", r"tomorrow", r"this morning",
    r"important", r"critical",
]


def classify_intent(message: str) -> tuple[AgentRole, TaskPriority, str, list[AgentRole]]:
    """Classify a message into an agent route and priority.

    Returns:
        (primary_agent, priority, intent_description, secondary_agents)
    """
    lower = message.lower().strip()

    # 1. Check explicit prefix routing
    first_word = lower.split()[0] if lower.split() else ""
    # Also check "word:" format
    prefix_check = first_word.rstrip(":")

    if prefix_check in PREFIX_ROUTES:
        primary = PREFIX_ROUTES[prefix_check]
        priority = _classify_priority(lower)
        intent = f"explicit_{primary.value}_request"
        secondary = _get_secondary_agents(primary, lower)
        log.info(
            "router.prefix_match",
            prefix=prefix_check,
            agent=primary.value,
        )
        return primary, priority, intent, secondary

    # 2. Keyword-based scoring
    scores: dict[AgentRole, int] = {role: 0 for role in AgentRole}

    for role, patterns in KEYWORD_PATTERNS.items():
        for pattern in patterns:
            matches = re.findall(pattern, lower)
            scores[role] += len(matches)

    # Get top agent
    top_role = max(scores, key=scores.get)
    top_score = scores[top_role]

    if top_score == 0:
        # Default to COMMANDER for general questions
        top_role = AgentRole.COMMANDER
        intent = "general_question"
    else:
        intent = f"keyword_match_{top_role.value}"

    # Find secondary agents (any with score > 0 that aren't primary)
    secondary = [
        role for role, score in sorted(
            scores.items(), key=lambda x: x[1], reverse=True
        )
        if score > 0 and role != top_role
    ][:2]

    priority = _classify_priority(lower)

    log.info(
        "router.classified",
        primary=top_role.value,
        priority=priority.value,
        intent=intent,
        scores={k.value: v for k, v in scores.items() if v > 0},
    )

    return top_role, priority, intent, secondary


def _classify_priority(message: str) -> TaskPriority:
    """Determine task priority from message content."""
    for pattern in URGENT_KEYWORDS:
        if re.search(pattern, message):
            return TaskPriority.URGENT

    for pattern in HIGH_KEYWORDS:
        if re.search(pattern, message):
            return TaskPriority.HIGH

    return TaskPriority.NORMAL


def _get_secondary_agents(primary: AgentRole, message: str) -> list[AgentRole]:
    """Determine if additional agents should be consulted."""
    secondary = []

    # Strategy requests often need intel
    if primary == AgentRole.COMMANDER:
        if re.search(r"opponent|deegan|candidate", message):
            secondary.append(AgentRole.SCOUT)

    # Content requests may need compliance check
    if primary == AgentRole.STORYTELLER:
        secondary.append(AgentRole.SENTINEL)

    # Outreach may need content support
    if primary == AgentRole.CONNECTOR:
        if re.search(r"write|draft|message", message):
            secondary.append(AgentRole.STORYTELLER)

    return secondary[:2]
