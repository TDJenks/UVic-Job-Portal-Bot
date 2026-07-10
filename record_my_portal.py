from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    # Connect playwright to chrome via port 9222 
    # (must have launch_chrome.bat running first)
    browser = p.chromium.connect_over_cdp("http://localhost:9222")
    
    # Opens codegen for the first tab in the browser (records actions as playwright code)
    context = browser.contexts[0]
    page = context.pages[0]
    print("--- SCRIPT STARTED SUCCESSFULY ---")
    page.pause()