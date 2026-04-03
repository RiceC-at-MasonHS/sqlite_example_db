# SQLite Database Lab 🐚

Welcome to Bikini Bottom! In this lab, you will learn the fundamentals of **Relational Databases** using **SQLite**.

## 🌟 What makes SQLite special?
Unlike "gold-standard" databases like PostgreSQL, which run as a separate "server" process, SQLite is **embedded**. 

- **Serverless**: No separate server to manage. The database is just a file on your disk (e.g., `citizens.db`).
- **Zero-Configuration**: No users, no permissions, no complex setup. Just point your app at the file.
- **Application File Format**: SQLite is used everywhere—from your web browser's history to your mobile phone's apps.

---

## 🏗️ Project Architecture

We are running three main containers:
1.  **Registry Web UI (Flask)**: A simple website for managing citizens (`http://localhost:5000`).
2.  **Database Browser (sqlite-web)**: A simple web-based database viewer (`http://localhost:8080`).
3.  **Citizen CLI**: A terminal environment for running raw SQL commands.

---

## 🛠️ Mission 0: Launch & Setup

1.  **Start the environment:**
    ```bash
    docker compose up -d
    ```
2.  **Initialize the database (one-time setup):**
    ```bash
    docker exec -it citizen_cli python db_tool.py init
    docker exec -it citizen_cli python db_tool.py seed
    ```

---

## 🎓 Mission 1: The CRUD Mirror (Web UI vs. SQL)

Databases revolve around **CRUD**: Create, Read, Update, and Delete. Let's perform these actions first through a "normal" website, then see the raw SQL that makes it happen.

### 1. CREATE (Adding data)
-   **Web UI**: Go to [Add Citizen](http://localhost:5000/add) and add `Plankton`, species `Plankton`, career `Evil Genius`, age `50`.
-   **SQL Equivalent** (Run in `citizen_cli`):
    ```sql
    INSERT INTO Citizens (name, species, career, age) 
    VALUES ('Lenord Fishman', 'Flounder', 'Plebian', 37);
    ```

### 2. READ (Finding data)
-   **Web UI**: Look at the main table at `http://localhost:5000/`.
-   **SQL Equivalent** (Run in `citizen_cli`):
    ```sql
    -- Find everyone older than 25, ordered by age
    SELECT * FROM Citizens WHERE age > 25 ORDER BY age DESC;
    ```

### 3. UPDATE (Modifying data)
-   **Web UI**: Click **Edit** next to Squidward and change his career to `Artist`.
-   **SQL Equivalent** (Run in `citizen_cli`):
    ```sql
    UPDATE Citizens SET career = 'Superhero' WHERE name = 'Spongebob Squarepants';
    ```

### 4. DELETE (Removing data)
-   **Web UI**: Click **Delete** next to Patrick Star.
-   **SQL Equivalent** (Run in `citizen_cli`):
    ```sql
    DELETE FROM Citizens WHERE name = 'Patrick Star';
    ```

> [!TIP]
> **Fundamental Fact:** No matter how fancy the website's button is, it is ultimately just generating and sending a SQL command to the database file!

---

## 🖥️ Mission 2: Professional Inspection (sqlite-web)

Open [sqlite-web](http://localhost:8080).

1.  **Data Explorer**: Click on the **Citizens** table name. You can instantly see all records in a spreadsheet view.
2.  **Execute SQL**: Click the **Query** tab. Type `SELECT * FROM Citizens;` and press the **Execute** button. 
3.  **Why use it?** `sqlite-web` is a perfect tool for quickly browsing database files that are stored inside a container without needing a full-blown database server.

---

## 🛡️ Mission 3: Data Integrity & Security

### 1. Constraints (The Rules)
In your `db_tool.py`, the database was created with **Constraints**:
-   `name TEXT NOT NULL`: Every citizen MUST have a name.
-   `age INTEGER CHECK(age >= 0)`: Negative ages are banned.

**Challenge:** Try to use sqlite-web's **Query** tab to insert a citizen with an age of `-5`. *What error does SQLite give you?*

### 2. SQL Injection (Security Lab)
Visit the [Security Lab](http://localhost:5000/security-lab).

-   **Internal Path**: Notice the internal database path displayed in the blue box. Because we use a **Docker Volume**, the file exists inside the container's environment, not your host desktop.
-   **Vulnerable Mode**: Search for `' OR '1'='1`. You just tricked the database into showing everything!
-   **Secured Mode**: Search for the same thing. It returns zero results because of **Parameter Binding**.

---

## 📈 Mission 4: Schema Evolution (Migrations)

As applications grow, we need more tables and columns. 

1.  **Run the Migration command:**
    ```bash
    docker exec -it citizen_cli python db_tool.py migrate
    ```
2.  **Check the changes in sqlite-web:**
    -   Refresh your browser.
    -   Notice the new `home_address` column in `Citizens`.
    -   Notice the two new tables: `Employers` and `WorksAt`.

This process of updating the database structure is called a **Migration**.
