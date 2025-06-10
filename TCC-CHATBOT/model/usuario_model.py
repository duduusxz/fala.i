import sqlite3
import bcrypt

def get_db_connection():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn

def setup_database():
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                rm INTEGER UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                senha BLOB NOT NULL
            )
        ''')
        conn.commit()

def cadastrar_usuario(email, rm,  password):
    if not rm or not email or not password:
        return False
    try:
        hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        with get_db_connection() as conn:
            conn.execute("INSERT INTO usuarios (rm, email, senha) VALUES (?, ?, ?)", (rm, email, hashed))
        return True
    except sqlite3.IntegrityError:
        return False
    
    
    
def login_check(rm, email, password):
    with get_db_connection() as conn:
        user = conn.execute("SELECT id, senha FROM usuarios WHERE rm = ? AND email = ?", (rm, email)).fetchone()
    if user and bcrypt.checkpw(password.encode(), user['senha']):
        return user['id']
    return None
