from django.utils.timezone import localtime, now, get_current_timezone

SECONDS_IN_ONE_HOUR = 3600
SECONDS_IN_ONE_MINUTE = 60
STRANGE_VISIT_THRESHOLD = SECONDS_IN_ONE_HOUR


def format_duration(duration):
    try:
        seconds = int(duration.total_seconds())
    except AttributeError:  
        return "Не завершен"

    hours = int(seconds // SECONDS_IN_ONE_HOUR)
    minutes = int((seconds % SECONDS_IN_ONE_HOUR) // SECONDS_IN_ONE_MINUTE)
    seconds = int(seconds % SECONDS_IN_ONE_MINUTE)
    return f"{hours}:{minutes:02d}:{seconds:02d}"


def get_duration(visit):
    
    if not visit.entered_at:
        return None  

    if not visit.entered_at.tzinfo:
        entered_at = visit.entered_at.replace(tzinfo=get_current_timezone())
    else:
        entered_at = visit.entered_at

    leaved_at = visit.leaved_at if visit.leaved_at else now()
    if not leaved_at.tzinfo:
        leaved_at = leaved_at.replace(tzinfo=get_current_timezone())
    
    return leaved_at - entered_at


def is_visit_strange(duration):

    return duration and duration.total_seconds() > STRANGE_VISIT_THRESHOLD
