import json
from pathlib import Path

import pytest
from pytest_httpx import HTTPXMock

from scripts.sources.github_source import fetch_github_metrics

FIXTURES = Path(__file__).parent / "fixtures"


@pytest.mark.asyncio
async def test_fetch_github_metrics_nominal(httpx_mock: HTTPXMock):
    repo_data = json.loads((FIXTURES / "github_response.json").read_text())
    commits_data = json.loads((FIXTURES / "github_commits_response.json").read_text())
    httpx_mock.add_response(url="https://api.github.com/repos/microsoft/TypeScript", json=repo_data)
    httpx_mock.add_response(
        url="https://api.github.com/repos/microsoft/TypeScript/commits?per_page=1",
        json=commits_data,
    )
    result = await fetch_github_metrics("microsoft/TypeScript")
    assert result is not None
    assert result["stars"] == 98500
    assert result["forks"] == 12300
    assert result["open_issues"] == 5200
    assert result["stars_delta_30d"] is None
    assert result["last_commit_days_ago"] is not None
    assert "fetched_at" in result


@pytest.mark.asyncio
async def test_fetch_github_metrics_with_previous(httpx_mock: HTTPXMock):
    repo_data = json.loads((FIXTURES / "github_response.json").read_text())
    commits_data = json.loads((FIXTURES / "github_commits_response.json").read_text())
    httpx_mock.add_response(url="https://api.github.com/repos/microsoft/TypeScript", json=repo_data)
    httpx_mock.add_response(
        url="https://api.github.com/repos/microsoft/TypeScript/commits?per_page=1",
        json=commits_data,
    )
    previous = {"stars": 97500}
    result = await fetch_github_metrics("microsoft/TypeScript", previous)
    assert result is not None
    assert result["stars_delta_30d"] == 1000


@pytest.mark.asyncio
async def test_fetch_github_metrics_rate_limit(httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        url="https://api.github.com/repos/microsoft/TypeScript",
        status_code=429,
        headers={"Retry-After": "1"},
    )
    httpx_mock.add_response(
        url="https://api.github.com/repos/microsoft/TypeScript",
        status_code=429,
        headers={"Retry-After": "1"},
    )
    httpx_mock.add_response(
        url="https://api.github.com/repos/microsoft/TypeScript",
        status_code=429,
        headers={"Retry-After": "1"},
    )
    result = await fetch_github_metrics("microsoft/TypeScript")
    assert result is None


@pytest.mark.asyncio
async def test_fetch_github_metrics_not_found(httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        url="https://api.github.com/repos/nonexistent/repo",
        status_code=404,
    )
    result = await fetch_github_metrics("nonexistent/repo")
    assert result is None


@pytest.mark.asyncio
async def test_fetch_github_metrics_server_error(httpx_mock: HTTPXMock):
    for _ in range(3):
        httpx_mock.add_response(
            url="https://api.github.com/repos/microsoft/TypeScript",
            status_code=500,
        )
    result = await fetch_github_metrics("microsoft/TypeScript")
    assert result is None
