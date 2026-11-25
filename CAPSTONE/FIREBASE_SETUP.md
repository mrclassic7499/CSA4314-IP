# Firebase Realtime Database Integration & Configuration Guide

This guide provides step-by-step instructions for connecting the **Smart Parking Reservation and Slot Availability Management System** to a genuine **Firebase Realtime Database** project for cloud-synchronized, multi-user real-time parking operations.

---

## 1. Prerequisites
* A Google account.
* Access to the [Firebase Console](https://console.firebase.google.com).
* Python 3.10+ installed locally with dependencies from `requirements.txt`.

---

## 2. Step-by-Step Firebase Project Setup

### Step 2.1: Create a Firebase Project
1. Open the [Firebase Console](https://console.firebase.google.com).
2. Click **Add project** (or **Create a project**).
3. Name your project (e.g., `smart-parking-system-2026`).
4. Disable Google Analytics (optional, not required) and click **Create project**.
5. Wait for Firebase to finish provisioning, then click **Continue**.

### Step 2.2: Enable Firebase Realtime Database
1. In the left navigation menu of the Firebase Console, navigate to **Build** &rarr; **Realtime Database**.
2. Click **Create Database**.
3. Choose a database location:
   * Recommended for India / Asia: `Singapore (asia-southeast1)` or `United States (us-central1)`.
4. In the **Security rules** step:
   * Select **Start in locked mode** (security rules will be deployed in Step 2.5).
   * Click **Enable**.
5. Once created, note the **Database URL** displayed at the top of the Data tab:
   * Example: `https://smart-parking-system-default-rtdb.asia-southeast1.firebasedatabase.app/`
   * Or: `https://smart-parking-system-default-rtdb.firebaseio.com/`

### Step 2.3: Generate Server-Side Service Account Credentials (Admin SDK)
1. In the Firebase Console, click the **Gear icon (⚙️)** next to *Project Overview* and select **Project settings**.
2. Click the **Service accounts** tab.
3. Ensure **Python** is selected under the *Admin SDK configuration snippet*.
4. Click **Generate new private key**, then click **Generate key** in the confirmation modal.
5. A JSON file will download to your computer.
6. Rename or move this file into your project workspace:
   ```
   Smart Parking System/
   └── credentials/
       └── firebase-service-account.json
   ```
   > ⚠️ **SECURITY WARNING**: Never commit `firebase-service-account.json` to public Git repositories. The file is excluded by `.gitignore`.

### Step 2.4: Register a Web App for Client-Side Real-Time Listeners
1. Still in **Project settings**, click the **General** tab.
2. Scroll down to the **Your apps** section and click the **Web icon (</>)**.
3. Enter an app nickname (e.g., `Smart Parking Web`).
4. Do *not* check Firebase Hosting for now. Click **Register app**.
5. Copy the configuration values (`apiKey`, `authDomain`, `projectId`, `storageBucket`, `messagingSenderId`, `appId`).

### Step 2.5: Apply Firebase Database Security Rules
1. In the Firebase Console, go to **Build** &rarr; **Realtime Database** &rarr; **Rules** tab.
2. Copy the entire contents of `database.rules.json` from this project workspace.
3. Paste into the rules editor and click **Publish**.

---

## 3. Environment Configuration (`.env`)

1. In the root directory of the project, create a `.env` file by copying `.env.example`:
   ```bash
   cp .env.example .env
   ```
2. Open `.env` and fill in your genuine Firebase details:

```ini
# Flask Secret
SECRET_KEY=smart-parking-secret-key-2026-prod-sec

# Firebase Realtime Database URL
FIREBASE_DATABASE_URL=https://your-project-default-rtdb.firebaseio.com/

# Path to downloaded service account private key JSON
FIREBASE_CREDENTIALS_PATH=credentials/firebase-service-account.json

# Web App Client Credentials (from Step 2.4)
FIREBASE_API_KEY=AIzaSyA1B2C3D4E5F6G7H8I9J0
FIREBASE_AUTH_DOMAIN=your-project.firebaseapp.com
FIREBASE_PROJECT_ID=your-project
FIREBASE_STORAGE_BUCKET=your-project.appspot.com
FIREBASE_MESSAGING_SENDER_ID=123456789012
FIREBASE_APP_ID=1:123456789012:web:abcdef123456
```

---

## 4. Ingest Existing Datasets into Firebase Realtime Database

Once your `.env` file is saved with the valid credentials, execute the Firebase ingestion script:

```bash
python scripts/import_firebase.py
```

### Expected Output:
```
==================================================================
  Smart Parking System - Firebase & Local Database Ingestion
==================================================================
[*] Connecting to Firebase Realtime Database...
[*] Firebase Status: Firebase Realtime Database (Online)
[*] Target Database URL: https://your-project-default-rtdb.firebaseio.com/
[+] Genuinely connected to Firebase Realtime Database!
[*] Synchronizing parking facilities, slots, and historical records to Firebase...
[+] Successfully pushed to Firebase:
    - Facilities: 4
    - Parking Slots: 90
    - Historical Records: 250
[SUCCESS] Firebase Realtime Database is completely populated and live!
```

---

## 5. Running the Real-Time Application

Start the application:
```bash
python app.py
```

Access in your browser:
```
http://127.0.0.1:5000
```

### Verifying Real-Time Multi-User Synchronization:
1. Open **Browser Session 1** (e.g. Chrome) and log in as Driver (`driver@example.com` / `Driver@12345`).
2. Open **Browser Session 2** (e.g. Incognito or Edge) and view the Dashboard (`/dashboard`) or Slot Bay Layout (`/slots/1`).
3. In **Session 1**, reserve an available slot (e.g., `A-01`).
4. Observe **Session 2**: Within a fraction of a second, without touching the mouse or refreshing the page, Slot `A-01` turns **Blue (Reserved)**, and the availability counters automatically decrement!
5. In **Session 2**, attempt to reserve `A-01` for the same time window. The server rejects the overlapping reservation with a clear conflict warning.
6. In **Session 1**, cancel the reservation. Slot `A-01` in **Session 2** turns **Green (Available)** immediately!
