import tkinter as tk
from tkinter import *
from tkinter import ttk
import os

from Database import Database
import os

here = os.path.dirname(os.path.abspath(__file__))

books_csv = os.path.join(here, 'books.csv')

accounts_csv = os.path.join(here, 'accounts.csv')

db = Database(books_csv, accounts_csv)
print(db)

class LibraryGUI:
    def __init__(self, root):
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
        self.libraries_section()

    def items_section(self):
        # Items tab creation
        ttk.Label(self.items_frame,text="Library Items",font=("Arial",16)).pack()
        self.item_notebook=ttk.Notebook(self.items_frame)
        self.item_notebook.pack(expand=True,fill="both")

        self.book_frame=ttk.Frame(self.item_notebook)
        self.magazine_frame=ttk.Frame(self.item_notebook)

        self.item_notebook.add(self.book_frame,text="Books")
        self.item_notebook.add(self.magazine_frame,text="Magazines")
        
        # Books
        self.book_tree=ttk.Treeview(self.book_frame,columns=("ISBN","Title","Author","Publisher","Library"),show="headings")
        self.book_tree.heading("ISBN",text="ISBN")
        self.book_tree.heading("Title",text="Title")
        self.book_tree.heading("Author",text="Author")
        self.book_tree.heading("Publisher",text="Publisher")
        self.book_tree.heading("Library",text="Library")
        self.book_tree.pack(fill="both",expand=True)
        
        for library in db.libraries:
            for book in db.books:
                if hasattr(book,"ISBN"): # This is to check if the item is a book
                    self.book_tree.insert("","end",values=(book.ISBN,book.title,book.author,book.author,library.location)) # Returns available Books

            # Search for Books
        search_frame_books=ttk.Frame(self.book_frame)
        search_frame_books.pack(pady=10)

        ttk.Label(search_frame_books,text="Search By:").grid(row=0,column=0,padx=5,pady=5)
        self.book_search_attr=tk.StringVar()
        book_search_attrs=["title","author","publisher","ISBN","library"]
        book_search_dropdown=ttk.Combobox(search_frame_books,textvariable=self.book_search_attr,values=book_search_attrs)
        book_search_dropdown.grid(row=0,column=1,padx=5,pady=5)

        ttk.Label(search_frame_books,text="Keyword:").grid(row=0,column=2,padx=5,pady=5)
        self.book_search_entry=ttk.Entry(search_frame_books,width=30)
        self.book_search_entry.grid(row=0,column=3,padx=5,pady=5)

        book_search_button=ttk.Button(search_frame_books,text="Search",command=lambda: self.search_items("book"))
        book_search_button.grid(row=0,column=4,padx=5,pady=5)

        self.book_search_tree=ttk.Treeview(self.book_frame,columns=("Title","Author","Publisher","ISBN","Status","Library"),show="headings")
        self.book_search_tree.heading("Title", text="Title")
        self.book_search_tree.heading("Author", text="Author")
        self.book_search_tree.heading("Publisher", text="Publisher")
        self.book_search_tree.heading("ISBN", text="ISBN")
        self.book_search_tree.heading("Status", text="Status")
        self.book_search_tree.heading("Library", text="Library")
        self.book_search_tree.pack(padx=10,pady=10,expand=True,fill="both")
        
        # Magazines
        self.magazine_tree=ttk.Treeview(self.magazine_frame,columns=("Title","Publisher","Issue Number","Library"),show="headings")
        self.magazine_tree.heading("Title",text="Title")
        self.magazine_tree.heading("Publisher",text="Publisher")
        self.magazine_tree.heading("Issue Number",text="Issue Number")
        self.magazine_tree.heading("Library",text="Library")
        self.magazine_tree.pack(fill="both",expand=True)
        
        for library in db.libraries:
            for item in db.books:
                if hasattr(item,"issue_num"): # This is to check if the item is a magazine
                    self.magazine_tree.insert("","end",values=(item.title,item.publisher,item.issue_num,library.location)) # Return available Magazines

            # Search for Magazines
        search_frame_magazines=ttk.Frame(self.magazine_frame)
        search_frame_magazines.pack(pady=10)

        ttk.Label(search_frame_magazines,text="Search By:").grid(row=0,column=0,padx=5,pady=5)
        self.magazine_search_attr=tk.StringVar()
        magazine_search_attrs=["title","publisher","issue_num"]
        magazine_search_dropdown=ttk.Combobox(search_frame_magazines,textvariable=self.magazine_search_attr,values=magazine_search_attrs)
        magazine_search_dropdown.grid(row=0,column=1,padx=5,pady=5)

        ttk.Label(search_frame_magazines,text="Keyword:").grid(row=0,column=2,padx=5, pady=5)
        self.magazine_search_entry=ttk.Entry(search_frame_magazines, width=30)
        self.magazine_search_entry.grid(row=0,column=3,padx=5,pady=5)

        magazine_search_button=ttk.Button(search_frame_magazines,text="Search",command=lambda: self.search_items("magazine"))
        magazine_search_button.grid(row=0,column=4,padx=5,pady=5)

        self.magazine_search_tree=ttk.Treeview(self.magazine_frame,columns=("Title","Publisher","Issue Number","Status","Library"),show="headings")
        self.magazine_search_tree.heading("Title",text="Title")
        self.magazine_search_tree.heading("Publisher",text="Publisher")
        self.magazine_search_tree.heading("Issue Number",text="Issue Number")
        self.magazine_search_tree.heading("Status",text="Status")
        self.magazine_search_tree.heading("Library",text="Library")
        self.magazine_search_tree.pack(padx=10,pady=10,expand=True,fill="both")

    def accounts_section(self):
        ttk.Label(self.accounts_frame,text="Search Account",font=("Arial",16)).pack()

        # Search for Accounts
        search_frame=ttk.Frame(self.accounts_frame)
        search_frame.pack(pady=10)
        self.account_search_entry=ttk.Entry(search_frame)
        self.account_search_entry.pack(side="left",padx=5)
        ttk.Button(search_frame,text="Search",command=self.search_account).pack(side="left")

        self.accounts_list=tk.Listbox(self.accounts_frame)
        self.accounts_list.pack(fill="both",expand=True)

    def libraries_section(self):
        ttk.Label(self.library_frame,text="Libraries", font=("Arial",16)).pack()

        self.libraries_tree=ttk.Treeview(self.library_frame, columns=("Location","Number of Books"),show="headings")
        self.libraries_tree.heading("Location",text="Location")
        self.libraries_tree.heading("Number of Books",text="Number of Books")
        self.libraries_tree.pack(fill="both",expand=True)

        for library in db.libraries:
            self.libraries_tree.insert("","end",values=(library.location,len(library.books))) # Return available libraries

    def search_items(self,item_type):
        if item_type=="book":
            search_tree=self.book_search_tree
            search_attr=self.book_search_attr.get()
            keyword=self.book_search_entry.get()
        else:
            search_tree=self.magazine_search_tree
            search_attr=self.magazine_search_attr.get()
            keyword=self.magazine_search_entry.get()

        # Clear previous search results
        for i in search_tree.get_children():
            search_tree.delete(i)

        # Perform search
        results=db.books_search(keyword,search_attr)
        
        for item in results:
            library_location = "Unknown"
            for library in db.libraries:
                if item in library.books:
                    library_location = library.location
                    break
            if (item_type=="book" and hasattr(item,"ISBN")) or (item_type=="magazine" and hasattr(item,"issue_num")):
                title=item.title
                if item_type=="book":
                    second_column=item.author 
                    third_column=item.publisher 
                    id_column=item.ISBN 
                else: 
                    second_column=item.publisher
                    third_column="Magazine"
                    id_column=item.issue_num
                if item.is_status():
                    item_status="Checked In"
                else:
                    item_status="Checked Out"

                search_tree.insert("","end",values=(title,second_column,third_column,id_column,item_status,library_location)) # Returns searched, available items
    def search_account(self):
        self.accounts_list.delete(0, tk.END) # Clear old results
        keyword = self.account_search_entry.get().lower()

        for account in db.accounts: # Search through accounts
            if (keyword in str(account.ID).lower() or keyword in account.get_first_name().lower() or keyword in account.get_last_name().lower()):
                account_info = f"ID: {account.ID}, Name: {account.get_first_name()} {account.get_last_name()}"
                self.accounts_list.insert(tk.END, account_info) # Return each account one by one

root=tk.Tk()
lb=LibraryGUI(root)
root.mainloop()