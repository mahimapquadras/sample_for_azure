# import pytest
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.chrome.options import Options as ChromeOptions
# from selenium.webdriver.remote.webdriver import WebDriver as RemoteWebDriver
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# import os
# import time

# # BrowserStack credentials and build name will be set by the Azure Pipeline task
# BROWSERSTACK_USERNAME = os.environ.get("BROWSERSTACK_USERNAME")
# BROWSERSTACK_ACCESS_KEY = os.environ.get("BROWSERSTACK_ACCESS_KEY")
# BROWSERSTACK_BUILD_NAME = os.environ.get("BROWSERSTACK_BUILD_NAME")

# # BrowserStack Hub URL
# BROWSERSTACK_URL = f"https://{BROWSERSTACK_USERNAME}:{BROWSERSTACK_ACCESS_KEY}@hub-cloud.browserstack.com/wd/hub"

# @pytest.fixture(scope="module")
# def browser():
#     # Define desired capabilities for BrowserStack
#     bstack_options = ChromeOptions() # Using ChromeOptions for general browser settings
#     bstack_options.browser_version = "latest" # Use the latest Chrome version
#     bstack_options.platform_name = "Windows 10" # Or "macOS Catalina", "Windows 11", etc.

#     # Add BrowserStack-specific capabilities
#     bstack_options.set_capability("bstack:options", {
#         "os": "Windows",
#         "osVersion": "10",
#         "browserName": "Chrome",
#         "browserVersion": "latest",
#         "projectName": "Selenium Azure DevOps Demo",
#         "buildName": BROWSERSTACK_BUILD_NAME, # This is crucial for reporting
#         "sessionName": "Wikipedia Azure DevOps Search Test",
#         # --- REMOVED THIS LINE: "seleniumVersion": "4.x.x", ---
#         "local": "false"
#     })

#     # Initialize Remote WebDriver to connect to BrowserStack
#     print(f"\nConnecting to BrowserStack Hub: {BROWSERSTACK_URL}")
#     driver = webdriver.Remote(
#         command_executor=BROWSERSTACK_URL,
#         options=bstack_options
#     )
#     driver.implicitly_wait(10) # wait up to 10 seconds for elements to appear
#     yield driver
#     driver.quit() # Teardown: close the browser after tests are done

# def test_azure(browser):
#     print("\nStarting test_azure (Wikipedia search on BrowserStack)...")
#     browser.get("https://www.wikipedia.org/")
#     print(f"Navigated to: {browser.current_url}")

#     search_input = WebDriverWait(browser, 10).until(
#         EC.presence_of_element_located((By.ID, "searchInput"))
#     )
#     search_input.send_keys("Azure DevOps")
#     print("Typed 'Azure DevOps' into search box.")

#     search_input.send_keys(Keys.ENTER)
#     print("Pressed ENTER to submit search.")

#     time.sleep(3) # Give some time for results to load

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

#     print("Test finished successfully on BrowserStack!")

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.remote.webdriver import WebDriver as RemoteWebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import time
import json # Import json for constructing the JavaScript executor command

# BrowserStack credentials and build name will be set by the Azure Pipeline task
BROWSERSTACK_USERNAME = os.environ.get("BROWSERSTACK_USERNAME")
BROWSERSTACK_ACCESS_KEY = os.environ.get("BROWSERSTACK_ACCESS_KEY")
BROWSERSTACK_BUILD_NAME = os.environ.get("BROWSERSTACK_BUILD_NAME")

# BrowserStack Hub URL
BROWSERSTACK_URL = f"https://{BROWSERSTACK_USERNAME}:{BROWSERSTACK_ACCESS_KEY}@hub-cloud.browserstack.com/wd/hub"

@pytest.fixture(scope="module")
def browser():
    bstack_options = ChromeOptions()
    bstack_options.browser_version = "latest"
    bstack_options.platform_name = "Windows 10"

    bstack_options.set_capability("bstack:options", {
        "os": "Windows",
        "osVersion": "10",
        "browserName": "Chrome",
        "browserVersion": "latest",
        "projectName": "Selenium Azure DevOps Demo",
        "buildName": BROWSERSTACK_BUILD_NAME,
        "sessionName": "Wikipedia Azure DevOps Search Test",
        "local": "false"
    })

    print(f"\nConnecting to BrowserStack Hub: {BROWSERSTACK_URL}")
    driver = webdriver.Remote(
        command_executor=BROWSERSTACK_URL,
        options=bstack_options
    )
    driver.implicitly_wait(10)
    yield driver
    driver.quit()

def test_azure(browser):
    status = "passed" # Default status
    reason = "Test completed successfully." # Default reason

    try:
        print("\nStarting test_azure (Wikipedia search on BrowserStack)...")
        browser.get("https://www.wikipedia.org/")
        print(f"Navigated to: {browser.current_url}")

        search_input = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.ID, "searchInput"))
        )
        search_input.send_keys("Azure DevOps")
        print("Typed 'Azure DevOps' into search box.")

        search_input.send_keys(Keys.ENTER)
        print("Pressed ENTER to submit search.")

        time.sleep(3) # Give some time for results to load

        # Assertion logic
        try:
            page_heading = WebDriverWait(browser, 10).until(
                EC.presence_of_element_located((By.ID, "firstHeading"))
            )
            assert "Azure DevOps" in page_heading.text
            print(f"Assertion passed: Page heading contains 'Azure DevOps'. Actual heading: '{page_heading.text}'")

        except Exception as e:
            print(f"Failed to find or assert 'Azure DevOps' in page heading: {e}")
            # Try fallback to search results page
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
                # If neither direct article nor search results work, mark as failed
                status = "failed"
                reason = f"Test failed: Neither direct article nor search results page for 'Azure DevOps' found. Error: {inner_e}"
                pytest.fail(reason) # Ensure pytest also registers this as a failure

    except Exception as e:
        status = "failed"
        reason = f"Unhandled test error: {e}"
        # If an unhandled exception occurs, pytest will mark it as error/failure automatically
        # No need for pytest.fail here if it's truly unhandled

    finally:
        # --- Mark the session status on BrowserStack ---
        # This will run regardless of whether the test passed or failed
        mark_session_status_script = json.dumps({
            "action": "setSessionStatus",
            "arguments": {
                "status": status,
                "reason": reason
            }
        })
        print(f"Marking BrowserStack session as '{status}' with reason: '{reason}'")
        browser.execute_script(f'browserstack_executor: {mark_session_status_script}')
        # -----------------------------------------------

    print("Test finished successfully on BrowserStack!")