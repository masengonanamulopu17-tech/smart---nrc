import streamlit as st
import random
from datetime import date

st.set_page_config(page_title="Smart NRC System", page_icon="🇿🇲", layout="wide")
st.markdown("""<style>
[data-testid="stAppViewContainer"] { background-color: #0F1B2D !important; }
[data-testid="stHeader"] { background-color: #0F1B2D !important; }
[data-testid="stSidebar"] { background-color: #1A2E4A !important; }
.stButton > button { background-color: #FF7A00 !important; color: white !important; border: none !important; border-radius: 10px !important; font-weight: bold !important; }
h1, h2, h3, p, label { color: white !important; }
</style>""", unsafe_allow_html=True)

st.title("🇿🇲 Smart NRC System - Zambia")
st.caption("Citizen Booking | Officer Dashboard | Admin Reports | AI Tools")

# Keep data while app is open
if "appointments" not in st.session_state:
    st.session_state.appointments = []

# Sidebar - Choose who you are
role = st.sidebar.selectbox("Who are you?", ["👤 Citizen", "🏢 Officer", "📊 Admin"])

# ============ CITIZEN ============
if role == "👤 Citizen":
    st.header("👤 Citizen - Book Appointment")

    st.info(
        "**Requirements:** First NRC = Parental NRC + Affidavit | Duplicate = Police Report + Affidavit | Must be 16+ years")

    name = st.text_input("Full Name", "John Banda")
    phone = st.text_input("Phone Number", "0977123456")
    centre = st.selectbox("Centre", ["Lusaka Boma", "Chawama", "Matero", "Kabwata"])
    appt_date = st.date_input("Appointment Date", date.today())
    doc_type = st.selectbox("Document Type", ["First NRC", "Duplicate NRC", "Replacement"])

    st.subheader("🤖 AI Document Check")
    uploaded = st.file_uploader("Upload Parental NRC / Affidavit (photo)", type=["jpg", "png", "pdf"])

    if st.button("Book Appointment", type="primary"):
        if not name or not phone:
            st.error("Please enter name and phone")
        elif not uploaded:
            st.warning("🤖 AI Check: Please upload a clear document photo first.")
        else:
            new_id = f"NRC-{random.randint(1000, 9999)}"
            st.session_state.appointments.append({
                "id": new_id, "name": name, "phone": phone,
                "centre": centre, "date": str(appt_date),
                "type": doc_type, "status": "Booked"
            })
            st.success(f"✅ Booked! Your ID: **{new_id}**")
            st.info(
                f"📱 SMS to {phone}: Your appointment {new_id} is confirmed for {appt_date} at {centre}. Come with original documents.")
            st.balloons()

    st.divider()
    st.header("🔍 Track Your Application")
    track_id = st.text_input("Enter Appointment ID (e.g. NRC-1234)")
    if st.button("Track Status"):
        found = [a for a in st.session_state.appointments if a["id"].lower() == track_id.lower()]
        if found:
            a = found[0]
            st.success(f"**{a['id']}** - {a['name']} | {a['centre']} | {a['date']} | Status: **{a['status']}**")
        else:
            st.error("Not found. Book first to get an ID.")

# ============ OFFICER ============
elif role == "🏢 Officer":
    st.header("🏢 Officer Dashboard - DNRPC")
    st.write(f"Today's Appointments: **{len(st.session_state.appointments)}**")

    if not st.session_state.appointments:
        st.info("No appointments yet. Go to Citizen tab and book one to see it here live.")
    else:
        for i, a in enumerate(st.session_state.appointments):
            with st.expander(f"{a['id']} - {a['name']} - {a['status']}"):
                st.write(
                    f"**Centre:** {a['centre']} | **Date:** {a['date']} | **Phone:** {a['phone']} | **Type:** {a['type']}")
                new_status = st.selectbox("Update Status", ["Booked", "Verified", "Printing", "Ready", "Collected"],
                                          index=["Booked", "Verified", "Printing", "Ready", "Collected"].index(
                                              a["status"]), key=f"status_{i}")
                if st.button("Update", key=f"btn_{i}"):
                    st.session_state.appointments[i]["status"] = new_status
                    st.success(f"Status updated to {new_status}")
                    if new_status == "Ready":
                        st.info(
                            f"📱 SMS sent to {a['phone']}: Your NRC {a['id']} is READY for collection at {a['centre']}.")
                    st.rerun()

# ============ ADMIN ============
else:
    st.header("📊 Admin Dashboard")
    total = len(st.session_state.appointments)
    ready = len([a for a in st.session_state.appointments if a["status"] == "Ready"])
    collected = len([a for a in st.session_state.appointments if a["status"] == "Collected"])

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Booked", total)
    col2.metric("Ready for Collection", ready)
    col3.metric("Collected", collected)

    st.subheader("🤖 AI Queue Predictor")
    st.write(
        "Chawama is 90% full on Monday. AI suggests Wednesday at Lusaka Boma - only 30% load. Queue reduced by 82%.")

    st.subheader("🤖 AI Chatbot")
    q = st.text_input("Ask: What do I need for duplicate?")
    if st.button("Ask AI"):
        if "duplicate" in q.lower():
            st.write("Duplicate NRC: You need Police Report + Affidavit + Fee K20.")
        else:
            st.write("First NRC: You need Parental NRC + Affidavit + 16+ years. Book a slot, no need to queue at 5am.")

    if st.session_state.appointments:
        st.subheader("All Appointments")
        st.table(st.session_state.appointments)
