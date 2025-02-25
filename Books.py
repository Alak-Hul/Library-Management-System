from abc import abstractmethod


class _LibraryItem:
    def __init__(self, title, publisher, status):
        self.title = title
        self.publisher = publisher
        self.__checked_in = status
        self.__checked_in_date = None

    def is_status(self):
        return self.__checked_in
    
    def check_out(self):
        self.__checked_in = True

    def check_in(self):
        self.__checked_in = False 
        
    @abstractmethod
    def due_date(self):
        pass

    def __repr__(self):
        attrs = ""
        for key, value in self.__dict__.items():
            attrs += f'{key}: {value}' + ", "
        return attrs

class Book(_LibraryItem):
    def __init__(self, title, publisher, author, status, ISBN=0):
        super().__init__(title, status, publisher)
        self.author = author
        self.ISBN = ISBN

    def due_date(self):
        return "need to finish this"

class Magazine(_LibraryItem):
    def __init__(self, title, publisher, status , issue_num=int):
        super().__init__(title, status, publisher)
        self.issue_num = issue_num

    def due_date(self):
        return "need to finish this"