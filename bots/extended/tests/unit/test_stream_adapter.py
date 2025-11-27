from unittest.mock import AsyncMock, MagicMock

import pytest

from src.domain.exceptions import StreamConnectionError
from src.infrastructure.extended.stream_adapter import StreamAdapter


@pytest.mark.asyncio
async def test_subscribe_to_bbo():
    mock_client = MagicMock()
    adapter = StreamAdapter(api_url="http://test.url")
    adapter.client = mock_client

    mock_connection = MagicMock()
    mock_stream = AsyncMock()

    mock_msg = MagicMock()
    mock_msg.data.bid = [MagicMock(price="100.0", qty="1.0")]
    mock_msg.data.ask = [MagicMock(price="101.0", qty="1.0")]
    mock_msg.ts = 1234567890

    mock_connection.__aenter__.return_value = mock_stream
    mock_connection.__aexit__.return_value = None

    mock_stream.__aiter__.return_value = [mock_msg]

    mock_client.subscribe_to_orderbooks.return_value = mock_connection

    updates = []
    async for update in adapter.subscribe_to_bbo("HYPE-USD"):
        updates.append(update)

    assert len(updates) == 1
    assert updates[0].pair == "HYPE-USD"
    assert updates[0].best_bid == (100.0, 1.0)
    assert updates[0].best_ask == (101.0, 1.0)
    mock_client.subscribe_to_orderbooks.assert_called_with(
        market_name="HYPE-USD", depth=1
    )


@pytest.mark.asyncio
async def test_subscribe_to_bbo_connection_error():
    mock_client = MagicMock()
    adapter = StreamAdapter(api_url="http://test.url")
    adapter.client = mock_client

    mock_client.subscribe_to_orderbooks.side_effect = Exception("Connection failed")

    with pytest.raises(StreamConnectionError):
        async for _ in adapter.subscribe_to_bbo("HYPE-USD"):
            pass


@pytest.mark.asyncio
async def test_subscribe_to_bbo_parsing_error():
    mock_client = MagicMock()
    adapter = StreamAdapter(api_url="http://test.url")
    adapter.client = mock_client

    mock_connection = MagicMock()
    mock_stream = AsyncMock()

    mock_msg = MagicMock()
    mock_msg.data.bid = [MagicMock(price="invalid", qty="1.0")]
    mock_msg.data.ask = [MagicMock(price="101.0", qty="1.0")]

    mock_connection.__aenter__.return_value = mock_stream
    mock_connection.__aexit__.return_value = None

    mock_stream.__aiter__.return_value = [mock_msg]

    mock_client.subscribe_to_orderbooks.return_value = mock_connection

    updates = []
    async for update in adapter.subscribe_to_bbo("HYPE-USD"):
        updates.append(update)

    assert len(updates) == 0
