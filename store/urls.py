from django.urls import path
from . import views

urlpatterns = [
    # Pages
    path('', views.home_view, name='home'),
    path('flash-sale/', views.flash_sale_view, name='flash_sale'),
    path('product/<slug:slug>/', views.product_detail_view, name='product_detail'),
    path('wishlist/', views.wishlist_view, name='wishlist'),
    path('cart/', views.cart_view, name='cart'),
    path('checkout/', views.checkout_view, name='checkout'),
    path('order-success/<str:order_id>/', views.order_success_view, name='order_success'),
    
    # Auth
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    
    # Static pages
    path('settings/', views.settings_view, name='settings'),
    path('about/', views.about_view, name='about'),
    
    # AJAX API Endpoints
    path('api/cart/add/', views.api_add_to_cart, name='api_add_to_cart'),
    path('api/cart/update/', views.api_update_cart, name='api_update_cart'),
    path('api/wishlist/add/', views.api_add_to_wishlist, name='api_add_to_wishlist'),
    path('api/wishlist/remove/', views.api_remove_from_wishlist, name='api_remove_from_wishlist'),
]
