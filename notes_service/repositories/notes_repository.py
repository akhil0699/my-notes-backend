"""Notes Repository Module"""

from typing import Any, Dict, List, Type, TypeVar, Union
from notes_service.config.settings import AppConfig
from sqlalchemy.orm import Session
from notes_service.database.models.notes import Content, Course, Subject
from notes_service.errors.notes_errors import NotesDBException
from notes_service.schema.notes import (
    SubjectSchema,
    CourseSchema,
    ContentSchema,
    ContentCreateSchema,
    SubjectCreateSchema,
    CourseCreateSchema,
)
from pydantic import BaseModel
from notes_service.config.logging import logger
from sqlalchemy.exc import SQLAlchemyError, NoResultFound

T = TypeVar("T", bound=BaseModel)


SCHEMA_TO_MODEL_MAP = {
    CourseSchema: Course,
    SubjectSchema: Subject,
    ContentSchema: Content,
}


class NotesRepository:
    """Concrete implementation of IRepository"""

    def __init__(
        self,
        app_config: AppConfig,
        session: Session,
        schema_class: Type[T],
    ) -> None:
        self.app_config = app_config
        self.session = session
        self.schema_class = schema_class

    async def get(
        self, item_id: str
    ) -> Union[CourseSchema, SubjectSchema, ContentSchema]:
        try:
            item: Union[Course, Subject, Content] = self.session.query(
                SCHEMA_TO_MODEL_MAP[self.schema_class]
            ).get(item_id)
            logger.info("Retrieved item with ID %s", item_id)
            return self.schema_class(**item.__dict__)
        except NoResultFound as e:
            logger.error("Error while reading the item: %s", str(e))
            raise NotesDBException(
                message="Error while reading the item", status_code=400, details=str(e)
            )

    async def save(
        self, item: Union[ContentCreateSchema, SubjectCreateSchema, CourseCreateSchema]
    ) -> Union[ContentSchema, SubjectSchema, CourseSchema]:
        try:
            model = SCHEMA_TO_MODEL_MAP[self.schema_class](**item.model_dump())
            self.session.add(model)
            self.session.commit()
            self.session.refresh(model)
            logger.info("Created item with ID %s", model.id)
            return self.schema_class(**model.__dict__)
        except SQLAlchemyError as e:
            logger.error("Error while creating the item: %s", str(e))
            raise NotesDBException(
                message="Error while creating the item", status_code=400, details=str(e)
            )

    async def update(
        self,
        item_id: str,
        item: Union[ContentSchema, SubjectSchema, CourseSchema],
    ) -> Union[ContentSchema, SubjectSchema, CourseSchema]:
        try:
            existing_item = self.session.query(
                SCHEMA_TO_MODEL_MAP[self.schema_class]
            ).get(item_id)
            if not existing_item:
                logger.error("Item with ID %s not found", item_id)
                raise NotesDBException(
                    message="Item not found",
                    status_code=404,
                    details=f"Item with ID {item_id} not found",
                )
            update_data = item.model_dump(exclude_unset=True)
            for key, value in update_data.items():
                if key == "id":
                    continue  # Don't update the primary key
                setattr(existing_item, key, value)
            self.session.commit()
            self.session.refresh(existing_item)
            logger.info("Updated item with ID %s", item_id)
            return self.schema_class(**existing_item.__dict__)
        except SQLAlchemyError as e:
            logger.error("Error while updating the item: %s", str(e))
            raise NotesDBException(
                message="Error while updating the item", status_code=400, details=str(e)
            )

    async def delete(self, item_id: str) -> None:
        try:
            existing_item = self.session.query(
                SCHEMA_TO_MODEL_MAP[self.schema_class]
            ).get(item_id)
            if not existing_item:
                logger.error("Item with ID %s not found", item_id)
                raise NotesDBException(
                    message="Item not found",
                    status_code=404,
                    details=f"Item with ID {item_id} not found",
                )
            self.session.delete(existing_item)
            self.session.commit()
            logger.info("Deleted item with ID %s", item_id)
        except SQLAlchemyError as e:
            logger.error("Error while deleting the item: %s", str(e))
            raise NotesDBException(
                message="Error while deleting the item", status_code=400, details=str(e)
            )

    async def get_by_filters(
        self, filters: Dict[str, Any]
    ) -> List[Union[ContentSchema, SubjectSchema, CourseSchema]]:
        try:
            items = self.session.query(SCHEMA_TO_MODEL_MAP[self.schema_class]).all()
            logger.info("Retrieved items with filters %s", filters)
            return_items: List[Union[ContentSchema, SubjectSchema, CourseSchema]] = []
            if filters.items():
                for key, value in filters.items():
                    return_items.extend(
                        [
                            self.schema_class(**item.__dict__)
                            for item in items
                            if item.__dict__[key] == value
                        ]
                    )
                return return_items
            return [self.schema_class(**item.__dict__) for item in items]
        except NoResultFound as e:
            logger.error("Error while retrieving items: %s", str(e))
            raise NotesDBException(
                message="Error while retrieving items", status_code=400, details=str(e)
            )
