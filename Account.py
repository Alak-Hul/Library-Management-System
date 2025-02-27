
class Account:
    def __init__(self, first_name, last_name, ID, books, ):
        self.__first_name=first_name
        self.__last_name=last_name
        self.ID = ID
        self.books = books

    def get_first_name(self):
        return self.__first_name
    
    def get_last_name(self):
        return self.__last_name

    def __repr__(self):
        attrs = ""
        for key, value in self.__dict__.items():
            attrs += f'{key}: {value}' + ", "
        return attrs