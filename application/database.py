import mysql.connector
from config import Config
from mysql.connector import Error
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, scoped_session

# Database connection configuration
DB_CONFIG = {
    'host': Config.DB_HOST,
    'user': Config.DB_USER,         # Change to your MySQL username
    'password': Config.DB_PWD, # Change to your MySQL password
    'database': Config.DB_NAME    # Change to your database name
}

# Utility function to get DB connection
def get_db_connection():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except Error as e:
        print(f"Database connection error: {e}")
        return None

# Create table if not exists
def init_db():
    conn = get_sqlalchemy_db_connection()
    if conn:
        conn.execute(text('''
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                password VARCHAR(250) NOT NULL,
                email VARCHAR(100) UNIQUE NOT NULL,
                theme VARCHAR(50) DEFAULT 'light',
                created_at TIMESTAMP DEFAULT NOW()
            );
            '''))
        conn.execute(text('''
                CREATE TABLE IF NOT EXISTS employees (
                id INT AUTO_INCREMENT PRIMARY KEY,
                emp_org_id INT  NOT NULL UNIQUE,
                first_name VARCHAR(100) NOT NULL,
                last_name VARCHAR(100) NOT NULL,
                work_email VARCHAR(200) NOT NULL UNIQUE,
                compentency VARCHAR(100),
                reporting_to INTEGER,
                grade VARCHAR(20),
                project_id INT,
                doj DATE,
                allocation_type VARCHAR(50),
                allocation_percent INTEGER,
                designation VARCHAR(100),
                created_at TIMESTAMP DEFAULT NOW()
            );
        '''))
        conn.execute(text('''
            CREATE TABLE if not exists projects (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            bussines_group TEXT,
            hd INT,
            customer_id INT,
            project_currency VARCHAR(50) DEFAULT 'INR',
            status VARCHAR(50) DEFAULT 'ongoing',
            manager_id INT REFERENCES employees(id),
            created_at TIMESTAMP DEFAULT NOW()
            );
        '''))
        conn.execute(text('''
            CREATE TABLE  if not exists reporting_managers (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            email VARCHAR(150) UNIQUE NOT NULL,
            created_at TIMESTAMP DEFAULT NOW()
            );
        '''))
        conn.execute(text('''
            CREATE TABLE  if not exists bussiness_groups (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            created_at TIMESTAMP DEFAULT NOW()
            );
        '''))
        conn.execute(text('''
            CREATE TABLE  if not exists customers (
            id SERIAL PRIMARY KEY,
            bussiness_group_id INT NOT NULL,
            customer_name VARCHAR(100) NOT NULL,
            customer_code VARCHAR(150) UNIQUE NOT NULL,
            created_at TIMESTAMP DEFAULT NOW()
            );
        '''))
        conn.commit()
        print("DB tables created successfully!!")
    return conn


def get_sqlalchemy_db_connection():
    engine = create_engine(Config.DATABASE_URL, pool_size=10, max_overflow=30, pool_pre_ping=True, pool_recycle=280, echo=False, future=True)
    print("Sql Alchemy connection created successfully.")
    session_factory = sessionmaker(bind=engine, autocommit=False, autoflush=False)
    Session = scoped_session(session_factory)
    return Session

