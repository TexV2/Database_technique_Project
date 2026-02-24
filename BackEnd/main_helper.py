
def sanitize_input(inp):
    inp = inp.strip()
    banned_symbols = [";", "'", '"', "`", "#", "=", "%", "@", "(", ")"]
    last_char = ""
    for char in inp:
        if char in banned_symbols or (last_char+char) in ["/*", "*/", "--"]:
            return False
        last_char = char
    return True



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
                ('Urban Builders Co.', 4.5, 'Road Construction', 'expensive'),
                ('Elevatech Ltd.', 4.0, 'Elevator Maintenance', 'moderate'),
                ('PipeWorks Inc.', 3.8, 'Plumbing', 'moderate'),
                ('Bright Lights LLC', 4.2, 'Electrical', 'cheap'),
                ('BridgeCare Solutions', 4.6, 'Bridge Maintenance', 'expensive'),
                ('SewerFix Corp.', 3.9, 'Sewer & Waste Management', 'moderate')
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


def table_viewer(table, table_info):
    table_info = [[str(col) for col in row] for row in table_info] #Convert everything to string
    returner = ""
    match table:
        case "Infrastructure":
            widest_id = 0 #Gets the widest entry of each column, will be used to know the minimum amount of space needed when formatting
            widest_type = 0
            widest_location = 0
            widest_install_date = 0
            widest_last_inspection = 0
            widest_state = 0
            for id, type, location, install_date, last_inspection, state in table_info:
                if len(id)>widest_id:
                    widest_id = len(id)               
                if len(type)>widest_type:
                    widest_type = len(type)
                if len(location)>widest_location:
                    widest_location = len(location)
                if len(install_date)>widest_install_date:
                    widest_install_date = len(install_date)
                if len(last_inspection)>widest_last_inspection:
                    widest_last_inspection = len(last_inspection)
                if len(state)>widest_state:
                    widest_state = len(state)
            returner = (
                f"{'ID':<{len('id') + widest_id}}  " #Formatting the header so that everything is properly aligned
                f"{'Type':<{len('type') + widest_type}}  "
                f"{'Location':<{len('location') + widest_location}}  "
                f"{'Install date':<{len('install date') + widest_install_date}}  "
                f"{'Last inspection':<{len('last inspection') + widest_last_inspection}}  "
                f"State\n"
                )
            returner += "-"*( #Just adds a "-----" divider between the header and the actual entries
                    (len('id') + widest_id) + 2 + 
                    (len('type') + widest_type) + 2 +
                    (len('location') + widest_location) + 2 +
                    (len('install date') + widest_install_date) + 2 +
                    (len('last inspection') + widest_last_inspection) + 2 +
                    len('State')
                )
            for id, type, location, install_date, last_inspection, state in table_info: #Actually adding the entries now with proper alignment
                returner += f"\n{id:<{len('id') + widest_id}}  "
                returner += f"{type:<{len('type') + widest_type}}  "
                returner += f"{location:<{len('location') + widest_location}}  "
                returner += f"{install_date:<{len('install date') + widest_install_date}}  "
                returner += f"{last_inspection:<{len('last inspection') + widest_last_inspection}}  "
                returner += state

        case "Contractor": #Very bad DRY, but idk how to do the for-loops since each table has a different amount of attributes to them
            widest_id = 0
            widest_name = 0
            widest_rating = 0
            widest_field = 0
            widest_cost = 0
            for id, name, rating, field, cost in table_info:
                if len(id)>widest_id:
                    widest_id = len(id)
                if len(name)>widest_name:
                    widest_name = len(name)
                if len(rating)>widest_rating:
                    widest_rating = len(rating)
                if len(field)>widest_field:
                    widest_field = len(field)
                if len(cost)>widest_cost:
                    widest_cost = len(cost)
            returner = (
                f"{'ID':<{len('id') + widest_id}}  "
                f"{'Name':<{len('name') + widest_name}}  "
                f"{'Rating':<{len('rating') + widest_rating}}  "
                f"{'Field':<{len('field') + widest_field}}  "
                f"Cost\n"
                )
            returner += "-"*(
                    (len('id') + widest_id) + 2 + 
                    (len('name') + widest_name) + 2 +
                    (len('rating') + widest_rating) + 2 +
                    (len('field') + widest_field) + 2 +
                    len('Cost')
                )
            for id, name, rating, field, cost in table_info:
                returner += f"\n{id:<{len('id') + widest_id}}  "
                returner += f"{name:<{len('name') + widest_name}}  "
                returner += f"{rating:<{len('rating') + widest_rating}}  "
                returner += f"{field:<{len('field') + widest_field}}  "
                returner += cost

        case "Assignment":
            widest_id = 0
            widest_infrastructure_id = 0
            widest_contractor_id = 0
            widest_task_type = 0
            widest_projected_cost = 0
            widest_projected_start_date = 0
            widest_projected_end_date = 0
            for id, infrastructure_id, contractor_id, task_type, projected_cost, projected_start_date, projected_end_date in table_info:
                if len(id)>widest_id:
                    widest_id = len(id)               
                if len(infrastructure_id)>widest_infrastructure_id:
                    widest_infrastructure_id = len(infrastructure_id)
                if len(contractor_id)>widest_contractor_id:
                    widest_contractor_id = len(contractor_id)
                if len(task_type)>widest_task_type:
                    widest_task_type = len(task_type)
                if len(projected_cost)>widest_projected_cost:
                    widest_projected_cost = len(projected_cost)
                if len(projected_start_date)>widest_projected_start_date:
                    widest_projected_start_date = len(projected_start_date)
                if len(projected_end_date)>widest_projected_end_date:
                    widest_projected_end_date = len(projected_end_date)
            returner = (
                f"{'ID':<{len('id') + widest_id}}  "
                f"{'Infrastructure ID':<{len('infrastructure id') + widest_infrastructure_id}}  "
                f"{'Contractor ID':<{len('contractor id') + widest_contractor_id}}  "
                f"{'Task type':<{len('task type') + widest_task_type}}  "
                f"{'Projected cost':<{len('projected cost') + widest_projected_cost}}  "
                f"{'Projected start date':<{len('projected start date') + widest_projected_start_date}}  "
                f"Projected end date\n"
                )
            returner += "-"*(
                    (len('id') + widest_id) + 2 +
                    (len('infrastructure id') + widest_infrastructure_id) + 2 +
                    (len('contractor id') + widest_contractor_id) + 2 +
                    (len('task type') + widest_task_type) + 2 +
                    (len('projected cost') + widest_projected_cost) + 2 +
                    (len('projected start date') + widest_projected_start_date) + 2 +
                    len('Projected end date')
                )
            for id, infrastructure_id, contractor_id, task_type, projected_cost, projected_start_date, projected_end_date in table_info:
                returner += f"\n{id:<{len('id') + widest_id}}  "
                returner += f"{infrastructure_id:<{len('infrastructure id') + widest_infrastructure_id}}  "
                returner += f"{contractor_id:<{len('contractor id') + widest_contractor_id}}  "
                returner += f"{task_type:<{len('task type') + widest_task_type}}  "
                returner += f"{projected_cost:<{len('projected cost') + widest_projected_cost}}  "
                returner += f"{projected_start_date:<{len('projected start date') + widest_projected_start_date}}  "
                returner += projected_end_date

        case "MaintenanceLog":
            widest_assignment_id = 0
            widest_start_date = 0
            widest_end_date = 0
            widest_cost = 0
            widest_result = 0
            widest_review = 0
            for assignment_id, start_date, end_date, cost, result, review in table_info:
                if len(assignment_id)>widest_assignment_id:
                    widest_assignment_id = len(assignment_id)               
                if len(start_date)>widest_start_date:
                    widest_start_date = len(start_date)
                if len(end_date)>widest_end_date:
                    widest_end_date = len(end_date)
                if len(cost)>widest_cost:
                    widest_cost = len(cost)
                if len(result)>widest_result:
                    widest_result = len(result)
                if len(review)>widest_review:
                    widest_review = len(review)
            returner = (
                f"{'Assignment ID':<{len('assignment id') + widest_assignment_id}}  "
                f"{'Start date':<{len('start date') + widest_start_date}}  "
                f"{'End date':<{len('end date') + widest_end_date}}  "
                f"{'Cost':<{len('cost') + widest_cost}}  "
                f"{'Result':<{len('result') + widest_result}}  "
                f"Review\n"
                )
            returner += "-"*(
                    (len('assignment id') + widest_assignment_id) + 2 +
                    (len('start date') + widest_start_date) + 2 +
                    (len('end date') + widest_end_date) + 2 +
                    (len('cost') + widest_cost) + 2 +
                    (len('result') + widest_result) + 2 +
                    len('Review')
                )
            for assignment_id, start_date, end_date, cost, result, review in table_info:
                returner += f"\n{assignment_id:<{len('assignment id') + widest_assignment_id}}  "
                returner += f"{start_date:<{len('start date') + widest_start_date}}  "
                returner += f"{end_date:<{len('end date') + widest_end_date}}  "
                returner += f"{cost:<{len('cost') + widest_cost}}  "
                returner += f"{result:<{len('result') + widest_result}}  "
                returner += review
    return returner