# Clinical Data Access and Analytics System

## Overview

This Python project simulates a secure, role-based hospital data management system that allows different user types to interact with patient records and clinical notes. It supports essential functionalities such as adding/removing patients, viewing patient records, counting visits, and generating statistical reports.

This program was developed for **HI 741 Spring 2025 Programming Assignment 3**.

---

## Features

- **Role-Based Access Control (RBAC)** for four user roles: `admin`, `clinician`, `nurse`, `management`.
- **Credential Authentication** from a CSV file.
- **Patient Record Management**: Add, remove, retrieve patients.
- **Clinical Notes Viewer** based on visit dates.
- **Statistical Reports** for hospital management including:
  - Age distribution
  - Insurance types
  - Gender, Race, and Ethnicity breakdowns
- **Command-line Interface** for interactive use.

---

## Roles & Permissions

| Role        | Actions Allowed                                                                 |
|-------------|----------------------------------------------------------------------------------|
| admin       | `count_visits` on a specified date                                               |
| clinician   | `add_patient`, `remove_patient`, `retrieve_patient`, `count_visits`, `view_note`|
| nurse       | Same as `clinician`                                                              |
| management  | Generates summary statistics only                                                |

---

## Directory Structure

```
.
├── Credentials.csv
├── Notes.csv
├── Patient_data.csv
├── main.py
├── user.py
├── patient.py
├── stats.py
├── utils.py
├── notebook_runner.py
└── README.md
```

---

## Usage

### Run the Program

```bash
python user_interface.py
```

---

## File Descriptions

| File              | Purpose                                                        |
|-------------------|----------------------------------------------------------------|
| `main.py`         | Main entry point. Parses arguments and routes by user role     |
| `user.py`         | Handles user authentication and role assignment                |
| `patient.py`      | Manages patient data operations                                |
| `stats.py`        | Generates and saves patient statistics as images               |
| `utils.py`        | Utilities for loading/saving data                              |
| `notebook_runner.py` | Notebook-friendly runner (alternative to CLI)              |

---

## Data Files

- `Credentials.csv`: Contains username, password, and role
- `Patient_data.csv`: Contains patient demographics and visit records
- `Notes.csv`: Contains clinical notes tied to visit IDs

---

## Output

- For **management**, plots are saved as:
  - `hist_age_distribution.png`
  - `hist_insurance.png`
  - `pie_gender_distribution.png`
  - `hist_race.png`
  - `hist_ethnicity.png`

---

## Requirements

- Python 3.x
- pandas
- matplotlib

Install dependencies:

```bash
pip install pandas matplotlib
```

---

## Notes

- Patient visit IDs are auto-generated.
- Dates must be in `YYYY-MM-DD` format.
- Changes to patient records are written back to `Patient_data.csv`.
