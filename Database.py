import csv
import pickle
from Books import Book, Magazine
from Library import Library
from Account import Account

class Database:
    def __init__(self, books_file, magazine_file, libraries_file, accounts_file):
        self.books_file = books_file
        self.accounts_file = accounts_file
        self.libraries_file = libraries_file
        self.magazine_file = magazine_file
       
        self.libraries = []
        self.accounts = []
        
        
        #All the code below for books and accounts was made with the intention that it wouldn't be added too if books, magazines, or accounts had aditional attributes added in the future
        try:
            #Books & Libraries
            books_grouped_by_library = {}
            with open(books_file, newline='') as csvfile:
                reader = csv.DictReader(csvfile, delimiter=",", quotechar='"')

                for book_in_csv in reader:
                    library_in_csv = book_in_csv.popitem()[1]
                    if library_in_csv not in books_grouped_by_library:
                        books_grouped_by_library[library_in_csv] = []
                    new_book = Book(**book_in_csv)
                    books_grouped_by_library[library_in_csv].append(new_book)

                
                for location, books in books_grouped_by_library.items():
                    self.libraries.append(Library(location, books))

        except FileNotFoundError:
            print("ERROR: INVALID BOOK FILE NAME")


        #Magazine & Libraries
        try:
            magazines_grouped_by_library = {}
            with open(magazine_file, newline='') as csvfile:
                reader = csv.DictReader(csvfile, delimiter=",", quotechar='"')

                for magazine_in_csv in reader:
                    library_in_csv = magazine_in_csv.popitem()[1]
                    if library_in_csv not in magazines_grouped_by_library:
                        magazines_grouped_by_library[library_in_csv] = []
                    new_magazine =  Magazine(**magazine_in_csv)
                    magazines_grouped_by_library[library_in_csv].append(new_magazine)

                for location, magazines in magazines_grouped_by_library.items():
                    existing_library = next(library for library in self.libraries if library.location == location)
                    if existing_library:
                        existing_library.magazines = magazines
                    else:
                        self.libraries.append(Library(location, magazines))

        except FileNotFoundError:
            print("ERROR: INVALID MAGAZINE FILE NAME")
    
        try:
            #ACCOUNTS
            with open(accounts_file, newline='') as csvfile:
                reader = csv.DictReader(csvfile, delimiter=",", quotechar='"')
                
                for account_in_csv in reader:

                    if account_in_csv["books"] != "":
                        ISBNs = account_in_csv["books"].split(",")
                        account_in_csv["books"] = []
                        for ISBN in ISBNs:
                            for library in self.libraries:
                                for book in library.books:
                                    if book == ISBN:
                                        account_in_csv["books"].append(book)
                    else:
                        account_in_csv["books"] = []

                    if account_in_csv["magazines"] != "":
                        ISSNs = account_in_csv["magazines"].split(",")
                        account_in_csv["magazines"] = []
                        #Todo Finish This
                    else:
                        account_in_csv["magazines"] = []
                    self.accounts.append(Account(**account_in_csv))
        except FileNotFoundError:
            print("ERROR: INVALID ACCOUNT FILE NAME")
        

        
    '''    
    # This caused for problem then it was worth
    def save_data(self):
        try:
            with open(self.books_file, "wb") as pkl_file:
                pickle.dump(self.books, pkl_file)
        except FileNotFoundError:
            print("ERROR: Invaild Books File")
        
        try:
            with open(self.magazine_file, 'wb') as pkl_file:
                pickle.dump(self.magazines, pkl_file)
        except FileNotFoundError:
            print("ERROR: Invaild Magazines File")

        try:
            with open(self.libraries_file, "wb") as pkl_file:
                pickle.dump(self.libraries, pkl_file)
        except FileNotFoundError:
            print("ERROR: Invaild Libraries File")

        try:
            with open(self.accounts_file, 'wb') as pkl_file:
                pickle.dump(self.accounts, pkl_file)
        except FileNotFoundError:
            print("ERROR: Invaild Accounts File")
        
            

    def load_data(self):
        with open(self.books_file, "rb") as pkl_file:
            self.books = pickle.load(pkl_file)
        
        with open(self.magazine_file, "rb") as pkl_file:
            self.magazines = pickle.load(pkl_file)

        with open(self.libraries_file, 'rb') as pkl_file:
            self.libraries = pickle.load(pkl_file)
        
        with open(self.accounts_file, "rb") as pkl_file:
            self.accounts = pickle.load(pkl_file)
    '''

    def save(self):
        books_file = self.books_file
        magazine_file = self.magazine_file
        accounts_file = self.accounts_file


        backup = ""

        with open(books_file, mode='r', newline='') as csvfile:
            backup = csvfile.read()


        #Books & Libraries
        try:
            with open(books_file, mode='w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                keys = list(self.libraries[0].books[0].__dict__.keys())
                keys.append("Library")

                writer.writerow(keys) # writes all book attribute names as well as "Library"

                for library in self.libraries:
                    for book in library.books:
                        values = list(book.__dict__.values())
                        values.append(library.location)
                        writer.writerow(values) # writes all book attribute values as well as its library location

        except Exception as error:
            #To stop all data getting deleted of a crash happens
            with open(books_file, mode='w', newline="") as csvfile:
                csvfile.write(backup)
            
            print("Error: Save Failed, Reverted to Most recent data")
            raise error
            
        with open(accounts_file, mode='r', newline='') as csvfile:
            backup = csvfile.read()


        #Magazines & Libraries
        with open(magazine_file, mode="r", newline='') as csvfile:
            backup = csvfile.read()

        try:
            with open(magazine_file, mode="w", newline="") as csvfile:
                writer = csv.writer(csvfile)
                keys = list(self.libraries[0].magazines[0].__dict__.keys())
                keys.append("Library")

                writer.writerow(keys)

                for library in self.libraries:
                    for magazine in library.magazines:
                        values = list(magazine.__dict__.values())
                        values.append(library.location)
                        writer.writerow(values)

        except Exception as error:
            #To stop all data getting deleted of a crash happens
            with open(magazine_file, mode='w', newline="") as csvfile:
                csvfile.write(backup)
            
            print("Error: Save Failed, Reverted to Most recent data")
            raise error



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
                            books_str += f"{book._ISBN}," # converts owned books into a str repersentation
                    account.books = books_str

                    magazine_str = None
                    if account.magazines != None:
                        magazine_str = ''
                        for magazine in account.magazines:
                            magazine_str += f"{magazine._ISSN}," # converts owned magazines into a str repersentation
                    account.magazines = magazine_str

                    values = list(account.__dict__.values())
                    writer.writerow(values) # writes all book attribute values
        except Exception as error:
            #To stop all data getting deleted if a crash happens
            with open(accounts_file, mode='w', newline="") as csvfile:
                csvfile.write(backup)
            
            print("Error: Save Failed, Reverted to Most recent data")
            raise error
            

    def books_search(self, keyword, attr):
        list = [] # just makes a list so append() can be used
        for library in self.libraries:
            for book in library.books: # Iterates though all books in the database
                if keyword.lower() in getattr(book, attr, "").lower(): # getattr() is just so the attrbute can be dynamic, it just finds the object's attribute that has a name that matches the string given. And lower() is just so it isn't case senstive
                    list.append(book) # adds the book that matchs the keyword to the list 
        return list # Returns a list of books that match the search criteria.
    
    def magazine_search(self, keyword, attr):
        list = [] # just makes a list so append() can be used
        for library in self.libraries:
            for magazine in library.magazines: # Iterates though all books in the database
                if keyword.lower() in getattr(magazine, attr, "").lower(): # getattr() is just so the attrbute can be dynamic, it just finds the object's attribute that has a name that matches the string given. And lower() is just so it isn't case senstive
                    list.append(magazine) # adds the book that matchs the keyword to the list 
        return list # Returns a list of books that match the search criteria.

    def create_account(self, name, id):
        name = name.split(" ")
        if len(name) < 2:
            name.append("None")
        self.accounts.append(Account(name[0], name[1], id, [], []))
        print(self.accounts[-1])
        self.save()
    
    def create_book(self, title, author, publisher, library_location="North"):
        print(f"{author = }, {publisher = }")
        highest = 0
        for book in self.books:
            current_ISBN = book._ISBN.split("-")
            if int(current_ISBN[2]) > highest:
                highest = int(current_ISBN[2])
        ISBN = f"0000-0000-{highest+1:04}"

        new_book = Book(title, publisher, author, ISBN)

        for library in self.libraries: # Find the library and add the book to it
            if library.location == library_location:
                library.books.append(new_book)
                break

        self.books.append(new_book)
        print(f"NEW BOOK: \n{self.books[-1]} ") # or you can make this return something if you want to display it in the UI 
    
    def create_magazine(self, title, publisher, issue_num, library_location="north"):
        highest = 0
        for magazine in self.magazines:
            current_ISSN = magazine._ISSN.split("-")
            if int(current_ISSN[1]) > highest:
                highest = int(current_ISSN[1])
        ISSN = f"0000-0000-{highest+1:04}"

        new_magazine = Magazine(title, publisher, issue_num, ISSN)

        for library in self.libraries: # Find the library and add the magazine to it
            if library.location == library_location:
                library.magazines.append(new_magazine)
                print(library)
                break
                
        self.magazines.append(new_magazine)
        print(f'NEW MAGAZINE: \n{self.magazines[-1:]}') # same for here: line 169

    def check_out_book(self, ISBN, account, library):
        book = next((book for book in library.books if book.get_ISBN() == ISBN), None) # finds book or give a default value of none

        if book and book not in account.books and book.is_status():
            account.books.append(book)
            print(account)
        return book
    
    def check_in_book(self, title, account):
        book = next((book for book in account.books if book.title == title), None) # finds book or give a default value of none
        if book:
            account.books.remove(book)
        return book

    def check_out_magazine(self, ISSN, account, library):
        
        magazine = next((magazine for magazine in library.magazines if magazine.get_ISSN()== ISSN), None) # finds book or give a default value of none

        if magazine and magazine not in account.magazines and magazine.is_status():
            account.magazines.append(magazine)
        return magazine
        
    def check_in_magazine(self, title, account):
        magazine = next((magazine for magazine in account.magazines if magazine.title == title), None) # finds book or give a default value of none
        if magazine:
            account.magazines.remove(magazine)
        return magazine
        



    def __repr__(self):
        str = "BOOKS:\n"
        str += "LIBRARIES: \n"
        for library in self.libraries:
            str += f"    {library}"
        str += "ACCOUNTS: \n"
        for account in self.accounts:
            str += f"    {account}"
        return str
    
