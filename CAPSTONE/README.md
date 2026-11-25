# Smart Parking Reservation and Slot Availability Management System

A production-grade, full-stack web application designed for intelligent parking space discovery, interval-based conflict-free reservations, real-time availability tracking, and parking operations analytics.

---

## 1. Project Overview

The **Smart Parking Reservation and Slot Availability Management System** solves urban parking congestion and eliminates reservation disputes. Drivers can inspect real-time bay occupancy, view interactive multi-level parking layouts, search available slots by vehicle category, and book guaranteed parking spaces in advance with conflict protection. Administrators gain real-time visibility over capacity, facility layouts, maintenance states, and revenue trends driven by real dataset analytics.

### Core Modules
* **Module 1: Parking Slot Availability Management**
  * Real-time slot status computation (Available, Reserved, Occupied, Maintenance).
  * Interactive visual parking grid grouped by floor levels and zones.
  * Multi-parameter search & dynamic interval filtering.
  * Administrator maintenance blocking and capacity controls.
* **Module 2: Smart Parking Reservation & Booking Management**
  * Concurrency-guarded reservations backed by database transactions.
  * Unique booking reference generation (`PRK-YYYYMMDD-XXXXXX`).
  * Digital printable receipt with QR verification links.
  * User self-service booking cancellation with instantaneous slot availability restoration.
  * Attendant check-in and check-out workflows.

---

## 2. Technology Stack

* **Frontend**: HTML5, CSS3, JavaScript (ES6+), Bootstrap 5.3, Bootstrap Icons, Chart.js 4.4.
* **Backend**: Python 3.10+ (tested on Python 3.13.5), Flask 3.1, Werkzeug, Jinja2, Flask-Login.
* **Real-Time Communication**: Firebase Realtime Database with Firebase JavaScript SDK (v9 compat) and background synchronization (`static/js/realtime_sync.js`).
* **Database & Cloud Services**:
  * **Primary Shared Cloud Database**: Firebase Realtime Database (`firebase-admin 7.7.0` for Python).
  * **Resilient Local Database & Fallback**: SQLite 3 with strict foreign key constraints (`PRAGMA foreign_keys = ON;`) and transactional locking.
* **Data Processing & Analytics**: Pandas, NumPy, Python standard library.
* **Production Deployment**: WSGI compatible (`wsgi.py`, Gunicorn / Waitress, `Procfile`).

---

## 3. Dataset Architecture & Integration

The system natively integrates a three-tier relational dataset located in `data/`:

| Dataset File | Records | Key Columns | Purpose |
| :--- | :--- | :--- | :--- |
| **`data/parking_facilities.csv`** | 4 facilities | `lot_id`, `lot_name`, `location`, `city`, `total_floors`, `total_capacity`, `base_hourly_rate`, `operating_hours`, `contact_phone`, `latitude`, `longitude` | Facility master definitions across commercial hubs. |
| **`data/parking_slots.csv`** | 90 slots | `slot_id`, `lot_id`, `floor_level`, `zone`, `slot_number`, `slot_type`, `hourly_rate`, `operational_status`, `is_accessible` | Slot master data (51 Car, 27 Bike, 12 EV Charging; 87 Active, 3 Maintenance). |
| **`data/historical_occupancy.csv`** | 250 records | `record_id`, `lot_id`, `slot_id`, `vehicle_number`, `vehicle_type`, `entry_time`, `exit_time`, `duration_hours`, `hourly_rate`, `total_amount`, `payment_status`, `day_of_week` | Historical parking transactions used for peak hour analytics and revenue charts. |

---

## 4. Conflict-Free Availability Logic

To guarantee that no two drivers reserve the same bay for overlapping times, the system enforces end-exclusive interval overlap checking:

$$\text{Conflict} \iff (\text{Existing Start} < \text{Requested End}) \land (\text{Existing End} > \text{Requested Start})$$

### Interval Examples:
* **Booking A:** 10:00 AM to 12:00 PM
* **Booking B:** 11:00 AM to 01:00 PM $\rightarrow$ **CONFLICT** (Rejected on the server).
* **Booking C:** 12:00 PM to 02:00 PM $\rightarrow$ **NO CONFLICT** (Allowed because end times are exclusive).
* **Cancelled Bookings:** Released immediately; cancelled records do not block slots.

---

## 5. Getting Started & Installation

### Step 1: System Requirements
* Python **3.10** or higher.
* Operating System: Windows, macOS, or Linux.

### Step 2: Set Up Virtual Environment (Recommended)

#### On Windows (PowerShell):
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

#### On Linux / macOS:
```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Required Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Initialize Database & Ingest Datasets
Execute the automated database initialization and data ingestion script:
```bash
python scripts/import_dataset.py
```
This command:
1. Creates the SQLite schema in `instance/parking.db`.
2. Seeds default Administrator, Attendant, and Driver accounts.
3. Ingests all 4 parking facilities, 90 parking bays, and 250 historical occupancy logs.
4. Validates schema and skips any duplicate records safely.

---

## 6. Pre-Configured Test Accounts

| Role | Email | Password | Permissions |
| :--- | :--- | :--- | :--- |
| **Administrator** | `admin@smartparking.com` | `Admin@12345` | Full admin dashboard, facility CRUD, slot management, maintenance toggles, dataset uploads. |
| **Attendant** | `attendant@smartparking.com` | `Attendant@123` | Gate QR verification, check-in, and check-out management. |
| **Driver / User** | `driver@example.com` | `Driver@12345` | Slot discovery, reservation booking, my bookings, receipt printing, cancellation. |

*Note: New drivers can also register directly via the **Register** page (`/register`). Public registration strictly assigns the `user` (Driver) role.*

---

## 7. Running the Web Application

Start the Flask local development server:
```bash
python app.py
```

Open your browser and navigate to:
```
http://127.0.0.1:5000
```

---

## 8. Application Routes & Site Map

### Public & Driver Routes
* **Home Page**: `GET /` &mdash; Welcome hero, system capacity summary, featured facilities.
* **Live Dashboard**: `GET /dashboard` &mdash; Interval-based availability metrics and facility cards.
* **Search & Filter Slots**: `GET /search` &mdash; Filter by facility, city, slot category (Car, Bike, EV), date, and time.
* **Interactive Slot Grid**: `GET /slots/<lot_id>` &mdash; Color-coded visual bay layout by floor and zone.
* **Slot Layout API**: `GET /api/slots/<lot_id>` &mdash; JSON endpoint for asynchronous time-window slot querying.
* **Reserve Slot**: `GET, POST /book/<slot_id>` &mdash; Reservation form with real-time fee and duration calculation.
* **Booking Confirmation**: `GET /booking/confirm/<booking_id>` &mdash; Printable confirmation and QR code.
* **My Bookings**: `GET /my-bookings` &mdash; Filter bookings by Upcoming, Completed, or Cancelled.
* **Booking Details**: `GET /booking/<booking_ref>` &mdash; Detailed reservation summary.
* **Cancel Booking**: `POST /booking/cancel/<booking_id>` &mdash; User cancellation releasing slot.
* **Verify Booking**: `GET /booking/verify/<booking_ref>` &mdash; QR verification endpoint for gate attendants.
* **User Login & Register**: `GET, POST /login`, `GET, POST /register`, `GET /logout`.

### Administrator Console
* **Admin Dashboard**: `GET /admin/dashboard` &mdash; Capacity metrics, Chart.js peak hours, weekly distribution, and vehicle share.
* **Facility Management**: `GET, POST /admin/lots` &mdash; Add, edit, or delete parking facilities.
* **Slot Management**: `GET, POST /admin/slots` &mdash; Add slots, edit rates, toggle maintenance states.
* **Reservation Registry**: `GET, POST /admin/bookings` &mdash; Search all reservations, check-in, check-out, cancel.
* **Dataset Management**: `GET, POST /admin/dataset` &mdash; Inspect dataset schemas, re-sync defaults, and upload custom CSV/XLSX/JSON files.
* **Real-Time Live Status API**: `GET /api/live-status` &mdash; Live JSON metrics and Firebase sync state.
* **Real-Time Slot Layout API**: `GET /api/live-slots/<lot_id>` &mdash; Live slot states for instantaneous DOM synchronization.

---

## 9. Real-Time Multi-User Synchronization & Firebase Setup

The application features a real-time synchronization engine (`static/js/realtime_sync.js`) that allows multiple simultaneous users to view live parking slot states and occupancy metrics without manual browser refreshes:

1. **Dual-Mode Architecture**:
   * **Live Firebase Mode**: When configured with your Firebase credentials, changes are broadcast instantaneously through Firebase Realtime Database Web SDK listeners (`child_changed`, `value`).
   * **Resilient Fallback Mode**: When running without Firebase credentials, the system automatically uses background sync (`/api/live-slots/<lot_id>`) to synchronize DOM slot cards, colors, badges, and dashboard metrics across all open tabs.
2. **Setup Instructions**:
   * Refer to [`FIREBASE_SETUP.md`](file:///c:/Users/shaik/OneDrive/Desktop/Smart%20Parking%20System/FIREBASE_SETUP.md) for step-by-step instructions on creating a Firebase project, downloading credentials, and configuring your `.env` file.
   * Deploy the authored security rules from [`database.rules.json`](file:///c:/Users/shaik/OneDrive/Desktop/Smart%20Parking%20System/database.rules.json).
   * Push master dataset records to Firebase using:
     ```bash
     python scripts/import_firebase.py
     ```

---

## 10. Running Automated Tests

A comprehensive automated test suite (**28 unit and integration tests across 6 modules**) is provided in `tests/`:

```bash
python -m unittest discover -s tests -p "test_*.py" -v
```

### Verified Test Suites:
1. **`test_dataset.py` (3 tests)**: Dataset ingestion, column validation, duplicate rejection, and analytics aggregation.
2. **`test_auth.py` (4 tests)**: Password hashing, role enforcement, duplicate email rejection, and case-insensitivity.
3. **`test_availability.py` (5 tests)**: Overlapping interval detection, back-to-back non-overlapping bookings, maintenance slot exclusion, and availability queries.
4. **`test_bookings.py` (7 tests)**: Transactional booking creation, double-booking rejection, maintenance slot booking prevention, cancellation availability restoration, and ownership verification.
5. **`test_e2e_workflow.py` (4 tests)**: End-to-end integration covering registration, login, slot search, booking, conflict rejection, cancellation, re-booking, and admin authorization.
6. **`test_firebase_integration.py` (5 tests)**: Firebase service status reporting, live status endpoint, live slots endpoint, atomic booking transactions, and reservation cancellation restoration.

---

## 11. Production Deployment

For production deployments, execute with a production WSGI server via `wsgi.py`:

```bash
# Using Gunicorn (Linux/Container)
gunicorn --bind 0.0.0.0:5000 wsgi:app

# Or run directly on Windows / Development
python app.py
```

---

## 12. Dataset Notes & Limitations

* **Historical Data vs Live Sensors**: The application derives historical occupancy patterns and peak-hour analytics from `data/historical_occupancy.csv`. Physical occupancy during live reservations is driven by confirmed check-ins (`Checked-In` status) rather than unverified simulated sensors.
* **Time Zone Handling**: Timestamps are stored and processed in local system time in standardized ISO string format (`YYYY-MM-DD HH:MM:SS`).
