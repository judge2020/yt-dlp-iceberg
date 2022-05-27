# noinspection PyMethodMayBeStatic
from dataclasses import dataclass
from typing import List


@dataclass
class Preset:
    interval_minutes: int = None
    options: List[str] = None
    post_command: str = None
