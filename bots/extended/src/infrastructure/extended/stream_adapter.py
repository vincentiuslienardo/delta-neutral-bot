from collections.abc import AsyncIterator

import structlog
from x10.perpetual.stream_client.stream_client import PerpetualStreamClient

from src.application.ports.stream_port import StreamPort
from src.domain.exceptions import DataParsingError, StreamConnectionError
from src.domain.order_book import OrderBookUpdate

logger = structlog.get_logger()


class StreamAdapter(StreamPort):
    def __init__(self, api_url: str):
        self.client = PerpetualStreamClient(api_url=api_url)

    async def subscribe_to_bbo(self, pair: str) -> AsyncIterator[OrderBookUpdate]:
        logger.info("subscribing_to_bbo", pair=pair)
        try:
            connection = self.client.subscribe_to_orderbooks(market_name=pair, depth=1)
            async with connection as stream:
                async for msg in stream:
                    if not msg.data:
                        continue

                    try:
                        bids = self._extract_price_qty(msg.data, "bid")
                        asks = self._extract_price_qty(msg.data, "ask")

                        yield OrderBookUpdate(
                            pair=pair,
                            bids=bids,
                            asks=asks,
                            timestamp=getattr(msg, "ts", None),
                        )
                    except DataParsingError as e:
                        logger.error("data_parsing_error", error=str(e), pair=pair)
                        continue
        except Exception as e:
            logger.error("stream_connection_error", error=str(e), pair=pair)
            raise StreamConnectionError(
                f"Failed to subscribe to BBO for {pair}: {e}"
            ) from e

    def _extract_price_qty(self, data, side: str) -> list[list[float]]:
        try:
            items = getattr(data, side, [])
            if not items:
                return []
            return [[float(item.price), float(item.qty)] for item in items]
        except (AttributeError, ValueError, TypeError) as e:
            raise DataParsingError(f"Failed to extract {side} data: {e}") from e
