from datacenter.models import Visit
from django.shortcuts import render
from django.utils.timezone import localtime
from datacenter.duration_helpers import is_visit_strange, get_duration,  format_duration


def storage_information_view(request):
    active_visits = Visit.objects.filter(leaved_at=None)
    non_closed_visits = []

    for visit in active_visits:
        duration = get_duration(visit) 
        
        try:
            formatted_duration = format_duration(duration)
            non_closed_visits.append({
                'who_entered': visit.passcard.owner_name,
                'entered_at': localtime(visit.entered_at),
                'duration': formatted_duration,
                'is_strange': is_visit_strange(duration),
            })
        except (AttributeError, TypeError):
            
            continue

    context = {
        'non_closed_visits': non_closed_visits,
    }
    return render(request, 'storage_information.html', context)
