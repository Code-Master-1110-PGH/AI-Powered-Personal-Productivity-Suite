"""
Generic Base Repository Module.

Implements the Repository Pattern, decoupling the domain and business logic
from direct ORM/SQL operations and standardizing CRUD behaviors.
"""

from typing import Generic, TypeVar, Type, Optional, List, Any, Dict, Union
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.core.database import Base

ModelType = TypeVar("ModelType", bound=Base)


class BaseRepository(Generic[ModelType]):
    """
    Base Repository class with default methods for Create, Read, Update, Delete (CRUD).
    """

    def __init__(self, model: Type[ModelType], db: Session):
        """
        Instantiate repository with the model type and database session.

        :param model: The SQLAlchemy ORM class.
        :param db: An active SQLAlchemy Session.
        """
        self.model = model
        self.db = db

    def get_by_id(self, id: int) -> Optional[ModelType]:
        """Fetch a single record by its primary key ID."""
        return self.db.query(self.model).filter(self.model.id == id).first()

    def get_multi(self, skip: int = 0, limit: int = 100) -> List[ModelType]:
        """Retrieve paginated records."""
        return self.db.query(self.model).offset(skip).limit(limit).all()

    def create(self, obj_in: Union[BaseModel, Dict[str, Any]]) -> ModelType:
        """Insert and commit a new record."""
        if isinstance(obj_in, dict):
            create_data = obj_in
        else:
            create_data = obj_in.model_dump()

        db_obj = self.model(**create_data)
        self.db.add(db_obj)
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj

    def update(
        self, db_obj: ModelType, obj_in: Union[BaseModel, Dict[str, Any]]
    ) -> ModelType:
        """Update an existing record with new attributes."""
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            if hasattr(db_obj, field):
                setattr(db_obj, field, value)

        self.db.add(db_obj)
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj

    def delete(self, id: int) -> Optional[ModelType]:
        """Delete a record by primary key."""
        obj = self.get_by_id(id)
        if obj:
            self.db.delete(obj)
            self.db.commit()
        return obj

