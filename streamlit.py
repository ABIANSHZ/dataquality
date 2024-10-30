import streamlit as st
import pandas as pd
from datetime import datetime

uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])
if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.write("Data Preview:")
    st.write(df)

    missing_data = df.isnull().mean() * 100
    missing_data = missing_data[missing_data > 0]
    if not missing_data.empty:
        st.write(missing_data)
    else:
        st.write("No missing data detected.")

    st.subheader("Conformity Check")
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
    if conformity_issues:
        st.write(conformity_issues)
    else:
        st.write("All columns conform to expected data types.")

    st.subheader("Accuracy Check: BMI Calculation")
    df['Calculated_BMI'] = df['Weight_kg'] / (df['Height_cm'] / 100) ** 2
    accuracy_issues = df[df['BMI'] != df['Calculated_BMI'].round(1)]
    if not accuracy_issues.empty:
        st.write(accuracy_issues[['BMI', 'Calculated_BMI']])
    else:
        st.write("No accuracy issues detected in BMI calculation.")

    st.subheader("Consistency Check: Duplicate Patient Records")
    inconsistent_records = df[df.duplicated(subset=['PatientID', 'BloodType'], keep=False)]
    if not inconsistent_records.empty:
        st.write(inconsistent_records)
    else:
        st.write("No inconsistent records found.")

    st.subheader("Continuity Check: Admission and Discharge Dates")
    current_year = datetime.now().year
    df['AdmissionDate'] = pd.to_datetime(df['AdmissionDate'], errors='coerce')
    df['DischargeDate'] = pd.to_datetime(df['DischargeDate'], errors='coerce')
    continuity_issues = df[(df['AdmissionDate'].dt.year < current_year - 5) | 
                           (df['DischargeDate'].dt.year < current_year - 5)]
    if not continuity_issues.empty:
        st.write(continuity_issues[['AdmissionDate', 'DischargeDate']])
    else:
        st.write("No continuity issues found in dates.")

    st.subheader("Uniqueness Check: Duplicate Patient IDs")
    duplicate_patient_ids = df[df.duplicated(subset='PatientID')]
    if not duplicate_patient_ids.empty:
        st.write(duplicate_patient_ids[['PatientID']])
    else:
        st.write("No duplicate patient IDs found.")

    st.subheader("Uniqueness Check for Patient, Admission Date, and Diagnosis")
    unique_issues = df[df.duplicated(subset=['PatientID', 'AdmissionDate', 'Diagnosis'], keep=False)]
    if not unique_issues.empty:
        st.write(unique_issues)
    else:
        st.write("No uniqueness issues in the specific combination found.")

    st.subheader("Redundancy Check: Identical Records")
    redundant_data = df[df.duplicated()]
    if not redundant_data.empty:
        st.write(redundant_data)
    else:
        st.write("No redundant records found.")

    st.subheader("Referential Integrity Check")
    medical_records = pd.DataFrame({'PatientID': [1, 2, 3, 4, 5]})
    missing_references = medical_records[~medical_records['PatientID'].isin(df['PatientID'])]
    if not missing_references.empty:
        st.write(missing_references)
    else:
        st.write("No missing references found in medical records.")
