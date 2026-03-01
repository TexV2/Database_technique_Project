import main
from BackEnd import infrastructure as infrastructure
from BackEnd import contractors as contractors
from BackEnd import assignments as assignments
from BackEnd import log as log
from BackEnd import schema as schema

def schemaMenu():
    end = False
    while not end:
        print ("Choose: ")
        print ("1) Drop all tables")
        print ("2) Reset all tables")
        print ("3) Show all tables")
        print ("4) Go back")
        choice = input("-->").lower().strip()
        match choice:
            case "1":
                schema.dropAllTables(main.get_name(), main.get_connection())
                print("\n\nData has successfully been dropped")
            case "2":
                schema.dropAllTables(main.get_name(), main.get_connection())
                main.main_setup()
                print("\n\nData has successfully been reset")
            case "3":
                conn = main.get_connection()
                curr = conn.cursor()
                main.print_tables(curr, conn)
            case "4":
                print ("Going back to main menu ")
                end = True

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
        choice = input("-->").lower().strip()
        match choice:
            case "1":
                schemaMenu()
            case "2":
                print("Idk yet")
            case "q":
                print("Goodbye.")
                end = True
            case _:
                print("Invalid input, please try again.")

        if not end:
            input("\nPress enter to continue...")