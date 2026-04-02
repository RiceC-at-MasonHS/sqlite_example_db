# SQLite Database Lab 🐚

Welcome to Bikini Bottom! In this lab, you will learn the fundamentals of **Relational Databases** using **SQLite**, the most widely deployed database engine in the world.

## 🚀 Why SQLite?

Unlike "gold-standard" databases like PostgreSQL, which run as a separate "server" process, SQLite is **embedded**. 

### 🌟 1. Unique Features of SQLite
- **Serverless**: There is no separate "server" to install or manage. The database engine runs directly as part of your application.
- **Zero-Configuration**: No setup, no users, no permissions to manage. Just point your app at a file.
- **Single File**: The entire database (tables, indexes, and data) is stored in **one single file** on your hard drive (e.g., `citizens.db`).
- **Application File Format**: Because it's a single file, SQLite is often used as a file format for applications. For example:
    - **Web Browsers**: Your Chrome/Firefox history and cookies are stored in SQLite files.
    - **Mobile Apps**: Most iOS and Android apps use SQLite to store local data.
    - **Adobe Lightroom**: Uses SQLite for its catalog format.

---

## 🏗️ Project Architecture

This lab environment consists of three containers:
1.  **Registry Web UI (Flask)**: A simple website to view and manage citizens (`http://localhost:5000`).
2.  **DB Browser for SQLite (DB4S)**: A professional GUI to inspect the raw database (`http://localhost:3000`).
3.  **Citizen CLI**: A terminal tool for advanced database operations and manual SQL commands.

---

## 🛠️ Quick Start

### 1. Launch the Lab
Run the following command to start the environment:

```bash
docker compose up -d
```

### 2. Initialize the Database
Before the website can show anything, we need to create the table and add some data.

```bash
# Enter the CLI container
docker exec -it citizen_cli bash

# Inside the container, run these commands:
python db_tool.py init
python db_tool.py seed
```

---

## 🎓 Mission 1: Core SQL (CRUD)

CRUD stands for **Create, Read, Update, and Delete**. Open the **Citizen CLI** or use the **Execute SQL** tab in DB Browser (`http://localhost:3000`) to run these commands.

### 1. CREATE (Insert Data)
Let's add a new citizen to Bikini Bottom.

```sql
INSERT INTO Citizens (name, species, career, age) 
VALUES ('Plankton', 'Plankton', 'Evil Genius', 50);
```

### 2. READ (Select Data)
Find specific citizens using filters.

```sql
-- Find all sea sponges
SELECT * FROM Citizens WHERE species = 'Sea Sponge';

-- Find everyone older than 25, ordered by age
SELECT * FROM Citizens WHERE age > 25 ORDER BY age DESC;
```

### 3. UPDATE (Modify Data)
Squidward finally got a promotion (or a pay cut).

```sql
UPDATE Citizens SET career = 'Artist' WHERE name = 'Squidward Tentacles';
```

### 4. DELETE (Remove Data)
Someone moved out of town.

```sql
DELETE FROM Citizens WHERE name = 'Patrick Star';
```

---

## 🛡️ Mission 2: Data Integrity & Constraints

Databases aren't just for storing data; they're for **protecting** it. We use **Constraints** to enforce rules.

### 1. NOT NULL
We should never have a citizen without a name.
```sql
-- In our schema, the 'name' column is defined as:
-- name TEXT NOT NULL
```

### 2. CHECK Constraints
In our CLI tool (`db_tool.py`), we defined the `age` column with a rule:
```sql
-- age INTEGER CHECK(age >= 0)
```
Try to insert a citizen with a negative age in DB Browser and see what happens!

---

## 🔐 Mission 3: SQL Injection (Security Lab)

Visit `http://localhost:5000/security-lab` in your browser.

### The Danger: String Concatenation
When developers build queries by adding strings together, attackers can "inject" their own SQL.

**The Vulnerable Query (in Python):**
```python
query = f"SELECT * FROM Citizens WHERE name = '{user_input}'"
```

If an attacker types `' OR '1'='1`, the final query becomes:
`SELECT * FROM Citizens WHERE name = '' OR '1'='1'`
Since `1=1` is always true, the database returns **every single record**!

### The Solution: Parameter Binding
Professional developers use **Parameter Binding**. We send the query and the data to the database separately.

**The Secure Query (in Python):**
```python
# The '?' is a placeholder
cursor.execute("SELECT * FROM Citizens WHERE name = ?", (user_input,))
```
The database now treats the entire input as a single literal string, making the attack impossible.

---

## 📈 Mission 4: Schema Evolution (Migrations)

As applications grow, their databases must change. We call this a **Migration**.

### 1. Adding a Column
Bikini Bottom now needs to track home addresses.
```sql
ALTER TABLE Citizens ADD COLUMN home_address TEXT;
```

### 2. Linking Tables (Foreign Keys)
Let's create an `Employers` table and link it to our `Citizens`.

```sql
CREATE TABLE Employers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    company_name TEXT NOT NULL,
    industry TEXT
);

-- Linking table (Many-to-Many or One-to-Many)
CREATE TABLE WorksAt (
    citizen_id INTEGER,
    employer_id INTEGER,
    job_title TEXT,
    FOREIGN KEY (citizen_id) REFERENCES Citizens(id),
    FOREIGN KEY (employer_id) REFERENCES Employers(id)
);
```

**Run the migration command in the CLI container:**
```bash
python db_tool.py migrate
```

Now use DB Browser to see how the "Database Structure" has changed!
