import customtkinter as ctk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.ticker import MultipleLocator
import order_data
import order_item_data


# Pharmacy Management (Report Interface)
def Report_window(root):
    left_frame = None
    orders = order_data.fetch_all_orders()
    ordersid = [id[0] for id in orders]
    if ordersid != []:
        # Set appearance
        ctk.set_appearance_mode("Light")
        ctk.set_default_color_theme("blue")

        # Right Frame (Enlarged)
        right_frame = ctk.CTkFrame(root)
        right_frame.grid(row=0, column=1, sticky="nsew", padx=10)

        bg_color = "#4169E1"
        font_color = "#E7EBEE"

        # Title for the Pharmacy Report Page
        title = ctk.CTkLabel(
            right_frame,
            text="Pharmacy Sales Report",
            text_color=font_color,
            fg_color=bg_color,
            font=("Bodoni MT Black", 25, "bold"),
            corner_radius=6,
        )
        title.grid(row=0, column=0, columnspan=4, pady=10, sticky="ew")

        # Scrollable Frame for the Column Chart
        chart_frame = ctk.CTkFrame(right_frame, corner_radius=10)
        chart_frame.grid(row=1, column=0, sticky="nsew")

        # Adding a canvas for scroll functionality
        canvas = ctk.CTkCanvas(chart_frame, width=510, height=290)
        canvas.grid(row=0, column=0, sticky="nsew")

        # Add a horizontal scrollbar
        horizontal_scrollbar = ttk.Scrollbar(
            chart_frame, orient="horizontal", command=canvas.xview
        )
        horizontal_scrollbar.grid(row=1, column=0, sticky="ew")

        # Add a vertical scrollbar
        vertical_scrollbar = ttk.Scrollbar(
            chart_frame, orient="vertical", command=canvas.yview
        )
        vertical_scrollbar.grid(row=0, column=1, sticky="ns")

        # Configure the canvas to use the scrollbars
        canvas.configure(
            xscrollcommand=horizontal_scrollbar.set,
            yscrollcommand=vertical_scrollbar.set,
        )

        # Create a frame inside the canvas that will contain the chart
        chart_container = ctk.CTkFrame(canvas)
        canvas.create_window((0, 0), window=chart_container, anchor="nw")

        orders = order_data.fetch_all_orders()
        ordersid = [id[0] for id in orders]
        categories = []
        values = []
        ids = []
        for id in ordersid:
            data = order_item_data.fetch_order_items(id)
            for i in range(len(data)):
                if data[i][1] not in categories:
                    categories.append(data[i][1])
                if data[i][2] not in ids:
                    ids.append(data[i][2])
        for id in ids:
            qun = 0
            data = order_item_data.fetch_Quntity(id)
            for i in range(len(data)):
                qun += int(data[i][0])
            values.append(qun)

        # Dynamically adjust figure size based on the number of categories
        chart_width = max(7, len(categories) * 0.5)  # Ensure chart width is at least 6
        chart_height = 10  # You can adjust this as well if necessary

        # Create a column (bar) chart with dynamic sizing
        figure = plt.Figure(
            figsize=(chart_width, chart_height), dpi=70
        )  # Size of the chart based on number of categories
        ax = figure.add_subplot(111)

        # Add padding to the categories (adjusting the bar width)
        bar_width = 0.1  # You can decrease this for more spacing between bars
        x_positions = range(len(categories))
        ax.bar(
            x_positions, values, color="#0078D4", width=bar_width
        )  # Bar chart with customized color

        # Add padding to the x-axis labels
        ax.set_xticks(x_positions)
        ax.set_xticklabels(
            categories, rotation=45, ha="right"
        )  # Rotate labels and add padding

        ax.set_title("Sales Over Categories")
        ax.set_xlabel("Categories")
        ax.set_ylabel("Values")
        # Control the range of the Y-axis
        ax.set_ylim(
            0, max(values if values != [] else [0])
        )  # Customize the Y-axis range (from 0 to 40 for example)
        ax.yaxis.set_major_locator(MultipleLocator(10))
        canvas_chart = FigureCanvasTkAgg(figure, chart_container)
        canvas_chart.get_tk_widget().pack(fill="both", expand=True)

        # Update the scrollable region to fit the chart
        chart_container.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))

        # Create frame2 to display max category label
        frame2 = ctk.CTkFrame(right_frame, corner_radius=10)
        frame2.grid(
            row=1, column=1, sticky="ns", padx=10, pady=10
        )  # Positioning frame2 next to the chart

        # max_category_label inside frame2
        max_category_label = ctk.CTkLabel(
            frame2,
            text=f"Highest Sales: {categories[values.index(max(values if values!=[] else [0]))]}\n with value: {max(values if values!=[] else [0])}",
            text_color="#FFFFFF",
            fg_color="#FF5733",  # Customize the background color of the label
            font=("Arial", 20, "bold"),
            corner_radius=6,
        )
        max_category_label.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        max_category_label = ctk.CTkLabel(
            frame2,
            text=f"min Sales: {categories[values.index(min(values if values!=[] else [0]))]}\n with value: {min(values if values!=[] else [0])}",
            text_color="#FFFFFF",
            fg_color="#FF5733",  # Customize the background color of the label
            font=("Arial", 20, "bold"),
            corner_radius=6,
        )
        max_category_label.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

        # =================================================================================Show
        # Define columns (Updated to remove unnecessary columns and add Date)
        columns = (
            "order_id",
            "staff_id",
            "total_price",
            "order_date",
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
                    label = ctk.CTkLabel(
                        self, text=col, font=("Helvetica", 16), padx=10
                    )
                    label.grid(
                        row=0, column=self.columns.index(col), sticky="nsew", pady=5
                    )
                    self.headers.append(label)

                # Adjust grid weights
                for i in range(len(columns)):
                    self.grid_columnconfigure(i, weight=1)

                self.rows = []

            def add_row(self, values):
                row_index = len(self.rows) + 1
                row_data = []

                # Add each value to the row
                for col_index, value in enumerate(values):
                    if (
                        col_index == len(values) - 1
                    ):  # Add a button in the Actions column
                        # Check if medications are available (view is not null)
                        button = ctk.CTkButton(
                            self,
                            text="View",
                            font=("Helvetica", 14),
                            command=lambda v=values: self.view_action(v),
                        )
                        button.grid(
                            row=row_index, column=col_index, sticky="nsew", pady=2
                        )
                        row_data.append(button)
                    else:
                        label = ctk.CTkLabel(
                            self, text=value, font=("Helvetica", 14), padx=5
                        )
                        label.grid(
                            row=row_index, column=col_index, sticky="nsew", pady=2
                        )
                        row_data.append(label)

                self.rows.append(row_data)

            def add_row2(self, values):
                row_index = len(self.rows) + 1
                for col_index, value in enumerate(values):
                    label = ctk.CTkLabel(
                        self, text=value, font=("Helvetica", 14), padx=5
                    )
                    label.grid(row=row_index, column=col_index, sticky="nsew", pady=2)
                self.rows.append(values)

            def view_action(self, value):
                view(value)

        table = ModernTable(
            right_frame, columns, width=700, height=400, corner_radius=10
        )
        table.grid(row=2, column=0, padx=10, pady=10, columnspan=4, sticky="nsew")

        orders = (
            order_data.fetch_all_orders()
        )  # (order_id, staff_id, total_price, order_date)
        for row in orders:
            table.add_row(row + ("",))

        def view(row_data):
            nonlocal left_frame

            # Destroy existing left frame if it exists
            if left_frame is not None:
                return

            # Create new frame for details
            left_frame = ctk.CTkFrame(
                right_frame, width=500, height=300, corner_radius=15
            )
            left_frame.place(x=150, y=250)

            # Title Label
            title_label = ctk.CTkLabel(
                left_frame, text="Order Details", font=("Helvetica", 18, "bold")
            )
            title_label.grid(row=0, column=0, columnspan=2, pady=10)

            # Extract relevant details from row_data
            order_id = row_data[0]

            # Create a table for medication details
            med_table = ModernTable(
                left_frame,
                ("order_id", "name", "product_id", "quantity", "price", "total"),
                width=500,
                height=200,
            )
            med_table.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

            # # Fetch medication details for the current request
            medicationsx = order_item_data.fetch_order_items(order_id)
            for med in medicationsx:
                med_table.add_row2(med)

            # Add Exit Button to close the details view
            def exit_view():
                nonlocal left_frame
                if left_frame is not None:
                    left_frame.destroy()
                    left_frame = None

            exit_button = ctk.CTkButton(left_frame, text="Close", command=exit_view)
            exit_button.grid(row=2, column=0, pady=10)

        # ===========================================================================================

        # Make the grid expand as needed
        right_frame.grid_rowconfigure(0, weight=0)  # Title row
        right_frame.grid_rowconfigure(
            1, weight=1
        )  # Chart row (it will expand to fill space)
        right_frame.grid_rowconfigure(2, weight=0)  # Category display row (frame2)
        right_frame.grid_rowconfigure(
            3, weight=1
        )  # Data Table row (it will expand to fill space)
        right_frame.grid_columnconfigure(0, weight=1)  # Allow column to expand
        right_frame.grid_columnconfigure(
            1, weight=0
        )  # Allow frame2 to sit next to the chart

        return right_frame
    else:
        # Set appearance
        ctk.set_appearance_mode("Light")
        ctk.set_default_color_theme("blue")

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
            text="Report Management",
            text_color=font_color,
            fg_color=bg_color,
            font=("Bodoni MT Black", 25, "bold"),
            corner_radius=6,
        )
        title.grid(row=0, column=0, columnspan=4, pady=10, sticky="ew")

        # Data Table (Enlarged)
        table = ctk.CTkTextbox(right_frame, width=700, height=400, corner_radius=10)
        table.grid(row=2, column=0, columnspan=4, padx=10, pady=10)
        table.configure(state="normal")
        table.insert("end", f"Not Reporte Avilabel")
        table.insert("end", "-" * 160 + "\n")  # Adds a divider line for clarity
        table.configure(state="disabled")
        return right_frame
