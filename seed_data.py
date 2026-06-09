import os
import django
import random
from django.utils.text import slugify

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'zivi_project.settings')
django.setup()

from django.contrib.auth.models import User
from store.models import Category, Brand, Product, Review, UserProfile

# Category-specific Unsplash image lists to ensure gorgeous visual variety
IMAGES_BY_CATEGORY = {
    "sports": [
        "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=600&auto=format&fit=crop",
        "https://images.unsplash.com/photo-1601925260368-ae2f83cf8b7f?w=600&auto=format&fit=crop",
        "https://images.unsplash.com/photo-1517838277536-f5f99be501cd?w=600&auto=format&fit=crop",
        "https://images.unsplash.com/photo-1517649763962-0c623066013b?w=600&auto=format&fit=crop",
        "https://images.unsplash.com/photo-1584735935682-2f2b69dff9d2?w=600&auto=format&fit=crop",
        "https://images.unsplash.com/photo-1552674605-db6ffd4facb5?w=600&auto=format&fit=crop",
        "https://images.unsplash.com/photo-1519766304817-4f37bda74a27?w=600&auto=format&fit=crop",
    ],
    "men": [
        "https://images.unsplash.com/photo-1507679799987-c73779587ccf?w=600&auto=format&fit=crop",
        "https://images.unsplash.com/photo-1596755094514-f87e34085b2c?w=600&auto=format&fit=crop",
        "https://images.unsplash.com/photo-1617137968427-85924c800a22?w=600&auto=format&fit=crop",
        "https://images.unsplash.com/photo-1618886614638-80e3c103d31a?w=600&auto=format&fit=crop",
        "https://images.unsplash.com/photo-1505022610485-0249ba5b3675?w=600&auto=format&fit=crop",
        "https://images.unsplash.com/photo-1492562080023-ab3db95bfbce?w=600&auto=format&fit=crop",
    ],
    "women": [
        "https://images.unsplash.com/photo-1595777457583-95e059d581b8?w=600&auto=format&fit=crop",
        "https://images.unsplash.com/photo-1612336307429-8a898d10e223?w=600&auto=format&fit=crop",
        "https://images.unsplash.com/photo-1572804013309-59a88b7e92f1?w=600&auto=format&fit=crop",
        "https://images.unsplash.com/photo-1485968579580-b6d095142e6e?w=600&auto=format&fit=crop",
        "https://images.unsplash.com/photo-1494790108377-be9c29b29330?w=600&auto=format&fit=crop",
        "https://images.unsplash.com/photo-1544005313-94ddf0286df2?w=600&auto=format&fit=crop",
    ],
    "girls": [
        "https://images.unsplash.com/photo-1621452773781-0f992fd1f5cb?w=600&auto=format&fit=crop",
        "https://images.unsplash.com/photo-1518831959646-742c3a14ebf7?w=600&auto=format&fit=crop",
        "https://images.unsplash.com/photo-1503919545889-aef636e10ad4?w=600&auto=format&fit=crop",
        "https://images.unsplash.com/photo-1607990283143-e81e7a2c93ab?w=600&auto=format&fit=crop",
        "https://images.unsplash.com/photo-1490902931801-d6f80ca94fe4?w=600&auto=format&fit=crop",
    ],
    "children": [
        "https://images.unsplash.com/photo-1519457431-44ccd64a579b?w=600&auto=format&fit=crop",
        "https://images.unsplash.com/photo-1519238263530-99bdd11df2ea?w=600&auto=format&fit=crop",
        "https://images.unsplash.com/photo-1502086223501-7ea6ecd79368?w=600&auto=format&fit=crop",
        "https://images.unsplash.com/photo-1471286174890-9c112ffca5b4?w=600&auto=format&fit=crop",
        "https://images.unsplash.com/photo-1515488042361-404e9250afef?w=600&auto=format&fit=crop",
    ],
    "toys": [
        "https://images.unsplash.com/photo-1587654780291-39c9404d746b?w=600&auto=format&fit=crop",
        "https://images.unsplash.com/photo-1596461404969-9ae70f2830c1?w=600&auto=format&fit=crop",
        "https://images.unsplash.com/photo-1559251606-c623743a6d76?w=600&auto=format&fit=crop",
        "https://images.unsplash.com/photo-1566577134770-3d85bb3a9cc4?w=600&auto=format&fit=crop",
        "https://images.unsplash.com/photo-1599643478518-a784e5dc4c8f?w=600&auto=format&fit=crop",
        "https://images.unsplash.com/photo-1531346878377-a5be20888e57?w=600&auto=format&fit=crop",
    ],
    "home": [
        "https://images.unsplash.com/photo-1578500494198-246f612d3b3d?w=600&auto=format&fit=crop",
        "https://images.unsplash.com/photo-1603006905003-be475563bc59?w=600&auto=format&fit=crop",
        "https://images.unsplash.com/photo-1567538096630-e0c55bd6374c?w=600&auto=format&fit=crop",
        "https://images.unsplash.com/photo-1505691938895-1758d7feb511?w=600&auto=format&fit=crop",
        "https://images.unsplash.com/photo-1513694203232-719a280e022f?w=600&auto=format&fit=crop",
        "https://images.unsplash.com/photo-1586023492125-27b2c045efd7?w=600&auto=format&fit=crop",
    ],
    "electronics": [
        "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=600&auto=format&fit=crop",
        "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=600&auto=format&fit=crop",
        "https://images.unsplash.com/photo-1587829741301-dc798b83add3?w=600&auto=format&fit=crop",
        "https://images.unsplash.com/photo-1527443224154-c4a3942d3acf?w=600&auto=format&fit=crop",
        "https://images.unsplash.com/photo-1572569511254-d8f925fe2cbb?w=600&auto=format&fit=crop",
        "https://images.unsplash.com/photo-1498049794561-7780e7231661?w=600&auto=format&fit=crop",
    ],
    "fashion": [
        "https://images.unsplash.com/photo-1576995853123-5a10305d93c0?w=600&auto=format&fit=crop",
        "https://images.unsplash.com/photo-1620799140408-edc6dcb6d633?w=600&auto=format&fit=crop",
        "https://images.unsplash.com/photo-1483985988355-763728e1935b?w=600&auto=format&fit=crop",
        "https://images.unsplash.com/photo-1515886657613-9f3515b0c78f?w=600&auto=format&fit=crop",
        "https://images.unsplash.com/photo-1539109136881-3be0616acf4b?w=600&auto=format&fit=crop",
    ],
    "beauty": [
        "https://images.unsplash.com/photo-1608248597279-f99d160bfcbc?w=600&auto=format&fit=crop",
        "https://images.unsplash.com/photo-1601049541289-9b1b7bbbfe19?w=600&auto=format&fit=crop",
        "https://images.unsplash.com/photo-1598440947619-2c35fc9aa908?w=600&auto=format&fit=crop",
        "https://images.unsplash.com/photo-1620916566398-39f1143ab7be?w=600&auto=format&fit=crop",
        "https://images.unsplash.com/photo-1596462502278-27bfdc403348?w=600&auto=format&fit=crop",
    ],
    "accessories": [
        "https://images.unsplash.com/photo-1511499767150-a48a237f0083?w=600&auto=format&fit=crop",
        "https://images.unsplash.com/photo-1627124765111-fcf214e87758?w=600&auto=format&fit=crop",
        "https://images.unsplash.com/photo-1524592094714-0f0654e20314?w=600&auto=format&fit=crop",
        "https://images.unsplash.com/photo-1523293182086-7651a899d37f?w=600&auto=format&fit=crop",
        "https://images.unsplash.com/photo-1547996160-81dfa63595aa?w=600&auto=format&fit=crop",
    ],
    "gifts": [
        "https://images.unsplash.com/photo-1548907040-4d42b52145ca?w=600&auto=format&fit=crop",
        "https://images.unsplash.com/photo-1584622650111-993a426fbf0a?w=600&auto=format&fit=crop",
        "https://images.unsplash.com/photo-1547793549-70bff8667646?w=600&auto=format&fit=crop",
        "https://images.unsplash.com/photo-1549465220-1a8b9238cd48?w=600&auto=format&fit=crop",
        "https://images.unsplash.com/photo-1512909006721-3d6018887383?w=600&auto=format&fit=crop",
    ]
}

# Vocabulary for product name generation by category
VOCABULARY = {
    "sports": {
        "prefixes": ["Pro", "Ultra", "Elite", "Active", "Apex", "Endure", "Velocity"],
        "nouns": ["Running Shoes", "Yoga Mat", "Kettlebell", "Steel Dumbbells", "Ergonomic Water Bottle", "Gym Duffel Bag", "Speed Skipping Rope", "Carbon Badminton Racket", "Championship Tennis Balls", "Thermal Track Pants"]
    },
    "men": {
        "prefixes": ["Casual", "Slim-Fit", "Classic", "Premium", "Tailored", "Urban", "Rustic"],
        "nouns": ["Linen Shirt", "Cotton Blazer", "Denim Jeans", "Chino Trousers", "Polo T-Shirt", "Leather Bomber Jacket", "Full-Grain Leather Belt", "Suede Chelsea Boots", "Formal Suit", "Woolen Cardigan"]
    },
    "women": {
        "prefixes": ["Floral", "Silk", "Knitted", "Designer", "Elegant", "Boho", "Graceful"],
        "nouns": ["Evening Wrap Dress", "Cotton Sundress", "Denim Pencil Skirt", "Knit Cardigan", "Saffiano Leather Handbag", "Stiletto Heels", "Leather Pointed Flats", "Silk Wrap Top", "Classic Trench Coat", "High-Waist Trousers"]
    },
    "girls": {
        "prefixes": ["Pastel", "Floral", "Checkered", "Embroidered", "Cute", "Sweet", "Playful"],
        "nouns": ["Pleated Skirt", "Knit Cardigan", "Cotton Frill Socks", "Sparkly Hairband Set", "Summer Sundress", "Active Canvas Sneakers", "Denim Jacket", "Graphic Tee", "Pajama Set"]
    },
    "children": {
        "prefixes": ["Kids", "Toddler", "Baby", "Soft", "Comfy", "Tiny", "Little"],
        "nouns": ["Waterproof Raincoat", "Denim Dungarees", "Organic Cotton Socks", "Fleece Pajamas", "Ribbed Cotton Romper", "Knitted Beanie", "Velcro Sneakers", "Warm Mittens", "Crewneck Tee"]
    },
    "toys": {
        "prefixes": ["Lego", "Interactive", "Wooden", "Cuddly", "Magic", "Creative", "Mindplay"],
        "nouns": ["Technic Race Car Kit", "Railway Train Set", "Stuffed Teddy Bear", "3D Wooden Puzzle", "Superhero Action Figure", "Strategy Board Game", "Fluffy Plush Dinosaur", "Modular Dollhouse"]
    },
    "home": {
        "prefixes": ["Minimalist", "Aromatic", "Nordic", "Ceramic", "Modern", "Bohemian", "Cozy"],
        "nouns": ["Flower Vase", "Soy Scented Candle Set", "Wood Lounge Chair", "Acoustic Table Lamp", "Framed Abstract Wall Art", "Velvet Cushion Covers", "Knit Throw Blanket", "Oak Coffee Table"]
    },
    "electronics": {
        "prefixes": ["Wireless", "Smart", "Mechanical", "Ultra-Thin", "Noise-Cancelling", "Hi-Fi", "HD"],
        "nouns": ["Over-Ear Headphones", "Sports Fitness Tracker", "RGB Mechanical Keyboard", "Ergonomic Gaming Mouse", "Aluminum Laptop Stand", "Bluetooth Waterproof Speaker", "Multi-Device Charger Dock", "Type-C Hub"]
    },
    "fashion": {
        "prefixes": ["Retro", "Breton", "Vintage", "Urban", "Streetwear", "Hipster", "Chic"],
        "nouns": ["Unisex Denim Jacket", "Cotton Crewneck Sweater", "Fleece Pullover Hoodie", "Multi-Pocket Cargo Pants", "Knitted Fringe Scarf", "Polarized Retro Sunglasses", "Canvas Tote Bag", "Leather Sneakers"]
    },
    "beauty": {
        "prefixes": ["Hydrating", "Cold-Pressed", "Mineral", "Organic", "Vegan", "Soothing", "Nourishing"],
        "nouns": ["Rosewater Facial Mist", "Pure Argan Oil", "SPF 50 Mineral Sunscreen", "Dead Sea Clay Mask", "Beeswax Lip Balm", "Hyaluronic Acid Serum", "Aloe Vera Moisturizer", "Sulfate-Free Shampoo"]
    },
    "accessories": {
        "prefixes": ["Retro", "Minimalist", "Quartz", "Polarized", "Sleek", "Classic", "Premium"],
        "nouns": ["Aviator Sunglasses", "Slim Bifold Leather Wallet", "Analog Quartz Wristwatch", "Engraved Wooden Keychain", "Water-Resistant Backpack", "Beaded Leather Bracelet", "Sterling Silver Ring"]
    },
    "gifts": {
        "prefixes": ["Gourmet", "Custom", "Relaxing", "Luxury", "Surprise", "Sweet", "Festive"],
        "nouns": ["Truffle Chocolate Box", "Custom Keyring", "Fizzy Bath Bomb Gift Set", "Essential Oil Diffuser", "Digital Gift Card", "Engraved Photo Frame", "Ceramic Mug Set", "Pampering Spa Voucher"]
    }
}

def seed_database():
    print("Initializing Database Seeding...")

    # Create Superuser if not exists
    if not User.objects.filter(username="admin").exists():
        User.objects.create_superuser("admin", "admin@zivi.com", "admin123")
        print("Created superuser: admin / admin123")

    # Create dummy users for reviews
    reviewers = []
    reviewer_data = [
        ("john_doe", "john@gmail.com", "John Doe"),
        ("sarah_m", "sarah@gmail.com", "Sarah Miller"),
        ("alex_p", "alex@gmail.com", "Alex Patterson"),
        ("lisa_k", "lisa@gmail.com", "Lisa K."),
    ]
    for username, email, full_name in reviewer_data:
        user, created = User.objects.get_or_create(username=username, email=email)
        if created:
            user.set_password("user123")
            first_name = full_name.split()[0]
            last_name = full_name.split()[1] if len(full_name.split()) > 1 else ""
            user.first_name = first_name
            user.last_name = last_name
            user.save()
            print(f"Created reviewer: {username}")
        reviewers.append(user)

    # Categories List
    categories_info = [
        {"name": "Sports", "slug": "sports", "icon_class": "fa-running", "image_url": "https://images.unsplash.com/photo-1461896836934-ffe607ba8211?w=600&auto=format&fit=crop"},
        {"name": "Men", "slug": "men", "icon_class": "fa-mars", "image_url": "https://images.unsplash.com/photo-1492562080023-ab3db95bfbce?w=600&auto=format&fit=crop"},
        {"name": "Women", "slug": "women", "icon_class": "fa-venus", "image_url": "https://images.unsplash.com/photo-1487412720507-e7ab37603c6f?w=600&auto=format&fit=crop"},
        {"name": "Girls", "slug": "girls", "icon_class": "fa-child-dress", "image_url": "https://images.unsplash.com/photo-1503919545889-aef636e10ad4?w=600&auto=format&fit=crop"},
        {"name": "Children", "slug": "children", "icon_class": "fa-child", "image_url": "https://images.unsplash.com/photo-1502086223501-7ea6ecd79368?w=600&auto=format&fit=crop"},
        {"name": "Toys", "slug": "toys", "icon_class": "fa-gamepad", "image_url": "https://images.unsplash.com/photo-1531346878377-a5be20888e57?w=600&auto=format&fit=crop"},
        {"name": "Home", "slug": "home", "icon_class": "fa-home", "image_url": "https://images.unsplash.com/photo-1513694203232-719a280e022f?w=600&auto=format&fit=crop"},
        {"name": "Electronics", "slug": "electronics", "icon_class": "fa-laptop", "image_url": "https://images.unsplash.com/photo-1498049794561-7780e7231661?w=600&auto=format&fit=crop"},
        {"name": "Fashion", "slug": "fashion", "icon_class": "fa-shirt", "image_url": "https://images.unsplash.com/photo-1483985988355-763728e1935b?w=600&auto=format&fit=crop"},
        {"name": "Beauty", "slug": "beauty", "icon_class": "fa-sparkles", "image_url": "https://images.unsplash.com/photo-1596462502278-27bfdc403348?w=600&auto=format&fit=crop"},
        {"name": "Accessories", "slug": "accessories", "icon_class": "fa-gem", "image_url": "https://images.unsplash.com/photo-1523293182086-7651a899d37f?w=600&auto=format&fit=crop"},
        {"name": "Gifts", "slug": "gifts", "icon_class": "fa-gift", "image_url": "https://images.unsplash.com/photo-1549465220-1a8b9238cd48?w=600&auto=format&fit=crop"},
    ]

    categories = {}
    for cat in categories_info:
        c, created = Category.objects.get_or_create(
            slug=cat["slug"],
            defaults={"name": cat["name"], "icon_class": cat["icon_class"], "image_url": cat["image_url"]}
        )
        categories[cat["slug"]] = c
        if created:
            print(f"Registered Category: {c.name}")

    # Brands List
    brands_info = [
        {"name": "Nike", "slug": "nike"},
        {"name": "Levi's", "slug": "levis"},
        {"name": "Lego", "slug": "lego"},
        {"name": "Apple", "slug": "apple"},
        {"name": "Philips", "slug": "philips"},
        {"name": "L'Oreal", "slug": "loreal"},
        {"name": "Rolex", "slug": "rolex"},
        {"name": "Hallmark", "slug": "hallmark"},
        {"name": "Zara", "slug": "zara"},
        {"name": "Zivi Originals", "slug": "zivi-originals"},
    ]

    brands = {}
    for br in brands_info:
        b, created = Brand.objects.get_or_create(
            slug=br["slug"],
            defaults={"name": br["name"], "logo_url": ""}
        )
        brands[br["slug"]] = b
        if created:
             print(f"Registered Brand: {b.name}")

    # Programmatic Generation: 20-30 Products for each Category
    total_products_seeded = 0
    print("Generating products programmatically...")

    review_texts = [
        "Absolutely love this product! Exceeded my expectations. Shipping was incredibly fast.",
        "Very good quality for the price. Customer service was helpful, will buy again.",
        "Decent product, does the job. Came exactly as described. Standard delivery was prompt.",
        "Super premium feel. Highly recommended to everyone looking for quality.",
        "Exceeded all my expectations. High-grade materials and beautifully designed.",
        "Nice, clean aesthetics. It integrates very well and feels premium.",
        "Fast shipping! Ordered on Monday, arrived by Wednesday. Perfect seller support.",
        "Absolutely worth every cent. Will recommend Zivi to my friends."
    ]

    for cat_slug, cat_obj in categories.items():
        vocab = VOCABULARY.get(cat_slug, VOCABULARY["fashion"])
        images = IMAGES_BY_CATEGORY.get(cat_slug, IMAGES_BY_CATEGORY["fashion"])
        
        # Decide how many products to generate for this category (between 21 and 26 to guarantee "at least 20-30")
        num_products = random.randint(21, 26)
        
        brand_keys = list(brands.keys())
        
        for idx in range(1, num_products + 1):
            # Generate a nice name
            pref = random.choice(vocab["prefixes"])
            noun = random.choice(vocab["nouns"])
            name = f"{pref} {noun}"
            
            # To avoid duplicates if combinations conflict, append index
            # Check unique combinations
            slug = slugify(f"{name}-{cat_slug}-{idx}")
            
            # Image URL
            img_url = images[(idx - 1) % len(images)]
            
            # Gallery URLs (cycle through images, pick 2 other random ones from list)
            other_imgs = [img for img in images if img != img_url]
            gallery_sample = random.sample(other_imgs, min(2, len(other_imgs)))
            gallery_urls = ",".join([img_url] + gallery_sample)

            # Price
            price = random.randint(15, 299) + 0.99
            price = round(price, 2)
            
            # Discount (approx 40% of products are discounted)
            discount_price = None
            if random.random() < 0.40:
                 discount_pct = random.choice([10, 15, 20, 25, 30, 40, 50])
                 discount_price = round(price * (1 - discount_pct/100), 2)
            
            # Rating
            rating = round(random.uniform(4.0, 5.0), 1)

            # Flash sale (approx 15% of products are flash sales)
            is_flash_sale = random.random() < 0.15
            
            # Featured (approx 15% are featured)
            is_featured = random.random() < 0.15

            # Stock
            stock = random.choice([0, 5, 8, 12, 15, 20, 30, 50])

            # Brand selection
            selected_brand = brands[random.choice(brand_keys)]
            
            # Description
            description = (
                 f"Premium {name} tailored for excellence. Designed with top-grade materials "
                 f"incorporating modern technology to guarantee premium durability and style. "
                 f"The perfect addition to your collection, backed by Zivi's standard quality checks, "
                 f"lightning-fast delivery, and robust service support structure."
            )

            product, created = Product.objects.get_or_create(
                slug=slug,
                defaults={
                    "name": name,
                    "category": cat_obj,
                    "brand": selected_brand,
                    "description": description,
                    "price": price,
                    "discount_price": discount_price,
                    "rating": rating,
                    "image_url": img_url,
                    "gallery_urls": gallery_urls,
                    "stock": stock,
                    "is_flash_sale": is_flash_sale,
                    "is_featured": is_featured
                }
            )

            if created:
                 total_products_seeded += 1
                 # Add 2-3 reviews per product
                 num_reviews = random.randint(2, 4)
                 selected_reviewers = random.sample(reviewers, num_reviews)
                 for reviewer in selected_reviewers:
                      Review.objects.create(
                          user=reviewer,
                          product=product,
                          rating=random.choice([4, 5]),
                          comment=random.choice(review_texts)
                      )

        print(f"Generated {num_products} products in '{cat_obj.name}' category.")

    print(f"Seeding finished. Added {total_products_seeded} new products. Database is fully populated!")

if __name__ == "__main__":
    seed_database()
