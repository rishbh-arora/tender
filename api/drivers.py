from selenium import webdriver
from twocaptcha import TwoCaptcha
from tender.settings.base import SELENIUM_HEADLESS, DOWNLOAD_DIRECTORY
import os

class Selenium_Driver:
    _driver = None

    def __init__(self):
        raise Exception("This class should not be instantiated")

    @classmethod
    def get_driver(self):
        if not self._driver:
            options = webdriver.ChromeOptions()
            download_dir = DOWNLOAD_DIRECTORY
            options.add_experimental_option("prefs", {
            "download.default_directory": download_dir,  # Set your custom download path here
            "download.prompt_for_download": False,       # No download prompt
            "download.directory_upgrade": True,
            "safebrowsing.enabled": True
        })

            binary_location = os.getenv("CHROME_BINARY_PATH")
            assert binary_location, "Set the Chrome binary path in the CHROME_BINARY_PATH environment variable"
            options.binary_location = os.getenv("CHROME_BINARY_PATH")
            options.headless = SELENIUM_HEADLESS
            self._driver = webdriver.Chrome(options=options)
        return self._driver
    
class Captcha():
    _solver = None

    def __init__(self):
        raise Exception("This class should not be instantiated")

    @classmethod
    def get_solver(self):
        if not self._solver:
            api_key = os.environ.get("CAPTCHA_API_KEY")
            assert api_key, "Set the 2Captcha API key in the CAPTCHA_API_KEY environment variable"
            self._solver = TwoCaptcha(api_key)
        return self._solver
