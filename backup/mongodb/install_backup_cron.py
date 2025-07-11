#!/usr/bin/env python3
from crontab import CronTab
import getpass, os

# 1) Which user’s crontab?
user = getpass.getuser()

# 2) Full path to your bash script
script = '/home/ubuntu/project/flask-app/backup/mongodb/backup.sh'
if not os.path.isfile(script):
    raise FileNotFoundError(f"Backup script not found: {script}")

# 3) Prepare the cron entry
cron = CronTab(user=user)
cron.remove_all(comment='mongo_backup')

job = cron.new(
    command=f'{script} >> /tmp/backup_mongo.log 2>&1',
    comment='mongo_backup'
)

# Schedule: every minute
job.setall('* * * * *')

cron.write()
print(f"Installed cron job for {user}: {job}")
