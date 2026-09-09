# Migrations (Alembic)

Real Alembic migrations, wired to the app's `Settings.database_url` and
`Base.metadata` (`env.py`). Batch mode is on, so the ALTERs are SQLite-safe and
the same revisions apply to Azure SQL.

```bash
pip install alembic

# apply everything (fresh DB or upgrade)
alembic upgrade head

# after changing database/models.py
alembic revision --autogenerate -m "describe the change"
alembic upgrade head

# roll back one step
alembic downgrade -1
```

`versions/bb0db45cc726_*.py` is the initial schema: `drones`, `telemetry`,
`incidents`, `response_plans`, `alerts` (+ their indexes).

For the quick local demo, `backend.core.db.init_db()` (`create_all`) also builds
the schema in one step — Alembic is the path for real deployments and for any
schema change after the first.
