import httpx

from bs4 import BeautifulSoup as bs
from bs4.element import Tag
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("isitdown", "Help the user determine if a website is down or not.")

ISITDOWN_BASE_URL = "https://www.isitdownrightnow.com/check.php?domain="
USER_AGENT = "mcp-isitdown-server/0.0.2"


def get_last_down(last_down_row: Tag) -> str:
    """
    Extract the last down time from the HTML row.
    Args:
        last_down_row (bs4.Tag): The HTML row containing the last checked time.
    Returns:
        str: The last time the server found the website to be down.
    """
    last_down_time = last_down_row.find_next("span", class_="tab")
    if last_down_time is None:
        return "Last down time not found."
    else:
        return f"Last down time is: {last_down_time.text.strip()}"


def get_response_msg(is_down: bool, is_up: bool, last_down_time: str) -> str:
    """
    Format the response message based on website status.
    Args:
        is_down (bool): Whether the website is down.
        is_up (bool): Whether the website is up.
        last_down_time (str): The last time the website was down.
    Returns:
        str: Formatted status message.
    """
    if is_down:
        return f"The website is down. {last_down_time}"
    elif is_up:
        return f"The website is up. {last_down_time}"
    else:
        return "Could not determine the status of the website."


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

    last_down_time = "Could not determine information about the last down time."
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{ISITDOWN_BASE_URL}{root_domain}",
                headers={"User-Agent": USER_AGENT},
                timeout=10.0,
            )
            response.raise_for_status()
    except httpx.HTTPError:
        return "Could not determine the status of the website."
    soup = bs(response.text, "html.parser")
    is_up = soup.find("span", class_="upicon")
    is_down = soup.find("span", class_="downicon")
    tabletrsimple_divs = soup.find_all("div", class_="tabletrsimple")
    if len(tabletrsimple_divs) >= 2:
        last_down_row = tabletrsimple_divs[1]  # NOTE: Brittle - makes assumptions about HTML structure
        if isinstance(last_down_row, Tag):
            last_down_time = get_last_down(last_down_row)
    return get_response_msg(bool(is_down), bool(is_up), last_down_time)


if __name__ == "__main__":
    mcp.run(transport="stdio")
