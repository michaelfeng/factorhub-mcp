#!/usr/bin/env python3
"""FactorHub MCP Server — China A-share market data for AI agents.

Connects to the FactorHub public API (https://factorhub.cn/api/v1)
to provide factor data, market data, and backtest capabilities.

Environment variables:
    FACTORHUB_API_KEY  — Your API key (required). Get one at https://factorhub.cn/api-keys
    FACTORHUB_BASE_URL — API base URL (optional, default: https://factorhub.cn/api/v1)
"""

import json
import os
import sys

import httpx
from fastmcp import FastMCP

from .client import FactorHubClient


mcp = FastMCP(
    "FactorHub",
    instructions="China A-share market data for AI agents — factor scores, market quotes, valuations, and strategy backtesting",
)

_client: FactorHubClient | None = None


def _get_client() -> FactorHubClient:
    global _client
    if _client is None:
        api_key = os.environ.get("FACTORHUB_API_KEY", "")
        base_url = os.environ.get("FACTORHUB_BASE_URL", "https://factorhub.cn/api/v1")
        if not api_key:
            raise RuntimeError(
                "FACTORHUB_API_KEY environment variable is required.\n"
                "Get your free API key at https://factorhub.cn/api-keys"
            )
        _client = FactorHubClient(api_key=api_key, base_url=base_url)
    return _client


def _format(data) -> str:
    if isinstance(data, dict):
        return json.dumps(data, ensure_ascii=False, indent=2)
    return str(data)


def _handle_error(e: Exception) -> str:
    if isinstance(e, httpx.HTTPStatusError):
        status = e.response.status_code
        if status == 429:
            return "API 调用次数已达上限。请升级订阅：https://factorhub.cn/pricing"
        elif status == 401:
            return "API Key 无效或已过期。"
        elif status == 404:
            return "未找到请求的资源，请检查参数。"
        return f"API 请求失败 (HTTP {status})"
    return f"执行失败: {e}"


# ── Tools ────────────────────────────────────────────────────

@mcp.tool()
async def list_factors(
    category: str = "",
    search: str = "",
    page: int = 1,
    page_size: int = 20,
) -> str:
    """获取因子列表。支持按分类和关键词搜索。返回因子代码、名称、分类、年化收益、夏普比率等。"""
    try:
        result = await _get_client().list_factors(category, search, page, page_size)
        return _format(result)
    except Exception as e:
        return _handle_error(e)


@mcp.tool()
async def get_factor_scores(
    code: str,
    start_date: str = "",
    end_date: str = "",
) -> str:
    """获取单个因子的详细评分指标：年化收益、夏普比率、最大回撤、波动率、Alpha、Beta、IC均值等。"""
    try:
        result = await _get_client().factor_scores(code, start_date, end_date)
        return _format(result)
    except Exception as e:
        return _handle_error(e)


@mcp.tool()
async def get_factor_nav(
    code: str,
    start_date: str = "",
    end_date: str = "",
) -> str:
    """获取因子净值曲线数据，用于分析因子历史表现趋势。"""
    try:
        result = await _get_client().factor_nav(code, start_date, end_date)
        return _format(result)
    except Exception as e:
        return _handle_error(e)


@mcp.tool()
async def get_market_daily(
    ts_code: str,
    start_date: str = "",
    end_date: str = "",
) -> str:
    """获取个股日线行情数据（OHLCV + 涨跌幅）。ts_code 如 000001.SZ、600519.SH。"""
    try:
        result = await _get_client().market_daily(ts_code, start_date, end_date)
        return _format(result)
    except Exception as e:
        return _handle_error(e)


@mcp.tool()
async def get_index_daily(
    ts_code: str = "",
    start_date: str = "",
    end_date: str = "",
) -> str:
    """获取指数日线行情。常用：000001.SH(上证)、399001.SZ(深证)、000300.SH(沪深300)、000905.SH(中证500)。"""
    try:
        result = await _get_client().index_daily(ts_code, start_date, end_date)
        return _format(result)
    except Exception as e:
        return _handle_error(e)


@mcp.tool()
async def get_valuation(
    ts_code: str = "",
    trade_date: str = "",
) -> str:
    """获取股票估值指标：PE、PB、PS、股息率、总市值、流通市值、换手率等。"""
    try:
        result = await _get_client().valuation(ts_code, trade_date)
        return _format(result)
    except Exception as e:
        return _handle_error(e)


@mcp.tool()
async def get_stock_info(ts_code: str) -> str:
    """获取单只股票基本信息：名称、行业、上市日期、市场板块等。"""
    try:
        result = await _get_client().stock_info(ts_code)
        return _format(result)
    except Exception as e:
        return _handle_error(e)


@mcp.tool()
async def get_stock_list(
    exchange: str = "",
    industry: str = "",
    page: int = 1,
    page_size: int = 50,
) -> str:
    """按条件筛选股票列表。可按交易所(SSE/SZSE)、行业筛选。"""
    try:
        result = await _get_client().stock_list(exchange, industry, page, page_size)
        return _format(result)
    except Exception as e:
        return _handle_error(e)


@mcp.tool()
async def get_trade_dates(
    start_date: str = "",
    end_date: str = "",
) -> str:
    """获取交易日历，查询指定时间段内的交易日列表。"""
    try:
        result = await _get_client().trade_dates(start_date, end_date)
        return _format(result)
    except Exception as e:
        return _handle_error(e)


@mcp.tool()
async def run_backtest(
    strategy_type: str = "",
    strategy_params: dict | None = None,
    universe: str = "hs300",
    start: str = "20220101",
    end: str = "20241231",
    initial_capital: float = 1000000,
) -> str:
    """执行量化策略回测。内置策略：limit_up_first_board(涨停首板)、low_valuation(低估值)、momentum(动量)、mean_reversion(均值回归)。返回年化收益、夏普比率、最大回撤等。"""
    try:
        params = {
            "strategy_type": strategy_type,
            "universe": universe,
            "start": start,
            "end": end,
            "initial_capital": initial_capital,
        }
        if strategy_params:
            params["strategy_params"] = strategy_params
        result = await _get_client().run_backtest(params)
        return _format(result)
    except Exception as e:
        return _handle_error(e)


# ── Entry point ──────────────────────────────────────────────

def main():
    """Entry point. Supports stdio (default), --sse, and --http for remote modes."""
    port = int(os.environ.get("MCP_PORT", "8099"))
    if "--sse" in sys.argv or "--http" in sys.argv:
        mcp.run(transport="streamable-http", host="0.0.0.0", port=port)
    else:
        mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
