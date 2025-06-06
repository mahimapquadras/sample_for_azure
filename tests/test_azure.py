# import pytest
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
# from webdriver_manager.chrome import ChromeDriverManager
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# import time

# @pytest.fixture(scope="module")
# def browser():
#     chrome_options = Options()
#     # --- ADD THIS LINE FOR HEADLESS MODE ---
#     chrome_options.add_argument("--headless")
#     # Optional: Add other arguments for better CI/CD compatibility
#     chrome_options.add_argument("--no-sandbox") # Required for running as root in some Linux environments
#     chrome_options.add_argument("--disable-dev-shm-usage") # Overcomes limited resource problems
#     # ----------------------------------------

#     service = Service(ChromeDriverManager().install())
#     driver = webdriver.Chrome(service=service, options=chrome_options)
#     driver.implicitly_wait(10) # wait up to 10 seconds for elements to appear
#     yield driver
#     driver.quit() # Teardown: close the browser after tests are done

# def test_azure(browser):
#     print("\nStarting test_azure (Wikipedia search)...")
#     browser.get("https://www.wikipedia.org/")
#     print(f"Navigated to: {browser.current_url}")

#     search_input = WebDriverWait(browser, 10).until(
#         EC.presence_of_element_located((By.ID, "searchInput"))
#     )
#     search_input.send_keys("Azure DevOps")
#     print("Typed 'Azure DevOps' into search box.")

#     search_input.send_keys(Keys.ENTER) # Press ENTER to submit search
#     print("Pressed ENTER to submit search.")

#     time.sleep(3) # Give some time for results to load

#     # Assert that "Azure DevOps" is present in the title or the main heading of the results page
#     try:
#         page_heading = WebDriverWait(browser, 10).until(
#             EC.presence_of_element_located((By.ID, "firstHeading"))
#         )
#         assert "Azure DevOps" in page_heading.text
#         print(f"Assertion passed: Page heading contains 'Azure DevOps'. Actual heading: '{page_heading.text}'")

#     except Exception as e:
#         print(f"Failed to find or assert 'Azure DevOps' in page heading: {e}")
#         try:
#             search_results_header = WebDriverWait(browser, 5).until(
#                 EC.presence_of_element_located((By.CSS_SELECTOR, "h1.mw-search-top-table-header"))
#             )
#             assert "Search results for" in search_results_header.text
#             print("Found search results page header, but didn't land on direct article.")

#             azure_devops_link = WebDriverWait(browser, 5).until(
#                 EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, "Azure DevOps"))
#             )
#             assert azure_devops_link.is_displayed()
#             print("Assertion passed: Found 'Azure DevOps' link on search results page.")

#         except Exception as inner_e:
#             pytest.fail(f"Test failed: Neither direct article nor search results page for 'Azure DevOps' found. Error: {inner_e}")

#     print("Test finished successfully!")

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options as ChromeOptions # Using ChromeOptions for general browser settings
from selenium.webdriver.remote.webdriver import WebDriver as RemoteWebDriver # For clarity
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os # Import the os module to access environment variables
import time

# BrowserStack credentials and build name will be set by the Azure Pipeline task
BROWSERSTACK_USERNAME = os.environ.get("BROWSERSTACK_USERNAME")
BROWSERSTACK_ACCESS_KEY = os.environ.get("BROWSERSTACK_ACCESS_KEY")
BROWSERSTACK_BUILD_NAME = os.environ.get("BROWSERSTACK_BUILD_NAME")

# BrowserStack Hub URL
BROWSERSTACK_URL = f"https://{BROWSERSTACK_USERNAME}:{BROWSERSTACK_ACCESS_KEY}@hub-cloud.browserstack.com/wd/hub"

@pytest.fixture(scope="module")
def browser():
    # Define desired capabilities for BrowserStack
    bstack_options = ChromeOptions() # You can use generic Options for Chrome
    bstack_options.browser_version = "latest" # Use the latest Chrome version
    bstack_options.platform_name = "Windows 10" # Or "macOS Catalina", "Windows 11", etc.

    # Add BrowserStack-specific capabilities
    bstack_options.set_capability("bstack:options", {
        "os": "Windows",
        "osVersion": "10",
        "browserName": "Chrome",
        "browserVersion": "latest",
        "projectName": "Selenium Azure DevOps Demo",
        "buildName": BROWSERSTACK_BUILD_NAME, # Set the build capability here!
        "sessionName": "Wikipedia Azure DevOps Search Test",
        "seleniumVersion": "4.x.x", # Replace with your actual Selenium version if specific
        "local": "false" # Set to "true" if you're testing local websites with BrowserStack Local
    })

    # Initialize Remote WebDriver to connect to BrowserStack
    print(f"\nConnecting to BrowserStack Hub: {BROWSERSTACK_URL}")
    driver = webdriver.Remote(
        command_executor=BROWSERSTACK_URL,
        options=bstack_options
    )
    driver.implicitly_wait(10) # wait up to 10 seconds for elements to appear
    yield driver
    driver.quit() # Teardown: close the browser after tests are done

def test_azure(browser):
    print("\nStarting test_azure (Wikipedia search on BrowserStack)...")
    browser.get("https://www.wikipedia.org/")
    print(f"Navigated to: {browser.current_url}")

    search_input = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.ID, "searchInput"))
    )
    search_input.send_keys("Azure DevOps")
    print("Typed 'Azure DevOps' into search box.")

    search_input.send_keys(Keys.ENTER) # Press ENTER to submit search
    print("Pressed ENTER to submit search.")

    time.sleep(3) # Give some time for results to load

    # Assert that "Azure DevOps" is present in the title or the main heading of the results page
    try:
        page_heading = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.ID, "firstHeading"))
        )
        assert "Azure DevOps" in page_heading.text
        print(f"Assertion passed: Page heading contains 'Azure DevOps'. Actual heading: '{page_heading.text}'")

    except Exception as e:
        print(f"Failed to find or assert 'Azure DevOps' in page heading: {e}")
        try:
            search_results_header = WebDriverWait(browser, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "h1.mw-search-top-table-header"))
            )
            assert "Search results for" in search_results_header.text
            print("Found search results page header, but didn't land on direct article.")

            azure_devops_link = WebDriverWait(browser, 5).until(
                EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, "Azure DevOps"))
            )
            assert azure_devops_link.is_displayed()
            print("Assertion passed: Found 'Azure DevOps' link on search results page.")

        except Exception as inner_e:
            pytest.fail(f"Test failed: Neither direct article nor search results page for 'Azure DevOps' found. Error: {inner_e}")

    print("Test finished successfully on BrowserStack!")