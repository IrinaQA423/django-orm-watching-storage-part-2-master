from datacenter.models import Visit, format_duration
from django.shortcuts import render
from django.utils.timezone import localtime, now
from datacenter.passcard_info_view import is_visit_strange


def storage_information_view(request):

    active_visits = Visit.objects.filter(leaved_at=None)

    non_closed_visits = []
    for visit in active_visits:
        if not visit.entered_at.tzinfo:
            # Если дата naive, преобразуем её в aware
            from django.utils.timezone import get_current_timezone
            entered_at = visit.entered_at.replace(tzinfo=get_current_timezone())
        else:
            entered_at = visit.entered_at

        current_time = now()
        duration = current_time - entered_at

        non_closed_visits.append({
            'who_entered': visit.passcard.owner_name,
            'entered_at': localtime(entered_at),
            'duration': format_duration(duration),
            'is_strange': is_visit_strange(duration),
        })

    context = {
        'non_closed_visits': non_closed_visits,
    }
    return render(request, 'storage_information.html', context)
