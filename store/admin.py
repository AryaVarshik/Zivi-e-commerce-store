from django.contrib import admin
from .models import UserProfile, Category, Brand, Product, Wishlist, Cart, CartItem, Order, OrderItem, Review

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'city', 'dark_mode')
    search_fields = ('user__username', 'phone', 'city')

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'icon_class')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)

class BrandAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'discount_price', 'category', 'brand', 'stock', 'is_flash_sale', 'is_featured')
    list_filter = ('category', 'brand', 'is_flash_sale', 'is_featured')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}

class WishlistAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'added_at')
    list_filter = ('user',)

class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0

class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at', 'updated_at', 'total_items')
    inlines = [CartItemInline]

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'user', 'total_amount', 'status', 'payment_option', 'created_at')
    list_filter = ('status', 'payment_option', 'created_at')
    search_fields = ('order_id', 'user__username', 'email', 'phone')
    inlines = [OrderItemInline]

class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('user__username', 'product__name', 'comment')

admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Brand, BrandAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Wishlist, WishlistAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Review, ReviewAdmin)
