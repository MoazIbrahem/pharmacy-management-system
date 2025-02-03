import sqlite3
import datetime
# Connect to the database
db = sqlite3.connect(r"Project\database\data.db")
cr = db.cursor()

# ===================================================================================
# ================================== MEDICINE TABLE =================================
# ===================================================================================
cr.execute(
    """CREATE TABLE IF NOT EXISTS Medicine (
              name TEXT,
              id TEXT ,
              category TEXT,
              production_date TEXT,
              expiry_date TEXT,
              quantity TEXT,
              price TEXT
              )"""
)



# Function to add a new medicine record
def add_new_medicine(*details):
    """
    This function adds a new medicine to the database.
    Parameters:
    (name,id,category,production_date,expiry_date,quantity,price)
    """
    cr.execute(
        """INSERT INTO Medicine(name,id,category,production_date , expiry_date, quantity, price)
                      VALUES (?, ?, ?, ?, ?, ?, ?)""",
        details,
    )
    db.commit()


# Function to remove a medicine record by ID
def remove_medicine(medicine_id):
    """
    This function removes a medicine from the database by ID.
    """
    cr.execute("DELETE FROM Medicine WHERE id = ?", (medicine_id,))
    db.commit()


# Function to update medicine quantity
def update_quantity(medicine_id, new_quantity):
    """
    Updates the quantity of a medicine.
    """
    try:
        cr.execute(
            "UPDATE Medicine SET quantity = ? WHERE id = ?", (new_quantity, medicine_id)
        )
        db.commit()
        return True
    except sqlite3.Error:
        return False


# Function to update medicine price
def update_price(medicine_id, new_price):
    """
    Updates the price of a medicine.
    """
    try:
        cr.execute(
            "UPDATE Medicine SET price = ? WHERE id = ?", (new_price, medicine_id)
        )
        db.commit()
        return True
    except sqlite3.Error:
        return False

def update_Name(medicine_id, new_name):
    """
    Updates the price of a medicine.
    """
    try:
        cr.execute(
            "UPDATE Medicine SET name = ? WHERE id = ?", (new_name, medicine_id)
        )
        db.commit()
        return True
    except sqlite3.Error:
        return False
      
def update_id(medicine_id, id):
    """
    Updates the price of a medicine.
    """
    try:
        cr.execute(
            "UPDATE Medicine SET id = ? WHERE id = ?", (id, medicine_id)
        )
        db.commit()
        return True
    except sqlite3.Error:
        return False
      
def update_category(medicine_id, cat):
    """
    Updates the price of a medicine.
    """
    try:
        cr.execute(
            "UPDATE Medicine SET category = ? WHERE id = ?", (cat, medicine_id)
        )
        db.commit()
        return True
    except sqlite3.Error:
        return False

def update_production_date(medicine_id, production_date):
    """
    Updates the price of a medicine.
    """
    try:
        cr.execute(
            "UPDATE Medicine SET production_date = ? WHERE id = ?", (production_date, medicine_id)
        )
        db.commit()
        return True
    except sqlite3.Error:
        return False
      
def update_expiry_date(medicine_id, expiry_date):
    """
    Updates the price of a medicine.
    """
    try:
        cr.execute(
            "UPDATE Medicine SET expiry_date = ? WHERE id = ?", (expiry_date, medicine_id)
        )
        db.commit()
        return True
    except sqlite3.Error:
        return False


# Function to search for a medicine by ID
def search_medicine_by_id(medicine_id):
    """
    Searches for a medicine by ID.
    """
    cr.execute("SELECT * FROM Medicine WHERE id = ?", (medicine_id,))
    return cr.fetchone() is not None


def get_infromation(medicine_id):
    """
    Searches for a medicine by ID.
    """
    cr.execute("SELECT * FROM Medicine WHERE id = ?", (medicine_id,))
    return cr.fetchone()

def get_infromation_cate(category):
    """
    Searches for a medicine by ID.
    """
    cr.execute("SELECT * FROM Medicine WHERE category = ?", (category,))
    return cr.fetchall()

def get_infromation_cate_name(category,name):
    """
    Searches for a medicine by ID.
    """
    cr.execute("SELECT * FROM Medicine WHERE category = ? and name= ? ", (category,name))
    return cr.fetchone()

def get_name(medicine_id):
    """
    Searches for a medicine by ID.
    """
    cr.execute("SELECT name FROM Medicine WHERE id = ?", (medicine_id,))
    return cr.fetchone()[0]


def get_quantity_by_id(medicine_id):
    """
    Retrieves the quantity of a medicine by ID.
    :param medicine_id: The ID of the medicine to fetch the quantity for.
    :return: Quantity as an integer if the medicine exists, or None if it doesn't exist.
    """
    cr.execute("SELECT quantity FROM Medicine WHERE id = ?", (medicine_id,))
    result = cr.fetchone()
    return int(result[0]) if result else None

def get_price_by_id(medicine_id):
    """
    Retrieves the price of a medicine by ID.
    :param medicine_id: The ID of the medicine to fetch the price for.
    :return: Price as a float if the medicine exists, or None if it doesn't exist.
    """
    cr.execute("SELECT price FROM Medicine WHERE id = ?", (medicine_id,))
    result = cr.fetchone()
    return float(result[0]) if result else None

def search_medicine_category(category):
    """
    Searches for a medicine by ID.
    """
    cr.execute("SELECT * FROM Medicine WHERE id = ?", (category,))
    return cr.fetchall()

def fetchall_expiry_date():
    """
    return all medication expiry_date
    """
    def split_str(st):
        """Splits the date string by recognized separators """
        chars=["\\","/","#","%","&"]
        for i in chars:
          if i in st:
            return  str(st).split(i)
        return []
    cr.execute("SELECT * FROM Medicine")
    data=cr.fetchall()
    if data:
      result=[]
      for mid in data:
        mysplit2=split_str(mid[4])
        if datetime.date(int(mysplit2[2]),int(mysplit2[1]),int(mysplit2[0]))<= datetime.datetime.date(datetime.datetime.now()):
          result.append(mid)
      return result
    else:
      return []

def fetchall_medicine():
    cr.execute("SELECT * FROM Medicine")
    result = cr.fetchall()
    if result:
      return result
    else:
      return False
# ===================================================================================
# =============================== END MEDICINE TABLE ================================
# ===================================================================================
