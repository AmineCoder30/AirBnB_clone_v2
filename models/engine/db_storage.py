#!/usr/bin/python3
"""This module defines a class to manage file storage for hbnb clone"""
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review
from models.base_model import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.exc import IntegrityError, OperationalError
from os import getenv


class DBStorage:
    """Class Docs"""

    __engine = None
    __session = None

    def __init__(self):
        """Function Docs"""
        db_user = getenv("HBNB_MYSQL_USER")
        db_host = getenv("HBNB_MYSQL_HOST")
        db_name = getenv("HBNB_MYSQL_DB")
        db_env = getenv("HBNB_ENV")
        db_pswd = getenv("HBNB_MYSQL_PWD")

        self.__engine = create_engine(
            f"mysql+mysqldb://{db_user}:{db_pswd}@{db_host}/{db_name}",
            pool_pre_ping=True,
        )

        if db_env == "test":
            Base.metadata.drop_all(self.__engine)

    def reload(self):
        """ reload method """
        Base.metadata.create_all(self.__engine)
        Session = scoped_session(
            sessionmaker(bind=self.__engine, expire_on_commit=False)
        )
        self.__session = Session()

    def all(self, cls=None):
        """query all classes or specific one"""
        result = {}
        classes = [User, Place, State,
                   City, Amenity, Review]
        if cls is not None:
            for obj in self.__session.query(cls).all():
                ClsNme = obj.__class__.__name__
                kyNm = ClsNme + "." + obj.id
                result[kyNm] = obj
        else:
            for classe in classes:
                for obj in self.__session.query(classe).all():
                    ClsNme = obj.__class__.__name__
                    kyNm = ClsNme + "." + obj.id
                    result[kyNm] = obj
        return result

    def new(self, obj):
        """add object"""
        if obj:
            self.__session.add(obj)

    def save(self):
        """commit all changes"""
        self.__session.commit()

    def delete(self, obj=None):
        """delete from the current"""
        if obj:
            self.__session.delete(obj)
