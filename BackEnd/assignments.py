from BackEnd import schema as schema
from BackEnd import helper as helper
from BackEnd import infrastructure as infrastructure
from BackEnd import contractors as contractor


VALID_COLUMNS = {"task_type", "projected_cost", "projected_start_date", "projected_end_date"}
DISPLAY_COLUMNS =  ["ID", "Infrastructure ID", "Contractor ID", "Task type", "Projected cost", "Projected start date", "Projected end date"]


def method_picker(method, cur):
    conversion = {
        "assignment_id": "the ID",
        "infrastructure_id": "the infrastructure id",
        "contractor_id": "the contractor's id",
        "task_type": "the task type",
        "projected_cost": "the projected cost",
        "projected_start_date": "its projected start date",
        "projected_end_date": "it's projected end date"
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



def remove_assignment(ID):
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
    print("Assignment has been deleted")
    return



def update_assignment():
    accepted_input = True

    print("Enter the ID of the assignment you would like to update")
    ID = input("--> ").strip()
    accepted_input &= helper.sanitize_input(ID, numbers_only=True)
    conn = schema.get_connection()
    cur = conn.cursor()
    if not check_rows("assignment_id", ID, cur):
        print("Invalid ID, please try again later")
        cur.close()
        conn.close()
        return False
    cur.close()
    conn.close()

    print("Enter what column you would like to edit (task_type, projected_cost, projected_start_date, projected_end_date)")
    column = input("--> ").lower().strip()
    accepted_input &= helper.sanitize_input(column)
    if column not in VALID_COLUMNS:
        print(f"Invalid column: {column}")
        return False

    print("Enter the new value")
    new_value = input("--> ").lower().strip()
    if column == "projected_start_date" or column == "projected_end_date":
        accepted_input &= helper.sanitize_input(new_value, date_mode=True)
    elif column == "projected_cost":
        accepted_input &= helper.sanitize_input(new_value, numbers_only=True)
    else:
        accepted_input &= helper.sanitize_input(new_value)

    if accepted_input:
        conn = schema.get_connection()
        cur = conn.cursor()
        cur.execute(
                f"UPDATE Assignment SET `{column}` = %s WHERE assignment_id =%s ",
                (new_value, ID)
            )
        conn.commit()
        cur.close()
        conn.close()
        print("Row has been updated.")
        return True
    else:
        print("You have entered invalid data, please try again later.")
        return False



def view_assignment_between_dates():
    accepted_input = True

    print("What is the start date for the period you are looking for assignments in?")
    start_date = input("--> ").strip()
    accepted_input &= helper.sanitize_input(start_date, date_mode=True)
    print("What is the end date for the period you are looking for assignments in?")
    end_date = input("--> ").strip()
    accepted_input &= helper.sanitize_input(end_date, date_mode=True)
    if accepted_input:
        conn = schema.get_connection()
        cur = conn.cursor()
        helper.print_tables(cur, DISPLAY_COLUMNS, table_name="Assignment", where=f"projected_start_date >= '{start_date}' AND projected_end_date <= '{end_date}'")
        cur.close()
        conn.close()
    else:
        print("You have entered invalid data, please try again later.")
    return



def add_assignment():
    accepted_input = True

    print("What is the ID of the contractor working on your assignment?")
    con_id = input("--> ").strip()
    accepted_input &= helper.sanitize_input(con_id, numbers_only=True)
    conn = schema.get_connection()
    cur = conn.cursor()
    if accepted_input and not contractor.check_rows("contractor_id", con_id, cur):
        print("Invalid ID, please try again later")
        cur.close()
        conn.close()
        return False
    print("What is the ID of the infrastructure being worked on?")
    inf_id = input("--> ").strip()
    accepted_input &= helper.sanitize_input(inf_id, numbers_only=True)
    if accepted_input and not infrastructure.check_rows("infrastructure_id", inf_id, cur):
        print("Invalid ID, please try again later")
        cur.close()
        conn.close()
        return False
    cur.close()
    conn.close()

    print("What type of work is being done?")
    type = input("--> ").strip()
    accepted_input &= helper.sanitize_input(type)
    print("What is the projected cost?")
    cost = input("--> ").strip()
    accepted_input &= helper.sanitize_input(cost, numbers_only=True)
    print("What is the projected start date?")
    start_date = input("--> ")
    accepted_input &= helper.sanitize_input(start_date, date_mode=True)
    print("What is the projected end date?")
    end_date = input("--> ")
    accepted_input &= helper.sanitize_input(end_date, date_mode=True)
    if accepted_input:
        conn = schema.get_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO Assignment (contractor_id, infrastructure_id, task_type, projected_cost, projected_start_date, projected_end_date)" \
            "VALUES (%s, %s, %s, %s, %s, %s)", (con_id, inf_id, type, cost, start_date, end_date)
        )
        conn.commit()
        print("Row has been added.")
        return True
    else:
        print("You have entered invalid data, please try again later.")
        return False



def check_rows(method, data, cur):
    cur.execute(f"SELECT 1 FROM Assignment WHERE {method} = {data} LIMIT 1")
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
        helper.print_tables(cur, DISPLAY_COLUMNS, table_name="Assignment", where=f"{method} = {data}")
    cur.close()
    conn.close()

def show_finished_assignments():
    conn = schema.get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT 
            a.assignment_id,
            a.infrastructure_id,
            a.contractor_id,
            a.task_type,
            m.start_date,
            m.end_date,
            m.cost,
            m.result,
            m.review
        FROM MaintenanceLog m
        JOIN Assignment a ON a.assignment_id = m.assignment_id
    """)
    rows = cur.fetchall()
    columns = ["Assignment ID", "Infrastructure ID", "Contractor ID", "Task Type", "Start Date", "End Date", "Cost", "Result", "Review"]
    print("Finished Assignments:")
    print(helper.table_viewer(rows, columns))
    cur.close()
    conn.close()