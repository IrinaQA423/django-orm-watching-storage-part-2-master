from django.db import models
from django.utils.timezone import localtime
from datetime import datetime
from datacenter.duration_helpers import format_duration 


class Passcard(models.Model):
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=True)
    passcode = models.CharField(max_length=200, unique=True)
    owner_name = models.CharField(max_length=255)

    def __str__(self):
        if self.is_active:
            return self.owner_name
        return f'{self.owner_name} (inactive)'


class Visit(models.Model):
    created_at = models.DateTimeField(auto_now=True)
    passcard = models.ForeignKey(Passcard, on_delete=models.CASCADE)
    entered_at = models.DateTimeField()
    leaved_at = models.DateTimeField(null=True)

    def __str__(self):
        return '{user} entered at {entered} {leaved}'.format(
            user=self.passcard.owner_name,
            entered=self.entered_at,
            leaved=(
                f'leaved at {self.leaved_at}'
                if self.leaved_at else 'not leaved'
            )
        )


def get_duration(visit):
    
    if not visit.entered_at.tzinfo:
        
        from django.utils.timezone import get_current_timezone
        entered_at = visit.entered_at.replace(tzinfo=get_current_timezone())
    else:
        entered_at = visit.entered_at

    current_time = datetime.now()
    return current_time - entered_at


def get_visits_by_owner_name(owner_name):
    
    visits = Visit.objects.filter(passcard__owner_name=owner_name)

    visits = visits.order_by('-entered_at')

    return visits


def get_long_visits(min_duration=60):
    
    visits = Visit.objects.all()

    long_visits = []
    for visit in visits:
        duration = get_duration(visit)
        duration_minutes = duration.total_seconds() / 60

        if duration_minutes > min_duration:
            formatted_duration = format_duration(duration)
            visit_info = {
                'owner_name': visit.passcard.owner_name,
                'entered_at': localtime(visit.entered_at).strftime('%Y-%m-%d %H:%M:%S'),
                'duration': formatted_duration,
                'leaved_at': localtime(visit.leaved_at).strftime('%Y-%m-%d %H:%M:%S') if visit.leaved_at else 'still inside'
            }
            long_visits.append(visit_info)

    return long_visits


def get_long_visits_by_owner(owner_name, min_duration=60):
    
    visits = Visit.objects.filter(passcard__owner_name=owner_name)

    long_visits = []
    for visit in visits:
        duration = get_duration(visit)
        duration_minutes = duration.total_seconds() / 60

        if duration_minutes > min_duration:
            formatted_duration = format_duration(duration)
            visit_info = {
                'entered_at': localtime(visit.entered_at).strftime('%Y-%m-%d %H:%M:%S'),
                'duration': formatted_duration,
                'leaved_at': localtime(visit.leaved_at).strftime('%Y-%m-%d %H:%M:%S') if visit.leaved_at else 'еще в хранилище'
            }
            long_visits.append(visit_info)

    return long_visits
