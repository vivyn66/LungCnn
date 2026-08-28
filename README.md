# Lung Disease Prediction and Consultation Portal (LungCnn)

LungCnn is an integrated medical software portal containing a **Flask-based web application** and a **Tkinter-based desktop interface**. It categorizes chest X-ray scans into specific lung conditions using a deep learning model, and simulates a patient-to-doctor consultation workflow (booking appointments and managing prescriptions).

---

## Purpose
This project is built for educational and research simulation purposes. It demonstrates:
1. The integration of a trained TensorFlow/Keras convolutional neural network (CNN) within web and desktop applications.
2. A complete multi-role consultation workflow involving Patients, Doctors, and Administrators.
3. Production-ready web serving, database query parameterization for security, and containerization.

---

## Features

* **AI Image Classification:** Classifies chest X-ray scans into distinct disease states using a convolutional neural network.
* **Role-Based Workflows:** Distinct and secure dashboard systems for Patients, Doctors, and Administrators.
* **Specialist Search & Directory:** Patients can filter and search for medical specialists based on area of expertise.
* **Consultation Booking:** Patients can choose a specialist and book appointments.
* **Digital Prescription Desk:** Doctors can review appointments, prescribe medicines, add guidelines, and upload consultation reports.
* **Verification Test Suite:** Includes automated test runners to validate server configuration, database connections, and model predictions locally before deployment.
* **Containerized Build Support:** Complete configurations for production servers and Docker container builds.

---

## User Roles and Capabilities

### 🌐 Patient
* **Register & Login:** Create a profile and log in securely.
* **Upload Scan & Predict:** Upload a chest X-ray image to get an AI prediction.
* **Find a Specialist:** Search the registered specialist directory.
* **Book Appointments:** Securely book a consultation slot.
* **View Prescription Desk:** Check appointments and download PDF/image reports assigned by the doctor.

### 🩺 Doctor
* **Register & Login:** Sign up under a medical specialization and log in.
* **Review Consultations:** View scheduled appointments booked by patients.
* **Prescribe Treatments:** Fill out prescriptions (medicine names, custom notes, follow-up dates) and upload report attachments.
* **Treatment Registry:** Browse a history of all previously prescribed treatments.

### 🔑 Administrator
* **Secure Login:** Access via database-checked admin credentials.
* **Directory Controls:** View and audit registries of registered patients, doctors, and active prescriptions.

---

## Machine Learning Model Details
* **Model File:** [lungmodel.h5](lungmodel.h5) (backed by [lungmodel.json](lungmodel.json)).
* **Framework:** TensorFlow / Keras (version 2.11.0).
* **Input Image Requirements:** Target size `200 x 200` pixels with 3 color channels (RGB).
* **Preprocessing:** Rescales pixel values by normalisation (`/ 255.0`) and expands dimensions to batch size shape `(1, 200, 200, 3)`.
* **Prediction Categories:**
  * `Covid`
  * `Influenza`
  * `Normal`
  * `Pneumonia`
  * `Tuberculosis`
* **Inference Pipeline:** Performed on the local server via Flask `/predict` or locally in the offline Tkinter GUI.

---

## Technology Stack
* **Python Version:** 3.7.5
* **Backend Framework:** Flask 2.2.3
* **Production Server:** Waitress 2.1.2
* **ML Libraries:** TensorFlow/Keras 2.11.0, NumPy 1.21.5
* **Image Processing:** OpenCV (`opencv-python` 3.4.2.16), Pillow 9.0.1
* **Database Driver:** `mysql-connector-python` 8.0.33
* **Frontend:** Jinja2 templates, Bootstrap CSS, jQuery

---

## Application Architecture
```
┌──────────────┐      HTTP Requests      ┌──────────────┐
│  Web Client  │◄───────────────────────►│  Flask App   │
└──────────────┘                         └──────┬───────┘
                                                │
                                                ▼  get_db_connection()
┌──────────────┐      Model Inference    ┌──────────────┐
│  Keras Model │◄────────────────────────┤  MySQL DB    │
│(lungmodel.h5)│                         │(1lungdoctordb)│
└──────────────┘                         └──────────────┘
```
* **Database Parameterization:** Database query inputs are fully parameterized using placeholders (`%s`) to prevent SQL injection vulnerabilities.
* **Connection Management:** Connection handling is centralized inside `get_db_connection()` to avoid duplicate connection blocks.

---

## Project Structure
```
LungCnn/
├── .dockerignore
├── .env.example
├── .gitignore
├── App.py                    # Main Flask web application
├── Convertor.py              # Script to convert Keras model to TensorFlowJS
├── Dockerfile                # Production Docker configuration
├── Main.py                   # Tkinter-based desktop interface
├── model.py                  # Model architecture and training script
├── predict.py                # Isolated model prediction tester
├── requirements.txt          # Verified dependency manifest
├── verify_deployment.py      # Local pre-deployment sanity checks
├── verify_routes.py          # E2E integration route test suite
├── wsgi.py                   # Waitress production server entrypoint
├── model/                    # TensorFlowJS model output directory
├── Sample/
│   └── Covid (1).png         # Sample image for prediction verification
├── static/
│   ├── css/                  # Compiled styles
│   ├── images/               # Interface banners and graphics
│   ├── js/                   # Theme and Bootstrap scripts
│   └── upload/
│       └── .gitkeep          # Upload folder placeholder
└── templates/                # Jinja2 HTML templates
    ├── menu/                 # Navigation menus
    └── *.html
```

---

## Environment Variables
The application requires the following environment variables to be configured in a local `.env` file (see `.env.example`):
* `DB_HOST`: Host address of the MySQL database server.
* `DB_PORT`: MySQL connection port.
* `DB_USER`: Username for database connection.
* `DB_PASSWORD`: Password for database connection.
* `DB_NAME`: Schema name (`1lungdoctordb`).
* `SECRET_KEY`: Security signature for Flask sessions.
* `CORS_ALLOWED_ORIGINS`: Allowed origins (for CORS filtering).

---

## Local Setup

### Prerequisites
* Python 3.7
* MySQL Server (version 8.0 recommended)

### Installation
1. **Clone the Repository:**
   ```bash
   git clone https://github.com/vivyn66/LungCnn.git
   cd LungCnn
   ```
2. **Setup the Database:**
   * Create a database named `1lungdoctordb` in your MySQL Server.
   * Initialize the schema (including `regtb`, `doctortb`, `apptb`, and `drugtb` tables) on your local MySQL server.
3. **Configure Environment:**
   * Copy `.env.example` to `.env`.
   * Open `.env` and fill out your database settings and secret key.
4. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

---

## How to Run

### Development Mode (Flask Dev Server)
```bash
python App.py
```
> [!WARNING]
> **Development Server Warning:** Flask's built-in development server and debug mode are strictly for local testing and debugging. They must not be used in a production environment.

### Production Mode (Waitress WSGI Server)
```bash
python wsgi.py
```
Serves the application via the production-ready Waitress server.

### Desktop App (Tkinter Offline GUI)
```bash
python Main.py
```
Launches the offline desktop window to perform training or predictions.

---

## Docker/Deployment Configuration
The project is containerized for deployment using the included [Dockerfile](Dockerfile):
* **Base Image:** Runs on Python 3.7 slim.
* **System Libraries:** Automatically installs graphical libraries required by OpenCV and Pillow.
* **wsgi.py Command:** Configured to serve the application on port 5000 via Waitress.

---

## Verification and Testing
Two automated test suites are included to verify functionality:

### 1. Local Pre-Deployment Checks
Run [verify_deployment.py](verify_deployment.py) to check local deployment requirements:
* Validates startup crashes if required configs are missing.
* Checks health-check endpoint GET `/health`.
* Tests direct database connection.
* Evaluates Keras model loading and correct classification prediction.
* Tests extension validation and catches corrupt images.
* Performs a scan to ensure no plaintext secrets exist in code.

### 2. End-to-End Integration Tests
Run [verify_routes.py](verify_routes.py) to simulate a complete patient and doctor workflow:
```bash
python verify_routes.py
```
This tests registration, login errors, prediction, doctor specialist search, appointment booking, prescription writing, and secure report download.

---

## Limitations
* **Binary Image Processing:** Preprocessing operates on 3-channel RGB colors but does not segment or annotate bounding regions on the X-ray.
* **File-Based Upload Cleanup:** Uploaded reports are stored in local directories and require separate scheduled jobs for volume purging.

---

## Future Enhancements
* Migrate backend session storage from local files to a secure production-grade session store (e.g., redis-backed or database-backed sessions).
* Integrate visual diagnostic overlays (e.g., Grad-CAM heatmaps) to highlight classified chest anomalies.
* Sync the Tkinter desktop app database actions with the central MySQL application.

---

## Medical and Research Disclaimer
> [!WARNING]
> **Educational and Research Use Only:** This application is developed as an educational prototype. It has not been clinically validated, is not a certified medical diagnostic tool, and should not be used as a substitute for professional clinical medical evaluation, diagnosis, or treatment.
