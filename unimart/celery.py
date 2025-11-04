import os
from celery import Celery
from celery.schedules import crontab # Import crontab

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'unimart.settings')

app = Celery('unimart')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks() # This will find your new notifications.tasks

# --- THIS IS THE NEW PART ---
# Define the daily schedule
app.conf.beat_schedule = {
    'send-daily-nudges': {
        'task': 'notifications.tasks.find_old_listings_nudge',
        'schedule': crontab(hour=8, minute=0),  # Runs every morning at 8:00 AM
    },
}
# -----------------------------