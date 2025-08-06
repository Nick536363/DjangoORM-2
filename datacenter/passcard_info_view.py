from datacenter.models import Passcard
from datacenter.models import Visit, format_duration
from django.shortcuts import render, get_object_or_404


def passcard_info_view(request, passcode):
    passcard = get_object_or_404(Passcard, passcode=passcode)
    this_passcard_visits = []
    # Программируем здесь
    for visit in Visit.objects.filter(passcard=passcard):
        this_passcard_visits.append({
            "entered_at": visit.entered_at,
            "duration": format_duration(visit.get_duration()),
            "is_strange": visit.is_visit_long()
        })
    context = {
        'passcard': passcard,
        'this_passcard_visits': this_passcard_visits
    }
    return render(request, 'passcard_info.html', context)
