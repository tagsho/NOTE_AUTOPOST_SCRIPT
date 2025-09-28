"""Configuration utilities for the Note auto posting script."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import time
from typing import Iterable, List, Sequence
import os


@dataclass(frozen=True)
class TwitterCredentials:
    """Holds the credential values necessary to interact with the Twitter API."""

    api_key: str
    api_secret: str
    access_token: str
    access_token_secret: str

    @classmethod
    def from_env(cls, prefix: str = "TWITTER_") -> "TwitterCredentials":
        """Create credentials from environment variables.

        Parameters
        ----------
        prefix:
            Optional prefix for the environment variable names. The default
            maps to the canonical Twitter environment variables, e.g.
            ``TWITTER_API_KEY``.
        """

        def required(name: str) -> str:
            value = os.getenv(name)
            if not value:
                raise RuntimeError(f"Missing required environment variable: {name}")
            return value

        return cls(
            api_key=required(f"{prefix}API_KEY"),
            api_secret=required(f"{prefix}API_SECRET"),
            access_token=required(f"{prefix}ACCESS_TOKEN"),
            access_token_secret=required(f"{prefix}ACCESS_TOKEN_SECRET"),
        )


@dataclass(frozen=True)
class NoteCredentials:
    """Credential bundle for the Note.com automation."""

    email: str
    password: str
    price_range: Sequence[int]

    @classmethod
    def from_env(cls, prefix: str = "NOTE_") -> "NoteCredentials":
        email = os.getenv(f"{prefix}EMAIL")
        password = os.getenv(f"{prefix}PASSWORD")
        if not email or not password:
            raise RuntimeError("NOTE_EMAIL and NOTE_PASSWORD must be set in the environment")
        price_min = int(os.getenv(f"{prefix}PRICE_MIN", "300"))
        price_max = int(os.getenv(f"{prefix}PRICE_MAX", "500"))
        if price_min > price_max:
            raise ValueError("NOTE_PRICE_MIN must be less than or equal to NOTE_PRICE_MAX")
        return cls(email=email, password=password, price_range=(price_min, price_max))


@dataclass(frozen=True)
class PostingWindow:
    """Represents a posting window for routine tweets."""

    times: List[time]

    @classmethod
    def from_strings(cls, values: Iterable[str]) -> "PostingWindow":
        parsed: List[time] = []
        for raw in values:
            hours, minutes = raw.split(":")
            parsed.append(time(int(hours), int(minutes)))
        return cls(parsed)


@dataclass(frozen=True)
class AppConfig:
    """Aggregates configuration for the auto posting application."""

    twitter: TwitterCredentials
    note: NoteCredentials
    twitter_posting_window: PostingWindow
    timezone: str = "Asia/Tokyo"

    @classmethod
    def from_env(cls) -> "AppConfig":
        twitter = TwitterCredentials.from_env()
        note = NoteCredentials.from_env()
        windows = os.getenv("TWITTER_POST_TIMES", "08:30,12:30,18:30,22:30")
        posting_window = PostingWindow.from_strings(time_str.strip() for time_str in windows.split(","))
        timezone = os.getenv("APP_TIMEZONE", "Asia/Tokyo")
        return cls(twitter=twitter, note=note, twitter_posting_window=posting_window, timezone=timezone)
