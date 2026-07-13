### Notes

#### Recently Done:
changed json format to 'company%%job' : job_info
Started rank_jobs.py - created qualification dictionary => 'company%%job' : qualifications

#### Next steps:
Figure out how to use qualification dictionary to work with sentence-transformers
- use new line delimeters to break up individual qualifications (might not work for all jobs)



##### Vector Embedding
[ ] 1. Environment Setup: Open your IDE and pip install sentence-transformers.

[ ] 2. Data Ingestion: Use json.load() to read your job file, and paste your raw resume text into a string variable.

[ ] 3. Data Flattening: Run a clean loop to dig into your nested JSON (Company -> Job Title -> Details) and glue the Description and Qualifications together into one long text block per job.

[ ] 4. The Math Matrix: Let the model encode both your resume and the job blocks into vectors, run the similarity score, and sort the results from highest to lowest match.

