
# Import the FastAPI Framework
from fastapi import FastAPI, Body 

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

@app.post("/create-book")
async def create_book(book_request= Body()):
    BOOKS.append(book_request)
