import main #Unnecessary?
from BackEnd import infrastructure as infrastructure
from BackEnd import contractors as contractors
from BackEnd import assignments as assignments
from BackEnd import log as log
from BackEnd import schema as schema
from BackEnd import helper as helper 


def schema_menu():
    print()
    end = False
    while not end:
        print ("Choose: ")
        print ("1) Drop all tables") #Unnecessary?
        print ("2) Reset all tables")
        print ("3) Show all tables")
        print ("b) Go back")
        choice = input("--> ").lower().strip()
        match choice:
            case "1":
                schema.dropAllTables(main.get_name(), main.get_connection())
                print("\n\nData has successfully been dropped.")
            case "2":
                schema.dropAllTables(main.get_name(), main.get_connection())
                main.main_setup()
                print("\n\nData has successfully been reset.")
            case "3":
                conn = main.get_connection()
                curr = conn.cursor()
                helper.print_tables(curr)
            case "b":
                print ("Going back to main menu. ")
                end = True
            case _:
                print("Invalid input, please try again.")

        if not end:    
            input("\nPress enter to continue...")

def infrastructure_submenu(menu_choice):
    end = False
    while not end:
        match menu_choice:
            case 3:
                print("Choose search method:")
                print("1) ID")
                print("2) Location")
                print("3) Install date")
                print("4) Last inspection")
                print("5) State")
                print("b) Go back")
                choice = input("--> ").lower().strip()
                match choice:
                    case "1":
                        input("Enter the ID: ").lower().strip()
                    case _:




        if not end:
            input("Press enter to continue...")

def infrastructure_menu():
    print()
    end = False
    while not end:
        print("Choose:")
        print("1) Show table")
        print("2) Add infrastructure")
        print("3) More information about a specific infrastructure")
        print("4) Update specific infrastructure")
        print("b) Go back")
        choice = input("--> ").lower().strip()
        match choice:
            case "1":
                conn = main.get_connection()
                cur = conn.cursor()
                print()
                helper.print_tables(cur, "Infrastructure")
            case "3":
                infrastructure_submenu(3)
            case "b":
                print ("Going back to main menu. ")
                end = True
            case _:
                print("Invalid input, please try again.")

        if not end:
            input("\nPress enter to continue...")

def menu():
    end = False
    while not end:
        print("Choose:")
        print("1) Schema commands ")
        print("2) Infrastructure commands ")
        print("3) Contractor commands ")
        print("4) Assignment commands ")
        print("5) Log commands")
        print("q) Quit")
        choice = input("--> ").lower().strip()
        match choice:
            case "1":
                schema_menu()
            case "2":
                pass
                infrastructure_menu()
            case "q":
                print("Goodbye.")
                end = True
            case _:
                print("Invalid input, please try again.")

        if not end:
            input("\nPress enter to continue...")