import io

from clvm_rs import Program

from chia_base.bls12_381.bls_signature import BLSSignature
from chia_base.core import Coin, CoinSpend, SpendBundle
from chia_base.util.std_hash import std_hash


def bytes_for_class_streamable(s) -> bytes:
    f = io.BytesIO()
    s._class_stream(s, f)
    return f.getvalue()


def test_simple():
    def check_rt(obj, hexpected):
        try:
            b = bytes_for_class_streamable(obj)
        except Exception:
            b = bytes(obj)
        assert b.hex() == hexpected
        new_obj = obj.__class__.parse(io.BytesIO(b))
        assert obj == new_obj

    parent_coin_id = std_hash(b"1")
    puzzle = Program.fromhex("80")
    puzzle_hash = puzzle.tree_hash()

    amount = 10000
    coin = Coin(parent_coin_id, puzzle_hash, amount)
    hexpected = f"{parent_coin_id.hex()}{puzzle_hash.hex()}{amount:016x}"
    check_rt(coin, hexpected)

    assert coin.name() == std_hash(
        parent_coin_id, puzzle_hash, Program.int_to_bytes(amount)
    )
    assert (
        coin.name().hex()
        == "bdd96a13c474043e413a8c4dc8204c60f34e89e735c8b28bc4e16f526bcc6ca3"
    )

    solution = Program.to([1, 2, 3, 4])
    coin_spend = CoinSpend(coin, puzzle, solution)
    cs_hexpected = f"{hexpected}{bytes(puzzle).hex()}{bytes(solution).hex()}"
    check_rt(coin_spend, cs_hexpected)

    sig = BLSSignature.generator()
    spend_bundle = SpendBundle([coin_spend], sig)
    sb_hexpected = f"00000001{cs_hexpected}{bytes(sig).hex()}"
    check_rt(spend_bundle, sb_hexpected)
