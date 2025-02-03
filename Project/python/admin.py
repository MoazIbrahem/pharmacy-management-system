from tkinter import *
from PIL import Image, ImageTk
from customtkinter import *
import login
import billing
import staff
import inventory
from medicine_data import fetchall_expiry_date
import Report
import expir_medications
from Request_Table import get_null_View
import  pharmacist_gui

# Initialize the main window
def admin_window(information,root):
    # =======================================================================================================
    # Function to handle login backend
    def go_home():
        # Clear the right side and display the initial home page layout again
        for widget in root.grid_slaves(row=0, column=1):
            widget.destroy()

        # Add a background image on the right (initial state)
        bg_image = Image.open(r"Project\image\medical-composition-with-pills.jpg")
        bg_image = bg_image.resize(
            (850, 500), Image.Resampling.LANCZOS
        )  # Adjust the size of the image
        bg_photo = ImageTk.PhotoImage(bg_image)

        # Preserve the reference to the image so it doesn't get garbage collected
        bg_label = Label(root, image=bg_photo)
        bg_label.image = bg_photo  # Important step to retain the reference to the image
        bg_label.grid(row=0, column=1, sticky="nsew")  # Stretches to fill the space

    def show_billing_page():
        # Clear the right side and show the billing content
        for widget in root.grid_slaves(row=0, column=1):
            widget.destroy()
        # Call the billing function or frame to display the billing page content
        billing_frame = billing.billing(
            root, information[3]
        )  # Assuming this returns the billing UI
        billing_frame.grid(row=0, column=1, sticky="nsew")

    def show_staff_page():
        # Clear the right side and show the staff management content
        for widget in root.grid_slaves(row=0, column=1):
            widget.destroy()
        # Call the staff_window function to display the staff management UI
        staff_frame = staff.staff_window(
            root
        )  # Assuming this returns the staff management UI
        staff_frame.grid(row=0, column=1, sticky="nsew")

    def show_inventory_page():
        # Clear the right side and show the staff management content
        for widget in root.grid_slaves(row=0, column=1):
            widget.destroy()
        # Call the show_inventory_page function to display the inventory management UI
        inventory_frame = inventory.inentory_window(
            root
        )  # Assuming this returns the staff management UI
        inventory_frame.grid(row=0, column=1, sticky="nsew")

    def show_Repotr_page():
        # Clear the right side and show the Repotr content
        for widget in root.grid_slaves(row=0, column=1):
            widget.destroy()
        # Call the show_Repotr_page function to display Repotr management UI
        inventory_frame = Report.Report_window(
            root
        )  # Assuming this returns the Repotr management UI
        inventory_frame.grid(row=0, column=1, sticky="nsew")

    def show_requist():
              # Clear the right side and show the requist content
        for widget in root.grid_slaves(row=0, column=1):
            widget.destroy()
        btn_r.configure(bg="#80C7E7")
        inventory_frame = pharmacist_gui.request_window(
            root
        )  # Assuming this returns the requist management UI
        inventory_frame.grid(row=0, column=1, sticky="nsew")

    def show_ex_page():
        # Clear the right side and show the ex_page content
        for widget in root.grid_slaves(row=0, column=1):
            widget.destroy()
        btn5.configure(bg="#80C7E7")
        inventory_frame = expir_medications.ex_window(
            root
        )  # Assuming this returns the ex_page management UI
        inventory_frame.grid(row=0, column=1, sticky="nsew")

    def logout():
        """
        this function destroy the old window and display new window wiht the small size
        """
        for widget in root.grid_slaves():
            widget.destroy()
        root.title("Login Page")
        root.config(bg="white")
        root.geometry("850x500")
        root.resizable(False, False)
        # Center the window on the screen
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        x_position = (screen_width // 2) - (850 // 2)
        y_position = (screen_height // 2) - (500 // 2)
        root.geometry(f"850x500+{x_position}+{y_position}")
        login.login(root)# go to the login page

    # =======================================================================================================

    # Configure the grid layout for the root window
    root.grid_rowconfigure(0, weight=1)  # Allow row 0 to expand
    root.grid_columnconfigure(0, weight=0)  # Fix column 0 (frame column)
    root.grid_columnconfigure(1, weight=1)  # Allow column 1 (image) to expand

    # Add a frame on the left
    frame1 = CTkFrame(root, fg_color="#D9D9D9", corner_radius=20)
    frame1.grid(row=0, column=0, padx=10,sticky="ns")

    # Add a background image on the right
    bg_image = Image.open(r"Project\image\medical-composition-with-pills.jpg")
    bg_image = bg_image.resize((850, 500), Image.Resampling.LANCZOS)
    bg_photo = ImageTk.PhotoImage(bg_image)

    bg_label = Label(root, image=bg_photo)
    bg_label.image = bg_photo
    bg_label.grid(row=0, column=1, sticky="nsew")


    data_display = LabelFrame(
        frame1,
        text="User Data",
        font=("Arial", 14),
        bg="#f5f5f5",
        fg="black",
        labelanchor="n",
    )  # Centered title
    data_display.pack(pady=20, padx=10, fill="x")

    # Add a Label inside the LabelFrame for user data
    user_data_label = Label(
        data_display,
        text=f"Name: {information[2]}\nID: {information[3]} \nUsername: {information[0]}\nStatus: Active",
        font=("Arial", 12),
        bg="white",
        justify="left",
        anchor="nw",
    )
    user_data_label.pack(
        pady=10,
        padx=10,
        fill="both",
        expand=True,
    )
    
    # Add "Home Page" button to go back to the home screen
    btn_home = Button(
        frame1,
        text="Home Page",
        font=("Arial", 16),
        bg="#4CAF50",
        width=25,
        relief="flat",
        command=go_home,
    )
    btn_home.pack(pady=8)

    # Add buttons to the large frame with coordinated colors
    btn1 = Button(
        frame1,
        text="Billing",
        font=("Arial", 16),
        bg="#80C7E7",
        width=25,
        relief="flat",
        command=show_billing_page,  # Replace the background with billing page
    )
    btn1.pack(pady=8)
    btn2 = Button(
        frame1,
        text="Staff Management",
        font=("Arial", 16),
        bg="#80C7E7",
        width=25,
        relief="flat",
        command=show_staff_page,
    )
    btn2.pack(pady=8)
    
    btn3 = Button(
        frame1,
        text="Inventory Management",
        font=("Arial", 16),
        bg="#80C7E7",
        width=25,
        relief="flat",
        command=show_inventory_page,
    )

    btn3.pack(pady=8)
    btn5 = Button(
        frame1,
        text="Expire medication",
        font=("Arial", 16),
        bg="#80C7E7",
        width=25,
        relief="flat",
        command=show_ex_page
    )
    btn5.pack(pady=8)
    if fetchall_expiry_date():
      btn5.configure(bg="red") 
    # Add "Requsts" button
    btn_r = Button(
        frame1,
        text="Requsts",
        font=("Arial", 16),
        bg="#80C7E7",
        width=25,
        relief="flat",
        command=show_requist
    )
    btn_r.pack(pady=8)
    if get_null_View():
      btn_r.configure(bg="red")
    # Add "Expire medication" button with a different color to highlight it


    btnre = Button(
        frame1,
        text="Report",
        font=("Arial", 16),
        bg="#80C7E7",
        width=25,
        relief="flat",
        command=show_Repotr_page
    )
    btnre.pack(pady=8)

    # Add "Log Out" button with red color
    btn_logout = Button(
        frame1,
        text="Log Out",
        font=("Arial", 16),
        bg="#F44336",
        width=25,
        relief="flat",
        command=logout,
    )
    btn_logout.pack(pady=8)

    # Run the application
    return root

