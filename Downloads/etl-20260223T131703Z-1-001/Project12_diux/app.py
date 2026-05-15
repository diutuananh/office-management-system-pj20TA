from flask import Flask, render_template, request, redirect, jsonify, session
import mysql.connector

app = Flask(__name__)
app.secret_key = 'office_secret_key'

def get_db_connection():
    return mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="123456",
        database="office_management",
        port=3306
    )

# ======================
# LOGIN SYSTEM
# ======================
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        db = get_db_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Users WHERE Username=%s AND Password=%s", (username, password))
        user = cursor.fetchone()
        db.close()

        if user:
            session['user'] = user['Username']
            session['role'] = user['Role']
            return redirect('/')
        return "Invalid credentials"
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

# ======================
# DASHBOARD
# ======================
@app.route('/')
def dashboard():
    if 'user' not in session:
        return redirect('/login')
        
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    cursor.execute("SELECT COUNT(*) AS total FROM Equipment")
    total = cursor.fetchone()['total']

    cursor.execute("SELECT COUNT(*) AS available FROM Equipment WHERE Status='Available'")
    available = cursor.fetchone()['available']

    cursor.execute("SELECT COUNT(*) AS maintenance FROM Equipment WHERE Status='Maintenance'")
    maintenance = cursor.fetchone()['maintenance']

    cursor.execute("SELECT COUNT(*) AS in_use FROM Equipment WHERE Status='In Use'")
    in_use = cursor.fetchone()['in_use']

    db.close()

    return render_template(
        'dashboard.html',
        total=total,
        available=available,
        maintenance=maintenance,
        in_use=in_use
    )

# ======================
# EQUIPMENT LIST
# ======================
@app.route('/equipment')
def equipment():
    if 'user' not in session: return redirect('/login')
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    cursor.execute("""
        SELECT e.*, d.DepartmentName, emp.EmployeeName
        FROM Equipment e
        JOIN Departments d ON e.DepartmentID = d.DepartmentID
        LEFT JOIN Employees emp ON e.EmployeeID = emp.EmployeeID
        ORDER BY e.EquipmentID ASC
    """)

    equipments = cursor.fetchall()
    db.close()

    return render_template('equipment.html', equipments=equipments)

# ======================
# ADD EQUIPMENT
# ======================
@app.route('/add_equipment', methods=['GET', 'POST'])
def add_equipment():
    if 'user' not in session: return redirect('/login')
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    if request.method == 'POST':
        emp_id = request.form.get('employee')
        emp_id = emp_id if emp_id and emp_id != "" else None

        cursor.execute("""
            INSERT INTO Equipment
            (EquipmentName, Type, Unit, Status, DepartmentID, EmployeeID)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            request.form['name'],
            request.form['type'],
            request.form['unit'],
            request.form['status'],
            request.form['department'],
            emp_id
        ))

        db.commit()
        db.close()
        return redirect('/equipment')

    cursor.execute("SELECT * FROM Departments")
    departments = cursor.fetchall()

    cursor.execute("SELECT * FROM Employees")
    employees = cursor.fetchall()

    cursor.execute("SELECT DISTINCT Type FROM Equipment")
    types = [row['Type'] for row in cursor.fetchall()]

    cursor.execute("SELECT DISTINCT Unit FROM Equipment")
    units = [row['Unit'] for row in cursor.fetchall()]

    db.close()

    return render_template(
        'add_equipment.html',
        departments=departments,
        employees=employees,
        types=types,
        units=units
    )

# ======================
# DELETE EQUIPMENT
# ======================
@app.route('/delete_equipment/<int:id>')
def delete_equipment(id):
    if 'user' not in session: return redirect('/login')
    db = get_db_connection()
    cursor = db.cursor()

    cursor.execute("DELETE FROM Equipment WHERE EquipmentID=%s", (id,))
    db.commit()

    db.close()
    return redirect('/equipment')

# ======================
# EDIT / UPDATE EQUIPMENT
# ======================
@app.route('/update_equipment/<int:id>', methods=['POST'])
def update_equipment(id):
    if 'user' not in session: return jsonify({"success": False}), 403
    
    db = get_db_connection()
    cursor = db.cursor()
    
    if request.is_json:
        data = request.get_json()
        cursor.execute("""
            UPDATE Equipment
            SET EquipmentName=%s, Type=%s, Unit=%s, Status=%s
            WHERE EquipmentID=%s
        """, (data['name'], data['type'], data['unit'], data['status'], id))
    else:
        emp_id = request.form.get('employee')
        emp_id = emp_id if emp_id and emp_id != "" else None
        cursor.execute("""
            UPDATE Equipment
            SET EquipmentName=%s, Type=%s, Unit=%s, Status=%s, DepartmentID=%s, EmployeeID=%s
            WHERE EquipmentID=%s
        """, (
            request.form['name'], request.form['type'], request.form['unit'],
            request.form['status'], request.form['department'], emp_id, id
        ))

    db.commit()
    db.close()
    
    if request.is_json:
        return jsonify({"success": True})
    return redirect('/equipment')

# ======================
# REPORTS
# ======================
@app.route('/reports')
def reports():
    if 'user' not in session: return redirect('/login')
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    cursor.execute("SELECT * FROM View_Equipment_By_Dept")
    dept_report = cursor.fetchall()

    cursor.execute("SELECT * FROM View_Current_Usage")
    usage_report = cursor.fetchall()

    db.close()
    return render_template('reports.html', dept_report=dept_report, usage_report=usage_report)

# ======================
# MAINTENANCE
# ======================
@app.route('/maintenance')
def maintenance():
    if 'user' not in session: return redirect('/login')
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    cursor.execute("""
        SELECT m.*, e.EquipmentName 
        FROM Maintenance m 
        JOIN Equipment e ON m.EquipmentID = e.EquipmentID
    """)
    data = cursor.fetchall()

    db.close()
    return render_template('maintenance.html', maintenances=data)

# ======================
# PURCHASES
# ======================
@app.route('/purchases')
def purchases():
    if 'user' not in session: return redirect('/login')
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    cursor.execute("""
        SELECT p.*, e.EquipmentName 
        FROM Purchases p 
        JOIN Equipment e ON p.EquipmentID = e.EquipmentID
    """)
    data = cursor.fetchall()

    db.close()
    return render_template('purchases.html', purchases=data)

if __name__ == '__main__':
    app.run(debug=True)