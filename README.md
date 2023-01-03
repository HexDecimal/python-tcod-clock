# About

[![PyPI](https://img.shields.io/pypi/v/tcod-clock)](https://pypi.org/project/tcod-clock/)
[![PyPI - License](https://img.shields.io/pypi/l/tcod-clock)](https://github.com/HexDecimal/python-tcod-clock/blob/main/LICENSE)
[![Documentation Status](https://readthedocs.org/projects/python-tcod-clock/badge/?version=latest)](https://python-tcod-clock.readthedocs.io)
[![codecov](https://codecov.io/gh/HexDecimal/python-tcod-clock/branch/main/graph/badge.svg?token=UP161WEo0s)](https://codecov.io/gh/HexDecimal/python-tcod-clock)

Libtcod used to include a global framerate limiter which was later deprecated as libtcod was refactored.
This module was crated as a replacement for that feature.

```py
import time

from tcod.clock import Clock


FPS = 30

end_time = time.time() + 3  # Loop for 3 seconds.

clock = Clock()
while time.time() < end_time:
    clock.sync(1 / FPS)  # This loop will run at 30 FPS until interrupted.

# Timing information can be checked.  Check the docs for more info.
print(f"{clock.last_fps=}")
print(f"{clock.min_fps=}")
print(f"{clock.max_fps=}")
print(f"{clock.mean_fps=}")
print(f"{clock.median_fps=}")
```
