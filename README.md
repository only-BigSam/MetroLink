# MetroLink

MetroLink is a desktop transport booking and management system prototype built with Python. It demonstrates a complete backend API for managing passengers, drivers, vehicles, routes, trips, bookings, and administrators. The project is designed as a proof of concept for a larger transport management system where additional business rules and production features will be implemented.

---

## Features

### Authentication

* User registration
* Secure login using JWT authentication
* Role-based access control
* Password hashing

### Passenger

* View available trips
* Book seats
* Cancel bookings
* View booking history

### Driver

* View assigned trips
* Start scheduled trips
* Complete trips
* View passengers assigned to a trip

### Administrator

* Manage users
* Manage drivers
* Manage vehicles
* Manage routes
* Manage trips
* View bookings
* View system statistics

---

## Technology Stack

* Python 3.13
* FastAPI
* SQLAlchemy
* PostgreSQL
* Pydantic
* JWT Authentication
* Uvicorn

---

## Project Structure

```text
MetroLink/
│
├── backend/
│   ├── core/
│   ├── database/
│   ├── models/
│   ├── routes/
│   ├── schemas/
│   ├── main.py
│   └── requirements.txt
│
├── tests/
│
├── frontend/        (Coming Soon)
│
└── README.md
```

---

## Installation

Clone the repository:

```bash
git clone <repository-url>
```

Move into the backend directory:

```bash
cd MetroLink/backend
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate the virtual environment.

Install dependencies:

```bash
pip install -r requirements.txt
```

Configure your environment variables by creating a `.env` file inside the `backend` folder.

Run the application:

```bash
uvicorn main:app --reload
```

The API will be available at:

```
http://127.0.0.1:8000
```

Interactive documentation:

```
http://127.0.0.1:8000/docs
```

---

## Current Status

Backend development is complete for the prototype.

The next phase is building the desktop graphical user interface (GUI) using CustomTkinter.

---

## Author

Samuel Daniel
