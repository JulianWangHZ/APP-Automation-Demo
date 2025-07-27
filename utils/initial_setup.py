# initial_setup.py

import os
from pages.iOS.onboarding_page import OnboardingPage

def setup_flow(driver):
    """
    Initial setup flow
    This function will be called in conftest.py to handle the initial setup of the application
    
    Args:
        driver: WebDriver instance (required, provided by conftest.py)
    
    Returns:
        bool: True if setup successful, False otherwise
    
    Note: This function will be skipped when the test has 'onboarding' tag
    """
    print("Running initial setup flow...")

    # --- STEP 1: Execute complete onboarding flow
    try:
        print("Starting complete onboarding flow...")
        result = complete_onboarding_flow(driver)
        if result:
            print("Onboarding flow completed successfully")
        else:
            print("Onboarding flow failed")
            return False
    except Exception as e:
        print(f"Error during onboarding flow: {str(e)}")
        return False
    
    return True


def complete_onboarding_flow(driver) -> bool:
    try:
        onboarding_page = OnboardingPage(driver)
        
        # 1. Verify welcome screen elements
        print("Step 1: Verifying welcome screen elements...")
        if not onboarding_page.verify_welcome_screen_elements():
            print("Welcome screen elements verification failed")
            return False
        
        # 2. Click Get Started
        print("Step 2: Clicking Get Started button...")
        onboarding_page.click_get_started_button()
        
        # 3. Switch to Income tab
        print("Step 3: Switching to Income tab...")
        onboarding_page.click_income_tab()
        
        # 4. Click Paycheck option
        print("Step 4: Clicking Paycheck option...")
        onboarding_page.click_paycheck_option()
        
        # 5. Click New button
        print("Step 5: Clicking New button...")
        onboarding_page.click_new_button()
        
        # 6. Search stock emoji
        print("Step 6: Searching for stock emoji...")
        onboarding_page.search_emoji("stock")
        
        # 7. Select stock emoji
        print("Step 7: Selecting stock emoji...")
        onboarding_page.click_stock_emoji()
        
        # 8. Click add icon button
        print("Step 8: Clicking add icon button...")
        onboarding_page.click_add_icon_button()
        
        # 9. Enter category name
        print("Step 9: Entering category name 'Stock'...")
        onboarding_page.enter_category_name("Stock")
        
        # 10. Click add category button
        print("Step 10: Clicking add category button...")
        onboarding_page.click_add_category_button()
        
        # 11. Close bottom sheet
        print("Step 11: Closing bottom sheet...")
        onboarding_page.close_bottom_sheet()
        
        # 12. Click next button to complete onboarding
        print("Step 12: Clicking next button to complete onboarding...")
        onboarding_page.click_next_button()
        
        print("Complete onboarding flow finished successfully!")
        return True
        
    except Exception as e:
        print(f"Onboarding flow failed: {str(e)}")
        return False
