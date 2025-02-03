from customtkinter import CTk, CTkImage, CTkLabel, CTkFrame, CTkEntry, CTkButton
from PIL import Image
import Staff_data
import admin
import admin_data
import doctorGui
import pharmacy


def login(main):

    def destroy_window():
        """
        this function destroy the old window and display new window wiht the large size
        """
        for widget in main.grid_slaves():
            widget.destroy()
        main.geometry("1200x800")  # large size
        main.resizable(False, False)
        # display the window in mid of computer screen
        screen_width = main.winfo_screenwidth()
        screen_height = main.winfo_screenheight()
        window_width = int(screen_width * 0.95)  # 95%   of screen width change this percentage on your screen
        window_height = int(screen_height * 0.85)  # 85% of screen height change this percentage on your screen
        x_position = (screen_width // 2) - (window_width // 2)
        y_position = (screen_height // 2) - (window_height // 2)
        main.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

    def handle_login():
        """Handle login logic and navigation based on user role."""
        username = usrname_entry.get().strip()
        password = passwd_entry.get().strip()
        try:
            staff_info = Staff_data.check_username_and_password(username, password)
            admin_info = admin_data.check_username_and_password(username, password)
            if staff_info or admin_info:
                if admin_info:
                    # open admin Page
                    main.title("Admin Page")
                    destroy_window()
                    admin.admin_window(admin_info, main)
                elif str(staff_info[4]).lower() == "doctor":
                    # open Doctor Page
                    main.title("Doctor Page")
                    destroy_window()
                    doctorGui.doctor_page(staff_info, main)
                elif str(staff_info[4]).lower() == "staff":
                    # open Staff Page
                    destroy_window()
                    main.title("Staff Page")
                    pharmacy.pharmacy_window(staff_info, main)
                else:
                    message_label.configure(text="Invalid role", text_color="red")
            else:
                message_label.configure(
                    text="The username or password\nis incorrect", text_color="red"
                )
        except ValueError:
            message_label.configure(
                text="Error during login. Please try again.", text_color="red"
            )

    def toggle_password_visibility():
        """Toggle visibility of the password field."""
        if passwd_entry.cget("show") == "*":
            passwd_entry.configure(show="")
            eye_button.configure(image=open_eye_img)
        else:
            passwd_entry.configure(show="*")
            eye_button.configure(image=closed_eye_img)

    # Load images
    bg_img = CTkImage(dark_image=Image.open(r"pharmacy-management-system\Project\image\bg1.jpg"), size=(500, 500))
    open_eye_img = CTkImage(#pharmacy-management-system\Project\image\bg1.jpg
        light_image=Image.open(r"pharmacy-management-system\Project\image\visible.png").resize((20, 20))
    )
    closed_eye_img = CTkImage(light_image=Image.open(r"pharmacy-management-system\Project\image\eye.png").resize((20, 20)))

    # Background image label
    bg_label = CTkLabel(main, image=bg_img, text="")
    bg_label.grid(row=0, column=0)

    # Login frame
    frame1 = CTkFrame(
        main,
        fg_color="#D9D9D9",
        bg_color="white",
        height=350,
        width=300,
        corner_radius=20,
    )
    frame1.grid(row=0, column=1, padx=40)

    # Title label
    title = CTkLabel(
        frame1,
        text="Welcome Back!\nLogin to Account",
        text_color="black",
        font=("", 25, "bold"),
    )
    title.grid(row=0, column=0, sticky="nw", pady=30, padx=10)

    # Username entry
    usrname_entry = CTkEntry(
        frame1,
        text_color="white",
        placeholder_text="Username",
        fg_color="black",
        placeholder_text_color="white",
        font=("", 16, "bold"),
        width=200,
        corner_radius=15,
        height=45,
    )
    usrname_entry.grid(row=1, column=0, sticky="nwe", padx=30)

    # Password entry
    passwd_entry = CTkEntry(
        frame1,
        text_color="white",
        placeholder_text="Password",
        fg_color="black",
        placeholder_text_color="white",
        font=("", 16, "bold"),
        width=200,
        corner_radius=15,
        height=45,
        show="*",
    )
    passwd_entry.grid(row=2, column=0, sticky="nwe", padx=30, pady=20)

    # Eye button for password visibility
    eye_button = CTkButton(
        frame1,
        image=closed_eye_img,
        width=30,
        height=30,
        fg_color="#D9D9D9",
        hover_color="lightgray",
        text="",
        command=toggle_password_visibility,
    )
    eye_button.place(x=229, y=194)

    # Message label for feedback
    message_label = CTkLabel(frame1, text="", text_color="black", font=("", 12, "bold"))
    message_label.grid(row=4, column=0, sticky="nwe", padx=30, pady=10)

    # Login button
    login_button = CTkButton(
        frame1,
        text="Login",
        font=("", 15, "bold"),
        height=40,
        width=60,
        fg_color="#A020F0",
        cursor="hand2",
        corner_radius=15,
        command=handle_login,
    )
    login_button.grid(row=3, column=0, sticky="ne", pady=20, padx=35)

    main.mainloop()


if __name__ == "__main__":
    # Initialize main application window
    main = CTk()
    main.title("Login Page")
    main.config(bg="white")
    main.geometry("850x500")
    main.resizable(False, False)

    # Center the window on the screen
    screen_width = main.winfo_screenwidth()
    screen_height = main.winfo_screenheight()
    x_position = (screen_width // 2) - (850 // 2)
    y_position = (screen_height // 2) - (500 // 2)
    main.geometry(f"850x500+{x_position}+{y_position}")

    login(main)
