
# Import the FastAPI Framework
from fastapi import FastAPI

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
    Book(1, 'Thought Reform and the Psychology of Totalism','Robert Jay Lifton', "Informed by Erik Erikson\'s concept of the formation of ego identity, this book, which first appreared in 1961, is an analysis of the experiences of fifteen Chinese citizens and twenty-five Westerners who underwent 'brainwashing' by the Communist Chinese government. Robert Lifton constructs these case histories through personal interviews and outlines a thematic pattern of death and rebirth, accompanied by feelings of guilt, that characterizes the process of 'thought reform.' In a new preface, Lifton addresses the implications of his model for the study of American religious cults.", 5 ),
    Book(2, 'Ender\'s Game', 'Dude goes to space school to fight alien crickets.', 5),
    Book(3, 'Harry Potter', "dude findss out he's magic, learns to harness his razzmataz with other magic children", 4),
]



@app.get("/books")
async def read_all_books():
    return BOOKS