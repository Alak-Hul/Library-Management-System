
class Library:
    def __init__(self, location="Unknown", books=["testing", "testing2", "testing3"]):
        self.location = location #North, South
        self.books = books


    def __str__(self):
        str = f"Location: {self.location} \n    Books: \n"
        
        booksStr = ""
        for book in self.books:
            booksStr = booksStr + f'        {book} \n'

        return str +  booksStr + '\n'



lib = Library()
