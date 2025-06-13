from sqlalchemy import Table, Column, Integer, String, Boolean
from app.database import metadata

tasks = Table(
    "tasks",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("title", String, nullable=False),
    Column("completed", Boolean, default=False),
)

