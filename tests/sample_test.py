import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service


@pytest.mark.sanity
def test_the_truth():
    assert True


@pytest.mark.sanity
def test_the_falsehood():
    assert not False


@pytest.mark.regression
@pytest.mark.ui
def test_selenium():
    service = Service("tests/utils/chromedriver/chromedriver")
    service.start()

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=1920x1080")
    chrome_options.binary_location = "/usr/bin/google-chrome-stable"

    driver = webdriver.Remote(service.service_url, desired_capabilities=chrome_options.to_capabilities())

    driver.get("http://www.google.ro")
    lucky_button = driver.find_element_by_css_selector("[name=btnI]")
    lucky_button.click()

    driver.get_screenshot_as_file("capture01.png")

    driver.close()
    service.stop()
