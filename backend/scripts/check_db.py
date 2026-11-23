from sqlalchemy import create_engine, text

from app.core.config import get_settings

settings = get_settings()

targets = {
    "dev": settings.database_url,
    "test": settings.test_database_url,
}

for name, url in targets.items():
    engine = create_engine(url)
    with engine.connect() as conn:
        db, user = conn.execute(text("SELECT current_database(), current_user")).one()
        print(f"[{name}] database={db}  user={user}")
    engine.dispose()