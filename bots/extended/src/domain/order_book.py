from dataclasses import dataclass


@dataclass(frozen=True)
class OrderBookUpdate:
    pair: str
    bids: list[list[float]]
    asks: list[list[float]]
    timestamp: int | None = None

    @property
    def best_bid(self) -> tuple[float, float] | None:
        return (self.bids[0][0], self.bids[0][1]) if self.bids else None

    @property
    def best_ask(self) -> tuple[float, float] | None:
        return (self.asks[0][0], self.asks[0][1]) if self.asks else None
