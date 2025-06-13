# 🧾 TaskTrackr

> A clean and professional FastAPI project built to demonstrate 12-Factor App methodology and DevOps best practices from the ground up.

---

## 🧠 Project Overview

**TaskTrackr** is a CRUD-based task management API, designed as a beginner-friendly project to explore:

* Scalable web application architecture
* Configuration management using environment variables
* Containerization with Docker
* PostgreSQL integration via SQLAlchemy
* CI/CD workflows and cloud deployment readiness

---

## 🚀 Tech Stack

| Purpose          | Technology               |
| ---------------- | ------------------------ |
| 🌐 Web Framework | FastAPI                  |
| 💄 ORM           | SQLAlchemy               |
| 🐘 Database      | PostgreSQL (via Docker)  |
| 🐳 Containers    | Docker + Docker Compose  |
| ⚙️ Config Mgmt   | `.env` + `python-dotenv` |
| 🔁 CI/CD         | GitHub Actions           |
| ☁️ Deployment    | Render / Fly.io          |

---

## 📆 12-Factor App Implementation

| #      | Principle           | Implementation Summary                   |
| ------ | ------------------- | ---------------------------------------- |
| 1️⃣    | Codebase            | Tracked via Git, hosted on GitHub        |
| 2️⃣    | Dependencies        | Managed in `requirements.txt`            |
| 3️⃣    | Config              | Loaded securely via `.env` file          |
| 4️⃣    | Backing Services    | PostgreSQL service managed by Docker     |
| 5️⃣    | Build, Release, Run | Docker + GitHub Actions pipeline         |
| 6️⃣    | Processes           | Stateless app; data stored in DB         |
| 7️⃣    | Port Binding        | Uses port from environment configuration |
| 8️⃣    | Concurrency         | Supports Gunicorn deployment             |
| 9️⃣    | Disposability       | Fast start/stop with Docker              |
| 🔟     | Dev/prod parity     | Docker Compose for matching environments |
| 1️⃣1️⃣ | Logs                | Logs to console (stdout)                 |
| 1️⃣2️⃣ | Admin Processes     | DB seeding with `init_db.py`             |

---

## 📂 Project Structure

```bash
tasktrackr/
├── app/
│   ├── db/
│   │   ├── __init__.py
│   │   ├── database.py
│   │   ├── models.py
│   │   └── init_db.py
│   ├── routes/
│   │   └── tasks.py
│   └── main.py
├── docker-compose.yml
├── .env
├── .env.example
├── requirements.txt
├── README.md
```

---

## ⚙️ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/tasktrackr.git
cd tasktrackr
```

### 2. Set Up Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # or venv\Scripts\activate (Windows)
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file:

```env
APP_NAME=TaskTrackr
PORT=8000
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/tasktrackr
```

### 5. Start PostgreSQL via Docker

```bash
docker compose up -d
```

### 6. Initialize the Database

```bash
python -m app.db.init_db
```

### 7. Run the FastAPI Server

```bash
uvicorn app.main:app --reload
```

📍 Navigate to [http://localhost:8000/docs](http://localhost:8000/docs) to explore the API.

---

## 🔌 API Endpoints

| Method | Endpoint      | Description             |
| ------ | ------------- | ----------------------- |
| GET    | `/health`     | API status check        |
| GET    | `/tasks/`     | Retrieve all tasks      |
| POST   | `/tasks/`     | Create a new task       |
| GET    | `/tasks/{id}` | Get a task by ID        |
| PUT    | `/tasks/{id}` | Update an existing task |
| DELETE | `/tasks/{id}` | Delete a task by ID     |

---

## 🏁 Project Status

✅ Functional CRUD API
✅ Connected to real PostgreSQL DB
✅ CI/CD integration with GitHub Actions
✅ Cloud deployment (Render or Fly.io)

---

## 👤 Author

**John Carl Abucay**
📬 [abukiks.x@gmail.com](mailto:abukiks.x@gmail.com)
🔗 [LinkedIn](https://www.linkedin.com/in/abukiks)
📸 [Instagram](https://www.instagram.com/abukiks)

---

## 🌟 Learning Goals

* Master the 12-Factor App design
* Learn to dockerize and deploy modern Python apps
* Practice clean architecture and configuration management
* Implement CI/CD pipelines

---

> Made with ❤️ and Python — by John Carl Abucay
