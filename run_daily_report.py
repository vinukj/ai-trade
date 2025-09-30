import logging
from pathlib import Path
import pytz  # noqa: E0401  # add for IST date formatting
from datetime import datetime  # add for date header
import sys  # noqa: E402  # for exit on LLM errors

from ai_trade.fetch import fetch_nifty_spot
from ai_trade.prompt import build_prompt
from ai_trade.llm import call_llm
from ai_trade.notify import send_telegram


def main():
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    logger = logging.getLogger(__name__)

    logger.info("Starting daily Nifty report job")
    spot = fetch_nifty_spot()
    logger.info(f"Fetched Nifty spot at 09:30 IST: {spot}")

    template_path = Path(__file__).parent / "prompts" / "prompt_template.j2"
    prompt = build_prompt(str(template_path), spot)
    logger.info("Built prompt for LLM call")

    try:
        result = call_llm(prompt)
        logger.info("Received response from LLM")
    except Exception as e:
        logger.exception("LLM call failed")
        print("Error during LLM call:", e)
        sys.exit(1)

    # Build header with today's IST date and bullet the LLM's lines
    tz = pytz.timezone("Asia/Kolkata")
    # Weekday abbreviation and day-month for header
    weekday = datetime.now(tz).strftime("%a")
    daymonth = datetime.now(tz).strftime("%d %b")
    header = f"Today’s Nifty Actionable Summary – {weekday}, {daymonth}\n"
    lines = result.strip().splitlines()
    # extract only the three key summary lines from the LLM output
    strategy = next((l for l in lines if l.startswith("Strategy to Pursue")), None)
    probability = next((l for l in lines if l.startswith("Probability")), None)
    exit_rule = next((l for l in lines if l.startswith("Exit")), None)
    # format exactly: one space indent for strategy, bullets for the rest
    message = header
    if strategy:
        message += f" {strategy}\n"
    if probability:
        message += f"- {probability}\n"
    if exit_rule:
        message += f"- {exit_rule}\n"
    # print for local verification
    print(message)
    send_telegram(message)
    logger.info("Sent formatted summary to Telegram")


if __name__ == "__main__":
    main()
