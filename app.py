import streamlit as st
import pandas as pd
import os
from datetime import datetime, timedelta

# -----------------------
# CONFIGURATION
# -----------------------
PATIENT_FILE = "patients.csv"

CONSULTATION_FEES = {
    "General Checkup": 300,
    "Pediatrics": 500,
    "Dermatology": 700,
    "Cardiology": 1000,
    "Orthopedic": 800
}

DEPARTMENTS = {
    "General Medicine": ["Dr. R. Kumar", "Dr. Anita Singh"],
    "Pediatrics": ["Dr. N. Mehta", "Dr. P. Shah"],
    "Dermatology": ["Dr. R. Kapoor", "Dr. T. Desai"],
    "Cardiology": ["Dr. A. Naik", "Dr. B. Varma"],
    "Orthopedics": ["Dr. C. Patel", "Dr. M. Rao"]
}


# -----------------------
# HELPER FUNCTIONS
# -----------------------

def load_patients():
    if not os.path.exists(PATIENT_FILE):
        return pd.DataFrame()
    return pd.read_csv(PATIENT_FILE)


def save_patients(df):
    df.to_csv(PATIENT_FILE, index=False)


def generate_patient_id(patients):
    if patients.empty:
        return "P001"
    last_id = patients["patient_id"].str.extract(r'(\d+)').astype(int).max()[0]
    return f"P{last_id + 1:03d}"


def generate_invoice_id(patients):
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    return f"INV-{timestamp}"


def find_patient(patients, name, contact):
    if patients.empty:
        return None
    match = patients[
        (patients["name"].str.lower() == name.lower())
        & (patients["contact_number"].astype(str) == str(contact))
    ]
    if not match.empty:
        return match.iloc[-1].to_dict()
    return None


# -----------------------
# STREAMLIT UI STARTS HERE
# -----------------------

st.set_page_config(page_title="🏥 Hospital Management System", layout="centered")
st.title("🏥 Hospital Management System")
st.caption("Streamlit Interactive Version – Single File Edition")

menu = st.sidebar.radio("Navigation", ["New Visit", "Reports Dashboard", "Patient History"])

# -----------------------
# 1️⃣ REGISTER NEW VISIT
# -----------------------
if menu == "New Visit":
    st.subheader("➕ Register New Visit")

    name = st.text_input("Patient Name")
    guardian = st.text_input("Guardian Name")
    contact = st.text_input("Contact Number")
    address = st.text_area("Address")

    if st.button("Check Patient"):
        patients = load_patients()
        existing = find_patient(patients, name, contact)

        if existing:
            st.success(f"Returning patient found! ID: {existing['patient_id']}")
            st.session_state["patient"] = existing
        else:
            st.info("New patient. Please continue registration.")
            st.session_state["patient"] = {
                "patient_id": generate_patient_id(patients),
                "name": name,
                "guardian_name": guardian,
                "contact_number": contact,
                "address": address,
                "visit_number": 0
            }

    if "patient" in st.session_state:
        patient = st.session_state["patient"]
        st.write(f"**Patient ID:** {patient['patient_id']}")
        st.write(f"**Name:** {patient['name']}")

        consultation = st.selectbox("Consultation Type", list(CONSULTATION_FEES.keys()))
        department = st.selectbox("Department", list(DEPARTMENTS.keys()))
        doctor = st.selectbox("Doctor", DEPARTMENTS[department])
        payment_mode = st.radio("Payment Mode", ["Cash", "Card", "UPI"])

        total_fee = CONSULTATION_FEES[consultation]
        visit_number = int(patient.get("visit_number", 0)) + 1
        follow_up = "Yes" if visit_number > 1 else "No"

        if st.button("Save Visit"):
            patients = load_patients()
            invoice_id = generate_invoice_id(patients)
            visit_datetime = datetime.now().strftime("%Y-%m-%d %H:%M")

            new_record = {
                "invoice_id": invoice_id,
                "patient_id": patient["patient_id"],
                "name": patient["name"],
                "guardian_name": patient["guardian_name"],
                "contact_number": patient["contact_number"],
                "address": patient["address"],
                "consultation": consultation,
                "department": department,
                "doctor": doctor,
                "payment_mode": payment_mode,
                "visit_datetime": visit_datetime,
                "visit_number": visit_number,
                "follow_up": follow_up,
                "total_fee": total_fee
            }

            if patients.empty:
                patients = pd.DataFrame([new_record])
            else:
                patients = pd.concat([patients, pd.DataFrame([new_record])], ignore_index=True)

            save_patients(patients)

            st.success(f"✅ Visit saved successfully! Total Fee: ₹{total_fee}")
            st.write(new_record)
            del st.session_state["patient"]

# -----------------------
# 2️⃣ REPORTS DASHBOARD
# -----------------------
elif menu == "Reports Dashboard":
    st.subheader("📊 Reports Dashboard")

    df = load_patients()
    if df.empty:
        st.warning("No patient data available.")
    else:
        df["visit_date"] = pd.to_datetime(df["visit_datetime"]).dt.date
        df["visit_month"] = pd.to_datetime(df["visit_datetime"]).dt.to_period("M")

        report_type = st.radio("Select Report", ["Daily", "Weekly", "Monthly"])

        if report_type == "Daily":
            today = datetime.now().date()
            daily = df[df["visit_date"] == today]
            st.markdown(f"### 🗓️ Daily Report ({today})")
            if daily.empty:
                st.info("No visits today.")
            else:
                st.dataframe(daily[["invoice_id", "name", "consultation", "doctor", "total_fee"]])
                st.metric("Total Visits", len(daily))
                st.metric("Total Revenue", f"₹{daily['total_fee'].sum()}")

        elif report_type == "Weekly":
            today = datetime.now().date()
            week_start = today - timedelta(days=6)
            weekly = df[(df["visit_date"] >= week_start) & (df["visit_date"] <= today)]
            st.markdown(f"### 📅 Weekly Report ({week_start} → {today})")
            if weekly.empty:
                st.info("No visits this week.")
            else:
                summary = (
                    weekly.groupby("visit_date")["total_fee"]
                    .agg(Visits="count", Revenue="sum")
                    .reset_index()
                )
                st.dataframe(summary)
                st.metric("Total Visits", summary["Visits"].sum())
                st.metric("Total Revenue", f"₹{summary['Revenue'].sum()}")

        elif report_type == "Monthly":
            monthly = (
                df.groupby("visit_month")["total_fee"]
                .agg(Visits="count", Revenue="sum")
                .reset_index()
            )
            st.markdown("### 🧾 Monthly Summary")
            st.dataframe(monthly)
            st.metric("Total Visits", monthly["Visits"].sum())
            st.metric("Total Revenue", f"₹{monthly['Revenue'].sum()}")

# -----------------------
# 3️⃣ PATIENT HISTORY
# -----------------------
elif menu == "Patient History":
    st.subheader("📖 View Patient History")

    name = st.text_input("Patient Name")
    contact = st.text_input("Contact Number")

    if st.button("Search"):
        df = load_patients()
        if df.empty:
            st.warning("No records found.")
        else:
            records = df[
                (df["name"].str.lower() == name.lower())
                & (df["contact_number"].astype(str) == contact)
            ]
            if records.empty:
                st.info("No history found for this patient.")
            else:
                st.dataframe(records[
                    ["invoice_id", "visit_datetime", "consultation",
                     "department", "doctor", "payment_mode", "total_fee", "follow_up"]
                ])
