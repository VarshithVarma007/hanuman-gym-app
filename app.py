import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import time
from datetime import datetime, date, timedelta
import os

# Set page layout configuration to wide for a sweeping dashboard layout
st.set_page_config(page_title="Hanuman Gym OS", page_icon="🏋️‍♂️", layout="wide")

# 🎨 EXCLUSIVE STEALTH DARK PREMIUM RESUME STYLING ENGINE (CSS)
stealth_ui_css = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Inter:wght@300;400;600&display=swap');
    
    /* Obsidian Base Background */
    .stApp {
        background-color: #0B0C10 !important;
        color: #C5C6C7 !important;
        font-family: 'Inter', sans-serif;
    }
    
    /* Premium Sharp Typography Headers */
    h1, h2, h3, h4 {
        font-family: 'Orbitron', sans-serif !important;
        letter-spacing: 2px;
        color: #FFFFFF !important;
        text-transform: uppercase;
    }
    
    /* Clean Minimal Slate Cards */
    .stealth-card {
        background-color: #1F2833 !important;
        border-radius: 12px !important;
        padding: 24px !important;
        margin-bottom: 20px !important;
        border-left: 4px solid #950740 !important;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4) !important;
    }
    
    /* Form Input Box Corrections */
    .stTextInput>div>div>input, .stNumberInput>div>div>input, .stSelectbox>div>div {
        background-color: #0B0C10 !important;
        color: #FFFFFF !important;
        border: 1px solid #45A29E !important;
        border-radius: 6px !important;
    }
    
    /* Minimalist Segmented Tabs Bar Layout */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: #1F2833;
        padding: 6px;
        border-radius: 10px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 40px;
        background-color: #0B0C10;
        border-radius: 6px;
        color: #C5C6C7;
        padding: 0px 18px;
        font-weight: 600;
    }
    .stTabs [aria-selected="true"] {
        background-color: #950740 !important;
        color: #FFFFFF !important;
    }
</style>
"""
st.markdown(stealth_ui_css, unsafe_allow_html=True)

# 💾 LIVE DATA DISK STORAGE CONFIGURATION LAYER
users_file = "users_db.csv"
metrics_file = "metrics_ledger.csv"
payments_file = "payments_ledger.csv"
workout_plans_file = "workout_plans_db.csv"

def init_production_databases():
    if not os.path.exists(users_file):
        pd.DataFrame([{"Username": "varshith", "Password": "admin123", "Role": "Owner"}]).to_csv(users_file, index=False)
    if not os.path.exists(metrics_file):
        pd.DataFrame(columns=["Timestamp", "Username", "Weight", "Bicep", "Chest", "Waist", "BodyFat", "Goal", "CalorieTarget", "ProteinTarget"]).to_csv(metrics_file, index=False)
    if not os.path.exists(payments_file):
        pd.DataFrame([
            {"Timestamp": "2026-06-01 10:00:00", "Username": "rahul", "Plan": "Quarterly Pack", "Amount": 4000, "Status": "Approved"},
            {"Timestamp": "2026-06-20 09:15:00", "Username": "amit", "Plan": "Iron Elite VIP", "Amount": 12000, "Status": "Pending Verification"}
        ]).to_csv(payments_file, index=False)
    if not os.path.exists(workout_plans_file):
        pd.DataFrame([
            {"Day": "Push Day", "Exercise": "Flat Barbell Bench Press", "Sets": 4, "Reps": "6-8", "Instructions": "Keep shoulder blades retracted and drive hard."},
            {"Day": "Push Day", "Exercise": "Incline Dumbbell Flys", "Sets": 3, "Reps": "10-12", "Instructions": "Focus on deep stretch at the bottom layer."},
            {"Day": "Pull Day", "Exercise": "Conventional Deadlifts", "Sets": 3, "Reps": "5", "Instructions": "Keep spine completely neutral, drive through floor."},
            {"Day": "Leg Day", "Exercise": "Barbell Back Squats", "Sets": 4, "Reps": "6-8", "Instructions": "Hit depth below parallel safely."}
        ]).to_csv(workout_plans_file, index=False)

init_production_databases()

# State Memory Vector Management
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'active_username' not in st.session_state: st.session_state.active_username = None
if 'client_calc_results' not in st.session_state: st.session_state.client_calc_results = None

# Access control handlers
def load_user_registry():
    try:
        df = pd.read_csv(users_file)
        return dict(zip(df['Username'].astype(str), df['Password'].astype(str))), dict(zip(df['Username'].astype(str), df['Role'].astype(str)))
    except:
        return {"varshith": "admin123"}, {"varshith": "Owner"}

user_pass_db, user_role_db = load_user_registry()

# 🔒 ACCESS AUTHENTICATION FRAMEWAY LOCK
if not st.session_state.logged_in:
    cols = st.columns([1, 2, 1])
    with cols[1]:
        st.markdown("<div class='stealth-card' style='margin-top: 50px;'>", unsafe_allow_html=True)
        st.markdown("<h2 style='text-align: center;'>⚡ HANUMAN MASTER INTERFACE</h2>", unsafe_allow_html=True)
        
        auth_mode = st.radio("Access Node Execution:", ["Sign In to Account", "New Client Registration"], horizontal=True)
        u_in = st.text_input("Gym Username").strip().lower()
        p_in = st.text_input("Security Access Code", type="password").strip()
        
        if auth_mode == "Sign In to Account":
            if st.button("Authorize Session Node", use_container_width=True):
                if u_in in user_pass_db and str(user_pass_db[u_in]) == p_in:
                    st.session_state.logged_in = True
                    st.session_state.active_username = u_in
                    st.rerun()
                else: st.error("Access Refused. Credentials signature invalid.")
        else:
            if st.button("Initialize Secure Account Profile", use_container_width=True):
                if u_in == "" or p_in == "": st.error("Fields cannot be committed blank.")
                elif u_in in user_pass_db: st.error("Username already exists.")
                else:
                    pd.DataFrame([{"Username": u_in, "Password": p_in, "Role": "Member"}]).to_csv(users_file, mode='a', header=False, index=False)
                    st.session_state.logged_in = True
                    st.session_state.active_username = u_in
                    st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# Master Operator Roles
is_owner = (user_role_db.get(st.session_state.active_username, "Member") == "Owner")

# 🎛️ SYSTEM COHORT DASHBOARD MATRIX SEPARATION
st.markdown(
    "<div style='text-align: center; padding: 15px 0; border-bottom: 1px solid rgba(255,255,255,0.1); margin-bottom: 25px;'>"
    "<h1>🏋️‍♂️ HANUMAN CORE CONTROL STATION</h1>"
    f"<p style='color: #45A29E; letter-spacing: 3px;'>ACTIVE LOG NODE: {st.session_state.active_username.upper()} | MANAGEMENT ACCESS ENGAGED</p>"
    "</div>", 
    unsafe_allow_html=True
)

# Render tab blocks cleanly based on user role matrix definitions
if is_owner:
    tabs = st.tabs(["👑 Operational Admin HQ", "📋 Prescribed Workout Routines", "🍳 Dynamic Client Diagnostics Ledger", "💳 Financial Liquidity Hub"])
else:
    tabs = st.tabs(["📋 My Prescribed Workouts", "🍳 Biometric Assessment Engine", "📅 Personal Progress Tracker", "💳 Gateway Payment Station"])

# =========================================================================================
# OWNER ROUTE CHANNELS (OWNER WORKSTATION VIEW)
# =========================================================================================
if is_owner:
    # ADMIN TAB 1: OPERATIONAL ADMIN HQ
    with tabs[0]:
        st.markdown("<div class='stealth-card'>", unsafe_allow_html=True)
        st.markdown("### 👑 Master Client Roster & Operational Biometrics")
        st.write("Drill down into any active user profile to monitor their complete telemetry trail.")
        
        try:
            metrics_df = pd.read_csv(metrics_file)
            all_users = metrics_df['Username'].unique().tolist()
            
            if all_users:
                selected_client = st.selectbox("Select Active Client Account to Audit:", all_users)
                client_history = metrics_df[metrics_df['Username'] == selected_client].sort_values(by="Timestamp", ascending=False)
                
                st.write(f"#### Biometric Records History Ledger: `{selected_client.upper()}`")
                st.dataframe(client_history, use_container_width=True)
                
                if len(client_history) > 1:
                    st.write("#### 📈 Continuous Weight Progression Velocity Trend")
                    weight_chart = alt.Chart(client_history).mark_line(point=True, color='#950740').encode(
                        x=alt.X('Timestamp:T', title='Timeline Horizon Log Entry'),
                        y=alt.Y('Weight:Q', title='Body Mass Scale (kg)', scale=alt.Scale(zero=False))
                    ).properties(height=250)
                    st.altair_chart(weight_chart, use_container_width=True)
            else:
                st.info("No biometric tracking files logged by active clients yet.")
        except Exception as e:
            st.error(f"Failed to scan metrics database array parameters: {e}")
        st.markdown("</div>", unsafe_allow_html=True)

    # ADMIN TAB 2: ROUTINE PRESCRIBER MATRIX
    with tabs[1]:
        st.markdown("<div class='stealth-card'>", unsafe_allow_html=True)
        st.markdown("### 📋 Gym Workout Strategy Prescriber Core")
        st.write("Broadcast the exact training sequences you want running on the gym floor.")
        
        with st.form("add_workout_form"):
            w_day = st.selectbox("Select Target Blueprint Block Split:", ["Push Day", "Pull Day", "Leg Day", "Arm Overload Day", "Core/Cardio Conditioning"])
            w_ex = st.text_input("Exercise Name Designation Structure")
            w_sets = st.number_input("Target Sets Required:", min_value=1, max_value=10, value=4)
            w_reps = st.text_input("Target Repetition Spectrum Range Layout:", value="8-12")
            w_inst = st.text_area("Specific Mechanical Guidance / Coaching Variables Cueing")
            
            submit_w = st.form_submit_button("🚀 Broadcast Prescription Parameters to Global Database")
            if submit_w and w_ex != "":
                new_w = pd.DataFrame([{"Day": w_day, "Exercise": w_ex, "Sets": w_sets, "Reps": w_reps, "Instructions": w_inst}])
                new_w.to_csv(workout_plans_file, mode='a', header=False, index=False)
                st.success(f"Successfully broadcast training protocols for {w_ex} into matching split buckets.")
        
        st.write("---")
        st.write("#### 🛡️ Active Global Workout Architectures Currently Deployed")
        st.dataframe(pd.read_csv(workout_plans_file), use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # ADMIN TAB 3: DIAGNOSTICS CONFIGURATOR
    with tabs[2]:
        st.markdown("<div class='stealth-card'>", unsafe_allow_html=True)
        st.markdown("### 🍳 Administrative Macro Evaluation Panel")
        st.write("Review aggregated mathematical output arrays across the complete member cluster baseline framework.")
        if os.path.exists(metrics_file):
            st.dataframe(pd.read_csv(metrics_file), use_container_width=True)
        else:
            st.info("System logging array currently uninitialized on server local disk storage layers.")
        st.markdown("</div>", unsafe_allow_html=True)

    # ADMIN TAB 4: REVENUE MANAGEMENT CORE
    with tabs[3]:
        st.markdown("<div class='stealth-card'>", unsafe_allow_html=True)
        st.markdown("### 💳 Central Business Liquidity Ledgers")
        st.write("Verify customer incoming invoice sequences, change profile activation states, and track payment verifications.")
        
        if os.path.exists(payments_file):
            p_df = pd.read_csv(payments_file)
            
            c1, c2 = st.columns(2)
            c1.metric("Total Realized Cash Asset Flow Pool", f"₹ {p_df[p_df['Status'] == 'Approved']['Amount'].sum():,}")
            c2.metric("Total Outstanding Pending Verification Screens", f"{len(p_df[p_df['Status'] != 'Approved'])} Verification Requests")
            
            st.write("---")
            st.write("#### Invoices Stream Ledger")
            st.dataframe(p_df, use_container_width=True)
            
            # Simulated Verification Loop Engine
            pending_users = p_df[p_df['Status'] != 'Approved']['Username'].tolist()
            if pending_users:
                st.write("#### 🛡️ Gateway Verification Action Center")
                target_verify = st.selectbox("Select Pending User Account Access Request Queue:", pending_users)
                if st.button("Verify UPI Remittance Payload and Grant License Access Status", use_container_width=True):
                    p_df.loc[p_df['Username'] == target_verify, 'Status'] = 'Approved'
                    p_df.to_csv(payments_file, index=False)
                    st.success(f"Access tier granted to username profile: {target_verify.upper()}. Database parameters locked.")
                    st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

# =========================================================================================
# STANDARD CLIENT ROUTE CHANNELS (MEMBER WORKSTATION VIEW)
# =========================================================================================
else:
    # MEMBER TAB 1: WORKOUT PROTOCOLS PRESCRIBED BY OWNER
    with tabs[0]:
        st.markdown("<div class='stealth-card'>", unsafe_allow_html=True)
        st.markdown("### 📋 My Personalized Training Splits Directive")
        st.write("Review the workout routines designed for you by Coach Varshith.")
        
        plans_df = pd.read_csv(workout_plans_file)
        unique_days = plans_df['Day'].unique().tolist()
        
        selected_split_day = st.selectbox("Select Active Target Strategy Training Split Day Horizon:", unique_days)
        filtered_split = plans_df[plans_df['Day'] == selected_split_day].reset_index(drop=True)
        filtered_split.index = filtered_split.index + 1
        
        st.table(filtered_split)
        st.markdown("</div>", unsafe_allow_html=True)

    # MEMBER TAB 2: BIO-ANALYTICS ENGINE
    with tabs[1]:
        st.markdown("<div class='stealth-card'>", unsafe_allow_html=True)
        st.markdown("### 🍳 Athletic Bio-Nutritional Diagnostic Node")
        st.write("Input parameters manually inside the form grid container below to calculate your metrics.")
        
        with st.form("member_bio_form"):
            g_mode = st.radio("Select Training Vector:", ["🔥 Fat Loss", "⚖️ Body Recomposition", "💪 Muscle Gain (Bulk)"], horizontal=True)
            
            mc1, mc2, mc3 = st.columns(3)
            with mc1:
                w_kg = mc1.number_input("Current Body Weight (kg):", min_value=30.0, max_value=200.0, value=75.0, step=0.1)
                h_cm = mc1.number_input("Absolute Biological Height Scale (cm):", min_value=100.0, max_value=250.0, value=175.0, step=0.1)
            with mc2:
                age_y = mc2.number_input("Age Parameter (Years):", min_value=12, max_value=90, value=21)
                gender_s = mc2.selectbox("Biological Gender:", ["Male", "Female"])
            with mc3:
                bf_p = mc3.number_input("Estimated Body Fat Ratio (%):", min_value=4.0, max_value=50.0, value=15.0, step=0.1)
                t_freq = mc3.slider("Weekly Training Volume Frequency (Days/Week):", min_value=0, max_value=7, value=4)
                
            sub_bio = st.form_submit_button("🚀 COMPILE ATHLETIC METRICS BALANCES")
            
        if sub_bio:
            bmr = (10 * w_kg) + (6.25 * h_cm) - (5 * age_y) + (5 if gender_s == "Male" else -161)
            tdee = bmr * (1.2 + (t_freq * 0.08))
            
            if "Fat Loss" in g_mode: calories = int(tdee - 500)
            elif "Muscle Gain" in g_mode: calories = int(tdee + 350)
            else: calories = int(tdee - 100)
            
            protein = int(w_kg * (2.4 if "Fat Loss" in g_mode else 2.0))
            fats = int((calories * 0.25) / 9)
            carbs = int((calories - ((protein * 4) + (fats * 9))) / 4)
            bmi_calc = round(w_kg / ((h_cm / 100) ** 2), 1)
            
            st.session_state.client_calc_results = {
                "calories": calories, "tdee": int(tdee), "protein": protein, "carbs": carbs, "fats": fats, "bmi": bmi_calc
            }
            
            # Commit logs safely straight into local server disk storage metrics database tracking files array layer
            timestamp_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            pd.DataFrame([{
                "Timestamp": timestamp_str, "Username": st.session_state.active_username, "Weight": w_kg,
                "Bicep": 0.0, "Chest": 0.0, "Waist": 0.0, "BodyFat": bf_p, "Goal": g_mode,
                "CalorieTarget": calories, "ProteinTarget": protein
            }]).to_csv(metrics_file, mode='a', header=False, index=False)
            st.success("Calculations compiled and committed securely to master owner registry ledger channels successfully!")

        if st.session_state.client_calc_results is not None:
            r = st.session_state.client_calc_results
            st.write("---")
            st.markdown("#### **📊 Compiled Output Analytics HUD Layout**")
            
            h_c1, h_c2, h_c3, h_c4, h_c5 = st.columns(5)
            h_c1.markdown(f"<div style='background: #0B0C10; border: 1px solid rgba(69, 162, 158, 0.2); border-top: 3px solid #45A29E; padding: 15px; border-radius: 8px; text-align: center;'><div style='font-size: 10px; color: #888888; text-transform: uppercase;'>Calorie Target</div><div style='font-size: 20px; font-weight: 700; color: #FFFFFF; font-family: Orbitron;'>{r['calories']} <span style='font-size: 10px; color: #45A29E;'>kcal</span></div></div>", unsafe_allow_html=True)
            h_c2.markdown(f"<div style='background: #0B0C10; border: 1px solid rgba(69, 162, 158, 0.2); border-top: 3px solid #45A29E; padding: 15px; border-radius: 8px; text-align: center;'><div style='font-size: 10px; color: #888888; text-transform: uppercase;'>Protein Intake</div><div style='font-size: 20px; font-weight: 700; color: #FFFFFF; font-family: Orbitron;'>{r['protein']} <span style='font-size: 10px; color: #45A29E;'>g</span></div></div>", unsafe_allow_html=True)
            h_c3.markdown(f"<div style='background: #0B0C10; border: 1px solid rgba(69, 162, 158, 0.2); border-top: 3px solid #45A29E; padding: 15px; border-radius: 8px; text-align: center;'><div style='font-size: 10px; color: #888888; text-transform: uppercase;'>Carbohydrates</div><div style='font-size: 20px; font-weight: 700; color: #FFFFFF; font-family: Orbitron;'>{r['carbs']} <span style='font-size: 10px; color: #45A29E;'>g</span></div></div>", unsafe_allow_html=True)
            h_c4.markdown(f"<div style='background: #0B0C10; border: 1px solid rgba(69, 162, 158, 0.2); border-top: 3px solid #45A29E; padding: 15px; border-radius: 8px; text-align: center;'><div style='font-size: 10px; color: #888888; text-transform: uppercase;'>Fats Target</div><div style='font-size: 20px; font-weight: 700; color: #FFFFFF; font-family: Orbitron;'>{r['fats']} <span style='font-size: 10px; color: #45A29E;'>g</span></div></div>", unsafe_allow_html=True)
            h_c5.markdown(f"<div style='background: #0B0C10; border: 1px solid rgba(69, 162, 158, 0.2); border-top: 3px solid #45A29E; padding: 15px; border-radius: 8px; text-align: center;'><div style='font-size: 10px; color: #888888; text-transform: uppercase;'>Body BMI</div><div style='font-size: 20px; font-weight: 700; color: #FFFFFF; font-family: Orbitron;'>{r['bmi']}</div></div>", unsafe_allow_html=True)
            
            st.write("---")
            m_df = pd.DataFrame({"Source": ["Protein 🥩", "Carbs 🍚", "Fats 🥑"], "Calories": [r['protein']*4, r['carbs']*4, r['fats']*9]})
            d_chart = alt.Chart(m_df).mark_arc(innerRadius=60).encode(theta="Calories:Q", color=alt.Color("Source:N", scale=alt.Scale(domain=["Protein 🥩", "Carbs 🍚", "Fats 🥑"], range=["#950740", "#45A29E", "#1F2833"]))).properties(height=240)
            st.altair_chart(d_chart, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # MEMBER TAB 3: PERSONAL PROGRESS TRACKER (TELEMETRY INPUT BOARD)
    with tabs[2]:
        st.markdown("<div class='stealth-card'>", unsafe_allow_html=True)
        st.markdown("### 📅 Biometric Progress Synchronization Core")
        st.write("Manually log detailed metric arrays to synchronize directly to the trainer's terminal desktop files.")
        
        with st.form("measurements_log_form"):
            lm_w = st.number_input("Weight Measure (kg):", value=75.0, step=0.1)
            lm_bi = st.number_input("Bicep Diameter (inches):", value=14.0, step=0.1)
            lm_ch = st.number_input("Chest Circumference (inches):", value=38.0, step=0.1)
            lm_wa = st.number_input("Waist Circumference (inches):", value=32.0, step=0.1)
            lm_bf = st.number_input("Current Body Fat Ratio (%):", value=15.0, step=0.1)
            
            submit_log = st.form_submit_button("🔒 Sync Metrics Snapshot data blocks to Coach Ledger")
            if submit_log:
                timestamp_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                pd.DataFrame([{
                    "Timestamp": timestamp_str, "Username": st.session_state.active_username, "Weight": lm_w,
                    "Bicep": lm_bi, "Chest": lm_ch, "Waist": lm_wa, "BodyFat": lm_bf, "Goal": "Logged Update",
                    "CalorieTarget": 0, "ProteinTarget": 0
                }]).to_csv(metrics_file, mode='a', header=False, index=False)
                st.success("Telemetry payload synced successfully to server disk database.")
                
        if os.path.exists(metrics_file):
            with st.expander("📚 Access My Personal Historical Tracking Logs"):
                g_df = pd.read_csv(metrics_file)
                st.dataframe(g_df[g_df['Username'] == st.session_state.active_username], use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # MEMBER TAB 4: PAYWAY LOCK STATION
    with tabs[3]:
        st.markdown("<div class='stealth-card'>", unsafe_allow_html=True)
        st.markdown("### 💳 Transaction Clearance Gateway Node")
        st.write("Submit payment requests directly to the manager's action queue window loop.")
        
        col_p1, col_p2 = st.columns(2)
        with col_p1:
            st.markdown("#### **Active Subscription Packages Available**")
            chosen_plan = st.selectbox("Choose Target Package Module:", ["Starter Pass (₹1,500 / Mo)", "Quarterly Pack (₹4,000 / 3 Mo)", "Iron Elite VIP (₹12,000 / Yr)"])
            amt_map = {"Starter Pass (₹1,500 / Mo)": 1500, "Quarterly Pack (₹4,000 / 3 Mo)": 4000, "Iron Elite VIP (₹12,000 / Yr)": 12000}
            
            if st.button("Submit Intent Notification for Selected Package", use_container_width=True):
                timestamp_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                pd.DataFrame([{"Timestamp": timestamp_str, "Username": st.session_state.active_username, "Plan": chosen_plan, "Amount": amt_map[chosen_plan], "Status": "Pending Verification"}]).to_csv(payments_file, mode='a', header=False, index=False)
                st.success("Invoice status set to Pending. Present authorization screenshots to Coach Varshith to unblock access nodes.")
        with col_p2:
            qr_html = """
            <div style='border: 2px solid #950740; padding: 20px; border-radius: 10px; background-color: #ffffff; text-align: center; width: 200px; margin: auto;'>
                <h5 style='color: #111111; margin-top: 0; font-family: sans-serif;'>HANUMAN MERCH</h5>
                <div style='background-color: #0B0C10; width: 140px; height: 140px; margin: auto; border-radius: 6px; display: flex; align-items: center; justify-content: center;'>
                    <span style='color: #45A29E; font-size: 10px; font-weight: bold; font-family: monospace;'>[ UPI CODE ]</span>
                </div>
                <p style='color: #333333; font-size: 11px; margin-bottom: 0; font-weight: bold; margin-top: 8px; font-family: monospace;'>hanumangym@ybl</p>
            </div>
            """
            st.markdown(qr_html, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
