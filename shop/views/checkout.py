# shop/views/checkout.py
from ..models import Order, OrderItem
from django.contrib import messages
from django.shortcuts import render, redirect
from django.conf import settings
import stripe
import logging
from ..emails import send_order_confirmation_email, send_download_link_email
from .cart import Cart
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse


stripe.api_key = settings.STRIPE_SECRET_KEY

# Set up logger
logger = logging.getLogger("shop")


def checkout(request):
    if not request.user.is_authenticated:
        return redirect("accounts:login")

    cart = Cart(request)
    if len(cart) == 0:
        messages.error(request, "Your cart is empty.")
        return redirect("shop:cart_detail")

    try:
        total_price = cart.get_total_price()

        if total_price <= 0:
            messages.error(request, "Invalid cart total")
            return redirect("shop:cart_detail")

        # Create a new PaymentIntent each time user loads checkout
        intent = stripe.PaymentIntent.create(
            amount=int(total_price * 100),
            currency=getattr(settings, "STRIPE_CURRENCY", "gbp"),
            payment_method_types=["card"],
            metadata={
                "user_id": str(request.user.id),
            },
            receipt_email=request.user.email,
        )

        context = {
            "client_secret": intent.client_secret,
            "STRIPE_PUBLIC_KEY": settings.STRIPE_PUBLIC_KEY,
            "cart": cart,
            "payment_intent_id": intent.id,
        }
        return render(request, "shop/checkout.html", context)

    except stripe.error.StripeError as e:
        logger.error(f"Stripe error during checkout: {str(e)}")
        messages.error(request, f"Payment processing error: {str(e)}")
        return redirect("shop:cart_detail")

    except Exception as e:
        logger.error(f"Unexpected checkout error: {str(e)}")
        messages.error(request, "An error occurred during checkout. Please try again.")
        return redirect("shop:cart_detail")


def payment_success(request):
    payment_intent_id = request.GET.get("payment_intent")
    if not payment_intent_id:
        messages.error(request, "No payment information found.")
        return redirect("shop:cart_detail")

    try:
        # Verify payment with Stripe
        payment_intent = stripe.PaymentIntent.retrieve(payment_intent_id)
        if payment_intent.status != "succeeded":
            logger.warning(f"Payment intent {payment_intent_id} not succeeded")
            messages.error(request, "Payment was not successful.")
            return redirect("shop:cart_detail")

        if not request.user.is_authenticated:
            messages.error(request, "You must be logged in to complete checkout.")
            return redirect("accounts:login")

        email = request.user.email

        # Prevent duplicate order creation on refresh
        existing_order = Order.objects.filter(
            payment_intent_id=payment_intent_id
        ).first()
        if existing_order:
            return redirect("shop:purchases")

        cart = Cart(request)

        # Create order
        order = Order.objects.create(
            user=request.user,
            email=email,
            payment_intent_id=payment_intent_id,
            paid=True,
            status="completed",
        )

        for item in cart:
            # NEW: Determine platform from session
            platform_selection = request.session.get("platform_selection", {})

            OrderItem.objects.create(
                order=order,
                product=item["product"],
                platform=platform_selection.get(
                    str(item["product"].id), "windows"
                ),  # NEW
                price_paid_pence=int(item["price"] * 100),
                quantity=item["quantity"],
                downloads_remaining=item["product"].download_limit,
            )

            product = item["product"]
            product.purchase_count += item["quantity"]
            product.save()

        try:
            send_order_confirmation_email(order)
            from ..emails import send_admin_new_order_email

            send_admin_new_order_email(order)

        except Exception as e:
            logger.error(f"Failed to send order confirmation email: {str(e)}")

        request.session.pop("platform_selection", None)

        cart.clear()

        return render(request, "shop/success.html", {"order": order})

    except stripe.error.StripeError as e:
        logger.error(f"Stripe error: {str(e)}")
        messages.error(request, f"Error: {str(e)}")
        return redirect("shop:cart_detail")

    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        messages.error(request, "There was an error processing your order.")
        return redirect("shop:cart_detail")


def payment_cancel(request):
    messages.error(request, "Payment was cancelled.")
    return redirect("shop:cart_detail")


def handle_successful_payment(payment_intent):
    order = Order.objects.filter(payment_intent_id=payment_intent.id).first()
    if order and not order.paid:
        order.paid = True
        order.status = "completed"
        order.save()

        try:
            for order_item in order.items.all():
                send_download_link_email(order_item)
        except Exception as e:
            print(f"Error sending download emails in webhook: {str(e)}")

        try:
            send_order_confirmation_email(order)
        except Exception as e:
            print(f"Error sending order confirmation email: {str(e)}")


def handle_failed_payment(payment_intent):
    order = Order.objects.filter(payment_intent_id=payment_intent.id).first()
    if order:
        order.status = "failed"
        order.save()


@csrf_exempt
@require_POST
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get("HTTP_STRIPE_SIGNATURE")

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        logger.error(f"Something failed: {str(e)}")
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        logger.error(f"Something failed: {str(e)}")
        return HttpResponse(status=400)

    if event.type == "payment_intent.succeeded":
        payment_intent = event.data.object
        handle_successful_payment(payment_intent)
    elif event.type == "payment_intent.payment_failed":
        payment_intent = event.data.object
        handle_failed_payment(payment_intent)

    return HttpResponse(status=200)
