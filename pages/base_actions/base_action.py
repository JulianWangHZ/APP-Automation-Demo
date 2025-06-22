import time
from typing import Tuple, Union
from appium.webdriver.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.actions import interaction
from selenium.webdriver.common.actions.pointer_input import PointerInput
from selenium.webdriver.common.actions.action_builder import ActionBuilder

class BaseActions:
    def __init__(self, driver: WebDriver, default_timeout: int = 10):
        """
        Args:
            driver: WebDriver instance
            default_timeout: default timeout (seconds)
        """
        self.driver = driver
        self.wait = WebDriverWait(driver, default_timeout)
        self.default_timeout = default_timeout

    def find_element(self, locator_type: str, locator_value: str, timeout: int = None):
        """
        Use explicit wait to find element and return

        Args:
            locator_type: Locator type
            locator_value: Locator value
            timeout: Optional waiting time, if not specified, use default value

        Returns:
            WebElement: Found element

        Raises:
            TimeoutException: If the element is not found within the specified time
        """
        if timeout is None:
            timeout = self.default_timeout

        max_attempts = 3
        for attempt in range(max_attempts):
            try:
                return WebDriverWait(self.driver, timeout).until(
                    EC.presence_of_element_located((locator_type, locator_value))
                )
            except (TimeoutException, StaleElementReferenceException) as e:
                if attempt == max_attempts - 1:
                    raise TimeoutException(
                        f"Element ({locator_type}={locator_value}) not found after {max_attempts} attempts"
                    ) from e
                time.sleep(1)
                return None
        return None

    def is_element_visible(self, locator_type: str, locator_value: str, timeout: int = None):
        """
        Check if the element exists and is visible
        """
        if timeout is None:
            timeout = self.default_timeout

        max_attempts = 3
        for attempt in range(max_attempts):
            try:
                WebDriverWait(self.driver, timeout).until(
                    EC.visibility_of_element_located((locator_type, locator_value))
                )
                return True
            except (TimeoutException, StaleElementReferenceException):
                if attempt == max_attempts - 1:
                    return False
                time.sleep(1)
        return False

    def is_element_present(self, locator_type: str, locator_value: str) -> bool:
        """
        Check if the element exists
        """
        try:
            self.driver.find_element(locator_type, locator_value)
            return True
        except NoSuchElementException:
            return False

    def click_element(self, locator_type: str, locator_value: str, timeout: int = None):
        """
        Click the clickable element
        """
        if timeout is None:
             timeout = self.default_timeout

        max_attempts = 3
        for attempt in range(max_attempts):
            try:
                element = WebDriverWait(self.driver, timeout).until(
                    EC.element_to_be_clickable((locator_type, locator_value))
                )
                element.click()
                return
            except (TimeoutException, StaleElementReferenceException) as e:
                if attempt == max_attempts - 1:
                    raise TimeoutException(
                        f"Element ({locator_type}={locator_value}) not clickable after {max_attempts} attempts"
                    ) from e
                time.sleep(1)

    def click_if_exists(self, locator_type: str, locator_value: str) -> bool:
        """
        If the element exists, click it
        """
        if self.is_element_visible(locator_type, locator_value):
            self.click_element(locator_type, locator_value)
            return True
        return False

    def send_keys_to_element(self, locator_type: str, locator_value: str, text: str):
        """
        Send keyboard input to the specified element
        """
        element = self.find_element(locator_type, locator_value)
        # element.clear()
        element.send_keys(text)
        return element

    def clear_text(self, locator_type: str, locator_value: str):
        """
        Clear the text of the specified element
        """
        element = self.find_element(locator_type, locator_value)
        element.clear()

    def get_element_text(self, locator_type: str, locator_value: str) -> str:
        """
        Get the text of the specified element
        """
        element = self.find_element(locator_type, locator_value)
        return element.text

    def wait_for_element_visible(self, locator_type: str, locator_value: str, timeout: int = 30):
        """
        Quickly check if the element is visible
        If the element does not exist, return False immediately

        Args:
            locator_type: Locator type
            locator_value: Locator value
            timeout: Maximum waiting time (seconds)

        Returns:
            WebElement: If the element is visible, return WebElement, otherwise return False

        Raises:
            TimeoutException: If the element is not visible within the specified time
        """
        try:
            self.driver.implicitly_wait(0)
            wait = WebDriverWait(self.driver, timeout)
            return wait.until(
                EC.visibility_of_element_located((locator_type, locator_value))
            )
        except NoSuchElementException:
            return False
        except TimeoutException:
            actual_timeout = timeout
            raise TimeoutException(
                f"Element ({locator_type}={locator_value}) still not visible after {actual_timeout} seconds"
            )

    def wait_for_element_clickable(self, locator_type: str, locator_value: str) -> bool:
        """
        Wait until the specified element is clickable
        """
        try:
            self.wait.until(
                EC.element_to_be_clickable((locator_type, locator_value))
            )
            return True
        except TimeoutException:
            return False

    def verify_element_text(self, locator_type: str, locator_value: str, expected_text: str) -> bool:
        """
        Verify the text of the specified element
        """
        actual_text = self.get_element_text(locator_type, locator_value)
        return actual_text == expected_text

    def scroll_to_element(self, locator_type: str, locator_value: str, scroll_container: str = "//XCUIElementTypeScrollView", max_swipes: int = 5, timeout: float = 0.5) -> bool:
        """
        Scroll vertically in the UIScrollView until the specified element is found

        Args:
            locator_type: Locator type (e.g. AppiumBy.ID)
            locator_value: Locator value
            scroll_container: ScrollView container xpath, default is "//XCUIElementTypeScrollView"
            max_swipes: Maximum number of swipes, default is 5
            timeout: Waiting time after each swipe (seconds), default is 0.5 seconds

        Returns:
            bool: If the element is found and visible, return True, otherwise return False
        """
        self.driver.implicitly_wait(0)
        try:
            element = self.driver.find_element(locator_type, locator_value)
            if element.is_displayed():
                return True
        except (NoSuchElementException, StaleElementReferenceException):
            pass

        try:
            # Find UIScrollView container
            container = self.driver.find_element(By.XPATH, scroll_container)
            container_rect = container.rect

            # Use the size and position of the container
            start_y = container_rect['y'] + int(container_rect['height'] * 0.8)
            end_y = container_rect['y'] + int(container_rect['height'] * 0.2)
            start_x = container_rect['x'] + (container_rect['width'] // 2)

        except NoSuchElementException:
            print("Can't find the UIScrollView container")
            # When the container is not found, use the size of the entire screen
            screen_width, screen_height = self.get_screen_size()
            start_y = int(screen_height * 0.8)
            end_y = int(screen_height * 0.2)
            start_x = screen_width // 2

        for _ in range(max_swipes):
            self.swipe(start_x, start_y, start_x, end_y)
            time.sleep(timeout)
            try:
                element = self.driver.find_element(locator_type, locator_value)
                if element.is_displayed():
                    return True
            except (NoSuchElementException, StaleElementReferenceException):
                continue

        return False

    def swipe(self, start_x: int, start_y: int, end_x: int, end_y: int, duration: int = 800):
        """
        Execute swipe gesture
        """
        self.driver.swipe(start_x, start_y, end_x, end_y, duration)

    def tap(self, x_ratio: float, y_ratio: float):
        """
        Use W3C Actions API to tap on the screen at the specified ratio position

        Args:
            x_ratio (float): x coordinate of the screen ratio (0.0 ~ 1.0)
            y_ratio (float): y coordinate of the screen ratio (0.0 ~ 1.0)
        Ex.
        self.common_actions.tap(0.5, 0.9)
        """
        size = self.get_screen_size()
        x = int(size[0] * x_ratio)
        y = int(size[1] * y_ratio)
        actions = ActionChains(self.driver)
        pointer = PointerInput(interaction.POINTER_TOUCH, "touch")

        actions.w3c_actions = ActionBuilder(self.driver, mouse=pointer)
        actions.w3c_actions.pointer_action.move_to_location(x, y)
        actions.w3c_actions.pointer_action.pointer_down()
        actions.w3c_actions.pointer_action.pause(0.1)
        actions.w3c_actions.pointer_action.pointer_up()
        actions.perform()

    def hide_keyboard(self):
        """
        Hide keyboard
        """
        self.driver.hide_keyboard()

    def get_screen_size(self) -> Tuple[int, int]:
        """
        Get screen size
        """
        size = self.driver.get_window_size()
        return size['width'], size['height']

    def wait_for_element_present(self, locator_type: str, locator_value: str, timeout: int = 30) -> bool:
        """
        Wait for the element to appear in the DOM and be visible

        Args:
            locator_type: Locator type
            locator_value: Locator value
            timeout: Maximum waiting time (seconds)

        Returns:
            bool: If the element appears and is visible, return True, otherwise return False
        """
        try:
            # Temporarily disable implicit wait to avoid conflict with explicit wait
            self.driver.implicitly_wait(0)
            wait = WebDriverWait(self.driver, timeout)
            wait.until(
                EC.visibility_of_element_located((locator_type, locator_value))
            )
            return True
        except TimeoutException:
            return False

    def wait_for_element_disappear(self, locator_type: str, locator_value: str, timeout: int = 30) -> Union[WebElement, bool]:
        """
        Quickly check if the element exists and is visible
        If the element does not exist, return True immediately

        Args:
            locator_type: Locator type
            locator_value: Locator value
            timeout: Maximum waiting time (seconds)

        Returns:
            Union[WebElement, bool]: If the element disappears, return True, otherwise return False

        Raises:
            TimeoutException: If the element does not disappear within the specified time
        """
        try:
            self.driver.implicitly_wait(0)
            return WebDriverWait(self.driver, timeout).until(EC.invisibility_of_element_located((locator_type, locator_value)))
        except NoSuchElementException:
            return True
        except TimeoutException:
            raise TimeoutException(f"Element ({locator_type}={locator_value}) still visible after {timeout} seconds")

    def scroll_to_element_left(self, locator_type: str, locator_value: str, scroll_container: str = "//XCUIElementTypeCollectionView", max_swipes: int = 3, timeout: float = 0.5) -> bool:
        """
        Scroll to the left in the specified UICollectionView until the specified element is found

        Args:
            locator_type: Locator type (e.g. AppiumBy.ID)
            locator_value: Locator value
            scroll_container: CollectionView container xpath, default is "//XCUIElementTypeCollectionView"
            max_swipes: Maximum number of swipes, default is 3
            timeout: Waiting time after each swipe (seconds), default is 0.5 seconds

        Returns:
            bool: If the element is found and visible, return True, otherwise return False
        """

        self.driver.implicitly_wait(0)
        try:
            element = self.driver.find_element(locator_type, locator_value)
            if element.is_displayed():
                return True
        except (NoSuchElementException, StaleElementReferenceException):
            pass

        # Get the position and size of the UICollectionView
        try:
            collection_view = self.driver.find_element(By.XPATH, scroll_container)
            container_rect = collection_view.rect

            # Get the coordinates and size of the scroll container
            container_x = container_rect['x']
            container_y = container_rect['y']
            container_width = container_rect['width']
            container_height = container_rect['height']

            # Calculate the starting and ending points of the swipe
            start_x = container_x + int(container_width * 0.8)  # 80% of the container width
            end_x = container_x + int(container_width * 0.2)    # 20% of the container width
            swipe_y = container_y + (container_height // 2)     # Vertical center of the container

            for _ in range(max_swipes):
                self.swipe(start_x, swipe_y, end_x, swipe_y)
                time.sleep(timeout)
                try:
                    element = self.driver.find_element(locator_type, locator_value)
                    if element.is_displayed():
                        return True
                except (NoSuchElementException, StaleElementReferenceException):
                    continue

        except NoSuchElementException:
            print("Can't find the specified UICollectionView")
            return False

        return False

    def get_element_attribute(self, locator_type: str, locator_value: str, attribute: str) -> str:
        """
        Get the attribute value of the specified element

        Args:
            locator_type: Locator type
            locator_value: Locator value
            attribute: Attribute name

        Returns:
            str: Attribute value
        """
        element = self.find_element(locator_type, locator_value)
        return element.get_attribute(attribute)


    def get_element_location(self, locator_type: str, locator_value: str) -> Tuple[int, int]:
        """
        Get the location of the specified element

        Args:
            locator_type: Locator type
            locator_value: Locator value

        Returns:
            Tuple[int, int]: The x, y coordinates of the element
        """
        element = self.find_element(locator_type, locator_value)
        location = element.location
        return location['x'], location['y']

    def get_element_size(self, locator_type: str, locator_value: str) -> Tuple[int, int]:
        """
        Get the size of the specified element

        Args:
            locator_type: Locator type
            locator_value: Locator value

        Returns:
            Tuple[int, int]: The width and height of the element
        """
        element = self.find_element(locator_type, locator_value)
        size = element.size
        return size['width'], size['height']

    def is_toggle_on(self, locator_type: str, locator_value: str) -> bool:
        """
        Determine the state of the toggle based on the value attribute
        value="1" means ON, value="0" means OFF (iOS UISwitch)
        """
        try:
            element = self.find_element(locator_type, locator_value)
            value = element.get_attribute("value")
            print(f"Toggle value attribute: {value}")
            return value == "1"
        except (NoSuchElementException, TimeoutException):
            return False

    def toggle_switch(self, locator_type: str, locator_value: str, should_be_on: bool = True) -> bool:
        """
        Toggle the state of the toggle

        Args:
            locator_type: Locator type
            locator_value: Locator value
            should_be_on: The expected state, True means ON, False means OFF

        Returns:
            bool: If the state is switched to the expected state, return True, otherwise return False
        """
        try:
            current_state = self.is_toggle_on(locator_type, locator_value)
            if current_state != should_be_on:
                self.click_element(locator_type, locator_value)
                # Wait for the state to change
                time.sleep(0.5)
                return self.is_toggle_on(locator_type, locator_value) == should_be_on
            return True
        except (NoSuchElementException, TimeoutException):
            return False

    def toggle_switch_state(self, locator_type: str, locator_value: str, should_be_on: bool = True) -> bool:
        """
        Toggle the state of the toggle
        - Force the toggle to switch to the specified state (should_be_on)
        - If the current state is different from the expected state, switch it
        - If the current state is the same as the expected state, keep it unchanged

        Example:
        # Switch to ON state
        common_actions.toggle_switch_state(By.ID, "my_toggle", should_be_on=True)
        # Output:
        # Toggle Current State: Off
        # Toggle New State: On
        # Toggle switched to On state successfully

        # Switch to OFF state
        common_actions.toggle_switch_state(By.ID, "my_toggle", should_be_on=False)
        # Output:
        # Toggle Current State: On
        # Toggle New State: Off
        # Toggle switched to Off state successfully

        Args:
            locator_type: Locator type
            locator_value: Locator value
            should_be_on: The expected state, True means ON, False means OFF

        Returns:
            bool: If the state is switched to the expected state, return True, otherwise return False
        """
        try:
            current_state = self.is_toggle_on(locator_type, locator_value)
            print(f"Toggle Current State:{'On' if current_state else 'Off'}")
            
            # If the current state is different from the expected state, switch it
            if current_state != should_be_on:
                print(f"Switching toggle to {'On' if should_be_on else 'Off'} state")
                
                max_attempts = 3
                for attempt in range(max_attempts):
                    try:
                        element = self.wait.until(
                            EC.element_to_be_clickable((locator_type, locator_value))
                        )
                        element.click()
                        time.sleep(1) 
                        
                        new_state = self.is_toggle_on(locator_type, locator_value)
                        print(f"Toggle New State (Attempt {attempt + 1}):{'On' if new_state else 'Off'}")
                        
                        if new_state == should_be_on:
                            print(f"Toggle switched to {'On' if should_be_on else 'Off'} state successfully")
                            return True
                            
                        if attempt < max_attempts - 1:
                            print(f"Attempt {attempt + 1} failed, trying again...")
                            time.sleep(1)  # Wait for a moment and try again
                            
                    except Exception as e:
                        print(f"Error during attempt {attempt + 1}: {str(e)}")
                        if attempt < max_attempts - 1:
                            time.sleep(1)
                            continue
                
                print(f"Warning: Failed to switch toggle to {'On' if should_be_on else 'Off'} state after {max_attempts} attempts")
                return False
            else:
                print(f"Toggle is already {'On' if should_be_on else 'Off'}, no need to switch")
                return True
            
        except NoSuchElementException:
            print(f"Error: Toggle element not found ({locator_type}={locator_value})")
            return False
        except TimeoutException:
            print(f"Error: Waiting for Toggle element timeout ({locator_type}={locator_value})")
            return False
        except Exception as e:
            print(f"Error: Unknown error occurred while switching toggle state: {str(e)}")
            return False

    def get_element_count(self, locator_type: str, locator_value: str) -> int:
        """
        Find all matching elements and return the number
        """
        elements = self.driver.find_elements(locator_type, locator_value)
        return len(elements)