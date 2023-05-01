# Import the fast API Package for obvious reasons. 
from fastapi import FastAPI


# import our dummy data.
BOOKS = [
    {'title': 'Title One', 'author': 'Author One', 'category': 'science'},
    {'title': 'Title Two', 'author': 'Author Two', 'category': 'science'},
    {'title': 'Title Three', 'author': 'Author Three', 'category': 'history'},
    {'title': 'Title Four', 'author': 'Author Four', 'category': 'math'},
    {'title': 'Title Five', 'author': 'Author Five', 'category': 'math'},
    {'title': 'Title Six', 'author': 'Author Two', 'category': 'math'}
]

# Create an instance of a fast API called app
app = FastAPI()

#
# Define Endpoints
#

#Use the get() decoractor to create a get endpoint
@app.get("/books")
# Async is not needed for fast API because the functionality
# is added automatically behind the scenes.
async def read_all_books():
    "FastAPI Acknowledges Docstrings!"
    return BOOKS


@app.get("/books/{book_title}")
# "dynamic_param: str" this is called TYPE HINTING
async def get_book(book_title: str):
    for book in BOOKS:
        if book.get("title").casefold() == book_title.casefold():
            return book
