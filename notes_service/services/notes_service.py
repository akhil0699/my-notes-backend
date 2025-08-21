"""System Settings Service Module"""

from typing import Any, Dict, List, Union
from notes_service.errors.notes_errors import NotesDBException, NotesException
from notes_service.schema.notes import (
    SubjectSchema,
    CourseSchema,
    ContentSchema,
    ContentCreateSchema,
    SubjectCreateSchema,
    CourseCreateSchema,
)
from notes_service.config.logging import logger
from notes_service.repositories.notes_repository import NotesRepository


class NotesService:
    """Notes Service Class"""

    def __init__(self, repository: NotesRepository) -> None:
        self.repository = repository

    async def save(
        self,
        item: Union[ContentCreateSchema, SubjectCreateSchema, CourseCreateSchema],
    ) -> Union[ContentSchema, SubjectSchema, CourseSchema]:
        try:
            logger.info("Saving item")
            response = await self.repository.save(item=item)
            logger.info("Item saved successfully")
            return response
        except NotesDBException as exc:
            raise NotesException(
                message=exc.message, status_code=exc.status_code, details=exc.details
            )

    async def update(
        self,
        item_id: int,
        item: Union[ContentSchema, SubjectSchema, CourseSchema],
    ) -> Union[ContentSchema, SubjectSchema, CourseSchema]:
        try:
            logger.info("Updating item")
            response = await self.repository.update(item=item, item_id=item_id)
            logger.info("Item updated successfully")
            return response
        except NotesDBException as exc:
            raise NotesException(
                message=exc.message, status_code=exc.status_code, details=exc.details
            )

    async def delete(
        self,
        item_id: int,
    ) -> None:
        try:
            logger.info("Deleting item")
            await self.repository.delete(item_id=item_id)
            logger.info("Item deleted successfully")
        except NotesDBException as exc:
            raise NotesException(
                message=exc.message, status_code=exc.status_code, details=exc.details
            )

    async def get(
        self, item_id: str
    ) -> Union[ContentSchema, SubjectSchema, CourseSchema]:
        try:
            logger.info("Retrieving item with ID %s", item_id)
            response = await self.repository.get(item_id=item_id)
            logger.info("Item retrieved successfully")
            return response
        except NotesDBException as exc:
            raise NotesException(
                message=exc.message, status_code=exc.status_code, details=exc.details
            )

    async def get_by_filter(
        self, filters: Dict[str, Any]
    ) -> List[Union[ContentSchema, SubjectSchema, CourseSchema]]:
        try:
            logger.info("Retrieving items with filters %s", filters)
            response = await self.repository.get_by_filters(filters=filters)
            logger.info("Items retrieved successfully")
            return response
        except NotesDBException as exc:
            raise NotesException(
                message=exc.message, status_code=exc.status_code, details=exc.details
            )
