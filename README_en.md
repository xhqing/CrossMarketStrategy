# CBBC\_TRAE

Cross-market Major Events & Hong Kong Stock Leaders Strategy Research — An AI Agent-powered automated research report generation project.

## Overview

This project leverages an AI Agent (TRAE CN SOLO GLM5.1) to automatically generate cross-market strategy research reports, covering the A-share, Hong Kong stock, and US stock markets, with a core focus on Hong Kong stocks. Report content includes:

- **Data Acquisition**: Programmatic fetching of latest market data via Longport API / Yahoo Finance API
- **Major Events Analysis**: Recent events + one-week forward event predictions (with probabilistic scenario analysis)
- **Index Forecast**: Trend outlooks and target levels for 6 major indices
- **Stock Analysis**: In-depth analysis of 27 specified Hong Kong stocks + additional CBBC-active stocks
- **Reasoning Chain**: Complete macro → index → stock reasoning process

## Project Structure

```
CBBC_TRAE/
├── prompt.md                          # AI Agent report generation prompt (core config)
├── config.py                          # API credentials (NOT committed to git)
├── config_example.py                  # Template for API credentials
├── README.md                          # Project documentation (Chinese)
├── README_en.md                       # Project documentation (English)
├── fetch_market_data.py               # Market data fetching script
├── generate_report.py                 # Report generation script
├── quality_check.py                   # Quality validation script
├── debug_timestamp.py                 # Timestamp debugging script
├── .gitignore                         # Git ignore rules
├── LICENSE                            # AGPL-3.0 License
└── output/                            # Output directory
    ├── index_data.csv                 # Index data table
    ├── stock_data.csv                 # Specified stock data table
    ├── cbbc_stock_data.csv            # CBBC-active stock data table
    └── YB_000X_YYYYMMDDHHMMSS.html    # Generated research reports
```

## Covered Instruments

### Indices (6)

| Index | Code |
|-------|------|
| Hang Seng Index | HSI |
| Hang Seng Tech Index | HSTECH |
| HSCEI (China Enterprises Index) | HSCEI |
| Nasdaq 100 Index | .NDX |
| S&P 500 Index | .SPX |
| Dow Jones Industrial Average | .DJI |

### Specified Stocks (27 HK-listed)

Tencent Holdings, Alibaba, Xiaomi, Kuaishou, JD.com, Meituan, Zijin Mining, SMIC, Hua Hong Semiconductor, Pop Mart, China Shenhua Energy, CATL, Ganfeng Lithium, Kunlun Energy, Sinopec, Guotai Junan International, China Hongqiao, China Merchants Bank, China Construction Bank, Bank of China, HSBC, Innovent Biologics, WuXi Biologics, CNOOC, PetroChina, ICBC, BYD

### Additional CBBC-Active Stocks

Beyond the 27 specified stocks, additional Hong Kong stocks with tradable CBBCs are included (e.g., China Mobile, Ping An Insurance, NetEase, Baidu, Li Auto, etc.).

## Data Sources

| Priority | Data Source | Description |
|----------|-------------|-------------|
| Primary | Longport (Longbridge) API | Real-time Hong Kong index and stock quotes |
| Fallback | Yahoo Finance API | US indices and supplementary Hong Kong data |
| Fallback | AKShare / Tushare | A-shares and partial Hong Kong data |
| Fallback | Alpha Vantage | Global stock and index data |

## API Configuration

This project requires a [Longport (Longbridge)](https://www.longbridge.com/) API account. Create a `config.py` file in the project root with your credentials:

```python
LONGPORT_APP_KEY = "your_app_key"
LONGPORT_APP_SECRET = "your_app_secret"
LONGPORT_ACCESS_TOKEN = "your_access_token"
```

⚠️ **Important**: `config.py` is excluded from version control via `.gitignore`. Never commit API credentials to the repository.

## Usage

1. Open this project in Trae IDE
2. Give the AI Agent (TRAE CN SOLO GLM5.1) the following instruction:
   > "根据当前目录中的prompt.md中的具体需求生成一份最新的市场调研报告，该研报生成之后直接使用浏览器打开"
3. The Agent will automatically execute: data fetching → event analysis → index forecast → stock analysis → report generation
4. Reports are output to the `output/` directory in HTML format (naming: `YB_000X_YYYYMMDDHHMMSS.html`)

## Report Features

- **HTML format** with clickable table of contents
- **Real-time data** with accurate timestamps (HK time / US Eastern time)
- **Scenario probability analysis** for future events
- **9-field per-stock analysis** (trend, targets, position advice, logic)
- **Complete reasoning chain** (macro → index → stock)
- **Reference links** with full URLs and source attribution

## Quality Checks

Each generated report passes 30+ quality validations, including:
- ✅ Correct file naming convention
- ✅ All required fields present for indices and stocks
- ✅ Accurate timestamps (real trading times, not K-line dates)
- ✅ Clickable reference links
- ✅ Probability values for scenario analysis
- ✅ No estimated/simulated data

## License

This project is licensed under the **GNU Affero General Public License v3.0** (AGPL-3.0). See the [LICENSE](LICENSE) file for details.

## Disclaimer

Reports generated by this project are for reference only and do not constitute investment advice. Market investments carry risks. CBBCs are high-risk derivative products that may result in total loss upon knock-out. Investors should fully understand product terms and risks before making decisions.
