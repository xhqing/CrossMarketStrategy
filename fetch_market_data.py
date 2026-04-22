import os
import sys
import json
import time
import logging
import pandas as pd
import yaml
from datetime import datetime
import pytz

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'output')
os.makedirs(OUTPUT_DIR, exist_ok=True)

try:
    from longport.openapi import QuoteContext, Config, Period, AdjustType
    LONGPORT_AVAILABLE = True
    logger.info("Longport SDK available")
except ImportError:
    LONGPORT_AVAILABLE = False
    logger.warning("Longport SDK not available")

from config import LONGPORT_APP_KEY, LONGPORT_APP_SECRET, LONGPORT_ACCESS_TOKEN


def load_targets_config():
    config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'targets.yaml')
    if not os.path.exists(config_path):
        logger.warning(f"targets.yaml not found at {config_path}, using empty config")
        return {"hk_shares": {"index_major": [], "index_sector": [], "hkex_stocks": [], "hkex_etf": []}}

    with open(config_path, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)
    logger.info(f"Loaded targets config from {config_path}")
    return config


def filter_valid_targets(target_list):
    return [t for t in target_list if t.get('name') and t.get('code')]


def get_indices_from_config(config):
    indices = []
    hk_shares = config.get('hk_shares', {})

    for idx in hk_shares.get('index_major', []):
        if idx.get('name') and idx.get('code'):
            indices.append({
                "指数名称": idx['name'],
                "指数代码": idx['code'],
                "lp_code": idx['code']
            })

    for idx in hk_shares.get('index_sector', []):
        if idx.get('name') and idx.get('code'):
            indices.append({
                "指数名称": idx['name'],
                "指数代码": idx['code'],
                "lp_code": idx['code']
            })

    return indices


def get_stocks_from_config(config):
    stocks = []
    hk_shares = config.get('hk_shares', {})

    for stock in hk_shares.get('hkex_stocks', []):
        if stock.get('name') and stock.get('code'):
            stocks.append({
                "股票名称": stock['name'],
                "股票代码": stock['code'],
                "lp_code": stock['code']
            })

    return stocks


def get_longport_context():
    if not LONGPORT_AVAILABLE:
        return None
    try:
        config = Config(
            app_key=LONGPORT_APP_KEY,
            app_secret=LONGPORT_APP_SECRET,
            access_token=LONGPORT_ACCESS_TOKEN,
        )
        ctx = QuoteContext(config)
        logger.info("Longport context created successfully")
        return ctx
    except Exception as e:
        logger.error(f"Failed to create Longport context: {e}")
        return None


def fetch_longport_quote(ctx, symbols):
    if ctx is None:
        return {}
    results = {}
    try:
        quotes = ctx.quote(symbols)
        for q in quotes:
            results[q.symbol] = {
                "price": float(q.last_done),
                "timestamp": q.timestamp,
            }
        logger.info(f"Longport: Got quotes for {len(results)} symbols")
    except Exception as e:
        logger.warning(f"Longport quote failed: {e}")
        for i in range(0, len(symbols), 5):
            batch = symbols[i:i+5]
            try:
                quotes = ctx.quote(batch)
                for q in quotes:
                    results[q.symbol] = {
                        "price": float(q.last_done),
                        "timestamp": q.timestamp,
                    }
                time.sleep(0.5)
            except Exception as e2:
                logger.warning(f"Longport batch quote failed for {batch}: {e2}")
    return results


def fetch_longport_stock_data(ctx, symbol):
    if ctx is None:
        return None, None, None
    price = None
    ts = None
    source = "Longport API"
    try:
        quotes = ctx.quote([symbol])
        if quotes:
            q = quotes[0]
            price = round(float(q.last_done), 2)
            ts = q.timestamp
            if ts is not None and hasattr(ts, 'hour') and ts.hour == 0 and ts.minute == 0 and ts.second == 0:
                ts = None
        if price is None:
            try:
                candles = ctx.candlesticks(symbol, Period.Day, 1, AdjustType.NoAdjust)
                if candles:
                    latest = candles[-1]
                    price = round(float(latest.close), 2)
                    ts = latest.timestamp
            except Exception as e:
                logger.warning(f"Longport candlestick also failed for {symbol}: {e}")
    except Exception as e:
        logger.warning(f"Longport quote failed for {symbol}: {e}")
        try:
            candles = ctx.candlesticks(symbol, Period.Day, 1, AdjustType.NoAdjust)
            if candles:
                latest = candles[-1]
                price = round(float(latest.close), 2)
                ts = latest.timestamp
        except Exception as e2:
            logger.warning(f"Longport candlestick failed for {symbol}: {e2}")
    return price, ts, source


def format_timestamp(ts, is_us_index=False):
    try:
        if isinstance(ts, (int, float)):
            from datetime import timezone
            dt = datetime.fromtimestamp(ts, tz=timezone.utc)
            if is_us_index:
                local_tz = pytz.timezone('US/Eastern')
                dt_local = dt.astimezone(local_tz)
                return dt_local.strftime('%Y-%m-%d %H:%M:%S') + " (美东时间)"
            else:
                local_tz = pytz.timezone('Asia/Shanghai')
                dt_local = dt.astimezone(local_tz)
                return dt_local.strftime('%Y-%m-%d %H:%M:%S') + " (北京时间)"
        elif hasattr(ts, 'year'):
            dt = ts
            if is_us_index:
                if dt.tzinfo is None:
                    dt = pytz.timezone('US/Eastern').localize(dt)
                return dt.strftime('%Y-%m-%d %H:%M:%S') + " (美东时间)"
            else:
                if dt.tzinfo is None:
                    bj_tz = pytz.timezone('Asia/Shanghai')
                    dt = bj_tz.localize(dt)
                return dt.strftime('%Y-%m-%d %H:%M:%S') + " (北京时间)"
        else:
            return str(ts)
    except Exception as e:
        return str(ts)


CBBC_STOCKS = [
    {"股票名称": "新鸿基地产", "股票代码": "00016.HK", "lp_code": "00016.HK"},
    {"股票名称": "恒基地产", "股票代码": "00012.HK", "lp_code": "00012.HK"},
    {"股票名称": "新世界发展", "股票代码": "00017.HK", "lp_code": "00017.HK"},
    {"股票名称": "长实集团", "股票代码": "01113.HK", "lp_code": "01113.HK"},
    {"股票名称": "香港交易所", "股票代码": "00388.HK", "lp_code": "00388.HK"},
    {"股票名称": "友邦保险", "股票代码": "01299.HK", "lp_code": "01299.HK"},
    {"股票名称": "中国人寿", "股票代码": "02628.HK", "lp_code": "02628.HK"},
    {"股票名称": "中国平安", "股票代码": "02318.HK", "lp_code": "02318.HK"},
    {"股票名称": "中国移动", "股票代码": "00941.HK", "lp_code": "00941.HK"},
    {"股票名称": "中国联通", "股票代码": "00762.HK", "lp_code": "00762.HK"},
    {"股票名称": "中国电信", "股票代码": "00728.HK", "lp_code": "00728.HK"},
    {"股票名称": "网易", "股票代码": "09999.HK", "lp_code": "09999.HK"},
    {"股票名称": "百度集团", "股票代码": "09888.HK", "lp_code": "09888.HK"},
    {"股票名称": "哔哩哔哩", "股票代码": "09626.HK", "lp_code": "09626.HK"},
    {"股票名称": "蔚来", "股票代码": "09866.HK", "lp_code": "09866.HK"},
    {"股票名称": "理想汽车", "股票代码": "02015.HK", "lp_code": "02015.HK"},
    {"股票名称": "小鹏汽车", "股票代码": "09868.HK", "lp_code": "09868.HK"},
    {"股票名称": "海尔智家", "股票代码": "06690.HK", "lp_code": "06690.HK"},
    {"股票名称": "李宁", "股票代码": "02331.HK", "lp_code": "02331.HK"},
    {"股票名称": "安踏体育", "股票代码": "02020.HK", "lp_code": "02020.HK"},
]

SUPPLEMENT_INDICES = [
    {"指数名称": "纳斯达克100指数", "指数代码": ".NDX", "lp_code": ".NDX"},
    {"指数名称": "标普500指数", "指数代码": ".SPX", "lp_code": ".SPX"},
    {"指数名称": "道琼斯指数", "指数代码": ".DJI", "lp_code": ".DJI"},
]


def main():
    logger.info("=== Starting market data fetch via Longport SDK ===")

    targets_config = load_targets_config()
    INDICES = get_indices_from_config(targets_config)
    STOCKS = get_stocks_from_config(targets_config)

    INDICES = INDICES + SUPPLEMENT_INDICES

    logger.info(f"Loaded {len(INDICES)} indices and {len(STOCKS)} stocks from config")

    ctx = get_longport_context()

    if ctx is None:
        logger.error("Cannot create Longport context, exiting")
        sys.exit(1)

    logger.info("--- Fetching Index Data ---")
    index_results = []
    for idx in INDICES:
        logger.info(f"Fetching index: {idx['指数名称']} ({idx['lp_code']})")
        is_us = idx['指数名称'] in ["纳斯达克100指数", "标普500指数", "道琼斯指数"]
        price, ts, source = fetch_longport_stock_data(ctx, idx['lp_code'])

        time_str = format_timestamp(ts, is_us) if ts else "获取失败"
        index_results.append({
            "指数名称": idx['指数名称'],
            "指数代码": idx['指数代码'],
            "当前最新点数": price if price else "获取失败",
            "当前最新点数对应时间戳": time_str,
            "数据来源": source
        })
        time.sleep(0.3)

    df_index = pd.DataFrame(index_results)
    index_csv = os.path.join(OUTPUT_DIR, 'index_data.csv')
    df_index.to_csv(index_csv, index=False, encoding='utf-8-sig')
    logger.info(f"Index data saved to {index_csv}")

    logger.info("--- Fetching Stock Data ---")
    stock_results = []
    for i, stock in enumerate(STOCKS):
        logger.info(f"Fetching stock: {stock['股票名称']} ({stock['lp_code']})")
        price, ts, source = fetch_longport_stock_data(ctx, stock['lp_code'])
        time_str = format_timestamp(ts, False) if ts else "获取失败"
        stock_results.append({
            "股票名称": stock['股票名称'],
            "股票代码": stock['股票代码'],
            "当前最新价格(HKD)": price if price else "获取失败",
            "当前最新价格对应时间戳": time_str,
            "数据来源": source
        })
        time.sleep(0.3)

    df_stock = pd.DataFrame(stock_results)
    stock_csv = os.path.join(OUTPUT_DIR, 'stock_data.csv')
    df_stock.to_csv(stock_csv, index=False, encoding='utf-8-sig')
    logger.info(f"Stock data saved to {stock_csv}")

    logger.info("--- Fetching CBBC Stock Data ---")
    cbbc_results = []
    for stock in CBBC_STOCKS:
        logger.info(f"Fetching CBBC stock: {stock['股票名称']} ({stock['lp_code']})")
        price, ts, source = fetch_longport_stock_data(ctx, stock['lp_code'])
        time_str = format_timestamp(ts, False) if ts else "获取失败"
        cbbc_results.append({
            "股票名称": stock['股票名称'],
            "股票代码": stock['股票代码'],
            "当前最新价格(HKD)": price if price else "获取失败",
            "当前最新价格对应时间戳": time_str,
            "数据来源": source
        })
        time.sleep(0.3)

    df_cbbc = pd.DataFrame(cbbc_results)
    cbbc_csv = os.path.join(OUTPUT_DIR, 'cbbc_stock_data.csv')
    df_cbbc.to_csv(cbbc_csv, index=False, encoding='utf-8-sig')
    logger.info(f"CBBC stock data saved to {cbbc_csv}")

    logger.info("=== Data fetch completed ===")

    print("\n=== 指数数据 ===")
    print(df_index.to_string(index=False))
    print("\n=== 个股数据 ===")
    print(df_stock.to_string(index=False))
    print("\n=== 牛熊证个股数据 ===")
    print(df_cbbc.to_string(index=False))


if __name__ == "__main__":
    main()
