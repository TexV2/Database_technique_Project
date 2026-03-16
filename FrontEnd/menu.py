from BackEnd import infrastructure as infrastructure
from BackEnd import contractors as contractors
from BackEnd import assignments as assignments
from BackEnd import log as log
from BackEnd import schema as schema
from BackEnd import helper as helper 



INFRASTRUCTURE_DISPLAY_COLUMNS = ["ID", "Type", "Location", "Install date", "Last inspection", "State"]
CONTRACTOR_DISPLAY_COLUMNS = ["ID", "Name", "Rating", "Field", "Cost"]
ASSIGNMENT_DISPLAY_COLUMNS =  ["ID", "Infrastructure ID", "Contractor ID", "Task type", "Projected cost", "Projected start date", "Projected end date"]
MAINTENANCE_LOG_DISPLAY_COLUMNS =  ["Assignment ID", "Start date", "End date", "Cost", "Result", "Review"]


def infrastructure_submenu(menu_choice):
    while True:
        match menu_choice:
            case 2:
                return infrastructure.add_infrastructure()
            case 3:
                print("\nChoose Search Method:")
                print("1) ID")
                print("2) Type")
                print("3) Location")
                print("4) Install Date")
                print("5) Last Inspection")
                print("6) State")
                print("b) Go Back")
                choice = input("--> ").lower().strip()
                match choice:
                    case "1":
                        infrastructure.DRY("infrastructure_id")
                        return False
                    case "2":
                        infrastructure.DRY("type")
                        return False
                    case "3":
                        infrastructure.DRY("location")
                        return False
                    case "4":
                        infrastructure.DRY("install_date")
                        return False
                    case "5":
                        infrastructure.DRY("last_inspection")
                        return False
                    case "6":
                        infrastructure.DRY("state")
                        return False
                    case "b":
                        print("Going back to infrastructure menu. ")
                        return True
                    case _:
                        print("Invalid input, please try again.")
            case 4:
                return infrastructure.update_infrastructure()
            case 5:
                print("Enter the ID of the infrastructure you want to remove (enter 'b' to go back).")
                print("Removing a infrastructure will remove related assignments and logs.")
                choice = input("--> ").lower().strip()
                if choice == "b":
                    return True
                else:
                    print("Are you sure? y/n")
                    double_check = input("--> ").lower().strip()
                    if double_check[0] == "y":
                        infrastructure.remove_infrastructure(choice)
                        return False
                    elif double_check[0] == "n":
                        return True
                    else:
                        print("Invalid input, please try again later")
                        return False
            case 6:
                return infrastructure.show_infrastructure_summary()
        input("\nPress enter to continue...")



def assignment_submenu(menu_choice):
    while True:
        match menu_choice:
            case 2:
                return assignments.add_assignment()
            case 3:
                assignments.view_assignment_between_dates()
                input("Press enter to continue...")
                return True
            case 4:
                print("\nChoose Search Method:")
                print("1) ID")
                print("2) Infrastructure ID")
                print("3) Contractor ID")
                print("4) Task Type")
                print("5) Projected Cost")
                print("6) Projected Start Date")
                print("7) Projected End Date")
                print("b) Go Back")
                choice = input("--> ").lower().strip()
                match choice:
                    case "1":
                        assignments.DRY("assignment_id")
                        return False
                    case "2":
                        assignments.DRY("infrastructure_id")
                        return False
                    case "3":
                        assignments.DRY("contractor_id")
                        return False
                    case "4":
                        assignments.DRY("task_type")
                        return False
                    case "5":
                        assignments.DRY("projected_cost")
                        return False
                    case "6":
                        assignments.DRY("projected_start_date")
                        return False
                    case "7":
                        assignments.DRY("projected_end_date")
                        return False
                    case "b":
                        print("Going back to assignment menu. ")
                        return True
                    case _:
                        print("Invalid input, please try again.")
            case 5:
                return assignments.update_assignment()
            case 6:
                print("Enter the ID of the assignment you want to remove (enter 'b' to go back).")
                choice = input("--> ").lower().strip()
                if choice == "b":
                    return True
                else:
                    print("Are you sure? y/n")
                    double_check = input("--> ").lower().strip()
                    if double_check[0] == "y":
                        assignments.remove_assignment(choice)
                        return False
                    elif double_check[0] == "n":
                        return True
                    else:
                        print("Invalid input, please try again later")
                        return False
            case 7:
                assignments.show_finished_assignments()
                input("Press enter to continue\n")
                return True
        input("\nPress enter to continue...")



def log_submenu(menu_choice):
    while True:
        match menu_choice:
            case 2:
                return log.add_log()
            case 3:
                log.view_log_between_dates()
                return False
            case 4:
                print("\nChoose Search Method:")
                print("1) ID")
                print("2) Start Date")
                print("3) End Date")
                print("4) Cost")
                print("5) Result")
                print("6) Review")
                print("b) Go Back")
                choice = input("--> ").lower().strip()
                match choice:
                    case "1":
                        log.DRY("assignment_id")
                        return False
                    case "2":
                        log.DRY("start_date")
                        return False
                    case "3":
                        log.DRY("end_date")
                        return False
                    case "4":
                        log.DRY("cost")
                        return False
                    case "5":
                        log.DRY("result")
                        return False
                    case "6":
                        log.DRY("review")
                        return False
                    case "b":
                        print("Going back to assignment menu. ")
                        return True
                    case _:
                        print("Invalid input, please try again.")
            case 5:
                return log.update_log()
            case 6:
                print("Enter the ID of the maintenance log you want to remove (enter 'b' to go back).")
                choice = input("--> ").lower().strip()
                if choice == "b":
                    return True
                else:
                    print("Are you sure? y/n")
                    double_check = input("--> ").lower().strip()
                    if double_check[0] == "y":
                        log.remove_log(choice)
                        return False
                    elif double_check[0] == "n":
                        return True
                    else:
                        print("Invalid input, please try again later")
                        return False
        input("\nPress enter to continue...")



def contractor_submenu(menu_choice):
    while True:
        match menu_choice:
            case 2:
                return contractors.add_contractor()
            case 3:
                print("\nChoose Search Method:")
                print("1) ID")
                print("2) Name")
                print("3) Rating")
                print("4) Field")
                print("5) Cost")
                print("b) Go Back")
                choice = input("--> ").lower().strip()
                match choice:
                    case "1":
                        contractors.DRY("contractor_id")
                        return False
                    case "2":
                        contractors.DRY("name")
                        return False
                    case "3":
                        contractors.DRY("rating")
                        return False
                    case "4":
                        contractors.DRY("field")
                        return False
                    case "5":
                        contractors.DRY("cost")
                        return False
                    case "b":
                        print("Going back to infrastructure menu. ")
                        return True
                    case _:
                        print("Invalid input, please try again.")
            case 4:
                return contractors.update_contractor()
            case 5:
                print("Enter the ID of the contractor you want to remove (enter 'b' to go back).")
                print("Removing a contractor will remove related assignments and logs.")
                choice = input("--> ").lower().strip()
                if choice == "b":
                    return True
                else:
                    print("Are you sure? y/n")
                    double_check = input("--> ").lower().strip()
                    if double_check[0] == "y":
                        contractors.remove_contractor(choice)
                        return False
                    elif double_check[0] == "n":
                        return True
                    else:
                        print("Invalid input, please try again later")
                        return False
            case 6:
                print("Enter the ID of the contractor:")
                ID = input("--> ").strip()
                if helper.sanitize_input(ID, numbers_only=True):
                    return contractors.count_num_contractor_jobs(ID)
                else:
                    print("Invalid input, please try again later.")
                    return False
            case 7:
                contractors.global_contractor_avg_comparison()
                return False
        

        input("\nPress enter to continue...")



def schema_menu():
    while True:
        print ("\nSchema Menu: ")
        print ("1) Reset All tables") #Unnecessary?
        print ("2) Show All Tables")
        print ("b) Go back")
        choice = input("--> ").lower().strip()
        match choice:
            case "1":
                print("Do you want to reset with dummy data? y/n")
                choice = input ("--> ").lower().strip()
                if choice == "y":
                    schema.main_setup()
                elif choice == "n":
                    schema.main_setup(False)
                else:
                    print("Invalid input, please try again.")
            case "2":
                conn = schema.get_connection()
                curr = conn.cursor()
                helper.print_tables(curr, INFRASTRUCTURE_DISPLAY_COLUMNS, table_name="Infrastructure")
                helper.print_tables(curr, CONTRACTOR_DISPLAY_COLUMNS, table_name="Contractor")
                helper.print_tables(curr, ASSIGNMENT_DISPLAY_COLUMNS, table_name="Assignment")
                helper.print_tables(curr, MAINTENANCE_LOG_DISPLAY_COLUMNS, table_name="MaintenanceLog")
                conn.close()
                curr.close()
            case "b":
                print ("Going back to main menu. ")
                return True
            case _:
                print("Invalid input, please try again.")  
        input("\nPress enter to continue...")



def infrastructure_menu():
    while True:
        skip = False
        print("\nInfrastructure Menu:")
        print("1) Show Table")
        print("2) Add Infrastructure")
        print("3) Search & Filter")
        print("4) Update Infrastructure")
        print("5) Remove Infrastructure")
        print("6) Show Infrastructure summary")
        print("b) Go back")
        choice = input("--> ").lower().strip()
        match choice:
            case "1":
                conn = schema.get_connection()
                cur = conn.cursor()
                print()
                helper.print_tables(cur, INFRASTRUCTURE_DISPLAY_COLUMNS, table_name="Infrastructure")
            case "2":
                skip = infrastructure_submenu(2)
            case "3":
                skip = infrastructure_submenu(3)
            case "4":
                skip = infrastructure_submenu(4)
            case "5":
                skip = infrastructure_submenu(5)
            case "6":
                skip = infrastructure_submenu(6)
            case "b":
                print ("Going back to main menu. ")
                return True
            case _:
                print("Invalid input, please try again.")
        if not skip:
            input("\nPress enter to continue...")



def log_menu():
    while True:
        skip = False
        print("\nAssignment Log Menu:")
        print("1) Show Table")
        print("2) Add Log")
        print("3) Logs in Date Range")
        print("4) Search & Filter")
        print("5) Update Log")
        print("6) Remove Log")
        print("b) Go Back")
        choice = input("--> ").lower().strip()
        match choice:
            case "1":
                conn = schema.get_connection()
                cur = conn.cursor()
                print()
                helper.print_tables(cur, MAINTENANCE_LOG_DISPLAY_COLUMNS, table_name="MaintenanceLog")
            case "2":
                skip = log_submenu(2)
            case "3":
                skip = log_submenu(3)
            case "4":
                skip = log_submenu(4)
            case "5":
                skip = log_submenu(5)
            case "6":
                skip = log_submenu(6)
            case "b":
                print ("Going back to main menu. ")
                return True
            case _:
                print("Invalid input, please try again.")
        if not skip:
            input("\nPress enter to continue...")



def contractor_menu():
    while True:
        skip = False
        print("\nContractor Menu:")
        print("1) Show Table")
        print("2) Add Contractor")
        print("3) Search & Filter")
        print("4) Update Contractor")
        print("5) Remove Contractor")
        print("6) Contractor Jobs")
        print("7) Cost Comparison")
        print("b) Go back")
        choice = input("--> ").lower().strip()
        match choice:
            case "1":
                conn = schema.get_connection()
                cur = conn.cursor()
                print()
                helper.print_tables(cur, CONTRACTOR_DISPLAY_COLUMNS, table_name="Contractor")
            case "2":
                skip = contractor_submenu(2)
            case "3":
                skip = contractor_submenu(3)
            case "4":
                skip = contractor_submenu(4)
            case "5":
                skip = contractor_submenu(5)
            case "6":
                skip = contractor_submenu(6)
            case "7":
                skip = contractor_submenu(7)
            case "b":
                print ("Going back to main menu. ")
                return True
            case _:
                print("Invalid input, please try again.")
        if not skip:
            input("\nPress enter to continue...")



def assignment_menu():
    while True:
        skip = False
        print("\nAssignment Menu:")
        print("1) View Assignments")
        print("2) Add Assignment")
        print("3) Assignments in Date Range")
        print("4) Search & Filter")
        print("5) Update Assignment")
        print("6) Remove Assignment")
        print("7) Show finished Assignments")
        print("b) Go Back")
        choice = input("--> ").lower().strip()
        match choice:
            case "1":
                conn = schema.get_connection()
                cur = conn.cursor()
                print()
                helper.print_tables(cur, ASSIGNMENT_DISPLAY_COLUMNS, table_name="Assignment")
            case "2":
                skip = assignment_submenu(2)
            case "3":
                skip = assignment_submenu(3)
            case "4":
                skip = assignment_submenu(4)
            case "5":
                skip = assignment_submenu(5)
            case "6":
                skip = assignment_submenu(6)
            case "7":
                skip = assignment_submenu(7)
            case "b":
                print("Going back to the main menu")
                return True
        if not skip:
            input("\nPress enter to continue...")



def menu():
    while True:
        skip = False
        print("\nMain Menu:")
        print("1) Schema Commands ")
        print("2) Infrastructure Commands ")
        print("3) Contractor Commands ")
        print("4) Assignment Commands ")
        print("5) Log Commands")
        print("q) Quit")
        choice = input("--> ").lower().strip()
        
        match choice:
            case "1":
                skip = schema_menu()
            case "2":
                skip = infrastructure_menu()
            case "3":
                skip = contractor_menu()
            case "4":
                skip = assignment_menu()
            case "5":
                skip = log_menu()
            case "q":
                print("Goodbye.")
                return
            case _:
                print("Invalid input, please try again.")
        if not skip:
            input("\nPress enter to continue...")