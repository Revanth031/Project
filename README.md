# Clinical Data Warehouse - Final Project (Spring 2025)

This project is a clinical data management system built with Python and Tkinter. It allows authenticated users (admin, nurse, clinician, and management roles) to manage patient records, clinical notes, and view analytical statistics.

---

## 🚀 Features

- ✅ Role-based login system with credential verification
- ✅ Add, remove, and retrieve patient records
- ✅ Store and view clinical notes
- ✅ Count visits by date
- ✅ Generate and export statistics (histograms, pie charts)
- ✅ Usage logging for all user actions
- ✅ GUI built with Tkinter for a modern desktop experience
- ✅ Clean data export in CSV format (`Patient_data.csv`, `Notes.csv`, `usage_log.csv`)

---

## 🔐 Roles and Permissions

| Role       | Permissions                                         |
|------------|-----------------------------------------------------|
| `admin`    | Count visits only                                   |
| `nurse`    | Add/remove/retrieve patients, view notes, count     |
| `clinician`| Same as nurse                                       |
| `management` | Generate statistics only                          |

---

## 🧪 Sample Credentials (from Credentials.csv)

| Username    | Password   | Role        |
|-------------|------------|-------------|
| admin1      | admin123   | admin       |
| nurse1      | nurse123   | nurse       |
| doctor1     | doc123     | clinician   |
| manager1    | manage123  | management  |

---

🖥️ How to Run
Terminal (Command Line)

python main.py -username YOUR_USERNAME -password YOUR_PASSWORD

python user_interface.py

