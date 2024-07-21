from datetime import datetime, timezone, timedelta
from celery import shared_task
from django.core.mail import send_mail

from config import settings
from materials.models import Course, SubForCourseUpdate
from users.models import User


@shared_task
def sending_mails(pk):
    course = Course.objects.get(pk=pk)
    subscribers = SubForCourseUpdate.objects.filter(course=pk)

    send_mail(
        subject=f'Курс {course} обновлен',
        message=f'Курс {course} на который вы подписаны обновлен',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[subscribers.user.email],
    )


@shared_task
def deactivate_user():
    user = User.objects.filter(is_active=True)
    now = datetime.now(timezone.utc)
    for user in user:
        if user.last_login and now - user.last_login > timedelta(days=0):
            # user.is_active = False
            # user.save()
            print(f'{user.username} is deactivated')
