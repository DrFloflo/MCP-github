import datetime
import requests
from html_to_markdown import convert_to_markdown
import re
from core.logger import logger

def get_current_utc_timestamp() -> str:
    """
    Return the current UTC time in the format: YYYY-MM-DDTHH:MM:SS.ffffff0Z
    (i.e., 7 digits of fractional seconds, ending with 'Z').
    """
    now = datetime.datetime.now(datetime.timezone.utc)
    # now.microsecond is 0–999999 (6 digits); append '0' for a 7th digit
    fraction = f"{now.microsecond:06d}0"
    return f"{now.year:04d}-{now.month:02d}-{now.day:02d}T" \
           f"{now.hour:02d}:{now.minute:02d}:{now.second:02d}." \
           f"{fraction}Z"

def get_website_content(url: str) -> str:
    """
    Get the content of a website in Markdown format.

    Args:
        url: The URL of the website to get the content for.

    Returns:
        The content of the website cleaned in markdown.
    """
    try:
        response = requests.get(url)
        text = response.content.decode("utf-8")
        markdown_content = convert_to_markdown(text)
        markdown_content = re.sub(r'\n{2,}', '\n', markdown_content)
        return markdown_content
    except Exception as e:
        logger.error("Unable to connect or parse response, error: ", e)
        return "Unable to connect or parse response, error: " + str(e)