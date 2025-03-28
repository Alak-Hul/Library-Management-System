
class Account:
    def __init__(self, _first_name="None", _last_name="None", _ID=0, books=None, magazines=None): 
        self._first_name=_first_name
        self._last_name=_last_name
        self._ID = _ID
        self.books = books if books else [] # Python call by reference would break this causing multiple accounts to have the same books
        self.magazines = magazines if magazines else [] # same here

    def get_first_name(self):
        return self._first_name
    
    def get_last_name(self):
        return self._last_name
    
    def get_ID(self):
        return self._ID
    
    def __eq__(self, ID):
        return self._ID == ID

    def __repr__(self):
        attrs = ""
        for key, value in self.__dict__.items():
            attrs += f'{key}: {value}' + ", "
        return attrs