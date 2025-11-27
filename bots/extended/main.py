import asyncio

import structlog

from src.application.services.market_service import MarketService
from src.config import settings
from src.domain.exceptions import BotError
from src.infrastructure.extended.stream_adapter import StreamAdapter
from src.infrastructure.logging import setup_logging

logger = structlog.get_logger()


async def main():
    setup_logging()

    pair = settings.PAIR
    logger.info("starting_bot", pair=pair)

    # Infrastructure
    stream_adapter = StreamAdapter(api_url=settings.API_URL)

    # Application
    market_service = MarketService(stream_port=stream_adapter)

    try:
        await market_service.monitor_order_book(pair)
    except KeyboardInterrupt:
        logger.info("stopping_bot")
    except BotError as e:
        logger.critical("bot_fatal_error", error=str(e))
    except Exception as e:
        logger.critical("unexpected_fatal_error", error=str(e))


if __name__ == "__main__":
    asyncio.run(main())
