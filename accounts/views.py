# accounts/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings

from .models import User, EmailVerificationToken, MemberResource
from shop.models import OrderItem


# -------------------------
# Registration
# -------------------------
def register_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        if User.objects.filter(email=email).exists():
            messages.error(request, "An account with this email already exists.")
            return redirect("accounts:register")

        user = User.objects.create_user(
            email=email,
            password=password,
            is_active=True,
            is_verified=False,
        )

        token = EmailVerificationToken.objects.create(user=user)
        send_verification_email(request, user, token)

        return redirect("accounts:verification_sent")

    return render(request, "accounts/register.html")


def send_verification_email(request, user, token):
    verify_url = request.build_absolute_uri(
        reverse("accounts:verify_email", args=[str(token.token)])
    )

    context = {
        "user": user,
        "verify_url": verify_url,
    }

    subject = "Verify your email"
    html_message = render_to_string("accounts/email/verify_email.html", context)
    plain_message = strip_tags(html_message)

    send_mail(
        subject,
        plain_message,
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        html_message=html_message,
    )


def verification_sent(request):
    return render(request, "accounts/verification_sent.html")


def verify_email(request, token):
    try:
        token_obj = EmailVerificationToken.objects.get(token=token)
    except EmailVerificationToken.DoesNotExist:
        return render(request, "accounts/verification_failed.html")

    if not token_obj.is_valid():
        return render(request, "accounts/verification_failed.html")

    user = token_obj.user
    user.is_verified = True
    user.save()
    token_obj.delete()

    return render(request, "accounts/verification_success.html")


# -------------------------
# Login / Logout
# -------------------------
def login_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = authenticate(request, email=email, password=password)

        if user:
            if not user.is_verified:
                messages.error(request, "Please verify your email first.")
                return redirect("accounts:verification_sent")

            login(request, user)
            return redirect("accounts:dashboard")

        messages.error(request, "Invalid email or password.")

    return render(request, "accounts/login.html")


@login_required
def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect("accounts:login")


# -------------------------
# Dashboard (Shop-style)
# -------------------------
@login_required
def dashboard_view(request):
    user = request.user

    purchased_count = (
        OrderItem.objects.filter(order__user=user).values("product").distinct().count()
    )

    member_resources = MemberResource.objects.filter(is_active=True)

    context = {
        "purchased_count": purchased_count,
        "member_resources": member_resources,
    }

    return render(request, "accounts/dashboard.html", context)
