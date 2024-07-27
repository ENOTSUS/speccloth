import sqlite3

DATABASE = 'database.db'


def create_tables():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute('''
      CREATE TABLE employees (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    position TEXT NOT NULL,
    login TEXT NOT NULL,
    password TEXT NOT NULL
);
    ''')

    conn.commit()
    conn.close()


if __name__ == '__main__':
    create_tables()
