import stripe
from decimal import Decimal
from borrowings.models import Payment
from django.urls import reverse


def create_stripe_session_for_borrowing(borrowing, request):
    total_price = borrowing.book.daily_fee * Decimal(
        borrowing.calculate_borrowing_days()
    )

    payment = Payment.objects.create(
        borrowing=borrowing,
        payment_status=Payment.PaymentStatusChoices.PENDING,
        payment_type=Payment.PaymentTypeChoices.PAYMENT,
        usd_to_pay=total_price,
    )

    success_url = request.build_absolute_uri(
        reverse("borrowings:payment-success-payment", kwargs={"pk": payment.id})
    ) + "?session_id={CHECKOUT_SESSION_ID}"

    cancel_url = request.build_absolute_uri(
        reverse("borrowings:payment-cancel-payment", kwargs={"pk": payment.id})
    )

    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[{
            "price_data": {
                "currency": "usd",
                "product_data": {
                    "name": f"Borrowing Book: {borrowing.book.title}",
                },
                "unit_amount": int(total_price * 100),
            },
            "quantity": 1,
        }],
        mode="payment",
        success_url=success_url,
        cancel_url=cancel_url,
    )

    payment.session_id = session.id
    payment.session_url = session.url
    payment.save()

    return payment


def create_stripe_fine_payment(borrowing, fine_amount, request):
    payment = Payment.objects.create(
        borrowing=borrowing,
        payment_status=Payment.PaymentStatusChoices.PENDING,
        payment_type=Payment.PaymentTypeChoices.FINE,
        usd_to_pay=fine_amount,
    )

    success_url = request.build_absolute_uri(
        reverse("borrowings:payment-success-payment", kwargs={"pk": payment.id})
    ) + "?session_id={CHECKOUT_SESSION_ID}"

    cancel_url = request.build_absolute_uri(
        reverse("borrowings:payment-cancel-payment", kwargs={"pk": payment.id})
    )
    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[{
            "price_data": {
                "currency": "usd",
                "product_data": {
                    "name": f"Fine for overdue book: {borrowing.book.title}"
                },
                "unit_amount": int(fine_amount * 100),
            },
            "quantity": 1,
        }],
        mode="payment",
        success_url=success_url,
        cancel_url=cancel_url,
    )

    payment.session_id = session.id
    payment.session_url = session.url
    payment.save()

    return payment