import datetime
import pytz  # noqa: E0401  # type: ignore
from jinja2 import Template  # noqa: E0401  # type: ignore
from pathlib import Path


def build_prompt(template_path: str, spot: float) -> str:
    """
    Render and return the prompt using the Jinja2 template at template_path, injecting date, weekday, and spot.
    """
    tz = pytz.timezone("Asia/Kolkata")
    today = datetime.datetime.now(tz)
    context = {
        "date": today.strftime("%d %b %Y"),
        "weekday": today.strftime("%A"),
        "spot": int(spot),
    }
    template = Template(Path(template_path).read_text())
    return template.render(**context)
