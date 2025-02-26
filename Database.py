import csv
from Books import Book, Magazine
from Library import Library
from Account import Account

class Database:
    def __init__(self, books_file, accounts_file):
        self.books_file = books_file
        self.accounts_file = accounts_file
        books_grouped_by_library = {}
        libraries = []
        accounts = []
        
        
        try:
            #BOOKS & LIBRARIES
            with open(books_file, newline='') as csvfile:
                reader = csv.DictReader(csvfile, delimiter=",", quotechar='"')

                for book_in_csv in reader:
                    lib = book_in_csv.popitem()[1]
                    if lib not in books_grouped_by_library:
                        books_grouped_by_library[lib] = []
                    book = (Book(**book_in_csv))
                    books_grouped_by_library[lib].append(book)

                
                for key, value in books_grouped_by_library.items():
                    libraries.append(Library(key, value))

        except OSError:
            print("ERROR: INVALID BOOK FILE NAME")

        self.books = sum(books_grouped_by_library.values(),[]) # Ungroups the books
        self.libraries = libraries

        try:
            #ACCOUNTS
            with open(accounts_file, newline='') as csvfile:
                reader = csv.DictReader(csvfile, delimiter=",", quotechar='"')
                
                for account_in_csv in reader:
                    if account_in_csv["books"] != "None":
                        ISBNs = account_in_csv["books"].split(",")
                        account_in_csv["books"] = []
                        for ISBN in ISBNs:
                            for book in self.books:
                                if book == ISBN:
                                    account_in_csv["books"].append(book)
                    accounts.append(Account(**account_in_csv))
        except OSError:
            print("ERROR: INVALID ACCOUNT FILE NAME")


        self.accounts = accounts


    def save(self):
        books_file = self.books_file
        accounts_file = self.accounts_file

        #Books & Libraries
        with open(books_file, mode='w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["ISBN","title","author","publisher","status","library"])
            for lib in self.libraries:
                for book in lib.books:
                    writer.writerow([book.ISBN,book.title,book.author,book.publisher,book.is_status(),lib.location])
        

        # Accounts
        with open(accounts_file, mode="w", newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["ID","first_name","last_name","books"])
            for account in self.accounts:
                if account.books != None:
                    books_str = ''
                    for book in account.books:
                        books_str += f"{book.ISBN},"
                    books_str += ''
                writer.writerow([account.ID, str(account.get_first_name()), str(account.get_last_name()), books_str])


    def __repr__(self):
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
    
    