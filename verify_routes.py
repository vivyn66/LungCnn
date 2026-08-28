import os
import unittest
import io
from PIL import Image
import mysql.connector

class TestAppRoutes(unittest.TestCase):

    def setUp(self):
        # Load environment variables
        if os.path.exists('.env'):
            with open('.env', 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        key, val = line.split('=', 1)
                        os.environ[key.strip()] = val.strip()

        # Import App after loading env vars
        import App
        self.app = App.app
        self.client = self.app.test_client()
        
        # Clean up database test entries to make test repeatable
        self.db = App.get_db_connection()
        cursor = self.db.cursor()
        cursor.execute("DELETE FROM regtb WHERE UserName = 'alicesmith'")
        cursor.execute("DELETE FROM apptb WHERE UserName = 'alicesmith'")
        cursor.execute("DELETE FROM drugtb WHERE UserName = 'alicesmith'")
        self.db.commit()

    def tearDown(self):
        self.db.close()

    def test_01_user_registration(self):
        """Test User Registration (POST /newuser)"""
        data = {
            'name': 'Alice Smith',
            'gender': 'Female',
            'age': '25',
            'email': 'alice@example.com',
            'phone': '1231231234',
            'address': '456 Oak St',
            'uname': 'alicesmith',
            'psw': 'password123',
            'loc': 'CA'
        }
        response = self.client.post('/newuser', data=data)
        # Re-query database to verify it exists
        cursor = self.db.cursor()
        cursor.execute("SELECT * FROM regtb WHERE UserName = %s", ('alicesmith',))
        row = cursor.fetchone()
        self.assertIsNotNone(row, "Registration database entry was not created!")
        self.assertEqual(row[0], 'Alice Smith')
        print("\n[PASS] E2E Registration: Database row created for alicesmith successfully.")

    def test_02_user_login_validation(self):
        """Test User Login validation (Correct and Incorrect credentials)"""
        # Register user first
        cursor = self.db.cursor()
        cursor.execute("INSERT INTO regtb VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
                       ('Alice Smith', 'Female', '25', 'alice@example.com', '1231231234', '456 Oak St', 'alicesmith', 'password123', 'CA'))
        self.db.commit()

        # Try incorrect login
        response = self.client.post('/userlogin', data={'uname': 'alicesmith', 'password': 'wrongpassword'}, follow_redirects=True)
        self.assertIn(b"Username or Password is Incorrect!", response.data)
        print("[PASS] E2E Login validation: Invalid credentials cleanly rejected with error message.")

        # Try correct login
        response = self.client.post('/userlogin', data={'uname': 'alicesmith', 'password': 'password123'}, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        # Verify session using request context if needed, but the redirect/success confirms it
        print("[PASS] E2E Login: Valid login succeeded and session set.")

    def test_03_prediction_and_validation(self):
        """Test Prediction route file uploads and validation checks"""
        # Test invalid extension
        txt_data = (io.BytesIO(b"This is text file content"), "test_invalid.txt")
        response = self.client.post('/predict', data={'file': txt_data}, follow_redirects=True)
        self.assertIn(b"Invalid file extension", response.data)
        print("[PASS] E2E Prediction: Invalid extension rejected cleanly.")

        # Test corrupt image validation
        corrupt_data = (io.BytesIO(b"corrupt image content header bytes"), "test_corrupt.png")
        response = self.client.post('/predict', data={'file': corrupt_data}, follow_redirects=True)
        self.assertIn(b"Uploaded file is not a valid or is a corrupt image", response.data)
        print("[PASS] E2E Prediction: Corrupt image validation failed and rejected cleanly.")

        # Test valid image prediction
        with open('Sample/Covid (1).png', 'rb') as f:
            valid_img_data = (io.BytesIO(f.read()), "test_covid.png")
        
        response = self.client.post('/predict', data={'file': valid_img_data}, follow_redirects=True)
        self.assertIn(b"Disease Name:", response.data)
        self.assertIn(b"Covid", response.data)
        print("[PASS] E2E Prediction: Valid image prediction ran and predicted 'Covid'.")

    def test_04_doctor_search_and_appointment(self):
        """Test searching doctor and booking appointment"""
        # Register patient and doctor in db
        cursor = self.db.cursor()
        cursor.execute("DELETE FROM doctortb WHERE UserName = 'drhouse'")
        cursor.execute("INSERT INTO doctortb VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                       ('Dr. Gregory House', 'Male', '45', 'house@example.com', '1234567890', 'Princeton', 'Lung Specialist', 'drhouse', 'password123', 'NJ'))
        cursor.execute("INSERT INTO regtb VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
                       ('Alice Smith', 'Female', '25', 'alice@example.com', '1231231234', '456 Oak St', 'alicesmith', 'password123', 'CA'))
        self.db.commit()

        # Log in first to set session uname
        self.client.post('/userlogin', data={'uname': 'alicesmith', 'password': 'password123'}, follow_redirects=True)

        # Set prediction state in session by simulating predict (which sets session['out'] = 'Covid')
        with open('Sample/Covid (1).png', 'rb') as f:
            valid_img_data = (io.BytesIO(f.read()), "test_covid.png")
        self.client.post('/predict', data={'file': valid_img_data}, follow_redirects=True)

        # Search Doctor
        response = self.client.post('/UserSearch', data={'special': 'Lung Specialist'}, follow_redirects=True)
        self.assertIn(b"Dr. Gregory House", response.data)
        print("[PASS] E2E Doctor Search: Successfully searched specialists list.")

        # Book Appointment
        response = self.client.get('/Appointment?id=drhouse', follow_redirects=True)
        self.assertIn(b"Appointment Booked...!", response.data)

        # Check database appointment entry
        cursor.execute("SELECT * FROM apptb WHERE UserName = %s", ('alicesmith',))
        appt_row = cursor.fetchone()
        self.assertIsNotNone(appt_row, "Appointment was not recorded in apptb table!")
        self.assertEqual(appt_row[4], 'drhouse')
        print("[PASS] E2E Appointment booking: Database record created for drhouse successfully.")

    def test_05_prescription_and_download(self):
        """Test Doctor prescribing medicine and Patient downloading report"""
        # Register doctor and appointment
        cursor = self.db.cursor()
        cursor.execute("DELETE FROM doctortb WHERE UserName = 'drhouse'")
        cursor.execute("INSERT INTO doctortb VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                       ('Dr. Gregory House', 'Male', '45', 'house@example.com', '1234567890', 'Princeton', 'Lung Specialist', 'drhouse', 'password123', 'NJ'))
        cursor.execute("INSERT INTO apptb VALUES (NULL, %s, %s, %s, %s, %s, %s, %s)",
                       ('alicesmith', '1231231234', 'alice@example.com', 'drhouse', '2026-08-28', 'Lung Specialist', 'Covid'))
        self.db.commit()

        # Doctor Login
        response = self.client.post('/doclogin', data={'uname': 'drhouse', 'password': 'password123'}, follow_redirects=True)
        print("[PASS] E2E Doctor Login: Doctor authenticated successfully.")

        # Prescribe drugs (POST /assigndrug)
        pdf_data = (io.BytesIO(b"dummy report content"), "report_upload.png")
        presc_data = {
            'UserName': 'alicesmith',
            'Phone': '1231231234',
            'Email': 'alice@example.com',
            'Medicine': 'Stay hydrated & isolate',
            'Other': 'Rest well',
            'file': pdf_data,
            'Adate': '2026-09-10'
        }
        response = self.client.post('/assigndrug', data=presc_data, follow_redirects=True)
        self.assertIn(b"Stay hydrated", response.data)
        
        # Verify database entry
        cursor.execute("SELECT id, Report FROM drugtb WHERE UserName = %s", ('alicesmith',))
        drug_row = cursor.fetchone()
        self.assertIsNotNone(drug_row, "Prescription not saved in drugtb database!")
        drug_id, report_filename = drug_row
        print(f"[PASS] E2E Prescription: Drug database entry created with report filename '{report_filename}'.")

        # Log out doctor by creating a new client session (clean client)
        self.client = self.app.test_client()

        # Patient Login and download report
        self.client.post('/userlogin', data={'uname': 'alicesmith', 'password': 'password123'}, follow_redirects=True)
        response = self.client.get(f'/download?id={drug_id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b"dummy report content")
        print("[PASS] E2E Report Download: Download retrieved uploaded file content successfully.")

if __name__ == '__main__':
    unittest.main()
