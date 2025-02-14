from django_cron import CronJobBase, Schedule
from .models import DateMatch

class MyCronJob(CronJobBase):
    RUN_EVERY_MINS = 1 # every 2 hours

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'restaurantapi.my_cron_job'    # a unique code

    def do(self):
        DateMatch.objects.all().delete()