
class Account:
    def __init__(self, first_name="None", last_name="None", ID=0, books=None, magazines=None):
        self.__first_name=first_name
        self.__last_name=last_name
        self.ID = ID
        self.books = books if books != "None" else None
        self.magazines = magazines

    def get_first_name(self):
        return self.__first_name
    
    def get_last_name(self):
        return self.__last_name

    def __repr__(self):
        attrs = ""
        for key, value in self.__dict__.items():
            attrs += f'{key}: {value}' + ", "
        return attrs