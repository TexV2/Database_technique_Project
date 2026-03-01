
def dropAllTables(dbName, connection):
    conn = connection
    cur = conn.cursor()
    cur.execute(f"DROP DATABASE IF EXISTS `{dbName}`")
    conn.commit()
    cur.close()
    conn.close()
