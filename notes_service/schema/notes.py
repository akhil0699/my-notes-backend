"""Notes Service Schema module"""

from fastapi import Form
from pydantic import BaseModel


class CourseBase(BaseModel):
    course_name: str


class CourseCreateSchema(CourseBase):
    @classmethod
    def as_form(cls, course_name: str = Form(...)):
        return cls(
            course_name=course_name,
        )


class CourseSchema(CourseBase):
    id: int
    course_image: str | None = None


class SubjectBase(BaseModel):
    subject_name: str
    course_id: int


class SubjectCreateSchema(SubjectBase):
    @classmethod
    def as_form(cls, subject_name: str = Form(...), course_id: int = Form(...)):
        return cls(
            subject_name=subject_name,
            course_id=course_id,
        )


class SubjectSchema(SubjectBase):
    id: int
    subject_image: str | None = None


class ContentBaseSchema(BaseModel):
    content_title: str
    content_text: str | None = None
    subject_id: int


class ContentCreateSchema(ContentBaseSchema):
    @classmethod
    def as_form(
        cls,
        content_title: str = Form(...),
        content_text: str | None = Form(None),
        subject_id: int = Form(...),
    ):
        return cls(
            content_title=content_title,
            content_text=content_text,
            subject_id=subject_id,
        )


class ContentSchema(ContentBaseSchema):
    id: int
    content_pdf: str | None = None
    content_image: str | None = None
