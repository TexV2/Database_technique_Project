TABLES = ["Infrastructure", "Contractor", "Assignment", "MaintenanceLog"]

def sanitize_input(inp, numbers_only = False, date_mode = False, no_spaces = False):
    inp = inp.strip()
    if not date_mode:
        BANNED_SYMBOLS = [None, "" ";", "'", '"', "`", "#", "=", "%", "@", "(", ")"]
        last_char = ""
        for char in inp:
            if numbers_only and char not in "0123456789":
                return False
            if no_spaces and char == " ":
                return False
            if char in BANNED_SYMBOLS or (last_char+char) in ["/*", "*/", "--"]:
                return False
            last_char = char
        return True
    else:
        if len(inp) != 10:
            return False
        try:
            int(inp[:4]) #Year check
        except ValueError:
            return False
        year = int(inp[:4])
        if inp[4] != "-" and inp[7] != "-": #____-__-__ 
            return False

        try:
            int(inp[5:7]) #___-xx-__
        except ValueError:
            return False
        month = int(inp[5:7])
        if month > 12 or month == 0: #Valid month check
            return False

        try:
            int(inp[8:]) #Valid day check
        except ValueError:
            return False
        day = int(inp[8:])
        if day == 0: #___-__-00 Check
            return False
        if day > 31: #Valid day check
            return False
        if month in [4, 6, 9, 11] and day > 30: #Valid day by shorter month check
            return False

        if month == 2: #Ohh boy, february time
            leap_year = False
            year_divisible_by_four = year % 4 == 0
            if year_divisible_by_four:
                year_divisible_by_hundred = year % 100 == 0
                year_divisible_by_four_hundred = year % 400 == 0
                if not year_divisible_by_hundred or (year_divisible_by_hundred and year_divisible_by_four_hundred):
                    leap_year = True

            if leap_year and day > 29:
                return False
            elif not leap_year and day > 28:
                return False
        return True

def print_tables(cur, columns, table_name, where = None, custom_instructions=None):
    #Prints tables
    print(f"{table_name}:")
    if where is not None:
        cur.execute(f"SELECT * FROM `{table_name}` WHERE {where}")
    elif custom_instructions is not None:
        cur.execute(custom_instructions)
    else:
        cur.execute(f"SELECT * FROM `{table_name}`")
    table_info = cur.fetchall()
    print(table_viewer(table_info, columns))
    print()

def basic_values(table):
    match table:
        case "Infrastructure":
            return """
            INSERT INTO Infrastructure (type, location, install_date, last_inspection, state)
            VALUES
                ('Road', 'Main Street, Downtown', '2015-06-12', '2025-01-15', 'functional'),
                ('Elevator', 'City Hall, 3rd Floor', '2018-03-20', '2025-02-10', 'semi-functional'),
                ('Water Pipe', 'Elm Street, Block 5', '2010-09-10', '2024-11-30', 'in need of repairs'),
                ('Street Light', 'Maple Avenue', '2020-01-05', '2025-02-01', 'functional'),
                ('Bridge', 'River Road', '2005-07-22', '2023-08-15', 'in need of repairs'),
                ('Sewer System', 'Industrial Zone', '2012-11-11', '2024-10-20', 'functional'),
                ('Traffic Signal', '5th Ave & Pine St', '2016-05-03', '2025-01-10', 'functional'),
                ('Park Fountain', 'Central Park', '2019-04-15', '2024-12-01', 'semi-functional')
            """
        
        case "Contractor":
            return """
            INSERT INTO Contractor (name, rating, field, cost)
            VALUES
                ('Urban Builders Co.', 9, 'Road Construction', 'expensive'),
                ('Elevatech Ltd.', 8, 'Elevator Maintenance', 'moderate'),
                ('PipeWorks Inc.', 6, 'Plumbing', 'moderate'),
                ('Bright Lights LLC', 8, 'Electrical', 'cheap'),
                ('BridgeCare Solutions', 7, 'Bridge Maintenance', 'expensive'),
                ('SewerFix Corp.', 6, 'Sewer & Waste Management', 'moderate')
            """
        
        case "Assignment":
            return """
            INSERT INTO Assignment (infrastructure_id, contractor_id, task_type, projected_cost, projected_start_date, projected_end_date)
            VALUES
                (1, 1, 'Road Resurfacing', 120000, '2025-03-01', '2025-03-15'),
                (2, 2, 'Elevator Inspection and Lubrication', 5000, '2025-02-20', '2025-02-21'),
                (3, 3, 'Pipe Replacement', 25000, '2025-03-10', '2025-03-20'),
                (4, 4, 'Light Replacement', 2000, '2025-02-25', '2025-02-26'),
                (5, 5, 'Bridge Structural Repair', 200000, '2025-04-01', '2025-05-01'),
                (6, 6, 'Sewer Cleaning and Inspection', 15000, '2025-03-05', '2025-03-10'),
                (7, 4, 'Traffic Signal Electrical Check', 3000, '2025-02-28', '2025-02-28'),
                (8, 2, 'Fountain Pump Replacement', 8000, '2025-03-15', '2025-03-16')
            """

        case "MaintenanceLog":
            return """
            INSERT INTO MaintenanceLog (assignment_id, start_date, end_date, cost, result, review)
            VALUES
                (1, '2025-03-01', '2025-03-14', 118000, 'acceptable', 'Completed on time with minor issues, quality good.'),
                (2, '2025-02-20', '2025-02-21', 4800, 'acceptable', 'Elevator running smoothly, service performed professionally.'),
                (3, '2025-03-10', '2025-03-19', 26000, 'temporarily_fixed', 'Pipe replaced but minor leak detected afterward.'),
                (4, '2025-02-25', '2025-02-26', 2100, 'acceptable', 'Lights functional, minor delay due to parts shortage.'),
                (5, '2025-04-01', '2025-04-28', 198500, 'acceptable', 'Bridge repairs completed safely, documentation thorough.'),
                (6, '2025-03-05', '2025-03-09', 14800, 'acceptable', 'Sewer system cleaned and inspected, minor blockages cleared.'),
                (7, '2025-02-28', '2025-02-28', 2900, 'acceptable', 'Traffic signal fully operational, work performed efficiently.'),
                (8, '2025-03-15', '2025-03-16', 8200, 'failure', 'Pump failed after a week, replacement part defective, contractor to follow up.')
            """



def table_viewer(table_info, columns):
    table_info = [[str(col) for col in row] for row in table_info] #Convert everything to string
    returner = ""

    max_lengths = []
    for col in columns: #Minimum space needed
        max_lengths.append(len(col))

    for row in table_info: #Getting amount of spaces needed
        for i, column_value in enumerate(row):
            length = len(column_value)
            if length > max_lengths[i]:
                max_lengths[i] = length

    for formatting in range(len(columns)): #Building columns
        returner += f"{columns[formatting]:<{max_lengths[formatting]}}    "
    returner += "\n"
    
    for divider in max_lengths: #Getting divider
        returner += "-" * (divider + 4) 
    returner += "\n"    
    
    for row_adder in table_info: #Adding rows
        for i, column_value in enumerate(row_adder):
            returner += f"{column_value:<{max_lengths[i]}}    "
        returner += "\n"

    return returner