import re
from playwright.sync_api import sync_playwright, Page

# This is your recorded logic (I moved it into a standard function)
def run_portal_actions(page: Page):
    print("Navigating menu...")
    page.get_by_role("button", name="Toggle Main Menu").click()
    
    # UVic's portal can be slow, so we wait for the dropdown
    page.get_by_role("listitem").filter(
        has_text="keyboard_arrow_down Co-op Co-"
    ).get_by_label("Toggle Dropdown").click()
    
    print("Opening job postings...")
    page.get_by_role("link", name="Job postings", exact=True).click()
    
    # Clicking the specific "Fall" filter
    page.get_by_role("link", name="-Fall - all jobs open to me").click()
    
    # Handling the popup for a specific job
    print("Opening job details...")
    with page.expect_popup() as page1_info:
        page.get_by_role("button", name="Hydro-climatic data analysis").click()
    
    page1 = page1_info.value
    page1.wait_for_load_state() # Ensure the popup is fully loaded
    print(f"Now viewing: {page1.title()}")

def main():
    with sync_playwright() as p:
        # 1. Connect to your ALREADY LOGGED IN browser
        browser = p.chromium.connect_over_cdp("http://localhost:9222")
        
        # 2. Grab the existing page/tab
        context = browser.contexts[0]
        page = context.pages[0] 
        
        # 3. Run your logic
        run_portal_actions(page)

if __name__ == "__main__":
    main()
