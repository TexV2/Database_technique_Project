from BackEnd import schema as schema
from BackEnd import helper as helper
from BackEnd import assignments as assignment


VALID_COLUMNS = {"start_date", "end_date", "cost", "result", "review"}
DISPLAY_COLUMNS = ["Assignment ID", "Start date", "End date", "Cost", "Result", "Review"]


def method_picker(method, cur):
    conversion = {
        "assignment_id": "the assignment ID",
        "result": "the result",
        "review": "a review of the contractor",
        "cost": "cost",
        "start_date": "the start date",
        "end_date": "the end date"
    }
    data = input(f"Enter {conversion[method]}: ").lower().strip()
    if not helper.sanitize_input(data):
        return -1, data
    if method == "assignment_id":
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



def remove_log(ID):
    conn = schema.get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM MaintenanceLog WHERE assignment_id = %s", 
                (ID,)
                )

    cur.execute(
        "DELETE FROM Assignment WHERE assignment_id = %s", 
        (ID,)
    )
    conn.commit()
    cur.close()
    conn.close()
    print("Assignment and related logs have been deleted")
    return



def update_log():
    accepted_input = True

    print("Enter the assignment ID of the log you would like to update")
    ID = input("--> ").strip()
    accepted_input &= helper.sanitize_input(ID, numbers_only=True)
    conn = schema.get_connection()
    cur = conn.cursor()
    if accepted_input and not check_rows("assignment_id", ID, cur):
        print("Invalid ID, please try again later.")
        cur.close()
        conn.close()
        return False
    cur.close()
    conn.close()

    print("Enter what column you would like to edit (start_date end_date, cost, result, review)")
    column = input("--> ").lower().strip()
    if column not in VALID_COLUMNS:
        print(f"Invalid column: {column}")
        return False
    print("Enter the new value")
    new_value = input("--> ").lower().strip()
    if column in ["start_date", "end_date"]:
        accepted_input &= helper.sanitize_input(new_value, date_mode=True)
    elif column == "cost":
        accepted_input &= helper.sanitize_input(new_value, numbers_only=True)
    else:
        accepted_input &= helper.sanitize_input(new_value)
    
    if accepted_input:
        conn = schema.get_connection()
        cur = conn.cursor()
        cur.execute(
                f"UPDATE MaintenanceLog SET `{column}` = %s WHERE assignment_id =%s ",
                (new_value, ID)
            )
        conn.commit()
        cur.close()
        conn.close()
        print("Row has been updated.")
        return True
    else:
        print("You have entered invalid data, try again later.")
        return False



def view_log_between_dates():
    accepted_input = True

    print("What is the start date for the period you are looking for logs in?")
    start_date = input("--> ").strip()
    accepted_input &= helper.sanitize_input(start_date, date_mode=True)
    print("What is the end date for the period you are looking for logs in?")
    end_date = input("--> ").strip()
    accepted_input &= helper.sanitize_input(end_date, date_mode=True)
    if accepted_input:
        conn = schema.get_connection()
        cur = conn.cursor()
        helper.print_tables(cur, DISPLAY_COLUMNS, table_name="MaintenanceLog", where=f"start_date >= '{start_date}' AND end_date <= '{end_date}'")
        cur.close()
        conn.close()
        return True
    else:
        print("You have entered invalid data, please try again later.")
        return False



def add_log():
    accepted_input = True

    print("What is the id for the logs assignment?")
    ass_id = input("--> ").strip()
    accepted_input &= helper.sanitize_input(ass_id, numbers_only=True)
    conn = schema.get_connection()
    cur = conn.cursor()
    if accepted_input and (check_rows("assignment_id", ass_id, cur) or not assignment.check_rows("assignment_id", ass_id, cur)):
        print("Invalid ID, please try again later.")
        cur.close()
        conn.close()
        return False
    cur.close()
    conn.close()
    print("What is the start date?")
    start_date = input("--> ").strip()
    accepted_input &= helper.sanitize_input(start_date, date_mode=True)
    print("What is the end date?")
    end_date = input("--> ").strip()
    accepted_input &= helper.sanitize_input(end_date, date_mode=True)
    print("What was the actual cost?")
    cost = input("--> ").strip()
    accepted_input &= helper.sanitize_input(cost, numbers_only=True)
    print("What was the result?")
    result = input("--> ").strip()
    accepted_input &= helper.sanitize_input(result)
    print("How would you review the contractors performance?")
    review = input("--> ").strip()
    accepted_input &= helper.sanitize_input(review)

    if accepted_input:
        conn = schema.get_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO MaintenanceLog (assignment_id, start_date, end_date, cost, result, review)" \
            "VALUES (%s, %s, %s, %s, %s, %s)", (ass_id, start_date, end_date, cost, result, review)
        )
        conn.commit()
        print("Row has been added.")
        return True
    else:
        print("You have entered invalid data, please try again later.")
        return False



def check_rows(method, data, cur):
    cur.execute(f"SELECT 1 FROM MaintenanceLog WHERE {method} = {data} LIMIT 1")
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
        helper.print_tables(cur, DISPLAY_COLUMNS, table_name="MaintenanceLog", where=f"{method} = {data}")
    cur.close()
    conn.close()