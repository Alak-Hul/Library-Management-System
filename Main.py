import tkinter as tk
from tkinter import *
from tkinter import ttk
import os

from Database import Database
import os

here = os.path.dirname(os.path.abspath(__file__))

books_pkl = os.path.join(here, 'books.pkl')
magazine_pkl = os.path.join(here, 'magazines.pkl')
libraries_pkl = os.path.join(here, 'libraries.pkl')
accounts_pkl = os.path.join(here, 'accounts.pkl')

db = Database(books_pkl, magazine_pkl, libraries_pkl, accounts_pkl)
print(db)
db.load_data()
print(db)

class LibraryGUI:
    def __init__(self, root, admin_id=100982527): # Default admin ID is 100982527, Kurtis Stubbe
        self.root=root
        self.root.title("Library Management System")
        self.root.geometry("1280x720")

        self.admin_id = admin_id

        self.current_user=None # Initialize the current user

        self.main_frame=ttk.Frame(root)
        
        self.notebook=ttk.Notebook(self.main_frame)
        self.notebook.pack(expand=True,fill="both")
        
        self.login_frame=ttk.Frame(root) # Login frame

        self.account_creation_frame=ttk.Frame(root)


        self.items_frame=ttk.Frame(self.notebook)
        self.my_account_frame=ttk.Frame(self.notebook)
        self.library_frame=ttk.Frame(self.notebook)
        
        self.admin_frame = ttk.Frame(self.notebook)

        self.notebook.add(self.items_frame,text="Items")
        self.notebook.add(self.my_account_frame,text="My Account")
        self.notebook.add(self.library_frame,text="Libraries")

        self.items_section()
        self.libraries_section()
        self.admin_section()

        self.login_screen()

    def login_screen(self):
        if hasattr(self, 'login_frame'):  # for the back function of account_creation
            self.login_frame.destroy()  # Destroy the old frame if it exists

        self.login_frame = ttk.Frame(self.root)  # Recreate the frame
        self.login_frame.pack(expand=True, fill="both")

        self.login_frame.pack(expand=True, fill="both")
        ttk.Label(self.login_frame,text="Library Management System Login",font=("Arial", 16)).pack(pady=20)
        login_form=ttk.Frame(self.login_frame)
        login_form.pack(pady=20)

        ttk.Label(login_form,text="User ID:").grid(row=0,column=0,padx=5,pady=5,sticky="e")
        self.login_id_entry=ttk.Entry(login_form,width=30)
        self.login_id_entry.grid(row=0,column=1,padx=5,pady=5)

        ttk.Button(login_form,text="Sign In",command= lambda: self.login(self.login_id_entry.get().strip())).grid(row=1,column=0,columnspan=2,pady=10) # Normal user access
        
        ttk.Button(login_form,text="Create Account",command=self.account_creation).grid(row=2,column=0,columnspan=2,pady=5) # Create new account
        
        ttk.Button(login_form,text="Continue as Guest",command=self.guest_login).grid(row=3,column=0,columnspan=2,pady=5) # Guest access

    def login(self, login_id):
        if login_id:
            matching_login=None
            for account in db.accounts:
                if str(account.get_ID())==login_id:
                    matching_login=account
                    break
            
            if matching_login:
                self.current_user=matching_login
                # Notify that the login was successful
                print(f"login success {matching_login.get_first_name()} {matching_login.get_last_name()}")
                self.login_frame.pack_forget()
                self.my_account_section()
                self.toggle_admin_tab()
                self.main_frame.pack(expand=True,fill="both")
            else:
                # Show error that id isnt found
                print("error id not found")
        else:
            # Show error
            print("error")
    
    def toggle_admin_tab(self):
        admin_tab_exists=False
        for i in range(self.notebook.index("end")):
            if self.notebook.tab(i,"text")==("Admin Panel"): # This is to check if the admin page already exists
                admin_tab_exists=True
                break
        
        is_admin=(self.current_user.get_ID()==str(self.admin_id)) # Check if current user is admin - True if yes, False if not
        if is_admin and not admin_tab_exists:
            self.notebook.add(self.admin_frame,text="Admin Panel") # Adds admin page if the user is an admin
        elif not is_admin and admin_tab_exists:
            for i in range(self.notebook.index("end")): # Removes admin page if the user is not admin and the admin tab already created
                if self.notebook.tab(i,"text")=="Admin Panel":
                    self.notebook.forget(i)
                    break

    def account_back(self): #honestly I hate this, but it works so who cares
        self.account_creation_frame.pack_forget()
        self.account_creation_frame.destroy()
        self.account_creation_frame=ttk.Frame(root) 
        self.login_screen()

    def account_generate(self, name, id):
        if name and id:
            self.account_creation_frame.pack_forget()
            self.account_creation_frame.destroy()
            self.account_creation_frame=ttk.Frame(root) 
            db.create_account(name, id)
            self.login(id)
        else: 
            ttk.Label(self.account_creation_frame, text="Invaild Name, or ID",font=("Arial", 16)).pack(pady=20)

    def account_creation(self):
        self.login_frame.pack_forget()
        self.account_creation_frame.pack(expand=True, fill="both")
        ttk.Label(self.account_creation_frame, text="Library Management System Account Creation",font=("Arial", 16)).pack(pady=20)
        account_creation_form = ttk.Frame(self.account_creation_frame)
        account_creation_form.pack(pady=20)

        ttk.Label(account_creation_form,text="Full Name(First and Last):").grid(row=0,column=0,padx=5,pady=5,sticky="e")
        account_full_name_entry = ttk.Entry(account_creation_form, width=30)
        account_full_name_entry.grid(row=0,column=1,padx=5,pady=5)


        ttk.Label(account_creation_form,text="Student ID:").grid(row=1,column=0,padx=5,pady=5,sticky="e")
        account_ID_entry = ttk.Entry(account_creation_form, width=30)
        account_ID_entry.grid(row=1,column=1,padx=5,pady=5)
        

        ttk.Button(account_creation_form, text="Submit", command=lambda: self.account_generate(account_full_name_entry.get().strip(), account_ID_entry.get().strip())).grid(row=2,column=0,columnspan=2,pady=10)
        ttk.Button(account_creation_form,text="Back",command=self.account_back).grid(row=3,column=0,columnspan=2,pady=10)

    def guest_login(self):
        self.current_user=None
        self.login_frame.pack_forget()
        self.main_frame.pack(expand=True,fill="both")
        self.my_account_section()

        self.toggle_admin_tab()

    def logout(self):
        self.current_user=None
        self.main_frame.pack_forget()
        self.login_id_entry.delete(0,END)
        self.login_frame.pack(expand=True,fill="both")
        
        self.toggle_admin_tab()

    def admin_section(self):
        ttk.Label(self.admin_frame,text="Admin Panel",font=("Arial",16)).pack(pady=10)
        
        admin_notebook=ttk.Notebook(self.admin_frame)
        admin_notebook.pack(expand=True,fill="both",padx=10,pady=10)
        add_book_frame=ttk.Frame(admin_notebook)
        add_magazine_frame=ttk.Frame(admin_notebook)
        
        # Books
        admin_notebook.add(add_book_frame,text="Add Book")
        admin_notebook.add(add_magazine_frame,text="Add Magazine")
        
        ttk.Label(add_book_frame,text="Add New Book",font=("Arial",14)).pack(pady=10)
        
        book_form=ttk.Frame(add_book_frame)
        book_form.pack(pady=10)
        
        ttk.Label(book_form,text="Title:").grid(row=0,column=0,padx=5,pady=5,sticky="e")
        self.book_title_entry=ttk.Entry(book_form,width=30)
        self.book_title_entry.grid(row=0,column=1,padx=5,pady=5)
    
        ttk.Label(book_form,text="Author:").grid(row=1,column=0,padx=5,pady=5,sticky="e")
        self.book_author_entry=ttk.Entry(book_form,width=30)
        self.book_author_entry.grid(row=1,column=1,padx=5,pady=5)
        
        ttk.Label(book_form,text="Publisher:").grid(row=2,column=0,padx=5,pady=5,sticky="e")
        self.book_publisher_entry=ttk.Entry(book_form,width=30)
        self.book_publisher_entry.grid(row=2,column=1,padx=5,pady=5)
        
        # Library selection for book
        ttk.Label(book_form,text="Library Location:").grid(row=3,column=0,padx=5,pady=5,sticky="e")
        self.book_library_var=tk.StringVar()
        library_locations=[lib.location for lib in db.libraries]
        self.book_library_dropdown=ttk.Combobox(book_form,textvariable=self.book_library_var,values=library_locations)
        self.book_library_dropdown.grid(row=3,column=1,padx=5,pady=5)
        if library_locations:
            self.book_library_dropdown.current(0)
        ttk.Button(book_form, text="Add Book", command=self.add_new_book).grid(row=4, column=0, columnspan=2, pady=10)
        
        self.book_status_label=ttk.Label(add_book_frame,text="") # Status label for when adding books
        self.book_status_label.pack(pady=10)
        
        # Magazines
        ttk.Label(add_magazine_frame,text="Add New Magazine",font=("Arial",14)).pack(pady=10)
        
        magazine_form = ttk.Frame(add_magazine_frame)
        magazine_form.pack(pady=10)
        
        ttk.Label(magazine_form, text="Title:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.magazine_title_entry = ttk.Entry(magazine_form, width=30)
        self.magazine_title_entry.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(magazine_form, text="Publisher:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.magazine_publisher_entry = ttk.Entry(magazine_form, width=30)
        self.magazine_publisher_entry.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(magazine_form, text="Issue Number:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.magazine_issue_entry = ttk.Entry(magazine_form, width=30)
        self.magazine_issue_entry.grid(row=2, column=1, padx=5, pady=5)
        
        # Library selection for magazine
        ttk.Label(magazine_form, text="Library Location:").grid(row=3, column=0, padx=5, pady=5, sticky="e")
        self.magazine_library_var = tk.StringVar()
        self.magazine_library_dropdown = ttk.Combobox(magazine_form, textvariable=self.magazine_library_var, values=library_locations)
        self.magazine_library_dropdown.grid(row=3, column=1, padx=5, pady=5)
        if library_locations:
            self.magazine_library_dropdown.current(0)
        ttk.Button(magazine_form, text="Add Magazine", command=self.add_new_magazine).grid(row=4, column=0, columnspan=2, pady=10)
        
        self.magazine_status_label = ttk.Label(add_magazine_frame, text="")
        self.magazine_status_label.pack(pady=10)
        
        # Admin info section
        admin_info_frame = ttk.LabelFrame(self.admin_frame, text="Admin Information")
        admin_info_frame.pack(fill="x", padx=10, pady=10, side="bottom")
        
        ttk.Label(admin_info_frame, text=f"Current Admin ID: {self.admin_id}").pack(pady=5)

    def add_new_book(self):
        title = self.book_title_entry.get().strip()
        author = self.book_author_entry.get().strip()
        publisher = self.book_publisher_entry.get().strip()
        library_location = self.book_library_var.get()

        print(f'{author = }, {publisher = }')
        
        if not (title and author and publisher and library_location):
            self.book_status_label.config(text="Please fill in all the fields.")
            return
        
        db.create_book(title, author, publisher, library_location) # Create the new book
        
        self.book_status_label.config(text=f"Book '{title}' added successfully!")
        self.book_title_entry.delete(0, END) # Clears entry boxes
        self.book_author_entry.delete(0, END) #
        self.book_publisher_entry.delete(0, END) #
        
        self.refresh_book_tree() # Refresh book tree now that a new book is added

    def add_new_magazine(self):
        title = self.magazine_title_entry.get().strip()
        publisher = self.magazine_publisher_entry.get().strip()
        issue_num = self.magazine_issue_entry.get().strip()
        library_location = self.magazine_library_var.get()
        
        if not (title and publisher and issue_num and library_location):
            self.magazine_status_label.config(text="Please fill in all fields")
            return
        
        try:
            issue_num = int(issue_num)
        except ValueError:
            self.magazine_status_label.config(text="Issue Number must be a number")
            return
        
        db.create_magazine(title, publisher, issue_num, library_location) # Create the new magazine

        self.magazine_status_label.config(text=f"Magazine '{title}' added successfully!")
        self.magazine_title_entry.delete(0, END) # Clears entry boxes
        self.magazine_publisher_entry.delete(0, END) #
        self.magazine_issue_entry.delete(0, END) #
        
        self.refresh_magazine_tree() # Refresh book tree now that a new magazine is added

    def refresh_book_tree(self):
        for item in self.book_tree.get_children(): # Clear old list
            self.book_tree.delete(item)
        
        for library in db.libraries: # Refreshes the book tree
            for book in library.books:
                if hasattr(book, "_ISBN"): # This is to check if the item is a book
                    self.book_tree.insert("", "end", values=(book.get_ISBN(), book.title, book.author, book.publisher, library.location))

    def refresh_magazine_tree(self):
        for item in self.magazine_tree.get_children(): # Clear old list
            self.magazine_tree.delete(item)
        
        for library in db.libraries: # Refreshes the book tree
            for magazine in library.magazines:
                    self.magazine_tree.insert("", "end", values=(magazine.title, magazine.publisher, magazine.issue_num, library.location))
 
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
            for book in library.books:
                self.book_tree.insert("","end",values=(book.get_ISBN(),book.title,book.author,book.publisher,library.location)) # Returns available Books

            # Search for Books
        search_frame_books=ttk.Frame(self.book_frame)
        search_frame_books.pack(pady=10)

        ttk.Label(search_frame_books,text="Search By:").grid(row=0,column=0,padx=5,pady=5)
        self.book_search_attr=tk.StringVar()
        book_search_attrs=["Title","Author","Publisher","ISBN","Library"]
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

        book_checkout_button=ttk.Button(self.book_frame,text="Check Out Selected Book",command=lambda:self.check_out_item("book"))
        book_checkout_button.pack(pady=5)
        
        # Magazines
        self.magazine_tree=ttk.Treeview(self.magazine_frame,columns=("Title","Publisher","Issue Number","Library"),show="headings")
        self.magazine_tree.heading("Title",text="Title")
        self.magazine_tree.heading("Publisher",text="Publisher")
        self.magazine_tree.heading("Issue Number",text="Issue Number")
        self.magazine_tree.heading("Library",text="Library")
        self.magazine_tree.pack(fill="both",expand=True)
        
        for library in db.libraries:
            for magazine in library.magazines:
                self.magazine_tree.insert("","end",values=(magazine.title,magazine.publisher,magazine.issue_num,library.location)) # Return available Magazines

            # Search for Magazines
        search_frame_magazines=ttk.Frame(self.magazine_frame)
        search_frame_magazines.pack(pady=10)

        ttk.Label(search_frame_magazines,text="Search By:").grid(row=0,column=0,padx=5,pady=5)
        self.magazine_search_attr=tk.StringVar()
        magazine_search_attrs=["Title","Publisher","Issue Number", "ISSN"]
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

        magazine_checkout_button=ttk.Button(self.magazine_frame,text="Check Out Selected Magazine",command=lambda:self.check_out_item("magazine"))
        magazine_checkout_button.pack(pady=5)

    def my_account_section(self):
        for i in self.my_account_frame.winfo_children():
            i.destroy()
        
        if self.current_user:
            ttk.Label(self.my_account_frame, text=f"{self.current_user.get_first_name()} {self.current_user.get_last_name()}",font=("Arial", 16)).pack(pady=10)
            ttk.Label(self.my_account_frame, text=f"Account ID: {self.current_user.get_ID()}").pack()

            ttk.Button(self.my_account_frame, text="Logout", command=self.logout).pack(pady=10)

            ttk.Label(self.my_account_frame, text="My Checked Out Items", font=("Arial", 14)).pack(pady=10)

            self.my_checked_out_books_tree=ttk.Treeview(self.my_account_frame,columns=("Title","Type","Due Date","Status"),show="headings")
            self.my_checked_out_books_tree.heading("Title", text="Title")
            self.my_checked_out_books_tree.heading("Type", text="Type")
            self.my_checked_out_books_tree.heading("Due Date", text="Due Date")
            self.my_checked_out_books_tree.heading("Status", text="Status")
            self.my_checked_out_books_tree.pack(fill="both", expand=True, padx=10, pady=10)

            ttk.Button(self.my_account_frame,text="Return Selected Item",command=self.return_selected_item).pack(pady=10)

            self.refresh_my_checked_out_books() # Puts the user's checked out books in list
        else:
            ttk.Label(self.my_account_frame,text="Guest Mode",font=("Arial",16)).pack(pady=20)
            ttk.Label(self.my_account_frame,text="Please sign in to access your account").pack()
            ttk.Button(self.my_account_frame,text="Sign In",command=self.logout).pack(pady=20)

    def check_out_item(self,item_type):
        if not self.current_user:
            # Show error message that user isn't logged in
            return
        selected_item=None
        if item_type=="book": # Check if item is book
            selected_item=self.book_search_tree.selection()
            if not selected_item:
                # Show error message telling user to make a book selection
                return
            
            isbn = self.book_search_tree.item(selected_item[0],'values')[3] # 3 because ISBN is in index 3
            book_to_checkout=None
            for book in db.books:
                if hasattr(book,'_ISBN') and book._ISBN==isbn:
                    book_to_checkout=book
                    break
            
            if not book_to_checkout:
                # Show error saying book isnt found
                return
            
            if not book_to_checkout.is_status(): # Check if the book is already checked out
                # Show error saying the book is already checked out
                return
            
            book_to_checkout.check_in()
            
            if not self.current_user.books:
                self.current_user.books=[]
            
            if book_to_checkout not in self.current_user.books:
                self.current_user.books.append(book_to_checkout)
        elif item_type=="magazine": # Item must be a magazine
            selected_item=self.magazine_search_tree.selection()
            if not selected_item:
                # Show error message telling user to make a book selection
                return
            
            isbn=self.book_search_tree.item(selected_item[0],'values')[3]
        
        self.refresh_my_checked_out_books()
        # Show success message

    def return_selected_item(self):
        if not self.current_user:
            return
        
        selected_item=self.my_checked_out_books_tree.selection()
        if not selected_item:
            # Show error message telling user to make a book selection
            return
        
        title=self.my_checked_out_books_tree.item(selected_item[0],'values')[0]
        item_type=self.my_checked_out_books_tree.item(selected_item[0],'values')[1]
        
        item_to_return=None 
        
        if item_type.lower()=="book": # Check if item is a book
            if self.current_user.books:
                for book in self.current_user.books:
                    if book.title==title:
                        item_to_return=book
                        book.check_out()
                        self.current_user.books.remove(book) # Remove from user's books
                        break
        else:  # It must be a magazine
            if self.current_user.magazines:
                for magazine in self.current_user.magazines:
                    if magazine.title==title:
                        item_to_return=magazine
                        magazine.check_out()
                        self.current_user.magazines.remove(magazine) # Remove from user's magazines
                        break
        
        if item_to_return:
            # Update UI
            self.refresh_my_checked_out_books()
            # Show success message
        else:
            # Show error message telling the user the book isn't checked out by them
            pass
    
    def refresh_my_checked_out_books(self):
        if self.current_user and hasattr(self,"my_checked_out_books_tree"):
            for item in self.my_checked_out_books_tree.get_children():
                self.my_checked_out_books_tree.delete(item) # Clear current items
            
            if self.current_user.books:
                for book in self.current_user.books:
                    # Get book details
                    title=book.title
                    item_type="Book"

                    due_date=book.due_date()

                    if book.is_status():
                        status="Checked In"
                    else:
                        status="Checked Out" 
                    
                    self.my_checked_out_books_tree.insert("","end",values=(title,item_type, due_date,status))
            
            if self.current_user.magazines:
                for magazines in self.current_user.magazines:
                    # Get Magazine details
                    title=magazines.title
                    item_type="Magazine"
                    due_date=magazines.due_date()
                    if magazines.is_status():
                        status="Checked In"
                    else:
                        status="Checked Out" 
                    
                    self.my_checked_out_books_tree.insert("","end",values=(title,item_type, due_date,status))

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
        elif item_type=="magazine": # just makes it more readable nothing wrong with how you did it 
            search_tree=self.magazine_search_tree
            search_attr=self.magazine_search_attr.get()
            keyword=self.magazine_search_entry.get()

        # Clear previous search results
        for i in search_tree.get_children():
            search_tree.delete(i)

        # Perform search
        book_search_mapping={
            "Title": "title",
            "Author": "author",
            "Publisher": "publisher",
            "ISBN": "_ISBN",
            "Library": "library"
        }
        magazine_search_mapping={
            "Title": "title",
            "Publisher": "publisher",
            "ISSN": "_ISSN",
            "Issue Number": "issue num",
            "Library": "library"
        }

        if item_type == "book":
            results=db.books_search(keyword,book_search_mapping[search_attr]) # This just allows for the options in the drop down to be difference to the ones that get sent to book_search that way they can be capitalized and stuff
        elif item_type == "magazine":
            results=db.magazine_search(keyword,magazine_search_mapping[search_attr])        
        for item in results:
            library_location = "Unknown"
            for library in db.libraries:
                if item in library.books:
                    library_location = library.location
                    break
            if (item_type=="book" and hasattr(item,"_ISBN")) or (item_type=="magazine" and hasattr(item,"issue_num")):
                title=item.title
                if item_type=="book":
                    second_column=item.author 
                    third_column=item.publisher 
                    id_column=item._ISBN 
                if item_type=="magazine": # same here: line 288 
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
            if (keyword in str(account.get_ID()).lower() or keyword in account.get_first_name().lower() or keyword in account.get_last_name().lower()):
                account_info = f"ID: {account.get_ID()}, Name: {account.get_first_name()} {account.get_last_name()}"
                self.accounts_list.insert(tk.END, account_info) # Return each account one by one

def save_to_database():
    db.save_data()
    root.destroy()

root=tk.Tk()
lb=LibraryGUI(root)
# lb=LibraryGUI(root,XXXXXXXXX) Uncomment, and change X accordingly to whichever ID has the ability to create books

root.protocol("WM_DELETE_WINDOW", save_to_database)
root.mainloop()