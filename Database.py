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
        
        #All the code below for books and accounts was made with the intention that it wouldn't be added too if books, magazines, or accounts had aditional attributes added in the future
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
        self.magazines = []
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

        backup = ""

        with open(books_file, mode='r', newline='') as csvfile:
            backup = csvfile.read()


        #Books & Libraries
        try:
            with open(books_file, mode='w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                keys = list(self.books[0].__dict__.keys())
                keys.append("Library")

                writer.writerow(keys) # writes all book attribute names as well as "Library"

                for lib in self.libraries:
                    for book in lib.books:
                        values = list(book.__dict__.values())
                        values.append(lib.location)
                        writer.writerow(values) # writes all book attribute values as well as its library location
        except Exception as e:
            #To stop all data getting deleted of a crash happens
            with open(books_file, mode='w', newline="") as csvfile:
                csvfile.write(backup)
            
            print("Error: Save File Reverted to Most recent data")
            raise e
            
        with open(accounts_file, mode='r', newline='') as csvfile:
            backup = csvfile.read()



        # Accounts
        try:
            #this way made so that more attributes can be added to book and magazine and no addtional code would need to be added here
            with open(accounts_file, mode="w", newline='') as csvfile:
                writer = csv.writer(csvfile)
                keys = list(self.accounts[0].__dict__.keys())
                writer.writerow(keys) # writes all book attribute names

                for account in self.accounts:
                    books_str = None
                    if account.books != None:
                        books_str = ''
                        for book in account.books:
                            books_str += f"{book.ISBN}," # converts owned books into a str repersentation
                    account.books = books_str

                    mag_str = None
                    if account.magazines != None:
                        mag_str = ''
                        for mag in account.magazines:
                            mag_str += f"{mag.issue_num}," # converts owned magazines into a str repersentation
                    account.magazines = mag_str

                    values = list(account.__dict__.values())
                    writer.writerow(values) # writes all book attribute values
        except Exception as e:
            #To stop all data getting deleted if a crash happens
            with open(accounts_file, mode='w', newline="") as csvfile:
                csvfile.write(backup)
            
            print("Error: Save File Reverted to Most recent data")
            raise e
            

    def books_search(self, keyword, attr):
        list = [] # just makes a list so append() can be used
        for book in self.books: # Iterates though all books in the database
            if keyword.lower() in getattr(book, attr, "").lower(): # getattr() is just so the attrbute can be dynamic, it just finds the object's attribute that has a name that matches the string given. And lower() is just so it isn't case senstive
                list.append(book) # adds the book that matchs the keyword to the list 
        return list # Returns a list of books that match the search criteria.

    def create_account(self, name, id):
        name = name.split(" ")
        if len(name) < 2:
            name.append("None")
        self.accounts.append(Account(name[0], name[1], id))
        print(self.accounts[-1])
        self.save()
    
    def create_book(self, title, author, publisher):
        highest = 0
        for book in self.books:
            current_ISBN = book._ISBN.split("-")
            if int(current_ISBN[2]) > highest:
                highest = int(current_ISBN[2])
        ISBN = f"0000-0000-{highest+1:04}"

        self.books.append(Book(title, author, publisher, ISBN))
        print(f"NEW BOOK: \n{self.books[-1]} ") # or you can make this return something if you want to display it in the UI 
    
    def create_magazine(self, title, publisher, issue_num):
        highest = 0
        for mgzns in self.magazines:
            current_ISSN = mgzns._ISSN.split("-")
            if int(current_ISSN[2]) > highest:
                highest = int(current_ISSN[2])
        ISSN = f"0000-0000-{highest+1:04}"
        
        self.magazines.append(Magazine(title,publisher, issue_num, ISSN))
        print(f'NEW MAGAZINE: \n{self.magazines[-1:]}') # same for here

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
    
