import streamlit as st

st.set_page_config(layout="wide")
st.title("🚚 Prattville Mill Railcar Dashboard")

# Initialize session state for each column
for key in ["enroute", "yard", "mill"]:
    if key not in st.session_state:
        st.session_state[key] = []

# Input form
st.markdown("### ➕ Add New Railcar Entry")

with st.form("new_entry_form"):
    railcar_id = st.text_input("Enter Railcar ID:")
    supplier = st.text_input("Enter Supplier:")
    carrier = st.text_input("Enter Carrier:")
    category = st.selectbox("Select location:", ["Enroute", "Holding Yard", "In Mill"])
    submitted = st.form_submit_button("Add")

    if submitted and railcar_id:
        entry = {
            "railcar_id": railcar_id.strip(),
            "supplier": supplier.strip(),
            "carrier": carrier.strip()
        }
        if category == "Enroute":
            st.session_state.enroute.append(entry)
        elif category == "Holding Yard":
            st.session_state.yard.append(entry)
        elif category == "In Mill":
            st.session_state.mill.append(entry)

# Display in 3 columns
col1, col2, col3 = st.columns(3)

def display_entries(entries, color_func):
    for entry in entries:
        with st.container():
            color_func(f"🚆 {entry['railcar_id']}")
            st.markdown(f"**Supplier**: {entry['supplier']}  \n**Carrier**: {entry['carrier']}")

with col1:
    st.header("🟦 Enroute")
    display_entries(st.session_state.enroute, st.success)

with col2:
    st.header("🟨 Holding Yard")
    display_entries(st.session_state.yard, st.warning)

with col3:
    st.header("🟩 Mill Loading/Unloading")
    display_entries(st.session_state.mill, st.info)
