from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
from config import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME

app = Flask(__name__)

# Database connection
def get_db_connection():
    conn = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )
    return conn

# Home Page
@app.route('/')
def index():
    return render_template('index.html')

# Patients Page
@app.route('/patients', methods=['GET', 'POST'])
def patients():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        gender = request.form['gender']
        contact = request.form['contact']
        medical_history = request.form['medical_history']
        cursor.execute(
            "INSERT INTO patients (name, age, gender, contact, medical_history) VALUES (%s,%s,%s,%s,%s)",
            (name, age, gender, contact, medical_history)
        )
        conn.commit()
        return redirect(url_for('patients'))
    
    cursor.execute("SELECT * FROM patients")
    patients = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('patients.html', patients=patients)

# Doctors Page
@app.route('/doctors', methods=['GET', 'POST'])
def doctors():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    if request.method == 'POST':
        name = request.form['name']
        specialization = request.form['specialization']
        contact = request.form['contact']
        cursor.execute(
            "INSERT INTO doctors (name, specialization, contact) VALUES (%s,%s,%s)",
            (name, specialization, contact)
        )
        conn.commit()
        return redirect(url_for('doctors'))
    
    cursor.execute("SELECT * FROM doctors")
    doctors = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('doctors.html', doctors=doctors)

# Appointments Page
@app.route('/appointments', methods=['GET', 'POST'])
def appointments():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute("SELECT * FROM patients")
    patients = cursor.fetchall()
    
    cursor.execute("SELECT * FROM doctors")
    doctors = cursor.fetchall()
    
    if request.method == 'POST':
        patient_id = request.form['patient_id']
        doctor_id = request.form['doctor_id']
        appointment_date = request.form['appointment_date']
        appointment_time = request.form['appointment_time']
        cursor.execute(
            "INSERT INTO appointments (patient_id, doctor_id, appointment_date, appointment_time) VALUES (%s,%s,%s,%s)",
            (patient_id, doctor_id, appointment_date, appointment_time)
        )
        conn.commit()
        return redirect(url_for('appointments'))
    
    cursor.execute("""
        SELECT a.appointment_id, p.name AS patient_name, d.name AS doctor_name, appointment_date, appointment_time
        FROM appointments a
        JOIN patients p ON a.patient_id = p.patient_id
        JOIN doctors d ON a.doctor_id = d.doctor_id
    """)
    appointments = cursor.fetchall()
    
    cursor.close()
    conn.close()
    return render_template('appointments.html', appointments=appointments, patients=patients, doctors=doctors)

# Billing Page
@app.route('/billing', methods=['GET', 'POST'])
def billing():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute("SELECT * FROM patients")
    patients = cursor.fetchall()
    
    if request.method == 'POST':
        patient_id = request.form['patient_id']
        amount = request.form['amount']
        status = request.form['status']
        cursor.execute(
            "INSERT INTO billing (patient_id, amount, status) VALUES (%s,%s,%s)",
            (patient_id, amount, status)
        )
        conn.commit()
        return redirect(url_for('billing'))
    
    cursor.execute("""
        SELECT b.bill_id, p.name AS patient_name, amount, status
        FROM billing b
        JOIN patients p ON b.patient_id = p.patient_id
    """)
    bills = cursor.fetchall()
    
    cursor.close()
    conn.close()
    return render_template('billing.html', bills=bills, patients=patients)

if __name__ == "__main__":
    app.run(debug=True)
