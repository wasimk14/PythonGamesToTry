import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from PatientManager import PatientManager
from Visit import Visit

# Initialize patient manager
manager = PatientManager()

st.set_page_config(page_title="🏥 Hospital Management System", layout="centered")
st.title("🏥 Hospital Management System")
st.caption("Interactive Dashboard (Streamlit Version)")


# -----------------------
# Helper: Load patient data
# -----------------------
def load_data():
    try:
        return pd.read_csv(manager.file_path)
    except FileNotFoundError:
        return pd.DataFrame()


# -----------------------
# 1️⃣ Register New Visit
# -----------------------
st.sidebar.header("Navigation")
menu = st.sidebar.radio("Go to:", ["New Visit", "Reports Dashboard", "Patient History"])

if menu == "New Visit":
    st.subheader("➕ Register New Visit")

    with st.form("visit_form"):
        name = st.text_input("Patient Name")
        guardian = st.text_input("Guardian Name")
        contact = st.text_input("Contact Number")
        address = st.text_area("Address")
        submitted = st.form_submit_button("Register Visit")

    if submitted:
        if not name or not contact:
            st.warning("⚠️ Name and contact number are required.")
        else:
            patients = manager.load()
            existing = manager.find_patient(patients, name, contact)

            if existing:
                patient_id = existing["patient_id"]
                visit_number = int(existing["visit_number"]) + 1
                follow_up = "Yes"
                st.info(f"Returning patient — ID: {patient_id}")
            else:
                patient_id = manager.generate_patient_id(patients)
                visit_number = 1
                follow_up = "No"
                st.success(f"New patient registered — ID: {patient_id}")

            # Simulate visit
            consultation = st.selectbox(
                "Consultation Type",
                ["General Checkup", "Pediatrics", "Dermatology", "Cardiology", "Orthopedic"]
            )

            fees = {
                "General Checkup": 300,
                "Pediatrics": 500,
                "Dermatology": 700,
                "Cardiology": 1000,
                "Orthopedic": 800
            }

            department = st.selectbox(
                "Department",
                ["General Medicine", "Pediatrics", "Dermatology", "Cardiology", "Orthopedics"]
            )

            doctor = st.selectbox(
                "Doctor",
                ["Dr. R. Kumar", "Dr. Anita Singh", "Dr. Patel", "Dr. Naik"]
            )

            payment_mode = st.radio("Payment Mode", ["Cash", "Card", "UPI"])

            total_fee = fees.get(consultation, 0)

            if st.button("Save Visit"):
                invoice_id = manager.generate_invoice_id(patients)
                visit_datetime = datetime.now().strftime("%Y-%m-%d %H:%M")

                new_record = {
                    "invoice_id": invoice_id,
                    "patient_id": patient_id,
                    "name": name,
                    "guardian_name": guardian,
                    "contact_number": contact,
                    "address": address,
                    "consultation": consultation,
                    "department": department,
                    "doctor": doctor,
                    "payment_mode": payment_mode,
                    "visit_datetime": visit_datetime,
                    "visit_number": visit_number,
                    "follow_up": follow_up,
                    "total_fee": total_fee
                }

                df = load_data()
                df = pd.concat([df, pd.DataFrame([new_record])], ignore_index=True)
                df.to_csv(manager.file_path, index=False)

                st.success(f"✅ Visit saved successfully! Total: ₹{total_fee}")
                st.write(new_record)


# -----------------------
# 2️⃣ Reports Dashboard
# -----------------------
elif menu == "Reports Dashboard":
    st.subheader("📊 Reports Dashboard")

    df = load_data()
    if df.empty:
        st.warning("No records found yet.")
    else:
        df["visit_date"] = pd.to_datetime(df["visit_datetime"]).dt.date
        df["visit_month"] = pd.to_datetime(df["visit_datetime"]).dt.to_period("M")

        report_type = st.radio("Select Report Type", ["Daily", "Weekly", "Monthly"])

        if report_type == "Daily":
            today = datetime.now().date()
            daily_df = df[df["visit_date"] == today]
            st.markdown(f"**🗓️ Daily Report – {today}**")
            if daily_df.empty:
                st.info("No visits today.")
            else:
                st.dataframe(daily_df[["invoice_id", "name", "consultation", "doctor", "total_fee"]])
                st.metric("Total Visits", len(daily_df))
                st.metric("Total Revenue", f"₹{daily_df['total_fee'].sum()}")

        elif report_type == "Weekly":
            today = datetime.now().date()
            week_start = today - timedelta(days=6)
            week_df = df[(df["visit_date"] >= week_start) & (df["visit_date"] <= today)]
            st.markdown(f"**📅 Weekly Report ({week_start} → {today})**")
            if week_df.empty:
                st.info("No visits this week.")
            else:
                summary = week_df.groupby("visit_date")["total_fee"].agg(["count", "sum"]).reset_index()
                summary.columns = ["Date", "Visits", "Revenue"]
                st.dataframe(summary)
                st.metric("Total Visits", summary["Visits"].sum())
                st.metric("Total Revenue", f"₹{summary['Revenue'].sum()}")

        elif report_type == "Monthly":
            month_df = df.groupby("visit_month")["total_fee"].agg(["count", "sum"]).reset_index()
            month_df.columns = ["Month", "Visits", "Revenue"]
            st.markdown("**🧾 Monthly Summary**")
            st.dataframe(month_df)
            st.metric("Total Visits", month_df["Visits"].sum())
            st.metric("Total Revenue", f"₹{month_df['Revenue'].sum()}")


# -----------------------
# 3️⃣ View Patient History
# -----------------------
elif menu == "Patient History":
    st.subheader("📖 View Patient History")

    name = st.text_input("Patient Name")
    contact = st.text_input("Contact Number")

    if st.button("Search"):
        df = load_data()
        if df.empty:
            st.warning("No patient records found.")
        else:
            records = df[
                (df["name"].str.lower() == name.lower())
                & (df["contact_number"].astype(str) == contact)
            ]
            if records.empty:
                st.info("No records found for this patient.")
            else:
                st.dataframe(records[
                    ["invoice_id", "visit_datetime", "consultation", "doctor", "total_fee", "follow_up"]
                ])
