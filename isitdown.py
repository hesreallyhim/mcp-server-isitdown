import requests
from bs4 import BeautifulSoup as bs
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("isitdown")

# Constants
ISITDOWN_BASE_URL = "https://www.isitdownrightnow.com/check.php?domain="
USER_AGENT = "isitdown-app/0.0.1"

@mcp.tool()
def get_website_status(root_domain: str) -> str:
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
    if is_up:
        return "The website is up."
    elif is_down:
        return "The website is down."
    else:
        return "Could not determine the status of the website."

if __name__ == "__main__":
    mcp.run(transport='stdio')
