import time
from typing import Optional
from appium.webdriver.webdriver import WebDriver
from pages.base_actions.base_action import BaseActions
from pages.locators.onboarding_locators import OnboardingLocators


class OnboardingPage(BaseActions):
    def __init__(self, driver: WebDriver):
        super().__init__(driver)
        self.onboarding_locators = OnboardingLocators()

    def verify_welcome_screen_elements(self) -> bool:
        elements = [
            self.onboarding_locators.TRACK_FINANCES_TEXT,
            self.onboarding_locators.ANALYZE_EXPENDITURE_TEXT,
            self.onboarding_locators.STICK_TO_BUDGETS_TEXT
        ]
        
        for element in elements:
            if not self.wait_for_element_present(*element, timeout=10):
                return False
        return True

    def is_track_finances_displayed(self) -> bool:
        return self.is_element_visible(*self.onboarding_locators.TRACK_FINANCES_TEXT)

    def is_analyze_expenditure_displayed(self) -> bool:
        return self.is_element_visible(*self.onboarding_locators.ANALYZE_EXPENDITURE_TEXT)

    def is_stick_to_budgets_displayed(self) -> bool:
        return self.is_element_visible(*self.onboarding_locators.STICK_TO_BUDGETS_TEXT)

    def click_get_started_button(self) -> 'OnboardingPage':
        self.wait_for_element_present(*self.onboarding_locators.GET_STARTED_BUTTON)
        self.click_element(*self.onboarding_locators.GET_STARTED_BUTTON)
        return self

    def click_income_tab(self) -> 'OnboardingPage':
        self.wait_for_element_present(*self.onboarding_locators.INCOME_TAB)
        self.click_element(*self.onboarding_locators.INCOME_TAB)
        return self

    def click_paycheck_option(self) -> 'OnboardingPage':
        self.wait_for_element_present(*self.onboarding_locators.PAYCHECK_OPTION)
        self.click_element(*self.onboarding_locators.PAYCHECK_OPTION)
        return self

    def click_new_button(self) -> 'OnboardingPage':
        self.wait_for_element_present(*self.onboarding_locators.NEW_BUTTON)
        self.click_element(*self.onboarding_locators.NEW_BUTTON)
        return self

    def search_emoji(self, search_text: str) -> 'OnboardingPage':
        self.wait_for_element_present(*self.onboarding_locators.EMOJI_SEARCH_FIELD)
        self.clear_text(*self.onboarding_locators.EMOJI_SEARCH_FIELD)
        self.send_keys_to_element(*self.onboarding_locators.EMOJI_SEARCH_FIELD, search_text)
        return self

    def click_stock_emoji(self) -> 'OnboardingPage':
        self.wait_for_element_present(*self.onboarding_locators.STOCK_EMOJI_RESULT)
        self.click_element(*self.onboarding_locators.STOCK_EMOJI_RESULT)
        return self

    def click_add_icon_button(self) -> 'OnboardingPage':
        self.wait_for_element_present(*self.onboarding_locators.ADD_ICON_BUTTON)
        self.click_element(*self.onboarding_locators.ADD_ICON_BUTTON)
        return self

    def enter_category_name(self, category_name: str) -> 'OnboardingPage':
        self.wait_for_element_present(*self.onboarding_locators.CATEGORY_NAME_FIELD)
        self.clear_text(*self.onboarding_locators.CATEGORY_NAME_FIELD)
        self.send_keys_to_element(*self.onboarding_locators.CATEGORY_NAME_FIELD, category_name)
        return self

    def click_add_category_button(self) -> 'OnboardingPage':
        self.wait_for_element_present(*self.onboarding_locators.ADD_CATEGORY_ICON_BUTTON)
        self.click_element(*self.onboarding_locators.ADD_CATEGORY_ICON_BUTTON)
        return self

    def close_bottom_sheet(self) -> 'OnboardingPage':
        screen_width, screen_height = self.get_screen_size()
        self.tap(screen_width * 0.5, screen_height * 0.2)
        time.sleep(1.5)  
        return self

    def click_next_button(self) -> 'OnboardingPage':
        time.sleep(1)
        self.tap(0.85, 0.92)
        return self

 