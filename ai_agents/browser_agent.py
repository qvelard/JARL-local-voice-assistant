"""
Browser agent module for headless browsing and scraping.
"""
from typing import Optional
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
from services.utils import logger, load_config
import asyncio

class BrowserAgent:
    """
    Uses Playwright to browse and BeautifulSoup to scrape text.
    """
    def __init__(self) -> None:
        self.config = load_config()
        self.timeout: int = self.config.get('browser_agent', {}).get('timeout', 10000)

    async def fetch_text(self, url: str, selector: Optional[str] = None) -> Optional[str]:
        """
        Fetches and scrapes text from a web page.

        Args:
            url (str): The URL to visit.
            selector (Optional[str]): CSS selector to extract specific content.

        Returns:
            Optional[str]: Extracted text, or None if failed.
        """
        try:
            logger.info(f"Launching browser for {url}")
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)
                page = await browser.new_page()
                await page.goto(url, timeout=self.timeout)
                html = await page.content()
                await browser.close()
            soup = BeautifulSoup(html, 'html.parser')
            if selector:
                element = soup.select_one(selector)
                return element.get_text(strip=True) if element else None
            return soup.get_text(separator=' ', strip=True)
        except Exception as e:
            logger.error(f"BrowserAgent failed: {e}")
            return None 