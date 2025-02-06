from tkinter import *
from tkinter import ttk

from Books import Book, Magazine
from Account import Account
from Library import Library


book1 = Book("The Witcher: Last Wish", "SuperNowa", "Angry Polish Guy","0-061-96436-0")
magazine1 = ("People","Meredith Corperation", 10)

print(f'{book1.is_status() = }')
print(book1.ISBN,book1.author)

# Quick Tkinter Test
root = Tk()
frm = ttk.Frame(root, padding=10)
frm.grid()
ttk.Label(frm, text="Hello World!").grid(column=0, row=0)
ttk.Button(frm, text="Quit", command=root.destroy).grid(column=1, row=0)
root.mainloop()