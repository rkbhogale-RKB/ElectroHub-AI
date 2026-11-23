from app.database.base import Base
import app.models  # noqa: F401  (registers all models)

for name, table in Base.metadata.tables.items():
    print(name, "->", [c.name for c in table.columns])