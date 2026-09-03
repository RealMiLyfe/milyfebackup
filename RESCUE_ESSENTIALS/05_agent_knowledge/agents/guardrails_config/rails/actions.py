"""Custom guardrail actions for the HTC agent system."""

from nemoguardrails.actions import action


@action()
async def check_platform_write(context: dict) -> bool:
    """Check if a message attempts to write to the platform.

    Returns True if the message is SAFE (no write attempt).
    Returns False if blocked.
    """
    message = context.get("user_message", "").lower()

    write_indicators = [
        "delete", "modify", "push", "deploy", "alter", "drop",
        "write to supabase", "execute migration", "change user",
        "update platform", "insert into", "create table",
    ]

    for indicator in write_indicators:
        if indicator in message:
            # Check if it's about the platform specifically
            platform_refs = ["platform", "supabase", "production", "app", "milyfe"]
            if any(ref in message for ref in platform_refs):
                return False

    return True


@action()
async def check_dead_terminology(context: dict) -> bool:
    """Check if agent output contains dead terminology.

    Returns True if output is CLEAN.
    Returns False if it contains dead terms.
    """
    response = context.get("bot_message", "").lower()

    dead_terms = [
        "blockchain", "token", "did", "wallet", "node",
        "smart contract", "web3", "crypto", "mijaxx", "cos",
        "disruptive", "innovative", "revolutionary", "game-changing",
    ]

    for term in dead_terms:
        if term in response:
            return False

    return True


@action()
async def check_personal_attacks(context: dict) -> bool:
    """Check if agent output contains personal attacks.

    Returns True if output is CLEAN.
    Returns False if it attacks character rather than record.
    """
    response = context.get("bot_message", "").lower()

    attack_indicators = [
        "terrible person", "incompetent", "stupid", "idiot",
        "corrupt individual", "evil", "disgusting", "pathetic",
        "their family", "their children", "their spouse",
    ]

    for indicator in attack_indicators:
        if indicator in response:
            return False

    return True
