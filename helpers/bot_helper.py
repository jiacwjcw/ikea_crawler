import json
import logging
import time
from typing import Any

from selenium.common.exceptions import InvalidSelectorException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.expected_conditions import (
    alert_is_present,
    element_to_be_clickable,
    presence_of_element_located,
)
from selenium.webdriver.support.ui import Select, WebDriverWait

from configs import SETTINGS


class BotHelper:
    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.driver.implicitly_wait(SETTINGS.implicit_wait)

        self._wait = WebDriverWait(self.driver, SETTINGS.timeout)
        self._action = ActionChains(self.driver)

    def execute_script(self, script: str) -> Any:
        """
        Executes the specified JavaScript code.

        Args:
            script (str): The JavaScript code to execute.

        Returns:
            Any: The return value of the executed JavaScript code.
        """
        logging.debug(f"Executing script: {script}")
        return self.driver.execute_script(script)

    def close(self) -> None:
        """
        Closes the browser window.

        Returns:
            None
        """
        logging.debug("Closing browser window")
        self.driver.quit()

    def set_session_storage(self, content: dict) -> None:
        """
        Sets multiple key-value pairs in the session storage.

        Args:
            content (dict): The key-value pairs to set.

        Returns:
            None
        """
        for key, value in content.items():
            if isinstance(value, dict):
                value = json.dumps(value)
            logging.debug(f"Setting session storage: {key}={value}")
            self.driver.execute_script(f"sessionStorage.setItem('{key}', '{value}');")

    def is_page_load_complete(self) -> bool:
        """
        Checks if the page has finished loading.

        Returns:
            bool: True if the page has finished loading, False otherwise.
        """
        retry_times = 0
        while retry_times <= 5:
            try:
                js_state = self.driver.execute_script("return document.readyState;")
                if js_state == "complete":
                    return True
            except Exception:
                retry_times += 1
                time.sleep(0.5)
        return False

    def wait_page_until_loading(self):
        """
        Waits for the page to finish loading.

        This method waits for the page to finish loading by checking the document.readyState property.
        It will wait for the page to finish loading for a maximum of 30 seconds.
        """
        logging.debug(">>> Wait for page until loading...")
        start_t = time.time()

        self._wait.until(
            lambda driver: self.is_page_load_complete(),
            message="WAIT_PAGE_LOADING_TIMEOUT",
        )

        end_t = time.time()
        elapsedtime = round((end_t - start_t), 3)
        logging.debug("<<< Wait page loading spend time %s", elapsedtime)

    def wait_visit_to_url(self, url: str):
        """
        Waits for the driver to visit the specified URL.

        Args:
            url (str): The URL to wait for.

        Raises:
            TimeoutException: If the driver does not visit the URL within the specified timeout.

        Returns:
            None
        """
        logging.debug(f">>> Wait for visit to url: {url}...")
        self._wait.until(
            lambda driver: self.driver.current_url == url,
            message="WAIT_VISIT_URL_TIMEOUT",
        )
        logging.debug(f"<<< Wait visit to url: {url} completed")

    def wait_element_dispear(self, locator: tuple[By, str]):
        """
        Waits for the specified element to disappear from the page.

        Args:
            locator (tuple[By, str]): The locator of the element to wait for.

        Raises:
            TimeoutException: If the element does not disappear within the specified timeout.

        Returns:
            None
        """
        logging.debug(f"Wait for element {locator} to disappear")
        self._wait.until(
            lambda driver: len(self.find_all(locator)) == 0,
            message="WAIT_ELEMENT_DISAPPEAR_TIMEOUT",
        )

    def wait_element_appear(self, locator: tuple[By, str]):
        """
        Waits for the specified element to appear on the page.

        Args:
            locator (tuple[By, str]): The locator of the element to wait for.

        Raises:
            TimeoutException: If the element does not appear within the specified timeout.

        Returns:
            None
        """
        logging.debug(f"Wait for element {locator} to appear")
        self._wait.until(
            lambda driver: len(self.find_all(locator)) > 0,
            message="WAIT_ELEMENT_APPEAR_TIMEOUT",
        )

    def select_option(self, select_locator: tuple[By, str], option: str) -> None:
        """
        Selects an option from a dropdown list.

        Args:
            select_locator (tuple[By, str]): The locator of the dropdown list.
            option (str): The option to select.

        Returns:
            None
        """
        logging.debug(f"Selecting option {option} from dropdown list")
        select = (
            Select(select_locator)
            if isinstance(select_locator, WebElement)
            else Select(self.find(select_locator))
        )
        select.select_by_visible_text(option)

    def select_option_index(
        self, select_locator: tuple[By, str], option_index: int
    ) -> None:
        """
        Selects an option from a dropdown list.

        Args:
            select_locator (tuple[By, str]): The locator of the dropdown list.
            option_index (int): The index of the option to select.

        Returns:
            None
        """
        logging.debug(f"Selecting option {option_index} from dropdown list")
        select = Select(self.find(select_locator))
        select.select_by_index(option_index)

    def get_current_url(self) -> str:
        """
        Returns the current URL of the page.

        Returns:
            str: The current URL of the page.
        """
        logging.debug("Getting current URL")
        return self.driver.current_url

    def get_window_count(self) -> int:
        """
        Returns the number of windows currently open.

        Returns:
            int: The number of windows currently open.
        """
        logging.debug("Getting window count")
        return len(self.driver.window_handles)

    def get_text(self, locator: tuple[By, str]) -> str:
        """
        Returns the text of the specified element.

        Args:
            locator (tuple[By, str]): The locator of the element.

        Returns:
            str: The text of the element.
        """
        logging.debug(f"Getting text from element: {locator[1]}")
        return self.find(locator).text

    def get_value(self, locator: tuple[By, str]) -> Any:
        """
        Returns the value of the specified element.

        Args:
            locator (tuple[By, str]): The locator of the element.

        Returns:
            str: The value of the element.
        """
        logging.debug(f"Getting value from element: {locator[1]}")
        return self.find(locator).get_attribute("value")

    def get_src(self, locator: tuple[By, str]) -> Any:
        """
        Returns the image src value of the specified element.

        Args:
            locator (tuple[By, str]): The locator of the element.

        Returns:
            str: The value of the element.
        """
        logging.debug(f"Getting img src from element: {locator[1]}")
        return self.find(locator).get_attribute("src")

    def adjust_window_size(self, width: int, height: int) -> None:
        """
        Adjusts the window size to the specified width and height.

        Args:
            width (int): The width of the window.
            height (int): The height of the window.

        Returns:
            None
        """
        logging.debug(f"Adjusting window size to {width}x{height}")
        self.driver.set_window_size(width, height)

    def open_new_window(self) -> None:
        """
        Opens a new tab and switches to it.

        This method opens a new tab in the browser window and switches the driver's focus to the newly opened tab.

        Returns:
            None
        """
        logging.debug("Opening new window")
        self.driver.switch_to.new_window("window")

    def maximize_window(self) -> None:
        """
        Maximizes the window.

        Returns:
            None
        """
        logging.debug("Maximizing window")
        self.driver.maximize_window()

    def switch_window(self, index: int) -> None:
        """
        Switches the driver's focus to the window with the specified index.

        Args:
            index (int): The index of the window to switch to.

        Returns:
            None
        """
        logging.debug(f"Switching to window {index}")
        self.driver.switch_to.window(self.driver.window_handles[index])

    def visit(self, url: str) -> None:
        """Visits the specified URL.

        Args:
            url (str): The URL to visit.

        Returns:
            None
        """
        logging.debug(f"Visiting URL: {url}")
        self.driver.get(url)
        self.wait_page_until_loading()

    def click(self, locator: tuple[By, str], message: str = "") -> None:
        """Clicks the specified element.

        Args:
            locator (tuple[By, str]): The locator of the element to click.
            message (str): The message to log when clicking the element.

        Returns:
            None
        """
        logging.debug(f"Clicking element: {message}")
        element = self.find(locator)
        self._wait.until(element_to_be_clickable(element)).click()

    def input(self, locator: tuple[By, str], text: str) -> None:
        """Inputs the specified text into the specified element.

        Args:
            locator (tuple[By, str]): The locator of the element to input text into.
            text (str): The text to input.

        Returns:
            None
        """
        logging.debug(f"Inputting text: {text}")
        self.find(locator).send_keys(text)

    def scroll_to(self, element: WebElement, message: str = "") -> None:
        """Scrolls to the specified element.

        Args:
            element (WebElement): The element to scroll to.
            message (str): The message to log.

        Returns:
            None
        """
        logging.debug(f"Scrolling to element: {message}")
        self._action.move_to_element(element).perform()

    def find(self, locator: tuple[By, str]) -> WebElement:
        """
        Finds and returns a web element based on the given locator.

        Args:
            locator (tuple[By, str]): The locator used to find the web element.

        Returns:
            WebElement: The web element found.

        Raises:
            InvalidSelectorException: If the locator is invalid and cannot find the element.
        """
        logging.debug(f"Finding element: {locator}")
        try:
            element = self._wait.until(presence_of_element_located(locator))
            return element
        except InvalidSelectorException:
            logging.error("Could not find element")
            raise

    def find_all(self, locator: tuple[By, str]) -> list[WebElement]:
        """
        Finds and returns a list of web elements based on the given locator.

        Args:
            locator (tuple[By, str]): The locator used to find the web elements.

        Returns:
            list[WebElement]: The list of web elements found.

        """
        logging.debug(f"Finding all elements: {locator}")
        try:
            return self.driver.find_elements(*locator)
        except InvalidSelectorException:
            logging.error(f"Invalid selector: {locator}")
            return []

    def set_slider_value(self, slider: WebElement, value: float) -> None:
        """
        Sets the value on a horizontal slider

        Args:
            slider (WebElement): The slider element.
                The WebElement representing the slider.
            value (float): The desired value.
                The value to set on the slider.

        Returns:
            None
        """
        min_value = float(slider.get_attribute("min"))
        max_value = float(slider.get_attribute("max"))
        slider_h = slider.size["height"]
        slider_w = slider.size["width"]
        x_offset = int(value * slider_w / (max_value - min_value))
        y_offset = slider_h / 2

        if value < min_value or value > max_value:
            raise ValueError(
                f"Value {value} is out of range [{min_value}, {max_value}]"
            )

        logging.debug(f"Swiping slider to value: {value}")
        self._action.move_to_element_with_offset(
            slider, x_offset, y_offset
        ).click().perform()

    def screenshot(self, path: str) -> None:
        """
        Takes a screenshot of the current page and saves it to the specified path.

        Args:
            path (str): The path to save the screenshot to.

        Returns:
            None
        """
        logging.debug(f"Taking screenshot: {path}")
        self.driver.save_screenshot(path)

    def previous_page(self) -> None:
        """
        Navigates to the previous page in the browser history.

        Returns:
            None
        """
        logging.debug("Navigating to previous page")
        self.driver.back()

    def next_page(self) -> None:
        """
        Navigates to the next page in the browser history.

        Returns:
            None
        """
        logging.debug("Navigating to next page")
        self.driver.forward()

    def alert_present(self) -> bool:
        """
        Checks if an alert is present.

        Returns:
            bool: True if an alert is present, False otherwise.
        """
        logging.debug("Checking if alert is present")
        return self._wait.until(alert_is_present())

    def accept_alert(self) -> None:
        """
        Accepts the alert.

        Returns:
            None
        """
        logging.debug("Accepting alert")
        self.driver.switch_to.alert.accept()

    def dismiss_alert(self) -> None:
        """
        Dismisses the alert.

        Returns:
            None
        """
        logging.debug("Dismissing alert")
        self.driver.switch_to.alert.dismiss()
