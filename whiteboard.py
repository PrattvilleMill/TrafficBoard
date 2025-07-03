import streamlit as st

st.set_page_config(layout="wide")
st.title("🚚 Prattville Mill Railcar Dashboard")

# Section names for each tab
enroute_sections = [
    "Caustic",
    "Soap",
    "Tall Oil",
    "Acid",
    "Waste",
    "Sodium Hydrosulfide",
    "Turpentine"
]
yard_sections = enroute_sections + ["Empty Tanks"]
mill_sections = [
    "1. Acid",
    "1A. Acid",
    "2. Soap",
    "2A. Tall Oil",
    "2B. Tall Oil",
    "3. PowerHouse",
    "4A. Turpentine",
    "4B. Soap",
    "6A. NaHS",
    "6B. Caustic",
    "7. Caustic",
    "7A. Caustic",
    "7B. Caustic",
    "8. PaperMill Acid",
    "9W. Waste"
]

section_choices = {
    "Enroute": enroute_sections,
    "Holding Yard": yard_sections,
    "In Mill": mill_sections
}

# Session state reset for migration (REMOVE after one run if upgrading)
for k, sections in zip(["enroute", "yard", "mill"], [enroute_sections, yard_sections, mill_sections]):
    if k in st.session_state and not isinstance(st.session_state[k], dict):
        del st.session_state[k]

# Initialize session state for each category and section
if "enroute" not in st.session_state:
    st.session_state["enroute"] = {section: [] for section in enroute_sections}
if "yard" not in st.session_state:
    st.session_state["yard"] = {section: [] for section in yard_sections}
if "mill" not in st.session_state:
    st.session_state["mill"] = {section: [] for section in mill_sections}

# Input form
st.markdown("### ➕ Add New Railcar Entry")

with st.form("new_entry_form"):
    railcar_id = st.text_input("Enter Railcar ID:")
    supplier = st.text_input("Enter Supplier:")
    carrier = st.text_input("Enter Carrier:")
    category = st.selectbox("Select location:", ["Enroute", "Holding Yard", "In Mill"])
    section = st.selectbox("Select section:", section_choices[category])
    submitted = st.form_submit_button("Add")

    if submitted and railcar_id and section:
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
            st.session_state.mill[section].append(entry)

tab1, tab2, tab3 = st.tabs(["🟦 Enroute", "🟨 Holding Yard", "🟩 In Mill"])

def display_entries(entries, color, current_tab, current_section):
    color_map = {
        "success": "#dff0d8",
        "warning": "#fcf8e3",
        "info":    "#d9edf7"
    }
    border_map = {
        "success": "#3c763d",
        "warning": "#8a6d3b",
        "info":    "#31708f"
    }
    bg_color = color_map[color]
    border_color = border_map[color]
    for idx, entry in enumerate(entries):
        with st.container():
            st.markdown(
                f"""
                <div style='background-color:{bg_color};border-left:8px solid {border_color};padding:1em 1em 0.8em 1em;border-radius:6px; margin-bottom: 0.5em;'>
                    <span style='font-size:1.2em; font-weight:bold;'>🚆 {entry['railcar_id']}</span><br>
                    <span style='font-size:0.9em; color: #444;'>
                        Supplier: {entry['supplier']}<br>
                        Carrier: {entry['carrier']}
                    </span>
                </div>
                """,
                unsafe_allow_html=True
            )
            with st.expander("Move this entry"):
                # Select destination tab
                dest_tab = st.selectbox(
                    "Destination tab",
                    ["Enroute", "Holding Yard", "In Mill"],
                    key=f"move_tab_{current_tab}_{current_section}_{idx}"
                )
                # Select section according to chosen tab
                dest_section = st.selectbox(
                    "Destination section",
                    section_choices[dest_tab],
                    key=f"move_sec_{current_tab}_{current_section}_{idx}"
                )
                if st.button("Confirm Move", key=f"confirm_move_{current_tab}_{current_section}_{idx}"):
                    # Remove from current
                    entries.pop(idx)
                    # Add to new
                    if dest_tab == "Enroute":
                        st.session_state.enroute[dest_section].append(entry)
                    elif dest_tab == "Holding Yard":
                        st.session_state.yard[dest_section].append(entry)
                    elif dest_tab == "In Mill":
                        st.session_state.mill[dest_section].append(entry)
                    st.rerun()

with tab1:
    for section in enroute_sections:
        st.subheader(section)
        display_entries(st.session_state.enroute[section], "success", "enroute", section)

with tab2:
    for section in yard_sections:
        st.subheader(section)
        display_entries(st.session_state.yard[section], "warning", "yard", section)

with tab3:
    for section in mill_sections:
        st.subheader(section)
        display_entries(st.session_state.mill[section], "info", "mill", section)
