import pytest
from ratelimit_lite import TokenBucket


class FakeClock:
    def __init__(self) -> None:
        self.t = 0.0

    def __call__(self) -> float:
        return self.t


def test_allows_up_to_capacity_then_blocks():
    b = TokenBucket(3, 1, clock=FakeClock())
    assert [b.allow() for _ in range(4)] == [True, True, True, False]


def test_refills_over_time():
    clock = FakeClock()
    b = TokenBucket(2, 1, clock=clock)
    b.allow()
    b.allow()
    assert not b.allow()
    clock.t += 1
    assert b.allow()


def test_refill_capped_at_capacity():
    clock = FakeClock()
    b = TokenBucket(2, 10, clock=clock)
    clock.t += 100
    assert b.allow() and b.allow() and not b.allow()


def test_cost_greater_than_one():
    b = TokenBucket(5, 1, clock=FakeClock())
    assert b.allow(cost=5)
    assert not b.allow(cost=1)


@pytest.mark.parametrize("cap,rate", [(0, 1), (1, 0), (-1, 1)])
def test_invalid_config_rejected(cap, rate):
    with pytest.raises(ValueError):
        TokenBucket(cap, rate)


def test_invalid_cost_rejected():
    with pytest.raises(ValueError):
        TokenBucket(1, 1).allow(cost=0)
