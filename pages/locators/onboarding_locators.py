from appium.webdriver.common.appiumby import AppiumBy

class OnboardingLocators:
    # Welcome screen elements
    TRACK_FINANCES_TEXT = (AppiumBy.ACCESSIBILITY_ID, "Track your finances")
    ANALYZE_EXPENDITURE_TEXT = (AppiumBy.ACCESSIBILITY_ID, "Analyse your expenditure")
    STICK_TO_BUDGETS_TEXT = (AppiumBy.ACCESSIBILITY_ID, "Stick to budgets")
    GET_STARTED_BUTTON = (AppiumBy.ACCESSIBILITY_ID, "Get Started")
    
    # Category page elements
    INCOME_TAB = (AppiumBy.ACCESSIBILITY_ID, "Income")
    PAYCHECK_OPTION = (AppiumBy.ACCESSIBILITY_ID, "Paycheck")
    NEW_BUTTON = (AppiumBy.ACCESSIBILITY_ID, "New")
    
    # Emoji search elements
    EMOJI_SEARCH_FIELD = (AppiumBy.XPATH, '//XCUIElementTypeTextField[@value="Search Emoji"]')
    STOCK_EMOJI_RESULT = (AppiumBy.XPATH, '//XCUIElementTypeStaticText[@name="📈"]')
    
    # Category creation elements
    CATEGORY_NAME_FIELD = (AppiumBy.XPATH, '//XCUIElementTypeTextField[@value="Category Name"]')
    ADD_CATEGORY_ICON_BUTTON = (AppiumBy.XPATH, '//XCUIElementTypeButton[@name="plus" and @label="Add"]')
    CLOSE_BUTTON = (AppiumBy.ACCESSIBILITY_ID, "Close")
    
    
