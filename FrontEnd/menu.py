def menu():
    end = False
    while not end:
        print("Choose:")
        print("1) Reset all tables")
        print("2) other stuff idk")
        print("q) Quit")
        choice = input("-->").lower().strip()

        match choice:
            case "1":
                conn = get_connection()
                cur = conn.cursor()
                cur.execute(f"DROP DATABASE IF EXISTS {DB_NAME}")
                conn.commit()
                cur.close()
                conn.close()
                main_setup()
                print("\n\nData has successfully been reset to the default.")
            case "2":
                print("Idk yet")
            case "q":
                print("Goodbye.")
                end = True
            case _:
                print("Invalid input, please try again.")

        if not end:
            input("\nPress enter to continue...")