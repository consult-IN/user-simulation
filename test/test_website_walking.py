import os
import pytest
from dotenv import load_dotenv

from src.website_walking import BrowserAutomation


load_dotenv()


@pytest.fixture
def automation_browser_instance():
    return BrowserAutomation(
        binary_location=os.getenv("USER_SIMULATION_BROWSER_BINARY"),
        driver_location=os.getenv("USER_SIMULATION_DRIVER_LOCATION"),
        browser_visible=False,
    )


@pytest.mark.parametrize(
    "test_start_website, test_link_clicks",
    [
        (["https://de.wikipedia.org/wiki/Informationssicherheit"], 2),
        (["https://www.thi.de"], 1),
        (["https://www.bundesregierung.de"], 2),
    ],
)
def test_website_walking_request(
    test_start_website, test_link_clicks, automation_browser_instance
):
    """Test the function walk_websites for different inputs."""
    try:
        automation_browser_instance.walk_website(test_start_website, test_link_clicks)
    except Exception as e:
        assert False, f"Walking websites raised an exception {e}"


@pytest.mark.parametrize(
    "test_start_website, test_link_clicks",
    [
        (["https://de.wikipedia.org/wiki/Informationssicherheit"], 2),
        #(["https://www.thi.de"], 1),
        #(["https://www.bundesregierung.de"], 2),
    ],
)
def test_website_walking_selenium(
    test_start_website, test_link_clicks, automation_browser_instance
):
    """Test the function walk_websites with a visible browser for different inputs."""
    automation_browser_instance.browser_visible = True
    try:
        automation_browser_instance.walk_website(test_start_website, test_link_clicks)
    except Exception as e:
        assert False, f"Walking websites raised an exception {e}"
