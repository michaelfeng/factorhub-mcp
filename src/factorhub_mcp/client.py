"""FactorHub API client — calls the public REST API at factorhub.cn.

All data access goes through the public API with API key authentication.
No direct database access or internal business logic is included.
"""

import httpx
from typing import Any


DEFAULT_BASE_URL = "https://factorhub.cn/api/v1"
DEFAULT_TIMEOUT = 30.0
BACKTEST_TIMEOUT = 300.0


class FactorHubClient:
    """HTTP client for the FactorHub public API."""

    def __init__(self, api_key: str, base_url: str = DEFAULT_BASE_URL):
        if not api_key:
            raise ValueError(
                "API key is required. Get one at https://factorhub.cn/api-keys"
            )
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")

    def _headers(self) -> dict:
        return {"X-API-Key": self.api_key}

    async def _get(self, path: str, params: dict | None = None, timeout: float = DEFAULT_TIMEOUT) -> Any:
        filtered = {k: v for k, v in (params or {}).items() if v is not None and v != ""}
        async with httpx.AsyncClient(timeout=timeout) as client:
            resp = await client.get(
                f"{self.base_url}{path}",
                params=filtered,
                headers=self._headers(),
            )
            resp.raise_for_status()
            return resp.json()

    async def _post(self, path: str, json_data: dict, timeout: float = BACKTEST_TIMEOUT) -> Any:
        async with httpx.AsyncClient(timeout=timeout) as client:
            resp = await client.post(
                f"{self.base_url}{path}",
                json=json_data,
                headers=self._headers(),
            )
            resp.raise_for_status()
            return resp.json()

    # ── Factor data ──────────────────────────────────────────

    async def list_factors(
        self, category: str = "", search: str = "", page: int = 1, page_size: int = 20
    ) -> dict:
        return await self._get("/factors", {
            "category": category, "search": search,
            "page": page, "page_size": page_size,
        })

    async def factor_scores(self, code: str, start_date: str = "", end_date: str = "") -> dict:
        return await self._get(f"/factors/{code}/scores", {
            "start_date": start_date, "end_date": end_date,
        })

    async def factor_nav(self, code: str, start_date: str = "", end_date: str = "") -> dict:
        return await self._get(f"/factors/{code}/nav", {
            "start_date": start_date, "end_date": end_date,
        })

    # ── Market data ──────────────────────────────────────────

    async def market_daily(self, ts_code: str, start_date: str = "", end_date: str = "") -> dict:
        return await self._get("/market/daily", {
            "ts_code": ts_code, "start_date": start_date, "end_date": end_date,
        })

    async def index_daily(self, ts_code: str = "", start_date: str = "", end_date: str = "") -> dict:
        return await self._get("/market/index", {
            "ts_code": ts_code, "start_date": start_date, "end_date": end_date,
        })

    async def valuation(self, ts_code: str = "", trade_date: str = "") -> dict:
        return await self._get("/market/valuation", {
            "ts_code": ts_code, "trade_date": trade_date,
        })

    # ── Stock data ───────────────────────────────────────────

    async def stock_info(self, ts_code: str) -> dict:
        return await self._get("/stock/info", {"ts_code": ts_code})

    async def stock_list(
        self, exchange: str = "", industry: str = "", page: int = 1, page_size: int = 50
    ) -> dict:
        return await self._get("/stock/list", {
            "exchange": exchange, "industry": industry,
            "page": page, "page_size": page_size,
        })

    # ── Calendar ─────────────────────────────────────────────

    async def trade_dates(self, start_date: str = "", end_date: str = "") -> dict:
        return await self._get("/calendar/trade-dates", {
            "start_date": start_date, "end_date": end_date,
        })

    # ── Backtest ─────────────────────────────────────────────

    async def run_backtest(self, params: dict) -> dict:
        return await self._post("/backtest", params)
