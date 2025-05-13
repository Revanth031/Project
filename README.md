# Clinical Data Warehouse - Final Project

This project is a clinical data management system built in Python using Tkinter for the graphical user interface. It supports multiple user roles and enables management of patient records and clinical notes along with basic statistics generation.

## Features

- Role-based user login system
- Add, retrieve, and remove patient records
- View clinical notes by date
- Count visits on a specific date
- Generate visual statistics from patient data
- Usage logging for audit trails
- Clean and responsive Tkinter GUI

## Roles and Permissions

| Role        | Allowed Actions                                           |
|-------------|-----------------------------------------------------------|
| admin       | Count visits only                                         |
| nurse       | Add, remove, retrieve patients; view notes; count visits |
| clinician   | Same as nurse                                             |
| management  | Generate statistics only                                  |

## Directory Structure

