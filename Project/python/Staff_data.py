import sqlite3

# Connect to the database
database = sqlite3.connect(r"pharmacy-management-system\Project\database\data.db")
cr = database.cursor()

# ===================================================================================
# ====================================== STAFF TABLE ================================
# ===================================================================================
cr.execute(
    """CREATE TABLE IF NOT EXISTS Staff (
              username TEXT,
              password TEXT,
              name TEXT,
              id TEXT PRIMARY KEY,
              role TEXT,
              salary TEXT,
              Shift_From  TEXT,
              shift_to TEXT)"""
)

# Class Staff and operations on the database


def add_new_staff(*informations) -> tuple:
    """
    This function adds new staff to the database and commits the data.
    the attribute of this function :
    (username, password, name, id, role, salary, Shift_From , shift_to)
    """
    cr.execute(
        """INSERT INTO Staff(username, password, name, id, role, salary, Shift_From , shift_to)
                      VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
        informations,
    )
    database.commit()


def remove_staff(username_or_id):
    """
    This function removes a staff member from the database by username or id.
    """
    if str(username_or_id).isdecimal():
        cr.execute("DELETE FROM Staff WHERE id = ?", (username_or_id,))
    else:
        cr.execute("DELETE FROM Staff WHERE username = ?", (username_or_id,))
    database.commit()


def check_username_and_password(username, password):
    # if username and password is correct return the information of staff as tupel
    # (username, password, name, id, role, salary, attedancy, shift, shift_to)
    """
    This function checks if a username and password exist in the database.
    """
    cr.execute(
        "SELECT * FROM Staff WHERE username = ? AND password = ?", (username, password)
    )
    result = cr.fetchone()
    if result:
        return result
    else:
        return False


def search_on_username(
    username,
):  # used if add new staff because the usernaem is not repeated
    """
    Checks if a username exists in the Staff table.

    Args:
        username (str): The username to search for.

    Returns:
        bool: True if the username exists, False otherwise.
    """
    cr.execute("SELECT * FROM Staff WHERE username = ?", (username,))
    return cr.fetchone() is not None


def search_on_username_STAFF(
    username,
):  # used if add new staff because the usernaem is not repeated
    """
    Checks if a username exists in the Staff table.

    Args:
        username (str): The username to search for.

    Returns:
        bool: True if the username exists, False otherwise.
    """
    cr.execute("SELECT * FROM Staff WHERE username = ? AND role=staff", (username,))
    return cr.fetchone() is not None


def search_on_id(id):
    """
    Checks if an ID exists in the Staff table.

    Args:
        id (str): The ID to search for.

    Returns:
        bool: True if the ID exists, False otherwise.
    """
    cr.execute("SELECT * FROM Staff WHERE id = ?", (id,))
    return cr.fetchone() is not None


def update_username(old_username, new_username):
    """
    Updates the username of a staff member in the Staff table.

    Args:
        old_username (str): The current username of the staff member.
        new_username (str): The new username to assign.

    Returns:
        bool: True if the update was successful, False if the new username already exists.
    """
    # Check if the new username already exists
    if search_on_username(new_username):
        return False

    # Update the username
    cr.execute(
        "UPDATE Staff SET username = ? WHERE username = ?", (new_username, old_username)
    )
    database.commit()
    return True


def update_password(username, new_password):
    """
    Updates the password of a staff member in the Staff table.

    Args:
        username (str): The username of the staff member.
        new_password (str): The new password to assign.

    Returns:
        bool: True if the update was successful, False otherwise.
    """
    try:
        # Update the password
        cr.execute(
            "UPDATE Staff SET password = ? WHERE username = ?", (new_password, username)
        )
        database.commit()
        return True

    except sqlite3.Error:
        return False


def update_salary(username, new_salary):  # use just Admin
    """
    Updates the salary of a staff member in the Staff table.

    Args:
        username (str): The username of the staff member.
        new_salary (str or float): The new salary to assign.

    Returns:
        bool: True if the update was successful, False otherwise.
    """
    try:
        cr.execute(
            "UPDATE Staff SET salary = ? WHERE username = ?", (new_salary, username)
        )
        database.commit()
        return True
    except sqlite3.Error as e:
        return False


def update_name(username, new_name):
    """
    Updates the name of a staff member in the Staff table.

    Args:
        username (str): The username of the staff member.
        new_name (str): The new name to assign.

    Returns:
        bool: True if the update was successful, False otherwise.
    """
    try:
        cr.execute("UPDATE Staff SET name = ? WHERE username = ?", (new_name, username))
        database.commit()
        return True
    except sqlite3.Error:
        return False


def update_id(old_username, new_id):
    """
    Updates the ID of a staff member in the Staff table.

    Args:
        old_username (str): The username of the staff member whose ID is being updated.
        new_id (str): The new ID to assign.

    Returns:
        bool: True if the update was successful, False otherwise.
    """
    try:
        # Update the ID
        cr.execute("UPDATE Staff SET id = ? WHERE username = ?", (new_id, old_username))
        database.commit()
        return True
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        return False


def update_shiftAM(user_name, start):
    try:
        cr.execute(
            f"update Staff set Shift_From = '{start}' where username = '{user_name}'"
        )
        database.commit()

    except sqlite3.Error:
        return False


def update_shiftPM(user_name, END):
    try:
        cr.execute(
            f"update Staff set shift_to = '{END}' where username = '{user_name}'"
        )
        database.commit()

    except sqlite3.Error:
        return False


def get_username(id):
    cr.execute("SELECT username FROM Staff WHERE id = ?", (id,))
    return cr.fetchone()[0]


def get_id(username):
    cr.execute("SELECT id FROM Staff WHERE username = ?", (username,))
    return cr.fetchone()[0]


def update_role(user_name, role):
    try:
        cr.execute(f"update Staff set role = '{role}' where username = '{user_name}'")
        database.commit()

    except sqlite3.Error:
        return False


def fecheone_staff(username_or_id):
    """
    This function removes a staff member from the database by username or id.
    """
    if str(username_or_id).isdecimal():
        cr.execute("SELECT * FROM Staff WHERE id = ?", (username_or_id,))
        return [cr.fetchone()]
    else:
        cr.execute("SELECT * FROM Staff WHERE username = ?", (username_or_id,))
        return [cr.fetchone()]


def fecheall_staff():
    try:
        cr.execute("SELECT * FROM Staff ")
        return cr.fetchall()
    except sqlite3.Error:
        return False


# ===================================================================================
# ==================================== END STAFF TABLE ==============================
# ===================================================================================
