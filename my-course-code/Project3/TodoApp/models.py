# From SQLAlchemy import
from sqlalchemy import Column, Integer, String, Boolean

# Use the Base (datasource) we defined earlier
from database import Base


class Todos(Base):
    '''This class is responsible for defining the table that will store TODO Items.'''

    __tablename__ = 'todos'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    priority = Column(Integer)
    complete = Column(Boolean, default=False)

