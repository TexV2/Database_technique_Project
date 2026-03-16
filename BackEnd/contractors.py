from BackEnd import schema as schema
from BackEnd import helper as helper


VALID_COLUMNS = {"name", "rating", "field", "cost"}
DISPLAY_COLUMNS = ["ID", "Name", "Rating", "Field", "Cost"]


def method_picker(method, cur):
    conversion = {
        "contractor_id": "the ID",
        "name": "Contractor name",
        "rating": "the rating",
        "field": "the field",
        "cost": "the Cost",
    }
    data = input(f"Enter {conversion[method]}: ").lower().strip()
    if not helper.sanitize_input(data):
        return -1, data

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



def remove_contractor(ID):
    conn = schema.get_connection()
    cur = conn.cursor()
    cur.execute("""
        DELETE FROM MaintenanceLog 
        WHERE assignment_id IN (
            SELECT assignment_id FROM Assignment 
            WHERE contractor_id = %s
        )
    """, (ID,))

    cur.execute(
        "DELETE FROM Assignment WHERE contractor_id = %s", 
        (ID,)
    )
    cur.execute(
        "DELETE FROM Contractor WHERE contractor_id = %s", 
        (ID,)
    )
    conn.commit()
    cur.close()
    conn.close()
    print("Contractor and related assignments/logs have been deleted")
    return



def add_contractor():
    accepted_input = True

    print("What is the name of your contractor?")
    name = input("--> ").strip()
    accepted_input &= helper.sanitize_input(name)
    print("What field does your contractor work in?")
    field = input("--> ").strip()
    accepted_input &= helper.sanitize_input(field)
    print("What price range does your contractor operate within?")
    price_range = input("--> ").strip()
    accepted_input &= helper.sanitize_input(price_range, no_spaces=True)

    if accepted_input:
        conn = schema.get_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO Contractor (Name, Rating, Field, Cost) VALUES (%s, %s, %s, %s)",
            (name, 1, field, price_range)
        )
        conn.commit()
        cur.close()
        conn.close()
        print("Row has been added.")
        return True
    else:
        print("You have entered invalid data, please try again later.")
        return False



def update_contractor():
    accepted_input = True

    print("Enter the ID of the contractor you would like to update")
    ID = input("--> ").strip()
    accepted_input &= helper.sanitize_input(ID, numbers_only=True)
    conn = schema.get_connection()
    cur = conn.cursor()
    if accepted_input and not check_rows("contractor_id", ID, cur):
        print("Invalid ID, please try again later")
        cur.close()
        conn.close()
        return False
    cur.close()
    conn.close()

    print("Enter what column you would like to edit (name, rating, field, cost)")
    column = input("--> ").lower().strip()
    accepted_input &= helper.sanitize_input(column)
    if column not in VALID_COLUMNS:
        print(f"Invalid column: {column}")
        return

    print("Enter the new value")
    new_value = input("--> ").strip()
    if column == "Rating":
        accepted_input &= helper.sanitize_input(new_value, numbers_only=True)
    else:
        accepted_input &= helper.sanitize_input(new_value)

    if accepted_input:
        conn = schema.get_connection()
        cur = conn.cursor()
        cur.execute(
                f"UPDATE Contractor SET `{column}` = %s WHERE contractor_id =%s ",
                (new_value, ID)
            )
        conn.commit()
        conn.close()
        cur.close()
        print("Row has been updated.")
    else:
        print("You have entered invalid data, please try again later.")
    return



def count_num_contractor_jobs(ID):
    conn = schema.get_connection()
    cur = conn.cursor()

    cur.execute(f"SELECT CountNumContractorJobs({ID})")
    result = cur.fetchone()[0]
    if result == 1:
        print(f"The contractor has done {result} job in total")
    else:
        print(f"The contractor has done {result} jobs in total")
    cur.close()
    conn.close()
    return False



def global_contractor_avg_comparison():
    custom_instruction = """SELECT 
                                c.contractor_id, 
                                c.name, 
                                AVG(m.cost) AS contractor_avg_cost,
                                AVG(m.cost)-(SELECT AVG(cost) FROM MaintenanceLog) as cost_difference_from_global_avg
                                FROM Contractor c
                                INNER JOIN Assignment a ON c.contractor_id = a.contractor_id
                                INNER JOIN MaintenanceLog m ON a.assignment_id = m.assignment_id
                                GROUP BY(c.contractor_id)
                                ORDER BY(cost_difference_from_global_avg) DESC"""
    conn = schema.get_connection()
    cur = conn.cursor()
    helper.print_tables(cur, ["ID", "Name", "Contractor Avg Cost", "Cost Diff From Global Avg"], "Cost Comparison", custom_instructions=custom_instruction)
    cur.close()
    conn.close()



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
        helper.print_tables(cur, DISPLAY_COLUMNS, table_name="Contractor", where=f"{method} = {data}")
    cur.close()
    conn.close()