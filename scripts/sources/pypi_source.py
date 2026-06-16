import logging
from datetime import UTC, datetime
from typing import Any

from scripts.utils.http_client import get_json

logger = logging.getLogger(__name__)

BASE_URL = "https://pypistats.org/api/packages"


async def fetch_pypi_metrics(package: str, previous: dict | None = None) -> dict[str, Any] | None:
    fetched_at = datetime.now(UTC).isoformat()

    data = await get_json(f"{BASE_URL}/{package}/recent")
    if data is None:
        return None

    recent = data.get("data", {})
    downloads_last_month = recent.get("last_month", 0)
    downloads_last_week = recent.get("last_week", 0)

    delta_pct = None
    if previous and previous.get("downloads_last_week"):
        prev = previous["downloads_last_week"]
        if prev > 0:
            delta_pct = round((downloads_last_week - prev) / prev * 100, 2)

    return {
        "downloads_last_month": downloads_last_month,
        "downloads_last_week": downloads_last_week,
        "downloads_delta_pct": delta_pct,
        "fetched_at": fetched_at,
    }
