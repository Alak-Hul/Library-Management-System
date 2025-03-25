
class Library:
    def __init__(self, location="Unknown", books=[], magazines=[] ):
        self.location = location #North, South
        self.books = books
        self.magazines = magazines if magazines is not None else [] # this is the strangest thing I have ever seen python do it would treat magazines as the same list across all libraries dispite using self


    def __str__(self):
        str = f"Location: {self.location} \n"
        
        booksStr = "Books: \n"
        for book in self.books:
            booksStr = booksStr + f'        {book} \n'


        magazine_str = "f'Magazines: \n"
        for magazine in self.magazines:
            magazine_str = magazine_str + f"         {magazine} \n"
        return str +  booksStr + '\n' + magazine_str

