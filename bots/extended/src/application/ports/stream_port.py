from abc import ABC, abstractmethod
from collections.abc import AsyncIterator

from src.domain.order_book import OrderBookUpdate


class StreamPort(ABC):
    @abstractmethod
    async def subscribe_to_bbo(self, pair: str) -> AsyncIterator[OrderBookUpdate]:
        pass
