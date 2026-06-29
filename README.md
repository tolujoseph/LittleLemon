# LittleLemon Restaurant API

A production-ready REST API for a restaurant booking and menu management system, built as the capstone project for the **Meta Backend Developer Professional Certificate** on Coursera.

## What This Project Demonstrates

- **Django REST Framework** — ListCreateAPIView, RetrieveUpdateDestroyAPIView, ModelViewSet
- **Token Authentication** — via Djoser and DRF's built-in token auth
- **Role-Based Permissions** — managers (is_staff) can create/update/delete menu items; regular authenticated users have read-only access
- **API Testing** — 35 unit tests across auth, menu, and booking endpoints using Django's APITestCase
- **MySQL Database** — production database configuration with Django ORM
- **RESTful API Design** — consistent endpoint structure, proper HTTP status codes, serializer validation

---

## Project Structure

LittleLemon/

└── littlelemon/

├── littlelemon/          # Project settings and URL config

│   ├── settings.py

│   └── urls.py

├── restaurant/           # Main app

│   ├── models.py         # Menu and Booking models

│   ├── serializers.py    # DRF serializers

│   ├── views.py          # API views with role-based permissions

│   ├── urls.py           # App-level URL routing

│   └── tests/

│       ├── test_menu.py      # 14 tests — CRUD + permissions

│       ├── test_bookings.py  # 9 tests — booking endpoints

│       ├── test_auth.py      # 10 tests — registration, login, logout

│       ├── test_models.py    # Model unit tests

│       └── test_views.py     # View integration tests

└── manage.py

---

## Prerequisites

- Python 3.11+
- MySQL 8.0+
- pip

---

## Installation

**1. Clone the repository**
```bash
git clone https://github.com/tolujoseph/LittleLemon.git
cd LittleLemon/littlelemon
```

**2. Create and activate a virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

**3. Install dependencies**
```bash
pip install django djangorestframework djoser mysqlclient djangorestframework-simplejwt python-dotenv
```

**4. Set up the MySQL database**
```sql
CREATE DATABASE LittleLemon;
```

**5. Update database credentials in `littlelemon/settings.py`**
```python
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "LittleLemon",
        "USER": "your_mysql_user",
        "PASSWORD": "your_mysql_password",
        "HOST": "127.0.0.1",
        "PORT": "3306",
    }
}
```

**6. Run migrations**
```bash
python manage.py migrate
```

**7. Create a superuser (manager account)**
```bash
python manage.py createsuperuser
```

---

## Running the API

```bash
python manage.py runserver
```

The API will be available at `http://127.0.0.1:8000`

---

## Running the Tests

```bash
python manage.py test restaurant.tests --verbosity=2
```

Expected output: **35 tests, 0 failures**

### Test Coverage

| File | Tests | What it covers |
|---|---|---|
| `test_menu.py` | 14 | Full CRUD on menu items, manager vs regular user permissions, unauthenticated access |
| `test_bookings.py` | 9 | Booking creation, retrieval, update, delete — authenticated vs unauthenticated |
| `test_auth.py` | 10 | User registration, password validation, token login/logout, profile retrieval |
| `test_models.py` | 1 | Menu model string representation |
| `test_views.py` | 1 | Menu list endpoint serializer consistency |

---

## API Endpoints

### Authentication (Djoser)

| Method | Endpoint | Description | Auth Required |
|---|---|---|---|
| POST | `/auth/users/` | Register a new user | No |
| POST | `/auth/token/login/` | Obtain auth token | No |
| POST | `/auth/token/logout/` | Invalidate auth token | Yes |
| GET | `/auth/users/me/` | Get current user profile | Yes |

### Menu

| Method | Endpoint | Description | Auth Required |
|---|---|---|---|
| GET | `/restaurant/menu/items` | List all menu items | No |
| POST | `/restaurant/menu/items` | Create a menu item | Manager only |
| GET | `/restaurant/menu/items/<id>` | Get a single menu item | No |
| PUT | `/restaurant/menu/items/<id>` | Update a menu item | Manager only |
| PATCH | `/restaurant/menu/items/<id>` | Partially update a menu item | Manager only |
| DELETE | `/restaurant/menu/items/<id>` | Delete a menu item | Manager only |

### Bookings

| Method | Endpoint | Description | Auth Required |
|---|---|---|---|
| GET | `/restaurant/booking/tables/` | List all bookings | Yes |
| POST | `/restaurant/booking/tables/` | Create a booking | Yes |
| GET | `/restaurant/booking/tables/<id>/` | Get a single booking | Yes |
| PUT | `/restaurant/booking/tables/<id>/` | Update a booking | Yes |
| DELETE | `/restaurant/booking/tables/<id>/` | Delete a booking | Yes |

---

## Authentication Usage

**Register a user:**
```bash
curl -X POST http://127.0.0.1:8000/auth/users/ \
  -H "Content-Type: application/json" \
  -d '{"username": "john", "password": "securepass123", "re_password": "securepass123"}'
```

**Get a token:**
```bash
curl -X POST http://127.0.0.1:8000/auth/token/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "john", "password": "securepass123"}'
```

**Use the token:**
```bash
curl http://127.0.0.1:8000/restaurant/booking/tables/ \
  -H "Authorization: Token <your_token_here>"
```

---

## Built With

- [Django](https://www.djangoproject.com/) 6.0
- [Django REST Framework](https://www.django-rest-framework.org/) 3.17
- [Djoser](https://djoser.readthedocs.io/) 2.3
- [MySQL](https://www.mysql.com/) 8.0
EOF