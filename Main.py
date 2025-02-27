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
        self.accounts_frame=ttk.Frame(self.notebook)
        self.library_frame=ttk.Frame(self.notebook)

        self.notebook.add(self.items_frame,text="Items")
        self.notebook.add(self.accounts_frame,text="Accounts")
        self.notebook.add(self.library_frame,text="Libraries")

        self.items_section()
        self.accounts_section()

    def items_section(self):
        ttk.Label(self.items_frame,text="Library Items",font=("Arial",16)).pack()
        self.item_notebook=ttk.Notebook(self.items_frame)
        self.item_notebook.pack(expand=True,fill="both")

        self.book_frame=ttk.Frame(self.item_notebook)
        self.magazine_frame=ttk.Frame(self.item_notebook)

        self.item_notebook.add(self.book_frame,text="Books")
        self.item_notebook.add(self.magazine_frame,text="Magazines")

        # Book Section
        ttk.Label(self.book_frame,text="Books List",font=("Arial",12)).pack()
        self.book_tree=ttk.Treeview(self.book_frame,columns=("ISBN","Title","Publisher","Status"),show="headings")
            # Search button
        search_frame=ttk.Frame(self.book_frame)
        search_frame.pack(pady=10)

        self.search_entry=ttk.Entry(search_frame)
        self.search_entry.pack(side="left",padx=5)
        ttk.Button(self.book_frame,text="Search",command=self.search_items).pack(side="left")

        # Magazine Section
        ttk.Label(self.magazine_frame,text="Magazines List",font=("Arial",12)).pack()
        self.magazine_tree = ttk.Treeview(self.magazine_frame, columns=("ISSN", "Title", "Publisher"), show="headings")
            # Search button
        search_frame=ttk.Frame(self.magazine_frame)
        search_frame.pack(pady=10)

        self.search_entry=ttk.Entry(search_frame)
        self.search_entry.pack(side="left",padx=5)
        ttk.Button(self.magazine_frame,text="Search",command=self.search_items).pack(side="left")

    def accounts_section(self):
        ttk.Label(self.accounts_frame,text="Search Account",font=("Arial",16)).pack()

        # Search button
        search_frame=ttk.Frame(self.accounts_frame)
        search_frame.pack(pady=10)

        self.search_entry=ttk.Entry(search_frame)
        self.search_entry.pack(side="left",padx=5)
        ttk.Button(search_frame,text="Search",command=self.search_account).pack(side="left")

        self.accounts_list=tk.Listbox(self.accounts_frame)
        self.accounts_list.pack(fill="both",expand=True)

    def search_items(self):
        search_query=self.search_entry.get().strip()
        for account in db.accounts:
            if search_query.lower() in account.firstname.lower() or search_query in account.lastname.lower():
                pass # Return items that match search the search entry

    def search_account(self):
        pass

    def setup_libraries_tab(self):
        ttk.Label(self)

root=tk.Tk()
lb=LibraryGUI(root)
root.mainloop()