import stripe
from decimal import Decimal
from decouple import config
from borrowings.models import Payment


stripe.api_key = config("STRIPE_SECRET_KEY")


def create_stripe_session_for_borrowing(borrowing):
    total_price = (
        borrowing.book.daily_fee * Decimal(
            borrowing.calculate_borrowing_days()
        )
    )

    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[{
            "price_data": {
                "currency": "usd",
                "product_data": {
                    "name": f"Borrowing Book {borrowing.book.title}"
                },
                "unit_amount": int(total_price * 100),
            },
            "quantity": 1,
        }],
        mode="payment",
        success_url='https://example.com/success',
        cancel_url='https://example.com/cancel',
    )

    return Payment.objects.create(
        borrowing=borrowing,
        payment_status=Payment.PaymentStatusChoices.PENDING,
        payment_type=Payment.PaymentTypeChoices.PAYMENT,
        usd_to_pay=total_price,
        session_url=session.url,
        session_id=session.id,
    )