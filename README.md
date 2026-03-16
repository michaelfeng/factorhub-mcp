# FactorHub MCP Server

China A-share market data for AI agents. Query factor scores, market quotes, valuations, and run strategy backtests — all through the [Model Context Protocol (MCP)](https://modelcontextprotocol.io).

[![smithery badge](https://smithery.ai/badge/factorhub)](https://smithery.ai/server/factorhub)

## Features

| Tool | Description |
|------|-------------|
| `set_api_key` | 设置你的 API Key（可选，不设置使用免费体验额度） |
| `list_factors` | 因子列表（分类、搜索） |
| `get_factor_scores` | 因子评分指标（年化收益、夏普、IC等） |
| `get_factor_nav` | 因子净值曲线 |
| `get_market_daily` | 个股日线行情（OHLCV） |
| `get_index_daily` | 指数日线（上证、沪深300等） |
| `get_valuation` | 估值指标（PE、PB、PS、股息率） |
| `get_stock_info` | 个股基本信息 |
| `get_stock_list` | 股票筛选 |
| `get_trade_dates` | 交易日历 |
| `run_backtest` | 量化策略回测 |

## Quick Start

### Option 1: Try Free (No Registration)

Use the hosted server directly — no API key needed, includes free trial quota (10 calls/day).

**Claude Desktop** — add to `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "factorhub": {
      "command": "npx",
      "args": ["-y", "@smithery/cli@latest", "run", "factorhub"]
    }
  }
}
```

Or connect directly via SSE:

```
https://factorhub.cn/mcp/sse
```

### Option 2: Install with Your API Key

For higher quotas, register at [factorhub.cn](https://factorhub.cn) and get your API key at the [API Keys page](https://factorhub.cn/api-keys).

```bash
pip install factorhub-mcp
```

**Claude Desktop** — add to `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "factorhub": {
      "command": "factorhub-mcp",
      "env": {
        "FACTORHUB_API_KEY": "fh_your_api_key_here"
      }
    }
  }
}
```

**Cursor** — add to `.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "factorhub": {
      "command": "factorhub-mcp",
      "env": {
        "FACTORHUB_API_KEY": "fh_your_api_key_here"
      }
    }
  }
}
```

**Claude Code** — run:

```bash
claude mcp add factorhub -- env FACTORHUB_API_KEY=fh_your_api_key_here factorhub-mcp
```

**OpenClaw** — add to your skill config:

```yaml
providers:
  factorhub:
    type: mcp
    command: factorhub-mcp
    env:
      FACTORHUB_API_KEY: "fh_your_api_key_here"
```

### Option 3: Smithery

[![smithery badge](https://smithery.ai/badge/factorhub)](https://smithery.ai/server/factorhub)

Install via [Smithery](https://smithery.ai/server/factorhub) for automatic setup with any MCP client.

## Usage Examples

Once configured, ask your AI assistant:

- "查看 FactorHub 有哪些因子"
- "获取动量因子的历史表现"
- "帮我查一下贵州茅台最近一年的行情"
- "用低估值策略回测沪深300成分股"
- "对比动量因子和价值因子的夏普比率"

You can also set your own API key mid-conversation for higher quotas:

- "用我的 API Key fh_xxx 登录 FactorHub"

## Pricing

| Plan | API Calls/Day | Backtest/Day | Price |
|------|---------------|--------------|-------|
| Free | 10 | 1 | ¥0 |
| Starter | 50 | 5 | ¥39/mo |
| Pro | 200 | 20 | ¥99/mo |
| Enterprise | 1000 | 100 | ¥299/mo |

Upgrade at [factorhub.cn/pricing](https://factorhub.cn/pricing).

## Architecture

This MCP server is a **thin client** that calls the [FactorHub public API](https://factorhub.cn/api-docs). It does not access any database directly or contain proprietary logic.

```
AI Agent  →  MCP Protocol  →  factorhub-mcp  →  HTTPS  →  factorhub.cn/api/v1
```

## Security

- API key is stored in environment variables, never hardcoded
- All communication uses HTTPS
- No user data is stored locally
- Rate limiting is enforced server-side

## License

MIT
