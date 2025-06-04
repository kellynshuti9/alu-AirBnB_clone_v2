#!/usr/bin/python3
"""Database storage engine using SQLAlchemy"""

from os import getenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import Base
from models.state import State
from models.city import City
from models.user import User
from models.place import Place
from models.review import Review
from models.amenity import Amenity


class DBStorage:
    """Handles storage of models using a MySQL database via SQLAlchemy"""
    __engine = None
    __session = None

    def __init__(self):
        """Initializes engine and drops all tables if in test environment"""
        user = getenv("HBNB_MYSQL_USER")
        passwd = getenv("HBNB_MYSQL_PWD")
        db = getenv("HBNB_MYSQL_DB")
        host = getenv("HBNB_MYSQL_HOST")
        env = getenv("HBNB_ENV")

        self.__engine = create_engine(
            f'mysql+mysqldb://{user}:{passwd}@{host}/{db}',
            pool_pre_ping=True
        )

        if env == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Query all objects or all objects of a class"""
        obj_dict = {}
        classes = [State, City, User, Place, Review, Amenity]

        if cls:
            if isinstance(cls, str):
                cls = eval(cls)
            objs = self.__session.query(cls).all()
            for obj in objs:
                key = f"{type(obj).__name__}.{obj.id}"
                obj_dict[key] = obj
        else:
            for model in classes:
                for obj in self.__session.query(model).all():
                    key = f"{type(obj).__name__}.{obj.id}"
                    obj_dict[key] = obj

        return obj_dict

    def new(self, obj):
        """Adds an object to the current session"""
        self.__session.add(obj)

    def save(self):
        """Commits all changes to the current session"""
        self.__session.commit()

    def delete(self, obj=None):
        """Deletes obj from the session"""
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """Creates all tables and initializes the session"""
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session()

    def close(self):
        """Closes the current session"""
        self.__session.close()
