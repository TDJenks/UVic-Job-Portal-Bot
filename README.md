*Ranks jobs on the uvic co-op portal based on skills and experience to optimize job applications*

### How to use
This requires **two** terminals to be running **simultaneously**, as one is used to keep the chrome window open and the other is used to run the playwright script.
This can be done by hitting the plus button in the vs code terminal (top right of terminal window)
 * Use **launch_chrome.bat** and navigate to the home page of the uvic co-op portal
 * Login to the UVic Co-op Portal in the **new chrome window** and navigate to the desired co-op term (fall, spring, summer)
 * Open a second terminal window and run **scrape_and_save_jobs.py**
 * Once completed, using the same window or a different window, run **rank_jobs.py**
