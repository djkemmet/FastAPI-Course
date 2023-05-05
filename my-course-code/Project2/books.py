
# Import the FastAPI Framework
from fastapi import FastAPI, Body, Path, Query, HTTPException
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
    published_date: int

    # Class Constructor
    def __init__(self, id, title, author, description, rating, published_date):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating
        self.published_date = published_date

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
    published_date: int

    class Config:
        schema_extra = {
            'example': {
                'id': 'an optional parameter to identify the book',
                'title': " The name of the book",
                'author': 'The person who wrote the book',
                'description': 'A breif synopsis of the book',
                'rating': 'A Numerical valude from 1 to 6 on the quality or experience of the book'
            }
        }



# Create a data structure to hold the books in our API
BOOKS = [
   Book(id=1, title="My Neat Book", author="Rob Tobulox", description="This is a description", rating=1, published_date=2000),
   Book(id=2, title="My Cool Book", author="Jurry Bobulox", description="This is a description", rating=5, published_date=2000),
   Book(id=3, title="My Keen Book", author="Felicity Glorgox", description="This is a description", rating=4, published_date=2000),
   Book(id=4, title="My Nifty Book", author="Michael Fremulon", description="This is a description", rating=4, published_date=2000),
   Book(id=5, title="My Radical Book", author="Prassad Gorbechav", description="This is a description", rating=5, published_date=2000),
   Book(id=6, title="My Awesome Book", author="Justice Northwind", description="This is a description", rating=3, published_date=2000),
   Book(id=7, title="My Mighty Book", author="Constantine Frindle", description="This is a description", rating=2, published_date=2000),
   Book(id=8, title="My Boring Book", author="Bobulox Arzronand", description="This is a description", rating=5, published_date=2000)
]

#
# GETs
#
@app.get("/books")
async def read_all_books():
    return BOOKS

@app.get("/books/{id}")
async def read_book(id: int = Path(gt = 0)):
    for book in BOOKS:
        if book.id == id:
            return book
        
    raise HTTPException(detail=f"A book with ID {id} was not found.", status_code=404)
    
@app.get("/books_by_rating/{book_rating}")
async def get_book_by_rating(book_rating: int = Path(gt=0, lt=6)):
    books_to_return = []
    for book in BOOKS:
        if book.rating == book_rating:
            books_to_return.append(book)
    return books_to_return

@app.get("/books/in-year/{year}")
async def get_book_by_year(published_date: int = Query(gt=1999, lt=2031)):
    books_to_return = []
    for book_number in range(len(BOOKS)):
        if BOOKS[book_number].published_date == published_date:
            books_to_return.add(BOOKS[book_number])
    return books_to_return

#
# POSTs
#
@app.post("/create-book")
async def create_book(book_request: BookRequest):
    
    # Create a new book object for the Keyword Arguments (** means kwargs)
    # we're creating by unpacking the body as a dictionary. Basically,
    # the request body is a dictionary that supplies the keywords to be 
    # unpacked by the **
    new_book = Book(**book_request.dict())
    BOOKS.append(find_book_id(new_book))

#
# PUTs
#
@app.put("/books/update-book") 
# This function needs to unpack the data from the body
# into a BookRequest validator
async def update_book(book: BookRequest):
    #Did our book change? 
    book_changed = False

    # Iterate through our books
    for book_number in range(len(BOOKS)):

        # If the book we're currently looking at shares
        # the ID of the updated book data we sent through
        # the API
        if BOOKS[book_number].id == book.id:
            
            # Replace the data at that index, effectively 
            # updating the book.
            BOOKS[book_number] = book
            book_changed = True
    if not book_changed:
        raise HTTPException(status_code=404, detail="Item not found.")


@app.delete("/delete-book/{book_id}")
async def delete_book(book_id: int = Path(gt=0)):
    book_changed = False
    print(f"Book ID is {book_id}")
    for book_number in range(len(BOOKS)):
        if BOOKS[book_number].id == book_id:
            BOOKS.pop(book_number)
            book_changed = True
    if not book_changed:
        raise HTTPException(status_code=404, detail="Item not found.")

def find_book_id(book: Book):
    if len(BOOKS) > 0:
        book.id = BOOKS[-1].id + 1
    else:           
         book.id = 1

    # This should be the actuall object, not the refernce
    # to the class.
    return book