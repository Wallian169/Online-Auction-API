# 🏆 Auction Platform

An online auction platform built with Django, DRF, and PostgreSQL. The system supports user authentication, bidding, and automated auction closing using Celery.

## 🚀 Features

- **User Authentication** – Secure login and registration.
- **Auction Management** – Create, update, and monitor auctions.
- **Bidding System** – Place and track bids in real time.
- **Automated Auction Closing** – Background tasks using Celery and Redis.
- **REST API** – Expose auction data via a well-structured API.
- **Database Support** – PostgreSQL for robust and scalable data storage.
- **Dockerized Deployment** – Easily deploy the project using Docker.

## 🏗️ Tech Stack

- **Backend:** Python, Django, Django REST Framework (DRF)
- **Database:** PostgreSQL
- **Task Queue:** Celery + Redis
- **Containerization:** Docker, Docker Compose

## 🔧 Installation & Setup

### 1️⃣ Prerequisites
Ensure you have the following installed:

- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)

### 2️⃣ Clone the Repository
```bash
git clone https://github.com/yourusername/auction-platform.git
cd auction-platform
```

### 3️⃣ Environment Variables
Create a `.env` file in the project root and configure the following variables:
```env
DJANGO_SECRET_KEY=your_secret_key
POSTGRES_DB=auction_db
POSTGRES_USER=auction_user
POSTGRES_PASSWORD=secure_password
REDIS_HOST=redis
REDIS_PORT=6379
```

### 4️⃣ Start the Application
Run the following command to start the project using Docker:
```bash
docker-compose up --build
```
After first built use:
```bash
docker-compose up
```

### 5️⃣Create a Superuser, load categories preset
```bash
docker exec -it mate_auction_be-app-1 
```

```bash
python manage.py createsuperuser
```
```bash
python manage.py loaddata categories.json
```

### ️6️⃣ Access the Application
- **API Endpoints:** `http://localhost:8000/api/`
- **Admin Panel:** `http://localhost:8000/admin/`

## 🛠️ Useful Commands

### Check Logs
```bash
docker-compose logs -f
```

### Stop Containers
```bash
docker-compose down
```

## 📜 API Documentation
You can access the automatically generated API documentation at:
```
http://localhost:8000/api/schema/swagger-ui/
```
or
```
http://localhost:8000/redoc/
```

## 📌 Future Enhancements
- WebSocket integration for real-time bidding updates.
- Advanced filtering and search for auctions.
- Role-based access control.

## 💡 Contributing
Feel free to open issues and submit pull requests to enhance the platform.

## 📜 License
This project is licensed under the MIT License.

---
🚀 Happy Bidding!
