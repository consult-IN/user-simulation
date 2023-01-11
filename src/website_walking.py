import os
import random
import time
from pathlib import Path
import requests

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options

from src.setup_logger import logger


class BrowserAutomation:
    """
    This class offers functionalities to execute user interactions via
    a browsers.
    """

    browser_visible: bool = False

    def __init__(
        self,
        binary_location: Path,
        driver_location: Path,
        browser_visible: bool = False,
    ) -> None:
        """Initializes the class. If the browser should be visible the
        selenium driver is initialized.

        Args:
            binary_location (Path): Location of the binary of the firefox
                browser on your machine
            driver_location (Path): Location of the geckodriver for the
                firefox browser on your machine.
            browser_visible (bool, optional): Switch to either see the
                actions inside the browser or to only see them in the terminal. Defaults to False.
        """
        self.browser_visible = browser_visible
        if self.browser_visible:
            self.__init_driver__(
                binary_location=binary_location, driver_location=driver_location
            )
            self.driver.maximize_window()

    def __init_driver__(self, binary_location: Path, driver_location: Path):
        """Encapsulation of the initializaton of the driver for the firefox browser.

        Args:
            binary_location (Path): Path to the firefox binary (.exe)
            driver_location (Path): Path to the firefox driver (.exe)
        """
        firefox_options = Options()
        firefox_options.binary = binary_location
        service = Service(executable_path=driver_location)
        self.driver = webdriver.Firefox(service=service, options=firefox_options)

    def walk_website(self, urls_available: list[str], link_clicks: int) -> None:
        """
        This function requests a website to crawl all the available links.
        This selection is recursively passed to the next invocation of this function.

        Args:
            urls_available (list[str]): List of available urls on a website
            link_clicks (int): Step counter how many steps through a website should be taken

        Raises:
            Exception: On failed request

        Returns:
            None
        """
        if len(urls_available) == 0:
            logger.info("No further steps possible")
            return

        next_url = random.choices(urls_available, k=1)[0]
        logger.info(f"Next URL to access is: {next_url}")

        logger.info(f"Step: {link_clicks}")

        if self.browser_visible:
            html_text = self.get_webpage_selenium(next_url)
        else:
            html_text = self.get_webpage_request(next_url)
        soup = BeautifulSoup(html_text, "html.parser")

        raw_urls = [
            link_on_website.get("href") for link_on_website in soup.find_all("a")
        ]
        urls_on_website = []
        for link in raw_urls:
            if link is not None:
                if "https" in link:
                    urls_on_website.append(link)
        logger.debug(urls_on_website)

        if link_clicks == 0:
            logger.info("Done")
        else:
            time.sleep(3)
            self.walk_website(urls_on_website, link_clicks=link_clicks - 1)

    def get_webpage_request(self, url_to_fetch_html: str) -> str:
        """Get the html for the webpage via request"""
        reqs = requests.get(url_to_fetch_html)
        if reqs.status_code != 200:
            raise Exception(
                f"The URL: {url_to_fetch_html} was not accessible: {reqs.status_code}"
            )
        return reqs.text

    def get_webpage_selenium(self, url_to_fetch_html: str) -> str:
        """Get the html for the webpage via selenium"""
        self.driver.get(url_to_fetch_html)
        return self.driver.page_source


if __name__ == "__main__":
    START_URL_LIST = ["https://de.wikipedia.org/wiki/Informationssicherheit"]
    SHOW_BROWSER = True

    auto_browser = BrowserAutomation(
        binary_location=os.getenv("USER_SIMULATION_BROWSER_BINARY"),
        driver_location=os.getenv("USER_SIMULATION_DRIVER_LOCATION"),
        browser_visible=SHOW_BROWSER,
    )
    auto_browser.walk_website(START_URL_LIST, link_clicks=3)
