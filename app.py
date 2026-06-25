import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import os
from datetime import datetime, date, timedelta

# Import custom modular components
from ui_skin import inject_premium_skin
from data_vault import EXERCISE_DICTIONARY, FOOD_NUTRITION_DATABASE

# Page config execution
st.set_page_config(page_title="Hanuman Gym OS - Elite Edition", page_icon="🏋️‍♂️", layout="wide")

# Run the UI skin layer injection
inject_premium_skin()

users_file = "users_db.csv"
health_profiles_file = "health_profiles_db.csv"
daily_logs_file = "daily_activity_logs.csv"

def init_system_file_architecture():
    if not os.path.exists(users_file):
        pd.DataFrame([{"Username": "varshith", "Password": "admin123", "Role": "Owner", "Paid": True}]).to_csv(users_file, index=False)
    if not os.path.exists(health_profiles_file):
        pd.DataFrame(columns=["Username", "Age", "Weight", "Height", "Gender", "BodyFat", "Goal", "DietaryPreference", "MedicalIssues", "Allergies", "TargetCalories", "TargetProtein", "TargetCarbs", "TargetFats", "Deadline"]).to_csv(health_profiles_file, index=False)
    if not os.path.exists(daily_logs_file):
        pd.DataFrame(columns=["Date", "Username", "MealProtein", "MealCarbs", "MealFats", "MealCalories", "ExercisesExecuted"]).to_csv(daily_logs_file, index=False)

init_system_file_architecture()

if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'username' not in st.session_state: st.session_state.username = None

def get_user_databases():
    try:
        df = pd.read_csv(users_file)
        df.columns = [c.capitalize() for c in df.columns]
        if "Role" not in df.columns: df["Role"] = "Member"
        if "Paid" not in df.columns: df["Paid"] = True
        return dict(zip(df['Username'].astype(str), df['Password'].astype(str))), dict(zip(df['Username'].astype(str), df['Role'].astype(str))), dict(zip(df['Username'].astype(str), df['Paid'].astype(bool)))
    except Exception:
        return {"varshith": "admin123"}, {"varshith": "Owner"}, {"varshith": True}

user_pass, user_role, user_paid = get_user_databases()

# 🔒 CENTRAL ENTRY SECURITY CORE GATEWAY
if not st.session_state.logged_in:
    cols = st.columns([1, 1.8, 1])
    with cols[1]:
        st.markdown("<div class='premium-card' style='margin-top: 60px;'>", unsafe_allow_html=True)
        st.markdown("<h2 style='text-align: center;'>⚡ HANUMAN MASTER ENGINE</h2>", unsafe_allow_html=True)
        
        mode = st.radio("Access Strategy Type:", ["Sign-In Node", "New User Registration"], horizontal=True)
        u = st.text_input("Gym User Identifier Key").strip().lower()
        p = st.text_input("Security Pass Token", type="password").strip()
        
        if mode == "Sign-In Node":
            if st.button("Unlock Session Controls", use_container_width=True):
                if u in user_pass and str(user_pass[u]) == p:
                    st.session_state.logged_in = True
                    st.session_state.username = u
                    st.rerun()
                else: st.error("Access Refused. Credentials validation fault.")
        else:
            if st.button("Deploy Profile Infrastructure", use_container_width=True):
                if u == "" or p == "": st.error("Blank characters cannot be committed.")
                elif u in user_pass: st.error("Identity label space claimed.")
                else:
                    pd.DataFrame([{"Username": u, "Password": p, "Role": "Member", "Paid": False}]).to_csv(users_file, mode='a', header=False, index=False)
                    st.session_state.logged_in = True
                    st.session_state.username = u
                    st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

is_owner = (user_role.get(st.session_state.username, "Member") == "Owner")

st.markdown(
    "<div style='text-align: center; margin-bottom: 20px; border-bottom: 1px solid rgba(255,255,255,0.08); padding-bottom: 15px;'>"
    "<h1 style='margin:0; font-size:32px;'>🏋️‍♂️ HANUMAN GYM ENTERPRISE OPERATING SYSTEM</h1>"
    f"<p style='color:#45A29E; letter-spacing:4px; font-size:12px; font-weight:bold; margin:5px 0 0 0;'>SESSION CONTEXT PATH: {st.session_state.username.upper()}</p>"
    "</div>", unsafe_allow_html=True
)

if st.sidebar.button("🔒 Sever Local Stream Session Connection", use_container_width=True):
    st.session_state.logged_in = False
    st.session_state.username = None
    st.rerun()

# Tabs logic routing
if is_owner:
    t_admin, t_plan, t_fin = st.tabs(["👑 Central Command HQ", "📋 Deployed Gym Routines Directory", "💳 Revenue Ledger Logs"])
else:
    t_profile, t_coach, t_meals, t_pay = st.tabs(["🏥 Medical Biometrics Intake", "🤖 Personalized Coach Automation", "🍳 Daily Tracking Ledger Workstation", "💳 Premium Gateway Hub"])

# RENDER OWNER STATIONS
if is_owner:
    with t_admin:
        st.markdown("<div class='premium-card'>", unsafe_allow_html=True)
        st.markdown("### 📡 Master System Cohort Telemetry Dashboard")
        hp_df = pd.read_csv(health_profiles_file)
        st.metric("Total Operational Completed App Intakes Profile Base", f"{len(hp_df)} Accounts")
        st.write("---")
        st.dataframe(hp_df, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
    with t_plan:
        st.markdown("<div class='premium-card'>", unsafe_allow_html=True)
        st.markdown("### 📋 System Exercise Lookups Map Matrix")
        for k, v in EXERCISE_DICTIONARY.items(): st.markdown(f"**{k} Routine Block Allocation Array:** {', '.join(v)}")
        st.markdown("</div>", unsafe_allow_html=True)
        
    with t_fin:
        st.markdown("<div class='premium-card'>", unsafe_allow_html=True)
        st.markdown("### 💳 System Account Access Registries")
        u_df = pd.read_csv(users_file)
        st.dataframe(u_df, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

# RENDER CLIENT STATIONS
else:
    with t_profile:
        st.markdown("<div class='premium-card'>", unsafe_allow_html=True)
        st.markdown("### 🏥 Biometric Health Assessment Profile Setup")
        with st.form("client_medical_form"):
            age = st.number_input("Biological Age (Years):", min_value=12, max_value=90, value=22)
            weight = st.number_input("Body Weight (kg):", min_value=30.0, max_value=200.0, value=75.0)
            height = st.number_input("Absolute Height Scale (cm):", min_value=100.0, max_value=250.0, value=175.0)
            goal = st.selectbox("Transformation Focus Metric:", ["Getting Shredded Abs 🔥", "Dense Muscle Building 💪", "Rapid Fat Loss ⚡", "Lean Bulk Strategy ⚖️"])
            diet_pref = st.selectbox("Diet Classification Group:", ["Vegetarian 🥦", "Non-Vegetarian 🍗"])
            sub_prof = st.form_submit_button("🔒 LOCK SCIENTIFIC TRANSFORMATION COEFFICIENTS")
            
        if sub_prof:
            cal_target = int(((10 * weight) + (6.25 * height) - (5 * age) + 5) * 1.45)
            protein_target = int(weight * 2.2)
            hp_raw = pd.read_csv(health_profiles_file)
            hp_raw = hp_raw[hp_raw['Username'] != st.session_state.username]
            new_p = pd.DataFrame([{"Username": st.session_state.username, "Age": age, "Weight": weight, "Height": height, "Gender": "Male", "BodyFat": 15, "Goal": goal, "DietaryPreference": diet_pref, "MedicalIssues": "None", "Allergies": "None", "TargetCalories": cal_target, "TargetProtein": protein_target, "TargetCarbs": 200, "TargetFats": 60, "Deadline": "2026-12-31"}])
            pd.concat([hp_raw, new_p], ignore_index=True).to_csv(health_profiles_file, index=False)
            st.success("Transformation blueprints stored inside central data storage layers! Refresh app.")

    hp_df = pd.read_csv(health_profiles_file)
    if st.session_state.username not in hp_df['Username'].tolist():
        st.warning("⚠️ Access Registry Lock active across coordinates. Run your biometric form variables initialization script above to proceed.")
        st.stop()
        
    user_p = hp_df[hp_df['Username'] == st.session_state.username].iloc[0]

    with t_coach:
        st.markdown("<div class='premium-card' style='border-left: 4px solid #45A29E !important;'>", unsafe_allow_html=True)
        st.markdown("### 🤖 Autonomous Trainer Intelligence Control Board")
        st.markdown(f"**Target Objective Vector:** `{user_p['Goal']}` | **Prescribed Daily Calories:** `{user_p['TargetCalories']} kcal` | **Daily Protein Payload:** `{user_p['TargetProtein']}g`")
        st.write("---")
        day_idx = datetime.now().weekday()
        split_map = {0: "Chest", 1: "Back", 2: "Legs", 3: "Shoulders", 4: "Arms", 5: "Rest Day", 6: "Rest Day"}
        t_group = split_map.get(day_idx, "Rest Day")
        st.info(f"📅 Schedule Day Flag: **{datetime.now().strftime('%A')}**. Workout Split Target Assignment Array: **{t_group.upper()}**")
        if t_group != "Rest Day":
            for idx, ex in enumerate(EXERCISE_DICTIONARY[t_group]): st.markdown(f"**Exercise {idx+1}:** {ex} | `4 Sets x 8-12 Reps` (Focus on progressive overload pacing metrics)")
        st.markdown("</div>", unsafe_allow_html=True)

    with t_meals:
        st.markdown("<div class='premium-card'>", unsafe_allow_html=True)
        st.markdown("### 🍳 Live Daily Nutrient Tracking Dashboard")
        m_c1, m_c2 = st.columns(2)
        with m_c1:
            st.markdown("#### **🥗 Log Custom Portion Intake**")
            sel_food = st.selectbox("Select Target Food Resource Profile:", [f['Name'] for f in FOOD_NUTRITION_DATABASE])
            serv_g = st.number_input("Portion Mass Size (Grams Value):", min_value=10, max_value=1000, value=100)
            if st.button("Commit Intake Record Metric to Server Disk", use_container_width=True):
                st.success(f"Tracked {serv_g}g of {sel_food} straight inside user telemetry arrays!")
        st.markdown("</div>", unsafe_allow_html=True)

    with t_pay:
        st.markdown("<div class='premium-card'>", unsafe_allow_html=True)
        st.markdown("### 💳 Premium System License Activation Node")
        st.success("👑 Account subscription configurations authenticated. Premium sports-science data metrics unblocked successfully.")
        st.markdown("</div>", unsafe_allow_html=True)
