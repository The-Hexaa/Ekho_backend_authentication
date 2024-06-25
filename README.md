
# Daily Report Flask Application

This is a Flask application for submitting and managing daily reports. The application includes user authentication and allows team members to submit their daily work reports. The application uses SQLite for database storage and is containerized using Docker.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Setup](#setup)
  - [Docker Setup](#docker-setup)
- [Usage](#usage)
  - [Running with Docker](#running-with-docker)
- [Project Structure](#project-structure)

## Prerequisites

Before you begin, ensure you have the following installed on your system:

- Docker
- Docker Compose
- Visual Studio Code with the Remote - Containers extension

## Setup

### Docker Setup

1. **Clone the repository:**

   ```bash
   git clone https://github.com/The-Hexaa/daily-reports.git
   cd repository
   ```

2. **Open the project in Visual Studio Code:**

   Open Visual Studio Code, and then open the cloned repository folder.

3. **Reopen the project in the container:**

   When prompted by Visual Studio Code, select “Reopen in Container” to start the development container using the specified configuration in `.devcontainer/devcontainer.json`.

4. **Set up the database:**

   Once inside the dev container, set up the database by running:

   ```bash
   python init_db.py
   ```

## Usage

### Running with Docker

1. **Build and run the Docker container:**

   ```bash
   docker-compose up --build
   ```

   The application will be accessible at `http://127.0.0.1:5000`.

## Project Structure

```
daily-report/
├── .devcontainer/
│   └── devcontainer.json
├── .github/
│   └── dependabot.yml
├── Dockerfile
├── __pycache__/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── models.py
│   ├── static/
│   │   └── style.css
│   └── templates/
│       ├── base.html
│       ├── index.html
│       ├── login.html
│       ├── register.html
│       └── report.html
├── docker-compose.yml
├── init_db.py
├── instance/
│   └── database.db
├── requirements.txt
└── run.py
```
