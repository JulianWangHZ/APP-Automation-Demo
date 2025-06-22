import pytest
import os
import time
import allure
import sys

from datetime import datetime
from utils.logger import logger

def is_running_in_ci():
    """Check if running in CI environment"""
    return os.getenv('CI') == 'true'

def pytest_configure(config):
    """
    Create screenshot directory and set up logging
    """
    # Create screenshot directory only in local environment
    if not is_running_in_ci():
        screenshots_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "screenshots")
        if not os.path.exists(screenshots_dir):
            os.makedirs(screenshots_dir)
            print(f"Created screenshots directory at {screenshots_dir}")
    
    # Set up logging
    log_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "logs")
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    log_file = os.path.join(log_dir, "test_execution.log")
    
    # Ensure log directory and file exist
    if not os.path.exists(log_file):
        with open(log_file, 'w') as f:
            f.write('')
    
    print(f"Logging configured. Log file: {log_file}")

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Take screenshot on test failure and add detailed error handling
    """
    # Execute test
    outcome = yield
    report = outcome.get_result()
    
    # Only take screenshot on test failure
    if report.when == "call" and report.failed:
        try:
            print(f"Test {item.name} failed - attempting to take screenshot")
            logger.info(f"Test {item.name} failed - attempting to take screenshot")

            # Get driver instance from request
            request = item._request
            if not request:
                error_msg = f"Test {item.name} failed - request object not found"
                print(error_msg)
                logger.error(error_msg)
                return

            driver = request.getfixturevalue("driver")
            if not driver:
                error_msg = f"Test {item.name} failed - driver instance not found"
                print(error_msg)
                logger.error(error_msg)
                return

            if not hasattr(driver, 'save_screenshot'):
                error_msg = f"driver instance does not support screenshot functionality"
                print(error_msg)
                logger.error(error_msg)
                return

            # Extract relevant part of the test name
            test_name = item.name
            if test_name.startswith('test_'):
                test_name = test_name[5:]  # Remove "test_" prefix

            if is_running_in_ci():
                # In CI environment, save screenshot to artifacts directory
                artifacts_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "artifacts")
                os.makedirs(artifacts_dir, exist_ok=True)

                timestamp = datetime.now().strftime("%Y%m%d_%H%M")
                screenshot_name = f"{test_name}_{timestamp}.png"
                screenshot_path = os.path.join(artifacts_dir, screenshot_name)

                # Save screenshot
                driver.save_screenshot(screenshot_path)
                success_msg = f"Screenshot saved to artifacts: {screenshot_path}"

                # Also attach to Allure
                with open(screenshot_path, 'rb') as f:
                    allure.attach(
                        f.read(),
                        name=f"{test_name}",
                        attachment_type=allure.attachment_type.PNG
                    )
            else:
                # In local environment, save to screenshots directory
                screenshots_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "screenshots")
                os.makedirs(screenshots_dir, exist_ok=True)

                timestamp = datetime.now().strftime("%Y%m%d_%H%M")
                screenshot_name = f"{test_name}_{timestamp}.png"
                screenshot_path = os.path.join(screenshots_dir, screenshot_name)

                # Save screenshot
                driver.save_screenshot(screenshot_path)
                success_msg = f"Screenshot saved: {screenshot_path}"

                # Also attach to Allure for local runs
                with open(screenshot_path, 'rb') as f:
                    allure.attach(
                        f.read(),
                        name=f"{test_name}",
                        attachment_type=allure.attachment_type.PNG
                    )

            print(success_msg)
            logger.info(success_msg)

            # Add failure information to log
            if hasattr(report, 'longrepr'):
                # get the first line of the error message
                error_str = str(report.longrepr)
                # get the full error message
                test_failure = f"FAILED {item.nodeid} - {error_str.split('E       ')[1].strip()}"
                error_msg = f"Test failure: {test_failure}"
                print(error_msg)
                logger.error(error_msg)

        except Exception as e:
            # only keep the first line of the error message
            error_msg = f"Screenshot process error: {str(e)}"
            print(error_msg)
            logger.error(error_msg)
