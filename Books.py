from abc import abstractmethod
from datetime import datetime, timedelta


class _LibraryItem:
    def __init__(self, title, publisher, _checked_in, _check_in_date=None):
        self.title = title
        self.publisher = publisher
        self._checked_in = True if _checked_in == "True" else False
        self._check_in_date = _check_in_date

    def is_status(self):
        return self._checked_in
    
    def check_in(self):
        self._checked_in = True
        self._check_in_date = None

    def check_out(self):
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
    def __init__(self, title, publisher, author, _ISBN, _checked_in = True, _check_in_date=None ):
        super().__init__(title, publisher, _checked_in, _check_in_date)
        self.author = author
        self._ISBN = _ISBN

    def get_ISBN(self):
        return self._ISBN

    def due_date(self):
        if self._check_in_date:
            return(datetime.strptime(self._checked_in_date,"%Y-%m-%d")+timedelta(days=14)).strftime("%Y-%m-%d")
        return("14 days from checkout")
    
    def __eq__(self, isbn):
        return self._ISBN == isbn

class Magazine(_LibraryItem):
    def __init__(self, title, publisher, issue_num=0, _ISSN=0, _checked_in = True, _check_in_date=None):
        super().__init__(title, publisher, _checked_in, _check_in_date)
        self.issue_num = f"{issue_num:03}"
        self._ISSN = _ISSN

    def get_ISSN(self):
        return self._ISSN

    def due_date(self):
        if self._check_in_date:
            return(datetime.strptime(self._check_in_date,"%Y-%m-%d")+timedelta(days=7)).strftime("%Y-%m-%d")
        return("7 days from checkout")
    
    def __eq__(self, ISSN):
        return self._ISSN == ISSN