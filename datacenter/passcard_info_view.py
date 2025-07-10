from datacenter.models import Passcard
from datacenter.models import Visit
from django.shortcuts import render, get_object_or_404
from django.utils.timezone import localtime
from datacenter.duration_helpers import get_duration, is_visit_strange, format_duration


def format_visit_time(visit_time):
    
    return localtime(visit_time).strftime('%d-%m-%Y %H:%M')

def passcard_info_view(request, passcode):
    passcard = get_object_or_404(Passcard, passcode=passcode)
    visits = Visit.objects.filter(passcard=passcard)
    
    this_passcard_visits = []
    for visit in visits:
        duration = get_duration(visit)
        this_passcard_visits.append({
            'entered_at': format_visit_time(visit.entered_at),
            'duration': format_duration(duration) if duration else 'Не завершен',
            'is_strange': is_visit_strange(duration)
        })

    context = {
        'passcard': passcard,
        'this_passcard_visits': this_passcard_visits
    }
    return render(request, 'passcard_info.html', context)