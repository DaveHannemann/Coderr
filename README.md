# Marketplace Backend API

Built as part of a full-stack learning journey.

This project is a **RESTful backend API for a marketplace platform** built with **Django** and **Django Rest Framework**.

The API allows users to create profiles, publish offers, place orders, and leave reviews with a clear role-based system (customer vs business).

This project was created to **practice and deepen backend architecture, validation logic, and role-based permissions with Django Rest Framework**.

---

# Features

* User registration and authentication (Token Authentication)
* Customer and Business profile system
* Create and manage offers with pricing tiers (basic, standard, premium)
* Order system with status workflow
* Review system with validation (only after interaction)
* Role-based permissions (customer vs business)
* Advanced filtering, search, and ordering
* Aggregated platform statistics

---

# Technologies

* Python 3.12
* Django
* Django Rest Framework
* django-filter
* Token Authentication
* SQLite (default Django database)

---

# Permissions

The API includes several custom permission classes:

* **Business User Only**
  Only business users can create and manage offers.

* **Order Ownership**
  Only the assigned business user or admin can modify orders.

* **Customer Only Actions**
  Only customers can create orders and reviews.

* **Review Ownership**
  Only the creator of a review can edit or delete it.

---

# Core Logic

Some important backend rules implemented in this project:

* Offers must include exactly:
  - basic
  - standard
  - premium

* Orders:
  - Created from an offer detail (snapshot logic)
  - Status transitions:
    - `in_progress → completed`
    - `in_progress → cancelled`

* Reviews:
  - Only allowed after an order exists between users
  - Only one review per business per customer

* Filtering:
  - Strict query parameter validation
  - Unknown parameters return errors

---

# Installation

Clone the repository:

```
git clone <repository-url>
cd backend
```

Create a virtual environment:

```
python -m venv venv
```

Activate the environment:

Linux / Mac

```
source venv/bin/activate
```

Windows

```
venv\Scripts\activate
```

Install dependencies:

```
pip install -r requirements.txt
```

Run migrations:

```
python manage.py migrate
```

Start the development server:

```
python manage.py runserver
```

---

# Purpose of this Project
This project was built to practice:

* Django Rest Framework
* REST API design
* role-based permissions
* serializer validation
* business logic enforcement
* query optimization with `select_related` and `annotate`

---

# License

This project is intended for **educational purposes**.