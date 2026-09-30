# SavorLane — Mobile Food Ordering Experience

**CodeAlpha Full Stack Development Internship · Task 1: E-commerce Store**  
**Developed by Nadakudhuti Rupasri**

SavorLane is a responsive Django South Indian food ordering concept. Customers can discover dishes, compare dietary choices and preparation times, add meals to a session cart, and place a simulated delivery or pickup order. Its warm editorial interface is designed for phones first and adapts to desktop screens.

> Portfolio demo only. The menu and orders are fictional. Food visuals are AI-generated photo-style images, not photographs of actual dishes being sold. There is no payment gateway or real delivery service.

## Features

- Menu with keyword search, category and dietary filters, plus price and preparation-time sorting
- Dish detail pages with cuisine, ingredients, dietary label, spice level, price, and availability
- Session-backed shopping bag with quantity updates, removal, and calculated totals
- Account registration, sign-in, sign-out, and account-specific order history
- Delivery or pickup checkout with preferred time window and conditional address validation
- Stock validation and transactional order placement; saved order lines retain names and prices
- Django admin for menu and order management, SQLite persistence, and nine South Indian demo dishes with photo-style visuals
- Responsive layouts, accessible labels, mobile navigation, and a local photo-style food atlas

## Technology

Python 3.11+, Django 5.2, SQLite, HTML, CSS, JavaScript, and SVG. Dependencies use compatible ranges in `requirements.txt`.

## Quick start on Windows

1. Extract this ZIP and open the extracted folder containing `START.bat`.
2. Double-click `START.bat` from that folder. Or open PowerShell **in the same folder** and run `./START.bat` (PowerShell also accepts `.\START.bat`).
3. The script creates `.venv`, installs packages, applies migrations, loads the sample menu, and starts Django.
4. Open <http://127.0.0.1:8000/>. Register a new account to place a demo order.
5. Stop with **Ctrl+C**. Re-run `START.bat` to start again; seeding is safe to repeat.

If `START.bat` is not found, your terminal is in a different folder. Run `dir START.bat` to check, then `cd` into the extracted folder that contains the file. The virtual environment is inside that app folder, so from PowerShell use `.\.venv\Scripts\python.exe manage.py ...` there.

Only run one project on port 8000 at a time. A different port works with `python manage.py runserver 8001`.

## Manual setup

```powershell
py -3 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe manage.py migrate
.\.venv\Scripts\python.exe manage.py seed_data
.\.venv\Scripts\python.exe manage.py runserver
```

For Linux or macOS, use `python3 -m venv .venv`, `.venv/bin/pip install -r requirements.txt`, then `.venv/bin/python manage.py migrate`, `seed_data`, and `runserver`.

Create your own admin credentials with `.\.venv\Scripts\python.exe manage.py createsuperuser`; visit <http://127.0.0.1:8000/admin/>. Demo catalog items are not accounts, and there is no preset password. A customer account is created at `/register/`.

## Main routes

| Route | Purpose |
| --- | --- |
| `/` | Home and featured food |
| `/products/` | Searchable, filtered menu |
| `/products/<slug>/` | Dish details |
| `/cart/` | Shopping bag |
| `/checkout/` | Delivery or pickup demo checkout (sign-in required) |
| `/orders/` | Your order history (sign-in required) |
| `/register/`, `/login/`, `/admin/` | Customer registration, authentication, administration |

## Project layout

```text
CodeAlpha_SavorLane/
├── START.bat                Windows setup and launcher
├── manage.py
├── requirements.txt
├── savorlane_core/          Django settings and URL configuration
├── store/                   Models, views, forms, cart, admin, tests, migrations, seed command
├── templates/               Storefront and account pages
└── static/                  CSS, JavaScript, icon, and South Indian photo-style food atlas
```

## Checks

Run `.\.venv\Scripts\python.exe manage.py test` for the included catalog, delivery validation, and pickup order tests. `python manage.py check` validates Django configuration.

## Notes

SQLite (`db.sqlite3`) and `.venv` are generated locally and are intentionally excluded from the ZIP. The development server is intended only for local demonstration. For deployment, set `DJANGO_SECRET_KEY`, turn off debug, configure allowed hosts, and use production hosting.
