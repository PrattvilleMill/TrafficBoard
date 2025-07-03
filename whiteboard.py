import streamlit as st

st.set_page_config(layout="wide")
st.title("🚚 Live Whiteboard Dashboard")

# Initialize session state for each column
for key in ["enroute", "yard", "mill"]:
    if key not in st.session_state:
        st.session_state[key] = []

# Input section
st.markdown("### ➕ Add New Entry")

with st.form("new_entry_form"):
    new_note = st.text_input("Enter a note:")
    category = st.selectbox("Select location:", ["Enroute", "Holding Yard", "Mill Loading/Unloading"])
    submitted = st.form_submit_button("Add")

    if submitted and new_note:
        if category == "Enroute":
            st.session_state.enroute.append(new_note)
        elif category == "Holding Yard":
            st.session_state.yard.append(new_note)
        elif category == "Mill Loading/Unloading":
            st.session_state.mill.append(new_note)

# Create three vertical columns
col1, col2, col3 = st.columns(3)

with col1:
    st.header("🟦 Enroute")
    for note in st.session_state.enroute:
        st.success(note)

with col2:
    st.header("🟨 Holding Yard")
    for note in st.session_state.yard:
        st.warning(note)

with col3:
    st.header("🟩 Mill Loading/Unloading")
    for note in st.session_state.mill:
        st.info(note)
