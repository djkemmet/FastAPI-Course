# From SQLAlchemy import
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey

# Use the Base (datasource) we defined earlier
from database import Base

class Users(Base):
    ''' This class represents a User object.'''

    # Table name as property of the class.
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True)
    username = Column(String, unique=True)
    first_name = Column(String)
    last_name = Column(String)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    role = Column(String)

    #Class Fields

class Todos(Base):
    '''This class represents a Todo object'''

    __tablename__ = 'todos'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    priority = Column(Integer)
    complete = Column(Boolean, default=False)
    owner_id = Column(Integer, ForeignKey("users.id"))
