import pytest
from pytest_bdd import scenarios, given, when, then, parsers

from pages.iOS.onboarding_page import OnboardingPage

scenarios('../../../features/onboarding.feature')


# Background 
@given('I launch the Dime application')
def launch_dime_application(driver):
    pass


@given('I am on the welcome screen')
def on_welcome_screen(driver):
    onboarding_page = OnboardingPage(driver)
    assert onboarding_page.wait_for_element_present(*onboarding_page.onboarding_locators.GET_STARTED_BUTTON), \
        "Welcome screen did not load properly"


# Complete onboarding flow
@given('I can see the welcome screen elements')
def can_see_welcome_screen_elements(driver):
    onboarding_page = OnboardingPage(driver)
    assert onboarding_page.verify_welcome_screen_elements(), \
        "Not all welcome screen elements are visible"


@when('I tap the Get Started button')
def tap_get_started_button(driver):
    onboarding_page = OnboardingPage(driver)
    onboarding_page.click_get_started_button()


@when('I am navigated to the categories page')
def navigated_to_categories_page(driver):
    onboarding_page = OnboardingPage(driver)
    assert onboarding_page.wait_for_element_present(*onboarding_page.onboarding_locators.INCOME_TAB), \
        "Categories page did not load properly"


@when('I tap on the Income tab')
def tap_income_tab(driver):
    onboarding_page = OnboardingPage(driver)
    onboarding_page.click_income_tab()


@when('I tap on the Paycheck option to add it to income categories')
def tap_paycheck_option(driver):
    onboarding_page = OnboardingPage(driver)
    onboarding_page.click_paycheck_option()


@when('I tap the New button to create a custom income category')
def tap_new_button(driver):
    onboarding_page = OnboardingPage(driver)
    onboarding_page.click_new_button()


@when(parsers.parse('I search for "{search_text}" emoji in the search field'))
def search_emoji_in_field(driver, search_text):
    onboarding_page = OnboardingPage(driver)
    onboarding_page.search_emoji(search_text)


@when('I select the stock emoji from search results')
def select_stock_emoji(driver):
    onboarding_page = OnboardingPage(driver)
    onboarding_page.click_stock_emoji()


@when('I tap the plus icon to add the emoji')
def tap_plus_icon_add_emoji(driver):
    onboarding_page = OnboardingPage(driver)
    onboarding_page.click_add_category_button()


@when(parsers.parse('I enter "{category_name}" as the category name'))
def enter_category_name(driver, category_name):
    onboarding_page = OnboardingPage(driver)
    onboarding_page.enter_category_name(category_name)


@when('I tap the plus button to create the income category')
def tap_plus_button_create_category(driver):
    onboarding_page = OnboardingPage(driver)
    onboarding_page.click_add_category_button()


@when('I close the bottom sheet by tapping outside')
def close_bottom_sheet(driver):
    onboarding_page = OnboardingPage(driver)
    onboarding_page.close_bottom_sheet()


@when('I tap the Next button to complete onboarding')
def tap_next_button_complete_onboarding(driver):
    onboarding_page = OnboardingPage(driver)
    onboarding_page.click_next_button()


@then('I should successfully complete the onboarding flow')
def should_complete_onboarding_flow(driver):
    pass



