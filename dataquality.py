import streamlit as st
import pandas as pd
from datetime import datetime
df = pd.read_csv(r"C:\Users\Abinash P\Downloads\ehr_healthcare_data_updated.csv")
st.write(df)
missing_data = df.isnull().mean() * 100
missing_data[missing_data > 0]
expected_data_types = {
    'Age': 'int64',
    'Gender': 'object',
    'Height_cm': 'float64',
    'Weight_kg': 'float64',
    'BMI': 'float64',
    'BloodType': 'object',
    'SystolicBP': 'int64',
    'DiastolicBP': 'int64',
    'HeartRate': 'int64',
    'RespiratoryRate': 'int64',
    'Temperature_C': 'float64',
    'AdmissionDate': 'datetime64[ns]',
    'DischargeDate': 'datetime64[ns]'
}
conformity_issues = {}
for col, expected_type in expected_data_types.items():
    if col in df.columns and df[col].dtype != expected_type:
        conformity_issues[col] = {'Expected': expected_type, 'Actual': df[col].dtype}

conformity_issues

df['Calculated_BMI'] = df['Weight_kg'] / (df['Height_cm'] / 100) ** 2
accuracy_issues = df[df['BMI'] != df['Calculated_BMI'].round(1)]
accuracy_issues[['BMI', 'Calculated_BMI']]

inconsistent_records = df[df.duplicated(subset=['PatientID', 'BloodType'], keep=False)]
inconsistent_records

current_year = datetime.now().year
df['AdmissionDate'] = pd.to_datetime(df['AdmissionDate'], errors='coerce')
df['DischargeDate'] = pd.to_datetime(df['DischargeDate'], errors='coerce')

continuity_issues = df[(df['AdmissionDate'].dt.year < current_year - 5) | 
                       (df['DischargeDate'].dt.year < current_year - 5)]
continuity_issues[['AdmissionDate', 'DischargeDate']]

duplicate_patient_ids = df[df.duplicated(subset='PatientID')]
duplicate_patient_ids[['PatientID']]

unique_issues = df[df.duplicated(subset=['PatientID', 'AdmissionDate', 'Diagnosis'], keep=False)]
unique_issues

redundant_data = df[df.duplicated()]
redundant_data

medical_records = pd.DataFrame({'PatientID': [1, 2, 3, 4, 5]})  
missing_references = medical_records[~medical_records['PatientID'].isin(df['PatientID'])]
missing_references
