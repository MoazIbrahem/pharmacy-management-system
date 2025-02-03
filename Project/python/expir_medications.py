import customtkinter as ctk
from tkinter.messagebox import showinfo
import medicine_data


def ex_window(root):
    # Set appearance
    ctk.set_appearance_mode("Light")
    ctk.set_default_color_theme("blue")

    # =======================================================================================================
    # Right Frame (Enlarged)
    right_frame = ctk.CTkFrame(
        root,
    )  # Increased width and height for right frame
    right_frame.grid(row=0, column=1, sticky="nsew", padx=10)

    bg_color = "#4169E1"
    font_color = "#E7EBEE"

    # Title for the Expiry Page
    title = ctk.CTkLabel(
        right_frame,
        text="Expiry Medications",
        text_color=font_color,
        fg_color=bg_color,
        font=("Bodoni MT Black", 25, "bold"),
        corner_radius=6,
    )
    title.grid(row=0, column=0, columnspan=4, pady=10, sticky="ew")

    # Data Table (Enlarged)
    table = ctk.CTkTextbox(right_frame, width=800, height=400, corner_radius=10)
    table.grid(row=2, column=0, columnspan=4, padx=10, pady=10)
    data = medicine_data.fetchall_expiry_date()
    table.configure(state="normal")
    table.delete("1.0", "end")
    table.insert(
        "end",
        f"{'Name':<20} | {'ID':<20} | {'Category':<30} | {'production_date':<18} | {'expiry_date':<10} | {'Quntity':<15} | {'Price':<15}\n",
    )
    table.insert("end", "-" * 160 + "\n")  # Adds a divider line for clarity
    table.configure(state="disabled")
    for info in data:
        table.configure(state="normal")
        table.insert(
            "end",
            f"{info[0]:<20} | {info[1]:<20} | {info[2]:<30} | {info[3]:<18} | {info[4]:<10}| {info[5]:<15} | {info[6]:<15}\n",
        )
        table.insert("end", "-" * 160 + "\n")
        table.configure(state="disabled")
    # Buttons Below Table (Larger buttons)

    return right_frame
