import os

from celery import Celery
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

from main.domain.aggregates import Order

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')

app = Celery('app')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()


@app.task(bind=True)
def send_email(self, order_data: dict):
    order = Order.model_validate(order_data)
    msg = EmailMessage(
        subject=f'Оформление заказа №{order.number}',
        body=render_to_string('users/order-email.html', context={'order': order}),
        to=(order.email,)
    )

    msg.content_subtype = 'html'
    msg.send()

    return f'Order-id:{order.number}, Email:{order.email}'
