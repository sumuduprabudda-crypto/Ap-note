import streamlit as st
import pandas as pd

# වෙබ් පිටුවේ ප්‍රධාන සැකසුම්
st.set_page_config(page_title="AP NOTES Platform", page_icon="📚", layout="centered")

# --- GOOGLE SHEET DATABASE CONNECT ---
# ⚠️ ඔයා කොපි කරපු Google Sheet ලින්ක් එක පල්ලෙහා තියෙන උඩු කමා ඇතුළට දාන්න:
sheet_url = "https://docs.google.com/spreadsheets/d/1spGvOt_0R70ygPRjMDNryeEdK8JzcJdUk9U0OWZo_rA/edit?usp=drivesdk"

# Google Sheet එක csv එකක් විදිහට කියවන්න ලින්ක් එක සකස් කිරීම
if "docs.google.com" in sheet_url:
    csv_url = sheet_url.replace("/edit?usp=sharing", "/gviz/tq?tqx=out:csv").replace("/edit#gid=", "/gviz/tq?tqx=out:csv&gid=").replace("/edit?usp=drivesdk", "/gviz/tq?tqx=out:csv")
else:
    csv_url = None

# Google Sheet එකේ තියෙන ඩේටා කියවීම
def load_data():
    if csv_url:
        try:
            return pd.read_csv(csv_url)
        except:
            return pd.DataFrame(columns=["Subject", "Topic", "Channel", "URL"])
    return pd.DataFrame(columns=["Subject", "Topic", "Channel", "URL"])

df = load_data()

# --- HEADER SECTION ---
st.title("📚 AP NOTES වේදිකාව")
st.write("ලංකාවේ විශිෂ්ටතම Telegram Notes එක තැනකින් ලබාගන්න.")
st.markdown("---")

# --- SIDEBAR (Owner වන ඔයාට විතරක් Notes දාන්න) ---
st.sidebar.header("👑 Owner Dashboard")
st.sidebar.write("ඔයාගේ අලුත් Notes ප්ලැට්ෆෝම් එකට එකතු කරන්න.")

# සරල Password ආරක්ෂාවක් (වෙන අය නෝට්ස් දාන එක නවත්තන්න)
password = st.sidebar.text_input("Owner Password එක ඇතුළත් කරන්න:", type="password")

if password == "ap123": # 👈 ඔයාට ඕන නම් මේ password එක වෙනස් කරන්න පුළුවන්
    st.sidebar.success("🔒 Owner Access Granted!")
    with st.sidebar.form(key="upload_form", clear_on_submit=True):
        subject = st.selectbox("විෂය:", ["Physics", "Chemistry", "Combined Maths"])
        topic = st.text_input("Notes වල මාතෘකාව (Topic):", placeholder="උදා: ප්‍රක්ෂිප්ත චලිතය")
        note_link = st.text_input("Note එකේ ලින්ක් එක (Drive/Telegram Link):")
        
        submit_button = st.form_submit_button(label="Platform එකට දාන්න 🚀")

    if submit_button:
        if topic and note_link:
            st.sidebar.success("✅ නෝට් එකේ විස්තර සූදානම්!")
            st.sidebar.info("💡 පල්ලෙහා බටන් එක ඔබලා විස්තර ටික Sheet එකට ඇතුළත් කරන්න.")
            
            # Google Sheet එකට කෙලින්ම Data දාන්න ලින්ක් එක දීම
            st.sidebar.markdown(f"[🔗 මෙතන ක්ලික් කර Sheet එකට Data දාන්න]({sheet_url})")
        else:
            st.sidebar.error("❌ කරුණාකර සියලු විස්තර පුරවන්න.")
else:
    st.sidebar.warning("🔒 Notes ඇතුළත් කිරීමට නිවැරදි Password එක ගහන්න.")

# --- MAIN PAGE (සිසුන්ට Notes බලාගැනීම) ---
st.subheader("🔍 Notes සොයන්න")
search_query = st.text_input("", placeholder="විෂය හෝ මාතෘකාව Type කරන්න...")

st.markdown("### 📂 දැනට පවතින Notes එකතුව")

# Sheet එකේ තියෙන Data ටික ප්ලැට්ෆෝම් එකට ලෝඩ් කිරීම
if not df.empty and "Topic" in df.columns:
    for index, row in df.iterrows():
        if pd.isna(row['Topic']):
            continue
            
        # සෙවුම් පෙරහන (Search Filter)
        if search_query.lower() in str(row["Subject"]).lower() or search_query.lower() in str(row["Topic"]).lower():
            with st.container():
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.markdown(f"#### 📝 {row['Topic']}")
                    st.caption(f"📚 විෂය: {row['Subject']} | 📢 Channel: {row['Channel']}")
                with col2:
                    st.markdown(f"[<button style='padding:8px; background-color:#FF4B4B; color:white; border:none; border-radius:5px; cursor:pointer;'>Download 📥</button>]({row['URL']})", unsafe_allow_html=True)
                st.markdown("---")
else:
    st.info("📂 තාම නෝට්ස් මුකුත් එකතු කරලා නැහැ. Google Sheet එකට නෝට් එකක් එකතු කරලා සයිට් එක Refresh කරන්න.")
