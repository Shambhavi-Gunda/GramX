

---

# 🚀 gramX – Full Stack Social Media Application

**gramX** is a **full-stack social media platform** built using **FastAPI (backend)** and **Streamlit (frontend)** that allows users to **sign up, log in, upload images & videos, view a live feed, and manage their posts**.

This project demonstrates **end-to-end full-stack development**, including API design, authentication, cloud media handling, and frontend–backend integration.

---

## ✨ Features

* 🔐 JWT Authentication (Login & Signup)
* 👤 User Management
* 📸 Image & Video Upload
* 🖼️ Real-time Feed Display
* 🗑️ Delete Own Posts
* 🧠 Session-based Login Handling
* 🌐 RESTful APIs using FastAPI
* ⚡ Interactive UI using Streamlit
* ☁️ ImageKit Cloud Storage Integration
* 🗃️ Async SQLAlchemy Database

---

## 🏗️ Tech Stack

### Backend

* FastAPI
* SQLAlchemy (Async)
* FastAPI Users (Authentication)
* SQLite
* ImageKit

### Frontend

* Streamlit
* Requests

---

## 📁 Project Structure

```
FASTAPI/
│
├── app/
│   ├── app.py          # FastAPI backend
│   ├── db.py           # Database models & session
│   ├── users.py        # Authentication logic
│   ├── imagekit.py     # ImageKit config
│   └── schemas.py      # Pydantic schemas
│
├── frontend.py         # Streamlit frontend
├── test.db             # SQLite database
├── .env                # Environment variables
└── README.md
```

---

## ⚙️ Setup Instructions

### 1️⃣ Clone Repository

```bash
git clone https://github.com/your-username/gramX.git
cd gramX
```

---

### 2️⃣ Create Virtual Environment

```bash
python -m venv .venv
.venv\Scripts\activate     # Windows
source .venv/bin/activate  # Mac/Linux
```

---

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 4️⃣ Start Backend Server

```bash
uvicorn app.app:app --reload --port 8001
```

Backend runs at:

```
http://127.0.0.1:8001
```

Swagger API Docs:

```
http://127.0.0.1:8001/docs
```

---

### 5️⃣ Start Frontend (Streamlit)

Open a new terminal:

```bash
streamlit run frontend.py
```

Frontend runs at:

```
http://localhost:8501
```

---

## 🔄 Application Flow

```
User → Streamlit UI → FastAPI API → Database + ImageKit → Response → UI
```

---

## 🧪 API Endpoints

| Method | Endpoint          | Description       |
| ------ | ----------------- | ----------------- |
| POST   | `/auth/register`  | Register new user |
| POST   | `/auth/jwt/login` | Login             |
| GET    | `/users/me`       | Get current user  |
| POST   | `/upload`         | Upload media      |
| GET    | `/feed`           | Get feed          |
| DELETE | `/posts/{id}`     | Delete post       |

---

## 🚀 Key Learnings

* End-to-end **full-stack system design**
* JWT authentication & secure API access
* Media upload + cloud storage handling
* Async database operations
* Frontend-backend integration
* Debugging real-world production issues

---

## 📌 Future Enhancements

* ❤️ Like system
* 💬 Comments
* 👤 User profile pages
* 🔔 Notifications
* 📜 Infinite scrolling feed
* 🌙 Dark mode UI

---

## 👩‍💻 Author

**Shambhavi Gunda**
Computer Science Student | Full-Stack Developer | ML Enthusiast

---

## ⭐ Support

If you like **gramX**, give it a ⭐ on GitHub — it helps a lot!

