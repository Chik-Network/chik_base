from dataclasses import dataclass

from klvm_rs import Program  # type: ignore


from .coin import Coin


@dataclass(frozen=True)
class CoinSpend:
    """
    This represents a coin spend on the chik blockchain.
    """

    coin: Coin
    puzzle_reveal: Program
    solution: Program
