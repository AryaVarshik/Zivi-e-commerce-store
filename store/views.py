import json
from decimal import Decimal
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.db.models import Q
from django.views.decorators.csrf import csrf_protect

from .models import UserProfile, Category, Brand, Product, Wishlist, Cart, CartItem, Order, OrderItem, Review

def get_cart_count(request):
    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user)
        return cart.total_items
    return 0

def get_wishlist_count(request):
    if request.user.is_authenticated:
        return Wishlist.objects.filter(user=request.user).count()
    return 0

def home_view(request):
    categories = Category.objects.all()
    brands = Brand.objects.all()
    reviews = Review.objects.all().order_by('-created_at')[:6]
    
    # Base products queryset
    products = Product.objects.all()

    # Search filter
    q = request.GET.get('q')
    if q:
        products = products.filter(Q(name__icontains=q) | Q(description__icontains=q))

    # Category filter
    category_slug = request.GET.get('category')
    if category_slug:
        products = products.filter(category__slug=category_slug)

    # Brand filter
    brand_slug = request.GET.get('brand')
    if brand_slug:
        products = products.filter(brand__slug=brand_slug)

    # Price filter
    price_min = request.GET.get('price_min')
    if price_min:
        try:
            products = products.filter(price__gte=Decimal(price_min))
        except:
            pass
            
    price_max = request.GET.get('price_max')
    if price_max:
        try:
            products = products.filter(price__lte=Decimal(price_max))
        except:
            pass

    # Rating filter
    rating_val = request.GET.get('rating')
    if rating_val:
        try:
            products = products.filter(rating__gte=float(rating_val))
        except:
            pass

    # Discount filter
    discount = request.GET.get('discount')
    if discount == 'true':
        products = products.filter(discount_price__isnull=False)

    # Availability filter
    availability = request.GET.get('availability')
    if availability == 'in_stock':
        products = products.filter(stock__gt=0)
    elif availability == 'out_of_stock':
        products = products.filter(stock=0)

    # Resolve some products for the carousel/banners (we need 10 banners)
    # Banner products selection
    banner_products = Product.objects.all()
    featured_products = banner_products.filter(is_featured=True)[:10]
    flash_sale_products = banner_products.filter(is_flash_sale=True)[:10]
    
    # Just in case there are not enough products, use normal products as fallback
    all_banner_prods = list(banner_products)
    while len(all_banner_prods) < 35:
         all_banner_prods.extend(list(banner_products))
    
    wishlisted_ids = []
    if request.user.is_authenticated:
        wishlisted_ids = list(Wishlist.objects.filter(user=request.user).values_list('product_id', flat=True))
    
    context = {
        'categories': categories,
        'brands': brands,
        'products': products[:30],
        'reviews': reviews,
        'cart_count': get_cart_count(request),
        'wishlist_count': get_wishlist_count(request),
        'wishlisted_ids': wishlisted_ids,
        'banner_products': all_banner_prods[:35],
        'featured_products': featured_products,
        'flash_sale_products': flash_sale_products,
        # Preserve filters in context for pre-populating fields
        'selected_category': category_slug,
        'selected_brand': brand_slug,
        'price_min': price_min,
        'price_max': price_max,
        'selected_rating': rating_val,
        'selected_discount': discount,
        'selected_availability': availability,
        'search_query': q,
    }
    return render(request, 'store/home.html', context)


def flash_sale_view(request):
    categories = Category.objects.all()
    brands = Brand.objects.all()
    
    # Base products queryset
    products = Product.objects.filter(is_flash_sale=True)

    # Search filter
    q = request.GET.get('q')
    if q:
        products = products.filter(Q(name__icontains=q) | Q(description__icontains=q))

    # Category filter
    category_slug = request.GET.get('category')
    if category_slug:
        products = products.filter(category__slug=category_slug)

    # Brand filter
    brand_slug = request.GET.get('brand')
    if brand_slug:
        products = products.filter(brand__slug=brand_slug)

    # Price filter
    price_min = request.GET.get('price_min')
    if price_min:
        try:
            products = products.filter(price__gte=Decimal(price_min))
        except:
            pass
            
    price_max = request.GET.get('price_max')
    if price_max:
        try:
            products = products.filter(price__lte=Decimal(price_max))
        except:
            pass

    # Rating filter
    rating_val = request.GET.get('rating')
    if rating_val:
        try:
            products = products.filter(rating__gte=float(rating_val))
        except:
            pass

    # Availability filter
    availability = request.GET.get('availability')
    if availability == 'in_stock':
        products = products.filter(stock__gt=0)

    wishlisted_ids = []
    if request.user.is_authenticated:
        wishlisted_ids = list(Wishlist.objects.filter(user=request.user).values_list('product_id', flat=True))

    context = {
        'categories': categories,
        'brands': brands,
        'products': products,
        'cart_count': get_cart_count(request),
        'wishlist_count': get_wishlist_count(request),
        'wishlisted_ids': wishlisted_ids,
        'selected_category': category_slug,
        'selected_brand': brand_slug,
        'price_min': price_min,
        'price_max': price_max,
        'selected_rating': rating_val,
        'selected_availability': availability,
        'search_query': q,
    }
    return render(request, 'store/flash_sale.html', context)


def product_detail_view(request, slug):
    product = get_object_or_404(Product, slug=slug)
    related_products = Product.objects.filter(category=product.category).exclude(id=product.id)[:4]
    
    # If not enough related products, fill with featured
    if related_products.count() < 4:
        extra_count = 4 - related_products.count()
        extras = Product.objects.exclude(id=product.id).exclude(id__in=[p.id for p in related_products])[:extra_count]
        related_products = list(related_products) + list(extras)

    reviews = product.reviews.all().order_by('-created_at')

    if request.method == 'POST':
        if not request.user.is_authenticated:
            messages.warning(request, "Please log in to write a review.")
            return redirect('login')
        
        rating = request.POST.get('rating', 5)
        comment = request.POST.get('comment', '')
        
        Review.objects.create(
            user=request.user,
            product=product,
            rating=int(rating),
            comment=comment
        )
        
        # Update product rating
        all_reviews = product.reviews.all()
        avg_rating = sum(r.rating for r in all_reviews) / len(all_reviews)
        product.rating = round(avg_rating, 1)
        product.save()
        
        messages.success(request, "Thank you for your review!")
        return redirect('product_detail', slug=slug)

    wishlisted_ids = []
    if request.user.is_authenticated:
        wishlisted_ids = list(Wishlist.objects.filter(user=request.user).values_list('product_id', flat=True))

    context = {
        'product': product,
        'related_products': related_products,
        'reviews': reviews,
        'cart_count': get_cart_count(request),
        'wishlist_count': get_wishlist_count(request),
        'wishlisted_ids': wishlisted_ids,
    }
    return render(request, 'store/product_detail.html', context)


@login_required
def wishlist_view(request):
    wishlist_items = Wishlist.objects.filter(user=request.user)
    
    # Recommendations
    related_products = Product.objects.all().order_by('?')[:4]
    exclusive_sale = Product.objects.filter(is_flash_sale=True)[:4]

    wishlisted_ids = []
    if request.user.is_authenticated:
        wishlisted_ids = list(Wishlist.objects.filter(user=request.user).values_list('product_id', flat=True))

    context = {
        'wishlist_items': wishlist_items,
        'related_products': related_products,
        'exclusive_sale': exclusive_sale,
        'cart_count': get_cart_count(request),
        'wishlist_count': wishlist_items.count(),
        'wishlisted_ids': wishlisted_ids,
    }
    return render(request, 'store/wishlist.html', context)


@login_required
def cart_view(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    
    # Recommendations
    related_products = Product.objects.all().order_by('?')[:4]
    exclusive_sale = Product.objects.filter(is_flash_sale=True)[:4]

    wishlisted_ids = []
    if request.user.is_authenticated:
        wishlisted_ids = list(Wishlist.objects.filter(user=request.user).values_list('product_id', flat=True))

    context = {
        'cart': cart,
        'related_products': related_products,
        'exclusive_sale': exclusive_sale,
        'cart_count': cart.total_items,
        'wishlist_count': get_wishlist_count(request),
        'wishlisted_ids': wishlisted_ids,
    }
    return render(request, 'store/cart.html', context)


@login_required
def checkout_view(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    if cart.total_items == 0:
        messages.warning(request, "Your cart is empty. Add products before checkout.")
        return redirect('cart')

    profile = request.user.profile

    if request.method == 'POST':
        shipping_address = request.POST.get('shipping_address')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        delivery_option = request.POST.get('delivery_option', 'Standard')
        is_gift = request.POST.get('is_gift') == 'on'
        gift_recipient_name = request.POST.get('gift_recipient_name')
        gift_recipient_phone = request.POST.get('gift_recipient_phone')
        gift_message = request.POST.get('gift_message')
        payment_option = request.POST.get('payment_option')

        # Check required fields
        if not shipping_address or not phone or not email or not payment_option:
            messages.error(request, "Please fill in all required fields.")
            return redirect('checkout')

        # Compute delivery charges based on options
        import decimal
        del_charge = decimal.Decimal('0.00')
        if delivery_option == 'Express':
            del_charge = decimal.Decimal('15.00')
        else:
            if cart.subtotal < 50:
                del_charge = decimal.Decimal('5.00')

        total_amount = cart.subtotal + del_charge

        # Create Order
        order = Order.objects.create(
            user=request.user,
            shipping_address=shipping_address,
            phone=phone,
            email=email,
            delivery_option=delivery_option,
            is_gift=is_gift,
            gift_recipient_name=gift_recipient_name if is_gift else None,
            gift_recipient_phone=gift_recipient_phone if is_gift else None,
            gift_message=gift_message if is_gift else None,
            payment_option=payment_option,
            total_amount=total_amount,
            status='Pending'
        )

        # Create OrderItems
        for item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.final_price
            )
            # Reduce product stock
            if item.product.stock >= item.quantity:
                item.product.stock -= item.quantity
                item.product.save()

        # Clear Cart
        cart.items.all().delete()

        messages.success(request, "Your order has been placed successfully!")
        return redirect('order_success', order_id=order.order_id)

    # Prefill from user profile if available
    prefill = {
        'address': profile.address or '',
        'phone': profile.phone or '',
        'email': request.user.email or '',
    }

    context = {
        'cart': cart,
        'prefill': prefill,
        'cart_count': cart.total_items,
        'wishlist_count': get_wishlist_count(request),
    }
    return render(request, 'store/checkout.html', context)


@login_required
def order_success_view(request, order_id):
    order = get_object_or_404(Order, order_id=order_id, user=request.user)
    
    # Calculate delivery date (say 3 days from now)
    import datetime
    est_delivery = order.created_at + datetime.timedelta(days=3)

    context = {
        'order': order,
        'est_delivery': est_delivery,
        'cart_count': get_cart_count(request),
        'wishlist_count': get_wishlist_count(request),
    }
    return render(request, 'store/order_success.html', context)


def signup_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Set optional email from POST parameter if present
            email = request.POST.get('email')
            if email:
                user.email = email
                user.save()
            
            # Update user profile
            profile = user.profile
            profile.phone = request.POST.get('phone', '')
            profile.address = request.POST.get('address', '')
            profile.city = request.POST.get('city', '')
            profile.zip_code = request.POST.get('zip_code', '')
            profile.save()

            login(request, user)
            messages.success(request, f"Welcome to Zivi, {user.username}! Your account has been created.")
            return redirect('home')
        else:
            for error in form.errors.values():
                messages.error(request, error)

    return render(request, 'store/signup.html', {
        'cart_count': 0,
        'wishlist_count': 0
    })


def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome back, {username}!")
                # Redirect to 'next' page if exists
                next_url = request.GET.get('next')
                if next_url:
                    return redirect(next_url)
                return redirect('home')
        else:
             messages.error(request, "Invalid username or password.")

    return render(request, 'store/login.html', {
        'cart_count': 0,
        'wishlist_count': 0
    })


def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect('home')


@login_required
def profile_view(request):
    profile = request.user.profile
    orders = Order.objects.filter(user=request.user).order_by('-created_at')

    if request.method == 'POST':
        # Update user profile details
        user = request.user
        user.first_name = request.POST.get('first_name', '')
        user.last_name = request.POST.get('last_name', '')
        user.email = request.POST.get('email', '')
        user.save()

        profile.phone = request.POST.get('phone', '')
        profile.address = request.POST.get('address', '')
        profile.city = request.POST.get('city', '')
        profile.zip_code = request.POST.get('zip_code', '')
        profile.save()

        messages.success(request, "Your profile details have been updated.")
        return redirect('profile')

    context = {
        'profile': profile,
        'orders': orders,
        'cart_count': get_cart_count(request),
        'wishlist_count': get_wishlist_count(request),
    }
    return render(request, 'store/profile.html', context)


def settings_view(request):
    if request.user.is_authenticated:
        profile = request.user.profile
        if request.method == 'POST':
            dark_mode = request.POST.get('dark_mode') == 'true'
            profile.dark_mode = dark_mode
            profile.save()
            return JsonResponse({'status': 'success'})
            
    context = {
        'cart_count': get_cart_count(request),
        'wishlist_count': get_wishlist_count(request),
    }
    return render(request, 'store/settings.html', context)


def about_view(request):
    context = {
        'cart_count': get_cart_count(request),
        'wishlist_count': get_wishlist_count(request),
    }
    return render(request, 'store/about.html', context)


# ==========================================
# AJAX APIs FOR INLINE INTERACTIONS
# ==========================================

def api_check_auth(view_func):
    # Custom decorator wrapper to return AJAX redirect response if anonymous
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            # Add message queueing
            messages.warning(request, "Please log in to access this feature.")
            return JsonResponse({
                'status': 'unauthorized', 
                'redirect_url': '/login/'
            }, status=401)
        return view_func(request, *args, **kwargs)
    return wrapper

@csrf_protect
@api_check_auth
@require_POST
def api_add_to_cart(request):
    try:
        data = json.loads(request.body)
        product_id = data.get('product_id')
        quantity = int(data.get('quantity', 1))
    except:
        return JsonResponse({'status': 'error', 'message': 'Invalid data format'}, status=400)

    product = Product.objects.filter(id=product_id).first()
    if not product:
        return JsonResponse({'status': 'error', 'message': 'Product not found'}, status=404)

    if product.stock < quantity:
        return JsonResponse({'status': 'error', 'message': f'Only {product.stock} items left in stock.'}, status=400)

    cart, _ = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    
    if not created:
        if product.stock < (cart_item.quantity + quantity):
            return JsonResponse({'status': 'error', 'message': f'Cannot add. Only {product.stock} items in stock and you already have {cart_item.quantity} in your cart.'}, status=400)
        cart_item.quantity += quantity
    else:
        cart_item.quantity = quantity
        
    cart_item.save()
    messages.success(request, f"Added {product.name} to your cart!")
    return JsonResponse({
        'status': 'success',
        'message': f'Added {product.name} to cart.',
        'cart_count': cart.total_items
    })

@csrf_protect
@api_check_auth
@require_POST
def api_update_cart(request):
    try:
        data = json.loads(request.body)
        product_id = data.get('product_id')
        action = data.get('action') # 'increase', 'decrease', or 'remove'
    except:
        return JsonResponse({'status': 'error', 'message': 'Invalid data format'}, status=400)

    cart = Cart.objects.filter(user=request.user).first()
    if not cart:
        return JsonResponse({'status': 'error', 'message': 'Cart not found'}, status=404)

    product = Product.objects.filter(id=product_id).first()
    if not product:
        return JsonResponse({'status': 'error', 'message': 'Product not found'}, status=404)

    cart_item = CartItem.objects.filter(cart=cart, product=product).first()
    if not cart_item:
        return JsonResponse({'status': 'error', 'message': 'Item not in cart'}, status=404)

    if action == 'increase':
        if product.stock <= cart_item.quantity:
             return JsonResponse({'status': 'error', 'message': 'Insufficient stock available.'}, status=400)
        cart_item.quantity += 1
        cart_item.save()
    elif action == 'decrease':
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    elif action == 'remove':
        cart_item.delete()
        messages.success(request, f"Removed {product.name} from your cart.")
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid action'}, status=400)

    # Re-evaluate numbers
    subtotal = cart.subtotal
    delivery = cart.delivery_charge
    total_discount = cart.total_discount
    grand_total = cart.grand_total

    return JsonResponse({
        'status': 'success',
        'cart_count': cart.total_items,
        'item_qty': cart_item.quantity if action != 'remove' and cart_item.id else 0,
        'item_total': float(cart_item.total_price) if action != 'remove' and cart_item.id else 0,
        'subtotal': float(subtotal),
        'delivery_charge': float(delivery),
        'total_discount': float(total_discount),
        'grand_total': float(grand_total)
    })

@csrf_protect
@api_check_auth
@require_POST
def api_add_to_wishlist(request):
    try:
        data = json.loads(request.body)
        product_id = data.get('product_id')
    except:
        return JsonResponse({'status': 'error', 'message': 'Invalid data format'}, status=400)

    product = Product.objects.filter(id=product_id).first()
    if not product:
        return JsonResponse({'status': 'error', 'message': 'Product not found'}, status=404)

    wishlist_item, created = Wishlist.objects.get_or_create(user=request.user, product=product)
    
    if created:
        messages.success(request, f"Added {product.name} to your wishlist!")
        return JsonResponse({
            'status': 'success',
            'message': f'Added {product.name} to wishlist.',
            'wishlist_count': Wishlist.objects.filter(user=request.user).count()
        })
    else:
        return JsonResponse({
            'status': 'info',
            'message': f'{product.name} is already in your wishlist.',
            'wishlist_count': Wishlist.objects.filter(user=request.user).count()
        })

@csrf_protect
@api_check_auth
@require_POST
def api_remove_from_wishlist(request):
    try:
        data = json.loads(request.body)
        product_id = data.get('product_id')
    except:
         return JsonResponse({'status': 'error', 'message': 'Invalid data format'}, status=400)

    wishlist_item = Wishlist.objects.filter(user=request.user, product_id=product_id).first()
    if wishlist_item:
        product_name = wishlist_item.product.name
        wishlist_item.delete()
        messages.success(request, f"Removed {product_name} from your wishlist.")
        return JsonResponse({
            'status': 'success',
            'message': f'Removed {product_name} from wishlist.',
            'wishlist_count': Wishlist.objects.filter(user=request.user).count()
        })
    return JsonResponse({'status': 'error', 'message': 'Item not in wishlist'}, status=404)
