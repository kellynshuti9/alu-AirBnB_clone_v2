#!/usr/bin/python3
"""This is the state class"""

from models.base_model import BaseModel, Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String
import models
import shlex


class State(BaseModel, Base):
    """This is the class for State
    Attributes:
        name (str): input name of the state
        cities (relationship): SQLAlchemy relationship to City objects
    """
    __tablename__ = "states"
    name = Column(String(128), nullable=False)

    # SQLAlchemy relationship: this will be used with DBStorage
    cities = relationship(
        "City",
        cascade='all, delete, delete-orphan',
        backref="state"
    )

    @property
    def cities_list(self):
        """Returns the list of City instances related to this State
        when using FileStorage
        """
        all_objs = models.storage.all()
        return [
            obj for obj in all_objs.values()
            if obj.__class__.__name__ == 'City' and obj.state_id == self.id
        ]
