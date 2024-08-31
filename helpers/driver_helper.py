from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.remote.webdriver import WebDriver
from webdriver_manager.chrome import ChromeDriverManager

from configs import SETTINGS


class DriverHelper:
    def __init__(self, browser: str = "chrome") -> None:
        self._browser = browser.lower()
        if not self.__is_valid_browser(self._browser):
            raise ValueError(f"Unsupported browser: {self._browser}")

        self._driver = None
        self._option = self.__get_options(self._browser)
        self.__set_up_driver()

    def __is_valid_browser(self, browser: str):
        return browser in SETTINGS.driver.keys()

    def __get_options(self, browser: str):
        options = {"chrome": ChromeOptions}
        option: ChromeOptions = options[browser]()
        arguments = SETTINGS.driver[browser].args

        if SETTINGS.debug and "--headless" in arguments:
            arguments.remove("--headless")
        [option.add_argument(argument) for argument in arguments]

        return option

    def __set_up_driver(self):
        driver_settings = {
            "chrome": {
                "driver": webdriver.Chrome,
                "service": ChromeService,
                "manager": ChromeDriverManager(),
            }
        }

        driver_setting = driver_settings[self._browser]

        self._driver = driver_setting["driver"](
            options=self._option,
            service=driver_setting["service"](driver_setting["manager"].install()),
        )

    @property
    def driver(self) -> WebDriver:
        return self._driver
