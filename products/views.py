from decimal import Decimal, InvalidOperation
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import ProductForm
from .models import Product, Category


def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    related = []
    if product.category:
        related = Product.objects.filter(category=product.category).exclude(id=product.id)[:4]
    return render(request, 'products/product_detail.html', {
        'product': product,
        'related': related,
    })

def home(request):
    return render(request, 'products/home.html')


def to_decimal(value):
    try:
        return Decimal(value)
    except (InvalidOperation, TypeError):
        return None


def product_list(request, slug=None):
    products = Product.objects.all()
    category = None
    subcategories = None

    if slug:
        category = get_object_or_404(Category, slug=slug)
        subcategories = category.children.all()
        products = products.filter(Q(category=category) | Q(category__parent=category))

    q = request.GET.get('q', '').strip()
    if q:
        products = products.filter(Q(name__icontains=q) | Q(description__icontains=q))

    min_price = request.GET.get('min_price', '')
    max_price = request.GET.get('max_price', '')
    if to_decimal(min_price) is not None:
        products = products.filter(price__gte=to_decimal(min_price))
    if to_decimal(max_price) is not None:
        products = products.filter(price__lte=to_decimal(max_price))

    sort = request.GET.get('sort', 'newest')
    orderings = {'newest': '-created_at', 'price_low': 'price', 'price_high': '-price'}
    products = products.order_by(orderings.get(sort, '-created_at'))

    return render(request, 'products/product_list.html', {
        'products': products,
        'category': category,
        'subcategories': subcategories,
        'q': q,
        'min_price': min_price,
        'max_price': max_price,
        'sort': sort,
    })


@login_required
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductForm()
    return render(request, 'products/add_product.html', {'form': form})