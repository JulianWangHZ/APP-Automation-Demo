import os
import pytest
import subprocess
import time
import re
import traceback
from dotenv import load_dotenv

# load .env file
load_dotenv()

from subprocess import run
from datetime import datetime

from setup import AppiumSetup
from utils.logger import logger
from pages.base_actions.base_action import BaseActions
from utils.initial_setup import setup_flow
from utils.permission_handler import handle_permission_dialogs
from screenshot_hooks import pytest_runtest_makereport


test_summary = []

def pytest_addoption(parser):
    """Add custom command line options"""
    parser.addoption(
        "--skipsetup",
        action="store_true",
        default=False,
        help="Skip app reinstallation and setup process"
    )
    
def handle_failed_test_reset(item, driver):
    """handle the failed test case to reset the app status"""
    print("test failed, starting to reset app status...")
    try:
        if driver:
            is_ci = os.getenv('IS_CI', 'false').lower() == 'true'

            if is_ci:
                try:
                    app_id = get_app_id()
                    
                    print(f"Terminate iOS app: {app_id}")
                    driver.terminate_app(app_id)
                    print("iOS app terminated successfully")
                    
                    print(f"Restart iOS app: {app_id}")
                    driver.activate_app(app_id)
                    print("iOS app restarted successfully")
                    
                except Exception as webdriver_error:
                    print(f"BrowserStack app reset failed: {webdriver_error}")
                    print("Cannot reset app in BrowserStack environment, continuing with next test")
            
            else:
                # Local environment 
                app_id = get_app_id()
                app_path = os.getenv('IOS_APP_PATH')
                
                if app_path:
                    print(f"Uninstall iOS app: {app_id}")
                    run(['xcrun', 'simctl', 'uninstall', 'booted', app_id], check=True)
                    print("iOS app uninstalled successfully")
                    
                    print(f"Reinstall iOS app: {app_path}")
                    run(['xcrun', 'simctl', 'install', 'booted', app_path], check=True)
                    print("iOS app reinstalled successfully")
                    
                    # Re-execute setup_flow for onboarding
                    try:
                        setup_flow()
                        print("Re-login successfully")
                    except Exception as setup_error:
                        print(f"Re-login failed: {setup_error}")
                else:
                    print("IOS_APP_PATH environment variable is not set, cannot reinstall")
            
            print("iOS app reset completed")
        else:
            print("No driver found, cannot reset app status")
    except Exception:
        print(traceback.format_exc())


def get_app_id():
    """Get the app bundle ID from environment variables"""
    return os.getenv('IOS_APP_BUNDLE_ID', 'com.rafaelsoh.dime')


@pytest.fixture(scope="session", autouse=True)
def driver(request):
    """Create driver and reinstall App before each test session"""
    print("\n=========== Session Start: Creating driver and preparing environment ===========")

    # Get environment variables
    platform = os.getenv('APPIUM_OS').lower()
    print(f"Current platform: {platform}")

    # Check if the skipsetup option is enabled
    skip_setup = request.config.getoption("--skipsetup")

    # Check if the previous test failed
    previous_test_failed = False
    if hasattr(request.session, 'previous_test_failed'):
        previous_test_failed = request.session.previous_test_failed

    # --- App cleanup process ---
    if not skip_setup:  # Only reinstall if skipsetup is not enabled
        try:
            print("Cleaning iOS application...")
            app_path = os.getenv('IOS_APP_PATH')
            app_id = get_app_id()
            
            if app_path:
                run(['xcrun', 'simctl', 'uninstall', 'booted', app_id], check=True)
                run(['xcrun', 'simctl', 'install', 'booted', app_path], check=True)
            else:
                print("Please set IOS_APP_PATH in your .env")
        except Exception as e:
            print(f"App cleanup failed: {e}")
    else:
        print("Skipping app reinstallation process due to --skipsetup flag")

    # --- Create driver ---
    appium_setup = AppiumSetup()
    driver = appium_setup.setUp()

    # Check if there are tests with the 'onboarding' marker in the current test collection
    has_onboarding_tag = False
    for item in request.session.items:
        if item.get_closest_marker('onboarding'):
            has_onboarding_tag = True
            break

    # --- Onboarding process ---
    if has_onboarding_tag or skip_setup:
        print("Found tests with onboarding marker or skipsetup flag, skipping onboarding process")
    else:
        print("Executing onboarding process...")
        try:
            setup_flow()
            print("Initialization process completed")
        except Exception as e:
            print(f"Onboarding process failed: {e}")

    yield driver

    # --- Cleanup at the end of the session ---
    appium_setup.tearDown()
    print("\n=========== Session End ===========")

def pytest_configure(config):
    """Configure test collection and markers"""

    if not config.args:
        logger.info("Configuring test collection for iOS platform")
        config.args = ['tests/steps/ios']


def pytest_bdd_apply_tag(tag, function):
    if tag == 'order':
        marker = pytest.mark.run(order=int(function.__doc__.split('order=')[1]))
        marker(function)
        return True
    return None


def pytest_collection_modifyitems(items):
    """Filter tests for iOS platform"""
    logger.info("Running tests for iOS platform")

    filtered_items = []
    for item in items:
        file_path = str(item.fspath)
        if '/ios/' in file_path:
            filtered_items.append(item)

    items[:] = filtered_items
    logger.info(f"Filtered test count: {len(filtered_items)}")


@pytest.fixture
def base_actions(driver):
    return BaseActions(driver)


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    # record test result
    if report.when == "call":  # only record test result when test is running
        # set the flag for the next test to reinstall the app
        if hasattr(item.session, 'previous_test_failed'):
            item.session.previous_test_failed = report.failed
        else:
            setattr(item.session, 'previous_test_failed', report.failed)

        if report.failed:
            # handle the failed test case to reset the app
            driver = None
            for fixture_name in item.fixturenames:
                if fixture_name == 'driver':
                    driver = item.funcargs.get('driver')
                    break
            handle_failed_test_reset(item, driver)


        # collect feature, scenario, result
        feature = item.module.__name__
        if hasattr(item, 'function') and hasattr(item.function, '__scenario__'):
            scenario = item.function.__scenario__.name
        else:
            scenario = item.name
        status = "PASS" if report.passed else "FAIL"
        test_summary.append((feature, scenario, status))

        # add a separator after the test result
        print(f"\n{'-' * 50}")

        # Get tags
        tags = []
        if hasattr(item, 'function') and hasattr(item.function, '__scenario__'):
            scenario_obj = item.function.__scenario__
            if hasattr(scenario_obj, 'tags'):
                tags = []
                for tag in scenario_obj.tags:
                    if isinstance(tag, str):
                        tags.append(tag)
                    elif hasattr(tag, 'name'):
                        tags.append(tag.name)

    if report.when == "call" and report.failed:
        driver = item.funcargs.get("driver")
        if driver:
            screenshots_dir = "screenshots"
            os.makedirs(screenshots_dir, exist_ok=True)

            if hasattr(item, 'function') and hasattr(item.function, '__scenario__'):
                scenario_obj = item.function.__scenario__
                scenario_name = getattr(scenario_obj, 'name', item.name)
            else:
                scenario_name = item.name

            # save screenshot
            time.sleep(2)
            safe_name = re.sub(r'[^a-zA-Z0-9_\\-]', '_', scenario_name)
            screenshot_path = os.path.join(screenshots_dir, f"{safe_name}_{datetime.now().strftime('%Y%m%d')}.png")
            driver.save_screenshot(screenshot_path)


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_setup(item):
    item.start_time = time.time()
    yield


def pytest_bdd_before_step(request, feature, scenario, step, step_func):
    """Record step information before each step"""
    # Get BDD step text
    step_text = step.name
    # Get step type (given/when/then)
    step_type = step.type

    # Define color codes
    colors = {
        'given': '\033[94m',  # Blue
        'when': '\033[92m',   # Green
        'then': '\033[96m',   # Cyan
        'reset': '\033[0m',   # Reset color
        'scenario': '\033[95m',  # Purple
        'tag': '\033[90m'     # Gray
    }

    # If it's the first step, print feature and scenario information
    if not hasattr(request.node, 'feature_printed'):
        # Get feature file name
        feature_file = os.path.basename(feature.filename)
        print(f"\n{'-' * 50}")
        print(f"{colors['scenario']}Feature: {feature_file}")
        print(f"Scenario: {scenario.name}{colors['reset']}")

        # Get and display tags
        if hasattr(scenario, 'tags'):
            tags = [tag for tag in scenario.tags if isinstance(tag, str)]
            if tags:
                print(f"{colors['tag']}Tags: {', '.join(tags)}{colors['reset']}")
        
        print()  # Empty line
        setattr(request.node, 'feature_printed', True)

    # Select color based on step type
    color = colors.get(step_type.lower(), colors['reset'])

    # Print step information with color
    print(f"{color}{step_type.upper()} {step_text}{colors['reset']}")

def pytest_warning_recorded(warning_message, when, nodeid, location):
    """ Handle pytestUnknownMarkWarning"""
    if "Unknown pytest.mark" in str(warning_message):
        return None
    return warning_message

def session_finished(session, exitstatus):
    print("\nTest Summary:")
    for feature, scenario, status in test_summary:
        print(f"{feature} - {scenario}")
        if status == "PASS":
            print(f"\033[92m{status}\033[0m")  # green
        else:
            print(f"\033[91m{status}\033[0m")  # red
        print()
