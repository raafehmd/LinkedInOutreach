# compliance_dashboard.py
import datetime
import logging

activities = []

def log_activity(activity):
    activity['timestamp'] = datetime.datetime.now().isoformat()
    activities.append(activity)
    logging.info("Activity logged: %s", activity)

def get_activities():
    return activities
