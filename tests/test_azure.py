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
#     service = Service(ChromeDriverManager().install())
#     driver = webdriver.Chrome(service=service, options=chrome_options)
#     driver.implicitly_wait(10)
#     yield driver
#     driver.quit()

# def test_azure(browser):
#     print("\nStarting test_azure (Wikipedia search)...")
#     browser.get("https://www.wikipedia.org/")
#     print(f"Navigated to: {browser.current_url}")

#     # Find the search input field by its ID
#     search_input = WebDriverWait(browser, 10).until(
#         EC.presence_of_element_located((By.ID, "searchInput"))
#     )
#     search_input.send_keys("Azure DevOps")
#     print("Typed 'Azure DevOps' into search box.")

#     # --- MODIFIED PART START ---
#     # Option 1: Press ENTER directly in the search box (most reliable for search forms)
#     search_input.send_keys(Keys.ENTER)
#     print("Pressed ENTER to submit search.")
#     # --- MODIFIED PART END ---

#     # Give some time for results to load
#     time.sleep(3) # Keep a short sleep here while we fine-tune the next assertion

#     # Assert that "Azure DevOps" is present in the title or the main heading of the results page
#     # Look for the main heading (h1) on the Wikipedia article page
#     try:
#         # After pressing ENTER, it should take you directly to the article if it exists.
#         # The main heading of a Wikipedia article is usually 'firstHeading'.
#         page_heading = WebDriverWait(browser, 10).until(
#             EC.presence_of_element_located((By.ID, "firstHeading"))
#         )
#         assert "Azure DevOps" in page_heading.text
#         print(f"Assertion passed: Page heading contains 'Azure DevOps'. Actual heading: '{page_heading.text}'")

#     except Exception as e:
#         print(f"Failed to find or assert 'Azure DevOps' in page heading: {e}")
#         # If it didn't land directly on the article, it might be on a search results page.
#         # Let's add a fallback check for a search results page if the direct article fails.
#         try:
#             # Check for "Search results for..." text or a specific result link
#             search_results_header = WebDriverWait(browser, 5).until(
#                 EC.presence_of_element_located((By.CSS_SELECTOR, "h1.mw-search-top-table-header")) # A common header for search result pages
#             )
#             assert "Search results for" in search_results_header.text
#             print("Found search results page header, but didn't land on direct article.")

#             # Optionally, look for a link to the "Azure DevOps" article
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
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

@pytest.fixture(scope="module")
def browser():
    chrome_options = Options()
    # --- ADD THIS LINE FOR HEADLESS MODE ---
    chrome_options.add_argument("--headless")
    # Optional: Add other arguments for better CI/CD compatibility
    chrome_options.add_argument("--no-sandbox") # Required for running as root in some Linux environments
    chrome_options.add_argument("--disable-dev-shm-usage") # Overcomes limited resource problems
    # ----------------------------------------

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.implicitly_wait(10) # wait up to 10 seconds for elements to appear
    yield driver
    driver.quit() # Teardown: close the browser after tests are done

def test_azure(browser):
    print("\nStarting test_azure (Wikipedia search)...")
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

    print("Test finished successfully!")