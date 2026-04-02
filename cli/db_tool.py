import sqlite3
import os
import argparse
import sys

DATABASE = os.getenv("DATABASE_PATH", "/data/citizens.db")

def get_connection():
    return sqlite3.connect(DATABASE)

def init_db():
    print(f"Initializing database at {DATABASE}...")
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Citizens (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            species TEXT,
            career TEXT,
            age INTEGER CHECK(age >= 0)
        )
    """)
    conn.commit()
    conn.close()
    print("Database initialized successfully.")

def seed_db():
    print("Seeding database with initial data...")
    conn = get_connection()
    cursor = conn.cursor()
    citizens = [
        ('Spongebob Squarepants', 'Sea Sponge', 'Fry Cook', 22),
        ('Patrick Star', 'Starfish', 'Unemployed', 22),
        ('Squidward Tentacles', 'Octopus', 'Cashier', 30),
        ('Eugene Krabs', 'Crab', 'Restaurant Owner', 62),
        ('Sandy Cheeks', 'Squirrel', 'Scientist', 25)
    ]
    cursor.executemany(
        "INSERT INTO Citizens (name, species, career, age) VALUES (?, ?, ?, ?)",
        citizens
    )
    conn.commit()
    conn.close()
    print("Database seeded successfully.")

def migrate():
    print("Running migrations...")
    conn = get_connection()
    cursor = conn.cursor()
    try:
        # Add home_address column
        cursor.execute("ALTER TABLE Citizens ADD COLUMN home_address TEXT")
        print("Added home_address column to Citizens table.")

        # Create Employers table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Employers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                company_name TEXT NOT NULL,
                industry TEXT
            )
        """)
        print("Created Employers table.")

        # Create WorksAt table (Linking table)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS WorksAt (
                citizen_id INTEGER,
                employer_id INTEGER,
                job_title TEXT,
                FOREIGN KEY (citizen_id) REFERENCES Citizens(id),
                FOREIGN KEY (employer_id) REFERENCES Employers(id),
                PRIMARY KEY (citizen_id, employer_id)
            )
        """)
        print("Created WorksAt table with foreign keys.")

        # Seed some advanced data
        cursor.execute("INSERT INTO Employers (company_name, industry) VALUES ('Krusty Krab', 'Fast Food')")
        cursor.execute("INSERT INTO Employers (company_name, industry) VALUES ('Chum Bucket', 'Evil / Fast Food')")
        
        conn.commit()
        print("Migrations complete.")
    except sqlite3.OperationalError as e:
        print(f"Migration error (already run?): {e}")
    finally:
        conn.close()

def reset_db():
    if os.path.exists(DATABASE):
        os.remove(DATABASE)
        print(f"Removed database at {DATABASE}")
    init_db()

def main():
    parser = argparse.ArgumentParser(description="Citizen DB Management Tool")
    parser.add_argument("command", choices=["init", "seed", "migrate", "reset", "shell"], help="Command to run")
    
    args = parser.parse_args()
    
    if args.command == "init":
        init_db()
    elif args.command == "seed":
        seed_db()
    elif args.command == "migrate":
        migrate()
    elif args.command == "reset":
        reset_db()
    elif args.command == "shell":
        # Launch sqlite3 shell
        os.system(f"sqlite3 {DATABASE}")

if __name__ == "__main__":
    main()
