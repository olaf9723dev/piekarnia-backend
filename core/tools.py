from django.contrib.auth.models import User
from fcm_django.models import FCMDevice
from firebase_admin.messaging import Message, Notification as FCMNotification
from rest_framework.pagination import PageNumberPagination

from core.models import Notification


def create_notification(to: User, title: str, content: str) -> bool:
    Notification.objects.create(
        user=to,
        title=title,
        content=content
    )
    fcm_devices = FCMDevice.objects.filter(user=to)
    for device in fcm_devices:
        device.send_message(
            Message(
                notification=FCMNotification(
                    title=title,
                    body=content
                )
            )
        )
    return True


class CustomPagination(PageNumberPagination):
    page_size = 16
