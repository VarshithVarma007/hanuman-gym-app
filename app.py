import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import time
from datetime import datetime, date, timedelta
import os

# Set page layout configuration to wide for a sweeping dashboard layout
st.set_page_config(page_title="Hanuman Gym Premium Portal", page_icon="🏋️‍♂️", layout="wide")

# 🎨 STEALTH MINIMALIST DESIGN THEME (CUSTOM CSS OVERWRITE)
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

# Live Business Storage File System Definitions
ledger_file = "metrics_ledger.csv"
users_file = "users_db.csv"  
payments_file = "payments_ledger.csv"

# Ensure core files exist on launch
def init_live_storage_files():
    if not os.path.exists(users_file):
        pd.DataFrame([{"username": "varshith", "password": "admin123", "tier": "Owner"}]).to_csv(users_file, index=False)
    if not os.path.exists(ledger_file):
        pd.DataFrame(columns=["Timestamp", "Username", "Bicep (in)", "Chest (in)", "Waist (in)", "Body Fat (%)"]).to_csv(ledger_file, index=False)
    if not os.path.exists(payments_file):
        pd.DataFrame([
            {"Timestamp": "2026-06-01 10:00:00", "Username": "rahul", "Plan": "Quarterly Pack", "Amount": 4000},
            {"Timestamp": "2026-06-15 14:30:00", "Username": "amit", "Plan": "Starter Pass", "Amount": 1500},
            {"Timestamp": "2026-06-20 09:15:00", "Username": "vikram", "Plan": "Iron Elite VIP", "Amount": 12000}
        ]).to_csv(payments_file, index=False)

init_live_storage_files()

# 📋 WORKOUT SPLIT SCHEDULER DATA REFERENCE
workout_splits = {
    "🔥 Push Day (Chest/Shoulders/Triceps)": [
        {"Exercise": "Flat Barbell Bench Press", "Sets": "4 Sets", "Reps": "6-8 Reps", "Rest": "120s"},
        {"Exercise": "Incline Dumbbell Press", "Sets": "3 Sets", "Reps": "8-10 Reps", "Rest": "90s"},
        {"Exercise": "Seated Overhead Barbell Press", "Sets": "4 Sets", "Reps": "8 Reps", "Rest": "90s"},
        {"Exercise": "Cable Lateral Raises", "Sets": "4 Sets", "Reps": "12-15 Reps", "Rest": "60s"},
        {"Exercise": "Overhead Rope Tricep Extensions", "Sets": "3 Sets", "Reps": "10-12 Reps", "Rest": "60s"}
    ],
    "⚡ Pull Day (Back/Rear Delts/Biceps)": [
        {"Exercise": "Conventional Deadlift", "Sets": "3 Sets", "Reps": "5 Reps (Heavy)", "Rest": "150s"},
        {"Exercise": "Lat Pulldown", "Sets": "4 Sets", "Reps": "8-10 Reps", "Rest": "90s"},
        {"Exercise": "Barbell Bent-Over Rows", "Sets": "3 Sets", "Reps": "8 Reps", "Rest": "90s"},
        {"Exercise": "Face Pulls for Rear Delts", "Sets": "4 Sets", "Reps": "15 Reps", "Rest": "60s"},
        {"Exercise": "Incline Dumbbell Bicep Curls", "Sets": "3 Sets", "Reps": "10-12 Reps", "Rest": "60s"}
    ],
    "🦵 Leg Day (Quads/Hamstrings/Calves)": [
        {"Exercise": "Barbell Back Squat", "Sets": "4 Sets", "Reps": "6-8 Reps", "Rest": "150s"},
        {"Exercise": "Romanian Deadlifts (RDLs)", "Sets": "3 Sets", "Reps": "10 Reps", "Rest": "90s"},
        {"Exercise": "Leg Press", "Sets": "3 Sets", "Reps": "12 Reps", "Rest": "90s"},
        {"Exercise": "Seated Leg Extensions", "Sets": "4 Sets", "Reps": "15 Reps", "Rest": "60s"},
        {"Exercise": "Standing Calf Raises", "Sets": "4 Sets", "Reps": "20 Reps", "Rest": "45s"}
    ]
}

# 🏆 INITIALIZE GLOBAL DATABASE STATE 
if 'leaderboard_data' not in st.session_state:
    st.session_state.leaderboard_data = pd.DataFrame([
        {"Member": "Varshith", "Bench Press (kg)": 100, "Squat (kg)": 140, "Deadlift (kg)": 180, "Total (kg)": 420},
        {"Member": "Rahul", "Bench Press (kg)": 90, "Squat (kg)": 120, "Deadlift (kg)": 160, "Total (kg)": 370},
        {"Member": "Amit", "Bench Press (kg)": 110, "Squat (kg)": 130, "Deadlift (kg)": 170, "Total (kg)": 410},
    ])

if 'streak_count' not in st.session_state: st.session_state.streak_count = 5
if 'live_scanned_count' not in st.session_state: st.session_state.live_scanned_count = 35
if 'user_goal_text' not in st.session_state: st.session_state.user_goal_text = "Pack on dense lean muscle mass!"
if 'user_goal_deadline' not in st.session_state: st.session_state.user_goal_deadline = date(2026, 8, 31)
if 'macro_results' not in st.session_state: st.session_state.macro_results = None

def load_users():
    try:
        df = pd.read_csv(users_file)
        return dict(zip(df['username'].astype(str), df['password'].astype(str)))
    except:
        return {"varshith": "admin123"}

def save_user(username, password):
    pd.DataFrame([{"username": username, "password": password, "tier": "Member"}]).to_csv(users_file, mode='a', header=False, index=False)

user_credentials_db = load_users()

if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'active_username' not in st.session_state: st.session_state.active_username = None

# 🔒 SECURITY ACCESS LOCK GATEWAY
if not st.session_state.logged_in:
    cols = st.columns([1, 2, 1])
    with cols[1]:
        st.markdown("<div class='stealth-card' style='margin-top: 50px;'>", unsafe_allow_html=True)
        st.markdown("<h2 style='text-align: center; color: #FFFFFF;'>⚡ HANUMAN LIVE INTERFACE</h2>", unsafe_allow_html=True)
        
        auth_mode = st.radio("Access Tier:", ["Sign In to Account", "Register New Profile"], horizontal=True)
        u_in = st.text_input("Gym Username Identification").strip().lower()
        p_in = st.text_input("Security Pass Token", type="password").strip()
        
        if auth_mode == "Sign In to Account":
            if st.button("Unlock Core Dashboard Systems", use_container_width=True):
                if u_in in user_credentials_db and str(user_credentials_db[u_in]) == p_in:
                    st.session_state.logged_in = True
                    st.session_state.active_username = u_in
                    st.rerun()
                else: st.error("Access Refused. Invalid credentials signature.")
        else:
            if st.button("Generate Account & Login", use_container_width=True):
                if u_in == "" or p_in == "": st.error("Tokens cannot be initialized blank.")
                elif u_in in user_credentials_db: st.error("Identification label already claimed.")
                else:
                    save_user(u_in, p_in)
                    st.session_state.logged_in = True
                    st.session_state.active_username = u_in
                    st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# 🎛️ MAIN PLATFORM TOP PANEL HEADER BRANDING
st.markdown(
    "<div style='text-align: center; padding: 20px 0; border-bottom: 2px dashed rgba(255,255,255,0.1); margin-bottom: 30px;'>"
    "<h1 style='margin: 0; font-size: 36px; color: #FFFFFF; font-weight: 700;'>🏋️‍♂️ HANUMAN GYM SOFTWARE</h1>"
    "<p style='margin: 5px 0 0 0; color: #45A29E; font-size: 13px; letter-spacing: 5px; font-weight:bold;'>STEALTH LIVE PRODUCTION SYSTEMS</p>"
    "</div>", 
    unsafe_allow_html=True
)

# Sidebar Identity Tag
st.sidebar.markdown(f"### 🚀 Current User: `{st.session_state.active_username.upper()}`")
if st.sidebar.button("🔒 Terminate Cloud Session", use_container_width=True):
    st.session_state.logged_in = False
    st.session_state.active_username = None
    st.session_state.macro_results = None
    st.rerun()

is_owner = (st.session_state.active_username == "varshith")

# Build Tab Horizon matrix layout arrays dynamically
tab_labels = ["🔴 Live Counter", "📊 Traffic Graphs", "🏆 PR Performance", "⚡ Split Planner", "🍳 Bio-Analytics Engine", "📅 Consistency Matrix", "💳 Pay Station"]
if is_owner:
    tab_labels.append("👑 Admin Headquarters")

tabs_list = st.tabs(tab_labels)

# -------------------------------------------------------------
# TAB 1: LIVE COUNTER
# -------------------------------------------------------------
with tabs_list[0]:
    st.markdown("<div class='stealth-card'>", unsafe_allow_html=True)
    st.subheader("📡 Live Occupancy Metrics")
    current_headcount = st.session_state.live_scanned_count
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Active Floor Headcount", f"{current_headcount} Members")
    col2.metric("Floor 1 (Free Weights)", f"{int(current_headcount * 0.55)} People")
    col3.metric("Floor 2 (Cardio / Legs)", f"{current_headcount - int(current_headcount * 0.55)} People")
    
    st.write("---")
    if current_headcount > 55: st.error(f"🔴 **HEAVY PEAK RUSH:** Capacity at high density load.")
    elif current_headcount > 25: st.warning(f"🟡 **MODERATE LOAD:** Standard training environment active.")
    else: st.success(f"🟢 **PEACEFUL ZONE:** Gym floor is clear. Ideal opportunity to train!")
    st.markdown("</div>", unsafe_allow_html=True)

# -------------------------------------------------------------
# TAB 2: TRAFFIC GRAPHS
# -------------------------------------------------------------
with tabs_list[1]:
    st.markdown("<div class='stealth-card'>", unsafe_allow_html=True)
    st.subheader("📈 Chronological Crowd Analytics")
    selected_day = st.selectbox("Choose Targeted Baseline Horizon", ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])
    if selected_day == 'Sunday':
        st.error("🔒 Sunday is official recovery rest day allocation.")
    else:
        hours = list(range(5, 22))
        crowd_estimates = [0 if 10 <= h < 17 else (65 + np.random.randint(-10, 10) if h in [7, 8, 18, 19] else 18 + np.random.randint(-4, 8)) for h in hours]
        chart_data = pd.DataFrame({'Time (24h Scale)': [f"{h}:00" for h in hours], 'Estimated Density': crowd_estimates})
        chart = alt.Chart(chart_data).mark_area(
            color=alt.Gradient(gradient='linear', stops=[alt.GradientStop(color='#45A29E', offset=0), alt.GradientStop(color='#0B0C10', offset=1)])
        ).encode(x=alt.X('Time (24h Scale):O', sort=None), y=alt.Y('Estimated Density:Q', title="Active Density Headcount"))
        st.altair_chart(chart, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

# -------------------------------------------------------------
# TAB 3: PR PERFORMANCE
# -------------------------------------------------------------
with tabs_list[2]:
    st.markdown("<div class='stealth-card'>", unsafe_allow_html=True)
    st.subheader("🏆 Compound Lift Performance Analytics")
    col1, col2 = st.columns(2)
    with col1:
        new_name = st.text_input("Competitor Name", value=st.session_state.active_username)
        bp_lift = st.number_input("1-Rep Max Bench Press (kg)", value=70)
    with col2:
        sq_lift = st.number_input("1-Rep Max Back Squat (kg)", value=90)
        dl_lift = st.number_input("1-Rep Max Conventional Deadlift (kg)", value=110)
        
    if st.button("Verify & Log Max Lift Payload", use_container_width=True):
        if new_name.strip() != "":
            total_lift = bp_lift + sq_lift + dl_lift
            new_entry = pd.DataFrame([{"Member": new_name, "Bench Press (kg)": bp_lift, "Squat (kg)": sq_lift, "Deadlift (kg)": dl_lift, "Total (kg)": total_lift}])
            st.session_state.leaderboard_data = pd.concat([st.session_state.leaderboard_data, new_entry], ignore_index=True)
            st.success("Compound parameters saved successfully to leaderboard matrix array!")
            st.rerun()

    st.write("### 🥇 Heavy Hitter Live Standings")
    sorted_board = st.session_state.leaderboard_data.sort_values(by="Total (kg)", ascending=False).reset_index(drop=True)
    sorted_board.index = sorted_board.index + 1
    st.dataframe(sorted_board, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

# -------------------------------------------------------------
# TAB 4: INTERACTIVE SPLIT PLANNER
# -------------------------------------------------------------
with tabs_list[3]:
    st.markdown("<div class='stealth-card'>", unsafe_allow_html=True)
    st.subheader("⚡ Hypertrophy Training Split Matrix")
    chosen_split = st.selectbox("Choose Target Routine Block", list(workout_splits.keys()))
    st.table(pd.DataFrame(workout_splits[chosen_split]))
    st.markdown("</div>", unsafe_allow_html=True)

# -------------------------------------------------------------
# TAB 5: BIO-ANALYTICS ENGINE
# -------------------------------------------------------------
with tabs_list[4]:
    st.markdown("<div class='stealth-card'>", unsafe_allow_html=True)
    st.subheader("🍳 TDEE & ATHLETIC CALCULATOR PORTAL")
    
    with st.form(key="biometrics_input_form"):
        goal_mode = st.radio("SELECT ATHLETIC TARGET VECTOR:", ["🔥 Fat Loss", "⚖️ Body Recomposition", "💪 Muscle Gain (Bulk)"], horizontal=True)
        st.write("---")
        col_input1, col_input2, col_input3 = st.columns(3)
        
        with col_input1:
            weight_kg = st.number_input("Current Weight (kg):", min_value=30.0, max_value=200.0, value=75.0, step=0.1)
            height_unit = st.selectbox("Height Format:", ["Centimeters (cm)", "Feet + Inches"])
            f_col, i_col = st.columns(2)
            ft = f_col.number_input("Feet:", min_value=3, max_value=8, value=5)
            inch = i_col.number_input("Inches:", min_value=0, max_value=11, value=9)
            height_cm_input = st.number_input("Height explicitly if cm selected:", min_value=100.0, max_value=250.0, value=175.0, step=0.1)
            
        with col_input2:
            age_years = st.number_input("Age (Years):", min_value=10, max_value=100, value=21)
            gender_type = st.selectbox("Gender Profile:", ["Male", "Female"])
            body_fat_pct = st.number_input("Body Fat Matrix (%):", min_value=3.0, max_value=50.0, value=16.0, step=0.1)
            
        with col_input3:
            training_days_w = st.number_input("Weekly Training Frequency (0-7 Days):", min_value=0, max_value=7, value=4)
            intensity_tier = st.selectbox("Intensity Threshold Scale:", ["Beginner", "Light", "Moderate", "Intense", "Athlete"], index=2)
            target_weight_kg = st.number_input("Target Weight Objective (kg):", min_value=30.0, max_value=200.0, value=70.0)
            rate_speed = st.selectbox("Target Adjustment Speed Scale (kg/Week):", [0.25, 0.50, 0.75, 1.00], index=1)

        st.write("---")
        submit_btn = st.form_submit_button("🚀 EXECUTE MATHEMATICAL METRICS PAYLOAD", use_container_width=True)

    if submit_btn:
        final_height = height_cm_input if height_unit == "Centimeters (cm)" else ((ft * 30.48) + (inch * 2.54))
        lean_body_mass_kg = round(weight_kg * (1 - (body_fat_pct / 100)), 1)
        bmr_calc = (10 * weight_kg) + (6.25 * final_height) - (5 * age_years) + (5 if gender_type == "Male" else -161)
        activity_factors = {"Beginner": 1.2, "Light": 1.375, "Moderate": 1.55, "Intense": 1.725, "Athlete": 1.9}
        tdee_calc = bmr_calc * (activity_factors[intensity_tier] + ((training_days_w - 3) * 0.025))
        
        adjusted_speed = 0.0 if "Body Recomposition" in goal_mode else rate_speed
        final_target_weight = weight_kg if "Body Recomposition" in goal_mode else target_weight_kg
        
        if "Fat Loss" in goal_mode: daily_calorie_target = max(1200, int(tdee_calc - (adjusted_speed * 1100)))
        elif "Muscle Gain" in goal_mode: daily_calorie_target = int(tdee_calc + (adjusted_speed * 550))
        else: daily_calorie_target = int(tdee_calc - 150)

        protein_per_kg = 2.4 if "Fat Loss" in goal_mode else (2.2 if "Body Recomposition" in goal_mode else 2.0)
        req_protein_g = int(weight_kg * protein_per_kg)
        req_fat_g = int((daily_calorie_target * 0.25) / 9)
        req_carbs_g = int(max(30, (daily_calorie_target - ((req_protein_g * 4) + (req_fat_g * 9))) / 4))
        base_water_liters = (weight_kg * 0.033) + (training_days_w * 0.35)
        computed_bmi = round(weight_kg / ((final_height / 100.0) ** 2), 1)
        weight_delta_abs = abs(final_target_weight - weight_kg)
        weeks_to_destination = int(np.ceil(weight_delta_abs / adjusted_speed)) if adjusted_speed > 0 else 12
        projected_completion_date = date.today() + timedelta(weeks=weeks_to_destination)

        st.session_state.macro_results = {
            "weight_kg": weight_kg, "target_weight_kg": final_target_weight, "rate_speed": adjusted_speed, "goal_mode": goal_mode,
            "daily_calorie_target": daily_calorie_target, "tdee_calc": int(tdee_calc), "req_protein_g": req_protein_g,
            "req_carbs_g": req_carbs_g, "req_fat_g": req_fat_g, "base_water_liters": base_water_liters, "computed_bmi": computed_bmi,
            "lean_body_mass_kg": lean_body_mass_kg, "weight_delta_abs": weight_delta_abs, "weeks_to_destination": weeks_to_destination,
            "projected_completion_date": projected_completion_date, "body_fat_pct": body_fat_pct
        }

    if st.session_state.macro_results is not None:
        res = st.session_state.macro_results
        st.write("---")
        st.markdown("### 📊 SYSTEM TARGET DIAGNOSTICS")
        
        st.markdown("<p style='color: #45A29E; font-weight: bold; letter-spacing: 1px; margin-bottom: 5px;'>🔋 DAILY NUTRITIONAL REQUIREMENTS</p>", unsafe_allow_html=True)
        num_cols = st.columns(5)
        num_cols[0].markdown(f"<div style='background: #0B0C10; border: 1px solid rgba(69, 162, 158, 0.2); border-top: 3px solid #45A29E; padding: 15px; border-radius: 8px; text-align: center;'><div style='font-size: 10px; color: #888888; text-transform: uppercase;'>Calories Target</div><div style='font-size: 22px; font-weight: 700; color: #FFFFFF; font-family: Orbitron;'>{res['daily_calorie_target']} <span style='font-size: 12px; color: #45A29E;'>kcal</span></div><div style='font-size: 10px; color: #888888; margin-top: 4px;'>TDEE: {res['tdee_calc']}</div></div>", unsafe_allow_html=True)
        num_cols[1].markdown(f"<div style='background: #0B0C10; border: 1px solid rgba(69, 162, 158, 0.2); border-top: 3px solid #45A29E; padding: 15px; border-radius: 8px; text-align: center;'><div style='font-size: 10px; color: #888888; text-transform: uppercase;'>Protein Intake</div><div style='font-size: 22px; font-weight: 700; color: #FFFFFF; font-family: Orbitron;'>{res['req_protein_g']} <span style='font-size: 12px; color: #45A29E;'>g</span></div><div style='font-size: 10px; color: #00E676; margin-top: 4px;'>LBM Preservation</div></div>", unsafe_allow_html=True)
        num_cols[2].markdown(f"<div style='background: #0B0C10; border: 1px solid rgba(69, 162, 158, 0.2); border-top: 3px solid #45A29E; padding: 15px; border-radius: 8px; text-align: center;'><div style='font-size: 10px; color: #888888; text-transform: uppercase;'>Carbohydrates</div><div style='font-size: 22px; font-weight: 700; color: #FFFFFF; font-family: Orbitron;'>{res['req_carbs_g']} <span style='font-size: 12px; color: #45A29E;'>g</span></div><div style='font-size: 10px; color: #888888; margin-top: 4px;'>Glycogen Fuel</div></div>", unsafe_allow_html=True)
        num_cols[3].markdown(f"<div style='background: #0B0C10; border: 1px solid rgba(69, 162, 158, 0.2); border-top: 3px solid #45A29E; padding: 15px; border-radius: 8px; text-align: center;'><div style='font-size: 10px; color: #888888; text-transform: uppercase;'>Fats Allocation</div><div style='font-size: 22px; font-weight: 700; color: #FFFFFF; font-family: Orbitron;'>{res['req_fat_g']} <span style='font-size: 12px; color: #45A29E;'>g</span></div><div style='font-size: 10px; color: #888888; margin-top: 4px;'>Hormonal Base</div></div>", unsafe_allow_html=True)
        num_cols[4].markdown(f"<div style='background: #0B0C10; border: 1px solid rgba(69, 162, 158, 0.2); border-top: 3px solid #45A29E; padding: 15px; border-radius: 8px; text-align: center;'><div style='font-size: 10px; color: #888888; text-transform: uppercase;'>Water Schedule</div><div style='font-size: 22px; font-weight: 700; color: #FFFFFF; font-family: Orbitron;'>{round(res['base_water_liters'], 1)} <span style='font-size: 12px; color: #45A29E;'>L</span></div><div style='font-size: 10px; color: #29B6F6; margin-top: 4px;'>Optimal Hydration</div></div>", unsafe_allow_html=True)

        st.write("") 
        st.markdown("<p style='color: #950740; font-weight: bold; letter-spacing: 1px; margin-bottom: 5px;'>🩺 BIOLOGICAL & TIMELINE METRICS</p>", unsafe_allow_html=True)
        bio_cols = st.columns(5)
        bio_cols[0].markdown(f"<div style='background: #0B0C10; border: 1px solid rgba(149, 7, 64, 0.2); border-top: 3px solid #950740; padding: 15px; border-radius: 8px; text-align: center;'><div style='font-size: 10px; color: #888888; text-transform: uppercase;'>Calculated BMI</div><div style='font-size: 22px; font-weight: 700; color: #FFFFFF; font-family: Orbitron;'>{res['computed_bmi']}</div><div style='font-size: 10px; color: #888888; margin-top: 4px;'>Body Mass Index</div></div>", unsafe_allow_html=True)
        bio_cols[1].markdown(f"<div style='background: #0B0C10; border: 1px solid rgba(149, 7, 64, 0.2); border-top: 3px solid #950740; padding: 15px; border-radius: 8px; text-align: center;'><div style='font-size: 10px; color: #888888; text-transform: uppercase;'>Lean Body Mass</div><div style='font-size: 22px; font-weight: 700; color: #FFFFFF; font-family: Orbitron;'>{res['lean_body_mass_kg']} <span style='font-size: 12px; color: #950740;'>kg</span></div><div style='font-size: 10px; color: #888888; margin-top: 4px;'>Pure Muscle Frame</div></div>", unsafe_allow_html=True)
        bio_cols[2].markdown(f"<div style='background: #0B0C10; border: 1px solid rgba(149, 7, 64, 0.2); border-top: 3px solid #950740; padding: 15px; border-radius: 8px; text-align: center;'><div style='font-size: 10px; color: #888888; text-transform: uppercase;'>Weight Delta</div><div style='font-size: 22px; font-weight: 700; color: #FFFFFF; font-family: Orbitron;'>{round(res['weight_delta_abs'], 1)} <span style='font-size: 12px; color: #950740;'>kg</span></div><div style='font-size: 10px; color: #FF4500; margin-top: 4px;'>Total Change</div></div>", unsafe_allow_html=True)
        bio_cols[3].markdown(f"<div style='background: #0B0C10; border: 1px solid rgba(149, 7, 64, 0.2); border-top: 3px solid #950740; padding: 15px; border-radius: 8px; text-align: center;'><div style='font-size: 10px; color: #888888; text-transform: uppercase;'>Timeline Target</div><div style='font-size: 22px; font-weight: 700; color: #FFFFFF; font-family: Orbitron;'>{res['weeks_to_destination']} <span style='font-size: 12px; color: #950740;'>Wks</span></div><div style='font-size: 10px; color: #888888; margin-top: 4px;'>Required Duration</div></div>", unsafe_allow_html=True)
        bio_cols[4].markdown(f"<div style='background: #0B0C10; border: 1px solid rgba(149, 7, 64, 0.2); border-top: 3px solid #950740; padding: 15px; border-radius: 8px; text-align: center;'><div style='font-size: 10px; color: #888888; text-transform: uppercase;'>Completion Date</div><div style='font-size: 14px; font-weight: 700; color: #FFFFFF; font-family: Orbitron; margin-top: 8px;'>{res['projected_completion_date'].strftime('%b %d, %Y')}</div><div style='font-size: 10px; color: #00E676; margin-top: 8px;'>Estimated Horizon</div></div>", unsafe_allow_html=True)

        st.write("---")
        graph_col1, graph_col2 = st.columns([1, 1])
        with graph_col1:
            st.markdown("<p style='text-align:center; font-weight:bold;'>🍩 Macronutrient Energy Split Matrix</p>", unsafe_allow_html=True)
            macro_chart_df = pd.DataFrame({"Macro Source": ["Protein 🥩", "Carbs 🍚", "Fats 🥑"], "Caloric Value": [res['req_protein_g'] * 4, res['req_carbs_g'] * 4, res['req_fat_g'] * 9]})
            donut_chart = alt.Chart(macro_chart_df).mark_arc(innerRadius=50).encode(theta=alt.Theta(field="Caloric Value", type="quantitative"), color=alt.Color(field="Macro Source", type="nominal", scale=alt.Scale(domain=["Protein 🥩", "Carbs 🍚", "Fats 🥑"], range=["#950740", "#45A29E", "#1F2833"])), tooltip=["Macro Source", "Caloric Value"]).properties(height=220)
            st.altair_chart(donut_chart, use_container_width=True)
        with graph_col2:
            st.markdown("<p style='text-align:center; font-weight:bold;'>📈 Chronological Trajectory Forecast</p>", unsafe_allow_html=True)
            timeline_weeks_list = list(range(res['weeks_to_destination'] + 1))
            weight_progression_trajectory = [res['weight_kg'] - (w * res['rate_speed']) if "Fat Loss" in res['goal_mode'] else (res['weight_kg'] + (w * res['rate_speed']) if "Muscle Gain" in res['goal_mode'] else res['weight_kg']) for w in timeline_weeks_list]
            forecast_chart = alt.Chart(pd.DataFrame({"Weeks": timeline_weeks_list, "Projected Weight (kg)": weight_progression_trajectory})).mark_line(point=True, color='#45A29E').encode(x=alt.X("Weeks:O", title="Timeline Weeks Horizon"), y=alt.Y("Projected Weight (kg):Q", title="Weight Profile", scale=alt.Scale(domain=[min(weight_progression_trajectory)-2, max(weight_progression_trajectory)+2]))).properties(height=220)
            st.altair_chart(forecast_chart, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

# -------------------------------------------------------------
# TAB 6: CONSISTENCY MATRIX
# -------------------------------------------------------------
with tabs_list[5]:
    st.markdown("<div class='stealth-card'>", unsafe_allow_html=True)
    st.subheader("📅 Tactical Timeline Tracking Engine")
    days_left = (st.session_state.user_goal_deadline - date.today()).days
    st.info(f"🎯 Pinned Target Block active across session horizons. Allocation Buffer: {days_left} Days.")
    sc1, sc2 = st.columns(2)
    sc1.metric("🔥 Attendance Streak Logs", f"{st.session_state.streak_count} Training Days")
    if sc2.button("💪 Log Attendance Session", use_container_width=True):
        st.session_state.streak_count += 1
        st.rerun()
        
    st.write("---")
    st.write("### 🩻 Digital Body Measurements Logging Matrix")
    m1, m2 = st.columns(2)
    with m1:
        bi = st.number_input("Bicep Diameter (in)", value=14.0, key="bi_m")
        ch = st.number_input("Chest Circumference (in)", value=38.0, key="ch_m")
    with m2:
        wa = st.number_input("Waist Line Axis (in)", value=32.0, key="wa_m")
        bf = st.number_input("Estimated Body Fat Ratio (%)", value=15, key="bf_m")
        
    if st.button("Sync Metrics Arrays to Local CSV Disk File Layer", use_container_width=True, key="save_m"):
        new_df = pd.DataFrame([{"Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "Bicep (in)": bi, "Chest (in)": ch, "Waist (in)": wa, "Body Fat (%)": bf}])
        new_df.to_csv(ledger_file, index=False) if not os.path.exists(ledger_file) else new_df.to_csv(ledger_file, mode='a', header=False, index=False)
        st.success("Telemetry payload synced successfully to server disk.")
    st.markdown("</div>", unsafe_allow_html=True)

# -------------------------------------------------------------
# TAB 7: PAY STATION
# -------------------------------------------------------------
with tabs_list[6]:
    st.markdown("<div class='stealth-card'>", unsafe_allow_html=True)
    st.subheader("💳 Membership Node Transaction Gateway")
    p1, p2, p3 = st.columns(3)
    p1.button("💪 Starter Pass\n\n ₹1,500 / Month", key="p_m1")
    p2.button("🔥 Quarterly Pack\n\n ₹4,000 / 3 Months", key="p_m2")
    p3.button("👑 Iron Elite VIP\n\n ₹12,000 / Year", key="p_m3")
    st.write("---")
    pay_col1, pay_col2 = st.columns([1, 1])
    with pay_col1:
        st.markdown("#### **UPI Clearing Instructions**")
        st.write("1. Open standard financial applications (GPay, PhonePe, Paytm).\n2. Initiate camera node scan on the right merchant placeholder frame.\n3. Input the exact matching package billing fee and confirm validation.")
    with pay_col2:
        qr_html = """
        <div style='border: 3px solid #950740; padding: 25px; border-radius: 12px; background-color: #ffffff; text-align: center; width: 220px; margin: auto;'>
            <h4 style='color: #111111; margin-top: 0; font-family: sans-serif; letter-spacing:1px;'>HANUMAN GYM MERCH</h4>
            <div style='background-color: #1a1a1a; width: 160px; height: 160px; margin: auto; border-radius: 8px; display: flex; align-items: center; justify-content: center;'>
                <span style='color: #45A29E; font-size: 11px; font-weight: bold; font-family: monospace;'>[ GATEWAY VALID ]</span>
            </div>
            <p style='color: #333333; font-size: 11px; margin-bottom: 0; font-weight: bold; margin-top: 10px; font-family: monospace;'>UPI: hanumangym@ybl</p>
        </div>
        """
        st.markdown(qr_html, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# -------------------------------------------------------------
# TAB 8: 👑 ADMIN HEADQUARTERS
# -------------------------------------------------------------
if is_owner:
    with tabs_list[7]:
        st.markdown("<div class='stealth-card' style='border-left-color: #45A29E !important;'>", unsafe_allow_html=True)
        st.markdown("## 👑 MASTER CONTROL ADMINISTRATIVE STATION")
        
        # 💰 FINANCIAL ANALYSIS SECTION
        st.markdown("### 💰 Financial Liquidity Ledgers")
        if os.path.exists(payments_file):
            pay_df = pd.read_csv(payments_file)
            total_gross_revenue = pay_df['Amount'].sum()
            total_transactions = len(pay_df)
            
            f_col1, f_col2, f_col3 = st.columns(3)
            f_col1.metric("Gross Collected Revenue", f"₹ {total_gross_revenue:,}")
            f_col2.metric("Settled Invoices", f"{total_transactions} Orders")
            f_col3.metric("Average Ticket Value", f"₹ {int(total_gross_revenue / max(1, total_transactions)):,}")
            
            with st.expander("📝 View Global Financial Transaction Stream Ledger"):
                st.dataframe(pay_df, use_container_width=True)
        
        st.write("---")
        
        # 📡 DIRECT INFRASTRUCTURE OVERWRITE CONTROL PANEL
        st.markdown("### 📡 Hardware Stream Multi-Overwrites")
        st.session_state.live_scanned_count = st.slider("🔧 Manual Override Facility Attendance Counters:", 0, 150, int(st.session_state.live_scanned_count))
        st.success(f"Headcount threshold locked at: {st.session_state.live_scanned_count} people inside facility boundaries.")
        st.markdown("</div>", unsafe_allow_html=True)
