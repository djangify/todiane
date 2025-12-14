# shop/views/wishlist.py
from ..models import Product
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_POST
from ..models import WishList


@login_required
@require_POST
def toggle_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    existing = WishList.objects.filter(user=request.user, product=product)
    if existing.exists():
        existing.delete()
        messages.success(request, f"{product.title} removed from your Wish List.")
    else:
        WishList.objects.create(user=request.user, product=product)
        messages.success(request, f"{product.title} added to your Wish List.")

    # Redirect back to the page the user was on
    referer = request.META.get("HTTP_REFERER")
    if referer:
        return redirect(referer)

    # Fallback: go to product page
    return redirect("shop:product_detail", slug=product.slug)


@login_required
def wishlist_list(request):
    items = WishList.objects.filter(user=request.user).select_related("product")
    return render(
        request, "accounts/includes/dashboard_wishlist.html", {"items": items}
    )
