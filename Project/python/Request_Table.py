import sqlite3
from datetime import datetime

# Database connection
db = sqlite3.connect(r"Project\database\data.db")
cr = db.cursor()

# Step 1: Create a new table with Date column
cr.execute("""
CREATE TABLE IF NOT EXISTS Request_New (
    Doctor TEXT,
    Dr_ID TEXT,
    Patient TEXT,
    Medication_Name TEXT,
    Category TEXT,
    Quantity TEXT,
    Patient_Phone TEXT,
    View TEXT,
    Date TEXT
)
""")
db.commit()

# Function to add a new order with a Date column
def add_order(doc_name, dr_id, pat_name, medicine, category, quantity, pat_phone, date=None):
    if date is None:
        # Default to the current date if no date is provided
        date = datetime.now().strftime("%d-%m-%Y\n%H:%M")
    cr.execute("""
    INSERT INTO Request_New (Doctor, Dr_ID, Patient, Medication_Name, Category, Quantity, Patient_Phone, Date)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (doc_name, dr_id, pat_name, medicine, category, quantity, pat_phone, date))
    db.commit()

# Function to remove an existing order
def remove_order(doc_name, dr_id, pat_name, medicine):
    try:
        cr.execute("""
        DELETE FROM Request_New WHERE Doctor = ? AND Dr_ID = ? AND Patient = ? AND Medication_Name = ?
        """, (doc_name, dr_id, pat_name, medicine))
        db.commit()
    except sqlite3.Error as err:
        return "There is a problem in removing order: " + str(err)


# Function to get rows where 'View' column is NULL
def get_null_View():
    try:
        cr.execute("SELECT * FROM Request_New WHERE View IS NULL")
        rows = cr.fetchall()
        return rows
    except sqlite3.Error as err:
        return "Error fetching data with NULL View: " + str(err)

# Function to fetch all data
def get_data():
    try:
        cr.execute("SELECT * FROM Request_New")
        rows = cr.fetchall()
        return rows
    except sqlite3.Error as err:
        return "Error fetching data: " + str(err)


# Function to get medication details based on Doctor, Dr_ID, Patient, Patient_Phone, and Date
def get_medication_details(doc_name, dr_id, pat_name, pat_phone, date):
    try:
        cr.execute("""
        SELECT Medication_Name, Category, Quantity,View
        FROM Request_New
        WHERE Doctor = ? AND Dr_ID = ? AND Patient = ? AND Patient_Phone = ? AND Date = ?
        """, (doc_name, dr_id, pat_name, pat_phone, date))
        rows = cr.fetchall()
        return rows
    except sqlite3.Error as err:
        return "Error fetching medication details: " + str(err)

# Function to update the 'View' column
def update_view(doc_name, dr_id, pat_name, pat_pho, new_view):
    try:
        cr.execute("""
        UPDATE Request_New
        SET View = ?
        WHERE Doctor = ? AND Dr_ID = ? AND Patient = ? AND Patient_Phone = ?
        """, (new_view, doc_name, dr_id, pat_name, pat_pho))
        db.commit()
        return "View updated successfully."
    except sqlite3.Error as err:
        return "There is a problem in updating the View: " + str(err)
