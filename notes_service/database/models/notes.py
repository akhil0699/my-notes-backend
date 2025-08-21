"""This module defines the database models for the notes service."""

from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, Integer, String, ForeignKey, Text

Base = declarative_base()


class Course(Base):
    __tablename__ = "course"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    course_name = Column(String, nullable=False)
    course_image = Column(String, nullable=True)

    # One-to-many relationship → A course has many subjects
    subjects = relationship(
        "Subject", back_populates="course", cascade="all, delete-orphan"
    )


class Subject(Base):
    __tablename__ = "subject"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    subject_name = Column(String, nullable=False)
    subject_image = Column(String, nullable=True)

    # Foreign key → Many subjects belong to one course
    course_id = Column(Integer, ForeignKey("course.id"), nullable=False)

    # Back-reference
    course = relationship("Course", back_populates="subjects")

    # One-to-many relationship → A subject has many contents
    contents = relationship(
        "Content", back_populates="subject", cascade="all, delete-orphan"
    )


class Content(Base):
    __tablename__ = "content"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    content_title = Column(String, nullable=False)
    content_image = Column(String, nullable=True)
    content_text = Column(Text, nullable=True)
    content_pdf = Column(String, nullable=True)

    # Foreign key → Many contents belong to one subject
    subject_id = Column(Integer, ForeignKey("subject.id"), nullable=False)

    # Back-reference
    subject = relationship("Subject", back_populates="contents")
