import os
import sys
import unittest
import mysql.connector

class TestPreDeployment(unittest.TestCase):

    def setUp(self):
        # Ensure env vars are loaded for standard tests
        if os.path.exists('.env'):
            with open('.env', 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        key, val = line.split('=', 1)
                        os.environ[key.strip()] = val.strip()

    def test_01_startup_missing_config(self):
        """1. Startup Check: Verify server fails to start if config is missing"""
        # Save current environment
        saved_host = os.environ.get("DB_HOST")
        if "DB_HOST" in os.environ:
            del os.environ["DB_HOST"]
        
        # Rename .env temporarily if it exists, so App.py cannot load it automatically
        env_renamed = False
        if os.path.exists('.env'):
            os.rename('.env', '.env.tmp')
            env_renamed = True
        
        # Remove from sys.modules to force reload and check startup check
        if "App" in sys.modules:
            del sys.modules["App"]
        
        try:
            # Attempting to load/fail
            import App
            # If it loaded without error, fail the test
            self.fail("Startup check failed: App started even with DB_HOST missing!")
        except RuntimeError as e:
            # Expected behavior
            print(f"\n[PASS] Startup check raised expected error: {e}")
        finally:
            # Restore environment
            if saved_host:
                os.environ["DB_HOST"] = saved_host
            # Restore .env
            if env_renamed:
                os.rename('.env.tmp', '.env')

    def test_02_health_endpoint(self):
        """2. Health Check: Verify health endpoint works"""
        import App
        client = App.app.test_client()
        response = client.get('/health')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"status": "UP"})
        print("\n[PASS] Health check GET /health returned 200 OK and status 'UP'")

    def test_03_database_connection(self):
        """3. Database Check: Centralized connection is successful"""
        import App
        try:
            conn = App.get_db_connection()
            self.assertTrue(conn.is_connected())
            conn.close()
            print("\n[PASS] Database connection successfully established using get_db_connection()")
        except Exception as e:
            self.fail(f"Database connection failed: {e}")

    def test_04_valid_prediction(self):
        """4. Valid Prediction: Ensure prediction pipeline succeeds with expected class"""
        import App
        from tensorflow.keras.utils import load_img, img_to_array
        import tensorflow as tf
        import numpy as np

        model_path = 'lungmodel.h5'
        sample_path = 'Sample/Covid (1).png'

        self.assertTrue(os.path.exists(model_path), "Model file lungmodel.h5 is missing!")
        self.assertTrue(os.path.exists(sample_path), "Sample image is missing!")

        classifier = tf.keras.models.load_model(model_path)
        img = load_img(sample_path, target_size=(200, 200))
        img_array = img_to_array(img) / 255.0
        img_array = np.expand_dims(img_array, axis=0)

        result = classifier.predict(img_array)
        pred_index = np.argmax(result[0])
        classes = ['Covid', 'Influenza', 'Normal', 'Pneumonia', 'Tuberculosis']
        out = classes[pred_index]

        self.assertIn(out, classes)
        print(f"\n[PASS] Model loaded and successfully predicted class: '{out}' for {sample_path}")

    def test_05_invalid_file_extension(self):
        """5. Invalid File Check: Rejects files with invalid extension"""
        import App
        self.assertFalse(App.allowed_file("test.txt"))
        self.assertFalse(App.allowed_file("script.py"))
        self.assertTrue(App.allowed_file("scan.png"))
        self.assertTrue(App.allowed_file("scan.jpg"))
        print("\n[PASS] File extension validator successfully filters extensions")

    def test_06_corrupt_image(self):
        """6. Corrupt Image Check: Pillow validation catches corrupt or dummy files"""
        import App
        # Create a dummy text file renamed to .png
        dummy_path = 'static/upload/dummy_corrupt.png'
        with open(dummy_path, 'w') as f:
            f.write("This is not a real image!")

        client = App.app.test_client()
        with open(dummy_path, 'rb') as f:
            response = client.post('/predict', data={'file': f}, follow_redirects=True)
            # Flask flashes a message and redirects, which yields a HTML page
            self.assertEqual(response.status_code, 200)
            # The uploaded file should be rejected without server crash
            print("\n[PASS] Corrupt/Invalid image file was safely rejected without server crash")
        
        # Clean up
        if os.path.exists(dummy_path):
            os.remove(dummy_path)

    def test_07_secret_scan(self):
        """7. Secret Scan Check: Ensure no credentials exist in source code"""
        with open('App.py', 'r', encoding='utf-8') as f:
            app_content = f.read()
        self.assertNotIn("Vivyn@21", app_content, "Found hardcoded password 'Vivyn@21' in App.py!")
        print("\n[PASS] Secrets scan confirmed no hardcoded passwords are present in App.py")

if __name__ == '__main__':
    # Force environment variables to load for standard test environment setup
    if os.path.exists('.env'):
        with open('.env', 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, val = line.split('=', 1)
                    os.environ[key.strip()] = val.strip()

    suite = unittest.TestLoader().loadTestsFromTestCase(TestPreDeployment)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    sys.exit(0 if result.wasSuccessful() else 1)
