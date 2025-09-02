from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

try:  # Allow importing when executed as a script
    from .database import Base
except ImportError:  # pragma: no cover - for script execution
    from database import Base  # type: ignore


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)

    packages = relationship("Package", back_populates="owner")


class Package(Base):
    __tablename__ = "packages"

    id = Column(Integer, primary_key=True, index=True)
    description = Column(String, index=True, nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="packages")
