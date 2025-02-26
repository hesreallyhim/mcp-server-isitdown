import requests
from bs4 import BeautifulSoup as bs
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("isitdown")

# Constants
ISITDOWN_BASE_URL = "https://www.isitdownrightnow.com/check.php?domain="
USER_AGENT = "isitdown-app/0.0.1"

@mcp.tool()
def get_website_status(root_domain: str) -> str:
    try:
        response = requests.get(
            f"{ISITDOWN_BASE_URL}{root_domain}", headers={"User-Agent": USER_AGENT}
        )
        response.raise_for_status()
    except requests.RequestException as e:
        return "Could not determine the status of the website."
    soup = bs(response.text, "html.parser")
    is_up = soup.find("span", class_="upicon")
    if is_up:
        return "The website is up."
    else:
        return "The website is down."

if __name__ == "__main__":
    mcp.run(transport='stdio')
