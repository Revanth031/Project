import tkinter as tk
from tkinter import messagebox, simpledialog, Toplevel, Label, Entry, Button, StringVar, OptionMenu, Frame
from user import authenticate_user
from patient import PatientManager
from stats import StatisticsGenerator
from utils import load_patient_data, save_patient_data, save_note_data, load_note_data
import datetime
import pandas as pd
from utils import log_usage

class ClinicalApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Clinical Data Warehouse")
        self.root.geometry("800x600")
        self.root.configure(bg="#f0f0f5")
        self.username = None
        self.user = None
        self.patient_data = load_patient_data("Patient_data.csv")
        self.note_data = load_note_data("Notes.csv")
        self.patient_manager = PatientManager(self.patient_data, self.note_data)
        self.login_screen()

    def styled_label(self, parent, text, font_size=12, width=40):
        return Label(parent, text=text, font=("Helvetica Neue", font_size), bg="#f0f0f5", width=width, anchor="w")

    def styled_entry(self, parent, width=40):
        return Entry(parent, font=("Helvetica Neue", 12), bd=2, relief="groove", width=width)

    def styled_button(self, parent, text, command, width=30):
        return Button(parent, text=text, command=command, font=("Helvetica Neue", 12), bg="#007aff", fg="white", relief="flat", padx=10, pady=5, width=width)

    def login_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        # Create a centered "card" frame
        card = Frame(self.root, bg="white", bd=1, relief="solid")
        card.place(relx=0.5, rely=0.5, anchor="center", width=400, height=320)
        
        Label(card, text="Welcome", font=("Helvetica Neue", 20, "bold"), bg="white").pack(pady=(20, 10))

        form = Frame(card, bg="white")
        form.pack(pady=10)

        # Username row
        Label(form, text="Username:", font=("Helvetica Neue", 12), bg="white").grid(row=0, column=0, sticky="e", padx=10, pady=8)
        username_entry = Entry(form, font=("Helvetica Neue", 12), width=25, relief="groove", bd=2)
        username_entry.grid(row=0, column=1, padx=10)

        # Password row
        Label(form, text="Password:", font=("Helvetica Neue", 12), bg="white").grid(row=1, column=0, sticky="e", padx=10, pady=8)
        password_entry = Entry(form, font=("Helvetica Neue", 12), width=25, relief="groove", bd=2, show='*')
        password_entry.grid(row=1, column=1, padx=10)

        def attempt_login():
            username = username_entry.get()
            password = password_entry.get()
            self.user = authenticate_user(username, password)
            if self.user:
                self.username = username
                log_usage(username, self.user.role, action="login", status="success")
                self.menu_screen()
            else:
                log_usage(username, "unknown", action="login", status="fail")
                messagebox.showerror("Login Failed", "Invalid username or password.")

        # Login button
        Button(card, text="Login", command=attempt_login, font=("Helvetica Neue", 12), bg="#007aff", fg="white",
            activebackground="#005bb5", width=20, relief="flat", bd=0).pack(pady=(10, 20))

    def menu_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        container = Frame(self.root, bg="white", bd=1, relief="solid", padx=20, pady=20)
        container.pack(pady=80)

        Label(container, text=f"Welcome, {self.username}", font=("Helvetica Neue", 14, "bold"), bg="white")\
            .pack(pady=(0, 4))

        Label(container, text=f"Role: {self.user.role.title()}", font=("Helvetica Neue", 11), fg="#666", bg="white")\
            .pack(pady=(0, 15))

        actions = {
            "admin": [("Count Visits", self.count_visits)],
            "management": [("Generate Key Statistics", self.generate_statistics)],
            "nurse": self.get_full_access_buttons(),
            "clinician": self.get_full_access_buttons()
        }

        for text, command in actions.get(self.user.role, []):
            Button(container, text=text, command=command, font=("Helvetica Neue", 11),
                bg="#007aff", fg="white", relief="flat", width=25).pack(pady=5)

        Button(container, text="Exit", command=self.root.quit,
            font=("Helvetica Neue", 11), bg="#ddd", fg="black", relief="flat", width=15).pack(pady=15)



    def get_full_access_buttons(self):
        return [
            ("Retrieve Patient", self.retrieve_patient),
            ("Add Patient", self.add_patient),
            ("Remove Patient", self.remove_patient),
            ("Count Visits", self.count_visits),
            ("View Note", self.view_note)
        ]

    def retrieve_patient(self):
        def fetch_patient():
            pid = entry.get()
            
            if not pid:
                form.destroy()
                return

            record = self.patient_manager.patients[
                self.patient_manager.patients['Patient_ID'].astype(str) == str(pid)
            ]

            form.destroy()

            if record.empty:
                messagebox.showinfo("Result", "Patient not found.")
                return

            info_lines = []
            for index, row in record.iterrows():
                info_lines.append(f"Visit ID     : {row['Visit_ID']}")
                info_lines.append(f"Date         : {row['Visit_time']}")
                info_lines.append(f"Department   : {row.get('Visit_department', 'N/A')}")
                info_lines.append(f"Gender       : {row.get('Gender', 'N/A')}")
                info_lines.append(f"Race         : {row.get('Race', 'N/A')}")
                info_lines.append(f"Ethnicity    : {row.get('Ethnicity', 'N/A')}")
                info_lines.append(f"Age          : {int(float(row.get('Age', 0)))}")
                info_lines.append(f"Zip Code     : {row.get('Zip_code', 'N/A')}")
                info_lines.append(f"Insurance    : {row.get('Insurance', 'N/A')}")
                info_lines.append(f"Complaint    : {row.get('Chief_complaint', 'N/A')}")
                info_lines.append(f"Note ID      : {row.get('Note_ID', 'N/A')}")
                info_lines.append(f"Note Type    : {row.get('Note_type', 'N/A')}")
                info_lines.append("")  # spacer between visits

            info_text = "\n".join(info_lines)
            log_usage(self.username, self.user.role, action="retrieve_patient")
            # Output window
            window = Toplevel(self.root)
            window.title("Patient Details")
            window.geometry("420x400")
            window.configure(bg="#ffffff")
            window.resizable(False, False)

            Label(window, text=f"Patient ID: {pid}", font=("Helvetica Neue", 13, "bold"), bg="white")\
                .pack(pady=(10, 5))

            text_area = tk.Text(window, wrap="word", font=("Helvetica Neue", 10), bg="#f7f7f7",
                                relief="flat", bd=1, padx=10, pady=10, height=20)
            text_area.insert("1.0", info_text)
            text_area.config(state="disabled")
            text_area.pack(padx=10, pady=(0, 10), expand=False, fill="both")


        # Custom input form
        form = Toplevel(self.root)
        form.title("Retrieve Patient")
        form.geometry("300x150")
        form.configure(bg="white")

        Label(form, text="Enter Patient_ID:", font=("Helvetica Neue", 12), bg="white").pack(pady=(20, 5))
        entry = Entry(form, font=("Helvetica Neue", 12), bd=2, relief="groove")
        entry.pack(pady=5)

        Button(form, text="Submit", command=fetch_patient, font=("Helvetica Neue", 11), bg="#007aff", fg="white", width=10).pack(pady=10)


    def add_patient(self):
        def submit():
            import random
            patient_id = entries['Patient_ID'].get()
            visit_time_input = entries['Visit_time'].get()
            try:
                visit_time = pd.to_datetime(visit_time_input, format='%Y-%m-%d').strftime('%m/%d/%Y')
            except ValueError:
                messagebox.showerror("Invalid Date", "Please enter the date in YYYY-MM-DD format.")
                return

            department = entries['Visit_department'].get()
            gender = gender_var.get()
            race = race_var.get()
            age = entries['Age'].get()
            ethnicity = ethnicity_var.get()
            insurance = insurance_var.get()
            zip_code = entries['Zip'].get()
            complaint = entries['Chief'].get()
            note_type = note_type_var.get()
            note_text = note_box.get("1.0", tk.END).strip()

            visit_id = self.patient_manager._generate_id()
            note_id = ''.join(random.choices("0123456789", k=6))

            self.patient_manager.add_new_patient(
                patient_id, visit_time, department, gender, race, int(age),
                ethnicity, insurance, zip_code, complaint,
                note_id=note_id, note_type=note_type, note_text=note_text
            )

            save_patient_data("Patient_data.csv", self.patient_manager.patients)
            save_note_data("Notes.csv", self.patient_manager.notes)

            form.destroy()
            messagebox.showinfo("Success", "Patient and note added.")
            log_usage(self.username, self.user.role, action="add_patient")

        # Create form window
        form = Toplevel(self.root)
        form.title("Add Patient")
        form.geometry("550x700")
        form.configure(bg="#f0f0f5")

        container = Frame(form, bg="#f0f0f5")
        container.pack(pady=20)

        fields = ["Patient_ID", "Visit_time (YYYY-MM-DD)", "Visit_department", "Age", "Zip code", "Chief complaint"]
        entries = {}

        for idx, field in enumerate(fields):
            Label(container, text=field + ":", font=("Helvetica Neue", 11), bg="#f0f0f5", anchor="e", width=20)\
                .grid(row=idx, column=0, padx=10, pady=5)
            entry = Entry(container, font=("Helvetica Neue", 11), width=30, relief="groove", bd=2)
            entry.grid(row=idx, column=1, padx=10, pady=5)
            entries[field.split()[0]] = entry  # remove (YYYY-MM-DD) from key

        # Dropdowns
        dropdowns = [
            ("Gender", ["Male", "Female", "Non-binary"]),
            ("Race", ["White", "Black", "Asian", "Pacific islanders", "Native Americans", "Unknown"]),
            ("Ethnicity", ["Hispanic", "Non-Hispanic", "Other", "Unknown"]),
            ("Insurance", ["Medicare", "Medicaid", "None", "Unknown"]),
            ("Note Type", ["Discharge", "Oncology", "Progress", "Other"])
        ]

        variables = []
        for i, (label, options) in enumerate(dropdowns):
            var = StringVar(form)
            var.set(f"Select {label}")
            variables.append(var)
            Label(container, text=label + ":", font=("Helvetica Neue", 11), bg="#f0f0f5", anchor="e", width=20)\
                .grid(row=len(fields)+i, column=0, padx=10, pady=5)
            OptionMenu(container, var, *options).grid(row=len(fields)+i, column=1, padx=10, pady=5, sticky="w")

        gender_var, race_var, ethnicity_var, insurance_var, note_type_var = variables

        # Note text field (smaller height)
        Label(container, text="Note Text:", font=("Helvetica Neue", 11), bg="#f0f0f5", anchor="e", width=20)\
            .grid(row=len(fields)+len(dropdowns), column=0, padx=10, pady=(10, 5))
        note_box = tk.Text(container, font=("Helvetica Neue", 11), width=30, height=4, wrap="word", bd=2, relief="groove")
        note_box.grid(row=len(fields)+len(dropdowns), column=1, padx=10, pady=(10, 5))

        Button(container, text="Submit", command=submit, font=("Helvetica Neue", 11),
            bg="#007aff", fg="white", width=20).grid(columnspan=2, pady=20)

    def remove_patient(self):
        def confirm_removal():
            pid = entry.get()
            form.destroy()

            if pid not in self.patient_manager.patients['Patient_ID'].astype(str).values:
                messagebox.showinfo("Not Found", f"Patient ID {pid} does not exist.")
                return

            # Remove from DataFrame
            self.patient_manager.patients = self.patient_manager.patients[
                self.patient_manager.patients['Patient_ID'].astype(str) != str(pid)
            ]

            save_patient_data("Patient_data.csv", self.patient_manager.patients)
            messagebox.showinfo("Removed", f"Patient ID {pid} has been removed.")
            log_usage(self.username, self.user.role, action="delete_patient")
        # Custom dialog window
        form = Toplevel(self.root)
        form.title("Remove Patient")
        form.geometry("300x150")
        form.configure(bg="white")

        Label(form, text="Enter Patient_ID to remove:", font=("Helvetica Neue", 12), bg="white").pack(pady=(20, 5))
        entry = Entry(form, font=("Helvetica Neue", 12), bd=2, relief="groove")
        entry.pack(pady=5)

        Button(form, text="Remove", command=confirm_removal, font=("Helvetica Neue", 11),
            bg="#ff3b30", fg="white", width=10).pack(pady=10)


    def count_visits(self):
        def submit_date():
            date = date_entry.get()
            form.destroy()

            try:
                # Normalize formats
                self.patient_manager.patients['Visit_time'] = pd.to_datetime(
                    self.patient_manager.patients['Visit_time'], errors='coerce', format='%m/%d/%Y'
                )
                input_date = pd.to_datetime(date, format='%Y-%m-%d')

                count = self.patient_manager.patients[
                    self.patient_manager.patients['Visit_time'].dt.date == input_date.date()
                ].shape[0]

                messagebox.showinfo("Visit Count", f"Total visits on {input_date.date()}: {count}")

            except Exception as e:
                messagebox.showerror("Error", f"Invalid date or data.\n{e}")
        log_usage(self.username, self.user.role, action="count_visits")
        form = Toplevel(self.root)
        form.title("Count Visits")
        form.geometry("300x150")
        form.configure(bg="white")

        Label(form, text="Enter date (YYYY-MM-DD):", font=("Helvetica Neue", 12), bg="white").pack(pady=(20, 5))
        date_entry = Entry(form, font=("Helvetica Neue", 12), bd=2, relief="groove")
        date_entry.pack(pady=5)

        Button(form, text="Count", command=submit_date, font=("Helvetica Neue", 11),
            bg="#007aff", fg="white", width=10).pack(pady=10)


    def view_note(self):
        def submit_date():
            date = date_entry.get()
            form.destroy()

            try:
                self.patient_manager.notes['Visit_ID'] = self.patient_manager.notes['Visit_ID'].astype(str)
                self.patient_manager.patients['Visit_ID'] = self.patient_manager.patients['Visit_ID'].astype(str)
                self.patient_manager.patients['Visit_time'] = pd.to_datetime(
                    self.patient_manager.patients['Visit_time'], errors='coerce', format='%m/%d/%Y'
                )
                input_date = pd.to_datetime(date, format='%Y-%m-%d')

                merged = pd.merge(
                    self.patient_manager.notes,
                    self.patient_manager.patients[['Visit_ID', 'Visit_time']],
                    on='Visit_ID', how='left'
                )

                filtered_notes = merged[merged['Visit_time'].dt.date == input_date.date()]

                if filtered_notes.empty:
                    messagebox.showinfo("No Notes", "No notes found for this date.")
                    return

                result_window = Toplevel(self.root)
                result_window.title(f"Notes on {input_date.date()}")
                result_window.geometry("500x400")
                result_window.configure(bg="white")

                text_area = tk.Text(result_window, wrap="word", font=("Helvetica Neue", 11),
                                    bg="#f9f9f9", relief="solid", bd=1)
                for _, row in filtered_notes.iterrows():
                    text_area.insert(tk.END, f"Note ID: {row['Note_ID']}\n")
                    text_area.insert(tk.END, f"{row['Note_text']}\n\n")

                text_area.config(state="disabled")
                text_area.pack(padx=10, pady=10, expand=True, fill="both")

            except Exception as e:
                messagebox.showerror("Error", f"Invalid date or data.\n{e}")
        log_usage(self.username, self.user.role, action="view_note")
        form = Toplevel(self.root)
        form.title("View Notes")
        form.geometry("300x150")
        form.configure(bg="white")

        Label(form, text="Enter date (YYYY-MM-DD):", font=("Helvetica Neue", 12), bg="white").pack(pady=(20, 5))
        date_entry = Entry(form, font=("Helvetica Neue", 12), bd=2, relief="groove")
        date_entry.pack(pady=5)

        Button(form, text="View", command=submit_date, font=("Helvetica Neue", 11),
            bg="#34c759", fg="white", width=10).pack(pady=10)



    def generate_statistics(self):
        StatisticsGenerator.generate_all_statistics(self.patient_manager.patients)
        log_usage(self.username, self.user.role, action="generate_stats")
        messagebox.showinfo(
            "Statistics Generated",
            "All histograms and charts have been saved as image files in the working directory."
        )


if __name__ == "__main__":
    root = tk.Tk()
    app = ClinicalApp(root)
    root.mainloop()
