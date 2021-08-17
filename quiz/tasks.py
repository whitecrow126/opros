from celery import shared_task
from django.utils import timezone


from .models import *

@shared_task
def check_interview():
    for interview in Interview.objects.filter(is_active=True):
        if interview.finish_date < timezone.now().date():
            interview.is_active = False
            interview.save()
