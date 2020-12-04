# Vlado Situm
# CNA330 Quarter Fall 2020 at RTC Renton
# This is group project of three members (Vlado, Abdi and Dorin).
# Liviu Patrasco helped us to write the code. The project will take jobs data from
# the US Bureau of Labor and Statistics and save it into a database for further quiring to make plots
#and graphs to help understand the average salaries per occupation, and the relation between them in order 
# to help students select preferred occupation.

import pandas as pd
from sqlalchemy import create_engine



# database config
db_host = 'localhost'
db_username = 'root'
db_password = ''
db_port = '3306'
db_name = 'sqlnewdb'

"""db_host = 'url'
db_username = 'admin'
db_password = 'root1root'
db_port = '3306'
db_name = 'CNA330' """

# The url for the source web page
html_source_url = "https://www.bls.gov/oes/2019/may/oes_nat.htm"


# function to create a database connection
def connect_to_sql():
    connection_string = "mysql+pymysql://{}:{}@{}:{}/{}".format(db_username, db_password, db_host, db_port, db_name)
    sql_engine = create_engine(connection_string)
    db_connection = sql_engine.connect()
    print('Connected to database %s OK' % db_name)
    return db_connection


def remove_empty_lines(job_data):
    job_data = job_data.dropna()
    job_data = job_data.where(pd.notnull(job_data), None)
    print('Cleaned empty lines')
    return job_data


# Read the data from web
jobs = pd.read_html(html_source_url)[1]
print('Read HTML page OK')

# Remove empty rows
jobs = remove_empty_lines(jobs)

# Remove duplicate rows
jobs = jobs.drop_duplicates()

# Convert 'dollar' columns from '$2000,000.00' to float 2000000
jobs['Median hourly wage'] = jobs['Median hourly wage'].replace('[$,()]', '', regex=True)
jobs['Median hourly wage'] = jobs['Median hourly wage'].astype(float)
jobs['Annual mean wage'] = jobs['Annual mean wage'].replace('[$,()]', '', regex=True)
jobs['Annual mean wage'] = jobs['Annual mean wage'].astype(float)
jobs['Mean hourly wage'] = jobs['Mean hourly wage'].replace('[$,()]', '', regex=True)
jobs['Mean hourly wage'] = jobs['Mean hourly wage'].astype(float)
jobs['Employment per 1,000 jobs'] = jobs['Employment per 1,000 jobs'].round(decimals=3)
print('Cleaned and converted data')

# Remove boring columns
jobs = jobs.drop(axis='columns', labels='Occupation code')
print('Removed an unneeded column')

# Rename columns: shorten if too long, remove '(' and ')' characters, replace ' ' spaces with '_'
jobs.rename(columns=lambda x: x[:25].strip(), inplace=True)
jobs.rename(columns=lambda x: x.replace(' ', '_').replace('(', '').replace(')', ''), inplace=True)
print('Renamed columns: shortened to 25 characters and removed spaces')

# Insert the data into mysql table, replace if already exists
jobs.to_sql('job_salaries', con=connect_to_sql(), if_exists='replace', index=False)
print('Data from {} was successfully saved in the {} database'.format(html_source_url, db_name))

print("Done!")
