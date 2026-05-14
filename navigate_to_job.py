import re
from playwright.sync_api import sync_playwright, Page

# This is your recorded logic (I moved it into a standard function)
def navigate_to_postings(page: Page):
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

def open_jobs(page: Page):
    # 1. Target the table specifically
    table = page.locator("#postingsTable")

    # 2. Find buttons ONLY inside that table
    job_buttons = table.get_by_role("button").all()

    i = 0
    for job in job_buttons:
        if job.inner_text().lower() == 'apply':
            continue
        # temporary for testing
        if i == 7:
            break
        
        i += 1
        print(f"Opening job {i}...")
        # Now you're only clicking buttons inside the grid
        with page.expect_popup() as job_info:
            job.click()
        new_tab = job_info.value
        new_tab.wait_for_load_state()

        # proof of function, for testing
        # new_tab.screenshot(path=f"job_screenshots/job{i}.png")
        # print(f"job {i} screenshot saved successfully!")
        
        new_tab.close()


def main():
    with sync_playwright() as p:
        # 1. Connect to your ALREADY LOGGED IN browser
        browser = p.chromium.connect_over_cdp("http://localhost:9222")
        
        # 2. Grab the existing page/tab
        context = browser.contexts[0]
        page = context.pages[0] 
        
        # 3. Run your logic
        navigate_to_postings(page)
        open_jobs(page)

if __name__ == "__main__":
    main()


