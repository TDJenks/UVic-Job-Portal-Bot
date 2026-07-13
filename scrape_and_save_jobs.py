import re
import json
from playwright.sync_api import sync_playwright, Page

job_dict_for_json = {}

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
    organization = page.locator(".panel-body").first.get_by_role("cell").all()
    organization_name = organization[1].inner_text()
    print(organization_name)

    # This is the form of a list where the first index is something like "Job Name"
    # and the second index describe that previous index like "Awesome software co-op"
    job_info = page.locator("div:nth-child(3) > .panel-body").first.get_by_role("cell").all()
    job_attribute_names = [attribute_name.inner_text() for attribute_name in job_info[::2]]
    job_attribute_details = [attribute_detail.inner_text() for attribute_detail in job_info[1::2]]
    
    job_info_dict = dict(zip(job_attribute_names, job_attribute_details))

    # Saves job as 'organization_name%%job_title : job_info
    job_dict_for_json[f'{organization_name}%%{job_info_dict['Job Title:']}'] = job_info_dict


def scrape_jobs(page: Page):
    table = page.locator("#postingsTable")

    job_buttons = table.get_by_role("button").all()

    # Go through the rows and 
    i = 0
    for job_button in job_buttons:
        if job_button.inner_text().lower() != 'apply':
            continue

        # temporary for testing
        # if i == 5:
        #     break
        i += 1

        print(f"Opening job {i}...")

        with page.expect_popup() as new_tab:
            job_button.click()
        job_posting = new_tab.value
        job_posting.wait_for_load_state()

        save_job_info(job_posting)
        
        job_posting.close()


def main():
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp("http://localhost:9222")
        context = browser.contexts[0]
        page = context.pages[0] 

        # uncomment this if you want it to start from the main page (outdated)
        #navigate_to_postings(page)

        scrape_jobs(page)

        with open('jobs.json', 'w') as file:
            json.dump(job_dict_for_json, file, indent=4)


if __name__ == "__main__":
    main()


