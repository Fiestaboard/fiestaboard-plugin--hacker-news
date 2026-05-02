# Hacker News Setup Guide

Display the top Hacker News story title and score on your board.

## Overview

The Hacker News plugin fetches top stories from the official HN Firebase API. It shows the title, score, and comment count of the highest-ranked story. No API key required.

- API reference: https://github.com/HackerNews/API

### Prerequisites

No API key or account required.

## Quick Setup

1. **Enable** — Go to **Integrations** in your FiestaBoard settings and enable **Hacker News**.
2. **Configure** — Fill in the plugin settings (see Configuration Reference below).
3. **Template** — Add a page using the `hacker_news` plugin variables:
   ```
   {{{ hacker_news.status }}}
   ```
4. **View** — Navigate to your board page to see the live display.

## Template Variables

| Variable | Description | Example |
|---|---|---|
| `hacker_news.title` | Story title (truncated to fit board) | `Ask HN: What are you` |
| `hacker_news.score` | Story score (upvotes) | `1234` |
| `hacker_news.comments` | Number of comments | `342` |
| `hacker_news.author` | Story author username | `pg` |

## Configuration Reference

| Setting | Name | Description | Default |
|---|---|---|---|
| `enabled` | Enabled |  | `False` |
| `story_index` | Story Position | Which story to display (1 = top story, 2 = second, etc.). | `1` |
| `feed` | Feed | Which HN feed to display. | `topstories` |
| `refresh_seconds` | Refresh Interval (seconds) | How often to fetch the top story. | `300` |

## Troubleshooting

- **Stale story** — the plugin shows a cached story; reduce the refresh interval.
- **Network error** — verify connectivity to `hacker-news.firebaseio.com`.

