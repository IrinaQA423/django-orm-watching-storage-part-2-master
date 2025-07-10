from django.utils.timezone import localtime, now

SECONDS_IN_ONE_HOUR = 3600
SECONDS_IN_ONE_MINUTE = 60
STRANGE_VISIT_THRESHOLD = SECONDS_IN_ONE_HOUR

def format_duration(duration):
    seconds = duration.total_seconds()

    hours = int(seconds // SECONDS_IN_ONE_HOUR)
    minutes = int((seconds % SECONDS_IN_ONE_HOUR) // SECONDS_IN_ONE_MINUTE)
    seconds = int(seconds % SECONDS_IN_ONE_MINUTE)
    return f"{hours}:{minutes:02d}:{seconds:02d}"


def get_visit_duration(visit):

    if not visit.leaved_at:
        return None
    return localtime(visit.leaved_at) - localtime(visit.entered_at)


def get_duration(visit):

    if not visit.entered_at.tzinfo:

        from django.utils.timezone import get_current_timezone
        entered_at = visit.entered_at.replace(tzinfo=get_current_timezone())
    else:
        entered_at = visit.entered_at

    current_time = now()
    return current_time - entered_at


def is_visit_strange(duration):

    if not duration:
        return False
    return duration.total_seconds() > STRANGE_VISIT_THRESHOLD
