from BackEnd import schema as schema
from BackEnd import helper as helper
VALID_COLUMNS = {"Name", "Rating", "Field", "Cost"}
def method_picker(method, cur):
    conversion = {
        "Contractor_id": "the ID",
        "Name": "Contractor name",
        "Rating": "the rating",
        "Field": "the field",
        "Cost": "the Cost",
    }
    data = input(f"Enter {conversion[method]}: ").lower().strip()
    if method == "Contractor_id":
        try:
            data = int(data)
        except ValueError:
            return -1, data
    else:
        data = f"'{data}'"

    found_rows = check_rows(method, data, cur)
    if found_rows:
        return 1, data
    return 0, data

def add_contractor():
    print("What is the name of your contractor?")
    name = input("--> ")
    print("What field does your contractor work in?")
    field = input("--> ")
    print("What price range does your contractor operate within?")
    price_range = input("--> ")

    conn = schema.get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO Contractor (Name, Rating, Field, Cost) VALUES (%s, %s, %s, %s)",
        (name, 0, field, price_range)
    )
    conn.commit()
    return True

def update_contractor():
    print("Enter the ID of the contractor you would like to update")
    ID = input("--> ")
    print("Enter what column you would like to edit")
    column = input("--> ")
    if column not in VALID_COLUMNS:
        print(f"Invalid column: {column}")
        return
    print("Enter the new value")
    new_value = input("--> ")
    conn = schema.get_connection()
    cur = conn.cursor()
    cur.execute(
            f"UPDATE Contractor SET {column} = %s WHERE contractor_id =%s ",
            (new_value, ID)
        )
    conn.commit()
    conn.close()
    cur.close()
    return

def check_rows(method, data, cur):
    cur.execute(f"SELECT 1 FROM Contractor WHERE {method} = {data} LIMIT 1")
    found_rows = cur.fetchone() is not None
    if found_rows:
        return True
    return False

def DRY(method):
    conn = schema.get_connection()
    cur = conn.cursor()
    result, data = method_picker(method, cur)
    print()
    if result == -1:
        print("Invalid input, please try again.")
    elif result == 0:
        print("No data was found.")
    elif result == 1:  
        helper.print_tables(cur, "Contractor", f"{method} = {data}")
    cur.close()
    conn.close()