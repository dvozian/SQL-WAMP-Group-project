# Vlado Situm
# CNA330 Quarter Fall 2020 at RTC Renton
# This is group project of three members (Vlado, Abdi and Dorin).
# Liviu Patrasco helped us to write the code. The project will take jobs data from 
# the US Bureau of Labor and Statistics and save it into a database for further quiring to make plots
# and graphs to help understand the average salaries per occupation, and the relation between them in order
# to help students select preferred occupation.

import pandas as pd
from sqlalchemy import create_engine
import matplotlib.pyplot as pp
import sys


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


# function to create a database connection
def connect_to_sql():
    print('Trying to connect to database: %s' % db_name)
    connection_string = "mysql+pymysql://{}:{}@{}:{}/{}".format(db_username, db_password, db_host, db_port, db_name)
    sql_engine = create_engine(connection_string)
    db_connection = sql_engine.connect()
    print('Connected to database %s OK' % db_name)
    return db_connection


def get_jobs_from_database(search_keyword):
    search_sql = "select * from job_salaries " \
                 "where lower(Occupation_title_click_o) like '%" + search_keyword + \
                 "%' limit 30"
    print(search_sql)
    jobs = pd.read_sql(search_sql, connect_to_sql())
    print('Read data from the database')
    return jobs


def plot_jobs(jobs):
    print('Plotting...')
    jobs.plot(x="Occupation_title_click_o", y='Annual_mean_wage', kind='barh')
    jobs.plot(x="Employment_per_1,000_jobs", y='Occupation_title_click_o', kind='scatter')
    pp.show()


def main():
    if len(sys.argv) > 1:
        search_keyword = sys.argv[1]
    else:
        search_keyword = 'computer'

    jobs = get_jobs_from_database(search_keyword)

    plot_jobs(jobs)


if __name__ == '__main__':
    main()
