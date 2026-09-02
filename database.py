import sqlite3


DB_NAME = "memory.db"


def get_connection():
    return sqlite3.connect(DB_NAME)


def init_database():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS memories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_prompt TEXT NOT NULL,
            result TEXT NOT NULL
        )
    """)

    connection.commit()
    connection.close()