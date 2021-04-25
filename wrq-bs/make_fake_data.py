import sql
import random
from apscheduler.schedulers.blocking import BlockingScheduler

def make_fake_data():
    t = 0
    v1 = round(random.uniform(0,3.3), 2)
    v2 = round(random.uniform(0,3.3), 2)
    data = sql.sql_dict(t, v1, v2).__dict__
    return data

def submit_fake_data(data):
    sql.mysql().insert_data(data)

def job():
    submit_fake_data(make_fake_data())

def startjob():
    scheduler = BlockingScheduler()
    scheduler.add_job(job, 'interval', seconds = 3)
    scheduler.start()

startjob()