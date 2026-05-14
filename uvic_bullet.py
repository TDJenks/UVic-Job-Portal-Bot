from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    # Instead of launching, connect to the existing instance
    browser = p.chromium.connect_over_cdp("http://localhost:9222")
    page = browser.contexts[0].pages[0]
    page.goto("https://learninginmotion.uvic.ca/myAccount/dashboard.htm")
    # Take a screenshot
    page.screenshot(path="example.png", timeout=5000, animations="disabled")
    
    print(f"Page Title: {page.title()}")
    
    browser.close()