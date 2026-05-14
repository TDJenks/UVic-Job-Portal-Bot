from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    # Launch a browser (headless=False lets you see it happen)
    browser = p.chromium.launch(headless=False)
    
    # Open a new page
    page = browser.new_page()
    
    # Navigate to a website
    page.goto("https://www.google.com")
    
    # Take a screenshot
    page.screenshot(path="example.png")
    
    print(f"Page Title: {page.title()}")
    
    browser.close()