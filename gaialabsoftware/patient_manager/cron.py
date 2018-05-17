
import os
from django.core import management
from django.conf import settings
#from django_cron import CronJobBase, Schedule

# class BackupDatabaseDropBox(CronJobBase):
# 	RUN_EVERY_MINS = 1 # every 5 min

# 	schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
# 	code = 'patient_manager.DropboxBackup'    # a unique code


# 	def do(self):
# 		management.call_command('dbbackup')    # do your thing here

def BackupDatabaseDropBox():
	management.call_command('dbbackup')
