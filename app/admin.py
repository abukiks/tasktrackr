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
