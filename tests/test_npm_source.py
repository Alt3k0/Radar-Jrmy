import json
from pathlib import Path

import pytest
from pytest_httpx import HTTPXMock

from scripts.sources.npm_source import fetch_npm_metrics

FIXTURES = Path(__file__).parent / "fixtures"


@pytest.mark.asyncio
async def test_fetch_npm_metrics_nominal(httpx_mock: HTTPXMock):
    npm_data = json.loads((FIXTURES / "npm_response.json").read_text())
    httpx_mock.add_response(
        url="https://api.npmjs.org/downloads/point/last-week/typescript",
        json=npm_data,
    )
    result = await fetch_npm_metrics("typescript")
    assert result is not None
    assert result["downloads_weekly"] == 48000000
    assert result["downloads_delta_pct"] is None
    assert "fetched_at" in result


@pytest.mark.asyncio
async def test_fetch_npm_metrics_with_previous(httpx_mock: HTTPXMock):
    npm_data = json.loads((FIXTURES / "npm_response.json").read_text())
    httpx_mock.add_response(
        url="https://api.npmjs.org/downloads/point/last-week/typescript",
        json=npm_data,
    )
    previous = {"downloads_weekly": 46000000}
    result = await fetch_npm_metrics("typescript", previous)
    assert result is not None
    assert result["downloads_delta_pct"] == pytest.approx(4.35, abs=0.01)


@pytest.mark.asyncio
async def test_fetch_npm_metrics_scoped_package(httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        url="https://api.npmjs.org/downloads/point/last-week/%40angular%2Fcore",
        json={"downloads": 5000000, "package": "@angular/core"},
    )
    result = await fetch_npm_metrics("@angular/core")
    assert result is not None
    assert result["downloads_weekly"] == 5000000


@pytest.mark.asyncio
async def test_fetch_npm_metrics_not_found(httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        url="https://api.npmjs.org/downloads/point/last-week/nonexistent-package-xyz",
        status_code=404,
    )
    result = await fetch_npm_metrics("nonexistent-package-xyz")
    assert result is None


@pytest.mark.asyncio
async def test_fetch_npm_metrics_server_error(httpx_mock: HTTPXMock):
    for _ in range(3):
        httpx_mock.add_response(
            url="https://api.npmjs.org/downloads/point/last-week/typescript",
            status_code=500,
        )
    result = await fetch_npm_metrics("typescript")
    assert result is None
