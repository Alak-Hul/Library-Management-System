class Book:
    def __init__(self, title, author):
        self.title = title
        self.author = author
        self.__checked_in = False

    def is_status(self):
        return self.__checked_in
    
    def check_out(self):
        self.__checked_in = True
        ## and change their status in the .csv

    def check_in(self):
        self.__checked_in = False
        ## and change their status in the .csv
