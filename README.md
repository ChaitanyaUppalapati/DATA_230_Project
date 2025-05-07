# Modern Job Market: Insights from LinkedIn Job Postings

## Introduction
What: Analyze LinkedIn job postings to uncover trends in job roles, skills, and industries.

Why: Empower job seekers, recruiters, and educators with data-driven insights about the evolving job market.

Who: Targeted at data analysts, career planners, workforce developers, and policy makers.

## Data Ingestion Workflow
- This project outlines the end-to-end pipeline for extracting, processing, and visualizing job postings data from LinkedIn. 
- Using Python and Selenium, real-time job data is scraped and standardized before undergoing an ETL process. 
- The cleaned dataset is then explored and visualized using tools like Seaborn, Plotly, Power BI, and Tableau to derive meaningful labor market insights.

## Setup
Add your LinkedIn credentials to `logins.csv`
```bash
python -m venv venv
source env/bin/activate
pip install -r requirements.txt
```

## Search Retriever
### Purpose:
Retrieves basic information about job postings listed on LinkedIn’s search results page.

#### How it works:
- Logs into LinkedIn using credentials stored in a logins.csv file.
- Navigates to the job search page using Selenium WebDriver (Edge or Chrome).
- Captures job posting IDs, job titles, and flags for promoted (sponsored) jobs.
- Stores these results in a local SQLite database.

#### To run use the below command
```bash 
python search_retriever.py
```

## Details Retriever
### Purpose:
Fetches full job descriptions and metadata for each job ID obtained by search_retriever.py.

#### How it works:
- Loads job IDs marked as scraped = 0 in the database.
- For each job ID, sends an authenticated API request to LinkedIn’s job details endpoint using requests.Session.
- Parses the JSON response to extract nested fields like job description, seniority, employment type, etc.
- Cleans the data (via helpers.py) and inserts it into the SQLite database.

#### To run use the below command
```bash 
python details_retriever.py
```

## Export data from database
The project uses `linkedin_jobs.db` sqlite database to store the scraped job information, this can be exported to csv using the `to_csv.py` script.

#### To run use the below command
```bash 
python to_csv.py --folder <destination folder> --database <linkedin_jobs.db>
```

## Analytics
All of the analytics is done under the `notebooks` folder, the data is exported as csv and uses matplotlib, pandas 
seaborn etc for visualization.

```bash
notebooks
├── Analytics.py
├── cleaned
│   ├── cleaned_benefits.csv
│   ├── cleaned_companies.csv
│   ├── cleaned_company_industries.csv
│   ├── cleaned_company_specialities.csv
│   ├── cleaned_employee_counts.csv
│   ├── cleaned_industries.csv
│   ├── cleaned_job_industries.csv
│   ├── cleaned_job_postings.csv
│   ├── cleaned_job_skills.csv
│   ├── cleaned_salaries.csv
│   └── cleaned_skills.csv
├── data
│   ├── companies
│   ├── jobs
│   ├── mappings
│   └── postings.csv
└── job_analysis.ipynb
```
![Power BI Dashboard](docs/Linkedin%20data.png)
