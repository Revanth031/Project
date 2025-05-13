from user import authenticate_user
from patient import PatientManager
from stats import StatisticsGenerator
from utils import load_patient_data, save_patient_data, load_note_data

def run_program_in_notebook(username, password):
    user = authenticate_user(username, password)
    if not user:
        print("Authentication failed. Invalid credentials.")
        return

    print(f"Login successful. Role: {user.role}\n")

    patient_data = load_patient_data("Patient_data.csv")
    note_data = load_note_data("Notes.csv")
    patient_manager = PatientManager(patient_data, note_data)

    if user.role == "management":
        StatisticsGenerator.generate_all_statistics(patient_data)
    elif user.role == "admin":
        date = input("Enter date (YYYY-MM-DD): ")
        patient_manager.count_visits(date)
    elif user.role in ["nurse", "clinician"]:
        while True:
            action = input("Enter action (add_patient, remove_patient, retrieve_patient, count_visits, view_note, Stop): ")
            if action == "Stop":
                break
            elif action == "add_patient":
                patient_manager.add_patient()
            elif action == "remove_patient":
                patient_manager.remove_patient()
            elif action == "retrieve_patient":
                patient_manager.retrieve_patient()
            elif action == "count_visits":
                date = input("Enter date (YYYY-MM-DD): ")
                patient_manager.count_visits(date)
            elif action == "view_note":
                date = input("Enter date (YYYY-MM-DD): ")
                patient_manager.view_note(date)
            else:
                print("Invalid action.")
        save_patient_data("Patient_data.csv", patient_manager.patients)
    else:
        print("Role not supported.")