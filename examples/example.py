#!/usr/bin/env python
"""Example script for tcod.clock."""

from __future__ import annotations

import time

import tcod.context
import tcod.event
from tcod.clock import Clock

WIDTH, HEIGHT = 720, 480


def main() -> None:
    """Demonstrate the synchronization of the Clock class."""
    # vsync is False in this example, but you'll want it to be True unless you
    # need to benchmark or set framerates above 60 FPS.
    with tcod.context.new(width=WIDTH, height=HEIGHT, vsync=False) as context:
        line_x = 0  # Highlight a line, helpful to measure frames visually.
        clock = Clock()
        delta_time = 0.0  # The time passed between frames.
        desired_fps = 50
        begin_time = time.perf_counter()
        while True:
            console = context.new_console(order="F")
            console.rgb["bg"][line_x % console.width, :] = (255, 0, 0)
            console.print(
                1,
                1,
                f"Current time:{(time.perf_counter()-begin_time) * 1000:8.2f}ms"
                f"\nDelta time:{delta_time * 1000:8.2f}ms"
                f"\nDesired FPS:{desired_fps:3d} (use scroll wheel to adjust)"
                f"\n  last:{clock.last_fps:.2f} fps"
                f"\n  mean:{clock.mean_fps:.2f} fps"
                f"\nmedian:{clock.median_fps:.2f} fps"
                f"\n   min:{clock.min_fps:.2f} fps"
                f"\n   max:{clock.max_fps:.2f} fps",
            )
            context.present(console, integer_scaling=True)
            delta_time = clock.sync(1 / desired_fps)
            line_x += 1

            # Handle events.
            for event in tcod.event.get():
                context.convert_event(event)  # Set tile coordinates for event.
                if isinstance(event, tcod.event.Quit):
                    raise SystemExit
                if isinstance(event, tcod.event.MouseWheel):
                    desired_fps = max(1, desired_fps + event.y)


if __name__ == "__main__":
    main()
