import re
from playwright.sync_api import sync_playwright, Page

# Automatically navigates to the job postings (currently goes to fall, needs to change to work for any season)
def navigate_to_postings(page: Page):
    print("Navigating menu...")
    page.get_by_role("button", name="Toggle Main Menu").click()
    
    page.get_by_role("listitem").filter(
        has_text="keyboard_arrow_down Co-op Co-"
    ).get_by_label("Toggle Dropdown").click()
    
    print("Opening job postings...")
    page.get_by_role("link", name="Job postings", exact=True).click()
    
    # Clicking the specific "Fall" filter
    page.get_by_role("link", name="-Fall - all jobs open to me").click()

def open_jobs(page: Page):
    # Defines the postings as a locator object for easy navigation
    table = page.locator("#postingsTable")

    # Focuses on only the button objects in the table
    job_buttons = table.get_by_role("button").all()

    # Go through the rows and 
    i = 0
    for job in job_buttons:
        if job.inner_text().lower() != 'apply':
            continue
        # temporary for testing
        if i == 7:
            break
        print(i)
        i += 1
        print(f"Opening job {i}...")
        # Now you're only clicking buttons inside the grid
        with page.expect_popup() as job_info:
            job.click()
        new_tab = job_info.value
        new_tab.wait_for_load_state()

        # Takes screenshot for debug purposes
        new_tab.screenshot(path=f"job_screenshots/job{i}.png")
        print(f"job {i} screenshot saved successfully!")
        
        new_tab.close()


def main():
    with sync_playwright() as p:
        # 1. Connect to your ALREADY LOGGED IN browser
        browser = p.chromium.connect_over_cdp("http://localhost:9222")
        
        # 2. Grab the existing page/tab
        context = browser.contexts[0]
        page = context.pages[0] 
        
        # uncomment this if you want it to start from the main page
        #navigate_to_postings(page)
        open_jobs(page)

if __name__ == "__main__":
    main()


