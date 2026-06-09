import uuid
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Helper function to generate order IDs
def generate_order_id():
    return f"ZIVI-{uuid.uuid4().hex.upper()[:10]}"

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    zip_code = models.CharField(max_length=20, blank=True, null=True)
    dark_mode = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username}'s Profile"

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    try:
        instance.profile.save()
    except UserProfile.DoesNotExist:
        UserProfile.objects.create(user=instance)


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=120, unique=True)
    description = models.TextField(blank=True, null=True)
    image_url = models.CharField(max_length=500, blank=True, null=True)
    icon_class = models.CharField(max_length=50, blank=True, null=True) # e.g. "fa-tshirt" for icon display

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class Brand(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=120, unique=True)
    logo_url = models.CharField(max_length=500, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True, blank=True, related_name='products')
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    rating = models.FloatField(default=5.0)
    image_url = models.CharField(max_length=500)
    gallery_urls = models.TextField(blank=True, null=True, help_text="Comma-separated image URLs")
    stock = models.IntegerField(default=10)
    is_flash_sale = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    @property
    def final_price(self):
        if self.discount_price:
            return self.discount_price
        return self.price

    @property
    def is_discounted(self):
        return self.discount_price is not None and self.discount_price < self.price

    @property
    def discount_percentage(self):
        if self.is_discounted:
            diff = self.price - self.discount_price
            return int((diff / self.price) * 100)
        return 0

    @property
    def gallery_list(self):
        if self.gallery_urls:
            return [url.strip() for url in self.gallery_urls.split(',') if url.strip()]
        return [self.image_url]

    @property
    def is_in_stock(self):
        return self.stock > 0

    @property
    def rating_stars_full(self):
        return range(int(self.rating))

    @property
    def rating_stars_half(self):
        # returns 1 if has decimal >= 0.5, else 0
        dec = self.rating - int(self.rating)
        return 1 if dec >= 0.5 else 0

    @property
    def rating_stars_empty(self):
        full = int(self.rating)
        half = 1 if (self.rating - full) >= 0.5 else 0
        return range(5 - full - half)


class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wishlist')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='wishlisted_by')
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product')

    def __str__(self):
        return f"{self.user.username} - {self.product.name}"


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cart')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Cart of {self.user.username}"

    @property
    def total_items(self):
        return sum(item.quantity for item in self.items.all())

    @property
    def subtotal(self):
        return sum(item.total_price for item in self.items.all())

    @property
    def total_discount(self):
        # Calculate difference between original price total and final price total
        original_total = sum(item.product.price * item.quantity for item in self.items.all())
        return original_total - self.subtotal

    @property
    def delivery_charge(self):
        # Let's say delivery is free for orders above $50, otherwise $5.00
        if self.subtotal == 0:
            return 0.00
        elif self.subtotal >= 50:
            return 0.00
        else:
            return 5.00

    @property
    def grand_total(self):
        import decimal
        return self.subtotal + decimal.Decimal(self.delivery_charge)


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='cart_items')
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ('cart', 'product')

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

    @property
    def total_price(self):
        return self.product.final_price * self.quantity


class Order(models.Model):
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Processing', 'Processing'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
    )

    DELIVERY_OPTIONS = (
        ('Standard', 'Standard Delivery ($5.00, Free > $50)'),
        ('Express', 'Express Delivery ($15.00)'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    shipping_address = models.TextField()
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    delivery_option = models.CharField(max_length=20, choices=DELIVERY_OPTIONS, default='Standard')
    is_gift = models.BooleanField(default=False)
    gift_recipient_name = models.CharField(max_length=255, blank=True, null=True)
    gift_recipient_phone = models.CharField(max_length=20, blank=True, null=True)
    gift_message = models.TextField(blank=True, null=True)
    payment_option = models.CharField(max_length=50)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)
    order_id = models.CharField(max_length=50, unique=True, default=generate_order_id)

    def __str__(self):
        return f"Order {self.order_id} by {self.user.username}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='order_items')
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2) # Price at which product was purchased

    def __str__(self):
        return f"{self.quantity} x {self.product.name} in Order {self.order.order_id}"

    @property
    def total_price(self):
        return self.price * self.quantity


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveIntegerField(default=5)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s review on {self.product.name} ({self.rating} stars)"

    @property
    def rating_stars_full(self):
        return range(self.rating)

    @property
    def rating_stars_empty(self):
        return range(5 - self.rating)
