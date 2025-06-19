### ✅ 0️⃣ Step 0: Project Init

| Task                   | Details                                                                       |
| ---------------------- | ----------------------------------------------------------------------------- |
| **Create GitHub Repo** | Go to [github.com](https://github.com), create a new repo named `tasktrackr`. |
| **Clone Locally**      | Run: `git clone https://github.com/yourusername/tasktrackr.git`               |
| **Go to directory**    | Run: `cd tasktrackr`                                                          |

**Why?**
This satisfies [12-Factor App #1: *Codebase*](https://12factor.net/codebase) — "One codebase tracked in version control, many deploys."

---

### ✅ 1️⃣ Step 1: App Bootstrap

| Task                | Command/Action                                   |
| ------------------- | ------------------------------------------------ |
| Initialize project  | `mkdir tasktrackr && cd tasktrackr` (if not yet) |
| Create FastAPI app  | `mkdir app && touch app/main.py`                 |
| Minimal app content | Paste the following inside `app/main.py`:        |

```python
# app/main.py
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to TaskTrackr!"}
```

\| Add `.gitignore`      | Create `.gitignore` file:                         |

```gitignore
__pycache__/
*.pyc
.env*
tasks.db
*.sqlite3
.dockerignore
```

---

### ✅ 2️⃣ Step 2: Dependency Management

| Task                       | Command/Action                                                                                       |
| -------------------------- | ---------------------------------------------------------------------------------------------------- |
| Create virtual environment | `python3 -m venv .venv`                                                                              |
| Activate it                | <ul><li>Linux/macOS: `source .venv/bin/activate`</li><li>Windows: `.venv\Scripts\activate`</li></ul> |
| Install FastAPI & Uvicorn  | `pip install fastapi uvicorn[standard]`                                                              |
| Freeze dependencies        | `pip freeze > requirements.txt`                                                                      |

📄 `requirements.txt` will now look like this (example):

```
fastapi==0.111.0
uvicorn[standard]==0.29.0
```

---

🔎 **Why This Matters?**
This follows **12-Factor App Principle #2: Dependencies**

> Explicitly declare and isolate dependencies — no relying on global Python installs or untracked packages.

---

📁 Updated file structure:

```
tasktrackr/
├── app/
│   └── main.py
├── requirements.txt
├── .gitignore
```
---

### ✅ 3️⃣ Step 3: App Logic – Build `/tasks` Endpoint

#### 🧱 Goal: Add basic `/tasks` routes with in-memory storage

We'll use a Python list to simulate a database for now (we’ll add real DB later in Step 5).

---

#### 📄 `app/main.py` – Update it like this:

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()

# Define task model
class Task(BaseModel):
    id: int
    title: str
    completed: bool = False

# In-memory "DB"
tasks: List[Task] = []

@app.get("/")
def root():
    return {"message": "Welcome to TaskTrackr!"}

@app.get("/tasks", response_model=List[Task])
def get_tasks():
    return tasks

@app.post("/tasks", response_model=Task)
def create_task(task: Task):
    tasks.append(task)
    return task

@app.get("/tasks/{task_id}", response_model=Task)
def read_task(task_id: int):
    for task in tasks:
        if task.id == task_id:
            return task
    raise HTTPException(status_code=404, detail="Task not found")

@app.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: int, updated_task: Task):
    for idx, task in enumerate(tasks):
        if task.id == task_id:
            tasks[idx] = updated_task
            return updated_task
    raise HTTPException(status_code=404, detail="Task not found")

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    for idx, task in enumerate(tasks):
        if task.id == task_id:
            tasks.pop(idx)
            return {"message": "Task deleted"}
    raise HTTPException(status_code=404, detail="Task not found")
```

---

#### 🧪 Run the app

```bash
uvicorn app.main:app --reload
```

Visit:

* Swagger docs: [http://localhost:8000/docs](http://localhost:8000/docs)
* `/tasks` CRUD: create, get, update, delete

---

🔎 **Why This Matters?**
This sets the **Functionality foundation** before we wire in real services like the database (Step 5).
It also prepares the app for further DevOps integration (testing, pipelines, etc.).

---

### ✅ 4️⃣ Step 4: Config Management – `.env` + `python-dotenv`

---

#### 🧩 Goal: Use environment variables for config like database URL, secret keys, etc.

We'll prepare for real-world deployment by loading sensitive config from `.env`.

---

#### 📦 Install `python-dotenv`

```bash
pip install python-dotenv
pip freeze > requirements.txt  # update dependencies file
```

---

#### 📄 Create `.env.dev` file

```dotenv
APP_NAME=TaskTrackr
DEBUG=True
```

✅ Add this to `.gitignore` if you haven’t already:

```
.env*
```

---

#### 📄 Create `app/config.py`

```python
import os
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env

class Settings:
    APP_NAME: str = os.getenv("APP_NAME", "TaskTrackr")
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"

settings = Settings()
```

---

#### 📄 Use in `main.py`

Update the root route to return app name from settings:

```python
from .config import settings

@app.get("/")
def root():
    return {"message": f"Welcome to {settings.APP_NAME}!"}
```

---

🔎 **Why This Matters?**
This fulfills **12-Factor App #3: Config**

> Store config in the environment — not hardcoded in source.

---

📁 Updated file structure:

```
tasktrackr/
├── app/
│   ├── main.py
│   └── config.py
├── requirements.txt
├── .env.dev
├── .gitignore
```
---

### ✅ 5️⃣ Step 5: Backing Service – Add a Database

#### 🧩 Goal: Use **SQLite** locally and be ready for **PostgreSQL** in production.

We’ll integrate SQLAlchemy ORM to define our task model and handle DB operations.

---

### 🛠️ Install Dependencies

```bash
pip install sqlalchemy aiosqlite databases
pip freeze > requirements.txt
```

---

### 🧱 1. Create `app/database.py`

```python
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "sqlite:///./tasks.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
metadata = MetaData()
```

---

### 🧱 2. Create `app/models.py`

```python
from sqlalchemy import Column, Integer, String, Boolean
from .database import Base

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    completed = Column(Boolean, default=False)
```

---

### 🧱 3. Update `app/main.py`

```python
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from app import models, database
from app.config import settings

from pydantic import BaseModel
from typing import List

app = FastAPI()

# Create tables
models.Base.metadata.create_all(bind=database.engine)

# Dependency
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Pydantic schema
class TaskSchema(BaseModel):
    id: int
    title: str
    completed: bool = False

    class Config:
        orm_mode = True

@app.get("/")
def root():
    return {"message": f"Welcome to {settings.APP_NAME}!"}

@app.get("/tasks", response_model=List[TaskSchema])
def get_tasks(db: Session = Depends(get_db)):
    return db.query(models.Task).all()

@app.post("/tasks", response_model=TaskSchema)
def create_task(task: TaskSchema, db: Session = Depends(get_db)):
    db_task = models.Task(**task.dict())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

@app.get("/tasks/{task_id}", response_model=TaskSchema)
def read_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(models.Task).get(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@app.put("/tasks/{task_id}", response_model=TaskSchema)
def update_task(task_id: int, updated: TaskSchema, db: Session = Depends(get_db)):
    task = db.query(models.Task).get(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    task.title = updated.title
    task.completed = updated.completed
    db.commit()
    db.refresh(task)
    return task

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(models.Task).get(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(task)
    db.commit()
    return {"message": "Task deleted"}
```

---

🔎 **Why This Matters?**
This implements **12-Factor App #4: Backing Services**

> Treat backing services (like DBs) as attached resources — easily swappable per environment.

---

📁 Updated structure:

```
tasktrackr/
├── app/
│   ├── main.py
│   ├── config.py
│   ├── database.py
│   └── models.py
├── requirements.txt
├── tasks.db           # (auto-created by app, ignored by Git)
├── .env.dev
├── .gitignore
```
---

### ✅ 6️⃣ Step 6: Build & Run – Create a Dockerfile

#### 🧩 Goal: Containerize the app so it can run consistently anywhere — locally or in production.

---

### 📄 Create `Dockerfile` in the root:

```Dockerfile
# Base image
FROM python:3.11-slim

# Set environment vars
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set workdir
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY . .

# Expose port
EXPOSE 8000

# Run the app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

### 📄 Create `.dockerignore`

```dockerignore
__pycache__/
*.pyc
.env*
tasks.db
.venv/
```

---

### 🐳 Build & Run the Docker Container

```bash
# Build the image
docker build -t tasktrackr .

# Run the container
docker run -d -p 8000:8000 --name tasktrackr tasktrackr
```

* App should be accessible at: [http://localhost:8000](http://localhost:8000)

✅ You can also view Swagger docs at [http://localhost:8000/docs](http://localhost:8000/docs)

---

🔎 **Why This Matters?**
This covers **12-Factor App #5: Build, Release, Run**

> Strictly separate build, release, and run stages — Docker helps achieve this.

---

📁 File structure now includes:

```
tasktrackr/
├── Dockerfile
├── .dockerignore
...
```
---

### ✅ 7️⃣ Step 7: Dev/Prod Parity – Separate `.env.dev` and `.env.prod`

#### 🧩 Goal: Mirror development and production as closely as possible.

We'll prepare different environment config files and ensure they're respected in Docker too.

---

### 📄 `.env.dev` – Already created earlier

Let’s expand it for development:

```env
APP_NAME=TaskTrackr (Dev)
DEBUG=True
DATABASE_URL=sqlite:///./tasks.db
```

---

### 📄 `.env.prod` – For deployment

```env
APP_NAME=TaskTrackr
DEBUG=False
DATABASE_URL=postgresql://user:password@db:5432/tasktrackr
```

(You’ll configure real DB values later in deployment steps.)

---

### 📄 Update `config.py` to read DATABASE\_URL

```python
import os
from dotenv import load_dotenv

load_dotenv()  # Load from .env.* file

class Settings:
    APP_NAME: str = os.getenv("APP_NAME", "TaskTrackr")
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./tasks.db")

settings = Settings()
```

---

### 📄 Update `database.py` to use `settings.DATABASE_URL`

```python
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker, declarative_base
from .config import settings

DATABASE_URL = settings.DATABASE_URL

engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
metadata = MetaData()
```

---

### 🐳 Load `.env.dev` in Docker (optional for local dev)

Update `Dockerfile` to copy `.env.dev`:

```Dockerfile
COPY .env.dev .env
```

Or pass it during `docker run`:

```bash
docker run --env-file .env.dev -p 8000:8000 tasktrackr
```

---

🔎 **Why This Matters?**
This satisfies **12-Factor App #10: Dev/Prod Parity**

> Keep dev, staging, and production as similar as possible to avoid surprises at deploy time.

---

### ✅ 8️⃣ Step 8: Logs – Stream to STDOUT

#### 🧩 Goal: Output all logs to `stdout` — no log files.

This allows easy log collection in containers, CI, cloud platforms, and aligns with 12-Factor principles.

---

### 📄 Update `main.py` to configure logging

We’ll set logging manually to standard output using Python’s built-in `logging` module.

```python
import logging
from fastapi import FastAPI
from .config import settings

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

@app.on_event("startup")
def startup_event():
    logger.info("🚀 TaskTrackr is starting up...")

@app.get("/")
def root():
    logger.info("Root endpoint hit")
    return {"message": f"Welcome to {settings.APP_NAME}!"}
```

---

### 🐳 Run the app to see logs:

```bash
# Regular
uvicorn app.main:app --reload

# Docker
docker run --env-file .env.dev -p 8000:8000 tasktrackr
```

🎯 You should see logs printed like:

```bash
INFO:__main__:🚀 TaskTrackr is starting up...
INFO:__main__:Root endpoint hit
```

---

🔎 **Why This Matters?**
This fulfills **12-Factor App #11: Logs**

> Treat logs as event streams — never write to files. Instead, output to stdout/stderr.

---

### ✅ 9️⃣ Step 9: Admin Processes – Add a CLI Script

#### 🧩 Goal: Run one-off admin tasks (like DB migrations, task inserts) via standalone CLI — not part of the main app.

This is essential for maintenance, debugging, or ops scripts in production.

---

### 📄 Create `app/admin.py`

```python
import argparse
from app.database import SessionLocal
from app.models import Task

def create_sample_task(title: str):
    db = SessionLocal()
    new_task = Task(title=title, completed=False)
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    db.close()
    print(f"✅ Created Task: {new_task.title} (ID: {new_task.id})")

def list_tasks():
    db = SessionLocal()
    tasks = db.query(Task).all()
    for task in tasks:
        print(f"{task.id}: {task.title} - {'✅' if task.completed else '❌'}")
    db.close()

def main():
    parser = argparse.ArgumentParser(description="TaskTrackr Admin CLI")
    subparsers = parser.add_subparsers(dest="command")

    add_parser = subparsers.add_parser("add")
    add_parser.add_argument("title", help="Title of the new task")

    subparsers.add_parser("list")

    args = parser.parse_args()

    if args.command == "add":
        create_sample_task(args.title)
    elif args.command == "list":
        list_tasks()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
```

---

### 🧪 Run admin CLI:

```bash
# Add a task
python -m app.admin add "Document TaskTrackr project"

# List tasks
python -m app.admin list
```

💡 You can even run this inside Docker like:

```bash
docker exec -it tasktrackr python app/admin.py list
```

---

🔎 **Why This Matters?**
This satisfies **12-Factor App #12: Admin Processes**

> Run one-off admin tasks as first-class citizens (scripts, not daemons).

---

📁 Updated structure:

```
tasktrackr/
├── app/
│   └── admin.py  # ← New
```

Excellent! Let’s set up:

---

### ✅ 🔟 Step 10: CI/CD Setup with GitHub Actions

#### 🧩 Goal: Automate linting, testing, and Docker build on every push.

This is essential for quality, reliability, and DevOps best practices.

---

### 📁 Create GitHub Actions Workflow

#### 📄 `.github/workflows/ci.yml`

```yaml
name: CI Pipeline

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
      - name: 🔄 Checkout code
        uses: actions/checkout@v3

      - name: 🐍 Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: 📦 Install dependencies
        run: |
          python -m venv .venv
          source .venv/bin/activate
          pip install --upgrade pip
          pip install -r requirements.txt

      - name: ✅ Lint with flake8
        run: |
          pip install flake8
          flake8 app --count --select=E9,F63,F7,F82 --show-source --statistics

      - name: 🐳 Build Docker image
        run: |
          docker build -t tasktrackr .
```

---

### 🧪 Optional: Add basic tests (for future test stage)

Create `tests/test_dummy.py`:

```python
def test_dummy():
    assert 1 + 1 == 2
```

Update `ci.yml` with:

```yaml
      - name: 🧪 Run Tests
        run: |
          pip install pytest
          pytest tests
```

---

🔎 **Why This Matters?**
✅ Implements **CI (Continuous Integration)** and follows **DevOps best practices**:

* Ensures app is testable
* Checks lint/errors
* Builds the Docker image for production parity

---

📁 Structure now includes:

```
tasktrackr/
├── .github/
│   └── workflows/
│       └── ci.yml
├── tests/
│   └── test_dummy.py
```

✅ CI/CD is now active! Push to GitHub and see the Actions run automatically.
