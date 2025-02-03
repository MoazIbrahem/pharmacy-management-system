import sqlite3

# Connect to the database
db = sqlite3.connect(r"Project\database\data.db")#Project\database\data.db
cr = db.cursor()

# Create the Orders table
cr.execute(
    """
    CREATE TABLE IF NOT EXISTS Orders (
        order_id TEXT,
        staff_id TEXT,
        total_price TEXT, 
        order_date TEXT
    )
    """
)

def check_order_id(order_id):
    """
    Checks if the order_id exists in the Orders table.
    Returns True if the order_id exists, otherwise False.
    """
    try:
        cr.execute("SELECT * FROM Orders WHERE order_id = ?", (order_id,))
        result = cr.fetchone()
        if result:
            return True  
        else:
            return False  
    except sqlite3.Error as e:
        print(f"Error checking order_id: {e}")
        return False

# CREATE: Add a new order
def add_order(order_id, staff_id, total_price, order_date):
    """
    Adds a new order to the Orders table.
    """
    try:
        cr.execute(
            """
            INSERT INTO Orders (order_id, staff_id, total_price, order_date)
            VALUES (?, ?, ?, ?)
            """,
            (order_id, staff_id, total_price, order_date),
        )
        db.commit()
    except sqlite3.Error as e:
        print(f"Error adding order: {e}")

def get_all_order_ids():
    """
    Retrieves all unique order IDs from the Orders table.
    """
    try:
        cr.execute("SELECT order_id FROM Orders")
        return [row[0] for row in cr.fetchall()]
    except sqlite3.Error as e:
        print(f"Error fetching order IDs: {e}")
        return []

# READ: Fetch all orders
def fetch_all_orders():
    """
    Retrieves all orders from the Orders table.
    """
    try:
        cr.execute("SELECT * FROM Orders")
        return cr.fetchall()
    except sqlite3.Error as e:
        return []

# READ: Fetch a single order by order_id
def fetch_order_by_id(order_id):
    """
    Retrieves a specific order by its ID.
    """
    try:
        cr.execute("SELECT * FROM Orders WHERE order_id = ?", (order_id,))
        return cr.fetchone()
    except sqlite3.Error as e:
        return None






