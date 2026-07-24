# --- TrialMind DSA export: traceability header ---
# Project:         Seizures (b0ff17c7-61de-4d2d-99e6-d69823d6371f)
# User:            zilal@keiji.ai
# Dataset version: 9e50addfcb6043ef8ef2163bd65daa54
# Execution ID:    6b4044c9-9b96-46e1-bd08-b795bd9a0bbd
# Source SHA-256:  07bacaef27791441aa3a566a282820a4b48ac95a0e402aafa6f98736fbe1c572  (of exported code, pre-header)
# Exported (UTC):  2026-07-24T06:50:24Z
# Approval status: NOT_APPROVED
# Decision Support — Not for diagnostic or clinical decision-making (override)
# -------------------------------------------------

import pyreadstat
import pandas as pd

# Load adverse events data
ae_df, ae_meta = pyreadstat.read_xport("/workdir/ae.xpt")  # trialmind:input id="/workdir/ae.xpt" kind=file name="Adverse Events"

# Load demographics to get total patient count
dm_df, dm_meta = pyreadstat.read_xport("/workdir/dm.xpt")  # trialmind:input id="/workdir/dm.xpt" kind=file name="Demographics"

print("=" * 60)
print("SEIZURE-FREE PATIENTS AFTER TREATMENT ANALYSIS")
print("=" * 60)

# Total unique patients in the study
total_patients = dm_df['USUBJID'].nunique()
print(f"\nTotal patients in study: {total_patients}")

# Define seizure-specific terms (excluding muscle spasms which are not seizures)
seizure_terms = ['SEIZURE', 'CONVULS', 'EPILEP']

# Filter adverse events for seizure-related events during treatment
ae_treatment = ae_df[ae_df['EPOCH'] == 'TREATMENT'].copy()
print(f"\nAdverse events during treatment phase: {len(ae_treatment)}")

# Identify seizure events (by AEDECOD)
seizure_mask = ae_treatment['AEDECOD'].str.upper().str.contains('|'.join(seizure_terms), na=False)
seizure_events = ae_treatment[seizure_mask]

print(f"\n--- Seizure Events During Treatment ---")
print(f"Total seizure events: {len(seizure_events)}")
if len(seizure_events) > 0:
    print("\nDetailed seizure events:")
    print(seizure_events[['USUBJID', 'AEDECOD', 'AESEV', 'AESTDTC']].to_string(index=False))

# Get unique patients with seizures during treatment
patients_with_seizures = seizure_events['USUBJID'].unique()
n_patients_with_seizures = len(patients_with_seizures)

print(f"\n--- Summary Statistics ---")
print(f"Patients who experienced seizures during treatment: {n_patients_with_seizures}")

# Calculate seizure-free patients
seizure_free_patients = total_patients - n_patients_with_seizures
seizure_free_percentage = (seizure_free_patients / total_patients) * 100

print(f"Patients seizure-free after treatment: {seizure_free_patients}")
print(f"\n" + "=" * 60)
print(f"PERCENTAGE OF SEIZURE-FREE PATIENTS: {seizure_free_percentage:.2f}%")
print(f"({seizure_free_patients} out of {total_patients} patients)")
print("=" * 60)

# Additional context: show patients with seizures
if n_patients_with_seizures > 0:
    print(f"\nPatients with seizure events:")
    for pid in patients_with_seizures:
        print(f"  - {pid}")

# Create summary table
summary_data = {
    'Metric': ['Total Patients', 'Patients with Seizures', 'Seizure-Free Patients', 'Seizure-Free Percentage (%)'],
    'Value': [total_patients, n_patients_with_seizures, seizure_free_patients, round(seizure_free_percentage, 2)]
}
summary_df = pd.DataFrame(summary_data)
summary_df.to_csv("/workdir/execution_outputs/seizure_free_analysis.csv", index=False)  # trialmind:output id="/workdir/execution_outputs/seizure_free_analysis.csv" kind=file name="Seizure-Free Analysis"
print(f"\nSummary saved to: /workdir/execution_outputs/seizure_free_analysis.csv")
