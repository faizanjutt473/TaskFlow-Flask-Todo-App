# TaskFlow - Flask Todo App

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.x-000000?logo=flask&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-Database-003B57?logo=sqlite&logoColor=white)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5-7952B3?logo=bootstrap&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)

**TaskFlow** is a full-stack todo list web application built with **Flask**, **SQLite** and **Bootstrap 5**. It includes secure user authentication, so every user has a private workspace where they can create, edit, complete and delete their own tasks, with a clean and responsive interface and a built-in dark mode.

![TaskFlow Preview](docs/preview.png)

> The preview above is a design mockup. Replace `docs/preview.png` with a real screenshot of your running app if you like.

---

## Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [System Architecture](#system-architecture)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [Database Schema](#database-schema)
- [Application Routes](#application-routes)
- [Security](#security)
- [Documentation](#documentation)
- [Future Improvements](#future-improvements)
- [Author](#author)
- [License](#license)

---

## Features

**Authentication**
- User registration with validation (unique email, minimum password length, password confirmation)
- Secure login and logout using Flask-Login sessions
- "Remember me" option
- Passwords stored as salted hashes, never as plain text

**Task Management**
- Create, read, update and delete (CRUD) tasks
- Mark tasks as complete or undo with one click
- Priority levels: Low, Medium, High (colour coded)
- Due dates with automatic **overdue** highlighting
- Search tasks by title
- Filter by All, Active or Completed
- Dashboard cards with total, active, completed tasks and a progress bar

**User Experience**
- Fully responsive layout (desktop, tablet, mobile)
- Light and dark mode with saved preference
- Flash messages for instant feedback
- Delete confirmation to prevent mistakes

---

## Tech Stack

| Layer | Technology |
|-------|------------|
| Backend | Python, Flask |
| Authentication | Flask-Login, Werkzeug (password hashing) |
| Database | SQLite with Flask-SQLAlchemy (ORM) |
| Frontend | HTML5, Jinja2, CSS3, JavaScript |
| UI Framework | Bootstrap 5, Bootstrap Icons, Inter font |

---

## System Architecture

![Architecture](docs/architecture.png)

The browser sends HTTP requests to Flask routes. Protected routes are guarded by Flask-Login, data is read and written through the SQLAlchemy ORM to SQLite, and Jinja2 renders the final HTML response.

---

## Project Structure

```
TaskFlow-Flask-Todo-App/
├── app.py                      # Flask app: config, models, routes
├── requirements.txt            # Python dependencies
├── README.md                   # Project documentation
├── LICENSE                     # MIT License
├── .gitignore                  # Ignored files (venv, db, cache)
│
├── docs/
│   ├── architecture.png        # System architecture diagram
│   ├── preview.png             # Application preview image
│   └── TaskFlow_Project_Report.pdf   # Detailed project report
│
├── static/
│   ├── css/
│   │   └── style.css           # Custom styles + dark mode
│   └── js/
│       └── main.js             # Delete confirm, alerts, theme toggle
│
└── templates/
    ├── base.html               # Base layout (navbar, flash messages)
    ├── index.html              # Dashboard: stats, add form, task list
    ├── edit.html               # Edit task page
    ├── login.html              # Login page
    └── register.html           # Registration page
```

> The `instance/` folder (with `todo.db`) is created automatically on the first run and is ignored by Git.

---

## Getting Started

### Prerequisites
- Python 3.10 or higher
- pip

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/faizanjutt473/TaskFlow-Flask-Todo-App.git
cd TaskFlow-Flask-Todo-App

# 2. Create and activate a virtual environment
python -m venv venv

# Windows
venv\Scripts\activate
# macOS / Linux
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the application
python app.py
```

Open **http://127.0.0.1:5000** in your browser, create an account and start adding tasks.

### Configuration

Before deploying, change the secret key in `app.py`, ideally by reading it from an environment variable:

```python
import os
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "change-this-secret-key")
```

---

## Database Schema

**user**

| Column | Type | Notes |
|--------|------|-------|
| id | Integer | Primary key |
| username | String(50) | Required |
| email | String(120) | Unique, required |
| password_hash | String(255) | Hashed password |
| created_at | DateTime | Default: current time |

**task**

| Column | Type | Notes |
|--------|------|-------|
| id | Integer | Primary key |
| title | String(150) | Required |
| description | Text | Optional |
| priority | String(10) | Low / Medium / High |
| due_date | Date | Optional |
| completed | Boolean | Default: False |
| created_at | DateTime | Default: current time |
| user_id | Integer | Foreign key to user.id |

One user can own many tasks (one-to-many relationship).

---

## Application Routes

| Route | Method | Description | Auth |
|-------|--------|-------------|------|
| `/register` | GET, POST | Create a new account | No |
| `/login` | GET, POST | Log in | No |
| `/logout` | GET | Log out | Yes |
| `/` | GET | Dashboard with search and filters | Yes |
| `/add` | POST | Add a new task | Yes |
| `/edit/<id>` | GET, POST | Edit a task | Yes |
| `/toggle/<id>` | GET | Mark complete / undo | Yes |
| `/delete/<id>` | POST | Delete a task | Yes |

---

## Security

- Passwords are hashed with Werkzeug before being stored
- All task routes are protected with `@login_required`
- Every query is scoped to `current_user.id`, so users can only view or modify their own tasks
- Open-redirect protection on the post-login `next` parameter
- Jinja2 auto-escaping helps prevent XSS
- Delete actions use POST requests

---

## Documentation

A detailed project report (objectives, design, database, routes, testing and future scope) is available here:

[docs/TaskFlow_Project_Report.pdf](docs/TaskFlow_Project_Report.pdf)

---

## Future Improvements

- Task categories and tags
- Email-based password reset
- Drag-and-drop task ordering
- REST API with JWT authentication
- Pagination for large task lists
- Docker support and cloud deployment
- Unit tests with pytest

---

## Author

**Muhammad Faizan Farooq**
Machine Learning and AI Engineer

- GitHub: [@faizanjutt473](https://github.com/faizanjutt473)

---

## License

This project is licensed under the [MIT License](LICENSE).
