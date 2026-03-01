import os
from pathlib import Path

from dotenv import load_dotenv
import mysql.connector

# Local imports (work when you run from the project root as a module)
from BackEnd import main_helper as helper
from FrontEnd import menu  # assuming FrontEnd is under project/ as well

# Load .env from the parent-of-project folder
ENV_PATH = Path(__file__).resolve().parents[3] / ".env"
load_dotenv(ENV_PATH)




#Names the database and tables
DB_NAME = "Infrastructure Maintenance" #helper.sanitize_input("Example") #Can put whatever here of course, but this gets the message across
TABLES = ["Infrastructure", "Contractor", "Assignment", "MaintenanceLog"]


#Connects to the mySql database
def get_connection():
    return mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    port=int(os.getenv("DB_PORT", "3306")),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database = DB_NAME
    )

def get_name():
    return DB_NAME

#Creates the database and then selects it
def db_setup(conn):
    cur = conn.cursor()
    cur.execute(f"CREATE DATABASE IF NOT EXISTS `{DB_NAME}` "
                "CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci" )
    cur.execute(f"USE `{DB_NAME}`")
    cur.close()


#Creates the database tables
def schema_setup(conn):
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS Infrastructure(
            infrastructure_id INT AUTO_INCREMENT,
            type VARCHAR(50) NOT NULL,
            location VARCHAR(100) NOT NULL,
            install_date DATE NOT NULL,
            last_inspection DATE NOT NULL,
            state VARCHAR(50) NOT NULL,
            PRIMARY KEY(infrastructure_id)
        )
        """
    )
    
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS Contractor(
            contractor_id INT AUTO_INCREMENT,
            name VARCHAR(100) NOT NULL,
            rating DECIMAL(2,1),
            field VARCHAR(100) NOT NULL,
            cost VARCHAR(50) NOT NULL,
            PRIMARY KEY(contractor_id)
        )
        """
    )
    
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS Assignment(
            assignment_id INT AUTO_INCREMENT,
            infrastructure_id INT NOT NULL,
            contractor_id INT NOT NULL,
            task_type VARCHAR(100) NOT NULL,
            projected_cost INT NOT NULL,
            projected_start_date DATE NOT NULL,
            projected_end_date DATE NOT NULL,
            PRIMARY KEY(assignment_id),
            FOREIGN KEY(infrastructure_id) REFERENCES Infrastructure(infrastructure_id),
            FOREIGN KEY(contractor_id) REFERENCES Contractor(contractor_id)
        )
        """
    )

    cur.execute( #What would happen if the program crashed before the user could submit a maintenance log? 
        """
        CREATE TABLE IF NOT EXISTS MaintenanceLog(
            assignment_id INT, 
            start_date DATE NOT NULL,
            end_date DATE NOT NULL,
            cost INT NOT NULL,
            result VARCHAR(50) NOT NULL,
            review VARCHAR(200) NOT NULL,
            PRIMARY KEY(assignment_id),
            FOREIGN KEY(assignment_id) REFERENCES Assignment(assignment_id)
        )
        """
    )
    
    conn.commit()
    cur.close()
    

def print_tables(cur, conn):
    #Prints tables
    for table in TABLES:
        print(f"{table}:")
        cur.execute(f"SELECT * FROM {table}")
        table_info = cur.fetchall()
        print(helper.table_viewer(table, table_info))
        print("\n\n\n")


#Initializes the database and then adds our dummy data
def main_setup():
    conn = get_connection()
#Initializes the database
    db_setup(conn)
    schema_setup(conn)
    conn.commit()
#Adds dummy data
    cur = conn.cursor()
    for table in TABLES:
        cur.execute(f"SELECT 1 FROM {table} LIMIT 1") #Checks if a table has data in it
        has_rows = cur.fetchone() is not None
        if not has_rows:
            cur.execute(helper.basic_values(table))
            conn.commit()
            print(f"Created {table} and filled it with dummy data")
        else:
            print(f"{table} already contains data — skipping")
            continue
    print_tables(cur, conn)
    cur.close()
    conn.close()



def main():
    load_dotenv()
    
    main_setup()
    menu.menu()



if __name__ == "__main__":
    main()