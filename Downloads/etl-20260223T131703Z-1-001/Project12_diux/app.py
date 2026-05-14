from flask import Flask, render_template, request, redirect, jsonify
import mysql.connector

app = Flask(__name__)

def get_db_connection():
    return mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="123456",
        database="office_management",
        port=3306
    )

# ======================
# DASHBOARD (FIX IN USE)
# ======================
@app.route('/')
def dashboard():
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
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    cursor.execute("""
        SELECT e.*, d.DepartmentName
        FROM Equipment e
        JOIN Departments d ON e.DepartmentID = d.DepartmentID
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

    cursor.execute("SELECT DISTINCT Type FROM Equipment")
    types = [row['Type'] for row in cursor.fetchall()]

    cursor.execute("SELECT DISTINCT Unit FROM Equipment")
    units = [row['Unit'] for row in cursor.fetchall()]

    db.close()

    return render_template(
        'add_equipment.html',
        departments=departments,
        types=types,
        units=units
    )

# ======================
# DELETE EQUIPMENT
# ======================
@app.route('/delete_equipment/<int:id>')
def delete_equipment(id):
    db = get_db_connection()
    cursor = db.cursor()

    cursor.execute("DELETE FROM Equipment WHERE EquipmentID=%s", (id,))
    db.commit()

    db.close()
    return redirect('/equipment')

# ======================
# EDIT EQUIPMENT (NEW)
# ======================
@app.route('/edit_equipment/<int:id>', methods=['GET', 'POST'])
def edit_equipment(id):
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    if request.method == 'POST':
        cursor.execute("""
            UPDATE Equipment
            SET EquipmentName=%s,
                Type=%s,
                Unit=%s,
                Status=%s,
                DepartmentID=%s
            WHERE EquipmentID=%s
        """, (
            request.form['name'],
            request.form['type'],
            request.form['unit'],
            request.form['status'],
            request.form['department'],
            id
        ))

        db.commit()
        db.close()
        return redirect('/equipment')

    cursor.execute("SELECT * FROM Equipment WHERE EquipmentID=%s", (id,))
    equipment = cursor.fetchone()

    cursor.execute("SELECT * FROM Departments")
    departments = cursor.fetchall()

    db.close()

    return render_template(
        'edit_equipment.html',
        equipment=equipment,
        departments=departments
    )

# ======================
# UPDATE EQUIPMENT AJAX (Sửa lỗi thiếu route cho nút Save)
# ======================
@app.route('/update_equipment/<int:id>', methods=['POST'])
def update_equipment(id):
    data = request.get_json()
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("""
        UPDATE Equipment 
        SET EquipmentName=%s, Type=%s, Unit=%s, Status=%s 
        WHERE EquipmentID=%s
    """, (data['name'], data['type'], data['unit'], data['status'], id))
    db.commit()
    db.close()
    return jsonify({"success": True})

# ======================
# AUTOCOMPLETE TYPE API
# ======================
@app.route('/api/types')
def get_types():
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    cursor.execute("SELECT DISTINCT Type FROM Equipment")
    data = [row['Type'] for row in cursor.fetchall()]

    db.close()
    return jsonify(data)

# ======================
# AUTOCOMPLETE UNIT API
# ======================
@app.route('/api/units')
def get_units():
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    cursor.execute("SELECT DISTINCT Unit FROM Equipment")
    data = [row['Unit'] for row in cursor.fetchall()]

    db.close()
    return jsonify(data)

# ======================
# MAINTENANCE
# ======================
@app.route('/maintenance')
def maintenance():
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    cursor.execute("SELECT * FROM Maintenance")
    data = cursor.fetchall()

    db.close()
    return render_template('maintenance.html', maintenances=data)

# ======================
# PURCHASES
# ======================
@app.route('/purchases')
def purchases():
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    cursor.execute("SELECT * FROM Purchases")
    data = cursor.fetchall()

    db.close()
    return render_template('purchases.html', purchases=data)

# ======================
if __name__ == '__main__':
    app.run(debug=True)