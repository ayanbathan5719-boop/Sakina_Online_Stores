from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import render, redirect, get_object_or_404
from products.models import Product
from .forms import CheckoutForm
from .models import Order, OrderItem


def build_cart_items(session):
    cart = session.get('cart', {})
    items = []
    for product_id, quantity in cart.items():
        product = Product.objects.filter(id=product_id).first()
        if product:
            items.append({'product': product, 'quantity': quantity,
                          'subtotal': product.price * quantity})
    return items


@login_required
def checkout(request):
    items = build_cart_items(request.session)
    if not items:
        messages.error(request, 'Your cart is empty.')
        return redirect('cart_detail')
    total = sum(i['subtotal'] for i in items)

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            for i in items:
                if i['quantity'] > i['product'].stock:
                    messages.error(request, f"Only {i['product'].stock} of {i['product'].name} left in stock.")
                    return redirect('cart_detail')
            with transaction.atomic():
                order = form.save(commit=False)
                order.user = request.user
                order.save()
                for i in items:
                    OrderItem.objects.create(
                        order=order,
                        product=i['product'],
                        product_name=i['product'].name,
                        price=i['product'].price,
                        quantity=i['quantity'],
                    )
                    i['product'].stock -= i['quantity']
                    i['product'].save()
            request.session['cart'] = {}
            messages.success(request, 'Order placed. Thank you!')
            return redirect('order_detail', order_id=order.id)
    else:
        form = CheckoutForm()
    return render(request, 'orders/checkout.html', {'form': form, 'items': items, 'total': total})


@login_required
def order_list(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'orders/order_list.html', {'orders': orders})


@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'orders/order_detail.html', {'order': order})