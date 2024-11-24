import mysql.connector
from mysql.connector import errorcode
from faker import Faker
import random

# Database connection configuration
config = {
    'user': 'root',
    'password': '',
    'host': 'localhost',
}

# Initialize Faker
fake = Faker()

# Database and tables definition
db_name = "school_management"
tables = {
    "Admin": """
        CREATE TABLE Admin (
           admin_id INT NOT NULL AUTO_INCREMENT,
           name VARCHAR(50),
           email VARCHAR(60),
           phone_number VARCHAR(20),
           password VARCHAR(50),
           PRIMARY KEY (admin_id)
        );
    """,
    "Teatcher": """
        CREATE TABLE Teatcher (
           admin_id2 INT NOT NULL AUTO_INCREMENT,
           name VARCHAR(50),
           email VARCHAR(60),
           phone_number VARCHAR(20),
           password VARCHAR(50),
           PRIMARY KEY (admin_id2)
        );
    """,
    "Student": """
        CREATE TABLE Student (
           student_id CHAR(10) NOT NULL,
           name VARCHAR(50),
           date_of_birth DATE,
           email VARCHAR(60),
           phone_number VARCHAR(20),
           password VARCHAR(50),
           PRIMARY KEY (student_id)
        );
    """,
    "Classes": """
        CREATE TABLE Classes (
           class_id INT NOT NULL AUTO_INCREMENT,
           class_name VARCHAR(50),
           section VARCHAR(50),
           level VARCHAR(50),
           PRIMARY KEY (class_id)
        );
    """,
    "Module": """
        CREATE TABLE Module (
           module_id INT NOT NULL AUTO_INCREMENT,
           class_id INT NOT NULL,
           module_name VARCHAR(50),
           description VARCHAR(100),
           semester VARCHAR(50),
           PRIMARY KEY (module_id),
           FOREIGN KEY (class_id) REFERENCES Classes (class_id) ON DELETE RESTRICT ON UPDATE RESTRICT
        );
    """,
    "Subject": """
        CREATE TABLE Subject (
           subject_id INT NOT NULL AUTO_INCREMENT,
           module_id INT NOT NULL,
           admin_id2 INT NOT NULL,
           subject_name VARCHAR(50),
           numbers_hours INT,
           passed_hours INT,
           PRIMARY KEY (subject_id),
           FOREIGN KEY (module_id) REFERENCES Module (module_id) ON DELETE RESTRICT ON UPDATE RESTRICT,
           FOREIGN KEY (admin_id2) REFERENCES Teatcher (admin_id2) ON DELETE RESTRICT ON UPDATE RESTRICT
        );
    """,
    "Courses": """
        CREATE TABLE Courses (
           Course_id INT NOT NULL AUTO_INCREMENT,
           subject_id INT NOT NULL,
           course_name VARCHAR(50),
           file_name VARCHAR(50),
           PRIMARY KEY (Course_id),
           FOREIGN KEY (subject_id) REFERENCES Subject (subject_id) ON DELETE RESTRICT ON UPDATE RESTRICT
        );
    """,
    "student_subject_information": """
        CREATE TABLE student_subject_information (
           module_id INT NOT NULL,
           subject_id INT NOT NULL,
           student_id CHAR(10) NOT NULL,
           Exam FLOAT,          
           Controle FLOAT,
           Tp FLOAT, 
           Moyenne FLOAT,          
           Presance INT,
           PRIMARY KEY (subject_id, student_id),
           FOREIGN KEY (student_id) REFERENCES Student (student_id) ON DELETE RESTRICT ON UPDATE RESTRICT,
           FOREIGN KEY (module_id) REFERENCES Module (module_id) ON DELETE RESTRICT ON UPDATE RESTRICT,
           FOREIGN KEY (subject_id) REFERENCES Subject (subject_id) ON DELETE RESTRICT ON UPDATE RESTRICT
        );
    """,
    "Supervision": """
        CREATE TABLE Supervision (
           admin_id INT NOT NULL,
           class_id INT NOT NULL,
           PRIMARY KEY (admin_id, class_id),
           FOREIGN KEY (admin_id) REFERENCES Admin (admin_id) ON DELETE RESTRICT ON UPDATE RESTRICT,
           FOREIGN KEY (class_id) REFERENCES Classes (class_id) ON DELETE RESTRICT ON UPDATE RESTRICT
        );
    """
}

# Connect to MySQL
try:
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()

    # Create the database
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
    cursor.execute(f"USE {db_name}")
    print(f"Database '{db_name}' created/selected successfully.")

    # Create tables
    for table_name, table_sql in tables.items():
        try:
            cursor.execute(table_sql)
            print(f"Table '{table_name}' created successfully.")
        except mysql.connector.Error as err:
            print(f"Error creating table '{table_name}': {err.msg}")

    # Insert fake data into tables
    # Admin Table
    for _ in range(5):
        cursor.execute("""
            INSERT INTO Admin (name, email, phone_number, password) 
            VALUES (%s, %s, %s, %s)
        """, (fake.name(), fake.email(), fake.phone_number(), fake.password()))

    # Teatcher Table
    for _ in range(5):
        cursor.execute("""
            INSERT INTO Teatcher (name, email, phone_number, password) 
            VALUES (%s, %s, %s, %s)
        """, (fake.name(), fake.email(), fake.phone_number(), fake.password()))

    # Student Table
    student_ids = []  # Save generated student IDs
    for _ in range(10):
        student_id = str(fake.unique.random_number(digits=10))
        student_ids.append(student_id)
        cursor.execute("""
            INSERT INTO Student (student_id, name, date_of_birth, email, phone_number, password) 
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (student_id, fake.name(), fake.date_of_birth(), fake.email(), fake.phone_number(), fake.password()))

    # Classes Table
    for _ in range(3):
        cursor.execute("""
            INSERT INTO Classes (class_name, section, level) 
            VALUES (%s, %s, %s)
        """, (fake.word(), fake.word(), fake.word()))

    # Module Table
    for class_id in range(1, 4):
        for _ in range(2):
            cursor.execute("""
                INSERT INTO Module (class_id, module_name, description, semester) 
                VALUES (%s, %s, %s, %s)
            """, (class_id, fake.word(), fake.text(), fake.word()))

    # Subject Table
    for module_id in range(1, 7):
        for _ in range(2):
            cursor.execute("""
                INSERT INTO Subject (module_id, admin_id2, subject_name, numbers_hours, passed_hours) 
                VALUES (%s, %s, %s, %s, %s)
            """, (module_id, random.randint(1, 5), fake.word(), random.randint(30, 60), random.randint(10, 30)))

    # Supervision Table
    for admin_id in range(1, 6):
        for class_id in range(1, 4):
            cursor.execute("""
                INSERT INTO Supervision (admin_id, class_id) 
                VALUES (%s, %s)
            """, (admin_id, class_id))

    # student_subject_information Table
    for student_id in student_ids:
        for subject_id in range(1, 13):
            module_id = (subject_id - 1) // 2 + 1  # Assuming 2 subjects per module
            cursor.execute("""
                INSERT INTO student_subject_information (module_id, subject_id, student_id, Exam, Controle, Tp, Moyenne, Presance) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (module_id, subject_id, student_id, random.uniform(0, 20), random.uniform(0, 20), random.uniform(0, 20), random.uniform(0, 20), random.randint(0, 20)))

    # Commit changes to the database
    conn.commit()
    print("Fake data inserted successfully.")

except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Invalid credentials: Please check your username and password.")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist.")
    else:
        print(err)

finally:
    if conn.is_connected():
        cursor.close()
        conn.close()
        print("Connection closed.")
