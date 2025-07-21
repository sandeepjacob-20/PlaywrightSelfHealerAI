from playwright.sync_api import sync_playwright
from llm_module import llm_caller
import sys

try:
    inference_mode = sys.argv[1] if len(sys.argv) > 1 else 'endpoint'
    print(f"Inference mode set to: {inference_mode}")
except:
    print("Inference mode (local, endpoint) not provided. Defaulting to 'endpoint'.")
    inference_mode = 'endpoint'

try:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        try:
            page.goto("https://duckduckgo.com/?t=h_")
            page.click("button:has-text('Accept all')")
            page.fill("input[name='q']", "cats")
            page.press("input[name='q']", "Enter")

            # Short wait for results (adjust as needed)
            page.wait_for_timeout(5000) 

            page.click("resul") # This is the key line to address the error
            page.wait_for_timeout(3000)
            browser.close()

        except Exception as e:
            print("Error occurred during automation:")
            print(e)
            # Remove if you do not need the LLM callback.
            # llm_caller(str(e),e,page,inference_mode)
            browser.close()

except Exception as outer:
    print("Playwright failed to start or browser error:", outer)
    browser.close()
