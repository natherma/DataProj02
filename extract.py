import requests
from bs4 import BeautifulSoup      # type: ignore
from datetime import date 
import pandas as pd
import os


today = date.today()

url = "https://www.linkedin.com/jobs/search?keywords=data&location=India&geoId=102713980&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0"
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')


if os.path.exists('linkedin_jobs.csv'):
    df = pd.read_csv('linkedin_jobs.csv')
    job_list = df.to_dict('records')
else:
    job_list = []

def extract_job_data(soup, jobs):
    results_container = soup.find('ul', class_='jobs-search__results-list')
    
    if not results_container:
        print("No jobs found. You might be blocked or the class name changed.")
        return

    for item in results_container.find_all('li', recursive=False):
        try:
            # Using .select_one is often cleaner for CSS classes
            title = item.select_one('.base-search-card__title').text.strip()
            company = item.select_one('.base-search-card__subtitle').text.strip()
            location = item.select_one('.job-search-card__location').text.strip()
            description = item.select_one('.base-search-card__snippet').text.strip() if item.select_one('.base-search-card__snippet') else 'N/A'
            
            time_tag = item.find('time')
            if time_tag and time_tag.has_attr('datetime'):
                date_posted = time_tag['datetime']
                job = {
                        'title': title,
                        'company': company,
                        'location': location,
                        'date_posted': date_posted,
                        'description': description
                    }
                if job not in jobs:
                        jobs.append(job)
        except Exception as e:
            continue


extract_job_data(soup, job_list)


df = pd.DataFrame(job_list)
df.to_csv('linkedin_jobs.csv', index=False)