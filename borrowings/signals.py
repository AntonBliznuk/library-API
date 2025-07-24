from django.db.models.signals import post_save
from django.dispatch import receiver

from borrowings.models import Borrowing
from utils.telegram import send_telegram_message


@receiver(post_save, sender=Borrowing)
def notify_on_borrowing_creation(sender, instance, created, **kwargs):
    if created:
        user = instance.user
        book = instance.book
        expected_return_date = instance.expected_return_date.strftime("%d-%m-%Y")

        message = (
            f"📚 <b>New Borrowing Created</b>\n\n"
            f"👤 User: {user.email}\n"
            f"📖 Book: {book.title}\n"
            f"📅 Expected Return: {expected_return_date}"
        )
        send_telegram_message(message)
