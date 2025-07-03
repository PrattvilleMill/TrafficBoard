import streamlit as st

st.set_page_config(layout="wide")
st.title("📝 Whiteboard Interface")

if "notes" not in st.session_state:
    st.session_state.notes = []

new_note = st.text_input("Enter your note:")
if st.button("Add Note") and new_note:
    st.session_state.notes.append(new_note)

st.markdown("### 🧠 Your Whiteboard Notes")
for i, note in enumerate(st.session_state.notes):
    st.write(f"📌 {i+1}. {note}")
