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
    
    page.get_by_role("link", name="-Fall - all jobs open to me").click()


def save_job_info(page: Page):
    organization_info = page.locator(".panel-body").first.get_by_role("cell").all()
    print(organization_info[1].inner_text())

    # This is the form of a list where the first index is something like "Job Name"
    # and the second index describe that previous index like "Awesome software co-op"
    job_info = page.locator("div:nth-child(3) > .panel-body").first.get_by_role("cell").all()
    job_attribute_names = [attribute_name.inner_text() for attribute_name in job_info[::2]]
    job_attribute_details = [attribute_detail.inner_text() for attribute_detail in job_info[1::2]]
    
    job_info_dict = dict(zip(job_attribute_names, job_attribute_details))

    i = 0
    for name, detail in job_info_dict.items():
        i += 1
        print(f"#{i} {name} | #{i} {detail}")


    
    # job_info_dict = dict(zip(job_posting[::2], job_posting[1::2]))

    # for k, v in job_info_dict:
    #     print(f"key: {k} -- value: {v}")



def scrape_jobs(page: Page):
    table = page.locator("#postingsTable")

    job_buttons = table.get_by_role("button").all()

    # Go through the rows and 
    i = 0
    for job_button in job_buttons:
        if job_button.inner_text().lower() != 'apply':
            continue

        # temporary for testing
        if i == 1:
            break

        i += 1
        print(f"Opening job {i}...")

        with page.expect_popup() as new_tab:
            job_button.click()
        job_posting = new_tab.value
        job_posting.wait_for_load_state()

        # Takes screenshot for debug purposes
        job_posting.screenshot(path=f"job_screenshots/job{i}.png")
        print(f"job {i} screenshot saved successfully!")

        # TODO
        # Create a function that can:
        # - Turn job posting into a readable table
        # - For each row, store the text as a json
        save_job_info(job_posting)
        
        job_posting.close()


def main():
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp("http://localhost:9222")
        context = browser.contexts[0]
        page = context.pages[0] 
        
        # uncomment this if you want it to start from the main page
        #navigate_to_postings(page)

        scrape_jobs(page)


if __name__ == "__main__":
    main()


