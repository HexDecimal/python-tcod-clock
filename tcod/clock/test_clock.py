from __future__ import annotations

import tcod.clock


def test_clock() -> None:
    clock = tcod.clock.Clock()
    assert clock.last_fps == 0
    assert clock.max_fps == 0
    assert clock.min_fps == 0
    assert clock.mean_fps == 0
    assert clock.median_fps == 0
    for _ in range(100):
        clock.sync()
        clock.last_fps
        clock.max_fps
        clock.min_fps
        clock.mean_fps
        clock.median_fps
    clock.max_samples = 0
    for _ in range(100):
        clock.sync()
        clock.last_fps
        clock.max_fps
        clock.min_fps
        clock.mean_fps
        clock.median_fps

    clock.sync(0.001)
    clock.sync(0.1)
