# PARTSTOCK API (Auto Parts Inventory)

A RESTful API built with **Django** and **Django REST Framework** for managing auto parts inventory, orchestrated with **Docker Compose**.

---

## 🚀 1. Getting Started

### 🧩 Prerequisites
Ensure you have **Docker** and **Docker Compose (v2)** installed.

Before running the project, rename the environment file:
```bash
cp .env.example .env
```

### ⚙️ 1.1. Run the Application
Build images and start all services in the background:
```bash
docker compose up --build -d
```

### 🛠️ 1.2. Initial Setup
After the services are up, apply database migrations and create an admin user:
```bash
docker compose exec web python manage.py createsuperuser
```

---

## 🧪 2. Running Tests

Execute the full test suite using the dedicated **test container**:
```bash
docker compose run --rm test pytest partstock/tests/
```

---

## 📚 3. API Endpoints Summary

> **Note:**  
> Authentication is required for all endpoints.  
> Write operations (**POST**, **DELETE**) require an **Admin User**.

---

### 🔐 3.1. Authentication

| Route | Method | Description |
|--------|---------|-------------|
| `/api/token/` | `POST` | Get access and refresh tokens |
| `/api/token/refresh/` | `POST` | Refresh access token |

---

### 🧰 3.2. Parts Management (`/api/parts/`)

| Method | Endpoint | Permission |
|---------|-----------|------------|
| `GET` | `/api/parts/` | Authenticated User |
| `POST` | `/api/parts/` | Admin |
| `DELETE` | `/api/parts/{pk}/` | Admin *(Protected by existing movements)* |
| `POST` | `/api/parts/upload/` | Admin *(Upload parts via file)* |
| `GET` | `/api/parts/upload/status/{pk}/` | Authenticated User *(Check upload task status)* |

---

### 📦 3.3. Stock Movements (`/api/movements/`)

| Method | Endpoint | Permission |
|---------|-----------|------------|
| `GET` | `/api/stock_movements/` | Authenticated User |
| `POST` | `/api/stock_movements/` | Admin |
| `GET` | `/api/stock_movements/{pk}/` | Authenticated User |

---

### 📑 3.4. Movement Items (`/api/movement_items/`)

| Method | Endpoint | Permission |
|---------|-----------|------------|
| `GET` | `/api/movement_items/` | Authenticated User |
| `POST` | `/api/movement_items/` | Admin |
| `GET` | `/api/movement_items/{pk}/` | Authenticated User |
| `DELETE` | `/api/movement_items/{pk}/` | Admin |

---
