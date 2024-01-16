import os

from celery import Celery
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')

app = Celery('app')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()


@app.task(bind=True)
def send_email(self, email: str, context: dict):
    order_id = context["order_id"]
    msg = EmailMessage(
        subject=f'Оформление заказа №{order_id}',
        body=render_to_string('users/order-email.html', context=context),
        to=(email,)
    )

    msg.content_subtype = 'html'
    msg.send()

    return f'Order-id:{order_id}, Email:{email}'
