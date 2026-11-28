# Sakina Online Stores

A small online shop built with Django. Customers browse products, add them to
a cart and place orders (payment on delivery). Shop staff manage products and
update order status.

## Features
- Customer registration, login and logout
- Product list and detail pages with categories
- Session-based shopping cart
- Checkout and order history (customers see only their own orders)
- Staff-only product add, edit and delete
- Order status updates in the admin (Pending, Shipped, Delivered)
- JSON API: /api/products/ (optional ?in_stock=1)

## How to run
1. Clone the repository
2. Create and activate a virtual environment:
   python -m venv .venv
   .venv\Scripts\Activate.ps1
3. Install packages: pip install -r requirements.txt
4. Create the database: python manage.py migrate
5. Create a shop owner account: python manage.py createsuperuser
6. Start the server: python manage.py runserver
7. Open http://127.0.0.1:8000/

## Security
CSRF tokens on all forms, automatic output escaping (XSS), ORM queries
(no raw SQL), hashed passwords, staff-only views, login-required checkout,
and settings that can come from environment variables.

## Technologies
Python, Django, SQLite, HTML/CSS