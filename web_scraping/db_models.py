from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class RestaurantT(Base):
    __tablename__ = 'restaurants_tripadvisor'

    _id = Column(Integer, primary_key=True)
    name = Column(String)
    rating = Column(Float)
    num_reviews = Column(Integer)
    cuisines = Column(String)
    address = Column(String)

    def __repr__(self):
        return f"<RestaurantT(_id={self._id}, name={self.name}, rating={self.rating}, num_reviews={self.num_reviews}, cuisine={self.cuisines}, address={self.address})>"
