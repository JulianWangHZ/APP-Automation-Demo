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



def pytest_addoption(parser):
    """Add custom command line options"""
    parser.addoption(
        "--skipsetup",
        action="store_true",
        default=False,
        help="Skip app reinstallation and setup process"
    )

@pytest.fixture(scope="session", autouse=True)
def driver(request):
    """Create driver and reinstall App before each test session"""
    print("\n=========== Session Start: Creating driver and preparing environment ===========")

    # Get environment variables
    platform = os.getenv('APPIUM_OS').lower()
    email = os.getenv('TEST_EMAIL')
    ver_code = os.getenv('VERIFICATION_CODE')
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
            if app_path:
                run(['xcrun', 'simctl', 'uninstall', 'booted', 'com.hunger.hotcakeapp.staging'], check=True)
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

    # Check if there are tests with the 'login' marker in the current test collection
    has_login_tag = False
    for item in request.session.items:
        if item.get_closest_marker('login'):
            has_login_tag = True
            break

    # --- Onboarding + login process ---
    if has_login_tag or skip_setup:
        print("Found tests with login marker or skipsetup flag, skipping onboarding and login process")
    else:
        print("Executing onboarding and login process...")
        try:
            setup_flow(driver, email, ver_code)
            print("Initialization process completed")
        except Exception as e:
            print(f"Onboarding/Login process failed: {e}")

    yield driver

    # --- Cleanup at the end of the session ---
    appium_setup.tearDown()
    print("\n=========== Session End ===========")

def pytest_configure(config):
    """Configure test collection and markers"""
    config.addinivalue_line("markers", "onboarding: Mark test as onboarding")
    config.addinivalue_line("markers", "login: login related tests run on port 4723")
    
    if not config.args:
        platform = os.getenv('APPIUM_OS').lower()
        logger.info(f"Configuring test collection for platform: {platform}")
        if platform == 'pados':
            config.args = ['tests/steps/padOS']
        else:
            config.args = ['tests/steps/ios']


def pytest_bdd_apply_tag(tag, function):
    if tag == 'order':
        marker = pytest.mark.run(order=int(function.__doc__.split('order=')[1]))
        marker(function)
        return True
    return None

def pytest_collection_modifyitems(items):
    """Filter tests for the selected platform"""
    platform = os.getenv('APPIUM_OS').lower()
    logger.info(f"Running tests for platform: {platform}")
    
    filtered_items = []
    for item in items:
        file_path = str(item.fspath)
        if platform == 'pados' and '/padOS/' in file_path:
            filtered_items.append(item)
        elif platform == 'ios' and '/ios/' in file_path:
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
    
    # Record test results
    if report.when == "call":  # Only record when the test is executed
        # Set the flag for whether the next test needs to be reinstalled
        if hasattr(item.session, 'previous_test_failed'):
            item.session.previous_test_failed = report.failed
        else:
            setattr(item.session, 'previous_test_failed', report.failed)
        
        if report.failed:
            # In BrowserStack environment, we can only reset the app state
            print(f"Test failed, starting to reset app state...")
            try:
                driver = None
                for fixture_name in item.fixturenames:
                    if fixture_name == 'driver':
                        driver = item.funcargs.get('driver')
                        break
                
                if driver:
                    is_ci = os.getenv('IS_CI', 'false').lower() == 'true'
                    platform = os.getenv('APPIUM_OS').lower()
                    
                    if is_ci:
                        try:
                            app_id = 'com.hunger.hotcakeapp.staging'
                            
                            print(f"Clearing app data: {app_id}")
                            driver.execute_script('mobile: clearApp', {'appId': app_id})
                            print("App data cleared successfully")
                            
                            print(f"Restarting app: {app_id}")
                            driver.activate_app(app_id)
                            print("App restarted successfully")
                                
                        except Exception as webdriver_error:
                            print(f"BrowserStack app reset failed: {webdriver_error}")
                            print("Cannot reset app in BrowserStack environment, continuing to next test")
                    
                    else:
                        app_id = 'com.hunger.hotcakeapp.staging'
                        app_path = os.getenv('IOS_APP_PATH')
                        
                        if app_path:
                            print(f"Uninstalling iOS app: {app_id}")
                            run(['xcrun', 'simctl', 'uninstall', 'booted', app_id], check=True)
                            print(f"Reinstalling iOS app: {app_path}")
                            run(['xcrun', 'simctl', 'install', 'booted', app_path], check=True)
                            print("iOS app reinstalled successfully")
                        else:
                            print("IOS_APP_PATH environment variable not set, cannot reinstall")
                    
                    # Re-execute setup_flow
                    email = os.getenv('TEST_EMAIL')
                    ver_code = os.getenv('VERIFICATION_CODE')
                    
                    if email and ver_code:
                        print(f"Starting to re-login, using email: {email}, ver_code: {ver_code}")
                        try:
                            setup_flow(driver, email, ver_code)
                            print("Re-login successful")
                        except Exception as setup_error:
                            print(f"Re-login failed: {setup_error}")
                else:
                    print("Driver not found, cannot reset app state")
            except Exception as e:
                print(traceback.format_exc())
        
        start_time = getattr(item, 'start_time', time.time())
        duration = time.time() - start_time
        
        # Get test related information
        test_name = item.name
        feature = item.module.__name__
        scenario = item.function.__doc__ or test_name
        
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
