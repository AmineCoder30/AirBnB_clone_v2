#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from models.city import City
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from os import getenv

storage_type = getenv("HBNB_TYPE_STORAGE")

class State(BaseModel, Base):
    """ State class"""
    __tablename__ = 'states'
    if storage_type == "db":
        name = Column(String(128), nullable=False, unique=True)
        cities = relationship('City', cascade="all,delete", backref="state")
    else:
        name = ""


        @property
        def cities(self):
            '''returns the list of City instances with
            '''
            from models import storage
            related_cities = []
            cities = storage.all(City)
            for city in cities.values():
                if city.state_id == self.id:
                    related_cities.append(city)
            return related_cities

