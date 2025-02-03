import customtkinter as ctk
import medicine_data
import order_data
import datetime
import random
import string
import order_item_data

totalbill = 0  # the price of billing
totalquntity = {}
# this as dictionary contain the {id of medication : the quantity of this medication}


def billing(root, staff_id):  # the staff id i need for generate the billing
    # =======================================================================================================
    # the backend functions
    def check_id():
        """
        this function check the id of medication in the database or not
        """
        pro_id = item_text.get()  # get the id from the product id label in Gui
        if medicine_data.search_medicine_by_id(pro_id):
            global info
            info = medicine_data.get_infromation(
                pro_id
            )  # get the all information of the medicatoin
            return True
        else:
            return False

    def check_quantity():
        """
        this function check the quantity of medication is correct or not
        """
        pro_qun = quantity_text.get()  # get the quantity from the quantity label in Gui
        try:
            if int(pro_qun) <= 0 or int(pro_qun) > int(info[5]):
                return False
            else:
                return True
        except:
            return False

    def add_item_inbill():
        """
        this function add a new item in the billing (name,quantity,price,total) of medication
        """
        global totalbill
        global totalquntity
        global cid, cqu

        # use the (cid and cqu) print the not valid input individually in product id and quntity id if the id or quantity is not valid
        # the initial value False
        # the (cid and cqu) is true if the id and quantity is valid
        cid = False
        cqu = False

        def clear_item_message_label():
            item_message_label.configure(text="")

        def clear_quntity_message_label():
            quantity_message_label.configure(text="")

        if check_id():
            item_message_label.configure(
                text="the id valid", text_color="green"
            )  # this message print on screen if id valid
            root.after(2000, clear_item_message_label)
            cid = True  # change the cid from False to True
        else:
            item_message_label.configure(
                text="the id is not valid", text_color="red"
            )  # this message print on screen if id not valid
            root.after(
                2000, clear_item_message_label
            )  # Clear the message after 1 seconds (2000 milliseconds)

        if check_quantity() and check_id():
            quantity_message_label.configure(
                text="the quntity valid ", text_color="green"
            )  # this message print on screen if quantity valid
            root.after(
                2000, clear_quntity_message_label
            )  # Clear the message after 1 seconds (2000 milliseconds)
            cqu = True
        else:
            quantity_message_label.configure(
                text="the quntity is not valid", text_color="red"
            )  # this message print on screen if quantity not valid
            root.after(
                2000, clear_quntity_message_label
            )  # Clear the message after 1 seconds (2000 milliseconds)

        if all((cid, cqu)):  # all return True if all item in iterabel is True
            global totalbill
            price = float(info[6])  # Assuming price is in the 6th index
            quantity = int(quantity_text.get())  # get the quanttiy from the label
            total = price * quantity
            totalbill += total
            medicine_data.update_quantity(
                info[1], str(medicine_data.get_quantity_by_id(info[1]) - quantity)
            )  # this function in database (update the quntity of meication)
            if info[1] in totalquntity.keys():
                #  info[i] => the id of medication
                #  update the quntity of the same id medication if mediction repeated in bill
                totalquntity[info[1]] = str(int(totalquntity[info[1]]) + quantity)
            else:
                #  assign a new id and quntity of medication in the bill
                totalquntity[info[1]] = str(quantity)
            textarea.configure(state="normal")
            # Add formatted item details to the invoice
            textarea.insert(
                "end",
                f"{info[0]:<10}  | {quantity:<7} | ${price:<7.2f} | ${total:<7.2f}\n",
            )
            textarea.configure(state="disabled")
            total_label.configure(text=f"Total Price: ${totalbill}")

    def clear_invoices():
        """
        this function clear the bill if not (empty or not generated the bill)
        and return the quntity in the bill in database
        """

        # clear the message of clear label
        def clear_clear_message_label():
            clear_message_label.configure(text="")

        global totalbill
        global totalquntity
        if totalquntity:
            totalbill = 0  # Reset the total bill to 0
            # retrun the quntity in database
            for id, qun in totalquntity.items():
                medicine_data.update_quantity(
                    id, str(medicine_data.get_quantity_by_id(id) + int(qun))
                )  # this function in database (update the quntity of meication)
            # return initial show of invoices screen
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
            clear_message_label.configure(text="Clear Successfully", text_color="green")
            root.after(2000, clear_clear_message_label)
        else:
            clear_message_label.configure(
                text="The Bill is empty", text_color="red"
            )  # this message print on screen if the bill is empty
            root.after(
                2000, clear_clear_message_label
            )  # Clear the message after 1 seconds (2000 milliseconds)

    def gnerate_bill():
        """
        this function generate the bill and save bill in database
        """
        global totalbill
        global totalquntity

        # create a random id as str
        def random_order_id():
            digits = string.digits
            count = 10
            rand_id = ""
            while count > 0:
                rand = random.randint(0, 9)
                rand_id += digits[rand]
                count -= 1
            return rand_id

        # clear the message of generate label
        def clear_generate_message_label():
            generate_message_label.configure(text="")

        if totalquntity:
            order_id = random_order_id()
            while (
                order_id in order_data.get_all_order_ids()
            ):  # loop because the order id is not repeated in database
                order_id = random_order_id()
            current_time = datetime.datetime.now()  # the date of the bill
            formatted_time = current_time.strftime(
                "Date: %d-%m-%Y\nTime: %I:%M:(%p)"
            )  # formating of date
            order_data.add_order(
                order_id, staff_id, totalbill, formatted_time
            )  # add  the order in database
            for id, qun in totalquntity.items():
                order_item_data.add_order_item(
                    order_id,
                    medicine_data.get_name(str(id)),
                    id,
                    qun,
                    medicine_data.get_price_by_id(id),
                )
            totalbill = 0  # Reset the total bill to 0
            # return initial show of invoices screen
            totalquntity = {}
            textarea.configure(state="normal")
            textarea.delete("1.0", "end")
            textarea.insert(
                "end", f"{'Name':<10} | {'Quantity':<7} | {'Price':<7} | {'Total':<7}\n"
            )
            textarea.insert("end", "-" * 50 + "\n")  # Adds a divider line for clarity
            textarea.configure(state="disabled")
            generate_message_label.configure(
                text="Generated Successfully", text_color="green"
            )
            total_label.configure(text="Total Price: $0.00")
            # Clear the message after 1 seconds (2000 milliseconds)
            root.after(1000, clear_generate_message_label)

        else:
            generate_message_label.configure(text="The Bill is empty", text_color="red")
            # Clear the message after 1 seconds (2000 milliseconds)
            root.after(2000, clear_generate_message_label)

    # =======================================================================================================

    # Initialize CustomTkinter settings
    ctk.set_appearance_mode("Light")
    ctk.set_default_color_theme("blue")

    # Create the main frame for the billing page
    billing_frame = ctk.CTkFrame(root)
    billing_frame.grid(row=0, column=1, sticky="nsew", padx=10)

    # Colors and Fonts
    bg_color = "#4169E1"
    font_color = "#E7EBEE"
    font_style = ("Arial", 18, "bold")

    # Title for the Billing Page
    title = ctk.CTkLabel(
        billing_frame,
        text="Billing System",
        text_color=font_color,
        fg_color=bg_color,
        font=("Bodoni MT Black", 25, "bold"),
        corner_radius=6,
    )
    title.grid(row=0, column=0, columnspan=2, pady=10, sticky="nsew")

    # Product Details Section (left side)
    product_frame = ctk.CTkFrame(billing_frame, corner_radius=10, width=400, height=500)
    product_frame.grid(row=1, column=0, padx=15, pady=20, sticky="nsew")

    # Product ID input
    item_label = ctk.CTkLabel(product_frame, text="Product ID", font=font_style)
    item_label.grid(row=1, column=0, padx=20, pady=10, sticky="w")
    item_text = ctk.CTkEntry(
        product_frame, width=250, font=("Arial", 15), placeholder_text="ID:1234"
    )
    item_text.grid(row=1, column=1, padx=20, pady=10)

    # Message label under Product ID
    item_message_label = ctk.CTkLabel(
        product_frame, text="", text_color="gray", font=("Arial", 20)
    )
    item_message_label.grid(
        row=2, column=0, columnspan=2, padx=10, pady=(5, 20), sticky="s"
    )

    # Product Quantity input
    quantity_label = ctk.CTkLabel(
        product_frame, text="Product Quantity", font=font_style
    )
    quantity_label.grid(row=3, column=0, padx=20, pady=10, sticky="w")
    quantity_text = ctk.CTkEntry(
        product_frame, width=250, font=("Arial", 15), placeholder_text="7"
    )
    quantity_text.grid(row=3, column=1, padx=20, pady=10)

    # Message label under Product Quantity
    quantity_message_label = ctk.CTkLabel(
        product_frame, text="", text_color="gray", font=("Arial", 20)
    )
    quantity_message_label.grid(
        row=4, column=0, columnspan=2, padx=10, pady=(5, 20), sticky="s"
    )

    # Action buttons
    btn_add = ctk.CTkButton(
        product_frame, text="Add Item", width=150, command=add_item_inbill
    )
    btn_add.grid(row=5, column=0, padx=10, pady=30)
    # Message label under Product Quantity

    btn_generate = ctk.CTkButton(
        product_frame,
        text="Generate Bill",
        width=150,
        command=gnerate_bill,
    )
    btn_generate.grid(row=5, column=1, padx=10, pady=30)

    generate_message_label = ctk.CTkLabel(
        product_frame, text="", text_color="gray", font=("Arial", 28, "bold")
    )
    generate_message_label.grid(
        row=8, column=0, columnspan=2, padx=10, pady=(10, 20), sticky="s"
    )

    btn_clear = ctk.CTkButton(
        product_frame, text="Clear", width=150, command=clear_invoices
    )
    btn_clear.grid(row=6, column=0, padx=10, pady=30)
    clear_message_label = ctk.CTkLabel(
        product_frame, text="", text_color="gray", font=("Arial", 30, "bold")
    )
    clear_message_label.grid(
        row=8, column=0, columnspan=2, padx=10, pady=(10, 20), sticky="s"
    )

    # Invoice Section (right side)
    invoice_frame = ctk.CTkFrame(billing_frame, corner_radius=10, width=700, height=500)
    invoice_frame.grid(row=1, column=1, padx=15, pady=20, sticky="nsew")

    # Invoice Title
    invoice_label = ctk.CTkLabel(
        invoice_frame,
        text="Invoice Details",
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
        width=280,  # Match or align with the new frame width
        height=300,  # Match or align with the new frame height
    )

    textarea.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
    scroll_y.configure(command=textarea.yview)
    textarea.configure(state="normal")
    textarea.insert(
        "end", f"{'Name':<10} | {'Quantity':<7} | {'Price':<7} | {'Total':<7}\n"
    )
    textarea.insert("end", "-" * 50 + "\n")  # Adds a divider line for clarity
    textarea.configure(state="disabled")

    # Displaying some static content in the  (for example purposes

    # Total Price Label (initialized to $0.00)
    total_label = ctk.CTkLabel(
        invoice_frame,
        text="Total Price: $0.00",
        font=("Arial", 16, "bold"),
        text_color="#FFFFFF",
        fg_color="#0078D4",
    )
    total_label.grid(row=2, column=0, pady=10, sticky="nsew")

    # Return the billing frame
    return billing_frame


def handle_action(action):
    try:
        print(action)
    except Exception as e:
        print(f"Error occurred while processing action: {e}")
