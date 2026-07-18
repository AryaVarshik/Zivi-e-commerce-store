# Zivi E-Commerce Web Application

### 🔗 Live Website: [http://aryavarshikchepyala.pythonanywhere.com/](http://aryavarshikchepyala.pythonanywhere.com/)

Zivi is a premium, fully responsive, full-stack e-commerce web application featuring a modern orange-and-white color palette, dynamic carousels, responsive product grids, user authentication, a wishlist, cart system, multi-step checkout process with gift options, dark/light mode toggle, settings management, and reviews slider. 

The application is built on **Django (Python)** with **SQLite** for the database, utilizing Django templates for rendering, and vanilla CSS/JS for frontend logic and animations.

---

## Key Features

1. **Stunning Orange & White UI**: Tailored color scheme using modern typography, harmonized contrast, and subtle micro-animations.
2. **Interactive 10-Slide Banner Slider**: Uses different grid layouts (1-grid, 2-grid, 4-grid, 6-grid, 10-product promo) representing different product categories (Fashion, Sports, Men, Girls, Children, Toys, Electronics, Home, Beauty, Accessories, Gifts). Slide 1 includes custom CSS expression-style animations.
3. **Advanced Filtering Engine**: Filters products dynamically by price range, brand, category, rating stars, discounts, and stock availability.
4. **Ajax-Powered Shopping Cart**: Increase/decrease items quantities or delete items inline. Subtotal, delivery fee, discounts, and grand totals recalculate instantly via AJAX without page reloads.
5. **Interactive Wishlist**: Add products to wishlist, view list, remove items, or move items to cart smoothly.
6. **Multi-Step Checkout**: Add shipping addresses, toggle conditional recipient gift info + message inputs, and choose between custom payment methods (Cash on Delivery, UPI, Cards, Net Banking, and Wallets).
7. **Robust Authentication**: Django auth-controlled views. Browsing is open to guests, but additions to cart/wishlist redirect to login with user-friendly warnings.
8. **Dynamic Light & Dark Modes**: PERSISTENT theme selection saved in local storage and synchronized across navbar switches and settings preferences.
9. **Interactive Reviews Carousel**: Auto-sliding user reviews at the bottom of the home page, and review creation forms inside product details.
10. **Seeded Catalog**: Includes a database seeder script populating 12 categories, multiple brands, and 240+ unique products (20+ per category) automatically on start.

---

## Tech Stack
* **Frontend**: Vanilla HTML5, Vanilla CSS3, Vanilla JavaScript (ES6), FontAwesome Icons
* **Backend**: Django (Python 3.13)
* **Database**: SQLite3
* **Development Server**: Django runserver

---

## Installation & Setup

Ensure you have **Python 3** and **pip** installed. Follow these steps:

### 1. Clone or Open the Directory
Open your terminal inside the workspace directory (`splendid-bohr`).

### 2. Set Up Virtual Environment & Install Dependencies
Create a virtual environment and install Django:
```bash
# Create venv
python -m venv venv

# Install Django
# Windows PowerShell:
.\venv\Scripts\pip install django

# Linux/macOS:
source venv/bin/activate
pip install django
```

### 3. Run the Bootstrap Script (Frictionless Launch)
We have bundled all setup, migrations, database seeding, and server starting into a single script. Simply run:
```bash
python run.py
```
This script will automatically:
1. Generate store database migrations.
2. Apply migrations to SQLite.
3. Call `seed_data.py` to create the Superuser and populate 240+ products across 12 categories.
4. Launch the local development server at `http://127.0.0.1:8000/`.

---

## Default Admin Credentials
The seeding script creates a default superuser account for managing the platform:
* **URL**: `http://127.0.0.1:8000/admin/`
* **Username**: `admin`
* **Password**: `admin123`

---

## Project Structure
```
splendid-bohr/
├── manage.py            # Django management command file
├── run.py               # Frictionless launch bootstrap script
├── seed_data.py         # 240+ products database seeder script
├── zivi_project/        # Project settings & URL routing
│   ├── settings.py      # Main settings configuration
│   └── urls.py          # Main URL patterns
└── store/               # Store main app directory
    ├── models.py        # Database models (Products, Cart, Orders, Reviews)
    ├── views.py         # Main views and AJAX API views
    ├── urls.py          # Clean app routing urls
    ├── admin.py         # Custom Django Admin panel registrations
    ├── static/          # App static assets
    │   └── store/
    │       ├── css/
    │       │   └── style.css  # Premium stylesheet
    │       └── js/
    │           └── script.js  # Interactive controllers
    └── templates/       # HTML template directory
        └── store/
            ├── base.html          # Main HTML structure shell
            ├── home.html          # Carousel, grids, reviews & filters
            ├── flash_sale.html    # Mega-discounts + countdown ticking
            ├── product_detail.html# Image gallery, options, related products & comments
            ├── wishlist.html      # Saved items dashboard
            ├── cart.html          # Shopping cart with inline AJAX total updates
            ├── checkout.html      # Gifting options + payment tabs
            ├── login.html         # Sign-in panel
            ├── signup.html        # Register panel
            ├── profile.html       # Edit profile details & previous orders
            ├── settings.html      # Theme switch & Accordion FAQ support
            ├── about.html         # Story, values & mission board
            └── order_success.html # Order ID summary + est. delivery dates
```

---

## Screenshots Placeholder
Below are placeholders for screenshots of the Zivi platform:
* **Home Page**: `C:\Users\aryav\Documents\antigravity\splendid-bohr\screenshots\home.png`
* **Checkout Page**: `C:\Users\aryav\Documents\antigravity\splendid-bohr\screenshots\checkout.png`
* **Product Details**: `C:\Users\aryav\Documents\antigravity\splendid-bohr\screenshots\detail.png`

---

## Future Improvements
1. **Dynamic Images**: Connect product image fields directly to an image storage bucket (e.g. AWS S3) for manual uploads in the Admin.
2. **Actual Payments**: Integrate Stripe, PayPal, or UPI merchant gateways on checkout.
3. **Delivery Tracking**: Add live delivery tracking and SMS/Email notifications on status updates.
