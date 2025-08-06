from django.db import models
from django.utils.timezone import localtime
from datetime import datetime


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

    def get_duration(self):
        if self.leaved_at == None:
            leaved_at = datetime.now()
        else:
            datetime_leave = str(localtime(self.leaved_at)).split()
            date_leave = datetime_leave[0].split("-")
            time_leave = datetime_leave[1].split("+")[0].split(":")
            leaved_at = datetime(int(date_leave[0]), int(date_leave[1]), int(date_leave[2]), int(time_leave[0]), int(time_leave[1]), int(time_leave[2]))
        datetime_enter = str(localtime(self.entered_at)).split()
        date_enter = datetime_enter[0].split("-")
        time_enter = datetime_enter[1].split("+")[0].split(":")
        datetime_enter = datetime(int(date_enter[0]), int(date_enter[1]), int(date_enter[2]), int(time_enter[0]), int(time_enter[1]), int(time_enter[2]))
        return (leaved_at - datetime_enter).total_seconds()

    def is_visit_long(self, minutes = 60):
        return True if self.get_duration() > minutes * 60 else False


def format_duration(total_seconds: int):
    hours_passed = int(total_seconds // 3600)
    minutes_passed = int((total_seconds % 3600) / 60)
    seconds_passed = int((total_seconds % 3600) % 60)
    return (str(hours_passed) if hours_passed >= 10 else "0"+str(hours_passed)) +":"+ (str(minutes_passed) if minutes_passed >= 10 else "0"+str(minutes_passed)) +":"+ (str(seconds_passed) if seconds_passed >= 10 else "0"+str(seconds_passed))
