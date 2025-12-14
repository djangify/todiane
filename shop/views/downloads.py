# shop/views/downloads.py
from ..models import Product, Order, OrderItem
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from ..emails import send_download_link_email
from django.core.exceptions import PermissionDenied
from django.http import FileResponse, Http404
from django.views.decorators.http import require_http_methods
import os
import mimetypes
from wsgiref.util import FileWrapper
import logging

# Set up logger
logger = logging.getLogger("shop")


@login_required
@require_http_methods(["GET"])
def secure_download(request, order_item_id):
    # Get the order item
    order_item = get_object_or_404(OrderItem, id=order_item_id)

    # Only the owner can download it
    if order_item.order.user != request.user:
        raise PermissionDenied

    # Get the correct file depending on platform
    file_field = order_item.get_download_file()
    if not file_field:
        raise Http404("No downloadable file found.")

    file_path = file_field.path

    if not os.path.exists(file_path):
        raise Http404("File missing on server.")

    # Handle download limits
    if order_item.downloads_remaining is not None:
        if order_item.downloads_remaining <= 0:
            raise PermissionDenied("Your download limit has been reached.")
        order_item.downloads_remaining -= 1

    # Track total download count
    order_item.download_count += 1
    order_item.save()

    # Build response
    filename = os.path.basename(file_path)
    content_type, _ = mimetypes.guess_type(filename)
    content_type = content_type or "application/octet-stream"

    file_handle = open(file_path, "rb")
    response = FileResponse(
        FileWrapper(file_handle), as_attachment=True, content_type=content_type
    )
    response["Content-Disposition"] = f'attachment; filename="{filename}"'

    return response


@login_required
def download_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    order_item = OrderItem.objects.filter(
        order__user=request.user, product=product
    ).first()

    if not order_item:
        messages.error(request, "You have not purchased this product.")
        return redirect("shop:product_detail", slug=product.slug)

    if order_item.download_count >= settings.MAX_DOWNLOAD_LIMIT:
        messages.error(request, "You have reached the download limit for this product.")
        return redirect("shop:purchases")

    # Increment download count
    order_item.download_count += 1
    order_item.save()

    # Send download link email
    try:
        context = {
            "order_item": order_item,
            "product": order_item.product,
            "site_url": settings.SITE_URL,
            "downloads_remaining": order_item.downloads_remaining,
            "user": order_item.order.user,
            "email": order_item.order.user.email,
            "unsubscribe_url": f"{settings.SITE_URL}/profiles/email-preferences/",
        }
        send_download_link_email(order_item, context)
    except Exception as e:
        logger.error(
            f"Failed to send download email for order item {order_item.id}: {str(e)}"
        )

    # Get download URL
    download_url = product.get_download_url()
    if not download_url:
        messages.error(request, "Download URL not available.")
        return redirect("shop:purchases")

    return redirect(download_url)


@login_required
def purchases(request):
    orders = Order.objects.filter(user=request.user).order_by("-created")
    return render(request, "shop/purchases.html", {"orders": orders})


@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by("-created")
    return render(request, "shop/order_history.html", {"orders": orders})


@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, order_id=order_id, user=request.user)
    return render(request, "shop/purchases.html", {"order": order})
