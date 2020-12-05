from apps.activity_log.enums import EXP
from apps.activity_log.models import ActivityLog


def create_activity_log(user, type, exp) :
    ActivityLog.objects.create(user=user, exp=exp)
