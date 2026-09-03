"""Entry point for the HTC multi-agent system.

Runs three things concurrently:
1. FastAPI health/webhook server (port 8067)
2. mmpy_bot Mattermost connection (websocket)
3. Daily rhythm scheduler (cron-based proactive agent tasks)
"""

import asyncio
import sys
import threading

import structlog

from htc_agents.config import settings


log = structlog.get_logger()


def main():
    """Start the multi-agent system with all subsystems."""
    log.info(
        "htc_agents.starting",
        version="0.2.0",
        environment=settings.ENVIRONMENT,
    )

    try:
        # Import here to trigger the httpx monkey-patch in bot/main.py
        from htc_agents.bot.main import (
            create_bot,
            initialize_system,
            api,
            _agents,
            _memory,
        )
        import uvicorn

        # 1. Run async initialization (loads knowledge, memory, agents, guardrails)
        asyncio.run(initialize_system())

        # 2. Start FastAPI in a background thread
        def run_api():
            uvicorn.run(api, host="0.0.0.0", port=8067, log_level="warning")

        api_thread = threading.Thread(target=run_api, daemon=True)
        api_thread.start()
        log.info("system.api_started", port=8067)

        # 3. Start the kernel loop + daily rhythm scheduler in a background thread.
        #    The kernel is what makes the system act on its own: it listens for events
        #    and dispatches agent work as durable jobs. The rhythm now feeds it events.
        def run_kernel_and_scheduler():
            from htc_agents.bot.scheduler import DailyRhythm
            from htc_agents.bot.main import _agents, _memory, start_kernel

            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

            # Start the kernel event loop (background task inside this loop).
            loop.run_until_complete(start_kernel())

            # Start the daily rhythm; it publishes events onto the kernel bus.
            rhythm = DailyRhythm(agents=_agents, memory=_memory)
            loop.run_until_complete(rhythm.start())

            # Keep the loop alive for the bus + scheduler.
            loop.run_forever()

        kernel_thread = threading.Thread(target=run_kernel_and_scheduler, daemon=True)
        kernel_thread.start()
        log.info("system.kernel_and_scheduler_started")

        # 4. Start the mmpy_bot (this blocks on the main thread via websocket)
        from htc_agents.bot.main import create_mattermost_bot

        bot = create_mattermost_bot()
        if bot is not None:
            # Ensure fresh event loop for mmpy_bot
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            log.info("system.bot_starting")
            bot.run()
        else:
            # API-only mode — keep alive
            log.warning("system.api_only_mode")
            import time
            while True:
                time.sleep(3600)

    except KeyboardInterrupt:
        log.info("htc_agents.shutdown", reason="keyboard_interrupt")
        sys.exit(0)
    except Exception as exc:
        log.error("htc_agents.fatal", error=str(exc))
        sys.exit(1)


if __name__ == "__main__":
    main()
