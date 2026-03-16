#!/usr/bin/env python3
"""FactorHub MCP Server — China A-share market data for AI agents.

Connects to the FactorHub public API (https://factorhub.cn/api/v1)
to provide factor data, market data, and backtest capabilities.

Environment variables:
    FACTORHUB_API_KEY  — Your API key (required). Get one at https://factorhub.cn/api-keys
    FACTORHUB_BASE_URL — API base URL (optional, default: https://factorhub.cn/api/v1)
"""

import asyncio
import json
import os
import sys
from typing import List

from mcp.server import Server
import mcp.server.stdio
import mcp.types as types

from .client import FactorHubClient


server = Server("factorhub")

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


def _format_result(data) -> str:
    """Format API response as readable text for LLM consumption."""
    if isinstance(data, dict):
        return json.dumps(data, ensure_ascii=False, indent=2)
    return str(data)


# ============================================================
# Tool definitions
# ============================================================

@server.list_tools()
async def handle_list_tools() -> List[types.Tool]:
    return [
        types.Tool(
            name="list_factors",
            description="获取因子列表。支持按分类和关键词搜索。返回因子代码、名称、分类、年化收益、夏普比率等。",
            inputSchema={
                "type": "object",
                "properties": {
                    "category": {"type": "string", "description": "因子分类，如 价值因子、动量因子、质量因子"},
                    "search": {"type": "string", "description": "搜索关键词（因子名称或代码）"},
                    "page": {"type": "integer", "description": "页码，默认1", "default": 1},
                    "page_size": {"type": "integer", "description": "每页数量，默认20", "default": 20},
                },
            },
        ),
        types.Tool(
            name="get_factor_scores",
            description="获取单个因子的详细评分指标：年化收益、夏普比率、最大回撤、波动率、Alpha、Beta、IC均值等。",
            inputSchema={
                "type": "object",
                "properties": {
                    "code": {"type": "string", "description": "因子代码，如 F001"},
                    "start_date": {"type": "string", "description": "开始日期 YYYY-MM-DD"},
                    "end_date": {"type": "string", "description": "结束日期 YYYY-MM-DD"},
                },
                "required": ["code"],
            },
        ),
        types.Tool(
            name="get_factor_nav",
            description="获取因子净值曲线数据，用于分析因子历史表现趋势。",
            inputSchema={
                "type": "object",
                "properties": {
                    "code": {"type": "string", "description": "因子代码，如 F001"},
                    "start_date": {"type": "string", "description": "开始日期 YYYY-MM-DD"},
                    "end_date": {"type": "string", "description": "结束日期 YYYY-MM-DD"},
                },
                "required": ["code"],
            },
        ),
        types.Tool(
            name="get_market_daily",
            description="获取个股日线行情数据（OHLCV + 涨跌幅）。",
            inputSchema={
                "type": "object",
                "properties": {
                    "ts_code": {"type": "string", "description": "股票代码，如 000001.SZ、600519.SH"},
                    "start_date": {"type": "string", "description": "开始日期 YYYYMMDD"},
                    "end_date": {"type": "string", "description": "结束日期 YYYYMMDD"},
                },
                "required": ["ts_code"],
            },
        ),
        types.Tool(
            name="get_index_daily",
            description="获取指数日线行情。常用指数：000001.SH(上证)、399001.SZ(深证)、000300.SH(沪深300)、000905.SH(中证500)。",
            inputSchema={
                "type": "object",
                "properties": {
                    "ts_code": {"type": "string", "description": "指数代码"},
                    "start_date": {"type": "string", "description": "开始日期 YYYYMMDD"},
                    "end_date": {"type": "string", "description": "结束日期 YYYYMMDD"},
                },
            },
        ),
        types.Tool(
            name="get_valuation",
            description="获取股票估值指标：PE、PB、PS、股息率、总市值、流通市值、换手率等。",
            inputSchema={
                "type": "object",
                "properties": {
                    "ts_code": {"type": "string", "description": "股票代码"},
                    "trade_date": {"type": "string", "description": "交易日期 YYYYMMDD"},
                },
            },
        ),
        types.Tool(
            name="get_stock_info",
            description="获取单只股票基本信息：名称、行业、上市日期、市场板块等。",
            inputSchema={
                "type": "object",
                "properties": {
                    "ts_code": {"type": "string", "description": "股票代码，如 000001.SZ"},
                },
                "required": ["ts_code"],
            },
        ),
        types.Tool(
            name="get_stock_list",
            description="按条件筛选股票列表。可按交易所、行业筛选。",
            inputSchema={
                "type": "object",
                "properties": {
                    "exchange": {"type": "string", "description": "交易所：SSE(上交所)、SZSE(深交所)"},
                    "industry": {"type": "string", "description": "行业名称，如 银行、半导体"},
                    "page": {"type": "integer", "description": "页码", "default": 1},
                    "page_size": {"type": "integer", "description": "每页数量", "default": 50},
                },
            },
        ),
        types.Tool(
            name="get_trade_dates",
            description="获取交易日历，查询指定时间段内的交易日列表。",
            inputSchema={
                "type": "object",
                "properties": {
                    "start_date": {"type": "string", "description": "开始日期 YYYYMMDD"},
                    "end_date": {"type": "string", "description": "结束日期 YYYYMMDD"},
                },
            },
        ),
        types.Tool(
            name="run_backtest",
            description="执行量化策略回测。支持内置策略（涨停首板、低估值、动量、均值回归）和自定义结构化策略。返回年化收益、夏普比率、最大回撤等指标。",
            inputSchema={
                "type": "object",
                "properties": {
                    "strategy_type": {
                        "type": "string",
                        "description": "内置策略：limit_up_first_board(涨停首板)/low_valuation(低估值)/momentum(动量)/mean_reversion(均值回归)",
                        "enum": ["limit_up_first_board", "low_valuation", "momentum", "mean_reversion"],
                    },
                    "strategy_params": {
                        "type": "object",
                        "description": "策略参数。low_valuation:{metric,max_value,top_n}; momentum:{lookback,top_n}; mean_reversion:{indicator,threshold,top_n}",
                    },
                    "universe": {
                        "type": "string",
                        "description": "股票池：hs300/zz500/zz1000/sz50/cyb_all/all",
                        "default": "hs300",
                    },
                    "start": {"type": "string", "description": "开始日期 YYYYMMDD", "default": "20220101"},
                    "end": {"type": "string", "description": "结束日期 YYYYMMDD", "default": "20241231"},
                    "initial_capital": {"type": "number", "description": "初始资金（元）", "default": 1000000},
                },
            },
        ),
    ]


# ============================================================
# Tool execution
# ============================================================

@server.call_tool()
async def handle_call_tool(name: str, arguments: dict) -> List[types.TextContent]:
    try:
        client = _get_client()
        result = await _dispatch(client, name, arguments)
        return [types.TextContent(type="text", text=_format_result(result))]
    except httpx.HTTPStatusError as e:
        status = e.response.status_code
        if status == 429:
            msg = "API 调用次数已达上限。请升级您的订阅方案：https://factorhub.cn/pricing"
        elif status == 401:
            msg = "API Key 无效或已过期。请检查 FACTORHUB_API_KEY 环境变量。"
        elif status == 404:
            msg = f"未找到请求的资源。请检查参数是否正确。"
        else:
            msg = f"API 请求失败 (HTTP {status})"
        return [types.TextContent(type="text", text=msg)]
    except Exception as e:
        return [types.TextContent(type="text", text=f"执行失败: {e}")]


async def _dispatch(client: FactorHubClient, name: str, args: dict):
    if name == "list_factors":
        return await client.list_factors(
            category=args.get("category", ""),
            search=args.get("search", ""),
            page=args.get("page", 1),
            page_size=args.get("page_size", 20),
        )
    elif name == "get_factor_scores":
        return await client.factor_scores(
            args["code"],
            start_date=args.get("start_date", ""),
            end_date=args.get("end_date", ""),
        )
    elif name == "get_factor_nav":
        return await client.factor_nav(
            args["code"],
            start_date=args.get("start_date", ""),
            end_date=args.get("end_date", ""),
        )
    elif name == "get_market_daily":
        return await client.market_daily(
            args["ts_code"],
            start_date=args.get("start_date", ""),
            end_date=args.get("end_date", ""),
        )
    elif name == "get_index_daily":
        return await client.index_daily(
            ts_code=args.get("ts_code", ""),
            start_date=args.get("start_date", ""),
            end_date=args.get("end_date", ""),
        )
    elif name == "get_valuation":
        return await client.valuation(
            ts_code=args.get("ts_code", ""),
            trade_date=args.get("trade_date", ""),
        )
    elif name == "get_stock_info":
        return await client.stock_info(args["ts_code"])
    elif name == "get_stock_list":
        return await client.stock_list(
            exchange=args.get("exchange", ""),
            industry=args.get("industry", ""),
            page=args.get("page", 1),
            page_size=args.get("page_size", 50),
        )
    elif name == "get_trade_dates":
        return await client.trade_dates(
            start_date=args.get("start_date", ""),
            end_date=args.get("end_date", ""),
        )
    elif name == "run_backtest":
        return await client.run_backtest(args)
    else:
        raise ValueError(f"Unknown tool: {name}")


# ============================================================
# Main — supports both stdio and HTTP/SSE transports
# ============================================================

def main():
    """Entry point. Use --sse flag for HTTP/SSE mode (for Smithery/remote)."""
    if "--sse" in sys.argv:
        _run_sse()
    else:
        asyncio.run(_run_stdio())


async def _run_stdio():
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream, write_stream,
            server.create_initialization_options(),
        )


def _run_sse():
    from starlette.applications import Starlette
    from starlette.routing import Mount, Route
    from mcp.server.sse import SseServerTransport
    import uvicorn

    sse = SseServerTransport("/messages/")

    async def handle_sse(request):
        async with sse.connect_sse(
            request.scope, request.receive, request._send
        ) as (read_stream, write_stream):
            await server.run(
                read_stream, write_stream,
                server.create_initialization_options(),
            )

    app = Starlette(
        routes=[
            Route("/sse", endpoint=handle_sse),
            Mount("/messages/", app=sse.handle_post_message),
        ],
    )

    host = os.environ.get("MCP_HOST", "0.0.0.0")
    port = int(os.environ.get("MCP_PORT", "8099"))
    uvicorn.run(app, host=host, port=port)


if __name__ == "__main__":
    main()
