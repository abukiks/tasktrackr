# 📝 TaskTrackr

A simple task-tracking API built with **FastAPI**, containerized with **Docker**, CI/CD-ready via **GitHub Actions**, and deployed to **Render**.  
Follows the [12-Factor App Methodology](https://12factor.net/) + DevOps best practices.

---

## 🚀 Live Demo

🌐 https://tasktrackr.onrender.com  
🔎 Swagger Docs: `/docs`  
✅ Healthcheck: `/health`

---

## 📦 Tech Stack

- **Python 3.11**
- **FastAPI** – lightweight web API framework
- **SQLite / PostgreSQL** – local & production DB
- **Docker** – containerized for portability
- **GitHub Actions** – CI/CD pipeline
- **Render** – cloud deployment

---

## 📐 File Structure

```

tasktrackr/
├── app/
│   ├── main.py          # FastAPI app
│   ├── models.py        # SQLAlchemy models
│   ├── database.py      # DB connection logic
│   ├── config.py        # .env loader via python-dotenv
│   └── admin.py         # CLI for admin tasks
├── .env.dev             # Dev environment config
├── .env.prod            # Production config sample
├── requirements.txt     # Python dependencies
├── Dockerfile           # Container build
├── .dockerignore
├── .gitignore
├── .github/workflows/ci.yml  # CI/CD pipeline
├── tests/               # Test files
│   └── test\_dummy.py
└── README.md

````

---

## 🧪 Running Locally

```bash
# 1. Clone
git clone https://github.com/YOUR_USERNAME/tasktrackr.git && cd tasktrackr

# 2. Setup virtualenv
python3 -m venv .venv && source .venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the app
uvicorn app.main:app --reload

# 5. Use the API at: http://localhost:8000/docs
````

---

## 🐳 Docker

```bash
# Build image
docker build -t tasktrackr .

# Run container
docker run -d -p 8000:8000 --env-file .env.dev tasktrackr
```

---

## ✅ 12-Factor App Checklist

| #  | Factor              | Implemented                          |
| -- | ------------------- | ------------------------------------ |
| 1  | Codebase            | ✅ GitHub repo                        |
| 2  | Dependencies        | ✅ `requirements.txt`                 |
| 3  | Config              | ✅ `.env`, `python-dotenv`            |
| 4  | Backing Services    | ✅ SQLite / PostgreSQL                |
| 5  | Build, Release, Run | ✅ Dockerfile                         |
| 6  | Processes           | ✅ `uvicorn` single stateless process |
| 7  | Port Binding        | ✅ `EXPOSE 8000` + FastAPI            |
| 8  | Concurrency         | ✅ Ready for Gunicorn/Uvicorn workers |
| 9  | Disposability       | ✅ Instant restart via Docker/Render  |
| 10 | Dev/Prod Parity     | ✅ `.env.dev` vs `.env.prod`          |
| 11 | Logs                | ✅ STDOUT logging                     |
| 12 | Admin Processes     | ✅ `admin.py` CLI                     |

---

## 📮 Contact

Built with ♥ by [John Carl Abucay](mailto:abukiks.x@gmail.com)

[LinkedIn](https://www.linkedin.com/in/your-link) • [GitHub](https://github.com/YOUR_USERNAME)

---

## 🏁 Final Words

This project showcases **DevOps skills**, **Python best practices**, and **12-Factor discipline** — deployable, observable, and extensible.
