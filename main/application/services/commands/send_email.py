from app.celery import send_email
from main.domain.aggregates import Order
from shared.application.services.commands.command import Command


class SendEmailWithOrder(Command):

    def __call__(self, order: Order):
        send_email.delay(order)
