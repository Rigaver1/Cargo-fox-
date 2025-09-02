"""Initialize the database and populate it with test data."""
from sqlalchemy import text

# Support running as a script or as part of a package
if __name__ == "__main__" and __package__ is None:  # pragma: no cover - runtime import fix
    import os
    import sys
    sys.path.append(os.path.dirname(__file__))
    from database import Base, engine, get_db  # type: ignore
    from models import Package, User  # type: ignore
else:
    from .database import Base, engine, get_db
    from .models import Package, User


def init_db() -> None:
    """Create tables and insert a small set of test data."""
    Base.metadata.create_all(bind=engine)

    db_gen = get_db()
    db = next(db_gen)
    try:
        if not db.query(User).first():
            user = User(name="Alice", email="alice@example.com")
            package = Package(description="Sample package", owner=user)
            db.add(user)
            db.add(package)
            db.commit()
            print("Inserted test data")
    finally:
        db_gen.close()


def test_connection() -> None:
    """Verify that a simple statement can be executed."""
    db_gen = get_db()
    db = next(db_gen)
    try:
        db.execute(text("SELECT 1"))
        print("Connection OK")
    finally:
        db_gen.close()


if __name__ == "__main__":
    init_db()
    test_connection()
