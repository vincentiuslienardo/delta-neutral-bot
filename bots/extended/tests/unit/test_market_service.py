from unittest.mock import MagicMock

import pytest

from src.application.services.market_service import MarketService
from src.domain.exceptions import StreamError
from src.domain.order_book import OrderBookUpdate


@pytest.mark.asyncio
async def test_monitor_order_book():
    mock_stream_port = MagicMock()
    mock_update = OrderBookUpdate(
        pair="HYPE-USD", bids=[[100.0, 1.0]], asks=[[101.0, 1.0]], timestamp=1234567890
    )

    async def async_generator():
        yield mock_update

    mock_stream_port.subscribe_to_bbo.return_value = async_generator()

    service = MarketService(stream_port=mock_stream_port)

    iterator = service.stream_port.subscribe_to_bbo("HYPE-USD")
    result = [i async for i in iterator]

    assert result[0] == mock_update
    mock_stream_port.subscribe_to_bbo.assert_called_with("HYPE-USD")


@pytest.mark.asyncio
async def test_monitor_order_book_stream_error():
    mock_stream_port = MagicMock()

    async def async_generator_error():
        raise StreamError("Stream failed")
        yield

    async def error_gen():
        raise StreamError("Stream failed")
        yield

    mock_stream_port.subscribe_to_bbo.return_value = error_gen()

    service = MarketService(stream_port=mock_stream_port)

    with pytest.raises(StreamError):
        await service.monitor_order_book("HYPE-USD")
