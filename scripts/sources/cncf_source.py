import logging
from datetime import UTC, datetime
from typing import Any

from scripts.utils.http_client import get_json

logger = logging.getLogger(__name__)

LANDSCAPE_URL = "https://landscape.cncf.io/data/exports/landscape.json"

_cache: dict | None = None


async def _load_landscape() -> dict | None:
    global _cache
    if _cache is None:
        _cache = await get_json(LANDSCAPE_URL)
    return _cache


async def fetch_cncf_metrics(project_name: str) -> dict[str, Any] | None:
    fetched_at = datetime.now(UTC).isoformat()
    landscape = await _load_landscape()
    if landscape is None:
        return None

    name_lower = project_name.lower()
    for category in landscape.get("landscape", []):
        for subcategory in category.get("subcategories", []):
            for item in subcategory.get("items", []):
                if item.get("name", "").lower() == name_lower:
                    maturity = item.get("project", "")
                    return {
                        "cncf_status": maturity or "listed",
                        "fetched_at": fetched_at,
                    }

    logger.warning("CNCF project not found: %s", project_name)
    return {"cncf_status": "not_found", "fetched_at": fetched_at}
