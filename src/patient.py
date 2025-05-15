import pandas as pd
import random
import string

class PatientManager:
    def __init__(self, patients_df, notes_df):
        self.patients = patients_df
        self.notes = notes_df

    def add_patient(self):
        patient_id = input("Enter Patient_ID: ")
        if patient_id in self.patients['Patient_ID'].values:
            visit_id = self._generate_id()
            visit_time = input("Enter Visit_time (YYYY-MM-DD): ")
            department = input("Enter Visit_department: ")
            row = {'Patient_ID': patient_id, 'Visit_ID': visit_id, 'Visit_time': visit_time, 'Visit_department': department}
            self.patients = pd.concat([self.patients, pd.DataFrame([row])], ignore_index=True)
        else:
            visit_id = self._generate_id()
            visit_time = input("Enter Visit_time (YYYY-MM-DD): ")
            department = input("Enter Visit_department: ")
            gender = input("Enter Gender: ")
            race = input("Enter Race: ")
            age = int(input("Enter Age: "))
            ethnicity = input("Enter Ethnicity: ")
            insurance = input("Enter Insurance: ")
            zip_code = input("Enter Zip code: ")
            complaint = input("Enter Chief complaint: ")
            row = {'Patient_ID': patient_id, 'Visit_ID': visit_id, 'Visit_time': visit_time, 'Visit_department': department,
                   'Gender': gender, 'Race': race, 'Age': age, 'Ethnicity': ethnicity, 'Insurance': insurance,
                   'Zip code': zip_code, 'Chief complaint': complaint}
            self.patients = pd.concat([self.patients, pd.DataFrame([row])], ignore_index=True)
        print("Patient record added.")

    def add_existing_patient(self, patient_id, visit_time, department):
        visit_id = self._generate_id()
        new_row = {
            'Patient_ID': patient_id,
            'Visit_ID': visit_id,
            'Visit_time': visit_time,
            'Visit_department': department
        }
        self.patients = pd.concat([self.patients, pd.DataFrame([new_row])], ignore_index=True)

    def add_new_patient(
        self, patient_id, visit_time, department, gender, race, age,
        ethnicity, insurance, zip_code, complaint,
        note_id=None, note_type=None, note_text=None
    ):
        visit_id = self._generate_id()

        new_patient_row = {
            'Patient_ID': patient_id,
            'Visit_ID': visit_id,
            'Visit_time': visit_time,
            'Visit_department': department,
            'Race': race,
            'Gender': gender,
            'Ethnicity': ethnicity,
            'Age': age,
            'Zip_code': zip_code,
            'Insurance': insurance,
            'Chief_complaint': complaint,
            'Note_ID': note_id,
            'Note_type': note_type
        }

        self.patients = pd.concat([self.patients, pd.DataFrame([new_patient_row])], ignore_index=True)

        if note_id and note_text:
            new_note_row = {
                'Patient_ID': patient_id,
                'Visit_ID': visit_id,
                'Note_ID': note_id,
                'Note_text': note_text
            }
            self.notes = pd.concat([self.notes, pd.DataFrame([new_note_row])], ignore_index=True)

        return visit_id


    def remove_patient(self):
        patient_id = input("Enter Patient_ID to remove: ")
        if patient_id not in self.patients['Patient_ID'].values:
            print("Patient ID does not exist.")
            return
        self.patients = self.patients[self.patients['Patient_ID'] != patient_id]
        print("Patient record removed.")

    def retrieve_patient(self):
        print("Available Patient IDs:", self.patients['Patient_ID'].unique())

        try:
            patient_id = int(input("Enter Patient_ID to retrieve: "))
        except ValueError:
            print("Invalid Patient_ID. Must be an integer.")
            return

        record = self.patients[self.patients['Patient_ID'] == patient_id]
        if record.empty:
            print("Patient ID not found.")
        else:
            print(record)


    def count_visits(self, date):
        # Convert Visit_time to datetime
        self.patients['Visit_time'] = pd.to_datetime(self.patients['Visit_time'], errors='coerce')

        # Convert input date to datetime
        try:
            input_date = pd.to_datetime(date, format='%Y-%m-%d')
        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD.")
            return

        # Filter by date
        count = self.patients[self.patients['Visit_time'].dt.date == input_date.date()].shape[0]
        print(f"Total visits on {input_date.date()}: {count}")


    def view_note(self, date):
        self.notes['Visit_ID'] = self.notes['Visit_ID'].astype(str)
        self.patients['Visit_ID'] = self.patients['Visit_ID'].astype(str)
        self.patients['Visit_time'] = pd.to_datetime(self.patients['Visit_time'], errors='coerce')

        try:
            input_date = pd.to_datetime(date, format='%Y-%m-%d')
        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD.")
            return

        merged = pd.merge(
            self.notes,
            self.patients[['Visit_ID', 'Visit_time']],
            on='Visit_ID',
            how='left'
        )

        filtered_notes = merged[merged['Visit_time'].dt.date == input_date.date()]

        if filtered_notes.empty:
            print("No notes found for this date.")
        else:
            print(f"\nClinical notes for {input_date.date()}:\n")
            for i, row in filtered_notes.iterrows():
                print(f"Note ID: {row['Note_ID']}")
                print(f"Note Text:\n{row['Note_text']}\n{'-'*60}")




    def _generate_id(self):
        return ''.join(random.choices(string.digits, k=6))
