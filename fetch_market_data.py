#!/usr/bin/env python3
"""
港股数据获取脚本 - 使用 Longport API + Yahoo Finance (备选) 获取指数和个股收盘价
对应 Prompt.md 第三章 数据获取
要求：所有数据必须通过 API 获取，禁止从网络搜索补充
"""

import csv
import os
import time
from datetime import datetime, timezone, timedelta

# 设置 Longport API 配置
os.environ["LONGPORT_APP_KEY"] = "aa01486322da47b757d479b7d934af5e"
os.environ["LONGPORT_APP_SECRET"] = "e07e845719888a88f245ee07161ca9d7bccd5c36a550d68dcea479b3cf419da3"
os.environ["LONGPORT_ACCESS_TOKEN"] = "m_eyJhbGciOiJSUzI1NiIsImtpZCI6ImQ5YWRiMGIxYTdlNzYxNzEiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJsb25nYnJpZGdlIiwic3ViIjoiYWNjZXNzX3Rva2VuIiwiZXhwIjoxNzg0MjY2MzM0LCJpYXQiOjE3NzY0OTAzMzUsImFrIjoiYWEwMTQ4NjMyMmRhNDdiNzU3ZDQ3OWI3ZDkzNGFmNWUiLCJhYWlkIjoyMDg2MTM4MCwiYWMiOiJsYl9wYXBlcnRyYWRpbmciLCJtaWQiOjE4NDIyMjcyLCJzaWQiOiJ5MENjY1kydXpDeW93b2w2ZTRwcUFBPT0iLCJibCI6MywidWwiOjAsImlrIjoibGJfcGFwZXJ0cmFkaW5nXzIwODYxMzgwIn0.JcuyfiWjzWCFSU--cWM6dv7UBL6iQUBY8qOwxx1VoW8zXY3MWtgxX7EUkA_Cy0R3wWpRrYYIwklX83ed7MZcc6YhcGxL-EmC-Ur_59QCyqu5pJ0ScPAPmke5JppML53nLqChwlqhZVMPHs8wKT9BiwKFIVu5wzOb2LI7v5QbFgzpzW5aLHM7iNXaLFGnhLRYDJ81kuzJ4KJtlK8okD1fsjnDQmrMoNBruWfUlmP2bthU3Xv222PTARdQS6EKqVh2PKe1KzLjC7gcZ93N9bqwOaetNl0_gM50SvlUYTILugOPIgW-RyFtkRkmgeb4Abx9c7rY9UYNmGSSCh7KCVN0jpC84jAjK3VEsJid9HAGP2LGWfCdHcgvX2yix6p5DLkoALDsg_iFgz4TfGeiAtGyVpMT0HKsfgz8UHK4ibbvRXm4B_uOHRRNa2F34BnULg0LewY1Ys-lmGka_5s0YMREcESZI-Zw9dju4stRLhArag1iaky_UbHwOZVzP9X-DcAhO2M-GSYgAwB0lImYe53BGzLAxH_aX8SalGs7y8p63dH8H_Vern1DU1h7fKdfN1iKR9r-OsAEvsOlOcQu1Tp-HbZOHg5t9Lf9lXdlyFSMWMy6cevjcW4KoLXi6agWBxc15TiNBZzyxhLTZlOdkOmSqlc7ICehJAPd0iPNC0d3ec4"

from longport.openapi import QuoteContext, Config, Period, AdjustType
import requests


INDICES = [
    ("恒生指数", "HSI", "0HSI.HK", "HK"),
    ("恒生科技指数", "HSTECH", "0HSTECH.HK", "HK"),
    ("国企指数", "HSCEI", "0HSCEI.HK", "HK"),
    ("纳斯达克100指数", ".NDX", "NDX.US", "US"),
    ("标普500指数", ".SPX", "SPX.US", "US"),
    ("道琼斯指数", ".DJI", "DJI.US", "US"),
]

STOCKS = [
    ("腾讯控股", "00700.HK"),
    ("阿里巴巴", "09988.HK"),
    ("小米", "01810.HK"),
    ("快手", "01024.HK"),
    ("京东", "09618.HK"),
    ("美团", "03690.HK"),
    ("紫金矿业", "02899.HK"),
    ("中芯国际", "00981.HK"),
    ("华虹半导体", "01347.HK"),
    ("泡泡玛特", "09992.HK"),
    ("中国神华", "01088.HK"),
    ("宁德时代", "03750.HK"),
    ("赣锋锂业", "01772.HK"),
    ("昆仑能源", "00135.HK"),
    ("中国石油化工股份", "00386.HK"),
    ("国泰君安国际", "01788.HK"),
    ("中国宏桥", "01378.HK"),
    ("招商银行", "03968.HK"),
    ("建设银行", "00939.HK"),
    ("中国银行", "03988.HK"),
    ("汇丰控股", "00005.HK"),
    ("信达生物", "01801.HK"),
    ("药明生物", "02269.HK"),
    ("中国海洋石油", "00883.HK"),
    ("中国石油股份", "00857.HK"),
    ("工商银行", "01398.HK"),
    ("比亚迪股份", "01211.HK"),
]

# Yahoo Finance 映射
YAHOO_SYMBOLS = {
    "NDX.US": "^NDX",
    "SPX.US": "^GSPC",
    "DJI.US": "^DJI",
}


def get_previous_trading_date(timezone_str="HK"):
    if timezone_str == "US":
        tz = timezone(timedelta(hours=-5))
    else:
        tz = timezone(timedelta(hours=8))

    now = datetime.now(tz)
    if now.weekday() == 0 and now.hour < 16:
        prev_date = now - timedelta(days=3)
    elif now.weekday() == 5:  # Saturday
        prev_date = now - timedelta(days=1)
    elif now.weekday() == 6:  # Sunday
        prev_date = now - timedelta(days=2)
    else:
        prev_date = now - timedelta(days=1)

    return prev_date.strftime("%Y-%m-%d")


def fetch_us_indices_from_yahoo():
    """使用 Yahoo Finance API 获取美股三大指数 (备选API)
    
    切换原因: Longport API 的 Nasdaq Basic 权限不包含指数报价，
    因此使用 Yahoo Finance API 作为补充数据源获取美股指数。
    """
    results = []
    errors = []

    for name, symbol, code, tz in [("纳斯达克100指数", ".NDX", "NDX.US", "US"),
                                     ("标普500指数", ".SPX", "SPX.US", "US"),
                                     ("道琼斯指数", ".DJI", "DJI.US", "US")]:
        yahoo_sym = YAHOO_SYMBOLS.get(code)
        if not yahoo_sym:
            errors.append((name, symbol, f"无对应的Yahoo Finance代码"))
            continue

        try:
            url = f"https://query1.finance.yahoo.com/v8/finance/chart/{yahoo_sym}?interval=1d&range=2d"
            headers = {"User-Agent": "Mozilla/5.0"}
            resp = requests.get(url, headers=headers, timeout=10)
            data = resp.json()
            result = data["chart"]["result"][0]
            quotes = result["indicators"]["quote"][0]
            timestamps = result["timestamp"]
            closes = quotes.get("close", [])

            # 获取最后一个有效收盘价
            last_close = None
            last_ts = None
            for i in range(len(closes) - 1, -1, -1):
                if closes[i] is not None:
                    last_close = closes[i]
                    last_ts = timestamps[i]
                    break

            if last_close is not None:
                price_str = f"{last_close:.2f}"
                last_date = get_previous_trading_date(tz)
                results.append([name, symbol, price_str, last_date])
                print(f"  ✓ {name} ({symbol}): {price_str} [Yahoo Finance] (日期: {last_date})")
            else:
                errors.append((name, symbol, "未能获取收盘价数据"))
                print(f"  ✗ {name} ({symbol}): 获取失败 - 无收盘价数据")
        except Exception as e:
            errors.append((name, symbol, f"Yahoo Finance API异常: {str(e)}"))
            print(f"  ✗ {name} ({symbol}): 获取失败 - {str(e)}")

    return results, errors


def fetch_data_with_longport():
    config = Config.from_env()
    ctx = QuoteContext(config)

    results = []
    errors = []

    # 获取港股指数
    print("=" * 60)
    print("正在获取港股指数数据 (Longport API)...")
    print("=" * 60)

    hk_index_codes = [idx[2] for idx in INDICES[:3]]
    try:
        quotes = ctx.quote(hk_index_codes)
        print(f"返回 {len(quotes)} 条港股指数报价")

        for i, idx in enumerate(INDICES[:3]):
            name, symbol, code, tz = idx
            if i < len(quotes):
                q = quotes[i]
                last_price = q.last_done
                last_date = get_previous_trading_date(tz)

                if last_price:
                    price_str = f"{last_price:.2f}"
                    results.append([name, symbol, price_str, last_date])
                    print(f"  ✓ {name} ({symbol}): {price_str} (日期: {last_date})")
                else:
                    error_msg = f"未能获取 {name} 的最新价格"
                    errors.append((name, symbol, error_msg))
                    print(f"  ✗ {name} ({symbol}): 获取失败 - {error_msg}")
            else:
                error_msg = f"指数 {name} 不在返回结果中"
                errors.append((name, symbol, error_msg))
                print(f"  ✗ {name} ({symbol}): 获取失败 - {error_msg}")
    except Exception as e:
        print(f"  ✗ 港股指数数据获取异常: {str(e)}")
        for idx in INDICES[:3]:
            name, symbol, _, _ = idx
            errors.append((name, symbol, f"API异常: {str(e)}"))

    # 尝试获取美股指数 (Longport)
    print("\n正在获取美股指数数据 (Longport API)...")
    us_index_codes = [idx[2] for idx in INDICES[3:]]
    try:
        quotes = ctx.quote(us_index_codes)
        print(f"返回 {len(quotes)} 条美股指数报价")

        for i, idx in enumerate(INDICES[3:]):
            name, symbol, code, tz = idx
            if i < len(quotes):
                q = quotes[i]
                last_price = q.last_done
                if last_price:
                    price_str = f"{last_price:.2f}"
                    last_date = get_previous_trading_date(tz)
                    results.append([name, symbol, price_str, last_date])
                    print(f"  ✓ {name} ({symbol}): {price_str} (日期: {last_date})")
                else:
                    errors.append((name, symbol, "Longport未返回价格"))
                    print(f"  ✗ {name} ({symbol}): Longport未返回价格，将使用Yahoo Finance备选")
            else:
                errors.append((name, symbol, "指数不在返回结果中"))
                print(f"  ✗ {name} ({symbol}): 指数不在返回结果中，将使用Yahoo Finance备选")
    except Exception as e:
        print(f"  ✗ 美股指数数据获取异常: {str(e)}，将使用Yahoo Finance备选")
        for idx in INDICES[3:]:
            name, symbol, _, _ = idx
            errors.append((name, symbol, f"将使用Yahoo Finance备选"))

    # 获取个股数据
    print("\n" + "=" * 60)
    print("正在获取个股数据 (Longport API)...")
    print("=" * 60)

    stock_codes = [s[1] for s in STOCKS]
    try:
        quotes = ctx.quote(stock_codes)
        for i, stock in enumerate(STOCKS):
            name, code = stock
            if i < len(quotes):
                q = quotes[i]
                last_price = q.last_done
                last_date = get_previous_trading_date("HK")

                if last_price:
                    price_str = f"{last_price:.2f}"
                    results.append([name, code, price_str, last_date])
                    print(f"  ✓ {name} ({code}): {price_str} (日期: {last_date})")
                else:
                    error_msg = f"未能获取 {name} 的最新价格"
                    errors.append((name, code, error_msg))
                    print(f"  ✗ {name} ({code}): 获取失败 - {error_msg}")
            else:
                error_msg = f"股票 {name} 不在返回结果中"
                errors.append((name, code, error_msg))
                print(f"  ✗ {name} ({code}): 获取失败 - {error_msg}")
    except Exception as e:
        print(f"  ✗ 个股数据获取异常: {str(e)}")
        for stock in STOCKS:
            name, code = stock
            errors.append((name, code, f"API异常: {str(e)}"))

    return results, errors


def save_to_csv(results, errors, filename="market_data.csv"):
    output_dir = os.path.join(os.path.dirname(__file__), "output")
    os.makedirs(output_dir, exist_ok=True)
    filepath = os.path.join(output_dir, filename)

    with open(filepath, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["标的名称", "代码", "上一交易日收盘价/点数", "上一交易日日期"])
        for row in results:
            writer.writerow(row)

        if errors:
            writer.writerow([])
            writer.writerow(["=== 获取失败的标的 ==="])
            writer.writerow(["标的名称", "代码", "失败原因"])
            for name, code, reason in errors:
                writer.writerow([name, code, reason])

    print(f"\n✓ 数据已保存到: {filepath}")
    return filepath


def main():
    print("港股数据获取脚本 - Longport API + Yahoo Finance (备选)")
    print(f"执行时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("数据源: Longport API (首选) + Yahoo Finance API (备选，仅用于美股指数)")
    print()

    results, errors = fetch_data_with_longport()

    # 如果美股指数获取失败，使用 Yahoo Finance 备选
    failed_us_indices = [(n, s) for n, s, r in errors if s in [".NDX", ".SPX", ".DJI"]]
    if failed_us_indices:
        print("\n" + "=" * 60)
        print("切换至 Yahoo Finance API 获取美股指数数据...")
        print("切换原因: Longport API 的 Nasdaq Basic 权限不包含指数报价")
        print("=" * 60)
        yahoo_results, yahoo_errors = fetch_us_indices_from_yahoo()
        results.extend(yahoo_results)
        # 移除之前失败的美股指数错误记录
        errors = [(n, s, r) for n, s, r in errors if s not in [".NDX", ".SPX", ".DJI"]]
        errors.extend(yahoo_errors)

    if results:
        filepath = save_to_csv(results, errors)
        print(f"\n✓ 成功获取 {len(results)} 个标的数据")
        print(f"✗ 失败 {len(errors)} 个标的")
    else:
        print("\n✗ 未能获取任何数据，请检查API配置")

    if errors:
        print("\n失败标的列表:")
        for name, code, reason in errors:
            print(f"  - {name} ({code}): {reason}")


if __name__ == "__main__":
    main()
