from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    # 1. Connect to your already-open Chrome
    browser = p.chromium.connect_over_cdp("http://localhost:9222")
    
    # 2. Grab the first open tab
    context = browser.contexts[0]
    page = context.pages[0]
    
    # 3. THE MAGIC COMMAND: This opens the Codegen/Inspector 
    # attached to your real, live browser tab.
    page.pause()