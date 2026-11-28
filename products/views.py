from decimal import Decimal, InvalidOperation
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import ProductForm
from .models import Product, Category
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.http import JsonResponse

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
    wanted = ["Modest Fashion", "Hijabs and Headwear", "Perfumes and Fragrance",
              "Islamic Essentials", "Bags and Accessories", "Gifts and Special Collections"]
    tops = {c.name: c for c in Category.objects.filter(parent__isnull=True, name__in=wanted)}
    return render(request, 'products/home.html', {
        'featured_categories': [tops[n] for n in wanted if n in tops],
        'featured': Product.objects.filter(is_featured=True)[:4],
        'new_arrivals': Product.objects.order_by('-created_at')[:4],
    })


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

@staff_member_required(login_url='login')
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product added.')
            return redirect('product_list')
    else:
        form = ProductForm()
    return render(request, 'products/product_form.html', {'form': form, 'title': 'Add product'})
@staff_member_required(login_url='login')
def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product updated.')
            return redirect('product_detail', product_id=product.id)
    else:
        form = ProductForm(instance=product)
    return render(request, 'products/product_form.html', {'form': form, 'title': 'Edit product'})


@staff_member_required(login_url='login')
def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        product.delete()
        messages.success(request, 'Product deleted.')
        return redirect('product_list')
    return render(request, 'products/product_confirm_delete.html', {'product': product})
def product_api(request):
    products = Product.objects.all()

    if request.GET.get('in_stock') == '1':
        products = products.filter(stock__gt=0)

    data = [
        {
            'id': p.id,
            'name': p.name,
            'price': float(p.price),
            'stock': p.stock,
        }
        for p in products
    ]
    return JsonResponse({'count': len(data), 'products': data})