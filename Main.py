from Books import Book

book1 = Book("The Witcher: Last Wish", "Angry Polish Guy","0-061-96436-0")

print(f'{book1.is_status() = }')
print(book1.ISBN,book1.author)