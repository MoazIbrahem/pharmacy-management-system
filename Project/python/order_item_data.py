import sqlite3

# Connect to the database
db = sqlite3.connect(r"pharmacy-management-system\Project\database\data.db")
cr = db.cursor()

# Create the OrderItem table
cr.execute(
    """
    CREATE TABLE IF NOT EXISTS OrderItem (
        order_id TEXT NOT NULL,
        name TEXT,
        product_id TEXT NOT NULL,
        quantity INTEGER NOT NULL,
        price REAL NOT NULL,
        total REAL NOT NULL
    )
    """
)


# CREATE: Add a new item to an order
def add_order_item(order_id,name,product_id, quantity, price):
    """
    Adds a new item to an order in the OrderItem table.
    """
    total = int(quantity) * float(price)
    try:
        cr.execute(
            """
            INSERT INTO OrderItem (order_id,name,product_id, quantity, price, total)
            VALUES (?, ?, ?, ?,?,?)
            """,
            (order_id,name,product_id, quantity, price, total),
        )
        db.commit()
    except sqlite3.Error as e:
        print(f"Error adding order item: {e}")

# READ: Fetch all items for a specific order
def fetch_order_items(order_id):
    """
    Fetches all items for a given order ID.
    """
    try:
        cr.execute("SELECT * FROM OrderItem WHERE order_id = ?", (order_id,))
        return cr.fetchall()
    except sqlite3.Error as e:
        return []

def fetch_Quntity(order_id):
    """
    Fetches all items for a given order ID.
    """
    try:
        cr.execute("SELECT quantity FROM OrderItem WHERE product_id = ?", (order_id,))
        return cr.fetchall()
    except sqlite3.Error as e:
        return []

def fetch_name(order_id):
    """
    Fetches all items for a given order ID.
    """
    try:
        cr.execute("SELECT name FROM OrderItem WHERE product_id = ?", (order_id,))
        return cr.fetchall()
    except sqlite3.Error as e:
        return []

# DELETE: Delete an order item
def delete_order_item(order_id, product_id):
    """
    Deletes an order item by its order ID and product ID.
    """
    try:
        cr.execute(
            "DELETE FROM OrderItem WHERE order_id = ? AND product_id = ?", 
            (order_id, product_id)
        )
        db.commit()
        print("Order item deleted successfully!")
    except sqlite3.Error as e:
        print(f"Error deleting order item: {e}")

