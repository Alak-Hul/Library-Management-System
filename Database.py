import csv
from Books import Book, Magazine
from Library import Library

class Database:
    def __init__(self, file):
        try:
            with open(file, newline='') as csvfile:
                reader = csv.DictReader(csvfile, delimiter=",", quotechar="|")

                books_grouped_by_library = {}
                for book_in_csv in reader:
                    lib = book_in_csv.popitem()[1]
                    if lib not in books_grouped_by_library:
                        books_grouped_by_library[lib] = []
                    book = (Book(**book_in_csv))
                    books_grouped_by_library[lib].append(book)

                libraries = []
                for key, value in books_grouped_by_library.items():
                    libraries.append(Library(key, value))
        except OSError:
            print("ERROR: Use A Vaild .csv File")

        self.books = list(books_grouped_by_library.values())[0]
        self.libraries = libraries
db = Database("books.csv")
print(db)