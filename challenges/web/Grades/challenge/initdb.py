import sqlite3
from hashlib import sha256

def init_db():
    conn = sqlite3.connect('grades.db')
    c = conn.cursor()
    c.execute('DROP TABLE IF EXISTS users')

    # Create the users table
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            email TEXT NOT NULL,
            reset_token TEXT DEFAULT NULL,
            reset_token_expires_at DATETIME DEFAULT NULL
        )
    ''')
    
    # Create the grades table
    c.execute('''
        CREATE TABLE IF NOT EXISTS grades (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            grade TEXT NOT NULL,
            FOREIGN KEY (username) REFERENCES users (username)
        )
    ''')

    # Insert admin user with pre-hashed password and default reset_token values
    admin_password = sha256('f8b6f7759d913137811994b7a127046efd36bedf47b2cf31f80c9469d7548daf'.encode()).hexdigest()
    c.execute('''
        INSERT OR IGNORE INTO users (username, password, email, reset_token, reset_token_expires_at)
        VALUES (?, ?, ?, NULL, NULL)
    ''', ('admin', admin_password, 'admin@example.com'))

    # Insert user1 with pre-hashed password and default reset_token values
    user_password = '76c94ff1a292bb55cb47de1890cd6ac5beb5d34977d9ad307de7aa47fb79edd6'  # Pre-hashed password
    c.execute('''
        INSERT OR IGNORE INTO users (username, password, email, reset_token, reset_token_expires_at)
        VALUES (?, ?, ?, NULL, NULL)
    ''', ('user1', user_password, 'user1@example.com'))

    # Insert sample grades
    c.execute('INSERT OR IGNORE INTO grades (username, grade) VALUES (?, ?)', ('user1', 'A'))
    c.execute('INSERT OR IGNORE INTO grades (username, grade) VALUES (?, ?)', ('user1', 'B'))
    c.execute('INSERT OR IGNORE INTO grades (username, grade) VALUES (?, ?)', ('admin', 'A'))

    # Commit changes and close the connection
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    print("Database initialized successfully.")
