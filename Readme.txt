Library Management System

Overview
  A Library Management System that allows users to browse, search, and check out books and magazines from multiple library locations. It features different access groups for regular users, guests, and administrators. It uses a tkinter graphical user interface. 

  User Management
    - User Authentication: Sign in with a unique ID
    - Guest Access: Browse items without signing in
    - Account Creation: New users can create accounts
    - Admin Panel: Special access for librarians to add new items
  
  Item Management
    - Books and Magazines: View, search, and manage both types of items
    - Advanced Search: Search by title, author, publisher, ISBN/ISSN, or library location
    - Check Out/Return: Users can check out and return items
    - Due Dates: Automatic tracking of due dates for borrowed items
  
  Library Management
    - Multiple Libraries: Support for multiple library locations
    - Inventory Tracking: See how many books and magazines are at each location

Installation
  1. Clone the repository:
  git clone https://github.com/yourusername/library-management-system.git
  2. Navigate to the projects directory:
  cd library-management-system
  3. Run the Application:
  python Main.py

How to use

  Regular User
    1. Log in with your user ID or create a new account
    2. Browse or search for books and magazines
    3. Check out items by selecting them and clicking "Check Out"
    4. View your checked out items in the "My Account" tab
    5. Return items when finished

  Guest User
    1. Click "Continue as Guest"
    2. Browse or search for items (Note: Guests cannot check out items)

  Administrator
    1. Log in with the admin ID (default: 100982527)
    2. Access the "Admin Panel" tab
    3. Add new books or magazines to the system
    4. Specify which library location to add items to

  Data Storage
    The application saves all changes to CSV files when closed properly. Data is stored in the following format:
    - Books: ISBN, title, author, publisher, status
    - Magazines: ISSN, title, publisher, issue number, status
    - Libraries: Location, books list, magazines list
    - Accounts: ID, name, checked-out items
