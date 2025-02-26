import tkinter as tk
from tkinter import *
from tkinter import ttk


from Database import Database


db = Database('books.csv', 'account.csv')
print(db)
db.save()

class LibraryGUI:
    def __init__(self,root):
        self.root=root
        self.root.title("Library Management System")
        self.root.geometry("960x540")
        self.notebook=ttk.Notebook(root)
        self.notebook.pack(expand=True,fill="both")

        self.items_frame=ttk.Frame(self.notebook)
        self.account_frame=ttk.Frame(self.notebook)
        self.library_frame=ttk.Frame(self.notebook)

        self.notebook.add(self.items_frame,text="Items")
        self.notebook.add(self.account_frame,text="Accounts")
        self.notebook.add(self.library_frame,text="Libraries")

        self.books_section()

    def books_section(self):
        ttk.Label(self.items_frame,text="Library Items",font=("Arial",16)).pack()
        self.item_notebook=ttk.Notebook(self.items_frame)
        self.item_notebook.pack(expand=True,fill="both")

        self.book_frame=ttk.Frame(self.item_notebook)
        self.magazine_frame=ttk.Frame(self.item_notebook)

        self.item_notebook.add(self.book_frame,text="Books")
        self.item_notebook.add(self.magazine_frame,text="Magazines")

        # Book Section
        ttk.Label(self.book_frame,text="Books List",font=("Arial",12)).pack()

        # Magazine Section
        ttk.Label(self.magazine_frame,text="Magazines List",font=("Arial",12)).pack()


root=tk.Tk()
lb=LibraryGUI(root)
root.mainloop()