from BackEnd import schema as schema
from BackEnd import helper as helper
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