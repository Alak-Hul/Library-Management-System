class _LibraryItem:
    def __init__(self, title, publisher):
        self.title = title
        self.publisher = publisher
        self.__checked_in = False

    def is_status(self):
        return self.__checked_in
    
    def check_out(self):
        self.__checked_in = True
        ## and change their status in the .csv

    def check_in(self):
        self.__checked_in = False
        ## and change their status in the .csv

class Book(_LibraryItem):
    def __init__(self, title, publisher, author, ISBN):
        super().__init__(title, publisher)
        self.author = author
        self.ISBN = ISBN

class Magazine(_LibraryItem):
    def __init__(self, title, publisher, issue_num=int):
        super().__init__(title, publisher)
        self.issue_num = issue_num

class Account:
    def __init__(self, first_name, last_name):
        self.first_name = first_name
        self.last_name = last_name
        # entry = 
        # self.accountId = entry + 1
        # 
        ## entry will read from a text file which contains all account ids of other accounts and 
        ## gather the latest entry and adds 1, then appends the id to the entries text file