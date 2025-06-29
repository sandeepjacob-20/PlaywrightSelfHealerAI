from playwright.sync_api import sync_playwright
import traceback
from llm_module import llm_caller

try:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        try:
            # Step 1: Visit DuckDuckGo
            page.goto("https://duckduckgo.com/?t=h_")

            # Step 2: Accept cookies if prompted
            try:
                page.click("button:has-text('Accept all')")
            except:
                pass

            # Step 3: Search
            page.fill("input[name='q']", "cats")
            page.press("input[name='q']", "Enter")

            # Step 4: Wait for search results
            page.wait_for_selector("resul")
            page.click("resul")

            page.wait_for_timeout(3000)
            browser.close()

        except Exception as e:
            path = traceback.format_exc().split('File')[1].split(',')[0]
            print("Error occurred during automation:")
            print(e)

            # Safely get the DOM here before browser is closed
            try:
                llm_caller(path,e,page)
            except Exception as dom_error:
                print("Failed to get DOM due to:", dom_error)

            browser.close()

except Exception as outer:
    print("Playwright failed to start or browser error:", outer)