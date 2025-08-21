"""System Settings Endpoint Module"""

from typing import Any, Dict, List
from urllib.parse import urljoin
from fastapi import APIRouter, UploadFile, File, Depends, Query
from fastapi.responses import JSONResponse

from notes_service.config import constants
from notes_service.config.settings import app_config
from notes_service.errors.notes_errors import NotesException
from notes_service.repositories.notes_repository import NotesRepository
from notes_service.schema.notes import (
    CourseCreateSchema,
    SubjectCreateSchema,
    ContentCreateSchema,
    SubjectSchema,
    CourseSchema,
    ContentSchema,
)
from notes_service.services import notes_service
from fastapi import status
from notes_service.database.connection.db_connection import DatabaseConnection
from notes_service.services.file_service import FileService

router = APIRouter(prefix="/notes")


@router.post(
    "/course",
    response_model=None,
    tags=["Course"],
    status_code=status.HTTP_201_CREATED,
)
async def add_course(
    data: CourseCreateSchema = Depends(CourseCreateSchema.as_form),
    file: UploadFile | None = File(None, description="File to be uploaded"),
) -> None | JSONResponse:
    """API to add course"""
    # Initialize connection
    session = DatabaseConnection(
        database_url=app_config.DATABASE_URL
    ).get_db_connection()
    # Initialize repository
    repo = NotesRepository(
        app_config=app_config,
        session=session,
        schema_class=CourseSchema,
    )
    # Initialize service
    service: notes_service.NotesService = notes_service.NotesService(repository=repo)
    try:
        response = await service.save(data)
        # Initialize file
        file_service: FileService = FileService(
            constants.COURSE_FILE_UPLOAD_DIR_NAME, app_config=app_config
        )
        # Upload file if any
        if file:
            file_path: str = await file_service.save_file(file=file)
            # Update image path to database
            response.course_image = file_path
            await service.update(item=response, item_id=response.id)
    except NotesException as exc:
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "message": str(exc.message),
                "details": exc.details,
                "status_code": exc.status_code,
            },
        )


@router.get(
    "/course/{course_id}",
    response_model=CourseSchema,
    tags=["Course"],
    status_code=status.HTTP_200_OK,
)
async def get_course(course_id: str) -> CourseSchema | JSONResponse:
    """API to get a course by ID"""
    # Initialize connection
    session = DatabaseConnection(
        database_url=app_config.DATABASE_URL
    ).get_db_connection()
    # Initialize repository
    repo = NotesRepository(
        app_config=app_config,
        session=session,
        schema_class=CourseSchema,
    )
    # Initialize service
    service: notes_service.NotesService = notes_service.NotesService(repository=repo)
    try:
        response: CourseSchema = await service.get(item_id=course_id)
        response.course_image = (
            urljoin(app_config.APP_URL, response.course_image, allow_fragments=True)
            if response.course_image
            else None
        )
        return response
    except NotesException as exc:
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "message": str(exc.message),
                "details": exc.details,
                "status_code": exc.status_code,
            },
        )


@router.get(
    "/course",
    response_model=List[CourseSchema],
    tags=["Course"],
    status_code=status.HTTP_200_OK,
)
async def get_course_by_filter(
    course_name: str | None = Query(None),
) -> List[CourseSchema] | JSONResponse:
    """API to get a course by ID"""
    # Initialize connection
    session = DatabaseConnection(
        database_url=app_config.DATABASE_URL
    ).get_db_connection()
    # Initialize repository
    repo = NotesRepository(
        app_config=app_config,
        session=session,
        schema_class=CourseSchema,
    )
    # Initialize service
    service: notes_service.NotesService = notes_service.NotesService(repository=repo)
    try:
        filters: Dict[str, Any] = {}
        if course_name:
            filters["course_name"] = course_name
        response: List[CourseSchema] = await service.get_by_filter(filters=filters)
        response = [
            CourseSchema(
                **course.model_dump(exclude={"course_image"}),
                course_image=(
                    urljoin(
                        app_config.APP_URL, course.course_image, allow_fragments=True
                    )
                    if course.course_image
                    else None
                )
            )
            for course in response
        ]
        return response
    except NotesException as exc:
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "message": str(exc.message),
                "details": exc.details,
                "status_code": exc.status_code,
            },
        )


@router.delete(
    "/course/{course_id}",
    response_model=None,
    tags=["Course"],
    status_code=status.HTTP_200_OK,
)
async def delete_course(course_id: str) -> None | JSONResponse:
    """API to delete a course by ID"""
    # Initialize connection
    session = DatabaseConnection(
        database_url=app_config.DATABASE_URL
    ).get_db_connection()
    # Initialize repository
    repo = NotesRepository(
        app_config=app_config,
        session=session,
        schema_class=CourseSchema,
    )
    # Initialize service
    service: notes_service.NotesService = notes_service.NotesService(repository=repo)
    try:
        item: CourseSchema = await service.get(item_id=course_id)
        # Delete associated files
        file_service: FileService = FileService(
            constants.COURSE_FILE_UPLOAD_DIR_NAME, app_config=app_config
        )
        if item.course_image:
            file_service.delete_file(file_path=item.course_image)
        # Delete the item from the database
        await service.delete(item_id=course_id)
    except NotesException as exc:
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "message": str(exc.message),
                "details": exc.details,
                "status_code": exc.status_code,
            },
        )


@router.post(
    "/subject",
    response_model=None,
    tags=["Subject"],
    status_code=status.HTTP_201_CREATED,
)
async def add_subject(
    data: SubjectCreateSchema = Depends(SubjectCreateSchema.as_form),
    file: UploadFile | None = File(None, description="File to be uploaded"),
) -> None | JSONResponse:
    """API to add subject"""
    # Initialize connection
    session = DatabaseConnection(
        database_url=app_config.DATABASE_URL
    ).get_db_connection()
    # Initialize repository
    repo = NotesRepository(
        app_config=app_config,
        session=session,
        schema_class=SubjectSchema,
    )
    # Initialize service
    service: notes_service.NotesService = notes_service.NotesService(repository=repo)
    try:
        response = await service.save(data)
        # Initialize file
        file_service: FileService = FileService(
            constants.SUBJECT_FILE_UPLOAD_DIR_NAME, app_config=app_config
        )
        # Upload file if any
        if file:
            file_path: str = await file_service.save_file(file=file)
            # Update image path to database
            response.subject_image = file_path
            await service.update(item=response, item_id=response.id)
    except NotesException as exc:
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "message": str(exc.message),
                "details": exc.details,
                "status_code": exc.status_code,
            },
        )


@router.get(
    "/subject/{subject_id}",
    response_model=SubjectSchema,
    tags=["Subject"],
    status_code=status.HTTP_200_OK,
)
async def get_subject(subject_id: str) -> SubjectSchema | JSONResponse:
    """API to get a subject by ID"""
    # Initialize connection
    session = DatabaseConnection(
        database_url=app_config.DATABASE_URL
    ).get_db_connection()
    # Initialize repository
    repo = NotesRepository(
        app_config=app_config,
        session=session,
        schema_class=SubjectSchema,
    )
    # Initialize service
    service: notes_service.NotesService = notes_service.NotesService(repository=repo)
    try:
        response: SubjectSchema = await service.get(item_id=subject_id)
        response.subject_image = (
            urljoin(app_config.APP_URL, response.subject_image, allow_fragments=True)
            if response.subject_image
            else None
        )
        return response
    except NotesException as exc:
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "message": str(exc.message),
                "details": exc.details,
                "status_code": exc.status_code,
            },
        )


@router.get(
    "/subject",
    response_model=List[SubjectSchema],
    tags=["Subject"],
    status_code=status.HTTP_200_OK,
)
async def get_subjects(
    subject_name: str | None = Query(None),
    course_id: int | None = Query(None),
) -> List[SubjectSchema] | JSONResponse:
    """API to get all subjects"""
    # Initialize connection
    session = DatabaseConnection(
        database_url=app_config.DATABASE_URL
    ).get_db_connection()
    # Initialize repository
    repo = NotesRepository(
        app_config=app_config,
        session=session,
        schema_class=SubjectSchema,
    )
    # Initialize service
    service: notes_service.NotesService = notes_service.NotesService(repository=repo)
    try:
        filters: Dict[str, Any] = {}
        if subject_name:
            filters["subject_name"] = subject_name
        if course_id:
            filters["course_id"] = course_id
        response: List[SubjectSchema] = await service.get_by_filter(filters=filters)
        response = [
            SubjectSchema(
                **subject.model_dump(exclude={"subject_image"}),
                subject_image=(
                    urljoin(
                        app_config.APP_URL, subject.subject_image, allow_fragments=True
                    )
                    if subject.subject_image
                    else None
                )
            )
            for subject in response
        ]
        return response
    except NotesException as exc:
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "message": str(exc.message),
                "details": exc.details,
                "status_code": exc.status_code,
            },
        )


@router.delete(
    "/subject/{subject_id}",
    response_model=None,
    tags=["Subject"],
    status_code=status.HTTP_200_OK,
)
async def delete_subject(subject_id: str) -> None | JSONResponse:
    """API to delete a subject by ID"""
    # Initialize connection
    session = DatabaseConnection(
        database_url=app_config.DATABASE_URL
    ).get_db_connection()
    # Initialize repository
    repo = NotesRepository(
        app_config=app_config,
        session=session,
        schema_class=SubjectSchema,
    )
    # Initialize service
    service: notes_service.NotesService = notes_service.NotesService(repository=repo)
    try:
        item: SubjectSchema = await service.get(item_id=subject_id)
        # Delete files
        file_service: FileService = FileService(
            constants.SUBJECT_FILE_UPLOAD_DIR_NAME, app_config=app_config
        )
        if item.subject_image:
            file_service.delete_file(file_path=item.subject_image)
        await service.delete(item_id=subject_id)
    except NotesException as exc:
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "message": str(exc.message),
                "details": exc.details,
                "status_code": exc.status_code,
            },
        )


@router.post(
    "/content",
    response_model=None,
    tags=["Content"],
    status_code=status.HTTP_201_CREATED,
)
async def add_content(
    data: ContentCreateSchema = Depends(ContentCreateSchema.as_form),
    content_pdf: UploadFile | None = File(None, description="Content PDF file"),
    content_image: UploadFile | None = File(None, description="Content image file"),
) -> None | JSONResponse:
    """API to add content"""
    # Initialize connection
    session = DatabaseConnection(
        database_url=app_config.DATABASE_URL
    ).get_db_connection()
    # Initialize repository
    repo = NotesRepository(
        app_config=app_config,
        session=session,
        schema_class=ContentSchema,
    )
    # Initialize service
    service: notes_service.NotesService = notes_service.NotesService(repository=repo)
    try:
        response = await service.save(data)
        # Initialize file
        file_service: FileService = FileService(
            constants.CONTENT_FILE_UPLOAD_DIR_NAME, app_config=app_config
        )
        # Upload file if any
        if content_image or content_pdf:
            if content_image:
                file_path: str = await file_service.save_file(file=content_image)
                # Update image path to database
                response.content_image = file_path
            if content_pdf:
                file_path: str = await file_service.save_file(file=content_pdf)
                # Update PDF path to database
                response.content_pdf = file_path
            await service.update(item=response, item_id=response.id)
    except NotesException as exc:
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "message": str(exc.message),
                "details": exc.details,
                "status_code": exc.status_code,
            },
        )


@router.get(
    "/content/{content_id}",
    response_model=ContentSchema,
    tags=["Content"],
    status_code=status.HTTP_200_OK,
)
async def get_content(content_id: str) -> ContentSchema | JSONResponse:
    """API to get a content by ID"""
    # Initialize connection
    session = DatabaseConnection(
        database_url=app_config.DATABASE_URL
    ).get_db_connection()
    # Initialize repository
    repo = NotesRepository(
        app_config=app_config,
        session=session,
        schema_class=ContentSchema,
    )
    # Initialize service
    service: notes_service.NotesService = notes_service.NotesService(repository=repo)
    try:
        response: ContentSchema = await service.get(item_id=content_id)
        response.content_image = (
            urljoin(app_config.APP_URL, response.content_image, allow_fragments=True)
            if response.content_image
            else None
        )
        response.content_pdf = (
            urljoin(app_config.APP_URL, response.content_pdf, allow_fragments=True)
            if response.content_pdf
            else None
        )
        return response
    except NotesException as exc:
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "message": str(exc.message),
                "details": exc.details,
                "status_code": exc.status_code,
            },
        )


@router.get(
    "/content",
    response_model=List[ContentSchema],
    tags=["Content"],
    status_code=status.HTTP_200_OK,
)
async def get_contents(
    content_title: str | None = Query(None),
    subject_id: int | None = Query(None),
) -> List[ContentSchema] | JSONResponse:
    """API to get a content by title"""
    # Initialize connection
    session = DatabaseConnection(
        database_url=app_config.DATABASE_URL
    ).get_db_connection()
    # Initialize repository
    repo = NotesRepository(
        app_config=app_config,
        session=session,
        schema_class=ContentSchema,
    )
    # Initialize service
    service: notes_service.NotesService = notes_service.NotesService(repository=repo)
    try:
        filters: Dict[str, Any] = {}
        if content_title:
            filters["content_title"] = content_title
        if subject_id:
            filters["subject_id"] = subject_id
        response: List[ContentSchema] = await service.get_by_filter(filters=filters)
        response = [
            ContentSchema(
                **content.model_dump(exclude={"content_image", "content_pdf"}),
                content_image=(
                    urljoin(
                        app_config.APP_URL, content.content_image, allow_fragments=True
                    )
                    if content.content_image
                    else None
                ),
                content_pdf=(
                    urljoin(
                        app_config.APP_URL, content.content_pdf, allow_fragments=True
                    )
                    if content.content_pdf
                    else None
                )
            )
            for content in response
        ]
        return response
    except NotesException as exc:
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "message": str(exc.message),
                "details": exc.details,
                "status_code": exc.status_code,
            },
        )


@router.delete(
    "/content/{content_id}",
    response_model=None,
    tags=["Content"],
    status_code=status.HTTP_200_OK,
)
async def delete_content(content_id: str) -> None | JSONResponse:
    """API to delete a content by ID"""
    # Initialize connection
    session = DatabaseConnection(
        database_url=app_config.DATABASE_URL
    ).get_db_connection()
    # Initialize repository
    repo = NotesRepository(
        app_config=app_config,
        session=session,
        schema_class=ContentSchema,
    )
    # Initialize service
    service: notes_service.NotesService = notes_service.NotesService(repository=repo)
    try:
        item: ContentSchema = await service.get(item_id=content_id)
        # Delete files
        file_service: FileService = FileService(
            constants.SUBJECT_FILE_UPLOAD_DIR_NAME, app_config=app_config
        )
        if item.content_image:
            file_service.delete_file(file_path=item.content_image)
        if item.content_pdf:
            file_service.delete_file(file_path=item.content_pdf)
        await service.delete(item_id=content_id)
    except NotesException as exc:
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "message": str(exc.message),
                "details": exc.details,
                "status_code": exc.status_code,
            },
        )


@router.put(
    "/content/{content_id}",
    response_model=None,
    tags=["Content"],
    status_code=status.HTTP_200_OK,
)
async def update_content(
    content_id: str,
    data: ContentCreateSchema = Depends(ContentCreateSchema.as_form),
    content_pdf: UploadFile | None = File(None, description="Content PDF file"),
    content_image: UploadFile | None = File(None, description="Content image file"),
) -> None | JSONResponse:
    """API to update content"""
    # Initialize connection
    session = DatabaseConnection(
        database_url=app_config.DATABASE_URL
    ).get_db_connection()
    # Initialize repository
    repo = NotesRepository(
        app_config=app_config,
        session=session,
        schema_class=ContentSchema,
    )
    # Initialize service
    service: notes_service.NotesService = notes_service.NotesService(repository=repo)
    try:
        response = await service.update(item=data, item_id=content_id)
        # Initialize file
        file_service: FileService = FileService(
            constants.CONTENT_FILE_UPLOAD_DIR_NAME, app_config=app_config
        )
        # Upload file if any
        if content_image or content_pdf:
            if content_image:
                file_path: str = await file_service.save_file(file=content_image)
                # Update image path to database
                response.content_image = file_path
            if content_pdf:
                file_path: str = await file_service.save_file(file=content_pdf)
                # Update PDF path to database
                response.content_pdf = file_path
            await service.update(item=response, item_id=response.id)
    except NotesException as exc:
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "message": str(exc.message),
                "details": exc.details,
                "status_code": exc.status_code,
            },
        )
