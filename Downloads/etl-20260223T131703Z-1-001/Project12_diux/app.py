from flask import Flask, render_template, request, redirect
import mysql.connector

app = Flask(__name__)

# ======================
# DB CONNECTION
# ======================
def get_db_connection():
    return mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="123456",
        database="office_management",
        port=3306
    )

# ======================
# DASHBOARD
# ======================
@app.route('/')
def dashboard():
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    cursor.execute("SELECT COUNT(*) AS total FROM Equipment")
    total = cursor.fetchone()['total']

    cursor.execute("""
        SELECT COUNT(*) AS available
        FROM Equipment
        WHERE Status = 'Available'
    """)
    available = cursor.fetchone()['available']

    cursor.execute("""
        SELECT COUNT(*) AS maintenance
        FROM Equipment
        WHERE Status = 'Maintenance'
    """)
    maintenance = cursor.fetchone()['maintenance']

    db.close()

    return render_template(
        'dashboard.html',
        total=total,
        available=available,
        maintenance=maintenance
    )

# ======================
# EQUIPMENT
# ======================
@app.route('/equipment')
def equipment():
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            Equipment.EquipmentID,
            Equipment.EquipmentName,
            Equipment.Type,
            Equipment.Unit,
            Equipment.Status,
            Departments.DepartmentName
        FROM Equipment
        JOIN Departments
        ON Equipment.DepartmentID = Departments.DepartmentID
    """)

    equipments = cursor.fetchall()
    db.close()

    return render_template('equipment.html', equipments=equipments)

# ======================
# ADD EQUIPMENT
# ======================
@app.route('/add_equipment', methods=['GET', 'POST'])
def add_equipment():
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    if request.method == 'POST':

        cursor.execute("""
            INSERT INTO Equipment
            (EquipmentName, Type, Unit, Status, DepartmentID)
            VALUES (%s, %s, %s, %s, %s)
        """, (
            request.form['name'],
            request.form['type'],
            request.form['unit'],
            request.form['status'],
            request.form['department']
        ))

        db.commit()
        db.close()
        return redirect('/equipment')

    cursor.execute("SELECT * FROM Departments")
    departments = cursor.fetchall()

    db.close()

    return render_template('add_equipment.html', departments=departments)

# ======================
# MAINTENANCE
# ======================
@app.route('/maintenance')
def maintenance():
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    cursor.execute("""
        SELECT *
        FROM Maintenance
    """)

    maintenances = cursor.fetchall()
    db.close()

    return render_template('maintenance.html', maintenances=maintenances)

# ======================
# PURCHASES
# ======================
@app.route('/purchases')
def purchases():
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    cursor.execute("""
        SELECT *
        FROM Purchases
    """)

    purchases = cursor.fetchall()
    db.close()

    return render_template('purchases.html', purchases=purchases)

# ======================
# RUN APP
# ======================
if __name__ == '__main__':
    app.run(debug=True)