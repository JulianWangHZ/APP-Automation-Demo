import time
import pytest
import unittest
import os
from dotenv import dotenv_values
from appium.webdriver import Remote
from appium.options.ios import XCUITestOptions


# TODO: Move the config and options to a separate file
config = dotenv_values(".env")

# Set default values
noReset_bool = config.get('NO_RESET', 'false').lower() == 'true'
platform = config.get('APPIUM_OS')
is_ci = config.get('IS_CI', 'false').lower() == 'true'

# Choose configuration based on environment
if is_ci:
    # BrowserStack configuration
    browserstack_options = {
        'userName': config.get('BROWSERSTACK_USERNAME'),
        'accessKey': config.get('BROWSERSTACK_ACCESS_KEY'),
        'projectName': config.get('BROWSERSTACK_PROJECT_NAME', 'App E2E Tests'),
        'buildName': config.get('BROWSERSTACK_BUILD_NAME', 'GitHub Actions Build'),
        'sessionName': config.get('BROWSERSTACK_SESSION_NAME', 'E2E Test Session'),
        'deviceName': config.get('BROWSERSTACK_DEVICE_NAME', 'iPhone 15 Pro'),
        'osVersion': config.get('BROWSERSTACK_OS_VERSION', '17.5'),
        'interactiveDebugging': True,
        'debug': True,
        'networkLogs': True,
        'appiumLogs': True,
        'deviceLogs': True,
        'video': True
    }

    options = XCUITestOptions()
    options.platform_name = 'iOS'
    options.automation_name = 'XCUITest'
    options.deviceName = config.get(
        'BROWSERSTACK_DEVICE_NAME', 'iPhone 15 Pro')
    options.os_version = config.get('BROWSERSTACK_OS_VERSION', '17.5')
    options.app = config.get('BROWSERSTACK_APP_ID')
    options.set_capability('autoAcceptAlerts', True)
    options.set_capability('autoGrantPermissions', True)
    options.set_capability('bstack:options', browserstack_options)
    options.set_capability('simulatorStartupTimeout', 60000)
    options.set_capability('disableAnimation', False)
    options.set_capability('noReset', noReset_bool)
    appium_server_url = config.get(
        'BROWSERSTACK_HUB_URL', 'https://hub-cloud.browserstack.com/wd/hub')
else:
    # Local configuration
    options = XCUITestOptions()
    options.platform_name = 'ios'
    options.automation_name = 'XCUITest'
    options.set_capability('language', 'zh')
    options.set_capability('locale', 'TW')
    options.set_capability('platformVersion', '17.5')
    options.set_capability('simulatorStartupTimeout', '90000')
    options.set_capability('app', config.get('IOS_APP_PATH'))
    options.set_capability('noReset', noReset_bool)
    options.set_capability('autoAcceptAlerts', True)
    options.set_capability('autoGrantPermissions', True)
    appium_server_url = config.get(
        'APPIUM_SERVER_URL', 'http://127.0.0.1:4723')


class AppiumSetup(unittest.TestCase):
    def setUp(self) -> Remote:
        # Setting global variables
        self.config = config
        self.platform = platform
        self.noReset_bool = noReset_bool

        # Create screenshots directory only in local environment
        if not is_ci:
            screenshots_dir = os.path.join(os.path.dirname(
                os.path.dirname(__file__)), "screenshots")
            os.makedirs(screenshots_dir, exist_ok=True)

        self.driver = Remote(appium_server_url, options=options)
        self.driver.implicitly_wait(int(config.get('IMPLICIT_WAIT', '25')))

        # Save BrowserStack session ID if running in CI
        if is_ci:
            with open('browserstack_session_id.txt', 'w') as f:
                f.write(self.driver.session_id)

        return self.driver

    def tearDown(self) -> None:
        if self.driver:
            self.driver.quit()
            time.sleep(10)


if __name__ == '__main__':
    unittest.main()
