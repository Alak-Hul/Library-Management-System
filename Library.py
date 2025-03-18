
class Library:
    def __init__(self, location="Unknown", books=[], magazines=None):
        self.location = location #North, South
        self.books = books
        self.magazines = magazines if magazines is not None else [] # this is the strangest thing I have ever seen python do it would treat magazines as the same list across all libraries dispite using self


    def __str__(self):
        str = f"Location: {self.location} \n    Books: \n"
        
        booksStr = ""
        for book in self.books:
            booksStr = booksStr + f'        {book} \n'

        return str +  booksStr + '\n'



lib = Library()
