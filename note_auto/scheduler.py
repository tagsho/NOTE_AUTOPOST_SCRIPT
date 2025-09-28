"""Scheduling helpers for Note/Twitter cross-posting."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta, time
from typing import Iterable, List
import logging
import random


logger = logging.getLogger(__name__)


@dataclass
class ScheduledTweet:
    text: str
    scheduled_time: datetime
    is_note_share: bool = False


def schedule_routine_tweets(base_times: Iterable[time], timezone) -> List[ScheduledTweet]:
    """Create scheduled tweet entries for the current day."""
    today = datetime.now(timezone).date()
    return [
        ScheduledTweet(text="", scheduled_time=datetime.combine(today, t, tzinfo=timezone))
        for t in base_times
    ]


def schedule_note_share(timezone, within: timedelta = timedelta(minutes=5)) -> datetime:
    """Return the timestamp used for sharing the Note link on Twitter."""
    now = datetime.now(timezone)
    jitter = random.uniform(0, within.total_seconds())
    scheduled = now + timedelta(seconds=jitter)
    logger.debug("Note share tweet scheduled for %s", scheduled)
    return scheduled


__all__ = ["ScheduledTweet", "schedule_routine_tweets", "schedule_note_share"]
