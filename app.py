import streamlit as st
import pandas as pd

# වෙබ් පිටුවේ ප්‍රධාන සැකසුම් (Title & Icon)
st.set_page_config(page_title="AP NOTES Platform", page_icon="📚", layout="centered")

# --- DATABASE එකක් වෙනුවට තාවකාලික මතකය (Session State) ---
if "notes_db" not in st.st._session_state if hasattr(st, "_session_state") else st.session_state:
    st.session_state["notes_db"] = [
        {
            "subject": "Physics",
            "topic": "යාන්ත්‍ර විද්‍යාව (Mechanics)",
            "channel": "AP | Note's 2027",
            "file_name": "mechanics_short_note.pdf"
        },
        {
            "subject": "Chemistry",
            "topic": "රසායනික ගණනය කිරීම් (Stoichiometry)",
            "channel": "Chem Short Notes",
            "file_name": "stoichiometry_v1.pdf"
        }
    ]

# --- HEADER SECTION ---
st.title("📚 AP NOTES වේදිකාව")
st.write("ලංකාවේ විශිෂ්ටතම Telegram Notes එක තැනකින් ලබාගන්න.")
st.markdown("---")

# --- SIDEBAR (Notes ඇතුළත් කිරීමේ කොටස - Admins සඳහා) ---
st.sidebar.header("➕ Admin Access (Notes ඇතුළත් කරන්න)")
st.sidebar.write("ඔයාගේ Telegram Channel එකේ Notes මෙතනින් ප්ලැට්ෆෝම් එකට එකතු කරන්න.")

with st.sidebar.form(key="upload_form", clear_on_submit=True):
    subject = st.selectbox("විෂය තෝරන්න:", ["Physics", "Chemistry", "Combined Maths"])
    topic = st.text_input("Notes වල මාතෘකාව (Topic):", placeholder="උදා: ප්‍රක්ෂිප්ත චලිතය")
    channel_name = st.text_input("ඔයාගේ Telegram Channel නම:", placeholder="උදා: AP Notes 2027")
    uploaded_file = st.file_uploader("Note එක Upload කරන්න (PDF / Image):", type=["pdf", "png", "jpg", "jpeg"])
    
    submit_button = st.form_submit_button(label="Platform එකට ඇතුළත් කරන්න 🚀")

# Form එක Submit කළාම Data ටික Save කරගන්නා ආකාරය
if submit_button:
    if topic and channel_name and uploaded_file:
        new_note = {
            "subject": subject,
            "topic": topic,
            "channel": channel_name,
            "file_name": uploaded_file.name
        }
        st.session_state["notes_db"].append(new_note)
        st.sidebar.success(f"✅ {topic} Note එක සාර්ථකව ඇතුළත් කළා!")
    else:
        st.sidebar.error("❌ කරුණාකර සියලුම විස්තර සහ File එක ඇතුළත් කරන්න.")

# --- MAIN PAGE (සිසුන්ට Notes බලාගැනීමේ කොටස) ---
st.subheader("🔍 Notes සොයන්න")
search_query = st.text_input("", placeholder="විෂය හෝ මාතෘකාව Type කරන්න...")

st.markdown("### 📂 දැනට පවතින Notes එකතුව")

# Data ටික ලස්සනට Display කිරීම
for note in st.session_state["notes_db"]:
    # Search Filter එක වැඩ කරන විදිහ
    if search_query.lower() in note["subject"].lower() or search_query.lower() in note["topic"].lower():
        with st.container():
            col1, col2 = st.columns([3, 1])
            with col1:
                st.markdown(f"#### 📝 **{note['topic']}**")
                st.caption(f"📚 විෂය: {note['subject']} | 📢 Channel: **{note['channel']}**")
            with col2:
                # ෆෝන් එකෙන් ලේසියෙන්ම Download කරගන්න Button එකක්
                st.button("Download 📥", key=note["topic"]+note["channel"])
            st.markdown("---")
