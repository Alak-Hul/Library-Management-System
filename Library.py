
class Library:
    def __init__(self, location="Unknown", books=["testing", "testing2", "testing3"]):
        self.location = location #North, South, East, West
        self.books = books


    def __str__(self):
        str = f"Location: {self.location} \n\nBooks: \n"
        
        booksStr = ""
        for book in self.books:
            booksStr = booksStr + f' {book} \n'

        return str +  booksStr

lib = Library()

print(lib)
# this is just temp, I won't know how to make this until I see how the books are set up