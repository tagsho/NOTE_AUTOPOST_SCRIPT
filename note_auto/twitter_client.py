"""Thin Twitter client wrapper used by the automation script."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Optional
import logging


logger = logging.getLogger(__name__)


@dataclass
class TweetResult:
    tweet_id: str
    url: str


class TwitterClient:
    """Placeholder implementation around the Twitter/X posting API."""

    def __init__(self, api_key: str, api_secret: str, access_token: str, access_token_secret: str) -> None:
        self.api_key = api_key
        self.api_secret = api_secret
        self.access_token = access_token
        self.access_token_secret = access_token_secret

    def post(self, text: str, in_reply_to: Optional[str] = None) -> TweetResult:
        """Post a new tweet.

        In this reference implementation we log to stdout. Replace the body with
        calls to the Twitter API (via Tweepy or the official SDK) when deploying.
        """
        logger.info("Posting tweet: %s", text)
        if in_reply_to:
            logger.debug("Tweet is in reply to %s", in_reply_to)
        fake_id = hex(abs(hash(text)) % (10**12))[2:]
        return TweetResult(tweet_id=fake_id, url=f"https://twitter.com/user/status/{fake_id}")


__all__ = ["TwitterClient", "TweetResult"]
