from celery import shared_task
from django.utils.timezone import now
from borrowings.models import Borrowing
from utils.telegram import send_telegram_message


@shared_task
def check_overdue_borrowings():
    today = now().date()
    overdue = Borrowing.objects.filter(
        expected_return_date__lte=today,
        actual_return_date__isnull=True,
    )
    if not overdue.exists():
        send_telegram_message("✅ No borrowings overdue today!")
        return

    for borrowing in overdue:
        expected_date = borrowing.expected_return_date

        if expected_date == today:
            overdue_info = "⚠️ You have to return it today!"
        else:
            days_overdue = (today - expected_date).days
            overdue_info = f"⏳ Overdue by {days_overdue} day(s)!"

        message = (
            f"🚨 Overdue Borrowing!\n"
            f"{overdue_info}\n\n"
            f"👤 User: {borrowing.user.email}\n"
            f"📖 Book: {borrowing.book.title}\n"
            f"📅 Borrowed: {borrowing.borrow_date}\n"
            f"📅 Expected Return: {borrowing.expected_return_date}\n"
        )
        send_telegram_message(message)