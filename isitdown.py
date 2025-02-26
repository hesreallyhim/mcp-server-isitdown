import asyncio
from typing import TYPE_CHECKING

TYPE_CHECKING = True

from dotenv.cli import get
import requests
from bs4 import  BeautifulSoup as bs
from bs4._typing import Tag
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("isitdown")

ISITDOWN_BASE_URL = "https://www.isitdownrightnow.com/check.php?domain="
USER_AGENT = "isitdown-app/0.0.1"

def get_last_down(last_down_row: Tag) -> str:
    """
    Extract the last down time from the HTML row.
    Args:
        last_down_row (str): The HTML row containing the last checked time.
    Returns:
        str: The last time the server found the website to be down.
    """
    last_down_time = last_down_row.find_next("span", class_="tab")
    if last_down_time is None:
        return "Last down time not found."
    else:
        return f"Last down time is {last_down_time.text.strip()}"

@mcp.tool()
async def get_website_status(root_domain: str) -> str:
    """
    Check the status of a website.
    This function takes a root domain as input and checks whether the website is up or down
    by making a request to isitdownrightnow.com
    Args:
        root_domain (str): The root domain of the website to check.
    Returns:
        str: A message indicating whether the website is up or down, or if the status could not be determined.
    """
    
    try:
        response = requests.get(
            f"{ISITDOWN_BASE_URL}{root_domain}", headers={"User-Agent": USER_AGENT}
        )
        response.raise_for_status()
    except requests.RequestException as e:
        return "Could not determine the status of the website."
    soup = bs(response.text, "html.parser")
    is_up = soup.find("span", class_="upicon")
    is_down = soup.find("span", class_="downicon")
    tabletrsimple_divs = soup.find_all("div", class_="tabletrsimple")
    if len(tabletrsimple_divs) >= 1:
        last_down_row = tabletrsimple_divs[1] # NOTE: Brittle.
        if isinstance(last_down_row, Tag):
            last_down_time = get_last_down(last_down_row)
    if is_down:
        return f"The website is down. {last_down_time}."
    elif is_up:
        return f"The website is up. {last_down_time}."
    else:
        return "Could not determine the status of the website."

if __name__ == "__main__":
    asyncio.run(mcp.run_stdio_async())
