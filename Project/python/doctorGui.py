import customtkinter as ctk
from tkinter import *
from PIL import Image, ImageTk
from customtkinter import *
import login
import medicine_data
import re
import Request_Table

totalbill = 0  # the price of billing
totalquntity = {}


# this as dictionary contain the {id of medication : the quantity of this medication}
def doctor_window(root, information):
    ctk.set_appearance_mode("Light")
    ctk.set_default_color_theme("blue")

    def add_item():
        def check_quantity():
            """
            this function check the quantity of medication is correct or not
            """
            pro_qun = (
                quantity_entry.get().strip()
            )  # get the quantity from the quantity label in Gui
            try:
                if int(pro_qun) <= 0 or int(pro_qun) > int(info[5]):
                    return False
                else:
                    return True
            except:
                return False

        name = medication_entry.get().strip().title()
        quntity = quantity_entry.get().strip()
        cat = category_enter.get().title()
        info = medicine_data.get_infromation_cate_name(
            cat, name
        )  # (name,id,category,production_date , expiry_date, quantity, price)
        if info:
            try:
                if int(quntity) > 0:
                    if check_quantity():
                        global totalbill
                        price = float(info[6])  # Assuming price is in the 6th index
                        total = price * int(quntity)
                        totalbill += total
                        q = medicine_data.get_quantity_by_id(info[1])
                        test = True
                        if info[1] in totalquntity.keys():
                            totalquntity[info[1]] = str(
                                int(totalquntity[info[1]]) + int(quntity)
                            )
                            if int(totalquntity[info[1]]) > int(
                                q
                            ):  # check if the quntity large of quntity in database
                                generate_message_label.configure(
                                    text="The Quntity not valid", text_color="red"
                                )
                                root.after(
                                    2000,
                                    lambda: generate_message_label.configure(text=""),
                                )
                                test = False
                        else:
                            #  assign a new id and quntity of medication in the bill
                            totalquntity[info[1]] = str(quntity)
                            if int(quntity) > int(q):
                                generate_message_label.configure(
                                    text="The Quntity not valid", text_color="red"
                                )
                                del totalquntity[info[1]]
                                root.after(
                                    2000,
                                    lambda: generate_message_label.configure(text=""),
                                )
                                test = False
                        if test:
                            textarea.configure(state="normal")
                            # Add formatted item details to the invoice
                            textarea.insert(
                                "end",
                                f"{info[0]:<10}  | {quntity:<7} | ${price:<7.2f} | ${total:<7.2f}\n",
                            )
                            textarea.configure(state="disabled")
                            total_label.configure(text=f"Total Price: ${totalbill}")
                    else:
                        generate_message_label.configure(
                            text="The Quntity not valid", text_color="red"
                        )
                        root.after(
                            2000, lambda: generate_message_label.configure(text="")
                        )
                else:
                    generate_message_label.configure(
                        text="The Quntity not valid", text_color="red"
                    )
                    root.after(2000, lambda: generate_message_label.configure(text=""))
            except:
                generate_message_label.configure(
                    text="The category or Name or\nQuntity not valid ", text_color="red"
                )
                root.after(2000, lambda: generate_message_label.configure(text=""))
        else:
            generate_message_label.configure(
                text="The category or Name not valid", text_color="red"
            )
            root.after(2000, lambda: generate_message_label.configure(text=""))

    def clear_invoices():
        """
        this function clear the bill if not (empty or not generated the bill)
        and return the quntity in the bill in database
        """

        # clear the message of clear label
        def clear_clear_message_label():
            generate_message_label.configure(text="")

        global totalbill
        global totalquntity
        if totalquntity:
            totalbill = 0  # Reset the total bill to 0
            totalquntity = {}
            textarea.configure(state="normal")
            textarea.delete("1.0", "end")
            textarea.insert(
                "end", f"{'Name':<10} | {'Quantity':<7} | {'Price':<7} | {'Total':<7}\n"
            )
            textarea.insert("end", "-" * 50 + "\n")  # Adds a divider line for clarity
            textarea.configure(state="disabled")
            # Reset the total price label
            total_label.configure(text="Total Price: $0.00")
            generate_message_label.configure(
                text="Clear Successfully", text_color="green"
            )
            medication_entry.delete(0, "end")
            quantity_entry.delete(0, "end")
            category_enter.delete(0, "end")
            root.after(2000, clear_clear_message_label)
        else:
            generate_message_label.configure(
                text="The Bill is empty", text_color="red"
            )  # this message print on screen if the bill is empty
            root.after(
                2000, clear_clear_message_label
            )  # Clear the message after 1 seconds (2000 milliseconds)

    def gnerate_bill(info):
        generate_message_label = ctk.CTkLabel(
            product_frame, text="", text_color="gray", font=("Arial", 28, "bold")
        )
        generate_message_label.grid(
            row=8, column=0, columnspan=2, padx=10, pady=(10, 20), sticky="s"
        )
        global totalbill
        global totalquntity
        cusname = customer_name_entry.get().strip()
        cusphone = customer_phone_entry.get().strip()
        if totalquntity:
            if cusname:
                if cusphone:
                    if bool(
                        re.match(r"^[a-zA-Z\s]+$", cusname)
                    ):  # check the customer name is letter only
                        if cusphone.isdigit():
                            if int(cusphone) != 0:
                                if len(cusphone) == 11:
                                    for id, qun in totalquntity.items():
                                        Request_Table.add_order(
                                            info[2],
                                            info[3],
                                            cusname,
                                            medicine_data.get_name(id),
                                            category_enter.get().title(),
                                            qun,
                                            cusphone,
                                        )
                                    totalbill = 0  # Reset the total bill to 0
                                    # return initial show of invoices screen
                                    totalquntity = {}
                                    textarea.configure(state="normal")
                                    textarea.delete("1.0", "end")
                                    textarea.insert(
                                        "end",
                                        f"{'Name':<10} | {'Quantity':<7} | {'Price':<7} | {'Total':<7}\n",
                                    )
                                    textarea.insert(
                                        "end", "-" * 50 + "\n"
                                    )  # Adds a divider line for clarity
                                    textarea.configure(state="disabled")
                                    generate_message_label.configure(
                                        text="Generated Successfully",
                                        text_color="green",
                                    )
                                    medication_entry.delete(0, "end")
                                    quantity_entry.delete(0, "end")
                                    category_enter.delete(0, "end")
                                    customer_name_entry.delete(0, "end")
                                    customer_phone_entry.delete(0, "end")
                                    total_label.configure(text="Total Price: $0.00")
                                    # Clear the message after 1 seconds (1000 milliseconds)
                                    root.after(
                                        1000,
                                        lambda: generate_message_label.configure(
                                            text=""
                                        ),
                                    )
                                else:
                                    generate_message_label.configure(
                                        text="The customer phone must be 11 number",
                                        text_color="red",
                                    )
                                    root.after(
                                        2000,
                                        lambda: generate_message_label.configure(
                                            text=""
                                        ),
                                    )
                            else:
                                generate_message_label.configure(
                                    text="The customer phone not Accepted",
                                    text_color="red",
                                )
                                root.after(
                                    2000,
                                    lambda: generate_message_label.configure(text=""),
                                )
                        else:
                            generate_message_label.configure(
                                text="The customer phone must be digits",
                                text_color="red",
                            )
                            root.after(
                                2000, lambda: generate_message_label.configure(text="")
                            )
                    else:
                        generate_message_label.configure(
                            text="The customer name must be letter only",
                            text_color="red",
                        )
                        root.after(
                            2000, lambda: generate_message_label.configure(text="")
                        )
                else:
                    generate_message_label.configure(
                        text="The customer phone required", text_color="red"
                    )
                    root.after(2000, lambda: generate_message_label.configure(text=""))

            else:
                generate_message_label.configure(
                    text="The customer name required", text_color="red"
                )
                root.after(2000, lambda: generate_message_label.configure(text=""))
        else:
            generate_message_label.configure(text="The Bill empty", text_color="red")
            root.after(2000, lambda: generate_message_label.configure(text=""))

    # Create the main frame for the billing page
    billing_frame = ctk.CTkFrame(root)
    billing_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=(50, 20))

    # Colors and Fonts
    bg_color = "#4169E1"
    font_color = "#E7EBEE"
    font_style = ("Arial", 18, "bold")

    # Title for the Billing Page
    title = ctk.CTkLabel(
        billing_frame,
        text="Electronic Prescription",
        text_color=font_color,
        fg_color=bg_color,
        font=("Bodoni MT Black", 25, "bold"),
        corner_radius=6,
    )
    title.grid(row=0, column=0, columnspan=2, pady=10, sticky="nsew")

    # Customer Details Frame (Separate Frame for Name and Phone)
    customer_frame = ctk.CTkFrame(
        billing_frame, corner_radius=10, width=400, height=150
    )
    customer_frame.grid(row=2, column=0, padx=15, pady=10, sticky="nsew")

    # Customer Name input
    customer_name_label = ctk.CTkLabel(
        customer_frame, text="Customer Name", font=font_style
    )
    customer_name_label.grid(row=0, column=0, padx=20, sticky="w")
    customer_name_entry = ctk.CTkEntry(customer_frame, width=250, font=("Arial", 15))
    customer_name_entry.grid(row=0, column=1, padx=20, pady=10)

    # Customer Phone Number input
    customer_phone_label = ctk.CTkLabel(
        customer_frame, text="Phone Number", font=font_style
    )
    customer_phone_label.grid(row=1, column=0, padx=20, sticky="w")
    customer_phone_entry = ctk.CTkEntry(customer_frame, width=250, font=("Arial", 15))
    customer_phone_entry.grid(row=1, column=1, padx=20, pady=10)

    # Product Details Frame (Separate Frame for Medication Details)
    product_frame = ctk.CTkFrame(billing_frame, corner_radius=10, width=400, height=500)
    product_frame.grid(row=3, column=0, padx=15, pady=10, sticky="nsew")

    # Medication Name input
    medication_label = ctk.CTkLabel(
        product_frame, text="Medication Name", font=font_style
    )
    medication_label.grid(row=0, column=0, padx=20, sticky="w")
    medication_entry = ctk.CTkEntry(product_frame, width=250, font=("Arial", 15))
    medication_entry.grid(row=0, column=1, padx=20, pady=10)

    # Medication Quantity input
    quantity_label = ctk.CTkLabel(
        product_frame, text="Medication Quantity", font=font_style
    )
    quantity_label.grid(row=1, column=0, padx=20, pady=10, sticky="w")
    quantity_entry = ctk.CTkEntry(product_frame, width=250, font=("Arial", 15))
    quantity_entry.grid(row=1, column=1, padx=20, pady=10)

    category_label = ctk.CTkLabel(
        product_frame, text="Medication Category", font=font_style
    )
    category_label.grid(row=3, column=0, padx=20, pady=10, sticky="w")
    category_enter = ctk.CTkEntry(product_frame, width=250, font=("Arial", 15))
    category_enter.grid(row=3, column=1, padx=20, pady=10)

    # Action buttons
    btn_add = ctk.CTkButton(product_frame, text="Add Item", width=150, command=add_item)
    btn_add.grid(row=4, column=0, padx=10, pady=30)

    btn_generate = ctk.CTkButton(
        product_frame,
        text="Generate RX",
        width=150,
        command=lambda: gnerate_bill(information),
    )
    btn_generate.grid(row=4, column=1, padx=10, pady=30)
    generate_message_label = ctk.CTkLabel(
        product_frame, text="", text_color="gray", font=("Arial", 28, "bold")
    )
    generate_message_label.grid(
        row=8, column=0, columnspan=2, padx=10, pady=(10, 20), sticky="s"
    )

    btn_clear = ctk.CTkButton(
        product_frame, text="Clear", width=150, command=clear_invoices
    )
    btn_clear.grid(row=5, column=0, padx=10, pady=30)

    # Invoice Section (right side)
    invoice_frame = ctk.CTkFrame(billing_frame, corner_radius=10, width=700, height=500)
    invoice_frame.grid(row=1, column=1, rowspan=3, padx=15, pady=20, sticky="nsew")

    # Invoice Title
    invoice_label = ctk.CTkLabel(
        invoice_frame,
        text="Prescription Area",
        font=("Arial", 22, "bold"),
        text_color="#FFFFFF",
        fg_color="#0078D4",
    )
    invoice_label.grid(row=0, column=0, pady=20, sticky="nsew")

    # Scrollbar for the invoice content
    scroll_y = ctk.CTkScrollbar(invoice_frame, orientation="vertical")
    scroll_y.grid(row=1, column=1, sticky="ns")

    # Text area to show the invoice content (non-editable)
    textarea = ctk.CTkTextbox(
        invoice_frame,
        font=("Arial", 14),
        yscrollcommand=scroll_y.set,
        wrap="word",
        state="disabled",
        width=280,
        height=300,
    )
    textarea.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
    scroll_y.configure(command=textarea.yview)
    textarea.configure(state="normal")
    textarea.insert(
        "end", f"{'Name':<10} | {'Quantity':<7} | {'Price':<7} | {'Total':<7}\n"
    )
    textarea.insert("end", "-" * 50 + "\n")
    textarea.configure(state="disabled")
    # Total Price Label (initialized to $0.00)
    total_label = ctk.CTkLabel(
        invoice_frame,
        text="Total Price: $0.00",
        font=("Arial", 16, "bold"),
        text_color="#FFFFFF",
        fg_color="#0078D4",
    )
    total_label.grid(row=2, column=0, pady=10, sticky="nsew")

    return billing_frame


def doctor_page(information, root):
    # =======================================================================================================
    # =======================================================================================================
    # =======================================================================================================
    # Function to handle login backend
    def go_home():
        for widget in root.grid_slaves(row=0, column=1):
            widget.destroy()

        # Add a background image on the right (initial state)
        bg_image = Image.open(r"Project\image\medical-composition-with-pills.jpg")
        bg_image = bg_image.resize((850, 500), Image.Resampling.LANCZOS)
        bg_photo = ImageTk.PhotoImage(bg_image)

        bg_label = Label(root, image=bg_photo)
        bg_label.image = bg_photo  # Keep reference to prevent garbage collection
        bg_label.grid(row=0, column=1, sticky="nsew")

    def show_request(information):
        for widget in root.grid_slaves(row=0, column=1):
            widget.destroy()
        billing_frame = doctor_window(root, information)
        billing_frame.grid(row=0, column=1, sticky="nsew")

    def logout():
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
        login.login(root)

    # =======================================================================================================
    # =======================================================================================================
    # =======================================================================================================
    root.grid_rowconfigure(0, weight=1)  # Allow row 0 to expand
    root.grid_columnconfigure(0, weight=0)  # Fix column 0 (frame column)
    root.grid_columnconfigure(1, weight=1)  # Allow column 1 (image) to expand

    frame1 = CTkFrame(root, fg_color="#D9D9D9", corner_radius=20)
    frame1.grid(row=0, column=0, padx=10, sticky="ns")

    bg_image = Image.open(r"Project\image\medical-composition-with-pills.jpg")
    bg_image = bg_image.resize((850, 500), Image.Resampling.LANCZOS)
    bg_photo = ImageTk.PhotoImage(bg_image)

    bg_label = Label(root, image=bg_photo)
    bg_label.image = bg_photo  # Keep reference
    bg_label.grid(row=0, column=1, sticky="nsew")

    data_display = LabelFrame(
        frame1,
        text="User Data",
        font=("Arial", 14),
        bg="#f5f5f5",
        fg="black",
        labelanchor="n",
    )
    data_display.pack(pady=20, padx=10, fill="x")

    user_data_label = Label(
        data_display,
        text=f"Name: {information[2]}\nID: {information[3]} \nUsername: {information[0]}\nStatus: Active",
        font=("Arial", 12),
        bg="white",
        justify="left",
        anchor="nw",
    )
    user_data_label.pack(pady=10, padx=10, fill="both", expand=True)

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

    btn1 = Button(
        frame1,
        text="New Request",
        font=("Arial", 16),
        bg="#80C7E7",
        width=25,
        relief="flat",
        command=lambda: show_request(information),
    )
    btn1.pack(pady=8)

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

    return root

