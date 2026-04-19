import pandas as pd
from sqlalchemy import create_engine


jobs_df = pd.read_csv('linkedin_jobs.csv')

big4 = ['Deloitte', 'EY', 'PwC', 'KPMG']
service_based = ['TCS', 'Infosys', 'Wipro', 'HCLTech']
fang = ['Google', 'Microsoft', 'Amazon', 'Facebook', 'Apple']

jobs_df['company_category'] = jobs_df['company'].apply(
    lambda x: 'Big 4' if any(b in x for b in big4) 
    else 'Service-based' if any(s in x for s in service_based)
    else 'FAANG' if any(f in x for f in fang)

    else 'Other'
)

DATABASE_URL = "postgresql+psycopg2://postgres:12345678@localhost:5432/practice"
engine = create_engine(DATABASE_URL)

# Load data
jobs_df.to_sql('job_listings', engine, if_exists='replace', index=False)

print("Data loaded to PostgreSQL")

