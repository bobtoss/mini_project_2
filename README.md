# Student Management System


## Features

- **User Authentication**: JWT-based authentication using Djoser.
- **Student and Course Management**: Manage student profiles, courses, and enrollments.
- **Attendance and Grade Tracking**: Keep track of student attendance and grades.
- **Email and Push Notifications**: Asynchronous notifications using Celery and Redis.
- **Caching**: Use Redis to cache frequently accessed data.
- **Real-Time Notifications**: Implemented using Django Channels for WebSocket support (optional).

---

## Table of Contents

- [Prerequisites](#prerequisites)
- [Setup and Installation](#setup-and-installation)
- [Project Structure](#project-structure)
- [Running the Project](#running-the-project)
- [Testing](#testing)

---

## Prerequisites

- Python 3.8+
- Redis
- SQLite (or another supported database)

---

## Setup and Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-username/student-management-system.git
   cd student-management-system

2. **Create a Virtual Environment**:
   ```bash
   python -m venv venv
    source venv/bin/activate  # On macOS/Linux
    venv\Scripts\activate  # On Windows

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt

4. **Set Up setting.py**:
   ```bash
    DEBUG=True
    EMAIL_HOST=smtp.gmail.com
    EMAIL_PORT=587
    EMAIL_HOST_USER=your_email@example.com
    EMAIL_HOST_PASSWORD=your_email_password
    REDIS_URL=redis://127.0.0.1:6379/0

5. **Create a Superuser**:
   ```bash
    python manage.py createsuperuser

6. **Start the Development Server**:
   ```bash
    python manage.py runserver

## Running the Project

1. **Start Redis**:
   ```bash
    redis-server

2. **Start the Celery Worker**:
   ```bash
    celery -A StudentManagementSystem worker --loglevel=info
   
3. **Start the Celery Beat Scheduler**:
   ```bash
    celery -A StudentManagementSystem worker --loglevel=info

## Testing

1. **Run Unit Tests**:
   ```bash
    python manage.py test
