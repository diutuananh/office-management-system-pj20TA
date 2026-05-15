# Office Management System

This is an Office Management System built using Flask, MySQL, HTML, CSS, and JavaScript. The system is designed to manage office equipment, departments, maintenance records, and purchase history with integrated user authentication and analytical reporting.

## Features

- User Authentication: Secure login and session management for system access.
- Dashboard: Real-time display of total equipment statistics and status charts.
- Equipment Management: Full CRUD (Add, Edit/Update, and Delete) functionality.
- Inline Editing: AJAX-based (Fetch API) updates for equipment details without page reloads.
- Assignment Tracking: Manage equipment distribution among employees and departments.
- Reports Module: Analytical views for equipment distribution and current usage status.
- Maintenance Tracking: Records for equipment repair history and service logs.
- Purchase History: Tracking of procurement dates, costs, and quantities.
- Data Visualization: Integrated charts using Chart.js for inventory insights.

## Technologies Used

- Backend: Flask (Python)
- Database: MySQL (Relational Schema & SQL Views)
- Frontend: HTML, CSS, JavaScript (ES6+)
- Libraries: mysql-connector-python, Chart.js, Jinja2

## Project Structure

```
Project12_diux/
│
├── app.py                  # Core application logic and API routes
├── office_management.sql   # Database schema, Views, and initialization data
│
├── templates/              # Jinja2 templates
│   ├── login.html          # User authentication portal
│   ├── dashboard.html      # Stats overview
│   ├── equipment.html      # Asset management list
│   ├── add_equipment.html  # New asset registration
│   ├── edit_equipment.html # Record modification
│   ├── maintenance.html    # Maintenance records
│   ├── purchases.html      # Purchase records
│   └── reports.html        # Analytical reports and usage status
│
├── static/
│   └── style.css           # Global system styling
│
└── README.md
```

## Database Setup

### Step 1: Create Database

Run the following SQL commands in MySQL:

```sql
CREATE DATABASE office_management;
USE office_management;
```

### Step 2: Import Database

Import the provided SQL file:

```bash
office_management.sql
```

Or execute it using MySQL Workbench.

## Installation and Running the Project

### Step 1: Clone the repository

```bash
git clone https://github.com/diutuananh/office-management-system-pj20TA.git
cd office-management-system-pj20TA
```

### Step 2: Install dependencies

```bash
pip install flask mysql-connector-python
```

### Step 3: Configure database connection

Open `app.py` and update:

```python
host = "127.0.0.1"
user = "root"
password = "123456"
database = "office_management"
port = 3306
```

### Step 4: Run the application

```bash
python app.py
```

### Step 5: Open browser

```
http://127.0.0.1:5000
```
## System Credentials

- Username: admin
- Password: 123456

## System Pages

- Login: Secure portal for system entry.
- Dashboard: Displays overall statistics and status charts.
- Equipment: List of equipment with inline edit and assignment details.
- Reports: Detailed reports on equipment by department and assignment status.
- Maintenance: Logs for repair and service history.
- Purchases: Historical purchase records.

## API Endpoints

- GET /api/types: Autocomplete for equipment types
- GET /api/units: Autocomplete for measurement units
- POST /update_equipment/<id>: Update equipment details via AJAX (JSON/Form data).

## Notes

- SQL Optimization: Uses SQL Views (View_Equipment_By_Dept, View_Current_Usage) for reporting.
- Session Management: Secure route protection using Flask-Session.
- Ensure MySQL server is running before starting the application.
- Database credentials must match your local MySQL configuration.

## Future Improvements

- Improve UI using Bootstrap or Tailwind CSS.
- Add pagination and advanced filtering features.
- Export reports to PDF or Excel formats.
- Deploy project to cloud hosting platforms.
