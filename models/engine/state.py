#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel
from models.city import City
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

class State(BaseModel):
    """ State class """
    name = Column(String(128), nullable=False)
    cities = relationship('City', backref='state',
                              cascade='all, delete, delete-orphan')
    @property
    def cities(self):
        '''returns the list of City instances
        '''
        from models import storage
        related_cities = []
        cities = storage.all(City)
        for city in cities.values():
            if city.state_id == self.id:
                related_cities.append(city)
        return related_cities