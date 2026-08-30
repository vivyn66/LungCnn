from flask import Flask, render_template, flash, request, session, send_file
from flask import render_template, redirect, url_for, request
from werkzeug.utils import secure_filename
import mysql.connector
import sys

import pickle

import os

# Custom .env loader to support local development
if os.path.exists('.env'):
    with open('.env', 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, val = line.split('=', 1)
                os.environ[key.strip()] = val.strip()

def get_env_or_fail(var_name):
    val = os.environ.get(var_name)
    if not val:
        raise RuntimeError(f"Startup failure: Required environment variable '{var_name}' is missing.")
    return val

DB_HOST = get_env_or_fail("DB_HOST")
DB_PORT = int(os.environ.get("DB_PORT", "3306"))
DB_USER = get_env_or_fail("DB_USER")
DB_PASSWORD = get_env_or_fail("DB_PASSWORD")
DB_NAME = get_env_or_fail("DB_NAME")
SECRET_KEY = get_env_or_fail("SECRET_KEY")



ADMIN_USERNAME = get_env_or_fail("ADMIN_USERNAME")



ADMIN_PASSWORD = get_env_or_fail("ADMIN_PASSWORD")

DB_SSL_CA_CONTENT = os.environ.get("DB_SSL_CA_CONTENT")
DB_SSL_CA_PATH = None
if DB_SSL_CA_CONTENT:
    import tempfile
    try:
        temp_ca = tempfile.NamedTemporaryFile(delete=False, suffix=".pem", mode='w', encoding='utf-8')
        temp_ca.write(DB_SSL_CA_CONTENT)
        temp_ca.close()
        DB_SSL_CA_PATH = temp_ca.name
    except Exception as e:
        raise RuntimeError(f"Startup failure: Failed to write DB_SSL_CA_CONTENT to temporary file: {e}")


app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024 # 5MB limit

# Use an absolute runtime path so uploads work on Render/Linux.
UPLOAD_DIR = os.path.join(app.root_path, 'static', 'upload')
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.before_request
def restrict_uploads():
    # Block direct HTTP requests to static/upload/ files
    if request.path.startswith('/static/upload/'):
        return "Access Forbidden", 403


ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_db_connection():
    try:
        conn_kwargs = {
            'user': DB_USER,
            'password': DB_PASSWORD,
            'host': DB_HOST,
            'port': DB_PORT,
            'database': DB_NAME
        }
        if DB_SSL_CA_PATH:
            conn_kwargs['ssl_ca'] = DB_SSL_CA_PATH
            conn_kwargs['ssl_verify_cert'] = True
        return mysql.connector.connect(**conn_kwargs)
    except mysql.connector.Error as err:
        app.logger.error(f"Database connection error: {err}")
        raise RuntimeError("Database connection failed.")


@app.route("/")
def homepage():
    return render_template('index.html')


@app.route("/Home")
def Home():
    return render_template('index.html')


@app.route("/DoctorLogin")
def DoctorLogin():
    return render_template('DoctorLogin.html')


@app.route("/NewDoctor")
def NewDoctor():
    return render_template('NewDoctor.html')


@app.route("/AdminLogin")
def AdminLogin():
    return render_template('AdminLogin.html')


@app.route("/UserLogin")
def UserLogin():
    return render_template('UserLogin.html')


@app.route("/NewUser")
def NewUser():
    return render_template('NewUser.html')


@app.route("/Cancer")
def Cancer():
    return render_template('Cancer.html')


@app.route("/Diabetes")
def Diabetes():
    return render_template('Diabetes.html')


@app.route("/Heart")
def Heart():
    return render_template('Heart.html')


@app.route("/adminlogin", methods=['GET', 'POST'])
def adminlogin():
    error = None
    if request.method == 'POST':
        if request.form['uname'] == ADMIN_USERNAME and request.form['password'] == ADMIN_PASSWORD:

            conn = get_db_connection()
            # cursor = conn.cursor()
            cur = conn.cursor()
            cur.execute("SELECT * FROM regtb ")
            data = cur.fetchall()
            flash('You are Logged In...!')
            return render_template('AdminHome.html', data=data)

        else:

            flash('Username or Password is wrong')
            return render_template('AdminLogin.html')


@app.route("/AdminHome")
def AdminHome():
    conn = get_db_connection()
    # cursor = conn.cursor()
    cur = conn.cursor()
    cur.execute("SELECT * FROM regtb ")
    data = cur.fetchall()

    return render_template('AdminHome.html', data=data)


@app.route("/AdminUserInfo")
def AdminUserInfo():
    conn = get_db_connection()
    # cursor = conn.cursor()
    cur = conn.cursor()
    cur.execute("SELECT * FROM doctortb ")
    data = cur.fetchall()

    return render_template('AdminUserInfo.html', data=data)


@app.route("/AdminAssignInfo")
def AdminAssignInfo():
    conn = get_db_connection()
    # cursor = conn.cursor()
    cur = conn.cursor()
    cur.execute("SELECT * FROM drugtb ")
    data = cur.fetchall()

    return render_template('AdminAssignInfo.html', data=data)


@app.route("/DoctorUserInfo")
def DoctorUserInfo():
    dname = session['dname']

    conn = get_db_connection()
    # cursor = conn.cursor()
    cur = conn.cursor()
    cur.execute("SELECT * FROM apptb where DoctorName = %s", (dname,))
    data = cur.fetchall()

    return render_template('DoctorUserInfo.html', data=data)


@app.route("/DoctorAssignInfo")
def DoctorAssignInfo():
    dname = session['dname']

    conn = get_db_connection()
    # cursor = conn.cursor()
    cur = conn.cursor()
    cur.execute("SELECT * FROM drugtb where DoctorName = %s", (dname,))
    data = cur.fetchall()

    return render_template('DoctorAssignInfo.html', data=data)


@app.route("/doclogin", methods=['GET', 'POST'])
def doclogin():
    if request.method == 'POST':
        username = request.form['uname']
        password = request.form['password']
        session['dname'] = request.form['uname']

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * from doctortb where username = %s and Password = %s", (username, password))
        data = cursor.fetchone()
        if data is None:


            flash('Username or Password is wrong')
            return render_template('DoctorLogin.html')


        else:
            print(data[0])
            session['uid'] = data[0]
            conn = get_db_connection()
            # cursor = conn.cursor()
            cur = conn.cursor()
            cur.execute("SELECT * FROM doctortb where username = %s and Password = %s", (username, password))
            data = cur.fetchall()
            flash('You are Logged In...!')
            return render_template('DoctorHome.html', data=data)


@app.route("/DoctorHome")
def DoctorHome():
    uname = session['dname']
    conn = get_db_connection()
    # cursor = conn.cursor()
    cur = conn.cursor()
    cur.execute("SELECT * FROM doctortb where username = %s", (uname,))
    data = cur.fetchall()

    return render_template('DoctorHome.html', data=data)


@app.route("/UserHome")
def UserHome():
    uname = session['uname']
    conn = get_db_connection()
    # cursor = conn.cursor()
    cur = conn.cursor()
    cur.execute("SELECT * FROM regtb where username = %s", (uname,))
    data = cur.fetchall()

    return render_template('UserHome.html', data=data)



@app.route("/searchid")
def searchid():
    user = request.args.get('user')
    session['user'] = user
    print(user)
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM apptb where id = %s", (user,))
    data = cur.fetchall()
    #print(data)

    return render_template('AdminAssign.html', data=data)


@app.route("/assigndrug", methods=['GET', 'POST'])
def assigndrug():
    if request.method == 'POST':
        uname = request.form['UserName']
        phone = request.form['Phone']
        email = request.form['Email']
        dname = session['dname']
        medi = request.form['Medicine']
        other = request.form['Other']
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_DIR, filename))
        else:
            flash('Invalid report file type. Only JPG, JPEG, and PNG are allowed.')
            return redirect(url_for('ViewDoctor'))
        Adate = request.form['Adate']

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO drugtb VALUES (NULL, %s, %s, %s, %s, %s, %s, %s, %s)", (uname, phone, email, dname, medi, other, file.filename, Adate))
        conn.commit()
        conn.close()

        # return 'file register successfully'
        conn = get_db_connection()
        # cursor = conn.cursor()
        cur = conn.cursor()
        cur.execute("SELECT * FROM drugtb where DoctorName = %s", (dname,))
        data = cur.fetchall()

    return render_template('DoctorAssignInfo.html', data=data)


@app.route("/newuser", methods=['GET', 'POST'])
def newuser():
    if request.method == 'POST':
        name1 = request.form['name']
        gender1 = request.form['gender']
        Age = request.form['age']
        email = request.form['email']
        pnumber = request.form['phone']
        address = request.form['address']

        uname = request.form['uname']
        password = request.form['psw']
        loc = request.form['loc']

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO regtb VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)", (name1, gender1, Age, email, pnumber, address, uname, password, loc))
        conn.commit()
        conn.close()
        # return 'file register successfully'
    flash("Record Saved...!")
    return render_template('UserLogin.html')


@app.route("/newdoctor", methods=['GET', 'POST'])
def newcoor():
    if request.method == 'POST':
        name1 = request.form['name']
        gender1 = request.form['gender']
        Age = request.form['age']
        email = request.form['email']
        pnumber = request.form['phone']
        address = request.form['address']
        special = request.form['special']
        loc = request.form['loc']

        uname = request.form['uname']
        password = request.form['psw']

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO doctortb VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (name1, gender1, Age, email, pnumber, address, special, uname, password, loc))
        conn.commit()
        conn.close()

    flash('Record Saved...!')
    return render_template('NewDoctor.html')


@app.route("/userlogin", methods=['GET', 'POST'])
def userlogin():
    error = None
    if request.method == 'POST':
        username = request.form['uname']
        password = request.form['password']
        session['uname'] = request.form['uname']

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * from regtb where username = %s and Password = %s", (username, password))
        data = cursor.fetchone()
        if data is None:

            flash('Username or Password is Incorrect!')
            return render_template('UserLogin.html')



        else:
            print(data[0])
            session['uid'] = data[0]
            session['loca'] = data[8]

            conn = get_db_connection()
            # cursor = conn.cursor()
            cur = conn.cursor()
            cur.execute("SELECT * FROM regtb where username = %s and Password = %s", (username, password))
            data = cur.fetchall()
            flash('You are Logged In...!')
            return render_template('UserHome.html', data=data)


@app.route("/ViewDoctor")
def ViewDoctor():
    return render_template('UserAppointment.html')


@app.route("/predict", methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(url_for('ViewDoctor'))
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(url_for('ViewDoctor'))
        if not allowed_file(file.filename):
            flash('Invalid file extension. Only JPG, JPEG, and PNG are allowed.')
            return redirect(url_for('ViewDoctor'))

        # Verify image integrity with Pillow
        from PIL import Image
        try:
            img_check = Image.open(file)
            img_check.verify()
            file.seek(0)
        except Exception:
            flash('Uploaded file is not a valid or is a corrupt image.')
            return redirect(url_for('ViewDoctor'))

        # Save file securely
        upload_path = os.path.join(UPLOAD_DIR, 'Test.jpg')
        file.save(upload_path)

        import warnings
        warnings.filterwarnings('ignore')
        import tensorflow as tf
        import numpy as np
        from tensorflow.keras.utils import load_img, img_to_array

        try:
            # Load model
            classifierLoad = tf.keras.models.load_model('lungmodel.h5')

            # Load and preprocess the image
            img = load_img(upload_path, target_size=(200, 200))
            img_array = img_to_array(img) / 255.0
            img_array = np.expand_dims(img_array, axis=0)  # shape: (1, 200, 200, 3)

            # Predict
            result = classifierLoad.predict(img_array)
            pred_index = np.argmax(result[0])
            classes = ['Covid', 'Influenza', 'Normal', 'Pneumonia', 'Tuberculosis']
            out = classes[pred_index]

            print("Predicted:", out)
        except Exception as e:
            app.logger.error(f"Inference error: {e}", exc_info=True)
            flash('An error occurred during image processing. Please try again.')
            return redirect(url_for('ViewDoctor'))

        # If Normal, go directly
        if out == "Normal":
            return render_template('UserAppointment.html', pre=out)
        else:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute("SELECT * FROM doctortb")
            data = cur.fetchall()
            session['out'] = out
            return render_template('UserAppointment.html', pre=out, data=data)


@app.route("/UserSearch", methods=['GET', 'POST'])
def UserSearch():
    if request.method == 'POST':
        special = request.form['special']
        conn = get_db_connection()
        # cursor = conn.cursor()
        cur = conn.cursor()
        cur.execute("SELECT * FROM doctortb where Specialist = %s", (special,))
        data = cur.fetchall()

        return render_template('UserAppointment.html', data=data)


@app.route("/UserAppointment")
def UserAppointment():
    uname = session['uname']

    conn = get_db_connection()
    # cursor = conn.cursor()
    cur = conn.cursor()
    cur.execute("SELECT * FROM apptb where UserName = %s", (uname,))
    data = cur.fetchall()

    return render_template('UserAppointmentinfo.html', data=data)


@app.route("/UserAssignDrugInfo")
def UserAssignDrugInfo():
    uname = session['uname']
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM drugtb where UserName = %s", (uname,))
    data = cur.fetchall()

    return render_template('UserAssignDrugInfo.html', data=data)


@app.route("/Appointment")
def Appointment():
    dusername = request.args.get('id')
    import datetime
    date = datetime.datetime.now().strftime('%Y-%m-%d')
    uname = session['uname']
    dise = session['out']

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM doctortb where UserName = %s", (dusername,))
    data = cursor.fetchone()

    if data:
        spec = data[6]



    else:

        return 'Incorrect username / password !'

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM regtb where UserName = %s", (uname,))
    data = cursor.fetchone()

    if data:
        mobile = data[4]
        email = data[3]


    else:

        return 'Incorrect username / password !'

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO apptb VALUES (NULL, %s, %s, %s, %s, %s, %s, %s)", (uname, mobile, email, dusername, date, spec, dise))
    conn.commit()
    conn.close()


    uname = session['uname']
    conn = get_db_connection()
    # cursor = conn.cursor()
    cur = conn.cursor()
    cur.execute("SELECT * FROM regtb where username = %s", (uname,))
    data = cur.fetchall()
    flash('Appointment Booked...!')
    return render_template('UserHome.html', data=data)


@app.route('/download')
def download():
    id = request.args.get('id')

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM drugtb where id = %s", (id,))
    data = cursor.fetchone()
    if data:
        filename = os.path.join(UPLOAD_DIR, data[7])

        return send_file(filename, as_attachment=True)

    else:
        return 'Incorrect username / password !'


@app.route("/search", methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        date = request.form['date']

        conn = get_db_connection()
        # cursor = conn.cursor()
        cur = conn.cursor()
        cur.execute("SELECT * FROM assigntb where Lastdate = %s", (date,))
        data = cur.fetchall()

        return render_template('Notification.html', data=data)


@app.route("/health", methods=['GET'])

def health():
    required_tables = ('admintb', 'apptb', 'doctortb', 'drugtb', 'regtb')
    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT DATABASE()")
        database_name = cur.fetchone()[0]

        placeholders = ','.join(['%s'] * len(required_tables))
        params = (database_name,) + required_tables
        cur.execute(
            "SELECT TABLE_NAME FROM information_schema.TABLES "
            "WHERE TABLE_SCHEMA = %s AND TABLE_NAME IN (" + placeholders + ")",
            params
        )
        found_tables = {row[0] for row in cur.fetchall()}
        missing_tables = [table for table in required_tables if table not in found_tables]

        if missing_tables:
            return {
                "status": "DOWN",
                "database": "MISSING_TABLES",
                "database_name": database_name,
                "missing_tables": missing_tables
            }, 503

        return {
            "status": "UP",
            "database": "UP",
            "database_name": database_name,
            "required_tables": list(required_tables)
        }
    except Exception:
        app.logger.exception("Database health check failed")
        return {"status": "DOWN", "database": "UNAVAILABLE"}, 503
    finally:
        if conn is not None:
            conn.close()

@app.errorhandler(413)
def request_entity_too_large(error):
    flash('File is too large. Maximum allowed size is 5MB.')
    return redirect(request.referrer or url_for('homepage'))

@app.errorhandler(Exception)
def handle_exception(e):
    app.logger.error(f"Unhandled exception: {e}", exc_info=True)
    flash("A system error occurred. Please try again later.")
    return redirect(url_for('homepage'))

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
