from decimal import Decimal
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.http import require_POST
from .cart import Cart
from .forms import CheckoutForm, RegisterForm
from .models import Order, OrderItem, Product


def home(request):
    products = Product.objects.filter(is_active=True).order_by('id')[:6]
    return render(request, 'store/home.html', {'products': products})


def product_list(request):
    products = Product.objects.filter(is_active=True)
    q = request.GET.get('q', '').strip()[:100]
    category = request.GET.get('category', '').strip()
    dietary = request.GET.get('dietary', '').strip().upper()
    if q:
        products = products.filter(Q(name__icontains=q) | Q(description__icontains=q) | Q(cuisine__icontains=q))
    if category:
        products = products.filter(category=category)
    if dietary in dict(Product.DIETS):
        products = products.filter(dietary=dietary)
    else:
        dietary = ''
    sort = request.GET.get('sort', 'featured')
    ordering = {'featured': 'id', 'price_asc': 'price', 'price_desc': '-price', 'quickest': 'prep_minutes'}
    products = products.order_by(ordering.get(sort, 'id'))
    categories = Product.objects.filter(is_active=True).values_list('category', flat=True).distinct().order_by('category')
    return render(request, 'store/product_list.html', {'products': products, 'categories': categories, 'q': q, 'selected_category': category, 'selected_dietary': dietary, 'sort': sort})


def product_detail(request, slug):
    dish = get_object_or_404(Product, slug=slug, is_active=True)
    return render(request, 'store/product_detail.html', {'product': dish})


def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    form = RegisterForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, 'Your account is ready. Welcome to SavorLane!')
        return redirect('home')
    return render(request, 'registration/register.html', {'form': form})


def cart_detail(request):
    return render(request, 'store/cart.html', {'cart': Cart(request)})


@require_POST
def cart_add(request, product_id):
    product = get_object_or_404(Product, id=product_id, is_active=True)
    try:
        qty = max(1, int(request.POST.get('quantity', 1)))
    except (TypeError, ValueError):
        qty = 1
    if product.stock:
        Cart(request).add(product, qty)
        messages.success(request, f'{product.name} added to your bag.')
    else:
        messages.error(request, 'This dish is sold out.')
    destination = request.POST.get('next', '')
    return redirect(destination if url_has_allowed_host_and_scheme(destination, {request.get_host()}) else 'cart')


@require_POST
def cart_update(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    try:
        qty = int(request.POST.get('quantity', 1))
    except (TypeError, ValueError):
        qty = 1
    Cart(request).add(product, min(max(0, qty), product.stock), override=True)
    return redirect('cart')


@require_POST
def cart_remove(request, product_id):
    Cart(request).remove(get_object_or_404(Product, id=product_id))
    return redirect('cart')


@login_required
def checkout(request):
    cart = Cart(request)
    if not len(cart):
        messages.info(request, 'Your bag is empty.')
        return redirect('products')
    initial = {'full_name': request.user.get_full_name() or request.user.username, 'email': request.user.email}
    form = CheckoutForm(request.POST or None, initial=initial)
    if request.method == 'POST' and form.is_valid():
        rows = list(cart)
        with transaction.atomic():
            locked = {p.id: p for p in Product.objects.select_for_update().filter(id__in=[r['product'].id for r in rows], is_active=True)}
            if any((p := locked.get(r['product'].id)) is None or r['quantity'] > p.stock for r in rows):
                messages.error(request, 'Availability changed. Please review your bag.')
                return redirect('cart')
            order = form.save(commit=False)
            order.user = request.user
            order.total_amount = sum((locked[r['product'].id].price * r['quantity'] for r in rows), Decimal('0'))
            order.save()
            for row in rows:
                product = locked[row['product'].id]
                OrderItem.objects.create(order=order, product=product, product_name=product.name, unit_price=product.price, quantity=row['quantity'])
                product.stock -= row['quantity']
                product.save(update_fields=['stock'])
        cart.clear()
        messages.success(request, f'Demo order #{order.id} received.')
        return redirect('order_success', order_id=order.id)
    return render(request, 'store/checkout.html', {'cart': cart, 'form': form})


@login_required
def order_success(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'store/order_success.html', {'order': order})


@login_required
def order_history(request):
    orders = request.user.food_orders.prefetch_related('items').order_by('-created_at')
    return render(request, 'store/order_history.html', {'orders': orders})
