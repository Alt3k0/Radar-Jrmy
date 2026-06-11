import json
from pathlib import Path

import pytest
from pytest_httpx import HTTPXMock

from scripts.sources.pypi_source import fetch_pypi_metrics

FIXTURES = Path(__file__).parent / "fixtures"


@pytest.mark.asyncio
async def test_fetch_pypi_metrics_nominal(httpx_mock: HTTPXMock):
    pypi_data = json.loads((FIXTURES / "pypi_response.json").read_text())
    httpx_mock.add_response(
        url="https://pypistats.org/api/packages/pip/recent",
        json=pypi_data,
    )
    result = await fetch_pypi_metrics("pip")
    assert result is not None
    assert result["downloads_last_month"] == 45000000
    assert result["downloads_last_week"] == 10500000
    assert result["downloads_delta_pct"] is None
    assert "fetched_at" in result


@pytest.mark.asyncio
async def test_fetch_pypi_metrics_with_previous(httpx_mock: HTTPXMock):
    pypi_data = json.loads((FIXTURES / "pypi_response.json").read_text())
    httpx_mock.add_response(
        url="https://pypistats.org/api/packages/pip/recent",
        json=pypi_data,
    )
    previous = {"downloads_last_week": 10000000}
    result = await fetch_pypi_metrics("pip", previous)
    assert result is not None
    assert result["downloads_delta_pct"] == pytest.approx(5.0, abs=0.01)


@pytest.mark.asyncio
async def test_fetch_pypi_metrics_declining(httpx_mock: HTTPXMock):
    pypi_data = json.loads((FIXTURES / "pypi_response.json").read_text())
    httpx_mock.add_response(
        url="https://pypistats.org/api/packages/pip/recent",
        json=pypi_data,
    )
    previous = {"downloads_last_week": 12000000}
    result = await fetch_pypi_metrics("pip", previous)
    assert result is not None
    assert result["downloads_delta_pct"] < 0


@pytest.mark.asyncio
async def test_fetch_pypi_metrics_not_found(httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        url="https://pypistats.org/api/packages/nonexistent/recent",
        status_code=404,
    )
    result = await fetch_pypi_metrics("nonexistent")
    assert result is None


@pytest.mark.asyncio
async def test_fetch_pypi_metrics_timeout(httpx_mock: HTTPXMock):
    import httpx as httpx_lib
    httpx_mock.add_exception(
        httpx_lib.TimeoutException("timeout"),
        url="https://pypistats.org/api/packages/pip/recent",
    )
    httpx_mock.add_exception(
        httpx_lib.TimeoutException("timeout"),
        url="https://pypistats.org/api/packages/pip/recent",
    )
    httpx_mock.add_exception(
        httpx_lib.TimeoutException("timeout"),
        url="https://pypistats.org/api/packages/pip/recent",
    )
    result = await fetch_pypi_metrics("pip")
    assert result is None
