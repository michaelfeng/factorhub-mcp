# FactorHub MCP Server

[English](#english) | [中文](#中文)

[![smithery badge](https://smithery.ai/badge/factorhub)](https://smithery.ai/server/factorhub)

---

<a id="中文"></a>

## 中文

A 股量化数据 MCP 服务器 —— 让 Claude、Cursor 等 AI 工具直接查询因子数据、行情、估值、回测。

### 功能列表

| 工具 | 说明 |
|------|------|
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

### 快速开始

#### 方式一：免费体验（无需注册）

使用托管服务器，无需 API Key，自带免费额度（10 次/天）。

**Claude Desktop** —— 编辑 `claude_desktop_config.json`：

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

或直接远程连接：

```
https://factorhub.cn/mcp/sse
```

#### 方式二：安装到本地（使用自己的 API Key）

注册 [factorhub.cn](https://factorhub.cn)，在 [API Key 管理页](https://factorhub.cn/api-keys) 生成 Key，获得更高额度。

```bash
pip install factorhub-mcp
```

**Claude Desktop** —— 编辑 `claude_desktop_config.json`：

```json
{
  "mcpServers": {
    "factorhub": {
      "command": "factorhub-mcp",
      "env": {
        "FACTORHUB_API_KEY": "fh_你的密钥"
      }
    }
  }
}
```

**Cursor** —— 编辑 `.cursor/mcp.json`，格式同上。

**Claude Code** —— 运行：

```bash
claude mcp add factorhub -- env FACTORHUB_API_KEY=fh_你的密钥 factorhub-mcp
```

**OpenClaw** —— 添加到技能配置：

```yaml
providers:
  factorhub:
    type: mcp
    command: factorhub-mcp
    env:
      FACTORHUB_API_KEY: "fh_你的密钥"
```

#### 方式三：通过 Smithery 安装

[![smithery badge](https://smithery.ai/badge/factorhub)](https://smithery.ai/server/factorhub)

在 [Smithery](https://smithery.ai/server/factorhub) 一键安装，自动配置到你的 AI 客户端。

### 使用示例

配置完成后，直接对你的 AI 助手说：

- "查看 FactorHub 有哪些因子"
- "获取动量因子的历史表现"
- "帮我查一下贵州茅台最近一年的行情"
- "用低估值策略回测沪深300成分股"
- "对比动量因子和价值因子的夏普比率"

也可以在对话中设置自己的 Key 来获得更多额度：

- "用我的 API Key fh_xxx 登录 FactorHub"

### 定价

| 方案 | API 调用/天 | 回测/天 | 价格 |
|------|------------|---------|------|
| Free | 20 | 3 | ¥0 |
| Pro | 10,000 | 20 | ¥99/月 |
| Pro Max | 40,000 | 100 | ¥199/月 |
| Ultra | 不限 | 不限 | ¥899/月 |

升级方案：[factorhub.cn/pricing](https://factorhub.cn/pricing)

### 架构

本 MCP 服务器是一个**轻量客户端**，通过 HTTPS 调用 [FactorHub 公开 API](https://factorhub.cn/api-docs)，不直接访问数据库，不包含任何私有逻辑。

```
AI 助手  →  MCP 协议  →  factorhub-mcp  →  HTTPS  →  factorhub.cn/api/v1
```

### 安全

- API Key 存储在环境变量中，不会硬编码
- 所有通信使用 HTTPS 加密
- 本地不存储任何用户数据
- 服务端强制频率限制

---

<a id="english"></a>

## English

China A-share market data for AI agents. Query factor scores, market quotes, valuations, and run strategy backtests — all through the [Model Context Protocol (MCP)](https://modelcontextprotocol.io).

### Features

| Tool | Description |
|------|-------------|
| `set_api_key` | Set your API key (optional, defaults to free trial quota) |
| `list_factors` | List factors with category/search filters |
| `get_factor_scores` | Factor metrics: annual return, Sharpe, max drawdown, IC, etc. |
| `get_factor_nav` | Factor NAV curve for trend analysis |
| `get_market_daily` | Stock daily OHLCV data |
| `get_index_daily` | Index daily data (SSE, CSI 300, CSI 500, etc.) |
| `get_valuation` | Valuation metrics: PE, PB, PS, dividend yield |
| `get_stock_info` | Stock basic info |
| `get_stock_list` | Stock screening by exchange/industry |
| `get_trade_dates` | Trading calendar |
| `run_backtest` | Strategy backtesting |

### Quick Start

#### Option 1: Try Free (No Registration)

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

#### Option 2: Install with Your API Key

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

**Cursor** — add to `.cursor/mcp.json` (same format as above).

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

#### Option 3: Smithery

[![smithery badge](https://smithery.ai/badge/factorhub)](https://smithery.ai/server/factorhub)

Install via [Smithery](https://smithery.ai/server/factorhub) for automatic setup with any MCP client.

### Usage Examples

Once configured, ask your AI assistant:

- "List all available factors on FactorHub"
- "Show momentum factor performance"
- "Get Kweichow Moutai stock data for the past year"
- "Backtest a low-valuation strategy on CSI 300"
- "Compare Sharpe ratios of momentum vs value factors"

Set your own API key mid-conversation for higher quotas:

- "Set my FactorHub API key to fh_xxx"

### Pricing

| Plan | API Calls/Day | Backtest/Day | Price |
|------|---------------|--------------|-------|
| Free | 20 | 3 | ¥0 |
| Pro | 10,000 | 20 | ¥99/mo |
| Pro Max | 40,000 | 100 | ¥199/mo |
| Ultra | Unlimited | Unlimited | ¥899/mo |

Upgrade at [factorhub.cn/pricing](https://factorhub.cn/pricing).

### Architecture

This MCP server is a **thin client** that calls the [FactorHub public API](https://factorhub.cn/api-docs). It does not access any database directly or contain proprietary logic.

```
AI Agent  →  MCP Protocol  →  factorhub-mcp  →  HTTPS  →  factorhub.cn/api/v1
```

### Security

- API key is stored in environment variables, never hardcoded
- All communication uses HTTPS
- No user data is stored locally
- Rate limiting is enforced server-side

## License

MIT
