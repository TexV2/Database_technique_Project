from BackEnd import schema as schema
from BackEnd import helper as helper
VALID_COLUMNS = {"type", "location", "install_date", "state", "last_inspected"}
def method_picker(method, cur):
    conversion = {
        "infrastructure_id": "the ID",
        "type": "infrastructure type",
        "location": "the location",
        "install_date": "the install date",
        "last_inspection": "its last inspection",
        "state": "its current state"
    }
    data = input(f"Enter {conversion[method]}: ").lower().strip()
    if method == "infrastructure_id":
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

def update_infrastructure():
    print("Enter the ID of the infrastructure you would like to update")
    ID = input("--> ").lower()
    print("Enter what column you would like to edit")
    column = input("--> ").lower()
    if column not in VALID_COLUMNS:
        print(f"Invalid column: {column}")
        return
    print("Enter the new value")
    new_value = input("--> ").lower()
    conn = schema.get_connection()
    cur = conn.cursor()
    cur.execute(
            f"UPDATE Infrastructure SET {column} = %s WHERE infrastructure_id =%s ",
            (new_value, ID)
        )
    conn.commit()
    conn.close()
    cur.close()
    return

def add_infrastructure():
    print("What type is your infrastructure?")
    type = input("--> ")
    print("Where is your infrastructure?")
    location = input("--> ")
    print("When was your infrastructure installed?")
    installation_date = input("--> ")
    print("When was your infrastructure last inspected?")
    last_inspection = input("--> ")
    print("What is the state of your infrastructure? ")
    state = input("--> ")
    conn = schema.get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO Infrastructure (type, location, install_date, state, last_inspection) VALUES (%s, %s, %s, %s, %s)",
        (type, location, installation_date, state, last_inspection)
    )
    conn.commit()
    return True

def check_rows(method, data, cur):
    cur.execute(f"SELECT 1 FROM Infrastructure WHERE {method} = {data} LIMIT 1")
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
        helper.print_tables(cur, "Infrastructure", f"{method} = {data}")
    cur.close()
    conn.close()