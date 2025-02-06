from Books import Book, Magazine

book1 = Book("The Witcher: Last Wish", "SuperNowa","Angry Polish Guy","0-061-96436-0")
magazine1=Magazine("People","Meredith Corperation", 10)

print(f'{book1.is_status() = }')
print(book1.ISBN,book1.publisher)
print(magazine1.issue_num,magazine1.publisher)