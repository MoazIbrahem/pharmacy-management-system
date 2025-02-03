# Pharmacy Management System

## Overview

The Pharmacy Management System is a software application designed to manage pharmacy-related activities, including inventory management, sales processing, and user authentication. This system is built using Python and utilizes the Tkinter and CustomTkinter libraries for its graphical user interface (GUI).

## Features

- **User Authentication**: Different access levels for Admin, Doctor, and Staff.
- **Inventory Management**: Keep track of medicines and stock levels.
- **Sales Processing**: Manage customer sales and generate invoices.
- **User-Friendly Interface**: Built with Tkinter and CustomTkinter.

## User Credentials

### Admin:

- **Username**: moaz
- **Password**: 1234

### Doctor:

- **Username**: mohamed
- **Password**: 1234

### Staff:

- **Username**: ahmed
- **Password**: 1234

## Libraries Used

- **Tkinter**: Standard Python library for building GUI applications.
- **CustomTkinter**: A modernized version of Tkinter that provides additional styling and UI enhancements.

## Installation

1. Ensure Python is installed on your system.

2. Install the required libraries:

   ```bash
   pip install tkinter customtkinter
   ```

3. Save the `login.py` file.

4. Open a terminal or command prompt and navigate to the directory where `login.py` is saved.

5. Run the script using:

   ```bash
   python login.py
   ```

6. The login interface will launch where you can enter the credentials provided below.

## Notes

- To update the body of the display screen, modify the screen width and height percentages in `login.py` at lines 23 and 24 according to your screen size.
- You may have problems with the database file path and image paths.

## Usage

- Log in using the provided credentials.
- Access different functionalities based on the user role.
- Manage inventory, process sales, and maintain records efficiently.
