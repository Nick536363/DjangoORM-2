from datacenter.models import Passcard
from datacenter.models import Visit
from django.shortcuts import render
from django.utils.timezone import localtime
from datetime import datetime
from datacenter.models import Visit


def storage_information_view(request):
    # Программируем здесь
    time_now =  datetime.now()
    for visit in Visit.objects.all():
        datetime_enter = str(localtime(visit.entered_at)).split()
        date_enter = datetime_enter[0].split("-")
        time_enter = datetime_enter[1].split("+")[0].split(":")
        datetime_enter = datetime(int(date_enter[0]), int(date_enter[1]), int(date_enter[2]), int(time_enter[0]), int(time_enter[1]), int(time_enter[2]))
        time_delta = (time_now - datetime_enter).total_seconds()
        hours_passed = int(time_delta // 3600)
        minutes_passed = int((time_delta % 3600) / 60)
        seconds_passed = int((time_delta % 3600) % 60)
        print("\n\n",visit.passcard.owner_name)
        print("Зашел в хранилище:\n",localtime(visit.entered_at),"\nНаходиться в хранилище:\n",f"{hours_passed}:{minutes_passed}:{seconds_passed}")

    non_closed_visits = [
        {
            'who_entered': 'Richard Shaw',
            'entered_at': '11-04-2018 25:34',
            'duration': '25:03',
        }
    ]
    context = {
        'non_closed_visits': non_closed_visits,  # не закрытые посещения
    }
    return render(request, 'storage_information.html', context)
