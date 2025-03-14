from abc import abstractmethod


class _LibraryItem:
    def __init__(self, title, publisher, _checked_in, _checked_in_date=None):
        self.title = title
        self.publisher = publisher
        self._checked_in = _checked_in
        self._checked_in_date = None

    def is_status(self):
        return self._checked_in
    
    def check_out(self):
        self._checked_in = True

    def check_in(self):
        self._checked_in = False 
        
    @abstractmethod
    def due_date(self):
        pass

    def __repr__(self):
        attrs = ""
        for key, value in self.__dict__.items():
            attrs += f'{key}: {value}' + ","
        return attrs

class Book(_LibraryItem):
    def __init__(self, title, publisher, author, _ISBN, _checked_in = True, _checked_in_date=None ):
        super().__init__(title, publisher, _checked_in, _checked_in_date)
        self.author = author
        self._ISBN = _ISBN

    def get_ISBN(self):
        return self._ISBN

    def due_date(self):
        return "need to finish this"
    
    def __eq__(self, isbn):
        return self._ISBN == isbn

class Magazine(_LibraryItem):
    def __init__(self, title, publisher, issue_num=0, _ISSN=0, _checked_in = True, _checked_in_date=None):
        super().__init__(title, publisher, _checked_in, _checked_in_date)
        self.issue_num = issue_num
        self._ISSN = _ISSN

    def due_date(self):
        return "need to finish this"