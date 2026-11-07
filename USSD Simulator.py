import streamlit as st

st.set_page_config(page_title="USSD Simulator - Smart NRC", page_icon="📱")

st.title("📱 Smart NRC - USSD Simulator")
st.caption("Dial: *384*123#  |  For citizens without smartphones")

if "ussd_step" not in st.session_state:
    st.session_state.ussd_step = "main"
if "history" not in st.session_state:
    st.session_state.history = []

def go_to(next_step):
    # Save where we are, so Back can return here
    st.session_state.history.append(st.session_state.ussd_step)
    st.session_state.ussd_step = next_step
    st.rerun()

def go_back():
    if st.session_state.history:
        st.session_state.ussd_step = st.session_state.history.pop()
        st.rerun()
    else:
        st.session_state.ussd_step = "main"
        st.rerun()

def show_screen(text):
    st.markdown(f"""
    <div style="background-color:#111; color:#00FF00; padding:20px; border-radius:15px; font-family:monospace; white-space:pre-line; font-size:18px; border:3px solid #333;">
    {text}
    </div>
    """, unsafe_allow_html=True)

def back_button():
    st.write("")
    if st.button("⬅️ Back"):
        go_back()

# --- MAIN MENU ---
if st.session_state.ussd_step == "main":
    show_screen("""CON Welcome to Smart NRC
1. Book Appointment
2. Check Requirements
3. Check NRC Status
4. Cancel Appointment
0. Exit""")
    choice = st.text_input("Enter choice (0-4):", key="main_input")
    if st.button("Send ➡️"):
        if choice == "1":
            go_to("book")
        elif choice == "2":
            go_to("req")
        elif choice == "3":
            go_to("status")
        elif choice == "4":
            go_to("cancel")
        elif choice == "0":
            go_to("exit")
        else:
            st.error("Invalid choice, try 1-4")

# --- BOOK ---
elif st.session_state.ussd_step == "book":
    show_screen("""CON Choose Centre:
1. Lusaka Boma
2. Chawama
3. Matero
0. Back""")
    choice = st.text_input("Choose centre:", key="book_input")
    if st.button("Send ➡️"):
        centres = {"1": "Lusaka Boma", "2": "Chawama", "3": "Matero"}
        if choice in centres:
            st.session_state.centre = centres[choice]
            go_to("book_done")
        elif choice == "0":
            go_back()
    back_button()

elif st.session_state.ussd_step == "book_done":
    show_screen(f"""END Appointment Booked!
Centre: {st.session_state.get('centre','Lusaka Boma')}
Date: Monday 10:00hrs
Ref: NRC-2026-1234
Source: USSD - Documents Pending
Bring documents to centre.
SMS sent to your phone.""")
    if st.button("Dial Again *384*123#"):
        st.session_state.history = []
        st.session_state.ussd_step = "main"
        st.rerun()
    back_button()

# --- REQUIREMENTS ---
elif st.session_state.ussd_step == "req":
    show_screen("""CON Requirements:
1. First NRC
2. Duplicate
3. Replacement
0. Back""")
    choice = st.text_input("Choose:", key="req_input")
    if st.button("Send ➡️"):
        if choice == "1":
            st.session_state.req_text = "First NRC: Birth Record, Parent's NRC, Affidavit, Proof of Residence"
            go_to("req_detail")
        elif choice == "2":
            st.session_state.req_text = "Duplicate: Police Report, Affidavit, Old NRC copy if available"
            go_to("req_detail")
        elif choice == "3":
            st.session_state.req_text = "Replacement: Police Report, Affidavit, K100 Fee"
            go_to("req_detail")
        elif choice == "0":
            go_back()
    back_button()

elif st.session_state.ussd_step == "req_detail":
    show_screen(f"END {st.session_state.get('req_text','')}")
    if st.button("Dial Again"):
        st.session_state.history = []
        st.session_state.ussd_step = "main"
        st.rerun()
    back_button()

# --- STATUS ---
elif st.session_state.ussd_step == "status":
    show_screen("CON Enter Reference / NRC Number:\nExample: NRC-2026-1234")
    ref = st.text_input("Reference:", key="status_input")
    if st.button("Send ➡️"):
        if ref:
            go_to("status_done")
        else:
            st.error("Enter reference number")
    back_button()

elif st.session_state.ussd_step == "status_done":
    show_screen("END Status: READY for collection\nPlease collect at Lusaka Boma with receipt.")
    if st.button("Dial Again"):
        st.session_state.history = []
        st.session_state.ussd_step = "main"
        st.rerun()
    back_button()

# --- CANCEL ---
elif st.session_state.ussd_step == "cancel":
    show_screen("CON Enter Reference to Cancel:\nExample: NRC-2026-1234")
    ref = st.text_input("Reference:", key="cancel_input")
    if st.button("Send ➡️"):
        go_to("cancel_done")
    back_button()

elif st.session_state.ussd_step == "cancel_done":
    show_screen("END Appointment Cancelled.\nDial *384*123# to book again.")
    if st.button("Dial Again"):
        st.session_state.history = []
        st.session_state.ussd_step = "main"
        st.rerun()
    back_button()

elif st.session_state.ussd_step == "exit":
    show_screen("END Thank you for using Smart NRC. Stay Safe.")
    if st.button("Dial Again"):
        st.session_state.history = []
        st.session_state.ussd_step = "main"
        st.rerun()
    back_button()