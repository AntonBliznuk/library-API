# 📚 library-API

## ⚠️ Warning
*Celery and Celery Beat run only in development, as there is no free worker deployment platform currently used.*

## 📝 Description

### ❓ Why?

This project was created to build a robust and reliable API while exploring modern technologies like Celery, Redis, Stripe, and Docker. It simulates real-world functionality such as book inventory tracking, payments, and notifications.

### ⚙️ How?

The solution uses Django and Django REST Framework to build the API, PostgreSQL as the database, Redis for task brokering, Celery & Celery Beat for background processing, and Stripe for handling payments. It also integrates with the Telegram API for sending real-time notifications. Everything is containerized using Docker for easy local setup and reproducibility.

### 👥 For Who?

This project is designed for:
- 👨‍💻 Frontend developers looking for a production-style API to integrate with
- 🎓 Backend developers who want to explore Django, Celery, Stripe, and Docker
- 🔍 Developers searching for reusable and extendable API 

## 🔗 See in Action

- 🌐 Live app: https://library-api-m7bp.onrender.com/api/doc/swagger
- 📢 Telegram bot group: https://t.me/+xWoCk5JuSa9kZmYy

## ✨ Features
- 📚 Books: Tracks available inventory of books
- 🔁 Borrowings: Updates book availability in real time
- 💳 Payments: Stripe integration for handling borrow fees
- 🤖 Telegram Notifications: Bot sends updates on borrow creation
- ⏰ Overdue Tasks: Celery Beat handles borrow expiration checks
- ✅ Payment Confirmations: Sends successful payment messages
- 🧪 Interactive Docs: Swagger UI documentation
- 🔐 Authentication: Secure JWT-based user authentication
- 🐳 Fully Dockerized: Easy to run using Docker Compose
- ⚙️ Developer Friendly: Minimal setup for local environment

## 🧰 Tech Stack

### 🗄️ Backend:
- Python 3.12
- Django 5.x
- Django REST Framework
- PostgreSQL
- Redis
- Celery + Celery Beat
- Stripe API
- Telegram Bot API
- JWT (via SimpleJWT)
- Swagger/OpenAPI
- Docker + Docker Compose

### 🛠️ Tools & Others:
- python-dotenv
- Render (deployment)

## 💻 Local Installation

> 🐳 Make sure [Docker](https://docs.docker.com/get-docker/) is installed.

**1. Clone the repo**:
```bash
git clone https://github.com/AntonBliznuk/library-API
cd library-API
```
**2. Create your environment config**:
```bash
cp .env.example .env
```
✏️ Modify .env with your own credentials.

**3. Build and run the project container**:
```bash
docker-compose up --build
```

**4. Access the app**:
- Admin panel: http://0.0.0.0:8000/admin/
- Swagger UI: http://0.0.0.0:8000/api/doc/swagger/
- Redoc: http://0.0.0.0:8000/api/doc/redoc/

**👑 Admin user credentials:**
> also works in production
- email: admin@admin.com
- password: admin


## 🏞️ UI Preview

This project is API-only, no frontend UI provided.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.


## 📬 Contact

- **Author**: Anton Bliznuk
- **Email**: bliznukantonmain@gmail.com
- **GitHub**: https://github.com/AntonBliznuk
- **LinkedIn**: https://www.linkedin.com/in/anton-bliznuk-3499b234b
