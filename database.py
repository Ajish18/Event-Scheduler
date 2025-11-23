import sqlite3

db_name = "events.db"

def create_tables():
    con=sqlite3.connect(db_name)
    cur=con.cursor()

    #event table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS Event (
            event_id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            start_time TEXT NOT NULL,
            end_time TEXT NOT NULL,
            description TEXT
        );
    """)

    #resource table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS Resource (
            resource_id INTEGER PRIMARY KEY AUTOINCREMENT,
            resource_name TEXT NOT NULL,
            resource_type TEXT NOT NULL
        );
    """)

    #allocation table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS EventResourceAllocation (
            allocation_id INTEGER PRIMARY KEY AUTOINCREMENT,
            event_id INTEGER NOT NULL,
            resource_id INTEGER NOT NULL,
            FOREIGN KEY(event_id) REFERENCES Event(event_id),
            FOREIGN KEY(resource_id) REFERENCES Resource(resource_id)
        );
    """)

    con.commit()
    con.close()
