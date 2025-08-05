from datacenter.models import Passcard
from datacenter.models import Visit
from django.shortcuts import render
from django.utils.timezone import localtime
from datetime import datetime
from datacenter.models import Visit


def get_duration(visit: Visit):
    time_now =  datetime.now()
    datetime_enter = str(localtime(visit.entered_at)).split()
    date_enter = datetime_enter[0].split("-")
    time_enter = datetime_enter[1].split("+")[0].split(":")
    datetime_enter = datetime(int(date_enter[0]), int(date_enter[1]), int(date_enter[2]), int(time_enter[0]), int(time_enter[1]), int(time_enter[2]))
    return (time_now - datetime_enter).total_seconds()


def format_duration(total_seconds: int):
    hours_passed = int(total_seconds // 3600)
    minutes_passed = int((total_seconds % 3600) / 60)
    seconds_passed = int((total_seconds % 3600) % 60)
    return (str(hours_passed) if hours_passed >= 10 else "0"+str(hours_passed)) +":"+ (str(minutes_passed) if minutes_passed >= 10 else "0"+str(minutes_passed)) +":"+ (str(seconds_passed) if seconds_passed >= 10 else "0"+str(seconds_passed))


def storage_information_view(request):
    # Программируем здесь
    non_closed_visits = []
    for visit in Visit.objects.filter(leaved_at=None):
        non_closed_visits.append({
            'who_entered': visit.passcard.owner_name,
            'entered_at': visit.entered_at,
            'duration': format_duration(get_duration(visit)),
        })

    context = {
        'non_closed_visits': non_closed_visits,  # не закрытые посещения
    }
    return render(request, 'storage_information.html', context)
