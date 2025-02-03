import customtkinter as ctk
from Request_Table import update_view, get_data,get_medication_details



def request_window(root):
    datadect = {}
    left_frame = None

    # Initialize customtkinter and main root window
    ctk.set_appearance_mode("Light")  # Modes: "Light", "Dark"
    ctk.set_default_color_theme("blue")  # Themes: "blue", "green", "dark-blue"

    # Create Table Frame
    table_frame = ctk.CTkFrame(root)
    table_frame.grid(row=1, column=1, sticky="nsew")

    # Title Label
    title_label = ctk.CTkLabel(
        table_frame, text="Requests Dashboard", font=("Helvetica", 24, "bold")
    )
    title_label.grid(row=0, column=0, pady=20, padx=20, columnspan=7, sticky="nsew")

    # Define columns (Updated to remove unnecessary columns and add Date)
    columns = (
        "Doctor Name",
        "Doctor ID",
        "Patient Name",
        "Patient Phone",
        "Date",
        "Actions",
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
            
            # Check if the view is null (no medication details)
            doc_name, dr_id, pat_name, pat_phone, date, _ = values
            medications = get_medication_details(doc_name, dr_id, pat_name, pat_phone, date)
            # Add each value to the row
            for col_index, value in enumerate(values):
                if col_index == len(values) - 1:  # Add a button in the Actions column
                    # Check if medications are available (view is not null)
                    if medications[0][3]=="True":
                        button = ctk.CTkButton(
                            self,
                            text="View",
                            font=("Helvetica", 14),
                            command=lambda v=values, btn=None: self.view_action(v, btn),
                        )
                    else:
                        button = ctk.CTkButton(
                            self,
                            text="Not View",
                            font=("Helvetica", 14),
                            fg_color="red",  # Set background to red if view is null
                            command=lambda v=values: self.view_action(v, button),
                        )
                    button.grid(row=row_index, column=col_index, sticky="nsew", pady=2)
                    row_data.append(button)
                else:
                    label = ctk.CTkLabel(
                        self, text=value, font=("Helvetica", 14), padx=5
                    )
                    label.grid(row=row_index, column=col_index, sticky="nsew", pady=2)
                    row_data.append(label)

            self.rows.append(row_data)

        def add_row2(self, values):
            row_index = len(self.rows) + 1
            for col_index, value in enumerate(values):
                label = ctk.CTkLabel(self, text=value, font=("Helvetica", 14), padx=5)
                label.grid(row=row_index, column=col_index, sticky="nsew", pady=2)
            self.rows.append(values)

        def view_action(self, value, button):
            nonlocal left_frame
            if left_frame is not None:
                return
            # If the button text is "Not View", change it to "View" and change color to blue
            if button and button.cget("text") == "Not View":
                button.configure(
                    text="View", fg_color="#169EE7"
                )  # Set button to blue and text to View
                
                update_view(value[0], value[1], value[2], value[3],"True")
            view(value)

    def view(row_data):
        nonlocal left_frame

        # Destroy existing left frame if it exists
        if left_frame is not None:
            return

        # Create new frame for details
        left_frame = ctk.CTkFrame(table_frame, width=300, height=300, corner_radius=15)
        left_frame.place(x=150, y=250)

        # Title Label
        title_label = ctk.CTkLabel(
            left_frame, text="Request Details", font=("Helvetica", 18, "bold")
        )
        title_label.grid(row=0, column=0, columnspan=2, pady=10)

        # Extract relevant details from row_data
        doc_name, dr_id, pat_name, pat_phone, date, _ = row_data

        # Create a table for medication details
        med_table = ModernTable(
            left_frame,
            ("Medication Name", "Category", "Quantity"),
            width=500,
            height=200,
        )
        med_table.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        # Fetch medication details for the current request
        medicationsx = datadect.get((doc_name, dr_id, pat_name, pat_phone, date))
        for med in medicationsx:
          med_table.add_row2(med[:3])

        # Add Exit Button to close the details view
        def exit_view():
            nonlocal left_frame
            if left_frame is not None:
                left_frame.destroy()
                left_frame = None

        exit_button = ctk.CTkButton(left_frame, text="Close", command=exit_view)
        exit_button.grid(row=2, column=0, pady=10)

    # Instantiate ModernTable
    table = ModernTable(table_frame, columns, width=800, height=600)
    table.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

    # Load data and populate the table
    data = get_data()
    for d in data:
        if (d[0], d[1], d[2], d[6], d[8]) not in datadect:
            datadect[(d[0], d[1], d[2], d[6], d[8])] = [(d[3], d[4], d[5], d[7])]
        else:
            datadect[(d[0], d[1], d[2], d[6], d[8])].append((d[3], d[4], d[5], d[7]))
    transformed_data = [
        (row[0], row[1], row[2], row[3], row[4], "") for row in datadect.keys()
    ]
    for row in transformed_data:
        table.add_row(row)

    return table_frame
