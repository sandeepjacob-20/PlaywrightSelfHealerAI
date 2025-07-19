from playwright.sync_api import sync_playwright
import traceback
from llm_module import llm_caller

inference_mode = 'endpoint' # or 'local', depending on your setup

try:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        try:
            # Step 1: Visit DuckDuckGo
            page.goto("https://duckduckgo.com/?t=h_")

            # Step 2: Accept cookies if prompted (optional, might not always appear)
            try:
                # Use a more specific selector if available, or a timeout for the click
                page.click("button:has-text('Accept all')", timeout=5000)
            except Exception as e:
                print(f"No cookie consent button found or clickable: {e}")
                pass # Continue if the button is not present

            # Step 3: Search
            page.fill("input[name='q']", "cats")
            page.press("input[name='q']", "Enter")

            # Step 4: Wait for search results using a correct selector
            # Waiting for the first search result article to be visible
            page.wait_for_selector("article[data-testid='result']")
            
            # The original code had page.click("resul") which was incorrect.
            # If you intended to click on the first search result, you would do:
            # page.click("article[data-testid='result']")
            # For now, we assume just waiting for results is sufficient, so we remove the click.

            page.wait_for_timeout(3000) # Wait for 3 seconds to observe
            browser.close()

        except Exception as e:
            path = traceback.format_exc().split('File')[1].split(',')[0]
            print("Error occurred during automation:")
            print(e)

            # Safely get the DOM here before browser is closed
            try:
                llm_caller(path,e,page,inference_mode)
            except Exception as dom_error:
                print("Failed to get DOM due to:", dom_error)

            browser.close()

except Exception as outer:
    print("Playwright failed to start or browser error:", outer)

