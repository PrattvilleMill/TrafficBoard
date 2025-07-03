import streamlit as st

st.set_page_config(layout="wide")
st.title("🚚 Prattville Mill Railcar Dashboard")

# Section names for tabs 1 & 2
sections = [
    "Caustic",
    "Soap",
    "Tall Oil",
    "Acid",
    "Waste",
    "Sodium Hydrosulfide",
    "Turpentine"
]

# Initialize session state for each category and section
for key in ["enroute", "yard", "mill"]:
    if key not in st.session_state:
        st.session_state[key] = {section: [] for section in sections} if key != "mill" else []

# Input form
st.markdown("### ➕ Add New Railcar Entry")

with st.form("new_entry_form"):
    railcar_id = st.text_input("Enter Railcar ID:")
    supplier = st.text_input("Enter Supplier:")
    carrier = st.text_input("Enter Carrier:")
    category = st.selectbox("Select location:", ["Enroute", "Holding Yard", "In Mill"])
    section = st.selectbox("Select section:", sections) if category in ["Enroute", "Holding Yard"] else None
    submitted = st.form_submit_button("Add")

    if submitted and railcar_id:
        entry = {
            "railcar_id": railcar_id.strip(),
            "supplier": supplier.strip(),
            "carrier": carrier.strip()
        }
        if category == "Enroute":
            st.session_state.enroute[section].append(entry)
        elif category == "Holding Yard":
            st.session_state.yard[section].append(entry)
        elif category == "In Mill":
            st.session_state.mill.append(entry)

# Tabs for the 3 categories
tab1, tab2, tab3 = st.tabs(["🟦 Enroute", "🟨 Holding Yard", "🟩 In Mill"])

def display_entries(entries, color_func):
    for entry in entries:
        with st.container():
            color_func(f"🚆 {entry['railcar_id']}")
            st.markdown(f"**Supplier**: {entry['supplier']}  \n**Carrier**: {entry['carrier']}")

# Tab 1: Enroute with sections
with tab1:
    for section in sections:
        st.subheader(section)
        display_entries(st.session_state.enroute[section], st.success)

# Tab 2: Holding Yard with sections
with tab2:
    for section in sections:
        st.subheader(section)
        display_entries(st.session_state.yard[section], st.warning)

# Tab 3: In Mill (no sub-sections)
with tab3:
    display_entries(st.session_state.mill, st.info)
