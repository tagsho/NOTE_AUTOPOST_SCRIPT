"""Main orchestration for the Note auto posting script."""
from __future__ import annotations

from dataclasses import asdict
from datetime import datetime
from zoneinfo import ZoneInfo
from typing import Dict
import logging

from .config import AppConfig
from .content_plan import build_daily_plan
from .note_client import NoteArticle, NoteClient
from .scheduler import schedule_note_share
from .twitter_client import TwitterClient


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="[%(asctime)s] %(levelname)s:%(name)s:%(message)s")


class AutoPostApp:
    """Bundle together Note publishing and Twitter amplification."""

    def __init__(self, config: AppConfig) -> None:
        self.config = config
        self.note_client = NoteClient(config.note.email, config.note.password)
        self.twitter_client = TwitterClient(
            config.twitter.api_key,
            config.twitter.api_secret,
            config.twitter.access_token,
            config.twitter.access_token_secret,
        )
        self.timezone = ZoneInfo(config.timezone)

    def run_daily_cycle(self) -> Dict[str, str]:
        """Create and publish content following the strategy."""
        plan = build_daily_plan()
        logger.info("Daily plan generated: %s", asdict(plan))

        article = NoteArticle(
            title=plan.note_title,
            free_section=plan.note_free_section,
            paid_section=plan.note_paid_section,
            price=plan.price,
        )
        note_url = self.note_client.publish(article)

        share_time = schedule_note_share(self.timezone)
        share_timestamp = share_time.astimezone(ZoneInfo("UTC")).isoformat()

        share_tweet = (
            f"{plan.teaser_tweet}\n\n"
            f"▼有料（{plan.price}円）はこちら\n{note_url}"
        )
        share_result = self.twitter_client.post(share_tweet)
        logger.info("Note share tweeted at %s", share_time)

        routine_results = []
        routine_urls = []
        for text in plan.scheduled_tweets:
            result = self.twitter_client.post(text)
            routine_results.append(result)
            routine_urls.append(result.url)

        summary = {
            "note_url": note_url,
            "note_share_tweet": share_result.url,
            "share_scheduled_utc": share_timestamp,
            "routine_tweets": ",".join(routine_urls),
        }
        summary["summary_ja"] = self._build_japanese_summary(summary, routine_urls)
        return summary

    @staticmethod
    def _build_japanese_summary(summary: Dict[str, str], routine_urls: list[str]) -> str:
        """Create a Japanese-language digest of the automation results."""
        lines = [
            f"Note記事URL: {summary['note_url']}",
            (
                "NoteシェアツイートURL: "
                f"{summary['note_share_tweet']}（UTC {summary['share_scheduled_utc']}）"
            ),
        ]
        if routine_urls:
            lines.append("定常ツイートURL: " + "、".join(routine_urls))
        else:
            lines.append("定常ツイートURL: なし")
        return "\n".join(lines)


def main() -> None:
    config = AppConfig.from_env()
    app = AutoPostApp(config)
    summary = app.run_daily_cycle()
    logger.info("Automation completed: %s", summary)
    if "summary_ja" in summary:
        logger.info("自動化サマリー（日本語）:\n%s", summary["summary_ja"])


if __name__ == "__main__":
    main()
