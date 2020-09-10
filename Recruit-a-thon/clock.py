from apscheduler.schedulers.blocking import BlockingScheduler
from mail import email_content

sched = BlockingScheduler()

@sched.scheduled_job('interval', minutes=1)
def timed_job():
    email_content(3,'rexdivakar@hotmail.com')
    
timed_job()