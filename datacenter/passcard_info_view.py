from datacenter.models import Passcard
from datacenter.models import Visit
from django.shortcuts import render, get_object_or_404
from django.utils.timezone import localtime


def get_visit_duration(visit):
    
    if not visit.leaved_at:
        return None
    return localtime(visit.leaved_at) - localtime(visit.entered_at)


def format_visit_time(visit_time):
    
    return localtime(visit_time).strftime('%d-%m-%Y %H:%M')


def is_visit_strange(duration):
    
    if not duration:
        return False
    return duration.total_seconds() > 3600


def prepare_visit_info(visit):
    
    duration = get_visit_duration(visit)

    return {
        'entered_at': format_visit_time(visit.entered_at),
        'duration': str(duration) if duration else 'Не завершен',
        'is_strange': is_visit_strange(duration)
    }


def get_passcard_visits(passcard):
    
    visits = Visit.objects.filter(passcard=passcard)
    return [prepare_visit_info(visit) for visit in visits]


def passcard_info_view(request, passcode):
    
    passcard = get_object_or_404(Passcard, passcode=passcode)

    context = {
        'passcard': passcard,
        'this_passcard_visits': get_passcard_visits(passcard)
    }
    return render(request, 'passcard_info.html', context)
