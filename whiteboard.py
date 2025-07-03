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
    category = st.selectbox("Select location:", ["Enroute", "Holding Yard", "Mill Loading/Unloading"])
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
        elif category == "Mill Loading/Unloading":
            st.session_state.mill.append(entry)

# Function to handle moving entries
def move_entry(source_list, entry_index, target_list_name):
    entry = source_list.pop(entry_index)
    st.session_state[target_list_name].append(entry)

# Function to display entries with move options
def display_entries(entries, list_name):
    for i, entry in enumerate(entries):
        with st.container():
            st.markdown(f"🚆 **{entry['railcar_id']}**")
            st.markdown(f"**Supplier**: {entry['supplier']}  \n**Carrier**: {entry['carrier']}")
            col1, col2 = st.columns([3, 1])
            with col1:
                target = st.selectbox(
                    "Move to:", 
                    ["-- Select --", "Enroute", "Holding Yard", "Mill Loading/Unloading"], 
                    key=f"{list_name}_{i}_move"
                )
            with col2:
                if st.button("Move", key=f"{list_name}_{i}_btn") and target != "-- Select --" and target != list_name:
                    move_entry(
                        st.session_state[list_name],
                        i,
                        {"Enroute": "enroute", "Holding Yard": "yard", "Mill Loading/Unloading": "mill"}[target]
                    )
                    st.experimental_rerun()

# Columns for each section
col1, col2, col3 = st.columns(3)

with col1:
    st.header("🟦 Enroute")
    display_entries(st.session_state.enroute, "enroute")

with col2:
    st.header("🟨 Holding Yard")
    display_entries(st.session_state.yard, "yard")

with col3:
    st.header("🟩 Mill Loading/Unloading")
    display_entries(st.session_state.mill, "mill")
