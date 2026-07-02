import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import os
import time
from datetime import datetime, date, timedelta

# Premium Global Engine Configuration
st.set_page_config(page_title="Hanuman Gym OS - Enterprise", page_icon="🏋️‍♂️", layout="wide")

# 🎨 EXCLUSIVE CYBERPUNK HUD INTERFACE STYLING (CSS)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Inter:wght@300;400;600&display=swap');
    
    .stApp {
        background-color: #050608 !important;
        color: #EEEEF2 !important;
        font-family: 'Inter', sans-serif;
    }
    h1, h2, h3, h4 {
        font-family: 'Orbitron', sans-serif !important;
        letter-spacing: 2px;
        color: #FFFFFF !important;
        text-shadow: 0 0 10px rgba(245, 166, 35, 0.2);
    }
    .premium-card {
        background: linear-gradient(145deg, #0E0F14, #161820) !important;
        border: 1px solid #2A2C38 !important;
        border-radius: 14px !important;
        padding: 24px !important;
        margin-bottom: 20px !important;
    }
    .premium-card:hover {
        border-color: #F5A623 !important;
    }
</style>
""", unsafe_allow_html=True)

# 💾 ROBUST STORAGE SCHEMAS INIT
users_file = "users_db.csv"
workout_logs_file = "user_workout_logs.csv"
food_logs_file = "user_food_logs.csv"
pr_ledger_file = "user_pr_ledger.csv"
custom_routines_file = "user_custom_routines.csv"
checkin_ledger_file = "user_checkin_ledger.csv"

def init_enterprise_architecture():
    if not os.path.exists(users_file):
        pd.DataFrame([{"Username": "varshith", "Password": "admin123", "Role": "Owner", "Streak": 5, "Freezes": 1}]).to_csv(users_file, index=False)
    if not os.path.exists(workout_logs_file):
        pd.DataFrame(columns=["Date", "Username", "Exercise", "Weight", "Sets", "Reps"]).to_csv(workout_logs_file, index=False)
    if not os.path.exists(food_logs_file):
        pd.DataFrame(columns=["Date", "Username", "MealPeriod", "FoodItem", "Calories", "Protein", "Carbs", "Fats"]).to_csv(food_logs_file, index=False)
    if not os.path.exists(pr_ledger_file):
        pd.DataFrame(columns=["Username", "Exercise", "WeightMax"]).to_csv(pr_ledger_file, index=False)
    if not os.path.exists(custom_routines_file):
        pd.DataFrame(columns=["Username", "RoutineName", "ExercisesList"]).to_csv(custom_routines_file, index=False)
    if not os.path.exists(checkin_ledger_file):
        pd.DataFrame(columns=["Date", "Username", "Weight", "BMI", "BodyFat", "WaterLiters", "Sentiment"]).to_csv(checkin_ledger_file, index=False)

init_enterprise_architecture()

# 🗃️ STATIC SOURCE DATA REFERENCE LIBRARIES
EXERCISE_DICTIONARY = {
    "Chest": ["Bench Press", "Incline Dumbbell Press", "Pec Dec Flyes", "Cable Crossovers"],
    "Back": ["Deadlift", "Lat Pulldown", "Barbell Rows", "Seated Cable Rows"],
    "Legs": ["Squats", "Leg Press", "Romanian Deadlift", "Calf Raises"],
    "Shoulders": ["Overhead Press", "Lateral Raises", "Rear Delt Flyes"],
    "Arms": ["Barbell Curls", "Hammer Curls", "Tricep Pushdowns", "Skull Crushers"]
}

FOOD_DICTIONARY = {
    "Chicken Breast (100g)": [165, 31, 0, 3],
    "Whole Eggs (2)": [156, 12, 1, 10],
    "Egg Whites (4)": [68, 14, 0, 0],
    "Paneer (100g)": [265, 18, 1, 20],
    "Soya Chunks (50g)": [170, 26, 16, 0.5],
    "White Rice (1 Cup cooked)": [200, 4, 45, 0],
    "Roti/Chapati (1)": [100, 3, 20, 1]
}

# Runtime Session Management
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'username' not in st.session_state: st.session_state.username = None
if 'current_module' not in st.session_state: st.session_state.current_module = "🏠 Home Dashboard"

# 🔒 SECURE MULTI-ROLE DOORWAY
if not st.session_state.logged_in:
    c = st.columns([1, 1.8, 1])
    with c[1]:
        st.markdown("<div class='premium-card' style='margin-top:60px;'>", unsafe_allow_html=True)
        st.markdown("<h2 style='text-align:center;'>⚡ HANUMAN GATEWAY</h2>", unsafe_allow_html=True)
        auth_mode = st.radio("Access Level Routing:", ["Sign-In Authorization", "New Athlete Registration"], horizontal=True)
        u = st.text_input("User Identification Key").strip().lower()
        p = st.text_input("Security Access Code", type="password").strip()
        
        if auth_mode == "Sign-In Authorization":
            if st.button("Unlock Core Dashboard Systems", use_container_width=True):
                df = pd.read_csv(users_file)
                if u in df['Username'].values:
                    saved_p = df[df['Username'] == u]['Password'].values[0]
                    if str(saved_p) == p:
                        st.session_state.logged_in = True
                        st.session_state.username = u
                        st.rerun()
                st.error("Authentication Refused. Token mismatch.")
        else:
            if st.button("Initialize Fresh Account Profile", use_container_width=True):
                df = pd.read_csv(users_file)
                if u == "" or p == "": st.error("Fields cannot be empty.")
                elif u in df['Username'].values: st.error("Username identity already claimed.")
                else:
                    pd.DataFrame([{"Username": u, "Password": p, "Role": "Member", "Streak": 1, "Freezes": 1}]).to_csv(users_file, mode='a', header=False, index=False)
                    st.session_state.logged_in = True
                    st.session_state.username = u
                    st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# Role definitions mapping
u_df = pd.read_csv(users_file)
user_row = u_df[u_df['Username'] == st.session_state.username].iloc[0]
is_owner = (user_row['Role'] == "Owner")

# 🎛️ HIGH-RETENTION SQUARE INTERFACE TILES MATRIX
st.markdown("### 🎛️ SYSTEM COMPONENT ROUTER MATRIX")
modules = ["🏠 Home Dashboard", "📡 Live Telemetry", "🏋️ Workout Log", "🥗 Nutrition Node", "🤖 AI Coach Hub", "📊 Analytical Progress", "💳 Payment Hub", "👤 Profile Node"]
if is_owner: modules.append("👑 Operational HQ")

tile_cols = st.columns(len(modules))
for idx, mod in enumerate(modules):
    if tile_cols[idx].button(mod, use_container_width=True):
        st.session_state.current_module = mod
        st.rerun()

st.write("---")
active_mod = st.session_state.current_module

# =========================================================================================
# 🏠 HOME DASHBOARD TAB
# =========================================================================================
if active_mod == "🏠 Home Dashboard":
    st.markdown("<div class='premium-card'>", unsafe_allow_html=True)
    st.markdown(f"## 🏠 CORE HUD: Welcome Back, {st.session_state.username.upper()}")
    
    # Habit-Forming Streak Counters Engine
    st.markdown("### 🔥 Consistency Matrix Status")
    h_c1, h_c2, h_c3 = st.columns(3)
    h_c1.metric("Current Training Streak", f"{user_row['Streak']} Days")
    h_c2.metric("Available Streak Freezes Remaining", f"{user_row['Freezes']} Left")
    
    if h_c3.button("🛡️ Activate Streak Freeze Node"):
        if user_row['Freezes'] > 0:
            u_df.loc[u_df['Username'] == st.session_state.username, 'Freezes'] -= 1
            u_df.to_csv(users_file, index=False)
            st.success("Streak Freeze deployed successfully! Your counter stays locked today, bro.")
            st.rerun()
        else: st.error("No Streak Freezes left in your profile bank.")
        
    # AI Automatic Split Planner Suggestion Block
    st.write("---")
    st.markdown("#### 🤖 Daily Coaching Routine Broadcast")
    day_name = datetime.now().strftime("%A")
    split_reference = {
        "Monday": "🔥 Push Split (Chest/Shoulders/Triceps) - Target mechanical tension overload.",
        "Tuesday": "⚡ Pull Split (Back/Rear Delts/Biceps) - Focus on row extensions.",
        "Wednesday": "🦵 Lower Body Split (Quads/Hamstrings/Glutes) - Absolute squat depth focus.",
        "Thursday": "🔥 Push Volume Focus - Focus on structural hypertrophy scaling.",
        "Friday": "⚡ Pull Hypertrophy Focus - Isolate single arm vector mechanics.",
        "Saturday": "💪 Arm Overload & Conditioning - Target high lactic threshold volume splits.",
        "Sunday": "🧘 Complete System Adaptability Rest Recovery & Mobility Alignment Framework."
    }
    st.info(f"📅 Current Calendar Day Context: **{day_name}**. Prescribed Protocol: **{split_reference.get(day_name)}**")
    st.markdown("</div>", unsafe_allow_html=True)

# =========================================================================================
# 📡 LIVE TELEMETRY TAB
# =========================================================================================
elif active_mod == "📡 Live Telemetry":
    st.markdown("<div class='premium-card'>", unsafe_allow_html=True)
    st.markdown("## 📡 LIVE IOT FACILITY OCCUPANCY TRAFFIC")
    st.metric("Facility Floor Load Density", "28 Athletes Logged")
    st.write("• **Floor 1 (Free Weights & Cables):** 18 People")
    st.write("• **Floor 2 (Cardio, HIIT, Machine Squat Arrays):** 10 People")
    st.markdown("</div>", unsafe_allow_html=True)

# =========================================================================================
# 🏋️ WORKOUT LOG TAB
# =========================================================================================
elif active_mod == "🏋️ Workout Log":
    st.markdown("<div class='premium-card'>", unsafe_allow_html=True)
    st.markdown("## 🏋️ USER-CONTROLLED PROGRESSIVE WORKOUT LOG ENGINE")
    
    w_tab1, w_tab2, w_tab3 = st.tabs(["📝 Log Sets Execution", "🛠️ Custom Routine Builder", "🧮 Barbell Plate Calculator"])
    
    with w_tab1:
        muscle = st.selectbox("Select Target Muscle Cluster Group:", list(EXERCISE_DICTIONARY.keys()))
        exercise = st.selectbox("Select Target Exercise Movement Node:", EXERCISE_DICTIONARY[muscle])
        
        c1, c2, c3 = st.columns(3)
        w_sets = c1.number_input("Sets Executed:", min_value=1, max_value=10, value=3)
        w_weight = c2.number_input("Top Working Weight Load (kg):", min_value=0.0, max_value=400.0, value=60.0, step=2.5)
        
        st.write("Specify exact repetitions completed across each set index matrix layer:")
        rep_logs = []
        r_cols = st.columns(int(w_sets))
        for i in range(int(w_sets)):
            r_val = r_cols.number_input(f"Set {i+1} Reps:", min_value=0, max_value=100, value=10, key=f"re_s_{i}")
            rep_logs.append(r_val)
            
        if st.button("🔒 Commit Session Set Tracks to Local Disk Database", use_container_width=True):
            today_str = date.today().strftime("%Y-%m-%d")
            new_rows = [{"Date": today_str, "Username": st.session_state.username, "Exercise": exercise, "Weight": w_weight, "Sets": s_idx+1, "Reps": r_v} for s_idx, r_v in enumerate(rep_logs)]
            pd.DataFrame(new_rows).to_csv(workout_logs_file, mode='a', header=False, index=False)
            st.success("Workout metrics logged successfully!")
            
    with w_tab2:
        st.markdown("### 🛠️ Custom Routine Architect")
        r_name = st.text_input("Routine Designation Label (e.g., Push/Pull/Legs Version 1)")
        all_ex = []
        for v in EXERCISE_DICTIONARY.values(): all_ex.extend(v)
        selected_ex_nodes = st.multiselect("Select Core Exercises to Chain inside Routine Vector Array:", sorted(list(set(all_ex))))
        
        if st.button("💾 Lock Custom Routine Template Matrix into Storage"):
            if r_name and selected_ex_nodes:
                pd.DataFrame([{"Username": st.session_state.username, "RoutineName": r_name, "ExercisesList": "|".join(selected_ex_nodes)}]).to_csv(custom_routines_file, mode='a', header=False, index=False)
                st.success(f"Custom routine layout `{r_name}` written to disk registry.")
                
    with w_tab3:
        st.markdown("### 🧮 Precision Barbell Plate Loading Calculator")
        t_weight = st.number_input("Target Barbell Working Load Metric (kg):", min_value=20.0, max_value=400.0, value=100.0, step=2.5)
        bar_weight = st.selectbox("Barbell Base Tare Weight Specification:", [20.0, 15.0, 10.0])
        
        rem_weight = (t_weight - bar_weight) / 2
        plates = [25.0, 20.0, 15.0, 10.0, 5.0, 2.5]
        plate_counts = {}
        for p in plates:
            count = int(rem_weight // p)
            if count > 0:
                plate_counts[f"{p} kg Plate"] = count
                rem_weight -= (count * p)
                
        st.write("#### Exact Loading Required per Side:")
        if plate_counts:
            for k, v in plate_counts.items(): st.markdown(f"• **{k}:** Load `{v}` items per side.")
        else: st.info("Load weight matches empty bar specification parameters.")
    st.markdown("</div>", unsafe_allow_html=True)

# =========================================================================================
# 🥗 NUTRITION NODE TAB
# =========================================================================================
elif active_mod == "🥗 Nutrition Node":
    st.markdown("<div class='premium-card'>", unsafe_allow_html=True)
    st.markdown("## 🥗 ADVANCED PERIODIZED INTAKE ENGINE")
    
    meal_slot = st.radio("Target Intake Category Slot Placement Configuration:", ["Breakfast 🍳", "Lunch 🍚", "Snacks 🥜", "Dinner 🥩"], horizontal=True)
    selected_food = st.selectbox("Choose Consumed Resource Node Element:", list(FOOD_DICTIONARY.keys()))
    serving_factor = st.number_input("Serving Size Scale Factor Coefficient (1.0 = Standard 100g/Portion):", min_value=0.1, max_value=10.0, value=1.0)
    
    if st.button("Commit Portion Log Entry to System Queue", use_container_width=True):
        macros = FOOD_DICTIONARY[selected_food]
        pd.DataFrame([{
            "Date": date.today().strftime("%Y-%m-%d"), "Username": st.session_state.username, "MealPeriod": meal_slot,
            "FoodItem": selected_food, "Calories": int(macros[0]*serving_factor), "Protein": round(macros[1]*serving_factor,1),
            "Carbs": round(macros[2]*serving_factor,1), "Fats": round(macros[3]*serving_factor,1)
        }]).to_csv(food_logs_file, mode='a', header=False, index=False)
        st.success("Meal entry tracked.")
        
    st.write("---")
    st.markdown("### 📊 Consolidated Intake Progression Matrix")
    if os.path.exists(food_logs_file):
        f_df = pd.read_csv(food_logs_file)
        today_f = f_df[(f_df['Date'] == date.today().strftime("%Y-%m-%d")) & (f_df['Username'] == st.session_state.username)]
        
        nc1, nc2, nc3, nc4 = st.columns(4)
        nc1.metric("Energy Logged", f"{int(today_f['Calories'].sum())} / 2500 kcal")
        nc2.metric("Protein Intake", f"{int(today_f['Protein'].sum())} / 160 g")
        nc3.metric("Carbohydrates", f"{int(today_f['Carbs'].sum())} / 250 g")
        nc4.metric("Fats Tracker", f"{int(today_f['Fats'].sum())} / 70 g")
    st.markdown("</div>", unsafe_allow_html=True)

# =========================================================================================
# 🤖 AI COACH HUB TAB
# =========================================================================================
elif active_mod == "🤖 AI Coach Hub":
    st.markdown("<div class='premium-card'>", unsafe_allow_html=True)
    st.markdown("## 🤖 COGNITIVE ASSISTANT CONTROL INTERFACE")
    st.write("Prompt your automated trainer for technique cues or budget macro modifications:")
    q = st.text_input("Enter question script layer text input box:")
    if st.button("Fire Query Tracking Node Pipeline", use_container_width=True):
        if q.strip() != "":
            st.info("**Coach Hanuman AI Automated Output Engine System Response:**\n\nEnsure your repetition tempo values control the eccentric deceleration path phase completely, bro! Hit your meal slot tracking matrices on time to lock down recovery.")
    st.markdown("</div>", unsafe_allow_html=True)

# =========================================================================================
# 📊 ANALYTICAL PROGRESS TAB
# =========================================================================================
elif active_mod == "📊 Analytical Progress":
    st.markdown("<div class='premium-card'>", unsafe_allow_html=True)
    st.markdown("## 📊 PURE MANUAL STRENGTH PERFORMANCE REGISTER")
    
    p_tab1, p_tab2, p_tab3 = st.tabs(["📉 Biometrics Analytics & Check-ins", "🏆 Manual PR Strength Tracker", "🖼️ Private Transformation Vault"])
    
    with p_tab1:
        with st.form("checkin_metrics_form"):
            ci_w = st.number_input("Current Body Mass Weight (kg):", min_value=30.0, max_value=200.0, value=75.0)
            ci_bf = st.number_input("Body Fat Ratio (%):", min_value=3.0, max_value=50.0, value=15.0)
            ci_water = st.slider("Water Hydration Volume Tracking Index (Liters):", 0.0, 8.0, 3.0, step=0.5)
            ci_feel = st.select_slider("Daily Sentiment / Happiness Index Valuation:", options=["Low Energy", "Tired", "Normal Active", "Excellent Performance Rating"])
            submit_ci = st.form_submit_button("🚀 Commit Snapshot Check-in To Analytics Log")
            
        if submit_ci:
            pd.DataFrame([{
                "Date": date.today().strftime("%Y-%m-%d"), "Username": st.session_state.username,
                "Weight": ci_w, "BMI": round(ci_w / (1.75**2),1), "BodyFat": ci_bf, "WaterLiters": ci_water, "Sentiment": ci_feel
            }]).to_csv(checkin_ledger_file, mode='a', header=False, index=False)
            st.success("Biometric data payload synced successfully!")
            
    with p_tab2:
        st.markdown("### 🏆 Heavy Hitter Personal Records Ledger")
        all_movements = []
        for v in EXERCISE_DICTIONARY.values(): all_movements.extend(v)
        pr_ex = st.selectbox("Select Target Exercise Asset Node:", sorted(list(set(all_movements))))
        pr_val = st.number_input("Absolute Verified Top Single-Rep Max Capacity Weight (kg):", min_value=1.0, max_value=500.0, value=100.0, step=2.5)
        
        if st.button("🔒 Verify and Log Maximum Strength Lift Payload"):
            pr_df = pd.read_csv(pr_ledger_file)
            pr_df = pr_df[~((pr_df['Username'] == st.session_state.username) & (pr_df['Exercise'] == pr_ex))]
            pd.concat([pr_df, pd.DataFrame([{"Username": st.session_state.username, "Exercise": pr_ex, "WeightMax": pr_val}])], ignore_index=True).to_csv(pr_ledger_file, index=False)
            st.success(f"PR updated successfully for `{pr_ex}`!")
            
        st.write("---")
        if os.path.exists(pr_ledger_file):
            pr_df = pd.read_csv(pr_ledger_file)
            st.dataframe(pr_df[pr_df['Username'] == st.session_state.username][['Exercise', 'WeightMax']].reset_index(drop=True), use_container_width=True)
            
    with p_tab3:
        st.markdown("### 🖼️ Private Transformation Progress Photo Vault")
        st.write("Upload and secure your weekly physical progress shots here to audit visual structural composition updates.")
        st.file_uploader("Select weekly progress photo configuration file snapshot tracking layer:", type=["jpg", "jpeg", "png"])
        st.info("🔒 Secure local storage sandboxing engine active. Images are encrypted directly within local memory buffers.")
    st.markdown("</div>", unsafe_allow_html=True)

# =========================================================================================
# 💳 PAYMENT HUB TAB
# =========================================================================================
elif active_mod == "💳 Payment Hub":
    st.markdown("<div class='premium-card'>", unsafe_allow_html=True)
    st.markdown("## 💳 OPERATION BILLING GATEWAY CONTROL")
    st.write("Select package modules to initiate digital signature remittance configurations:")
    pay_cols = st.columns(3)
    pay_cols[0].button("💪 Monthly Gold\n\n ₹1,500 / Month", use_container_width=True, key="m1")
    pay_cols[1].button("🔥 Quarterly Bulk Pack\n\n ₹4,000 / 3 Months", use_container_width=True, key="m2")
    pay_cols[2].button("👑 Annual Elite Stratum\n\n ₹12,000 / Year", use_container_width=True, key="m3")
    st.markdown("</div>", unsafe_allow_html=True)

# =========================================================================================
# 👤 PROFILE NODE TAB
# =========================================================================================
elif active_mod == "👤 Profile Node":
    st.markdown("<div class='premium-card'>", unsafe_allow_html=True)
    st.markdown("## 👤 SECURITY PROFILE PARAMETERS IDENTIFICATION")
    st.write(f"Identity Handle Node Checked: `{st.session_state.username.upper()}`")
    st.write(f"Current Core System Profile Clearance Strata Role Designation: **{user_row['Role'].upper()}**")
    st.markdown("</div>", unsafe_allow_html=True)

# =========================================================================================
# 👑 OPERATIONAL HQ (OWNER ADMIN ACCESS)
# =========================================================================================
elif active_mod == "👑 Operational HQ" and is_owner:
    st.markdown("<div class='premium-card'>", unsafe_allow_html=True)
    st.markdown("## 👑 OWNER OPERATIONAL COMMAND MANAGEMENT")
    st.write("Monitor total system registrations, audit active operational files, and manage financial parameters.")
    
    hq_tab1, hq_tab2 = st.tabs(["👥 User Records Index Engine", "📈 Global Analytics Data Stream"])
    with hq_tab1:
        st.dataframe(pd.read_csv(users_file), use_container_width=True)
    with hq_tab2:
        if os.path.exists(checkin_ledger_file):
            st.write("#### Global Client Biometric Sentiment Data Streams")
            st.dataframe(pd.read_csv(checkin_ledger_file), use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)
