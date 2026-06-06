"""Display the top Hacker News story title and score on your board."""

from __future__ import annotations

import logging
from typing import Any, Dict, List
import requests

from src.plugins.base import PluginBase, PluginResult

logger = logging.getLogger(__name__)

API_URL = "https://hacker-news.firebaseio.com/v0"
USER_AGENT = "FiestaBoard Hacker News Plugin (https://github.com/Fiestaboard/fiestaboard-plugin--hacker-news)"


class HackerNewsPlugin(PluginBase):
    """Hacker News plugin for FiestaBoard."""

    @property
    def plugin_id(self) -> str:
        return "hacker_news"

    def fetch_data(self) -> PluginResult:
        try:
            feed = self.config.get("feed") or "topstories"
            story_index = int(self.config.get("story_index") or 1) - 1

            # Fetch the list of story IDs
            list_response = requests.get(
                f"{API_URL}/{feed}.json",
                headers={"User-Agent": USER_AGENT},
                timeout=10,
            )
            list_response.raise_for_status()
            story_ids = list_response.json()

            if not story_ids or story_index >= len(story_ids):
                return PluginResult(available=False, error="No stories found")

            story_id = story_ids[story_index]

            # Fetch the story
            story_response = requests.get(
                f"{API_URL}/item/{story_id}.json",
                headers={"User-Agent": USER_AGENT},
                timeout=10,
            )
            story_response.raise_for_status()
            story = story_response.json()

            title = str(story.get("title", ""))
            score = int(story.get("score", 0))
            comments = int(story.get("descendants", 0))
            author = str(story.get("by", "unknown"))

            return PluginResult(
                available=True,
                data={
                    "title": title,
                    "score": score,
                    "comments": comments,
                    "author": author,
                },
            )
        except Exception as e:
            logger.exception("Error fetching Hacker News story")
            return PluginResult(available=False, error=str(e))

    def validate_config(self, config: Dict[str, Any]) -> List[str]:
        return []

    def cleanup(self) -> None:
        pass
