import pandas as pd
import matplotlib.pyplot as plt

class StatisticsGenerator:
    @staticmethod
    def generate_all_statistics(patients_df):
        patients_df['Visit_time'] = pd.to_datetime(patients_df['Visit_time'], errors='coerce')

        # Histogram 1: Age distribution
        if 'Age' in patients_df.columns:
            plt.figure(figsize=(10, 6))
            patients_df['Age'].dropna().astype(int).plot(kind='hist', bins=20, edgecolor='black')
            plt.title("Age Distribution of Patients", fontsize=14)
            plt.xlabel("Age", fontsize=12)
            plt.ylabel("Number of Patients", fontsize=12)
            plt.tight_layout()
            plt.savefig("hist_age_distribution.png", dpi=300)
            plt.close()

        # Histogram 2: Number of patients by insurance type
        if 'Insurance' in patients_df.columns:
            plt.figure(figsize=(10, 6))
            patients_df['Insurance'].value_counts().plot(kind='bar', edgecolor='black')
            plt.title("Distribution of Insurance Types", fontsize=14)
            plt.xlabel("Insurance Type", fontsize=12)
            plt.ylabel("Number of Patients", fontsize=12)
            plt.tight_layout()
            plt.savefig("hist_insurance.png", dpi=300)
            plt.close()

        # Histogram 3: Gender distribution
        # Pie Chart: Gender distribution
        if 'Gender' in patients_df.columns:
            gender_counts = patients_df['Gender'].value_counts()
            plt.figure(figsize=(8, 8))
            plt.pie(gender_counts, labels=gender_counts.index, autopct='%1.1f%%', startangle=90)
            plt.title("Gender Distribution", fontsize=14)
            plt.axis('equal')  # Equal aspect ratio ensures the pie is circular
            plt.tight_layout()
            plt.savefig("pie_gender_distribution.png", dpi=300)
            plt.close()


        # Histogram 4: Race distribution
        if 'Race' in patients_df.columns:
            plt.figure(figsize=(10, 6))
            patients_df['Race'].value_counts().plot(kind='bar', edgecolor='black')
            plt.title("Race Distribution", fontsize=14)
            plt.xlabel("Race", fontsize=12)
            plt.ylabel("Number of Patients", fontsize=12)
            plt.tight_layout()
            plt.savefig("hist_race.png", dpi=300)
            plt.close()

        # Histogram 5: Ethnicity distribution
        if 'Ethnicity' in patients_df.columns:
            plt.figure(figsize=(10, 6))
            patients_df['Ethnicity'].value_counts().plot(kind='bar', edgecolor='black')
            plt.title("Ethnicity Distribution", fontsize=14)
            plt.xlabel("Ethnicity", fontsize=12)
            plt.ylabel("Number of Patients", fontsize=12)
            plt.tight_layout()
            plt.savefig("hist_ethnicity.png", dpi=300)
            plt.close()

        print("Histogram statistics generated and saved as image files.")
