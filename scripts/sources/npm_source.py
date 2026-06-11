import logging
from datetime import datetime, timezone
from typing import Any
from urllib.parse import quote

from scripts.utils.http_client import get_json

logger = logging.getLogger(__name__)

BASE_URL = "https://api.npmjs.org/downloads/point"


async def fetch_npm_metrics(package: str, previous: dict | None = None) -> dict[str, Any] | None:
    encoded = quote(package, safe="")
    fetched_at = datetime.now(timezone.utc).isoformat()

    current = await get_json(f"{BASE_URL}/last-week/{encoded}")
    if current is None:
        return None

    downloads_weekly = current.get("downloads", 0)

    delta_pct = None
    if previous and previous.get("downloads_weekly"):
        prev_downloads = previous["downloads_weekly"]
        if prev_downloads > 0:
            delta_pct = round((downloads_weekly - prev_downloads) / prev_downloads * 100, 2)

    return {
        "downloads_weekly": downloads_weekly,
        "downloads_delta_pct": delta_pct,
        "fetched_at": fetched_at,
    }
