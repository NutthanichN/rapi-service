from sqlalchemy import Table, Column, Integer, String
from rapi_site.database import Base


class Restaurant(Base):
    # TODO: complete all columns
    __tablename__ = 'restaurant'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)

    def __init__(self, name=None):
        self.name = name


class District(Base):
    __tablename__ = 'district'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)

    def __init__(self, name=None):
        self.name = name


class Cuisine(Base):
    __tablename__ = 'cuisine'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)

    def __init__(self, name=None):
        self.name = name
