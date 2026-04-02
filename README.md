# SQLite Citizen Registry Lab 🐚

A teaching tool designed to demonstrate relational database concepts through a SpongeBob-themed application. This repository provides a complete environment including an embedded SQLite database, a Flask web interface, a CLI management tool, and DB Browser for SQLite (DB4S) for direct database inspection.

## 🌟 Why This Lab?

This lab focuses on **SQLite**, the world's most popular embedded database. It serves as an introduction to how databases work within applications, how to enforce data integrity, and how to protect against security vulnerabilities like SQL Injection.

## 🏗️ Technical Architecture

- **Database**: [SQLite 3](https://www.sqlite.org/)
- **Backend**: Python 3.13 + Flask
- **GUI Tool**: [DB Browser for SQLite (DB4S)](https://sqlitebrowser.org/)
- **Containerization**: [Docker](https://www.docker.com/) & [Docker Compose](https://docs.docker.com/compose/)

## 🚀 Getting Started

### 1. Prerequisites
- [Docker Desktop](https://www.docker.com/products/docker-desktop/) or Docker Engine installed.

### 2. Launch the Lab
```bash
docker compose up -d
```

### 3. Services
- **Citizen Registry (Web UI)**: [http://localhost:5000](http://localhost:5000)
- **CloudBeaver (Web-based GUI)**: [http://localhost:8978](http://localhost:8978)
- **CLI Tool**: `docker exec -it citizen_cli bash`

### 4. Setup the Data
```bash
docker exec -it citizen_cli python db_tool.py init
docker exec -it citizen_cli python db_tool.py seed
```

---

## 📚 Learning Path

Please see [**LESSON.md**](./LESSON.md) for the guided missions and instructions.

## 🛡️ Security Lab

Explore SQL Injection vulnerabilities and learn about **Parameter Binding** at [http://localhost:5000/security-lab](http://localhost:5000/security-lab).

---

GPL-3.0 License
