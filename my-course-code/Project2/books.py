
# Import the FastAPI Framework
from fastapi import FastAPI, Body 
from pydantic import BaseModel, Field
from typing import Optional

# Create an instance of a FastAPI
app = FastAPI()

#
# Model a Book Object.
#
class Book():
    
    # Class Properties
    id: int
    title: str
    author: str
    description: str
    rating: int

    # Class Constructor
    def __init__(self, id, title, author, description, rating):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating

#
# Model Request Validator
#
class BookRequest(BaseModel):

    # Class Properties
    id: Optional[int]
    title: str =  Field(min_length=3)
    author: str = Field(min_length=1)
    description: str =  Field(min_length=1, max_length=100)
    rating: int = Field(gt=0, lt=6)

    class Config:
        schema_extra = {
            'example': {
                'Title': " The name of the book",
                'Author': 'The person who wrote the book',
                'Description': 'A breif synopsis of the book',
                'Rating': 'A Numerical valude from 1 to 6 on the quality or experience of the book'
            }
        }



# Create a data structure to hold the books in our API
BOOKS = [
   Book(id=1, title="My Neat Book", author="Rob Tobulox", description="This is a description", rating=1),
   Book(id=2, title="My Cool Book", author="Jurry Bobulox", description="This is a description", rating=5),
   Book(id=3, title="My Keen Book", author="Felicity Glorgox", description="This is a description", rating=5),
   Book(id=4, title="My Nifty Book", author="Michael Fremulon", description="This is a description", rating=5),
   Book(id=5, title="My Swell Book", author="Turry Tobulox", description="This is a description", rating=5)
]



@app.get("/books")
async def read_all_books():
    return BOOKS

@ app.get("/books/{id}")
async def get_book_by_ID(id: int):
    for book in BOOKS:
        if book.id == id:
            return book
    

@app.post("/create-book")
async def create_book(book_request: BookRequest):
    
    # Create a new book object for the Keyword Arguments (** means kwargs)
    # we're creating by unpacking the body as a dictionary. Basically,
    # the request body is a dictionary that supplies the keywords to be 
    # unpacked by the **
    new_book = Book(**book_request.dict())
    BOOKS.append(find_book_id(new_book))




def find_book_id(book: Book):
    if len(BOOKS) > 0:
        book.id = BOOKS[-1].id + 1
    else:           
         book.id = 1

    # This should be the actuall object, not the refernce
    # to the class.
    return book