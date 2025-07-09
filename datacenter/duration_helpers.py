from django.utils.timezone import localtime, now


def format_duration(duration):
    seconds = duration.total_seconds()

    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = int(seconds % 60)
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
    return duration.total_seconds() > 3600
