import getpass
import os
import crontab
import json


print(getpass.getuser())
cron = crontab.CronTab(getpass.getuser())
with open("app_info.json", "r") as app_info_file:
    info = json.load(app_info_file)
    job = cron.new(command=f'. {os.getcwd()}/run_autoresponder.sh')
job.setall('*/15 * * * *')  # time interval between autoresponse sending
cron.write()
