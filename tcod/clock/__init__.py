"""Track and limit framerate of a program."""
from __future__ import annotations

import statistics
import time
from collections import deque
from typing import Deque, Optional

__version__ = "1.0.0"


class Clock:
    """Measure framerate performance and sync to a given framerate.

    Everything important is handled by :any:`Clock.sync`.
    You can use the fps properties to track the performance of an application.

    Time is sampled with :any:`time.perf_counter`.
    """

    max_samples = 64
    """Number of framerate samples to log.  This attribute be set in the class or instance."""

    def __init__(self) -> None:
        self.last_time = time.perf_counter()
        "Last time this was synced."
        self.time_samples: Deque[float] = deque()
        "Delta time samples."
        self.__drift_time = 0.0
        "Tracks how much the last frame was overshot."

    def sync(self, desired_framerate: Optional[float] = None) -> float:
        """Sync to a given framerate and return the delta time.

        Args:
            desired_framerate: The desired framerate in seconds.
                If None is given then this function will track the time and framerate without ever waiting.
                Must be above zero when not None.

        Returns:
            The delta time since the last call to sync, in seconds.
        """
        if desired_framerate is not None:
            # Wait until a target time based on the last time and framerate.
            target_time = self.last_time + desired_framerate - self.__drift_time
            # Sleep might take slightly longer than asked.
            sleep_time = max(0, target_time - self.last_time - 0.001)
            if sleep_time:
                time.sleep(sleep_time)
            # Busy wait until the target_time is reached.
            while True:
                drift_time = time.perf_counter() - target_time
                if drift_time >= 0:
                    break
            self.__drift_time = min(drift_time, desired_framerate)

        # Get the delta time.
        current_time = time.perf_counter()
        delta_time = max(0, current_time - self.last_time)
        self.last_time = current_time

        # Record the performance of the current frame.
        if self.max_samples:
            self.time_samples.append(delta_time)
            while len(self.time_samples) > self.max_samples:
                self.time_samples.popleft()

        return delta_time

    @property
    def min_fps(self) -> float:
        """The FPS of the slowest frame."""
        try:
            return 1 / max(self.time_samples)
        except (ValueError, ZeroDivisionError):
            return 0

    @property
    def max_fps(self) -> float:
        """The FPS of the fastest frame."""
        try:
            return 1 / min(self.time_samples)
        except (ValueError, ZeroDivisionError):
            return 0

    @property
    def mean_fps(self) -> float:
        """The FPS of the sampled frames overall."""
        if not self.time_samples:
            return 0
        try:
            return 1 / statistics.fmean(self.time_samples)
        except ZeroDivisionError:
            return 0

    @property
    def median_fps(self) -> float:
        """The FPS of the median frame."""
        if not self.time_samples:
            return 0
        try:
            return 1 / statistics.median(self.time_samples)
        except ZeroDivisionError:
            return 0

    @property
    def last_fps(self) -> float:
        """The FPS of the most recent frame."""
        try:
            return 1 / self.last_frame
        except ZeroDivisionError:
            return 0

    @property
    def last_frame(self) -> float:
        """The length of the most recent frame."""
        if not self.time_samples or self.time_samples[-1] == 0:
            return 0
        return self.time_samples[-1]
