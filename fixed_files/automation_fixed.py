from playwright.sync_api import sync_playwright
import traceback
# from llm_module import llm_caller # Commented out as llm_module is not provided and likely external

try:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        try:
            page.goto("https://duckduckgo.com/?t=h_")

            # Attempt to accept cookies if the button exists, with a short timeout.
            # If it doesn't appear or isn't clickable, the `except` block will handle it.
            try:
                page.locator("button:has-text('Accept all')").click(timeout=5000)
                print("Cookie banner accepted.")
            except Exception:
                print("No 'Accept all' cookie button found or click timed out.")
                pass # Continue if cookie banner is not present

            page.fill("input[name='q']", "cats")
            page.press("input[name='q']", "Enter")

            # CORRECTED: Wait for a visible search result element using a proper selector.
            # 'article[data-testid="result"]' targets the individual search result blocks.
            page.wait_for_selector("article[data-testid='result']")
            print("Search results loaded.")

            # Click on the first search result found
            page.click("article[data-testid='result']")
            print("Clicked on the first search result.")

            page.wait_for_timeout(3000) # Wait for 3 seconds to observe
            
        except Exception as e:
            print("Error occurred during automation:")
            print(traceback.format_exc()) # Print the full traceback for debugging

            # If you still need llm_caller, ensure it's imported and handles the input correctly
            # For example, if it expects the page content, you might use:
            # try:
            #     llm_caller("Automation Error", e, page.content())
            # except Exception as dom_error:
            #     print(f"Failed to call llm_caller: {dom_error}")

        finally:
            browser.close() # Ensure the browser is always closed

except Exception as outer_error:
    print("Playwright failed to start or browser initialization error:")
    print(traceback.format_exc())

