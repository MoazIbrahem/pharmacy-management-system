import customtkinter as ctk
from tkinter.messagebox import showinfo
import re
import medicine_data
import datetime
import testing
# Staff Management (Billing Interface)
def inentory_window(root):
    # Set appearance
    ctk.set_appearance_mode("Light")
    ctk.set_default_color_theme("blue")
    left_frame = None
    # =======================================================================================================
    # =======================================================================================================
    # =======================================================================================================
    # the backend functions

    def additm():
        nonlocal left_frame  # Use the outer scoped variable for left_frame
      # Check if the frame already exists
        if left_frame is not None:
            return  # If the frame exists, do not create it again
        # Create the Left Frame for Input Fields
        
        left_frame = ctk.CTkFrame(root, width=300, height=700, corner_radius=15)
        left_frame.place(x=600)

        # Input Fields in Left Frame
        labels = ["Name", "id", "category", "production_date[d/m/y]", "expiry_date[d/m/y]", "quantity","price"]
        entries = {} 
        messages = {} 

        for idx, label in enumerate(labels,start=1):
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
              # Title for the Billing Page
            title = ctk.CTkLabel(
                left_frame,
                text=testing.syntax_ex,
                text_color=font_color,
                fg_color=bg_color,
                font=("Arial",14),
                corner_radius=6,
            )
            title.grid(row=0, column=0, columnspan=4, pady=10, sticky="ew")

        # Function to handle saving the employee data
        def save_medication():
            cname = cid = ccat = cprodate = cexp = cqun = cpri = False
            def clear_Name_message_label():
                messages["Name"].configure(text="")

            def clear_ID_message_label():
                messages["id"].configure(text="")
                
            def clear_category_message_label():
                messages["category"].configure(text="")

            def clear_production_date_message_label():
                messages["production_date[d/m/y]"].configure(text="")

            def clear_expiry_date_message_label():
                messages["expiry_date[d/m/y]"].configure(text="")

            def clear_quantity_message_label():
                messages["quantity"].configure(text="")
            def clear_price_message_label():
                messages["price"].configure(text="")

            if not entries["Name"].get().strip():
                messages["Name"].configure(text="Name is required.")
                root.after(800, clear_Name_message_label)
                cname = False
            elif not bool(
                re.match(r"^[a-zA-Z\s]+$", str(entries["Name"].get().strip()).strip())
            ):
                messages["Name"].configure(text="Name must be contain letters only")
                root.after(800, clear_Name_message_label)
                cname = False
            else:
                cname = True

            if not entries["id"].get().strip():
                messages["id"].configure(text="ID is required.")
                root.after(800, clear_ID_message_label)
                cid = False
            elif medicine_data.search_medicine_by_id(entries["id"].get().strip()):
                messages["id"].configure(text="is already taken")
                root.after(800, clear_ID_message_label)
                cid = False
            elif not str(entries["id"].get().strip()).isdigit():
                messages["id"].configure(text="ID must be contain digits only")
                root.after(800, clear_ID_message_label)
                cid = False
            elif len(entries["id"].get().strip()) < 10:
                messages["id"].configure(text="is too short (minimum is 10 digits)")
                root.after(800, clear_ID_message_label)
                cid = False
            else:
                cid = True



            if not entries["category"].get().strip():
                messages["category"].configure(text="category is required.")
                root.after(800, clear_category_message_label)
                ccat = False
            elif not bool(
                re.match(r"^[a-zA-Z\s]+$", str(entries["Name"].get().strip()).strip())
            ):
                messages["category"].configure(
                    text="category must be contain letters only"
                )
                root.after(800, clear_category_message_label)
                ccat = False
            else:
                ccat = True

            mysplit1=testing.split_str(entries["production_date[d/m/y]"].get().strip())
            if not entries["production_date[d/m/y]"].get().strip():
                messages["production_date[d/m/y]"].configure(text="production_date is required.")
                root.after(800, clear_production_date_message_label)
                cprodate = False
            elif not testing.Accept_pattern(entries["production_date[d/m/y]"].get().strip()):
                messages["production_date[d/m/y]"].configure(text="Invalid Syntax")
                root.after(800, clear_production_date_message_label)
                cprodate = False
            elif not testing.check_date(mysplit1[0],mysplit1[1],mysplit1[2]):
                messages["production_date[d/m/y]"].configure(text="Invalid Date")
                root.after(800, clear_production_date_message_label)
                cprodate = False
            else:
                cprodate = True

            mysplit2=testing.split_str(entries["expiry_date[d/m/y]"].get().strip())
            if not entries["expiry_date[d/m/y]"].get().strip():
                messages["expiry_date[d/m/y]"].configure(text="expiry_date is required.")
                root.after(800, clear_expiry_date_message_label)
                cexp = False
            elif not testing.Accept_pattern(entries["expiry_date[d/m/y]"].get().strip()):
                messages["expiry_date[d/m/y]"].configure(text="Invalid Syntax")
                root.after(800, clear_expiry_date_message_label)
                cexp = False
            elif not testing.check_date(mysplit2[0],mysplit2[1],mysplit2[2]):
                messages["expiry_date[d/m/y]"].configure(text="Invalid Date")
                root.after(800, clear_expiry_date_message_label)
                cexp = False
            elif datetime.date(int(mysplit2[2]),int(mysplit2[1]),int(mysplit2[0]))<= datetime.datetime.date(datetime.datetime.now()):
                messages["expiry_date[d/m/y]"].configure(text="the medication expire")
                root.after(800, clear_expiry_date_message_label)
            else:
                cexp = True

            if not entries["quantity"].get().strip():
                messages["quantity"].configure(text="Quantity is required.")
                root.after(800, clear_quantity_message_label)
                cqun = False
            elif not str(entries["quantity"].get().strip()).isdigit():
                messages["quantity"].configure(text="Quantity must be contain digits only")
                root.after(800, clear_quantity_message_label)
                cqun = False
            elif int(entries["quantity"].get().strip()) == 0:
                messages["quantity"].configure(text="Quantity not valid")
                root.after(800, clear_quantity_message_label)
                cqun = False
            else:
                cqun = True

            if not entries["price"].get().strip():
                messages["price"].configure(text="price is required.")
                root.after(800, clear_price_message_label)
                cpri = False
            elif not str(entries["price"].get().strip()).isdigit():
                messages["price"].configure(text="price must be contain digits only")
                root.after(800, clear_price_message_label)
                cpri = False
            elif int(entries["price"].get().strip()) == 0:
                messages["price"].configure(text="price not valid")
                root.after(800, clear_price_message_label)
                cpri = False
            else:
                cpri = True


            if all([cname, cid, ccat, cid, cprodate, cexp, cqun, cpri]):
                  medication_data = [entries[label].get().strip().title() for label in labels]
                  medicine_data.add_new_medicine(medication_data[0],medication_data[1],medication_data[2],medication_data[3],medication_data[4],medication_data[5],medication_data[6])
                  save_message_label.configure(
                      text="Saved Successfully", text_color="green"
                  )
                  root.after(800, lambda: save_message_label.configure(text=""))
                  for entry in entries.values():
                    entry.delete(0, "end")  



        # Create the "Save" button
        save_btn = ctk.CTkButton(
            left_frame,
            text="Save",
            command=save_medication,
            width=180,
            font=("Arial", 14),
        )
        save_btn.grid(row=len(labels) * 2+2, column=0, columnspan=2, pady=20)
        save_message_label = ctk.CTkLabel(
            left_frame, text="", text_color="gray", font=("Arial", 20)
        )
        save_message_label.grid(row=len(labels) * 2 + 7, column=0, columnspan=2)

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
        exit_btn.grid(row=len(labels) * 2 + 3, column=0, columnspan=2, pady=10)

    def update():
        nonlocal left_frame  # Use the outer scoped variable for left_frame
        # Check if the frame already exists
        if left_frame is not None:
            return  # If the frame exists, do not create it again

        def GO_search():
          def save_changes():
            upbox=search_boxup2.get().strip() # the box what admin need updated
            up=search_entryUP2.get().strip() # The value updated
            if upbox=="Name":
                if up: # check the label is empty or not(1)
                      if bool(
                          re.match(r"^[a-zA-Z\s]+$", str(up).strip())
                        ):# check if Name contain the (2)
                        medicine_data.update_Name(search_entryUP.get().strip(),up)
                        save_message_labelup.configure(text="Saved Successfully",text_color="green")
                        root.after(800,lambda:save_message_labelup.configure(text=""))
                      else:
                        save_message_labelup.configure(text="the name must be contain letter",text_color="red")#(2)
                        root.after(800,lambda:save_message_labelup.configure(text=""))
                else:
                  save_message_labelup.configure(text="Name is required",text_color="red")#(1)
                  root.after(800,lambda:save_message_labelup.configure(text=""))
            elif upbox=="ID":
                if up:# check the label is empty or not(1)
                  if search_entryUP.get().strip()!=up:# check the new id is the same old or not(2)
                    if not (medicine_data.search_medicine_by_id(up)):#check the new id is repeated in database or not (3)
                        if up.isdigit():# check the id is number or not(4)
                          if len(up)>=10: # check len(new id) large than 10 size (5)
                            medicine_data.update_id(search_entryUP.get().strip(),up)
                            search_entryUP2.delete(0,"end")
                            # return the intial screen 
                            message_labelup.configure(text="Saved Successfully",text_color="green")
                            for widget in left_frame.grid_slaves(row=6, column=2):
                                  widget.destroy()
                            for widget in left_frame.grid_slaves(row=6, column=3):
                                  widget.destroy()
                            for widget in left_frame.grid_slaves(row=7, column=2):
                                  widget.destroy()
                            for widget in left_frame.grid_slaves(row=9, column=2):
                                  widget.destroy()
                            search_entryUP.delete(0,"end")
                            root.after(800,lambda:message_labelup.configure(text=""))
                          else:
                            save_message_labelup.configure(text="is too short (minimum is 10 digits)",text_color="red")#(5)
                            root.after(800,lambda:save_message_labelup.configure(text=""))
                        else:
                            save_message_labelup.configure(text="The id must be digits",text_color="red")#(4)
                            root.after(800,lambda:save_message_labelup.configure(text=""))
                    else:
                      save_message_labelup.configure(text="is already taken",text_color="red")#(3)
                      root.after(800,lambda:save_message_labelup.configure(text=""))
                else:
                    save_message_labelup.configure(text="ID required",text_color="red")#(3)
                    root.after(800,lambda:save_message_labelup.configure(text=""))
            elif upbox=="category":
                if up: # check the label is empty or not(1)
                      if bool(
                          re.match(r"^[a-zA-Z\s]+$", str(up).strip())
                        ):# check if Name contain the (2)
                        medicine_data.update_category(search_entryUP.get().strip(),up)
                        save_message_labelup.configure(text="Saved Successfully",text_color="green")
                        root.after(800,lambda:save_message_labelup.configure(text=""))
                        search_entryUP2.delete(0,"end")
                      else:
                        save_message_labelup.configure(text="the category must be contain letter",text_color="red")#(2)
                        root.after(800,lambda:save_message_labelup.configure(text=""))
                else:
                  save_message_labelup.configure(text="category is required",text_color="red")#(1)
                  root.after(800,lambda:save_message_labelup.configure(text=""))
            elif upbox=="production_date":
              mysplit1=testing.split_str(up.strip())
              if up.strip():
                  if testing.Accept_pattern(up.strip()):
                    if testing.check_date(mysplit1[0],mysplit1[1],mysplit1[2]):
                        medicine_data.update_production_date(search_entryUP.get().strip(),up)
                        save_message_labelup.configure(text="Saved Successfully",text_color="green")
                        root.after(800,lambda:save_message_labelup.configure(text=""))
                        search_entryUP2.delete(0,"end")
                        
                    else:
                        save_message_labelup.configure(text="Invalid Date")
                        root.after(800,lambda:save_message_labelup.configure(text=""))
                  else:
                      save_message_labelup.configure(text="Invalid Syntax")
                      root.after(800,lambda:save_message_labelup.configure(text=""))
              else:
                  save_message_labelup.configure(text="production_date is required")
                  root.after(800,lambda:save_message_labelup.configure(text=""))
            elif upbox=="expiry_date":
              mysplit1=testing.split_str(up.strip())
              if up.strip():
                  if testing.Accept_pattern(up.strip()):
                    if testing.check_date(mysplit1[0],mysplit1[1],mysplit1[2]):
                        if not (datetime.date(int(mysplit1[2]),int(mysplit1[1]),int(mysplit1[0]))<= datetime.datetime.date(datetime.datetime.now())):
                          medicine_data.update_expiry_date(search_entryUP.get().strip(),up)
                          save_message_labelup.configure(text="Saved Successfully",text_color="green")
                          root.after(800,lambda:save_message_labelup.configure(text=""))
                          search_entryUP2.delete(0,"end")
                        else:
                          save_message_labelup.configure(text="the medication expire")
                          root.after(800,lambda:save_message_labelup.configure(text=""))
                    else:
                        save_message_labelup.configure(text="Invalid Date",text_color="red")
                        root.after(800,lambda:save_message_labelup.configure(text=""))
                  else:
                      save_message_labelup.configure(text="Invalid Syntax",text_color="red")
                      root.after(800,lambda:save_message_labelup.configure(text=""))
              else:
                  save_message_labelup.configure(text="expiry_date is required",text_color="red")
                  root.after(800,lambda:save_message_labelup.configure(text=""))
            elif upbox=="quantity":
              if up:
                  if up.isdigit():
                    if int(up)!=0:
                          medicine_data.update_quantity(search_entryUP.get().strip(),up)
                          save_message_labelup.configure(text="Saved Successfully",text_color="green")
                          root.after(800,lambda:save_message_labelup.configure(text=""))
                          search_entryUP2.delete(0,"end")
                    else:
                      save_message_labelup.configure(text="Invaild Quntity",text_color="red")
                      root.after(800,lambda:save_message_labelup.configure(text=""))
                  else:
                    save_message_labelup.configure(text="Quantity must be contain digits only",text_color="red")
                    root.after(800,lambda:save_message_labelup.configure(text=""))
              else:
                  save_message_labelup.configure(text="Quntity is required",text_color="red")
                  root.after(800,lambda:save_message_labelup.configure(text=""))
            elif upbox=="price":
              if up:
                  if up.isdigit():
                    if int(up)!=0:
                          medicine_data.update_price(search_entryUP.get().strip(),up)
                          save_message_labelup.configure(text="Saved Successfully",text_color="green")
                          root.after(800,lambda:save_message_labelup.configure(text=""))
                          search_entryUP2.delete(0,"end")
                    else:
                      save_message_labelup.configure(text="Invaild Price",text_color="red")
                      root.after(800,lambda:save_message_labelup.configure(text=""))
                  else:
                    save_message_labelup.configure(text="Price must be contain digits only",text_color="red")
                    root.after(800,lambda:save_message_labelup.configure(text=""))
              else:
                  save_message_labelup.configure(text="Price is required",text_color="red")
                  root.after(800,lambda:save_message_labelup.configure(text=""))
            else:
              message_labelup.configure(text="Error",text_color="red")
              root.after(800,lambda:message_labelup.configure(text=""))

          if search_entryUP.get().strip():
            if medicine_data.search_medicine_by_id(search_entryUP.get().strip()):
              message_labelup.configure(text="what do you wnat update",text_color="green")
              search_boxup2 = ctk.CTkComboBox(
                    left_frame,
                    values=[
                          "Name",
                          "ID",
                          "category",
                          "production_date",
                          "expiry_date",
                          "quantity",
                          "price",
                          ],
                    width=100,
                    font=("Arial", 14),
                    )
              search_boxup2.grid(row=6, column=2, padx=10, sticky="w")
              search_entryUP2 = ctk.CTkEntry(left_frame, width=250, font=("Arial", 14))
              search_entryUP2.grid(row=6, column=3, padx=3, sticky="w")
              # Create the "Save" button
              save_up = ctk.CTkButton(
              left_frame,
              text="Save",
              width=180,
              font=("Arial", 14),
              command=save_changes
              )
              save_up.grid(row=7, column=2, columnspan=2, pady=20)
              save_message_labelup = ctk.CTkLabel(
              left_frame, text="", text_color="gray", font=("Arial", 20)
             )
              save_message_labelup.grid(row=9, column=2, columnspan=2)
            else:
                message_labelup.configure(text="The ID NOT correct",text_color="red")
                root.after(800,lambda:message_labelup.configure(text=""))
          else:
              message_labelup.configure(text="ID is required",text_color="red")
        left_frame = ctk.CTkFrame(root, width=600, height=500, corner_radius=15)
        left_frame.place(x=500, y=200)
        # Search Area
        title = ctk.CTkLabel(
        left_frame,
        text=f"Enter the Medication ID\n{testing.syntax_ex}",
        text_color=font_color,
        fg_color=bg_color,
        font=("Bodoni MT Black", 20, "bold"),
        corner_radius=6,
              )
        title.grid(row=0, column=0, columnspan=4, pady=10, sticky="ew")
        search_la = ctk.CTkLabel(left_frame, text="Medication ID :", font=font_style)
        search_la.grid(row=1, column=0,sticky="w")
        search_entryUP = ctk.CTkEntry(left_frame, width=250, font=("Arial", 14))
        search_entryUP.grid(row=1, column=3, padx=3, sticky="w")
        # Create a message label placed below each entry field
        message_labelup = ctk.CTkLabel(
                left_frame, text="", text_color="red", font=("Arial", 17,"bold")
            )
        message_labelup.grid(
                row=6, column=0,sticky="w",pady=10
            )  # Message label under entry field
        search_btnup = ctk.CTkButton(left_frame, text="Go", width=250,command=GO_search)
        search_btnup.grid(row=2, column=3, padx=3,pady=5,sticky="w")
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
        exit_btn.grid(row=2 , column=1, columnspan=2,padx=5)

    def delete():
        nonlocal left_frame  # Use the outer scoped variable for left_frame
        # Check if the frame already exists
        if left_frame is not None:
            return  # If the frame exists, do not create it again

        def save_changes():
          if search_entryUP.get().strip():
            if medicine_data.search_medicine_by_id(search_entryUP.get().strip()):
                medicine_data.remove_medicine(search_entryUP.get().strip())
                message_labelup.configure(text="Deleted Successfully",text_color="green")
                root.after(800,lambda:message_labelup.configure(text=""))
                search_entryUP.delete(0,"end") 
            else:
                message_labelup.configure(text="The ID NOT correct",text_color="red")
                root.after(800,lambda:message_labelup.configure(text=""))
          else:
              message_labelup.configure(text="ID is required",text_color="red")
        left_frame = ctk.CTkFrame(root, width=600, height=500, corner_radius=15)
        left_frame.place(x=500, y=200)
        # Search Area
        title = ctk.CTkLabel(
        left_frame,
        text="Enter the Medication ID ",
        text_color=font_color,
        fg_color=bg_color,
        font=("Bodoni MT Black", 25, "bold"),
        corner_radius=6,
              )
        title.grid(row=0, column=0, columnspan=4, pady=10, sticky="ew")
        search_la = ctk.CTkLabel(left_frame, text="Medication ID :", font=font_style)
        search_la.grid(row=1, column=0,sticky="w")
        search_entryUP = ctk.CTkEntry(left_frame, width=250, font=("Arial", 14))
        search_entryUP.grid(row=1, column=3, padx=3, sticky="w")
        # Create a message label placed below each entry field
        message_labelup = ctk.CTkLabel(
                left_frame, text="", text_color="red", font=("Arial", 17,"bold")
            )
        message_labelup.grid(
                row=6, column=0,sticky="w",pady=10
            )  # Message label under entry field
        search_btnup = ctk.CTkButton(left_frame, text="Save", width=250,command=save_changes)
        search_btnup.grid(row=2, column=3, padx=3,pady=5,sticky="w")
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
        exit_btn.grid(row=2 , column=1, columnspan=2,padx=5)

    def showAll():
        data=medicine_data.fetchall_medicine()
        table.delete_all_rows()
        for i in data:
          table.add_row(i)

    def search():
        if search_box.get().strip()=="ID":
          if medicine_data.get_infromation(search_entry.get().strip()):
            data= medicine_data.get_infromation(search_entry.get().strip())
            table.delete_all_rows()
            table.add_row(data)
          else:
                  left_frame = ctk.CTkFrame(table_frame, width=300, height=300, corner_radius=15)
                  left_frame.place(x=300, y=150)
                  title_label = ctk.CTkLabel(
                  left_frame, text="The ID not correct", font=("Helvetica", 20, "bold"),bg_color="red"
                          )
                  title_label.grid(row=0, column=0, columnspan=2, pady=10)
                  left_frame.after(2000,lambda:left_frame.destroy())
        elif search_box.get().strip()=="Category":
          if medicine_data.get_infromation_cate(search_entry.get().strip()):
            data= medicine_data.get_infromation_cate(search_entry.get().strip())
            table.delete_all_rows()
            for i in data:
                  table.add_row(i)
          else:
                  left_frame = ctk.CTkFrame(table_frame, width=300, height=300, corner_radius=15)
                  left_frame.place(x=300, y=150)
                  title_label = ctk.CTkLabel(
                  left_frame, text="The Category not correct", font=("Helvetica", 20, "bold"),bg_color="red"
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
        root,
    )  # Increased width and height for right frame
    right_frame.grid(row=0, column=1, sticky="nsew", padx=10)

    bg_color = "#4169E1"
    font_color = "#E7EBEE"
    font_style = ("Arial", 18, "bold")

    # Title for the Billing Page
    title = ctk.CTkLabel(
        right_frame,
        text="Inventory Management",
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
        right_frame, values=["ID", "Category"], width=180, font=("Arial", 14)
    )
    search_box.grid(row=1, column=1, padx=3, pady=20, sticky="w")

    search_entry = ctk.CTkEntry(right_frame, width=250, font=("Arial", 14))
    search_entry.grid(row=1, column=2, padx=3, pady=20, sticky="w")

    search_btn = ctk.CTkButton(right_frame, text="Go", width=100, command=search)
    search_btn.grid(row=1, column=3, padx=3, pady=20, sticky="w")
    #  {'Name':<20} | {'ID':<20} | {'Category':<30} | {'production_date':<18} | {'expiry_date':<10} | {'Quntity':<15} | {'Price':<15}
    # Create Table Frame
    table_frame = ctk.CTkFrame(right_frame)
    table_frame.grid(row=2, column=0, columnspan=4, padx=10, pady=10, sticky="nsew")
    # Define columns (Updated to remove unnecessary columns and add Date)
    columns = (
        "Name",
        "ID",
        "Category",
        "production_date",
        "expiry_date",
        "Quntity",
        "Price",
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
    buttons = {
        "Add medication": additm,
        "Update medication": update,
        "Delete medication": delete,
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
