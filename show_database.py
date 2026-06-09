"""
Zivi Database Inspector — run this to demonstrate how data is stored.

Usage:
    python show_database.py
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'zivi_project.settings')
django.setup()

from django.contrib.auth.models import User
from django.db import connection
from store.models import (
    UserProfile, Category, Brand, Product,
    Wishlist, Cart, CartItem, Order, OrderItem, Review,
)


def print_header(title):
    print()
    print('=' * 60)
    print(f'  {title}')
    print('=' * 60)


def show_table_counts():
    print_header('DATABASE OVERVIEW (SQLite: db.sqlite3)')
    tables = [
        ('Users', User.objects.count()),
        ('User Profiles', UserProfile.objects.count()),
        ('Categories', Category.objects.count()),
        ('Brands', Brand.objects.count()),
        ('Products', Product.objects.count()),
        ('Reviews', Review.objects.count()),
        ('Wishlists', Wishlist.objects.count()),
        ('Carts', Cart.objects.count()),
        ('Cart Items', CartItem.objects.count()),
        ('Orders', Order.objects.count()),
        ('Order Items', OrderItem.objects.count()),
    ]
    for name, count in tables:
        print(f'  {name:<20} {count:>6} rows')


def show_schema():
    print_header('TABLE STRUCTURE (columns per table)')
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%' ORDER BY name"
        )
        tables = [row[0] for row in cursor.fetchall()]

    for table in tables:
        with connection.cursor() as cursor:
            cursor.execute(f'PRAGMA table_info("{table}")')
            columns = cursor.fetchall()
        col_names = ', '.join(col[1] for col in columns)
        print(f'\n  {table}')
        print(f'    Columns: {col_names}')


def show_relationships():
    print_header('HOW TABLES CONNECT (relationships)')
    relationships = [
        'User  --1:1-->  UserProfile        (phone, address, dark_mode)',
        'User  --1:N-->  Cart               (one cart per user)',
        'Cart  --1:N-->  CartItem           (items in cart)',
        'CartItem --N:1-->  Product         (which product + quantity)',
        'User  --1:N-->  Wishlist           (saved products)',
        'Wishlist --N:1-->  Product',
        'User  --1:N-->  Order              (purchase history)',
        'Order --1:N-->  OrderItem          (snapshot of items at checkout)',
        'OrderItem --N:1-->  Product        (price frozen at purchase time)',
        'User  --1:N-->  Review',
        'Review --N:1-->  Product',
        'Category --1:N-->  Product',
        'Brand --1:N-->  Product',
    ]
    for rel in relationships:
        print(f'  {rel}')


def show_sample_data():
    print_header('SAMPLE DATA (what you can show live)')

    print('\n  Categories:')
    for cat in Category.objects.all()[:5]:
        product_count = cat.products.count()
        print(f'    [{cat.id}] {cat.name} ({cat.slug}) — {product_count} products')

    print('\n  Products (first 3):')
    for p in Product.objects.select_related('category', 'brand')[:3]:
        price = f'${p.final_price}'
        if p.is_discounted:
            price += f' (was ${p.price}, {p.discount_percentage}% off)'
        brand = p.brand.name if p.brand else 'N/A'
        print(f'    [{p.id}] {p.name}')
        print(f'         Category: {p.category.name} | Brand: {brand} | Price: {price} | Stock: {p.stock}')

    print('\n  Reviews (first 2):')
    for r in Review.objects.select_related('user', 'product')[:2]:
        print(f'    {r.user.username} rated "{r.product.name}" {r.rating}/5')
        print(f'         "{r.comment[:80]}..."' if len(r.comment) > 80 else f'         "{r.comment}"')

    orders = Order.objects.select_related('user').order_by('-created_at')[:2]
    if orders:
        print('\n  Recent Orders:')
        for o in orders:
            items = o.items.select_related('product')
            print(f'    {o.order_id} | {o.user.username} | ${o.total_amount} | {o.status}')
            for item in items:
                print(f'         {item.quantity}x {item.product.name} @ ${item.price}')


def show_data_flow():
    print_header('DATA FLOW (what happens when a user shops)')
    steps = [
        '1. SIGNUP  ->  Row created in auth_user + store_userprofile',
        '2. BROWSE  ->  Products read from store_product (filtered by category/brand/price)',
        '3. ADD TO CART  ->  store_cartitem row (user_id + product_id + quantity)',
        '4. CHECKOUT  ->  store_order + store_orderitem rows created',
        '                 Product stock reduced in store_product',
        '                 Cart items deleted from store_cartitem',
        '5. REVIEW  ->  store_review row; product rating recalculated',
    ]
    for step in steps:
        print(f'  {step}')


def show_admin_access():
    print_header('ADMIN PANEL (visual database browser)')
    print('  URL:      http://127.0.0.1:8000/admin/')
    print('  Username: admin')
    print('  Password: admin123')
    print()
    print('  From admin you can view/edit every table: Products, Orders, Users, etc.')


if __name__ == '__main__':
    print()
    print('  ZIVI E-COMMERCE — DATABASE & BACKEND DEMONSTRATION')
    show_table_counts()
    show_schema()
    show_relationships()
    show_sample_data()
    show_data_flow()
    show_admin_access()
    print()
