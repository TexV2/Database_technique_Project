from BackEnd import helper
import os
import mysql.connector

#Names the database and tables
DB_NAME = "InfrastructureMaintenance" #helper.sanitize_input("Example", True) #Can put whatever here of course, but this gets the message across
TABLES = ["Infrastructure", "Contractor", "Assignment", "MaintenanceLog"]

def get_name():
    return DB_NAME

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
    print("Created entity: Infrastructure")
    
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS Contractor(
            contractor_id INT AUTO_INCREMENT,
            name VARCHAR(100) NOT NULL,
            rating INT NOT NULL,
            field VARCHAR(100) NOT NULL,
            cost VARCHAR(50) NOT NULL,
            PRIMARY KEY(contractor_id)
        )
        """
    )
    print("Created entity: Contractor")

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
    print("Created entity: Assignment")

    cur.execute(
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
    print("Created entity: MaintenanceLog\n")
    
    conn.commit()
    cur.close()

def add_dummy_data(cur, conn):
    for table in TABLES:
        cur.execute(f"SELECT 1 FROM {table} LIMIT 1") #Checks if a table has data in it
        has_rows = cur.fetchone() is not None
        if not has_rows:
            cur.execute(helper.basic_values(table))
            conn.commit()
            print(f"Filled {table} with dummy data")
        else:
            print(f"{table} already contains data — skipping")
            continue
        #Prints the tables
        helper.print_tables(cur)

def advanced_mysql(cur, conn):
    cur.execute("DROP TRIGGER IF EXISTS UpdateLastInspection") #Infrastructure last_inspection updates to current date if state changes
    conn.commit()
    cur.execute("""
                DELIMITER $$
                CREATE TRIGGER UpdateLastInspection
                BEFORE UPDATE ON Infrastructure
                FOR EACH ROW
                BEGIN
                    IF OLD.state != NEW.state THEN
                        SET NEW.last_inspection = CURDATE();
                    END IF;
                END $$
                DELIMITER ;
                """)
    conn.commit()

    cur.execute("DROP FUNCTION IF EXISTS CountNumContractorJobs")
    conn.commit()
    cur.execute("""
                DELIMITER $$
                CREATE FUNCTION CountNumContractorJobs(p_contractor_id INT)
                RETURNS INT
                DETERMINISTIC
                BEGIN
                    DECLARE checkIfIDExists INT;
                    DECLARE numJobs INT;
                    
                    SELECT COUNT(*)
                    INTO checkIfIDExists
                    FROM Contractor
                    WHERE contractor_id = p_contractor_id;
                    
                    IF checkIfIDExists != 1 THEN
                        RETURN 0;
                    ELSE
                        SELECT COUNT(*)
                        INTO numJobs
                        FROM Assignment a
                        INNER JOIN MaintenanceLog ml 
                        ON a.assignment_id = ml.assignment_id AND a.contractor_id = p_contractor_id;
                        RETURN numJobs;
                    END IF;
                END$$
                DELIMITER ;
                """)
    conn.commit()



def main_setup(dummy_data = True):
    conn = get_connection(use_db=False)
#Drop existing database
    cur = conn.cursor()
    cur.execute(f"DROP DATABASE IF EXISTS `{DB_NAME}`")
    cur.close()
    conn.close()
#Initializes the database
    conn = get_connection(use_db=False)
    db_setup(conn)
    schema_setup(conn)
#Adds dummy data
    cur = conn.cursor()
    if dummy_data:
        add_dummy_data(cur, conn)
    cur.close()
    conn.close()
#Creates functions and triggers
    conn = get_connection()
    cur = conn.cursor()
    advanced_mysql(cur, conn)
    cur.close()
    conn.close()



#Connects to the mySql database
def get_connection(use_db=True):
    config = dict(
        host=os.getenv("DB_HOST"),
        port=int(os.getenv("DB_PORT", "3306")),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
    )
    if use_db:
        config["database"] = DB_NAME
    return mysql.connector.connect(**config)



#Creates the database and then selects it
def db_setup(conn):
    cur = conn.cursor()
    cur.execute(f"CREATE DATABASE IF NOT EXISTS `{DB_NAME}` "
                "CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci" )
    cur.execute(f"USE `{DB_NAME}`")
    cur.close()

