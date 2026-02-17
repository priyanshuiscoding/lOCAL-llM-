import psycopg2
from psycopg2 import sql

# Step 1: Connect to the default 'postgres' database
conn = psycopg2.connect(
    dbname="postgres",
    user="postgres",
    password="5386",  # replace with your actual password
    host="127.0.0.1",
    port="5432"
)
conn.autocommit = True  # Needed to create a new database
cur = conn.cursor()

# Step 2: Create a new database (if not exists)
db_name = "mytestdb"
try:
    cur.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(db_name)))
    print(f"✅ Database '{db_name}' created.")
except psycopg2.errors.DuplicateDatabase:
    print(f"ℹ️ Database '{db_name}' already exists.")

cur.close()
conn.close()

# Step 3: Connect to the newly created database
conn2 = psycopg2.connect(
    dbname=db_name,
    user="postgres",
    password="5386",
    host="127.0.0.1",
    port="5432"
)
cur2 = conn2.cursor()

# Step 4: Create a table
cur2.execute("""
    CREATE TABLE IF NOT EXISTS employees (
        id SERIAL PRIMARY KEY,
        name VARCHAR(100),
        age INT,
        department VARCHAR(50)
    )
""")
print("✅ Table 'employees' created or already exists.")

# Step 5: Insert data
cur2.execute("""
    INSERT INTO employees (name, age, department)
    VALUES (%s, %s, %s)
""", ("Priyanshu", 23, "AI & Robotics"))
print("✅ Data inserted.")

# Step 6: Commit & close
conn2.commit()
cur2.close()
conn2.close()
