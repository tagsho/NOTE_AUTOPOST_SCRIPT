"""Content strategy helpers for the Note/Twitter automation."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from random import choice
from typing import Dict, Iterable, List, Sequence


@dataclass(frozen=True)
class ContentTheme:
    """Represents a high-level theme for both Note articles and tweets."""

    name: str
    description: str
    talking_points: Sequence[str]


@dataclass(frozen=True)
class ContentPlan:
    """A content plan describing Note and Twitter messaging for a single day."""

    note_title: str
    note_free_section: str
    note_paid_section: str
    price: int
    teaser_tweet: str
    scheduled_tweets: List[str]


THEMES: Dict[str, ContentTheme] = {
    "relationships": ContentTheme(
        name="恋愛・人間関係 × 男性視点 × リアル語り",
        description=(
            "非モテ、職場での立ち位置、彼女との関係、自己肯定感との戦いなどを等身大で語る。"
        ),
        talking_points=[
            "20代後半の飲み会で感じた孤独感",
            "職場で頼られたいけど距離感が難しい件",
            "彼女の何気ない一言で救われた体験",
            "自己肯定感を守るためにやった小さな習慣",
        ],
    ),
    "daily_emotion": ContentTheme(
        name="日常 × 感情 × 生活改善・気づき",
        description="感情の揺らぎから生活改善のヒントを見つける。",
        talking_points=[
            "朝起きられない問題を感情ログで解決した話",
            "休日の虚無感を散歩で打ち消した気づき",
            "仕事帰りのルーティンに温かい飲み物を入れた理由",
            "スマホ時間を減らすための『強制オフライン』術",
        ],
    ),
    "ai_strategy": ContentTheme(
        name="AI活用 × 人生攻略（裏テーマ）",
        description="AIをひっそり味方につけて、日常と人間関係を攻略する裏技。",
        talking_points=[
            "AIで自分の感情パターンを見える化した話",
            "ChatGPTに彼女とのLINEを添削してもらったエピソード",
            "仕事の資料作りをAIで時短したら心の余裕ができた件",
            "AI習慣化コーチを導入して三日坊主を卒業した話",
        ],
    ),
}


TEASER_PATTERNS = [
    "無料部分で語り切れなかった本音は有料パートで。",
    "続きを読んだ人だけが、今日から一歩抜け出せるはず。",
    "有料パートでは、僕が実際にやった手順と失敗談も包み隠さず共有。",
]

PAID_VALUE_PROMISES = [
    "有料パートでは具体的な行動チェックリストと、感情が折れたときのリカバリープランをセットで。",
    "経験則とAI活用の手順を組み合わせて、明日から試せるロードマップにまとめました。",
    "失敗をどうリフレーミングしたか、リアルなやりとりのスクショ例も載せています。",
]


def build_daily_plan(seed: int | None = None) -> ContentPlan:
    """Create a daily content plan respecting the requested themes."""
    if seed is not None:
        import random

        random.seed(seed)

    today = datetime.now().strftime("%Y/%m/%d")
    theme_cycle = [THEMES["relationships"], THEMES["daily_emotion"], THEMES["ai_strategy"]]

    # Select talking points for the four routine tweets.
    routine_tweets: List[str] = []
    for idx in range(4):
        theme = theme_cycle[idx % len(theme_cycle)]
        talking_point = choice(list(theme.talking_points))
        routine_tweets.append(
            f"{talking_point} #日常の気づき #{theme.name.split(' × ')[0]} #{today}"
        )

    # Build Note article sections.
    headline_theme = theme_cycle[0]
    note_title = f"{headline_theme.name}｜{choice(list(headline_theme.talking_points))}"
    free_teaser = (
        f"今日の無料パートでは、{headline_theme.description}"
        "\n\n" + choice(TEASER_PATTERNS)
    )
    paid_teaser = choice(PAID_VALUE_PROMISES)

    price = choice(range(300, 501, 50))

    teaser_tweet = (
        f"{note_title}\n"
        f"無料パート→{headline_theme.talking_points[0]}のリアルな葛藤\n"
        "続きを読むと、AIと習慣を絡めた解決策まで辿り着けます。"
    )

    return ContentPlan(
        note_title=note_title,
        note_free_section=free_teaser,
        note_paid_section=paid_teaser,
        price=price,
        teaser_tweet=teaser_tweet,
        scheduled_tweets=routine_tweets,
    )


__all__ = ["ContentPlan", "ContentTheme", "build_daily_plan"]
