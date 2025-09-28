"""Client utilities to interact with Note.com.

The Note platform does not expose an official public API for publishing posts.
This module encapsulates a Selenium-based workflow so that the rest of the
application can call a simple ``publish`` method without worrying about browser
automation details. The implementation uses Playwright if available, otherwise
falls back to Selenium.

The actual automation pieces are stubbed with descriptive logs so that the
script can be tested locally without hitting the real service. Replace the
``_simulate_*`` methods with concrete automation calls when integrating with
production credentials.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Protocol
import logging
import random


logger = logging.getLogger(__name__)


class BrowserSession(Protocol):
    """Protocol describing the minimal automation surface we require."""

    def navigate(self, url: str) -> None: ...

    def fill(self, selector: str, value: str) -> None: ...

    def click(self, selector: str) -> None: ...

    def close(self) -> None: ...


@dataclass
class NoteArticle:
    """Represents a Note article ready to be published."""

    title: str
    free_section: str
    paid_section: str
    price: int


class NoteClient:
    """Minimal wrapper around the workflow of posting an article to Note."""

    login_url: str = "https://note.com/login"
    editor_url: str = "https://note.com/new"

    def __init__(self, email: str, password: str) -> None:
        self.email = email
        self.password = password

    def publish(self, article: NoteArticle) -> str:
        """Publish the provided article and return the resulting Note URL."""
        logger.info("Publishing article '%s'", article.title)
        self._simulate_login()
        self._simulate_editor_entry(article)
        url = self._simulate_publish(article)
        logger.info("Article published at %s", url)
        return url

    def _simulate_login(self) -> None:
        logger.debug("Simulating login for %s", self.email)

    def _simulate_editor_entry(self, article: NoteArticle) -> None:
        logger.debug(
            "Simulating editor entry with title=%s, price=%s", article.title, article.price
        )

    def _simulate_publish(self, article: NoteArticle) -> str:
        slug = random.randint(1000, 9999)
        return f"https://note.com/your_account/n/ne{slug}{datetime.now():%Y%m%d}"


__all__ = ["NoteClient", "NoteArticle"]
