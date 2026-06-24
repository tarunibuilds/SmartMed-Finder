import streamlit as st
import pandas as pd
import numpy as np
import time
import uuid
from utils.search import SearchEngine
from datetime import date

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(page_title="Hospital IR System", layout="wide")

# =========================
# PREMIUM UI
# =========================
st.markdown("""
<style>
body {background: #0f172a; color: white;}

.card {
    padding:20px;
    border-radius:18px;
    background: rgba(255,255,255,0.04);
    margin-bottom:20px;
    border:1px solid rgba(255,255,255,0.08);
    backdrop-filter: blur(12px);
    box-shadow:0 6px 20px rgba(0,0,0,0.4);
    transition:0.3s;
}
.card:hover {
    transform: translateY(-4px) scale(1.01);
}

.stButton>button {
    border-radius:12px;
    background: linear-gradient(45deg,#6366f1,#22c55e);
    color:white;
    font-weight:600;
}

</style>
""", unsafe_allow_html=True)

st.title("🏥 Hospital Information Retrieval System")

# =========================
# LOAD DATA
# =========================
@st.cache_data
def load_data():
    return pd.read_excel("dataset/improved_hospital_ir_dataset.xlsx")

df = load_data()
search_engine = SearchEngine(df)

# =========================
# SESSION STATE
# =========================
if "results" not in st.session_state:
    st.session_state["results"] = None

if "appointments" not in st.session_state:
    st.session_state["appointments"] = []

if "notifications" not in st.session_state:
    st.session_state["notifications"] = []

if "booking_step" not in st.session_state:
    st.session_state["booking_step"] = 0

if "selected_doctor" not in st.session_state:
    st.session_state["selected_doctor"] = None

# =========================
# SIDEBAR
# =========================
st.sidebar.header("🔍 Filters")

location_filter = st.sidebar.selectbox("Location", ["All"] + sorted(df["location"].unique()))
spec_filter = st.sidebar.selectbox("Specialization", ["All"] + sorted(df["specialization"].unique()))
availability_filter = st.sidebar.selectbox("Availability", ["All", "Available", "Busy"])

# 🔔 Notifications
st.sidebar.markdown("### 🔔 Notifications")
for note in st.session_state["notifications"][-5:]:
    st.sidebar.success(note)

# =========================
# SEARCH
# =========================
query = st.text_input("🔍 Search doctors, symptoms...")
search_type = st.radio("Search Type", ["TF-IDF Search", "Boolean Search"])

if st.button("Search") and query:

    with st.spinner("🔍 Searching..."):
        time.sleep(1)

        if search_type == "TF-IDF Search":
            results = search_engine.tfidf_search(query)
        else:
            results = search_engine.boolean_search(query)

    # Apply filters
    if location_filter != "All":
        results = results[results["location"] == location_filter]

    if spec_filter != "All":
        results = results[results["specialization"] == spec_filter]

    if availability_filter != "All":
        results = results[results["availability"] == availability_filter]

    results = results.reset_index(drop=True)

    st.session_state["results"] = results
    st.session_state["booking_step"] = 0

# =========================
# MAP + TOP DOCTORS
# =========================
if st.session_state["results"] is not None:

    results = st.session_state["results"]

    if not results.empty:

        # 🗺️ MAP
        st.subheader("🗺️ Hospital Locations")

        city_coords = {
            "Bangalore": (12.9716, 77.5946),
            "Hyderabad": (17.3850, 78.4867),
            "Chennai": (13.0827, 80.2707),
            "Mumbai": (19.0760, 72.8777),
            "Delhi": (28.7041, 77.1025)
        }

        map_df = results.copy()

        map_df["lat"] = map_df["location"].apply(lambda x: city_coords.get(x, (12.97, 77.59))[0])
        map_df["lon"] = map_df["location"].apply(lambda x: city_coords.get(x, (12.97, 77.59))[1])

        # jitter fix
        map_df["lat"] += np.random.uniform(-0.005, 0.005, len(map_df))
        map_df["lon"] += np.random.uniform(-0.005, 0.005, len(map_df))

        st.map(map_df[["lat", "lon"]])

        # ⭐ TOP DOCTORS (FIXED)
        st.subheader("⭐ Top Rated Doctors")

        top_docs = results.sort_values(by="rating", ascending=False).head(5)

        cols = st.columns(len(top_docs))

        for i, (_, doc) in enumerate(top_docs.iterrows()):
            with cols[i]:
                st.markdown('<div class="card">', unsafe_allow_html=True)
                st.write(f"👨‍⚕️ {doc['name']}")
                st.write(f"⭐ {doc['rating']}")
                st.write(doc["specialization"])
                st.write(doc["location"])

                if st.button("Book", key=f"top_{doc['doctor_id']}"):
                    st.session_state["selected_doctor"] = doc
                    st.session_state["booking_step"] = 1
                    st.rerun()

                st.markdown('</div>', unsafe_allow_html=True)

# =========================
# STEP 0 → RESULTS
# =========================
if st.session_state["results"] is not None and st.session_state["booking_step"] == 0:

    results = st.session_state["results"]

    if results.empty:
        st.error("❌ No results found")
    else:
        st.subheader(f"🔎 Showing {len(results)} results")

        for _, row in results.iterrows():

            st.markdown('<div class="card">', unsafe_allow_html=True)

            st.markdown(f"### 👨‍⚕️ {row['name']}")
            st.write(f"{row['specialization']} | {row['hospital']} ({row['location']})")
            st.write(f"⭐ {row['rating']} | {row['experience']} yrs | ₹{row['fees']}")
            st.write(f"📝 {row['description']}")

            if st.button("📅 Book Appointment", key=f"book_{row['doctor_id']}"):
                st.session_state["selected_doctor"] = row
                st.session_state["booking_step"] = 1
                st.rerun()

            st.markdown('</div>', unsafe_allow_html=True)

# =========================
# STEP 1 → BOOKING
# =========================
if st.session_state["booking_step"] == 1:

    doc = st.session_state["selected_doctor"]

    st.subheader("📅 Book Appointment")

    st.markdown('<div class="card">', unsafe_allow_html=True)

    st.write(f"👨‍⚕️ {doc['name']}")
    st.write(f"🏥 {doc['hospital']} ({doc['location']})")

    selected_date = st.date_input("Select Date", min_value=date.today())
    slot = st.selectbox("Select Time Slot", ["10 AM", "12 PM", "3 PM", "6 PM"])
    consult = st.radio("Consultation Mode", ["Online", "Offline"])

    col1, col2 = st.columns(2)

    if col1.button("➡️ Proceed to Payment"):
        st.session_state["slot"] = slot
        st.session_state["consult"] = consult
        st.session_state["date"] = selected_date
        st.session_state["booking_step"] = 2
        st.rerun()

    if col2.button("❌ Cancel"):
        st.session_state["booking_step"] = 0
        st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

# =========================
# STEP 2 → PAYMENT
# =========================
if st.session_state["booking_step"] == 2:

    doc = st.session_state["selected_doctor"]

    st.subheader("💳 Payment")

    st.markdown('<div class="card">', unsafe_allow_html=True)

    st.write(f"Doctor: {doc['name']}")
    st.write(f"Fees: ₹{doc['fees']}")
    st.write(f"Date: {st.session_state['date']}")
    st.write(f"Slot: {st.session_state['slot']}")
    st.write(f"Mode: {st.session_state['consult']}")

    col1, col2 = st.columns(2)

    if col1.button("💳 Pay Now"):

        appointment = {
            "id": str(uuid.uuid4())[:8],
            "doctor": doc["name"],
            "hospital": doc["hospital"],
            "location": doc["location"],
            "date": str(st.session_state["date"]),
            "slot": st.session_state["slot"],
            "consult": st.session_state["consult"],
            "status": "Confirmed"
        }

        st.session_state["appointments"].append(appointment)
        st.session_state["notifications"].append(
            f"Appointment confirmed with {appointment['doctor']}"
        )

        st.session_state["booking_step"] = 0
        st.success("✅ Payment Successful & Appointment Booked!")

        st.rerun()

    if col2.button("⬅ Back"):
        st.session_state["booking_step"] = 1
        st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

# =========================
# APPOINTMENTS
# =========================
st.subheader("📋 My Appointments")

if len(st.session_state["appointments"]) == 0:
    st.info("No appointments yet")
else:
    for i, appt in enumerate(st.session_state["appointments"]):

        st.markdown('<div class="card">', unsafe_allow_html=True)

        st.write(f"👨‍⚕️ {appt['doctor']}")
        st.write(f"🏥 {appt['hospital']} ({appt['location']})")
        st.write(f"📅 {appt['date']} | ⏰ {appt['slot']}")
        st.write(f"💻 {appt['consult']} | ✅ {appt['status']}")

        if st.button("❌ Cancel Appointment", key=f"cancel_{appt['id']}"):
            st.session_state["appointments"].pop(i)
            st.session_state["notifications"].append("Appointment cancelled")
            st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)