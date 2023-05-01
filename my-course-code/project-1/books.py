# Import the fast API Package for obvious reasons. 
from fastapi import Body, FastAPI


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


# Searching by a single criteria
@app.get("/books/")
async def read_category_by_query(category: str):
    books_to_return = []
    for book in BOOKS: 
        if book.get('category').casefold() == category.casefold():
            books_to_return.append(book)
    return books_to_return     

# Further filtering the search with a path and query parameter
@app.get("/books/{book_author}/")
async def read_author_category_by_query(book_author: str, category: str):
    books_to_return = []
    for book in BOOKS:
        if book.get('author').casefold() == book_author.casefold() and book.get('category').casefold() == category.casefold():
            books_to_return.append(book)
    return books_to_return



# Our first POST Function
@app.post("/books/create_book")
async def create_book(new_book=Body()):
    BOOKS.append(new_book)
