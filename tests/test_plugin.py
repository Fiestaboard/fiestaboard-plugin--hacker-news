"""Tests for the hacker_news plugin."""

from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import patch, Mock

import pytest

from plugins.hacker_news import HackerNewsPlugin
from src.plugins.base import PluginResult

MANIFEST = json.loads("""
{
    "id": "hacker_news",
    "name": "Hacker News",
    "version": "0.1.0",
    "settings_schema": {
        "type": "object",
        "properties": {
            "enabled": {
                "type": "boolean",
                "title": "Enabled",
                "default": false
            },
            "story_index": {
                "type": "integer",
                "title": "Story Position",
                "description": "Which story to display (1 = top story, 2 = second, etc.).",
                "default": 1,
                "minimum": 1,
                "maximum": 30
            },
            "feed": {
                "type": "string",
                "title": "Feed",
                "description": "Which HN feed to display.",
                "enum": [
                    "topstories",
                    "beststories",
                    "newstories",
                    "askstories",
                    "showstories"
                ],
                "default": "topstories"
            },
            "refresh_seconds": {
                "type": "integer",
                "title": "Refresh Interval (seconds)",
                "description": "How often to fetch the top story.",
                "default": 300,
                "minimum": 60
            }
        },
        "required": []
    }
}
""")

SAMPLE_RESPONSE = json.loads("""
{
    "id": 39999999,
    "title": "Show HN: My new project",
    "url": "https://example.com",
    "score": 1234,
    "descendants": 342,
    "by": "pg",
    "type": "story",
    "time": 1746000000
}
""")


@pytest.fixture
def plugin():
    return HackerNewsPlugin(MANIFEST)


@pytest.fixture
def configured_plugin():
    p = HackerNewsPlugin(MANIFEST)
    p.config = json.loads("""
{
    "story_index": 1,
    "feed": "topstories"
}
""")
    return p


class TestHackerNewsPlugin:

    def test_plugin_id(self, plugin):
        assert plugin.plugin_id == "hacker_news"

    def test_manifest_valid(self):
        manifest_path = Path(__file__).parent.parent / "manifest.json"
        with open(manifest_path) as f:
            m = json.load(f)
        for field in ("id", "name", "version"):
            assert field in m

    def test_manifest_includes_demo_page(self):
        manifest_path = Path(__file__).parent.parent / "manifest.json"
        with open(manifest_path) as f:
            m = json.load(f)
        assert "demo" in m
        assert isinstance(m["demo"], dict)
        assert m["demo"].get("name") == "Hacker News Demo"
        assert m["demo"].get("device_type") == "flagship"
        assert isinstance(m["demo"].get("template"), list)
        assert len(m["demo"].get("line_metadata", [])) == len(m["demo"].get("template", []))

    @patch("plugins.hacker_news.requests.get")
    def test_fetch_data_success(self, mock_get, configured_plugin):
        ids_response = Mock()
        ids_response.json.return_value = [39999999, 12345678, 9999999]
        ids_response.raise_for_status = Mock()
        story_response = Mock()
        story_response.json.return_value = SAMPLE_RESPONSE
        story_response.raise_for_status = Mock()
        mock_get.side_effect = [ids_response, story_response]

        result = configured_plugin.fetch_data()

        assert result.available is True
        assert result.error is None
        assert result.data is not None
        assert "title" in result.data, "missing variable: title"
        assert "score" in result.data, "missing variable: score"
        assert "comments" in result.data, "missing variable: comments"
        assert "author" in result.data, "missing variable: author"

    @patch("plugins.hacker_news.requests.get")
    def test_fetch_data_network_error(self, mock_get, configured_plugin):
        import requests as req_mod
        mock_get.side_effect = req_mod.exceptions.ConnectionError("network down")

        result = configured_plugin.fetch_data()

        assert result.available is False
        assert result.error is not None

    @patch("plugins.hacker_news.requests.get")
    def test_fetch_data_bad_json(self, mock_get, configured_plugin):
        mock_response = Mock()
        mock_response.json.side_effect = ValueError("bad json")
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        result = configured_plugin.fetch_data()

        assert result.available is False

