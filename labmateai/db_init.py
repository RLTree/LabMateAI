import sqlite3


def initialize_db(db_path='labmateai.db'):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Create users table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_name TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        department TEXT,
        role TEXT
    )
    ''')

    # Create tools table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS tools (
        tool_id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        category TEXT,
        features TEXT,
        cost TEXT,
        description TEXT,
        language TEXT,
        platform TEXT
    )
    ''')

    # Create interactions table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS interactions (
        interaction_id INTEGER PRIMARY KEY,
        user_id INTEGER,
        tool_id INTEGER,
        rating INTEGER,
        usage_frequency TEXT,
        timestamp TEXT,
        FOREIGN KEY(user_id) REFERENCES users(user_id),
        FOREIGN KEY(tool_id) REFERENCES tools(tool_id)
    )
    ''')

    conn.commit()
    conn.close()


if __name__ == '__main__':
    initialize_db()
