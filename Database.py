import csv
from Books import Book, Magazine
from Library import Library
from Account import Account

class Database:
    def __init__(self, books_file, accounts_file):
        books_grouped_by_library = {}
        libraries = []
        accounts = []
        
        
        try:
            #BOOKS & LIBRARIES
            with open(books_file, newline='') as csvfile:
                reader = csv.DictReader(csvfile, delimiter=",", quotechar="|")

                for book_in_csv in reader:
                    lib = book_in_csv.popitem()[1]
                    if lib not in books_grouped_by_library:
                        books_grouped_by_library[lib] = []
                    book = (Book(**book_in_csv))
                    books_grouped_by_library[lib].append(book)

                
                for key, value in books_grouped_by_library.items():
                    libraries.append(Library(key, value))

           

        except OSError:
            print("ERROR: INVAILD BOOK FILE NAME")

           
        self.books = list(books_grouped_by_library.values())[0]
        self.libraries = libraries
        try:
            #ACCOUNTS
            with open(accounts_file, newline='') as csvfile:
                reader = csv.DictReader(csvfile, delimiter=",", quotechar="|")
                
                for account_in_csv in reader:
                    accounts.append(Account(**account_in_csv))
        except OSError:
            print("ERROR: INVAILD ACCOUNT FILE NAME")


        self.accounts = accounts


    def __str__(self):
        str = "BOOKS:\n"
        for book in self.books:
            str += f"    {book} \n"
        str += "LIBRARIES: \n"
        for lib in self.libraries:
            str += f"    {lib}"
        str += "ACCOUNTS: \n"
        for acc in self.accounts:
            str += f"    {acc}"
        return str
    


