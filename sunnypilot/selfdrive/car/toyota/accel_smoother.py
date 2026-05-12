"""
Copyright (c) 2021-, Haibin Wen, sunnypilot, and a number of other contributors.

This file is part of sunnypilot and is licensed under the MIT License.
See the LICENSE.md file in the root directory for more details.
"""

from openpilot.common.realtime import DT_CTRL


WINDUP_JERK   = 2.0   # m/s^3, release direction
WINDDOWN_JERK = 6.0   # m/s^3, apply direction; preserves AEB ramp
WINDUP_STEP   = WINDUP_JERK   * DT_CTRL
WINDDOWN_STEP = WINDDOWN_JERK * DT_CTRL


class AccelSmoother:
  def __init__(self):
    self.prev: float | None = None

  def update(self, accel: float) -> float:
    if self.prev is None:
      self.prev = accel
      return accel
    d = accel - self.prev
    if d > WINDUP_STEP:
      self.prev += WINDUP_STEP
    elif d < -WINDDOWN_STEP:
      self.prev -= WINDDOWN_STEP
    else:
      self.prev = accel
    return self.prev
