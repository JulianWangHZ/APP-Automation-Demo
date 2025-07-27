@onboarding
Feature: Onboarding flow for new users

  Background:
    Given I launch the Dime application
    And I am on the welcome screen

  @regression @complete_onboarding_flow @onboarding
  Scenario: Complete onboarding flow with income category setup
    Given I can see the welcome screen elements
    When I tap the Get Started button
    And I am navigated to the categories page
    And I tap on the Income tab
    And I tap on the Paycheck option to add it to income categories
    And I tap the New button to create a custom income category
    And I search for "stock" emoji in the search field
    And I select the stock emoji from search results
    And I tap the plus icon to add the emoji
    And I enter "Stock" as the category name
    And I tap the plus button to create the income category
    And I close the bottom sheet by tapping outside
    And I tap the Next button to complete onboarding
    Then I should successfully complete the onboarding flow
