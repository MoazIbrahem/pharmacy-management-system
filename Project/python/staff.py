import customtkinter as ctk
from tkinter.messagebox import showinfo
import Staff_data
import re
import admin_data

# Staff Management
def staff_window(root):
    # Set appearance
    ctk.set_appearance_mode("Light")
    ctk.set_default_color_theme("blue")

    # =======================================================================================================
    # =======================================================================================================
    # =======================================================================================================
    # the backend functions

    # Global variable to store the frame reference
    left_frame = None

    def additm():
        nonlocal left_frame  # Use the outer scoped variable for left_frame

        # Check if the frame already exists
        if left_frame is not None:
            return  # If the frame exists, do not create it again

        # Create the Left Frame for Input Fields
        left_frame = ctk.CTkFrame(root, width=600, height=500, corner_radius=15)
        left_frame.place(x=600, y=50)

        # Input Fields in Left Frame
        labels = [
            "UserName",
            "Password",
            "Name",
            "ID",
            "Role",
            "Salary",
            "Shift_AM",
            "Shift_PM",
        ]
        entries = {}  # Dictionary to store references to the input fields
        messages = {}  # Dictionary to store references to the message labels

        for idx, label in enumerate(labels):
            lbl = ctk.CTkLabel(left_frame, text=label, font=("Arial", 14))
            lbl.grid(
                row=idx * 2, column=0, sticky="w", padx=10
            )  # Place label in separate rows

            entry = ctk.CTkEntry(left_frame, width=180, font=("Arial", 12))
            entry.grid(
                row=idx * 2, column=1, padx=10
            )  # Place entry in the row below the label
            entries[label] = entry  # Store each entry field

            # Create a message label placed below each entry field
            message_label = ctk.CTkLabel(
                left_frame, text="", text_color="red", font=("Arial", 12)
            )
            message_label.grid(
                row=idx * 2 + 1, column=1, padx=10, pady=5, sticky="w"
            )  # Message label under entry field
            messages[label] = message_label  # Store the message label

        # Function to handle saving the employee data
        def save_employee():
            cuser = cpass = cname = cid = crole = csalary = cshiftAM = cshiftpm = False

            # Extract data from input fields
            # ["UserName", "Password", "Name", "ID", "Role", "Salary", "Shift_AM", "Shift_PM"]

            def clear_Username_message_label():
                messages["UserName"].configure(text="")

            def clear_Password_message_label():
                messages["Password"].configure(text="")

            def clear_Name_message_label():
                messages["Name"].configure(text="")

            def clear_ID_message_label():
                messages["ID"].configure(text="")

            def clear_Role_message_label():
                messages["Role"].configure(text="")

            def clear_Salary_message_label():
                messages["Salary"].configure(text="")

            def clear_Shift_AM_message_label():
                messages["Shift_AM"].configure(text="")

            def clear_Shift_PM_message_label():
                messages["Shift_PM"].configure(text="")

            # Check if each field is filled and update the corresponding message label
            if not entries["UserName"].get().strip():
                messages["UserName"].configure(text="UserName is required.")
                root.after(2000, clear_Username_message_label)
                cuser = False
            elif Staff_data.search_on_username(
                entries["UserName"].get().strip()
            ) or admin_data.search_on_username(entries["UserName"].get().strip()):
                messages["UserName"].configure(text="is already taken")
                root.after(2000, clear_Username_message_label)
                cuser = False
            elif len(entries["UserName"].get().strip()) < 8:
                messages["UserName"].configure(
                    text="is too short (minimum is 8 characters)"
                )
                root.after(2000, clear_Username_message_label)
                cuser = False
            else:
                cuser = True

            if not entries["Password"].get().strip():
                messages["Password"].configure(text="Password is required.")
                root.after(2000, clear_Password_message_label)
                cpass = False
            elif len(entries["Password"].get().strip()) < 8:
                messages["Password"].configure(
                    text="is too short (minimum is 8 characters)"
                )
                root.after(2000, clear_Password_message_label)
                cpass = False
            else:
                cpass = True

            if not entries["Name"].get().strip():
                messages["Name"].configure(text="Name is required.")
                root.after(2000, clear_Name_message_label)
                cname = False
            elif not bool(
                re.match(r"^[a-zA-Z\s]+$", str(entries["Name"].get().strip()).strip())
            ):
                messages["Name"].configure(text="Name must be contain letters only")
                root.after(2000, clear_Name_message_label)
                cname = False
            else:
                cname = True

            if not entries["ID"].get().strip():
                messages["ID"].configure(text="ID is required.")
                root.after(2000, clear_ID_message_label)
                cid = False
            elif Staff_data.search_on_id(
                entries["ID"].get().strip()
            ) or admin_data.search_on_id(entries["ID"].get().strip()):
                messages["ID"].configure(text="is already taken")
                root.after(2000, clear_ID_message_label)
                cid = False
            elif not str(entries["ID"].get().strip()).isdigit():
                messages["ID"].configure(text="ID must be contain digits only")
                root.after(2000, clear_ID_message_label)
                cid = False
            elif len(entries["ID"].get().strip()) < 10:
                messages["ID"].configure(text="is too short (minimum is 10 digits)")
                root.after(2000, clear_ID_message_label)
                cid = False
            else:
                cid = True

            if not entries["Role"].get().strip():
                messages["Role"].configure(text="Role is required.")
                root.after(2000, clear_Role_message_label)
                crole = False
            elif str(entries["Role"].get().strip()).title() not in [
                "Staff",
                "Admin",
                "Doctor",
            ]:
                messages["Role"].configure(
                    text="Role must be one of this [Staff,Admin,Doctor]"
                )
                root.after(2000, clear_Role_message_label)
                crole = False
            else:
                crole = True

            if not entries["Salary"].get().strip():
                messages["Salary"].configure(text="Salary is required.")
                root.after(2000, clear_Salary_message_label)
                csalary = False
            elif not str(entries["Salary"].get().strip()).isdigit():
                messages["Salary"].configure(text="Salary must be contain digits only")
                root.after(2000, clear_Salary_message_label)

                csalary = False
            elif int(entries["Salary"].get().strip()) == 0:
                messages["Salary"].configure(text="Salary Not Accepted")
                root.after(2000, clear_Salary_message_label)
                csalary = False
            else:
                csalary = True
            try:
                if not entries["Shift_AM"].get().strip():
                    messages["Shift_AM"].configure(text="Shift_AM is required.")
                    root.after(2000, clear_Shift_AM_message_label)
                    cshiftAM = False
                elif "." in entries["Shift_AM"].get().strip():
                    test = entries["Shift_AM"].get().strip().split(".")
                    if len(test[1]) == 1:
                        test[1] = test[1] + "0"
                    if len(test[1]) > 2:
                        messages["Shift_AM"].configure(text="Shift_AM Not Accepted")
                        root.after(2000, clear_Shift_AM_message_label)
                        cshiftAM = False
                    elif int(test[1]) > 59:
                        messages["Shift_AM"].configure(text="Shift_AM Not Accepted")
                        root.after(2000, clear_Shift_AM_message_label)
                        cshiftpm = False
                    elif int(test[1]) == 59:
                        entries["Shift_AM"] = str(int(test[0]) + 1)
                        cshiftpm = True
                    elif int(test[1]) == 0:
                        entries["Shift_AM"] = test[0]
                        cshiftpm = True
                elif not (
                    float((entries["Shift_AM"].get().strip())) >= 8
                    and float((entries["Shift_AM"].get().strip())) < 12
                ):
                    messages["Shift_AM"].configure(
                        text="Shift_AM must be between 8am to 12 pm"
                    )
                    root.after(2000, clear_Shift_AM_message_label)
                    cshiftAM = False
                elif float((entries["Shift_AM"].get().strip())) == 0:
                    messages["Shift_AM"].configure(text="Shift_AM Not Accepted")
                    root.after(2000, clear_Shift_AM_message_label)
                    cshiftAM = False
                else:
                    cshiftAM = True
            except:
                messages["Shift_AM"].configure(
                    text="Shift_AM must be contain digits only"
                )
                print("f")
                root.after(2000, clear_Shift_AM_message_label)
            try:
                if not entries["Shift_PM"].get().strip():
                    messages["Shift_PM"].configure(text="Shift_PM is required.")
                    root.after(2000, clear_Shift_PM_message_label)
                    cshiftpm = False
                elif "." in entries["Shift_PM"].get().strip():
                    test = entries["Shift_PM"].get().strip().split(".")
                    if len(test[1]) == 1:
                        test[1] = test[1] + "0"
                    if len(test[1]) > 2:
                        messages["Shift_PM"].configure(text="Shift_PM Not Accepted")
                        root.after(2000, clear_Shift_PM_message_label)
                        cshiftpm = False
                    elif int(test[1]) > 59:
                        messages["Shift_PM"].configure(text="Shift_PM Not Accepted")
                        root.after(2000, clear_Shift_PM_message_label)
                        cshiftpm = False
                    elif int(test[1]) == 59:
                        entries["Shift_PM"] = str(int(test[0]) + 1)
                        cshiftpm = True
                    elif int(test[1]) == 0:
                        entries["Shift_PM"] = test[0]
                        cshiftpm = True
                elif not (
                    float((entries["Shift_PM"].get().strip())) >= 1
                    and float((entries["Shift_PM"].get().strip())) <= 12
                ):
                    messages["Shift_PM"].configure(
                        text="Shift_PM must be between 12pm to 12am"
                    )
                    root.after(2000, clear_Shift_PM_message_label)
                    cshiftpm = False
                elif float((entries["Shift_PM"].get().strip())) == 0:
                    messages["Shift_PM"].configure(text="Shift_PM Not Accepted")
                    root.after(2000, clear_Shift_PM_message_label)
                    cshiftpm = False
                else:
                    cshiftpm = True
            except:
                messages["Shift_PM"].configure(
                    text="Shift_PM must be contain digits only"
                )
                root.after(2000, clear_Shift_PM_message_label)
                cshiftpm = False
            # Save data if all fields are valid
            if all([cuser, cpass, cname, cid, crole, csalary, cshiftAM, cshiftpm]):
                employee_data = [entries[label].get().strip() for label in labels]
                if str(entries["Role"].get().strip()).title() == "Admin":
                    admin_data.add_new_Admin(
                        employee_data[0],
                        employee_data[1],
                        employee_data[2],
                        employee_data[3],
                        employee_data[4],
                        employee_data[5],
                        employee_data[6],
                        employee_data[7],
                    )
                    save_message_label.configure(
                        text="Saved Successfully", text_color="green"
                    )
                    root.after(2000, lambda: save_message_label.configure(text=""))
                else:
                    Staff_data.add_new_staff(
                        employee_data[0],
                        employee_data[1],
                        employee_data[2],
                        employee_data[3],
                        employee_data[4],
                        employee_data[5],
                        employee_data[6],
                        employee_data[7],
                    )
                    save_message_label.configure(
                        text="Saved Successfully", text_color="green"
                    )
                    root.after(2000, lambda: save_message_label.configure(text=""))
                # Optionally clear the fields after saving
                for entry in entries.values():
                    entry.delete(0, "end")  # Clear the entry field after saving

        # Create the "Save" button
        save_btn = ctk.CTkButton(
            left_frame,
            text="Save",
            command=save_employee,
            width=180,
            font=("Arial", 14),
        )
        save_btn.grid(row=len(labels) * 2, column=0, columnspan=2, pady=20)
        save_message_label = ctk.CTkLabel(
            left_frame, text="", text_color="gray", font=("Arial", 20)
        )
        save_message_label.grid(row=len(labels) * 2 + 5, column=0, columnspan=2)

        # Function to exit the application
        def exit_application():
            nonlocal left_frame
            if left_frame is not None:
                left_frame.destroy()  # This will close the application
                left_frame = None  # Reset the frame reference

        # Create the "Exit" button
        exit_btn = ctk.CTkButton(
            left_frame,
            text="Exit",
            command=exit_application,
            width=180,
            font=("Arial", 14),
        )
        exit_btn.grid(row=len(labels) * 2 + 1, column=0, columnspan=2, pady=10)

    def update():
        """
        this fuction update the information of staff
        """
        nonlocal left_frame  # Use the outer scoped variable for left_frame

        # Check if the frame already exists
        if left_frame is not None:
            return  # If the frame exists, do not create it again

        def GO_Search():
            def save_changes():
                info = (
                    search_boxup.get().strip()
                )  # the box of usernaem or ID of employee search by [ID,Usernaem]
                upbox = (
                    search_boxup2.get().strip()
                )  # the box what admin need update[Usernaem,Password,Name,ID,Role,Salary,Shift_Am,Shif_PM]
                up = search_entryUP2.get().strip()  # The value updated

                # Username operations ===========================
                if upbox == "UserName":
                    if info == "ID":  # if the box seach is ID
                        if up:  # check the up not empty(1)
                            if (
                                Staff_data.get_username(search_entryUP.get().strip())
                                != up
                            ):  # check if new username the same old uername(2)
                                if not (
                                    Staff_data.search_on_username(up)
                                    or admin_data.search_on_username(up)
                                ):  # check if the new username not repated in database(3)
                                    if (
                                        len(up) > 8
                                    ):  # check if len(new username) is less than 8 size(4)
                                        Staff_data.update_username(
                                            Staff_data.get_username(
                                                search_entryUP.get().strip()
                                            ),
                                            up,
                                        )
                                        save_message_labelup.configure(
                                            text="Saved Successfully",
                                            text_color="green",
                                        )
                                        root.after(
                                            2000,
                                            lambda: save_message_labelup.configure(
                                                text=""
                                            ),
                                        )
                                    else:
                                        save_message_labelup.configure(
                                            text="is too short (minimum is 8 digits)",
                                            text_color="red",
                                        )  # (4)
                                        root.after(
                                            2000,
                                            lambda: save_message_labelup.configure(
                                                text=""
                                            ),
                                        )
                                else:
                                    save_message_labelup.configure(
                                        text="is already taken", text_color="red"
                                    )  # (3)
                                    root.after(
                                        2000,
                                        lambda: save_message_labelup.configure(text=""),
                                    )
                            else:
                                save_message_labelup.configure(
                                    text="The Same Old Username", text_color="red"
                                )  # (2)
                                root.after(
                                    2000,
                                    lambda: save_message_labelup.configure(text=""),
                                )
                        else:
                            save_message_labelup.configure(
                                text="username is required", text_color="red"
                            )  # (1)
                            root.after(
                                2000, lambda: save_message_labelup.configure(text="")
                            )

                    else:  # if the box seach is Username
                        if up:  # check the up not empty(1)
                            if (
                                search_entryUP.get().strip() != up
                            ):  # check if new username the same old uername(2)
                                if not (
                                    Staff_data.search_on_username(up)
                                    or admin_data.search_on_username(up)
                                ):  # check if the new username not repated in database(3)
                                    if (
                                        len(up) > 8
                                    ):  # check if len(new username) is less than 8 size(4)
                                        search_entryUP2.delete(0, "end")
                                        # clear the screen and retrun the initial
                                        Staff_data.update_username(
                                            search_entryUP.get().strip(), up
                                        )
                                        message_labelup.configure(
                                            text="Saved Successfully",
                                            text_color="green",
                                        )
                                        for widget in left_frame.grid_slaves(
                                            row=6, column=2
                                        ):
                                            widget.destroy()
                                        for widget in left_frame.grid_slaves(
                                            row=6, column=3
                                        ):
                                            widget.destroy()
                                        for widget in left_frame.grid_slaves(
                                            row=7, column=2
                                        ):
                                            widget.destroy()
                                        for widget in left_frame.grid_slaves(
                                            row=9, column=2
                                        ):
                                            widget.destroy()
                                        search_entryUP.delete(0, "end")
                                        root.after(
                                            2000,
                                            lambda: message_labelup.configure(text=""),
                                        )
                                    else:
                                        save_message_labelup.configure(
                                            text="is too short (minimum is 8 digits)",
                                            text_color="red",
                                        )  # (4)
                                        root.after(
                                            2000,
                                            lambda: save_message_labelup.configure(
                                                text=""
                                            ),
                                        )
                                else:
                                    save_message_labelup.configure(
                                        text="is already taken", text_color="red"
                                    )  # (3)
                                    root.after(
                                        2000,
                                        lambda: save_message_labelup.configure(text=""),
                                    )
                            else:
                                save_message_labelup.configure(
                                    text="The Same Old Username", text_color="red"
                                )  # (2)
                                root.after(
                                    2000,
                                    lambda: save_message_labelup.configure(text=""),
                                )
                        else:
                            save_message_labelup.configure(
                                text="username is required", text_color="red"
                            )  # (1)
                            root.after(
                                2000, lambda: save_message_labelup.configure(text="")
                            )
                # Username operations END ===========================

                # Password operations =======
                elif upbox == "Password":
                    if info == "ID":  # if the box seach is ID
                        if up:  # check the label is empty or not (1)
                            if (
                                len(up) > 8
                            ):  # check the len(new password) large than 8 size(2)
                                Staff_data.update_password(
                                    Staff_data.get_username(
                                        search_entryUP.get().strip()
                                    ),
                                    up,
                                )
                                save_message_labelup.configure(
                                    text="Saved Successfully", text_color="green"
                                )
                                root.after(
                                    2000,
                                    lambda: save_message_labelup.configure(text=""),
                                )
                                search_entryUP2.delete(0, "end")
                            else:
                                save_message_labelup.configure(
                                    text="is too short (minimum is 8 digits)",
                                    text_color="red",
                                )  # (2)
                                root.after(
                                    2000,
                                    lambda: save_message_labelup.configure(text=""),
                                )
                        else:
                            save_message_labelup.configure(
                                text="Password is required", text_color="red"
                            )  # (1)
                            root.after(
                                2000, lambda: save_message_labelup.configure(text="")
                            )
                    else:  # if the box seach is Username
                        if up:  # check the label is empty or not (1)
                            if (
                                len(up) > 8
                            ):  # check the len(new password) large than 8 size(2)
                                Staff_data.update_password(
                                    search_entryUP.get().strip(), up
                                )
                                save_message_labelup.configure(
                                    text="Saved Successfully", text_color="green"
                                )
                                root.after(
                                    2000,
                                    lambda: save_message_labelup.configure(text=""),
                                )
                                search_entryUP2.delete(0, "end")
                            else:
                                save_message_labelup.configure(
                                    text="is too short (minimum is 8 digits)",
                                    text_color="red",
                                )  # (2)
                                root.after(
                                    2000,
                                    lambda: save_message_labelup.configure(text=""),
                                )
                        else:
                            save_message_labelup.configure(
                                text="password is required", text_color="red"
                            )  # (1)
                            root.after(
                                2000, lambda: save_message_labelup.configure(text="")
                            )
                        # Password operations  EDN =======

                        # Name   operations =======
                elif upbox == "Name":
                    if info == "ID":  # if the box seach is ID
                        if up:  # check the label is empty or not(1)
                            if bool(
                                re.match(r"^[a-zA-Z\s]+$", str(up).strip())
                            ):  # check if Name contain the (2)
                                Staff_data.update_name(
                                    Staff_data.get_username(
                                        search_entryUP.get().strip()
                                    ),
                                    up,
                                )
                                save_message_labelup.configure(
                                    text="Saved Successfully", text_color="green"
                                )
                                root.after(
                                    2000,
                                    lambda: save_message_labelup.configure(text=""),
                                )
                                search_entryUP2.delete(0, "end")
                            else:
                                save_message_labelup.configure(
                                    text="the name must be contain letter",
                                    text_color="red",
                                )  # (2)
                                root.after(
                                    2000,
                                    lambda: save_message_labelup.configure(text=""),
                                )
                        else:
                            save_message_labelup.configure(
                                text="Name is required", text_color="red"
                            )  # (1)
                            root.after(
                                2000, lambda: save_message_labelup.configure(text="")
                            )
                    else:  # if the box seach is Username
                        if up:  # check the label is empty or not(1)
                            if bool(
                                re.match(r"^[a-zA-Z\s]+$", up.strip())
                            ):  # check if Name contain the (2)
                                Staff_data.update_name(search_entryUP.get().strip(), up)
                                save_message_labelup.configure(
                                    text="Saved Successfully", text_color="green"
                                )
                                root.after(
                                    2000,
                                    lambda: save_message_labelup.configure(text=""),
                                )
                                search_entryUP2.delete(0, "end")
                            else:
                                save_message_labelup.configure(
                                    text="the name must be contain letter",
                                    text_color="red",
                                )  # (2)
                                root.after(
                                    2000,
                                    lambda: save_message_labelup.configure(text=""),
                                )
                        else:
                            save_message_labelup.configure(
                                text="Name is required", text_color="red"
                            )  # (1)
                            root.after(
                                2000, lambda: save_message_labelup.configure(text="")
                            )
                        #  Name operations end =======

                        # ID operations =======
                elif upbox == "ID":
                    if info == "ID":  # if the box seach is ID
                        if up:  # check the label is empty or not(1)
                            if (
                                search_entryUP.get().strip() != up
                            ):  # check the new id is the same old or not(2)
                                if not (
                                    Staff_data.search_on_id(up)
                                    or admin_data.search_on_id(up)
                                ):  # check the new id is repeated in database or not (3)
                                    if up.isdigit():  # check the id is number or not(4)
                                        if (
                                            len(up) >= 10
                                        ):  # check len(new id) large than 10 size (5)
                                            Staff_data.update_id(
                                                Staff_data.get_username(
                                                    search_entryUP.get().strip()
                                                ),
                                                up,
                                            )
                                            search_entryUP2.delete(0, "end")
                                            # return the intial screen
                                            message_labelup.configure(
                                                text="Saved Successfully",
                                                text_color="green",
                                            )
                                            for widget in left_frame.grid_slaves(
                                                row=6, column=2
                                            ):
                                                widget.destroy()
                                            for widget in left_frame.grid_slaves(
                                                row=6, column=3
                                            ):
                                                widget.destroy()
                                            for widget in left_frame.grid_slaves(
                                                row=7, column=2
                                            ):
                                                widget.destroy()
                                            for widget in left_frame.grid_slaves(
                                                row=9, column=2
                                            ):
                                                widget.destroy()
                                            search_entryUP.delete(0, "end")
                                            root.after(
                                                2000,
                                                lambda: message_labelup.configure(
                                                    text=""
                                                ),
                                            )
                                        else:
                                            save_message_labelup.configure(
                                                text="is too short (minimum is 10 digits)",
                                                text_color="red",
                                            )  # (5)
                                            root.after(
                                                2000,
                                                lambda: save_message_labelup.configure(
                                                    text=""
                                                ),
                                            )
                                    else:
                                        save_message_labelup.configure(
                                            text="The id must be digits",
                                            text_color="red",
                                        )  # (4)
                                        root.after(
                                            2000,
                                            lambda: save_message_labelup.configure(
                                                text=""
                                            ),
                                        )
                                else:
                                    save_message_labelup.configure(
                                        text="is already taken", text_color="red"
                                    )  # (3)
                                    root.after(
                                        2000,
                                        lambda: save_message_labelup.configure(text=""),
                                    )
                            else:
                                save_message_labelup.configure(
                                    text="The Same Old ID", text_color="red"
                                )  # (2)
                                root.after(
                                    2000,
                                    lambda: save_message_labelup.configure(text=""),
                                )
                        else:
                            save_message_labelup.configure(
                                text="ID is required", text_color="red"
                            )  # (1)
                            root.after(
                                2000, lambda: save_message_labelup.configure(text="")
                            )
                    else:  # if the box seach is Username
                        if up:  # check the label is empty or not(1)
                            if (
                                Staff_data.get_id(search_entryUP.get().strip()) != up
                            ):  # check the new id is the same old or not(2)
                                if not (
                                    Staff_data.search_on_id(up)
                                    or admin_data.search_on_id(up)
                                ):  # check the new id is repeated in database or not (3)
                                    if up.isdigit():  # check the id is number or not(4)
                                        if (
                                            len(up) >= 10
                                        ):  # check len(new id) large than 10 size (5)
                                            Staff_data.update_id(
                                                search_entryUP.get().strip(), up
                                            )
                                            save_message_labelup.configure(
                                                text="Saved Successfully",
                                                text_color="green",
                                            )
                                            root.after(
                                                2000,
                                                lambda: save_message_labelup.configure(
                                                    text=""
                                                ),
                                            )
                                            search_entryUP2.delete(0, "end")
                                        else:
                                            save_message_labelup.configure(
                                                text="is too short (minimum is 10 digits)",
                                                text_color="red",
                                            )  # (5)
                                            root.after(
                                                2000,
                                                lambda: save_message_labelup.configure(
                                                    text=""
                                                ),
                                            )
                                    else:
                                        save_message_labelup.configure(
                                            text="The id must be digits",
                                            text_color="red",
                                        )  # (4)
                                        root.after(
                                            2000,
                                            lambda: save_message_labelup.configure(
                                                text=""
                                            ),
                                        )
                                else:
                                    save_message_labelup.configure(
                                        text="is already taken", text_color="red"
                                    )  # (3)
                                    root.after(
                                        2000,
                                        lambda: save_message_labelup.configure(text=""),
                                    )
                            else:
                                save_message_labelup.configure(
                                    text="The Same Old ID", text_color="red"
                                )  # (2)
                                root.after(
                                    2000,
                                    lambda: save_message_labelup.configure(text=""),
                                )
                        else:
                            save_message_labelup.configure(
                                text="ID is required", text_color="red"
                            )  # (1)
                            root.after(
                                2000, lambda: save_message_labelup.configure(text="")
                            )
                    # ID operations end =======

                    # Role operations =======
                elif upbox == "Role":
                    if info == "ID":  # if the box seach is ID
                        if up:  # check the label is empty or not (1)
                            if up.lower() in [
                                "staff",
                                "doctor",
                                "admin",
                            ]:  # check the new role in this roles or not (2)
                                if up.lower() == "admin":
                                    staffinfo = Staff_data.fecheone_staff(
                                        search_entryUP.get().strip()
                                    )
                                    admin_data.add_new_Admin(
                                        staffinfo[0][0],
                                        staffinfo[0][1],
                                        staffinfo[0][2],
                                        staffinfo[0][3],
                                        "admin",
                                        staffinfo[0][5],
                                        staffinfo[0][6],
                                        staffinfo[0][7],
                                    )
                                    Staff_data.remove_staff(
                                        search_entryUP.get().strip()
                                    )
                                    search_entryUP2.delete(0, "end")
                                    # return the intial screen
                                    message_labelup.configure(
                                        text="Saved Successfully", text_color="green"
                                    )
                                    for widget in left_frame.grid_slaves(
                                        row=6, column=2
                                    ):
                                        widget.destroy()
                                    for widget in left_frame.grid_slaves(
                                        row=6, column=3
                                    ):
                                        widget.destroy()
                                    for widget in left_frame.grid_slaves(
                                        row=7, column=2
                                    ):
                                        widget.destroy()
                                    for widget in left_frame.grid_slaves(
                                        row=9, column=2
                                    ):
                                        widget.destroy()
                                    search_entryUP.delete(0, "end")
                                    root.after(
                                        2000, lambda: message_labelup.configure(text="")
                                    )
                                else:
                                    Staff_data.update_role(
                                        Staff_data.get_username(
                                            search_entryUP.get().strip()
                                        ),
                                        up,
                                    )
                                    save_message_labelup.configure(
                                        text="Saved Successfully", text_color="green"
                                    )
                                    root.after(
                                        2000,
                                        lambda: save_message_labelup.configure(text=""),
                                    )
                            else:
                                save_message_labelup.configure(
                                    text="Role must be in [staff,doctor,admin]",
                                    text_color="red",
                                )  # (2)
                                root.after(
                                    2000,
                                    lambda: save_message_labelup.configure(text=""),
                                )
                        else:
                            save_message_labelup.configure(
                                text="Role is required", text_color="red"
                            )  # (1)
                            root.after(
                                2000, lambda: save_message_labelup.configure(text="")
                            )
                    else:  # if the box seach is Username
                        if up:  # check the label is empty or not (1)
                            if up.lower() in [
                                "staff",
                                "doctor",
                                "admin",
                            ]:  # check the new role in this roles or not (2)
                                if up.lower() == "admin":
                                    staffinfo = Staff_data.fecheone_staff(
                                        search_entryUP.get().strip()
                                    )
                                    admin_data.add_new_Admin(
                                        staffinfo[0],
                                        staffinfo[1],
                                        staffinfo[2],
                                        staffinfo[3],
                                        "admin",
                                        staffinfo[5],
                                        staffinfo[6],
                                        staffinfo[7],
                                    )
                                    Staff_data.remove_staff(
                                        search_entryUP.get().strip()
                                    )
                                    search_entryUP2.delete(0, "end")
                                    # return the intial screen
                                    message_labelup.configure(
                                        text="Saved Successfully", text_color="green"
                                    )
                                    for widget in left_frame.grid_slaves(
                                        row=6, column=2
                                    ):
                                        widget.destroy()
                                    for widget in left_frame.grid_slaves(
                                        row=6, column=3
                                    ):
                                        widget.destroy()
                                    for widget in left_frame.grid_slaves(
                                        row=7, column=2
                                    ):
                                        widget.destroy()
                                    for widget in left_frame.grid_slaves(
                                        row=9, column=2
                                    ):
                                        widget.destroy()
                                    search_entryUP.delete(0, "end")
                                    root.after(
                                        2000, lambda: message_labelup.configure(text="")
                                    )
                                else:
                                    Staff_data.update_role(
                                        search_entryUP.get().strip(), up
                                    )
                                    save_message_labelup.configure(
                                        text="Saved Successfully", text_color="green"
                                    )
                                    root.after(
                                        2000,
                                        lambda: save_message_labelup.configure(text=""),
                                    )
                            else:
                                save_message_labelup.configure(
                                    text="Role must be in [staff,doctor,admin]",
                                    text_color="red",
                                )  # (2)
                                root.after(
                                    2000,
                                    lambda: save_message_labelup.configure(text=""),
                                )
                        else:
                            save_message_labelup.configure(
                                text="Role is required", text_color="red"
                            )  # (1)
                            root.after(
                                2000, lambda: save_message_labelup.configure(text="")
                            )
                    # Role operations end =======

                    # Salary operations =======
                elif upbox == "Salary":
                    if info == "ID":  # if the box seach is ID
                        if up:  # check the label is empty or not (1)
                            if up.isdigit():  # check the salary is a number or not(2)
                                if int(up) != 0:
                                    Staff_data.update_salary(
                                        Staff_data.get_username(
                                            search_entryUP.get().strip()
                                        ),
                                        up,
                                    )
                                    save_message_labelup.configure(
                                        text="Saved Successfully", text_color="green"
                                    )
                                    root.after(
                                        2000,
                                        lambda: save_message_labelup.configure(text=""),
                                    )
                                    search_entryUP2.delete(0, "end")
                                else:
                                    save_message_labelup.configure(
                                        text="The Salary not Accepted", text_color="red"
                                    )
                                    root.after(
                                        2000,
                                        lambda: save_message_labelup.configure(text=""),
                                    )
                            else:
                                save_message_labelup.configure(
                                    text="The Salary must be digits", text_color="red"
                                )  # (2)
                                root.after(
                                    2000,
                                    lambda: save_message_labelup.configure(text=""),
                                )
                        else:
                            save_message_labelup.configure(
                                text="Salary is required", text_color="red"
                            )  # (1)
                            root.after(
                                2000, lambda: save_message_labelup.configure(text="")
                            )
                    else:  # if the box seach is Username
                        if up:  # check the label is empty or not (1)
                            if up.isdigit():  # check the salary is a number or not(2)
                                if int(up) != 0:
                                    Staff_data.update_salary(
                                        search_entryUP.get().strip(), up
                                    )
                                    save_message_labelup.configure(
                                        text="Saved Successfully", text_color="green"
                                    )
                                    root.after(
                                        2000,
                                        lambda: save_message_labelup.configure(text=""),
                                    )
                                    search_entryUP2.delete(0, "end")
                                else:
                                    save_message_labelup.configure(
                                        text="The Salary not Accepted", text_color="red"
                                    )
                                    root.after(
                                        2000,
                                        lambda: save_message_labelup.configure(text=""),
                                    )
                            else:
                                save_message_labelup.configure(
                                    text="The Salary must be digits", text_color="red"
                                )  # (2)
                                root.after(
                                    2000,
                                    lambda: save_message_labelup.configure(text=""),
                                )
                        else:
                            save_message_labelup.configure(
                                text="Salary is required", text_color="red"
                            )  # (1)
                            root.after(
                                2000, lambda: save_message_labelup.configure(text="")
                            )
                    # Salary operations end =======

                    # Shift_AM operations =======
                elif upbox == "Shift_AM":
                    if info == "ID":  # if the box seach is ID
                        if up:  # check the label is empty or not (1)
                            if up.isdigit():  # check the salary is a number or not(2)
                                if (
                                    int(up) >= 8 and int(up) <= 11
                                ):  # check the correct shift_am 8am to 11 am(3)
                                    Staff_data.update_shiftAM(
                                        Staff_data.get_username(
                                            search_entryUP.get().strip()
                                        ),
                                        up,
                                    )
                                    save_message_labelup.configure(
                                        text="Saved Successfully", text_color="green"
                                    )
                                    root.after(
                                        2000,
                                        lambda: save_message_labelup.configure(text=""),
                                    )
                                    search_entryUP2.delete(0, "end")
                                else:
                                    save_message_labelup.configure(
                                        text="Shift_AM must be between 8am to 11am",
                                        text_color="red",
                                    )  # (3)
                                    root.after(
                                        2000,
                                        lambda: save_message_labelup.configure(text=""),
                                    )
                            else:
                                save_message_labelup.configure(
                                    text="the shift not Accepted", text_color="red"
                                )  # (3)
                                root.after(
                                    2000,
                                    lambda: save_message_labelup.configure(text=""),
                                )
                        else:
                            save_message_labelup.configure(
                                text="Shift_AM is required", text_color="red"
                            )  # (1)
                            root.after(
                                2000, lambda: save_message_labelup.configure(text="")
                            )
                    else:  # if the box seach is Username
                        if up:  # check the label is empty or not (1)
                            if up.isdigit():  # check the salary is a number or not(2)
                                if (
                                    int(up) >= 8 and int(up) <= 11
                                ):  # check the correct shift_am 8am to 11 am(3)
                                    Staff_data.update_shiftAM(
                                        search_entryUP.get().strip(), up
                                    )
                                    save_message_labelup.configure(
                                        text="Saved Successfully", text_color="green"
                                    )
                                    root.after(
                                        2000,
                                        lambda: save_message_labelup.configure(text=""),
                                    )
                                    search_entryUP2.delete(0, "end")
                                else:
                                    save_message_labelup.configure(
                                        text="Shift_AM must be between 8am to 11am",
                                        text_color="red",
                                    )  # (3)
                                    root.after(
                                        2000,
                                        lambda: save_message_labelup.configure(text=""),
                                    )
                            else:
                                save_message_labelup.configure(
                                    text="the Shift_AM not Accepted", text_color="red"
                                )  # (2)
                                root.after(
                                    2000,
                                    lambda: save_message_labelup.configure(text=""),
                                )
                        else:
                            save_message_labelup.configure(
                                text="Shift_AM is required", text_color="red"
                            )  # (1)
                            root.after(
                                2000, lambda: save_message_labelup.configure(text="")
                            )
                        # Shift_AM operations end =======

                        # Shift_PM operations =======
                else:
                    if info == "ID":  # if the box seach is ID
                        if up:  # check the label is empty or not (1)
                            if up.isdigit():  # check the salary is a number or not(2)
                                if (
                                    int(up) >= 1 and int(up) <= 12
                                ):  # check the correct shift_am 12pm to 12am (3)
                                    Staff_data.update_shiftPM(
                                        Staff_data.get_username(
                                            search_entryUP.get().strip()
                                        ),
                                        up,
                                    )
                                    save_message_labelup.configure(
                                        text="Saved Successfully", text_color="green"
                                    )
                                    root.after(
                                        2000,
                                        lambda: save_message_labelup.configure(text=""),
                                    )
                                    search_entryUP2.delete(0, "end")
                                else:
                                    save_message_labelup.configure(
                                        text="Shift_PM must be between 12pm to 12am",
                                        text_color="red",
                                    )  # (3)
                                    root.after(
                                        2000,
                                        lambda: save_message_labelup.configure(text=""),
                                    )
                            else:
                                save_message_labelup.configure(
                                    text="the shift not Accepted", text_color="red"
                                )  # (2)
                                root.after(
                                    2000,
                                    lambda: save_message_labelup.configure(text=""),
                                )
                        else:
                            save_message_labelup.configure(
                                text="Shift_PM is required", text_color="red"
                            )  # (1)
                            root.after(
                                2000, lambda: save_message_labelup.configure(text="")
                            )
                    else:  # if the box seach is Username
                        if up:  # check the label is empty or not (1)
                            if up.isdigit():  # check the salary is a number or not(2)
                                if (
                                    int(up) >= 1 and int(up) <= 12
                                ):  # check the correct shift_am 12pm to 12am (3)
                                    Staff_data.update_shiftPM(
                                        search_entryUP.get().strip(), up
                                    )
                                    save_message_labelup.configure(
                                        text="Saved Successfully", text_color="green"
                                    )
                                    root.after(
                                        2000,
                                        lambda: save_message_labelup.configure(text=""),
                                    )
                                    search_entryUP2.delete(0, "end")
                                else:
                                    save_message_labelup.configure(
                                        text="Shift_PM must be between 12pm to 12am",
                                        text_color="red",
                                    )  # (3)
                                    root.after(
                                        2000,
                                        lambda: save_message_labelup.configure(text=""),
                                    )
                            else:
                                save_message_labelup.configure(
                                    text="the Shift_AM not Accepted", text_color="red"
                                )  # (2)
                                root.after(
                                    2000,
                                    lambda: save_message_labelup.configure(text=""),
                                )
                        else:
                            save_message_labelup.configure(
                                text="Shift_AM is required", text_color="red"
                            )  # (1)
                            root.after(
                                2000, lambda: save_message_labelup.configure(text="")
                            )

            # =====================================================
            if search_boxup.get().strip() == "ID":
                if Staff_data.search_on_id(search_entryUP.get().strip()):
                    message_labelup.configure(
                        text="what do you wnat update", text_color="green"
                    )
                    search_boxup2 = ctk.CTkComboBox(
                        left_frame,
                        values=[
                            "UserName",
                            "Password",
                            "Name",
                            "ID",
                            "Role",
                            "Salary",
                            "Shift_AM",
                            "Shift_PM",
                        ],
                        width=100,
                        font=("Arial", 14),
                    )
                    search_boxup2.grid(row=6, column=2, padx=10, sticky="w")
                    search_entryUP2 = ctk.CTkEntry(
                        left_frame, width=250, font=("Arial", 14)
                    )
                    search_entryUP2.grid(row=6, column=3, padx=3, sticky="w")
                    # Create the "Save" button
                    save_up = ctk.CTkButton(
                        left_frame,
                        text="Save",
                        width=180,
                        font=("Arial", 14),
                        command=save_changes,
                    )
                    save_up.grid(row=7, column=2, columnspan=2, pady=20)
                    save_message_labelup = ctk.CTkLabel(
                        left_frame, text="", text_color="gray", font=("Arial", 20)
                    )
                    save_message_labelup.grid(row=9, column=2, columnspan=2)
                else:
                    message_labelup.configure(
                        text="The ID Not Correct", text_color="red"
                    )
                    for widget in left_frame.grid_slaves(row=6, column=2):
                        widget.destroy()
                    for widget in left_frame.grid_slaves(row=6, column=3):
                        widget.destroy()
                    for widget in left_frame.grid_slaves(row=7, column=2):
                        widget.destroy()
                    for widget in left_frame.grid_slaves(row=9, column=2):
                        widget.destroy()
            elif search_boxup.get().strip() == "UserName":
                if Staff_data.search_on_username(search_entryUP.get().strip()):
                    message_labelup.configure(
                        text="what do you wnat update", text_color="green"
                    )
                    search_boxup2 = ctk.CTkComboBox(
                        left_frame,
                        values=[
                            "UserName",
                            "Password",
                            "Name",
                            "ID",
                            "Role",
                            "Salary",
                            "Shift_AM",
                            "Shift_PM",
                        ],
                        width=100,
                        font=("Arial", 14),
                    )
                    search_boxup2.grid(row=6, column=2, padx=10, sticky="w")
                    search_entryUP2 = ctk.CTkEntry(
                        left_frame, width=250, font=("Arial", 14)
                    )
                    search_entryUP2.grid(row=6, column=3, padx=3, sticky="w")
                    # Create the "Save" button
                    save_up = ctk.CTkButton(
                        left_frame,
                        text="Save",
                        width=180,
                        font=("Arial", 14),
                        command=save_changes,
                    )
                    save_up.grid(row=7, column=2, columnspan=2, pady=20)
                    save_message_labelup = ctk.CTkLabel(
                        left_frame, text="", text_color="gray", font=("Arial", 20)
                    )
                    save_message_labelup.grid(row=9, column=2, columnspan=2)
                else:
                    message_labelup.configure(
                        text="The UserName Not Correct", text_color="red"
                    )
                    for widget in left_frame.grid_slaves(row=6, column=2):
                        widget.destroy()
                    for widget in left_frame.grid_slaves(row=6, column=3):
                        widget.destroy()
                    for widget in left_frame.grid_slaves(row=7, column=2):
                        widget.destroy()
                    for widget in left_frame.grid_slaves(row=9, column=2):
                        widget.destroy()
            else:
                message_labelup.configure(text="Error", text_color="red")

        left_frame = ctk.CTkFrame(root, width=600, height=500, corner_radius=15)
        left_frame.place(x=500, y=200)
        # Search Area
        title = ctk.CTkLabel(
            left_frame,
            text="Select the employee you wnat to modify",
            text_color=font_color,
            fg_color=bg_color,
            font=("Bodoni MT Black", 25, "bold"),
            corner_radius=6,
        )
        title.grid(row=0, column=0, columnspan=4, pady=10, sticky="ew")
        search_la = ctk.CTkLabel(
            left_frame, text="Employee Search by:", font=font_style
        )
        search_la.grid(row=1, column=0, sticky="w")
        search_entryUP = ctk.CTkEntry(left_frame, width=250, font=("Arial", 14))
        search_entryUP.grid(row=1, column=3, padx=3, sticky="w")
        # Create a message label placed below each entry field
        message_labelup = ctk.CTkLabel(
            left_frame, text="", text_color="red", font=("Arial", 17, "bold")
        )
        message_labelup.grid(
            row=6, column=0, sticky="w", pady=10
        )  # Message label under entry field
        search_boxup = ctk.CTkComboBox(
            left_frame,
            values=["ID", "UserName"],
            width=100,
            font=("Arial", 14),
        )
        search_boxup.grid(row=1, column=2, padx=10, sticky="w")
        search_btnup = ctk.CTkButton(
            left_frame, text="Go", width=250, command=GO_Search
        )
        search_btnup.grid(row=2, column=3, padx=3, pady=5, sticky="w")

        # Function to exit the application
        def exit_application():
            nonlocal left_frame
            if left_frame is not None:
                left_frame.destroy()  # This will close the application
                left_frame = None  # Reset the frame reference

        # Create the "Exit" button
        exit_btn = ctk.CTkButton(
            left_frame,
            text="Exit",
            command=exit_application,
            width=100,
            font=("Arial", 14),
        )
        exit_btn.grid(row=2, column=1, columnspan=2, padx=5)

    def delete():
        nonlocal left_frame  # Use the outer scoped variable for left_frame
        # Check if the frame already exists
        if left_frame is not None:
            return  # If the frame exists, do not create it again

        def save_changes():
            upox = search_boxup.get().strip()
            if upox == "UserName":
                if Staff_data.search_on_username(search_entryUP.get().strip()):
                    Staff_data.remove_staff(search_entryUP.get().strip())
                    message_labelup.configure(
                        text="Deleted Successfully", text_color="green"
                    )
                    root.after(2000, lambda: message_labelup.configure(text=""))
                    search_entryUP.delete(0, "end")
                else:
                    message_labelup.configure(
                        text="The UserName NOT correct", text_color="red"
                    )
                    root.after(2000, lambda: message_labelup.configure(text=""))
            else:
                if Staff_data.search_on_id(search_entryUP.get().strip()):
                    Staff_data.remove_staff(search_entryUP.get().strip())
                    message_labelup.configure(
                        text="Deleted Successfully", text_color="green"
                    )
                    root.after(2000, lambda: message_labelup.configure(text=""))
                    search_entryUP.delete(0, "end")
                else:
                    message_labelup.configure(
                        text="The ID NOT correct", text_color="red"
                    )
                    root.after(2000, lambda: message_labelup.configure(text=""))

        left_frame = ctk.CTkFrame(root, width=600, height=500, corner_radius=15)
        left_frame.place(x=500, y=200)
        # Search Area
        title = ctk.CTkLabel(
            left_frame,
            text="Enter the staff ID or Username",
            text_color=font_color,
            fg_color=bg_color,
            font=("Bodoni MT Black", 25, "bold"),
            corner_radius=6,
        )
        title.grid(row=0, column=0, columnspan=4, pady=10, sticky="ew")
        search_la = ctk.CTkLabel(
            left_frame, text="Employee Search by:", font=font_style
        )
        search_la.grid(row=1, column=0, sticky="w")
        search_entryUP = ctk.CTkEntry(left_frame, width=250, font=("Arial", 14))
        search_entryUP.grid(row=1, column=3, padx=3, sticky="w")
        # Create a message label placed below each entry field
        message_labelup = ctk.CTkLabel(
            left_frame, text="", text_color="red", font=("Arial", 17, "bold")
        )
        message_labelup.grid(
            row=6, column=0, sticky="w", pady=10
        )  # Message label under entry field
        search_boxup = ctk.CTkComboBox(
            left_frame,
            values=["ID", "UserName"],
            width=100,
            font=("Arial", 14),
        )
        search_boxup.grid(row=1, column=2, padx=10, sticky="w")
        search_btnup = ctk.CTkButton(
            left_frame, text="Save", width=250, command=save_changes
        )
        search_btnup.grid(row=2, column=3, padx=3, pady=5, sticky="w")

        # Function to exit the application
        def exit_application():
            nonlocal left_frame
            if left_frame is not None:
                left_frame.destroy()  # This will close the application
                left_frame = None  # Reset the frame reference

        # Create the "Exit" button
        exit_btn = ctk.CTkButton(
            left_frame,
            text="Exit",
            command=exit_application,
            width=100,
            font=("Arial", 14),
        )
        exit_btn.grid(row=2, column=1, columnspan=2, padx=5)

    def showAll():
        data = Staff_data.fecheall_staff()
        table.delete_all_rows()
        for i in data:
          table.add_row(i)

    def search():
        if search_box.get().strip() == "UserName":
            if Staff_data.search_on_username(search_entry.get().strip()):
                data = Staff_data.fecheone_staff(search_entry.get().strip())
                table.delete_all_rows()
                for i in data:
                  table.add_row(i)
            else:
                  left_frame = ctk.CTkFrame(table_frame, width=300, height=300, corner_radius=15)
                  left_frame.place(x=300, y=150)
                  title_label = ctk.CTkLabel(
                  left_frame, text="The Username not correct", font=("Helvetica", 20, "bold"),bg_color="red"
                          )
                  title_label.grid(row=0, column=0, columnspan=2, pady=10)
                  left_frame.after(2000,lambda:left_frame.destroy())
        elif search_box.get().strip() == "ID":
            if Staff_data.search_on_id(search_entry.get().strip()):
                data = Staff_data.fecheone_staff(search_entry.get().strip())
                table.delete_all_rows()
                for i in data:
                  table.add_row(i)
            else:
                  left_frame = ctk.CTkFrame(table_frame, width=300, height=300, corner_radius=15)
                  left_frame.place(x=300, y=150)
                  title_label = ctk.CTkLabel(
                  left_frame, text="The ID not correct", font=("Helvetica", 20, "bold"),bg_color="red"
                          )
                  title_label.grid(row=0, column=0, columnspan=2, pady=10)
                  left_frame.after(2000,lambda:left_frame.destroy())
        else:
              left_frame = ctk.CTkFrame(table_frame, width=300, height=300, corner_radius=15)
              left_frame.place(x=300, y=150)
              title_label = ctk.CTkLabel(
              left_frame, text="Invalid input", font=("Helvetica", 20, "bold"),bg_color="red"
                      )
              title_label.grid(row=0, column=0, columnspan=2, pady=10)
              left_frame.after(2000,lambda:left_frame.destroy())
          

    # =======================================================================================================
    # =======================================================================================================
    # =======================================================================================================
    # Right Frame (Enlarged)
    right_frame = ctk.CTkFrame(
        root, width=600, height=500
    )  # Increased width and height for right frame
    right_frame.grid(row=0, column=1, sticky="nsew", padx=10)

    bg_color = "#4169E1"
    font_color = "#E7EBEE"
    font_style = ("Arial", 18, "bold")

    # Title for the Billing Page
    title = ctk.CTkLabel(
        right_frame,
        text="Staff Management",
        text_color=font_color,
        fg_color=bg_color,
        font=("Bodoni MT Black", 25, "bold"),
        corner_radius=6,
    )
    title.grid(row=0, column=0, columnspan=4, pady=10, sticky="ew")

    # Search Area
    search_label = ctk.CTkLabel(right_frame, text="Search by:", font=font_style)
    search_label.grid(row=1, column=0, padx=20, pady=20, sticky="w")

    search_box = ctk.CTkComboBox(
        right_frame,
        values=["ID", "UserName"],
        width=180,
        font=("Arial", 14),
    )
    search_box.grid(row=1, column=1, padx=3, pady=20, sticky="w")

    search_entry = ctk.CTkEntry(right_frame, width=250, font=("Arial", 14))
    search_entry.grid(row=1, column=2, padx=3, pady=20, sticky="w")

    search_btn = ctk.CTkButton(right_frame, text="Go", width=100, command=search)
    search_btn.grid(row=1, column=3, padx=3, pady=20, sticky="w")

    # Create Table Frame
    table_frame = ctk.CTkFrame(right_frame)
    table_frame.grid(row=2, column=0, columnspan=4, padx=10, pady=10, sticky="nsew")
    # Define columns (Updated to remove unnecessary columns and add Date)
    columns = (
        "Username",
        "Password",
        "Name",
        "ID",
        "Role",
        "salary",
        "Shift_From",
        "shift_to",
    )

    # Create Treeview using CTk's ScrollableFrame for better visuals
    class ModernTable(ctk.CTkScrollableFrame):
        def __init__(self, parent, columns, *args, **kwargs):
            super().__init__(parent, *args, **kwargs)
            self.columns = columns
            self.headers = []

            # Create headers
            for col in self.columns:
                label = ctk.CTkLabel(self, text=col, font=("Helvetica", 16), padx=10)
                label.grid(row=0, column=self.columns.index(col), sticky="nsew", pady=5)
                self.headers.append(label)

            # Adjust grid weights
            for i in range(len(columns)):
                self.grid_columnconfigure(i, weight=1)

            self.rows = []

        def add_row(self, values):
            row_index = len(self.rows) + 1
            row_data = []

            for col_index, value in enumerate(values):
                label = ctk.CTkLabel(self, text=value, font=("Helvetica", 14), padx=5)
                label.grid(row=row_index, column=col_index, sticky="nsew", pady=2)
                row_data.append(label)

            self.rows.append(row_data)
        def delete_all_rows(self):
            """Delete all rows from the table."""
            for row in self.rows:
                for widget in row:
                    widget.destroy()
            self.rows.clear()

    # Instantiate ModernTable
    table = ModernTable(table_frame, columns, width=700, height=400)
    table.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

    # Buttons Below Table (Larger buttons)
    buttons = {
        "Add Employee": additm,
        "Update info Employee": update,
        "Delete Employee": delete,
        "Show All Data": showAll,
    }

    # Adjust grid to ensure buttons have proper width and spacing
    for idx, (btn_text, btn_command) in enumerate(buttons.items()):
        btn = ctk.CTkButton(
            right_frame,
            text=btn_text,
            command=btn_command,
            width=160,
            font=("Arial", 14),
        )
        btn.grid(row=3, column=idx, padx=10, pady=30, sticky="ew")

    return right_frame
