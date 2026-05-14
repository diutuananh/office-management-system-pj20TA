# Office Management System

This is a simple Office Management System built using Flask, MySQL, HTML, CSS, and JavaScript. The system is designed to manage office equipment, departments, maintenance records, and purchase history.

## Features

- Dashboard displaying total equipment statistics
- Equipment management (add and delete equipment)
- Department-based equipment classification
- Search functionality for equipment list
- Autocomplete support for equipment type and unit
- Maintenance tracking module
- Purchase history tracking
- Data visualization using Chart.js

## Technologies Used

- Backend: Flask (Python)
- Database: MySQL
- Frontend: HTML, CSS, JavaScript
- Charting: Chart.js

## Project Structure

```
Project12_diux/
│
├── app.py
├── office_management.sql
│
├── templates/
│   ├── dashboard.html
│   ├── equipment.html
│   ├── add_equipment.html
│   ├── maintenance.html
│   └── purchases.html
│
├── static/
│   └── style.css
│
└── README.md
```

## Database Setup

### Step 1: Create Database

Run the following SQL commands in MySQL:

```
CREATE DATABASE office_management;
USE office_management;
```

### Step 2: Import Database

Import the provided SQL file:

```
office_management.sql
```

Or execute it using MySQL Workbench.

## Installation and Running the Project

### Step 1: Clone the repository

```
git clone https://github.com/diutuananh/office-management-system-pj20TA.git
cd office-management-system-pj20TA
```

### Step 2: Install dependencies

```
pip install flask mysql-connector-python
```

### Step 3: Configure database connection

Open `app.py` and update:

```
host = "127.0.0.1"
user = "root"
password = "123456"
database = "office_management"
port = 3306
```

### Step 4: Run the application

```
python app.py
```

### Step 5: Open browser

```
http://127.0.0.1:5000
```

## System Pages

- Dashboard: Displays overall statistics and charts
- Equipment: Displays list of equipment
- Add Equipment: Form to add new equipment
- Maintenance: Displays maintenance records
- Purchases: Displays purchase records

## Notes

- Ensure MySQL server is running before starting the application
- Default Flask port is 5000
- Database credentials must match your local MySQL configuration

## Future Improvements

- Add edit/update equipment functionality
- Implement user authentication system
- Improve UI using Bootstrap or Tailwind CSS
- Add pagination and filtering features
- Deploy project to cloud hosting platforms

## Author

Developed by: diutuananh
