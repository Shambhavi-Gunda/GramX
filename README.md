# GramX

GramX is a simple Instagram-like social media backend built using **FastAPI**.
The project focuses on core social media features such as user interactions, posts, and feeds, while following clean API design and scalable backend practices.

This project is being developed incrementally to strengthen backend development skills and maintain consistent GitHub contributions.

---

## 🚀 Features (Planned & In Progress)

* User authentication (signup & login)
* Create and fetch posts
* User feed (similar to Instagram timeline)
* Like and comment functionality
* Secure and scalable API design

---

## 🛠️ Tech Stack

* **Backend Framework:** FastAPI
* **Language:** Python
* **Server:** Uvicorn
* **Version Control:** Git & GitHub

---

## 📁 Project Structure

```
GramX/
│
├── app/
│   └── app.py        # FastAPI application
│
├── main.py           # Application entry point
├── README.md
├── pyproject.toml
└── uv.lock
```

---

## ▶️ How to Run the Project

1. Clone the repository:

   ```bash
   git clone https://github.com/Shambhavi-Gunda/GramX.git
   ```

2. Navigate into the project directory:

   ```bash
   cd GramX
   ```

3. Install dependencies:

   ```bash
   python -m pip install fastapi uvicorn
   ```

4. Run the server:

   ```bash
   uvicorn app.app:app --host 127.0.0.1 --port 8001
   ```

5. Open in browser:

   * API: `http://127.0.0.1:8001`
   * Docs: `http://127.0.0.1:8001/docs`

---

## 📌 Project Status

🚧 **Under active development**
New features and improvements are being added regularly.

---

## ✨ Motivation

GramX is built as a learning-focused project to understand backend development, REST APIs, and real-world application structure inspired by Instagram.

---
