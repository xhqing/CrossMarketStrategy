import os
import sys
import logging
from datetime import datetime
import pytz

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

try:
    from longport.openapi import QuoteContext, Config, Period, AdjustType
    LONGPORT_AVAILABLE = True
except ImportError:
    LONGPORT_AVAILABLE = False
    logger.error("Longport SDK not available")

APP_KEY = "aa01486322da47b757d479b7d934af5e"
APP_SECRET = "e07e845719888a88f245ee07161ca9d7bccd5c36a550d68dcea479b3cf419da3"
ACCESS_TOKEN = "m_eyJhbGciOiJSUzI1NiIsImtpZCI6ImQ5YWRiMGIxYTdlNzYxNzEiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJsb25nYnJpZGdlIiwic3ViIjoiYWNjZXNzX3Rva2VuIiwiZXhwIjoxNzg0MjY2MzM0LCJpYXQiOjE3NzY0OTAzMzUsImFrIjoiYWEwMTQ4NjMyMmRhNDdiNzU3ZDQ3OWI3ZDkzNGFmNWUiLCJhYWlkIjoyMDg2MTM4MCwiYWMiOiJsYl9wYXBlcnRyYWRpbmciLCJtaWQiOjE4NDIyMjcyLCJzaWQiOiJ5MENjY1kydXpDeW93b2w2ZTRwcUFBPT0iLCJibCI6MywidWwiOjAsImlrIjoibGJfcGFwZXJ0cmFkaW5nXzIwODYxMzgwIn0.JcuyfiWjzWCFSU--cWM6dv7UBL6iQUBY8qOwxx1VoW8zXY3MWtgxX7EUkA_Cy0R3wWpRrYYIwklX83ed7MZcc6YhcGxL-EmC-Ur_59QCyqu5pJ0ScPAPmke5JppML53nLqChwlqhZVMPHs8wKT9BiwKFIVu5wzOb2LI7v5QbFgzpzW5aLHM7iNXaLFGnhLRYDJ81kuzJ4KJtlK8okD1fsjnDQmrMoNBruWfUlmP2bthU3Xv222PTARdQS6EKqVh2PKe1KzLjC7gcZ93N9bqwOaetNl0_gM50SvlUYTILugOPIgW-RyFtkRkmgeb4Abx9c7rY9UYNmGSSCh7KCVN0jpC84jAjK3VEsJid9HAGP2LGWfCdHcgvX2yix6p5DLkoALDsg_iFgz4TfGeiAtGyVpMT0HKsfgz8UHK4ibbvRXm4B_uOHRRNa2F34BnULg0LewY1Ys-lmGka_5s0YMREcESZI-Zw9dju4stRLhArag1iaky_UbHwOZVzP9X-DcAhO2M-GSYgAwB0lImYe53BGzLAxH_aX8SalGs7y8p63dH8H_Vern1DU1h7fKdfN1iKR9r-OsAEvsOlOcQu1Tp-HbZOHg5t9Lf9lXdlyFSMWMy6cevjcW4KoLXi6agWBxc15TiNBZzyxhLTZlOdkOmSqlc7ICehJAPd0iPNC0d3ec4"

def get_longport_context():
    if not LONGPORT_AVAILABLE:
        return None
    try:
        config = Config(app_key=APP_KEY, app_secret=APP_SECRET, access_token=ACCESS_TOKEN)
        ctx = QuoteContext(config)
        return ctx
    except Exception as e:
        logger.error(f"Failed to create Longport context: {e}")
        return None

def debug_timestamp():
    ctx = get_longport_context()
    if ctx is None:
        logger.error("Cannot create Longport context")
        return

    symbols = ["00700.HK", "09988.HK", "9988.HK"]

    for symbol in symbols:
        logger.info(f"\n=== Debugging symbol: {symbol} ===")

        logger.info("1. Testing ctx.quote()")
        try:
            quotes = ctx.quote([symbol])
            if quotes:
                q = quotes[0]
                print(f"  quote.last_done: {q.last_done}")
                print(f"  quote.timestamp: {q.timestamp} (type: {type(q.timestamp).__name__})")
                print(f"  quote.timestamp type value: {repr(q.timestamp)}")
        except Exception as e:
            print(f"  quote failed: {e}")

        logger.info("2. Testing ctx.candlesticks()")
        try:
            candles = ctx.candlesticks(symbol, Period.Day, 5, AdjustType.NoAdjust)
            if candles:
                print(f"  Number of candles: {len(candles)}")
                for i, c in enumerate(candles):
                    print(f"  Candle {i}: close={c.close}, timestamp={c.timestamp} (type: {type(c.timestamp).__name__})")
                    print(f"    timestamp repr: {repr(c.timestamp)}")
            else:
                print("  No candles returned")
        except Exception as e:
            print(f"  candlesticks failed: {e}")

        logger.info("3. Testing datetime conversion")
        try:
            candles = ctx.candlesticks(symbol, Period.Day, 1, AdjustType.NoAdjust)
            if candles:
                c = candles[-1]
                ts = c.timestamp
                print(f"  Original timestamp: {repr(ts)}")

                if isinstance(ts, (int, float)):
                    from datetime import timezone
                    dt = datetime.fromtimestamp(ts, tz=timezone.utc)
                    print(f"  As int/float -> UTC datetime: {dt}")
                elif hasattr(ts, 'year'):
                    print(f"  Has year attribute -> {ts}")

                bj_tz = pytz.timezone('Asia/Shanghai')
                if isinstance(ts, (int, float)):
                    dt_local = datetime.fromtimestamp(ts, tz=timezone.utc).astimezone(bj_tz)
                else:
                    dt_local = ts.astimezone(bj_tz) if hasattr(ts, 'astimezone') else str(ts)
                print(f"  Converted to Beijing time: {dt_local}")
        except Exception as e:
            print(f"  datetime conversion failed: {e}")

        print()

    bj_tz = pytz.timezone('Asia/Shanghai')
    now_bj = datetime.now(bj_tz)
    print(f"\nCurrent Beijing time: {now_bj}")
    print(f"Expected market close time (HK): 16:00-16:08 Beijing time")

if __name__ == "__main__":
    debug_timestamp()
