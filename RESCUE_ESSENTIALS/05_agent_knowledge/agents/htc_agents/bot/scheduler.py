"""Daily Rhythm Scheduler — proactive agent tasks on a schedule.

Agents work WITHOUT being asked:
- 6:00 AM: Morning brief (scout + analyst → commander)
- 8:00 AM: Opponent scan #1 (scout + oppo_tracker)
- 9:00 AM: Daily schedule post (scheduler)
- 2:00 PM: Opponent scan #2 (scout)
- 5:00 PM: Petition pace check (ground_game)
- 8:00 PM: Opponent scan #3 (scout)
- 9:00 PM: Daily wrap (analyst)
- Sunday 7 PM: Weekly retro (analyst + commander)
- Monday 8 AM: Week plan (scheduler + commander)
- 3 days before deadlines: Sentinel escalation
"""

from __future__ import annotations

import asyncio
from datetime import datetime, time as dtime
from typing import Any, Callable

import structlog

from htc_agents.config import settings
from htc_agents.tools.notify import post_to_channel, send_alert
from htc_agents.kernel.events import event_bus, EventType


log = structlog.get_logger()


class DailyRhythm:
    """Schedules proactive agent work throughout the day."""

    def __init__(self, agents: dict[str, Any], memory: Any = None):
        self.agents = agents
        self.memory = memory
        self._running = False
        self._task: asyncio.Task | None = None

    async def start(self):
        """Start the rhythm scheduler in the background."""
        self._running = True
        self._task = asyncio.create_task(self._run_loop())
        log.info("rhythm.started")

    async def stop(self):
        """Stop the scheduler."""
        self._running = False
        if self._task:
            self._task.cancel()
        log.info("rhythm.stopped")

    async def _run_loop(self):
        """Main scheduler loop — checks every minute for scheduled tasks."""
        last_executed: dict[str, str] = {}  # task_name → last date executed

        while self._running:
            try:
                now = datetime.now()
                current_time = now.strftime("%H:%M")
                today = now.strftime("%Y-%m-%d")
                weekday = now.strftime("%A")

                for task in DAILY_SCHEDULE:
                    task_key = f"{task['name']}_{today}"

                    # Skip if already run today
                    if task_key in last_executed:
                        continue

                    # Check if it's time
                    if current_time == task["time"]:
                        # Check day filter
                        if task.get("days") and weekday not in task["days"]:
                            continue

                        log.info("rhythm.executing", task=task["name"], time=current_time)
                        last_executed[task_key] = current_time

                        try:
                            await task["fn"](self.agents, self.memory)
                        except Exception as e:
                            log.error("rhythm.task_failed", task=task["name"], error=str(e))

            except asyncio.CancelledError:
                break
            except Exception as e:
                log.error("rhythm.loop_error", error=str(e))

            await asyncio.sleep(60)  # Check every minute

    # ─── Scheduled Task Implementations ────────────────────────
    #
    # These no longer call agents directly. They publish events onto the kernel bus,
    # and the kernel's reactions dispatch the agent work as durable jobs. A "scheduled
    # time" is now just one more event source — the same path an ad-hoc trigger uses.

    @staticmethod
    async def morning_brief(agents: dict, memory: Any):
        """6:00 AM — Emit the morning-brief event."""
        await event_bus.emit(EventType.RHYTHM_MORNING_BRIEF, source="rhythm")

    @staticmethod
    async def opponent_scan(agents: dict, memory: Any):
        """8am/2pm/8pm — Emit an opponent-scan event."""
        await event_bus.emit(EventType.RHYTHM_OPPONENT_SCAN, source="rhythm")

    @staticmethod
    async def daily_schedule(agents: dict, memory: Any):
        """9:00 AM — Emit the daily-schedule event."""
        await event_bus.emit(EventType.RHYTHM_DAILY_SCHEDULE, source="rhythm")

    @staticmethod
    async def petition_pace_check(agents: dict, memory: Any):
        """5:00 PM — Emit the petition-pace event."""
        await event_bus.emit(EventType.RHYTHM_PETITION_PACE, source="rhythm")

    @staticmethod
    async def daily_wrap(agents: dict, memory: Any):
        """9:00 PM — Emit the daily-wrap event."""
        await event_bus.emit(EventType.RHYTHM_DAILY_WRAP, source="rhythm")

    @staticmethod
    async def weekly_retro(agents: dict, memory: Any):
        """Sunday 7 PM — Full weekly retrospective."""
        from htc_agents.bot.chains import run_chain

        result = await run_chain(
            "Run the full weekly retrospective: what worked, what didn't, "
            "key metrics vs goals, and strategic recommendations for next week.",
            ["analyst", "ground_game", "commander"],
            agents,
            memory,
        )

        retro = result.get("final_response", "Retro generation failed.")
        await post_to_channel("ops", f"## 📋 Weekly Retrospective\n\n{retro}")

    @staticmethod
    async def week_plan(agents: dict, memory: Any):
        """Monday 8 AM — Build the week's plan."""
        from htc_agents.bot.chains import run_chain

        result = await run_chain(
            "Build this week's campaign plan: priority goals, key events, "
            "petition collection targets by day, content calendar, and any deadlines.",
            ["scheduler", "ground_game", "commander"],
            agents,
            memory,
        )

        plan = result.get("final_response", "Week plan generation failed.")
        await post_to_channel("ops", f"## 📆 This Week's Plan\n\n{plan}")

    @staticmethod
    async def deadline_check(agents: dict, memory: Any):
        """Daily — Emit the deadline-check event (sentinel reaction handles it)."""
        await event_bus.emit(EventType.RHYTHM_DEADLINE_CHECK, source="rhythm")


# ═══════════════════════════════════════════════════════════════
# SCHEDULE DEFINITION
# ═══════════════════════════════════════════════════════════════

DAILY_SCHEDULE = [
    {"name": "morning_brief", "time": "06:00", "fn": DailyRhythm.morning_brief},
    {"name": "opponent_scan_1", "time": "08:00", "fn": DailyRhythm.opponent_scan},
    {"name": "daily_schedule", "time": "09:00", "fn": DailyRhythm.daily_schedule},
    {"name": "deadline_check", "time": "10:00", "fn": DailyRhythm.deadline_check},
    {"name": "opponent_scan_2", "time": "14:00", "fn": DailyRhythm.opponent_scan},
    {"name": "petition_pace", "time": "17:00", "fn": DailyRhythm.petition_pace_check},
    {"name": "opponent_scan_3", "time": "20:00", "fn": DailyRhythm.opponent_scan},
    {"name": "daily_wrap", "time": "21:00", "fn": DailyRhythm.daily_wrap},
    {"name": "weekly_retro", "time": "19:00", "fn": DailyRhythm.weekly_retro, "days": ["Sunday"]},
    {"name": "week_plan", "time": "08:00", "fn": DailyRhythm.week_plan, "days": ["Monday"]},
]
