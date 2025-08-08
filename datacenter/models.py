from django.db import models
from django.utils.timezone import localtime


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
        entry_time = localtime(self.entered_at)
        exit_time = localtime(self.leaved_at)
        return (exit_time - entry_time).total_seconds()

    def is_visit_long(self, minutes = 60):
        return self.get_duration() > minutes * 60


def format_duration(total_seconds: int):
    SECONDS_IN_HOUR = 3600
    SECONDS_IN_MINUTE = 60
    hours_passed = int(total_seconds // SECONDS_IN_HOUR)
    minutes_passed = int((total_seconds % SECONDS_IN_HOUR) / SECONDS_IN_MINUTE)
    seconds_passed = int((total_seconds % SECONDS_IN_HOUR) % SECONDS_IN_MINUTE)
    return f"{hours_passed}:{minutes_passed}:{seconds_passed}"
