#!/usr/bin/python
""" class to handle the ameneties"""
import models
from models.base_model import BaseModel, Base
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class Amenity(BaseModel, Base):
    """Amenity models class """
    if models.storage_t == 'db':
        name = Column(String(128), nullable=False)
        __tablename__ = 'amenities'
    else:
        name = ""

    def __init__(self, *args, **kwargs):
        """initializes the class"""
        super().__init__(*args, **kwargs)
