from datetime import datetime

from sqlalchemy import String, Text, ForeignKey, DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.sql.functions import func
from sqlalchemy.sql.expression import false


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50), unique=True)
    password: Mapped[str] = mapped_column(String(150))
    email: Mapped[str] = mapped_column(String(150), unique=True)
    is_admin: Mapped[bool] = mapped_column(server_default=false())

    # SQLAlchemy relationships
    notes = relationship("Note", back_populates="author")

    def __str__(self):
        return self.username


class Note(Base):
    __tablename__ = "notes"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(150))
    content: Mapped[str] = mapped_column(Text)
    author_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    # SQLAlchemy relationships
    author: Mapped["User"] = relationship("User", back_populates="notes")
    tags = relationship("Tag", secondary="notes_tags", back_populates="notes")

    def __str__(self):
        return f"Note: {self.title}"


class NoteTag(Base):
    __tablename__ = "notes_tags"
    id: Mapped[int] = mapped_column(primary_key=True)
    note_id: Mapped[int] = mapped_column(ForeignKey("notes.id"))
    tag_id: Mapped[int] = mapped_column(ForeignKey("tags.id"))


class Tag(Base):
    __tablename__ = "tags"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=True)
    description: Mapped[str] = mapped_column(String(255))

    # SQLAlchemy relationships
    notes = relationship("Note", secondary="notes_tags", back_populates="tags")
