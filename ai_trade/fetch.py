import pytz  # noqa: E0401
from datetime import datetime, timedelta
import yfinance as yf  # noqa: E0401
import pandas as pd  # noqa: E0401  # type: ignore
import config  # add config import for FETCH_TIME


def fetch_nifty_spot():
    """
    Fetch the Nifty 50 spot price at the configured FETCH_TIME IST for today's session
    (fallback to previous trading day if needed).
    """
    tz = pytz.timezone("Asia/Kolkata")
    # get last two days of 1m bars
    data = yf.Ticker("^NSEI").history(period="2d", interval="1m")
    # ensure UTC index before converting
    if data.index.tzinfo is None:
        data.index = data.index.tz_localize("UTC")
    data = data.tz_convert(tz)

    today = datetime.now(tz).date()
    # try today first, then yesterday
    for target_date in (today, today - timedelta(days=1)):
        day_data = data.loc[data.index.date == target_date]
        # use configured fetch time (HH:MM IST)
        ft = config.FETCH_TIME
        frame = day_data.between_time(ft, ft)
        if not frame.empty:
            return frame["Close"].iloc[0]
    raise RuntimeError(f"No Nifty data available at {config.FETCH_TIME} IST for today or previous day")
