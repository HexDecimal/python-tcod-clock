"""Tests for tcod.clock."""

from __future__ import annotations

import tcod.clock

# ruff: noqa: D103


def test_clock() -> None:
    clock = tcod.clock.Clock()
    assert clock.last_fps == 0
    assert clock.max_fps == 0
    assert clock.min_fps == 0
    assert clock.mean_fps == 0
    assert clock.median_fps == 0
    for _ in range(100):
        clock.sync()
        clock.last_fps  # noqa: B018
        clock.max_fps  # noqa: B018
        clock.min_fps  # noqa: B018
        clock.mean_fps  # noqa: B018
        clock.median_fps  # noqa: B018
    clock.max_samples = 0
    for _ in range(100):
        clock.sync()
        clock.last_fps  # noqa: B018
        clock.max_fps  # noqa: B018
        clock.min_fps  # noqa: B018
        clock.mean_fps  # noqa: B018
        clock.median_fps  # noqa: B018

    clock.sync(0.001)
    clock.sync(0.1)
