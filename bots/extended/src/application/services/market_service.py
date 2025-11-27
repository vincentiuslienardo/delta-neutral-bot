import structlog

from src.application.ports.stream_port import StreamPort
from src.domain.exceptions import StreamError

logger = structlog.get_logger()


class MarketService:
    def __init__(self, stream_port: StreamPort):
        self.stream_port = stream_port

    async def monitor_order_book(self, pair: str, depth: int | None = None):
        logger.info("starting_order_book_monitor", pair=pair)
        try:
            async for update in self.stream_port.subscribe_to_bbo(pair):
                best_bid = update.best_bid
                best_ask = update.best_ask

                logger.info(
                    "order_book_update",
                    pair=update.pair,
                    best_bid=best_bid,
                    best_ask=best_ask,
                    timestamp=update.timestamp,
                )
        except StreamError as e:
            logger.error("stream_error", error=str(e), pair=pair)
            raise
        except Exception as e:
            logger.error("unexpected_error", error=str(e), pair=pair)
            raise
