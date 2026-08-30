# Lung Disease Prediction and Consultation Portal (LungCnn)

LungCnn is an integrated medical software portal containing a **Flask-based web application** (serving both the backend API and the Jinja2 HTML frontend UI) and an offline **Tkinter-based desktop interface**. It classifies chest X-ray scans into specific lung conditions using a deep learning model, and simulates a patient-to-doctor consultation workflow (booking appointments and managing prescriptions).

---

## Purpose
This project is built for educational and research simulation purposes. It demonstrates:
1. The integration of a trained TensorFlow/Keras convolutional neural network (CNN) within web and desktop applications.
2. A complete multi-role consultation workflow involving Patients, Doctors, and Administrators.
3. Deploying the Flask web application on Render Web Services with Aiven MySQL and parameterized database queries.

---

## Features

* **AI Image Classification:** Classifies chest X-ray scans into distinct disease states using a convolutional neural network.
* **Role-Based Workflows:** Separate dashboard flows for Patients, Doctors, and Administrators.
* **Specialist Search & Directory:** Patients can filter and search for medical specialists based on area of expertise.
* **Consultation Booking:** Patients can choose a specialist and book appointments.
* **Digital Prescription Desk:** Doctors can review appointments, prescribe medicines, add guidelines, and upload consultation reports.
* **Verification Test Suite:** Includes automated test runners to validate server configuration, database connections, and model predictions locally before deployment.
* **Containerized Build Support:** Complete configurations for production servers and Docker container builds.

---

## User Roles and Capabilities

### 🌐 Patient
* **Register & Login:** Create a profile and log in.
* **Upload Scan & Predict:** Upload a chest X-ray image to get an AI prediction.
* **Find a Specialist:** Search the registered specialist directory.
* **Book Appointments:** Book a consultation through the specialist directory.
* **View Prescription Desk:** Check appointments and download PDF/image reports assigned by the doctor.

### 🩺 Doctor
* **Register & Login:** Register under a medical specialization and log in.
* **Review Consultations:** View scheduled appointments booked by patients.
* **Prescribe Treatments:** Fill out prescriptions (medicine names, custom notes, follow-up dates) and upload report attachments.
* **Treatment Registry:** Browse a history of all previously prescribed treatments.

### 🔑 Administrator
* **Administrator Login:** Access administrator tools using credentials configured through environment variables.
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
* **Backend & UI Framework:** Flask 2.2.3 (integrated Jinja2 template frontend)
* **Production Web Server:** Waitress 2.1.2
* **ML Libraries:** TensorFlow/Keras 2.11.0, NumPy 1.21.5
* **Image Processing:** OpenCV (`opencv-python` 3.4.2.16), Pillow 9.0.1
* **Database Driver:** `mysql-connector-python` 8.0.33
* **Frontend Assets:** Jinja2 templates, Bootstrap CSS, jQuery

---

## Production Deployment Architecture

```
┌──────────────┐       HTTPS Requests      ┌──────────────────────┐
│  Web Client  │◄─────────────────────────►│  Render Web Service  │
└──────────────┘                           │(Waitress/Flask/Jinja)│
                                           └──────────┬───────────┘
                                                      │
                                                      │  get_db_connection()
                                                      ▼  (TLS/SSL Encrypted)
┌──────────────┐                           ┌──────────────────────┐
│  Keras Model │◄──────────────────────────┤     Aiven MySQL      │
│(lungmodel.h5)│                           │     (Production)     │
└──────────────┘                           └──────────────────────┘
```
* **Render Web Service:** Serves both the backend API and the frontend UI directly (same-origin, no separate frontend static hosting required).
* **Aiven MySQL:** A completely separate managed production database, connected securely over TLS/SSL.
* **Database Parameterization:** All database query inputs are fully parameterized using placeholders (`%s`) to prevent SQL injection vulnerabilities.
* **Secure Admin Access:** Verified dynamically via private environment variables `ADMIN_USERNAME` and `ADMIN_PASSWORD` (no default fallbacks or plaintext files committed).

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
├── init_db.py                # Database schema initialization helper
├── Main.py                   # Tkinter-based desktop interface
├── model.py                  # Model architecture and training script
├── predict.py                # Isolated model prediction tester
├── requirements.txt          # Verified dependency manifest
├── schema.sql                # Sanitized database structural schema
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
│   └── upload/                  # Created at runtime for temporary uploads
└── templates/                # Jinja2 HTML templates
    ├── menu/                 # Navigation menus
    └── *.html
```

---

## Environment Variables
Configure the following environment variables in the Render Service dashboard:
* `DB_HOST`: Host name of the Aiven MySQL database server.
* `DB_PORT`: Database connection port.
* `DB_USER`: Non-root username for database connection.
* `DB_PASSWORD`: Password for database connection.
* `DB_NAME`: Database name. For the deployed Aiven database, use exactly `lungcnn`.
* `SECRET_KEY`: Security signature for Flask sessions.
* `ADMIN_USERNAME`: Administrator username.
* `ADMIN_PASSWORD`: Administrator password.
* `DB_SSL_CA_CONTENT`: (Optional) The raw text content of Aiven's root CA certificate (which is written to a secure temporary file at runtime to authenticate database TLS connections).

---

## Local Setup & Development

### Local Prerequisites
* Python 3.7
* MySQL Server (version 8.0 recommended) or Docker Desktop (for Compose mockup)

### Installation
1. **Clone the Repository:**
   ```bash
   git clone https://github.com/vivyn66/LungCnn.git
   cd LungCnn
   ```
2. **Configure Environment:**
   * Copy `.env.example` to `.env`.
   * Open `.env` and fill out your local database settings, secret keys, and admin credentials.
3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

### Running Locally (Development Mode)
```bash
python App.py
```
> [!WARNING]
> **Development Server Warning:** Flask's built-in development server and debug mode are strictly for local testing and debugging. They must not be used in a production environment.

### Running Offline Desktop GUI
```bash
python Main.py
```

### Mocking Production Locally (Docker Compose)
We include a `docker-compose.yml` file to test a production-like multi-container setup locally:
```bash
docker-compose up --build -d
```
*App is mapped to `http://127.0.0.1:5000` on the local machine.*

---

## Production Deployment Sequence (Render + Aiven)

### Step 1: Initialize Database on Aiven
1. Create a MySQL database instance on Aiven.
2. Locally configure your `.env` variables to target the remote Aiven database.
3. Run the sanitized database initialization script to create tables securely:
   ```bash
   python init_db.py
   ```

### Step 2: Configure Render Web Service
1. Create a new **Web Service** on Render, linking your GitHub repository.
2. Select **Docker** as the runtime environment.
3. Under **Advanced Settings**, add the environment variables defined in the Environment Variables section. Note that for `DB_SSL_CA_CONTENT`, you should copy-paste the complete text content of Aiven's root CA certificate (`ca.pem`).
4. Choose a plan appropriate for your use case and deploy.

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

## Prototype Security Notes
This project is an educational prototype and should not be treated as a production medical system.

* User and doctor passwords are currently stored and compared as plain text. Before any real-world deployment, replace this with password hashing (for example, Werkzeug's password-hashing utilities) and migrate existing records safely.
* The application currently uses temporary local storage for uploaded files; see the upload limitations below.

---

## Upload Storage Limitations on Render Free Tier
* **Ephemeral Disk:** Because Render's Free Web Service tier filesystem is ephemeral, uploaded scans and prescription reports stored in `static/upload/` will be deleted whenever the container restarts or re-deploys.
* **Security Interceptor:** To prevent unauthorized direct browsing of uploads, the application implements a Flask request interceptor blocking access to `/static/upload/*` (returning `403 Forbidden`). All file downloads must pass through the authorized `/download?id=<id>` endpoint.
* **Showcase Mitigation:** This upload workflow operates within the container's temporary disk space for portfolio demonstration purposes. In a true production system, the upload destination should be mapped to an external S3-compatible object storage provider (e.g. AWS S3 or Supabase Storage).

---

## Medical and Research Disclaimer
> [!WARNING]
> **Educational and Research Use Only:** This application is developed as an educational prototype. It has not been clinically validated, is not a certified medical diagnostic tool, and should not be used as a substitute for professional clinical medical evaluation, diagnosis, or treatment. Predictions generated by the CNN model are image classifications and not confirmed clinical diagnoses.
