from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from rapi_site.database import Base


class Restaurant(Base):
    __tablename__ = 'restaurant'
    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    latitude = Column(String(10), nullable=False)
    longitude = Column(String(10), nullable=False)
    opening_hour = Column(String(15))
    wongnai_rating = Column(Float)
    tripadvisor_rating = Column(Float)
    address = Column(String(255))
    cuisine_id = Column(Integer, ForeignKey('cuisine.id', ondelete='CASCADE'))
    district_id = Column(Integer, ForeignKey('district.id', ondelete='CASCADE'))
    michelin_star = Column(Integer)

    def __repr__(self):
        return f"<Restaurant(name='{self.name}', lat='{self.latitude}', long='{self.longitude}', opening_hour='{self.opening_hour}', wongnai_rating='{self.wongnai_rating}', tripadvisor_rating='{self.tripadvisor_rating}, address='{self.address}, cuisine_id='{self.cuisine_id}, michelin_star ='{self.michelin_star }')>"


class District(Base):
    __tablename__ = 'district'
    id = Column(Integer, primary_key=True)
    name = Column(String(255))

    restaurant = relationship(
        'Restaurant',
        cascade='all, delete',
        passive_deletes=True
    )

    def __repr__(self):
        return f"<District(name='{self.name}')>"


class Cuisine(Base):
    __tablename__ = 'cuisine'
    id = Column(Integer, primary_key=True)
    name = Column(String(255))

    restaurant = relationship(
        'Restaurant',
        cascade='all, delete',
        passive_deletes=True
    )

    def __repr__(self):
        return f"<Cuisine(name='{self.name}')>"
