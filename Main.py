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

        self.current_user=None # Initialize the current user

        self.main_frame=ttk.Frame(root)
        
        self.notebook=ttk.Notebook(self.main_frame)
        self.notebook.pack(expand=True,fill="both")
        
        self.login_frame=ttk.Frame(root) # Login frame
        self.login_frame.pack(expand=True, fill="both")

        self.items_frame=ttk.Frame(self.notebook)
        self.my_account_frame=ttk.Frame(self.notebook)
        self.library_frame=ttk.Frame(self.notebook)

        self.notebook.add(self.items_frame,text="Items")
        self.notebook.add(self.my_account_frame,text="My Account")
        self.notebook.add(self.library_frame,text="Libraries")

        self.items_section()
        self.libraries_section()
        
        self.login_screen()

    def login_screen(self):
        ttk.Label(self.login_frame,text="Library Management System Login",font=("Arial", 16)).pack(pady=20)
        login_form=ttk.Frame(self.login_frame)
        login_form.pack(pady=20)

        ttk.Label(login_form,text="User ID:").grid(row=0,column=0,padx=5,pady=5,sticky="e")
        self.login_id_entry=ttk.Entry(login_form,width=30)
        self.login_id_entry.grid(row=0,column=1,padx=5,pady=5)

        ttk.Button(login_form,text="Sign In",command=self.login).grid(row=1,column=0,columnspan=2,pady=10) # Normal user access
        
        ttk.Button(login_form,text="Create Account",command=self.create_account).grid(row=2,column=0,columnspan=2,pady=5) # Create new account
        
        ttk.Button(login_form,text="Continue as Guest",command=self.guest_login).grid(row=3,column=0,columnspan=2,pady=5) # Guest access


    def login(self):
        login_id=self.login_id_entry.get().strip()
        if login_id:
            matching_login=None
            for account in db.accounts:
                if str(account.ID)==login_id:
                    matching_login=account
                    break
            
            if matching_login:
                self.current_user=matching_login
                # Notify that the login was successful
                print(f"login success {matching_login.get_first_name()} {matching_login.get_last_name()}")
                self.login_frame.pack_forget()
                self.my_account_section()
                self.main_frame.pack(expand=True,fill="both")
            else:
                # Show error that id isnt found
                print("error id not found")
                pass
        else:
            # Show error
            print("error")

    def create_account(self):
        # Implement account creation function here
        pass

    def guest_login(self):
        self.current_user=None
        self.login_frame.pack_forget()
        self.main_frame.pack(expand=True,fill="both")
        self.my_account_section()

    def logout(self):
        self.current_user=None
        self.main_frame.pack_forget()
        self.login_id_entry.delete(0,END)
        self.login_frame.pack(expand=True,fill="both")

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

    def my_account_section(self):
        for i in self.my_account_frame.winfo_children():
            i.destroy()
        
        if self.current_user:
            ttk.Label(self.my_account_frame, text=f"{self.current_user.get_first_name()} {self.current_user.get_last_name()}",font=("Arial", 16)).pack(pady=10)
            ttk.Label(self.my_account_frame, text=f"Account ID: {self.current_user.ID}").pack()

            ttk.Button(self.my_account_frame, text="Logout", command=self.logout).pack(pady=10)

            ttk.Label(self.my_account_frame, text="My Checked Out Items", font=("Arial", 14)).pack(pady=10)

            self.my_checked_out_books_tree=ttk.Treeview(self.my_account_frame,columns=("Title","Type","Due Date","Status"),show="headings")
            self.my_checked_out_books_tree.heading("Title", text="Title")
            self.my_checked_out_books_tree.heading("Type", text="Type")
            self.my_checked_out_books_tree.heading("Due Date", text="Due Date")
            self.my_checked_out_books_tree.heading("Status", text="Status")
            self.my_checked_out_books_tree.pack(fill="both", expand=True, padx=10, pady=10)

            # ttk.Button(self.my_account_frame,text="Return Selected Item",command=self.return_selected_item).pack(pady=10)
            # Need to add function that returns the selected item (return_selected_item())

            self.refresh_my_checked_out_books() # Puts the user's checked out books in list
        else:
            ttk.Label(self.my_account_frame,text="Guest Mode",font=("Arial",16)).pack(pady=20)
            ttk.Label(self.my_account_frame,text="Please sign in to access your account").pack()
            ttk.Button(self.my_account_frame,text="Sign In",command=self.logout).pack(pady=20)

    def refresh_my_checked_out_books(self):
        if self.current_user and hasattr(self,"my_books_tree"):
            for item in self.my_checked_out_books_tree.get_children():
                self.my_checked_out_books_tree.delete(item)
                
            if not self.current_user.books:
                return

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