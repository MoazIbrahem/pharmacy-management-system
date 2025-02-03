from tkinter import *
from PIL import Image, ImageTk
from customtkinter import *
import login
import billing
from medicine_data import fetchall_expiry_date
import expir_medications
from Request_Table import get_null_View
import pharmacist_gui


# Initialize the main window
def pharmacy_window(information, root):
    # =======================================================================================================
    # =======================================================================================================
    # =======================================================================================================
    # Function to handle login backend
    def go_home():
        """
        Clears the right-side content and resets the home page layout with a default image.
        """
        for widget in root.grid_slaves(row=0, column=1):
            widget.destroy()

        # Add a background image on the right (initial state)
        bg_image = Image.open(r"pharmacy-management-system\Project\image\medical-composition-with-pills.jpg")
        bg_image = bg_image.resize(
            (850, 500), Image.Resampling.LANCZOS
        )  # Adjust image size
        bg_photo = ImageTk.PhotoImage(bg_image)

        # Preserve the reference to the image to avoid garbage collection
        bg_label = Label(root, image=bg_photo)
        bg_label.image = bg_photo  # Save reference to avoid collection
        bg_label.grid(row=0, column=1, sticky="nsew")  # Fill space

    def show_billing_page():
        """
        Clears the right-side content and displays the billing page layout.
        """
        for widget in root.grid_slaves(row=0, column=1):
            widget.destroy()

        # Call the billing function to create and display billing page UI
        billing_frame = billing.billing(root, information[3])  # Pass staff ID
        billing_frame.grid(row=0, column=1, sticky="nsew")

    def show_requist():
        """
        Clears the right-side content and displays the requests page layout.
        """
        for widget in root.grid_slaves(row=0, column=1):
            widget.destroy()
        btn_r.configure(bg="#80C7E7")  # Reset button background color
        inventory_frame = pharmacist_gui.request_window(root)  # Requests UI
        inventory_frame.grid(row=0, column=1, sticky="nsew")

    def show_ex_page():
        """
        Clears the right-side content and displays the expired medications page layout.
        """
        for widget in root.grid_slaves(row=0, column=1):
            widget.destroy()
        btn5.configure(bg="#80C7E7")  # Reset button background color
        inventory_frame = expir_medications.ex_window(root)  # Expired medications UI
        inventory_frame.grid(row=0, column=1, sticky="nsew")

    def logout():
        """
        Logs out the user by destroying the current UI, resetting the root window, and loading the login screen.
        """
        for widget in root.grid_slaves():
            widget.destroy()

        # Set login window properties
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

        # Display login screen
        login.login(root)

    # =======================================================================================================
    # =======================================================================================================
    # =======================================================================================================
    # Configure the grid layout for the root window
    root.grid_rowconfigure(0, weight=1)  # Allow row 0 to expand
    root.grid_columnconfigure(0, weight=0)  # Fix column 0 (frame column)
    root.grid_columnconfigure(1, weight=1)  # Allow column 1 (image) to expand

    # Add a frame on the left
    frame1 = CTkFrame(root, fg_color="#D9D9D9", corner_radius=20)
    frame1.grid(row=0, column=0, padx=10, sticky="ns")

    # Add a background image on the right
    bg_image = Image.open(r"pharmacy-management-system\Project\image\medical-composition-with-pills.jpg")
    bg_image = bg_image.resize((850, 500), Image.Resampling.LANCZOS)
    bg_photo = ImageTk.PhotoImage(bg_image)

    bg_label = Label(root, image=bg_photo)
    bg_label.image = bg_photo
    bg_label.grid(row=0, column=1, sticky="nsew")

    # Display user data in a LabelFrame
    data_display = LabelFrame(
        frame1,
        text="User Data",
        font=("Arial", 14),
        bg="#f5f5f5",
        fg="black",
        labelanchor="n",
    )  # Centered title
    data_display.pack(pady=20, padx=10, fill="x")

    # Add user data inside the LabelFrame
    user_data_label = Label(
        data_display,
        text=f"Name: {information[2]}\nID: {information[3]} \nUsername: {information[0]}\nStatus: Active",
        font=("Arial", 12),
        bg="white",
        justify="left",
        anchor="nw",
    )
    user_data_label.pack(pady=10, padx=10, fill="both", expand=True)

    # Add navigation buttons
    # Home Page button
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

    # Billing button
    btn1 = Button(
        frame1,
        text="Billing",
        font=("Arial", 16),
        bg="#80C7E7",
        width=25,
        relief="flat",
        command=show_billing_page,  # Show billing page
    )
    btn1.pack(pady=8)

    # Expired medications button
    btn5 = Button(
        frame1,
        text="Expire medication",
        font=("Arial", 16),
        bg="#80C7E7",
        width=25,
        relief="flat",
        command=show_ex_page,
    )
    btn5.pack(pady=8)

    # Highlight if expired medications exist
    if fetchall_expiry_date():
        btn5.configure(bg="red")

    # Requests button
    btn_r = Button(
        frame1,
        text="Requsts",
        font=("Arial", 16),
        bg="#80C7E7",
        width=25,
        relief="flat",
        command=show_requist,
    )
    btn_r.pack(pady=8)

    # Highlight if pending requests exist
    if get_null_View():
        btn_r.configure(bg="red")

    # Log Out button
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
