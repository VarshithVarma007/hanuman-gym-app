import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import os
from datetime import datetime, date, timedelta

# Page Master Setup
st.set_page_config(page_title="Hanuman Gym OS", page_icon="🏋️‍♂️", layout="wide")

# 🎨 CUSTOM STYLING ENGINE FOR NAVIGATION CHIPS AND PREMIUM DESIGN
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Inter:wght@300;400;600&display=swap');
    
    .stApp {
        background-color: #0B0C10 !important;
        color: #C5C6C7 !important;
        font-family: 'Inter', sans-serif;
    }
    h1, h2, h3, h4 {
        font-family: 'Orbitron', sans-serif !important;
        letter-spacing: 2px;
        color: #FFFFFF !important;
    }
    .stealth-card {
        background-color: #1F2833 !important;
        border-radius: 12px !important;
        padding: 24px !important;
        margin-bottom: 20px !important;
        border-left: 4px solid #950740 !important;
    }
    /* Square Tile Navigation Styling */
    .nav-container {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(110px, 1fr));
        gap: 12px;
        margin-bottom: 25px;
    }
    .nav-tile {
        background-color: #1F2833;
        border: 1px solid #45A29E;
        border-radius: 8px;
        padding: 15px 5px;
        text-align: center;
        color: #FFFFFF;
        font-family: 'Orbitron', sans-serif;
        font-size: 11px;
        cursor: pointer;
        transition: all 0.2s ease;
    }
    .nav-tile:hover {
        background-color: #950740;
        border-color: #FFFFFF;
    }
</style>
""", unsafe_allow_html=True)

# 💾 SYSTEM STORAGE ROUTINES
users_file = "users_db.csv"
workout_logs_file = "user_workout_logs.csv"
food_logs_file = "user_food_logs.csv"
pr_ledger_file = "user_pr_ledger.csv"

def init_dbs():
    if not os.path.exists(users_file):
        pd.DataFrame([{"username": "varshith", "password": "admin123", "role": "Owner"}]).to_csv(users_file, index=False)
    if not os.path.exists(workout_logs_file):
        pd.DataFrame(columns=["Date", "Username", "WorkoutSplit", "Exercise", "SetNumber", "Reps"]).to_csv(workout_logs_file, index=False)
    if not os.path.exists(food_logs_file):
        pd.DataFrame(columns=["Date", "Username", "MealPeriod", "FoodItem", "Calories", "Protein", "Carbs", "Fats"]).to_csv(food_logs_file, index=False)
    if not os.path.exists(pr_ledger_file):
        pd.DataFrame(columns=["Username", "Exercise", "WeightMax"]).to_csv(pr_ledger_file, index=False)

init_dbs()

# 📋 MASTER DATA REGISTRIES
EXERCISE_DICTIONARY = {
    "Chest 🔴": ["Bench Press", "Incline Barbell Press", "Dumbbell Flyes", "Cable Crossovers", "Push-ups"],
    "Back 🍏": ["Deadlift", "Lat Pulldown", "Bent-Over Rows", "Seated Cable Rows", "Pull-ups"],
    "Legs 🦵": ["Squats", "Leg Press", "Romanian Deadlift", "Leg Extensions", "Calf Raises"],
    "Shoulders ⚡": ["Overhead Press", "Lateral Raises", "Rear Delt Flyes", "Front Raises"],
    "Arms 💪": ["Barbell Curls", "Hammer Curls", "Tricep Pushdowns", "Skull Crushers"]
}

FOOD_DICTIONARY = {
    "Chicken Breast (100g)": [165, 31, 0, 3],
    "Whole Eggs (2)": [156, 12, 1, 10],
    "Egg Whites (4)": [68, 14, 0, 0],
    "Paneer (100g)": [265, 18, 1, 20],
    "Soya Chunks (50g)": [170, 26, 16, 0.5],
    "White Rice (1 Cup cooked)": [200, 4, 45, 0],
    "Roti/Chapati (1)": [100, 3, 20, 1],
    "Peanut Butter (2 tbsp)": [190, 7, 6, 16],
    "Milk (250ml)": [120, 8, 12, 5]
}

# Session State Hooks
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'active_username' not in st.session_state: st.session_state.active_username = None
if 'current_tab' not in st.session_state: st.session_state.current_tab = "🏠 HOME"

# Security Gate
if not st.session_state.logged_in:
    cols = st.columns([1, 2, 1])
    with cols[1]:
        st.markdown("<div class='stealth-card' style='margin-top: 50px;'>", unsafe_allow_html=True)
        st.markdown("<h2>⚡ HANUMAN CORE DOORWAY</h2>", unsafe_allow_html=True)
        u_in = st.text_input("Username Identification").strip().lower()
        p_in = st.text_input("Access Token Key", type="password").strip()
        if st.button("Authorize Core Access", use_container_width=True):
            df = pd.read_csv(users_file)
            if u_in in df['username'].values:
                saved_pass = df[df['username'] == u_in]['password'].values[0]
                if str(saved_pass) == p_in:
                    st.session_state.logged_in = True
                    st.session_state.active_username = u_in
                    st.rerun()
            st.error("Invalid Signature Key Matrix.")
        st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# 🎛️ DYNAMIC SQUARE GRID TILES HEADER NAVIGATION
st.markdown("### 🎛️ CORE MODULE CONTROL INTERFACE")
nav_cols = st.columns(9)
tabs_map = {
    0: "🏠 HOME", 1: "📡 LIVE", 2: "🏋️ WORKOUT", 3: "🥗 NUTRITION", 
    4: "🤖 AI TRAINER", 5: "📊 PROGRESS", 6: "💳 PAYMENT", 7: "📍 LOCATION", 8: "👤 PROFILE"
}
for i, label in tabs_map.items():
    if nav_cols[i].button(label, use_container_width=True):
        st.session_state.current_tab = label
        st.rerun()

st.write("---")
current_selection = st.session_state.current_tab

# =========================================================================================
# 🏠 HOME TAB
# =========================================================================================
if current_selection == "🏠 HOME":
    st.markdown("<div class='stealth-card'>", unsafe_allow_html=True)
    st.markdown("## 🏠 CHAMPION COMMAND STATION")
    st.write(f"Welcome back, **{st.session_state.active_username.upper()}**! Here is your automated training operational directive:")
    
    # AI Bot Automated Split Suggestion System
    st.markdown("### 🤖 Automated Split Prescription Coach")
    day_name = datetime.now().strftime("%A")
    split_suggestions = {
        "Monday": "🔥 PUSH DAY (Chest/Shoulders/Triceps) — Focus on max force output vectors.",
        "Tuesday": "⚡ PULL DAY (Back/Rear Delts/Biceps) — Prioritize dynamic row contractions.",
        "Wednesday": "🦵 LEG DAY (Quads/Hamstrings/Calves) — Focus on absolute mechanical squat depth.",
        "Thursday": "🔥 PUSH DAY — Focus on dynamic hypertrophy targets.",
        "Friday": "⚡ PULL DAY — Accentuate deep mechanical width isolation row variations.",
        "Saturday": "🦵 LEG DAY / ARMS OVERLOAD — Secondary stimulation volume block.",
        "Sunday": "🧘 ABS & CARDIO CONDITIONING / RECOVERY REST SCHEDULING SYSTEM"
    }
    st.info(f"📅 Today is **{day_name}**. Your Coach prescribes: **{split_suggestions.get(day_name)}**")
    
    # Quick Summary Data Frames
    st.write("#### Today's Nutritional Baseline Horizon")
    if os.path.exists(food_logs_file):
        f_df = pd.read_csv(food_logs_file)
        today_f = f_df[(f_df['Date'] == date.today().strftime("%Y-%m-%d")) & (f_df['Username'] == st.session_state.active_username)]
        if not today_f.empty:
            st.metric("Total Calories Consumed", f"{int(today_f['Calories'].sum())} kcal")
            st.dataframe(today_f[['MealPeriod', 'FoodItem', 'Calories', 'Protein']], use_container_width=True)
        else:
            st.info("No nutritional records synchronized on disk for today yet.")
    st.markdown("</div>", unsafe_allow_html=True)

# =========================================================================================
# 📡 LIVE TAB
# =========================================================================================
elif current_selection == "📡 LIVE":
    st.markdown("<div class='stealth-card'>", unsafe_allow_html=True)
    st.markdown("## 📡 LIVE BIOMETRIC OCCUPANCY METRICS")
    st.metric("Active Floor Headcount", "38 Members Inside")
    st.write("• **Floor 1 (Strength Core Matrix):** 22 People")
    st.write("• **Floor 2 (Cardio & Mechanical Legs Array):** 16 People")
    st.markdown("</div>", unsafe_allow_html=True)

# =========================================================================================
# 🏋️ WORKOUT TAB
# =========================================================================================
elif current_selection == "🏋️ WORKOUT":
    st.markdown("<div class='stealth-card'>", unsafe_allow_html=True)
    st.markdown("## 🏋️ USER-CONTROLLED PROGRESSIVE WORKOUT LOG ENGINE")
    
    # 1. Select the Target Muscle Architecture Group
    muscle_group = st.selectbox("1. Choose Target Muscle Architecture:", list(EXERCISE_DICTIONARY.keys()))
    
    # 2. Select Exercise from Dictionary Array
    exercise_selected = st.selectbox("2. Choose Performed Movement Node:", EXERCISE_DICTIONARY[muscle_group])
    
    # 3. Dynamic Manual Sets Logging Configuration Form
    num_sets = st.number_input("3. Number of Sets Completed", min_value=1, max_value=10, value=3)
    
    st.write("#### 4. Specify Repetitions Executed Across Individual Sets Matrix:")
    logged_sets = []
    set_cols = st.columns(int(num_sets))
    for s in range(int(num_sets)):
        reps_done = set_cols.number_input(f"Set {s+1} Reps:", min_value=0, max_value=100, value=10, key=f"reps_s_{s}")
        logged_sets.append(reps_done)
        
    if st.button("🔒 SYNC WORKOUT SNAPSHOT LOGS TO DATA MATRIX DISK", use_container_width=True):
        timestamp_str = date.today().strftime("%Y-%m-%d")
        new_logs_list = []
        for s_idx, r_val in enumerate(logged_sets):
            new_logs_list.append({
                "Date": timestamp_str, "Username": st.session_state.active_username,
                "WorkoutSplit": muscle_group, "Exercise": exercise_selected, "SetNumber": s_idx + 1, "Reps": r_val
            })
        pd.DataFrame(new_logs_list).to_csv(workout_logs_file, mode='a', header=False, index=False)
        st.success(f"Successfully recorded performance tracks for `{exercise_selected}` onto system storage database.")
        
    st.write("---")
    st.write("### 📅 Today's Completed Training Logs")
    if os.path.exists(workout_logs_file):
        w_df = pd.read_csv(workout_logs_file)
        today_w = w_df[(w_df['Date'] == date.today().strftime("%Y-%m-%d")) & (w_df['Username'] == st.session_state.active_username)]
        st.dataframe(today_w, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

# =========================================================================================
# 🥗 NUTRITION TAB
# =========================================================================================
elif current_selection == "🥗 NUTRITION":
    st.markdown("<div class='stealth-card'>", unsafe_allow_html=True)
    st.markdown("## 🥗 ADVANCED PERIODIZED INTAKE ENGINE")
    
    # 1. Structural Separation Into Designated Meal Slots
    meal_slot = st.radio("Choose Targeted Meal Period Horizon Placement:", ["Breakfast 🍳", "Lunch 🍚", "Snacks 🥜", "Dinner 🥩"], horizontal=True)
    
    # 2. Food Resource Select Profile
    selected_food = st.selectbox("Choose Consumed Resource Core Node:", list(FOOD_DICTIONARY.keys()))
    serving_grams_multiplier = st.number_input("Serving Size Scale Factor Coefficient (1.0 = Standard 100g/Portion):", min_value=0.1, max_value=10.0, value=1.0, step=0.1)
    
    if st.button("Commit Portion Log Entry to System Queue", use_container_width=True):
        base_macros = FOOD_DICTIONARY[selected_food]
        cal_calc = int(base_macros[0] * serving_grams_multiplier)
        prot_calc = round(base_macros[1] * serving_grams_multiplier, 1)
        carb_calc = round(base_macros[2] * serving_grams_multiplier, 1)
        fat_calc = round(base_macros[3] * serving_grams_multiplier, 1)
        
        new_food_row = pd.DataFrame([{
            "Date": date.today().strftime("%Y-%m-%d"), "Username": st.session_state.active_username,
            "MealPeriod": meal_slot, "FoodItem": selected_food, "Calories": cal_calc,
            "Protein": prot_calc, "Carbs": carb_calc, "Fats": fat_calc
        }])
        new_food_row.to_csv(food_logs_file, mode='a', header=False, index=False)
        st.success(f"Tracked {selected_food} within the `{meal_slot}` bracket database matrix layout successfully.")
        
    st.write("---")
    st.markdown("### 📊 PERIODIZED MEAL TRACKING METRICS LAYER")
    
    if os.path.exists(food_logs_file):
        f_df = pd.read_csv(food_logs_file)
        user_today_f = f_df[(f_df['Date'] == date.today().strftime("%Y-%m-%d")) & (f_df['Username'] == st.session_state.active_username)]
        
        # Displaying segregated targets slots to user before absolute consolidation summing
        meal_periods_list = ["Breakfast 🍳", "Lunch 🍚", "Snacks 🥜", "Dinner 🥩"]
        p_cols = st.columns(4)
        for idx, period in enumerate(meal_periods_list):
            period_data = user_today_f[user_today_f['MealPeriod'] == period]
            p_cols[idx].markdown(f"**{period} Logs:**")
            if not period_data.empty:
                for f_idx, row in period_data.iterrows():
                    p_cols[idx].markdown(f"• {row['FoodItem']} (`{int(row['Calories'])} kcal`)")
            else:
                p_cols[idx].write("<span style='color:gray; font-size:11px;'>No item entries</span>", unsafe_allow_html=True)
                
        # 📈 TOTAL INTAKE CONSOLIDATED PROGRESS REGISTRY HUB PANEL
        st.write("---")
        st.markdown("#### **🔥 Total Consolidated Intake Progression Matrix**")
        total_cal = user_today_f['Calories'].sum()
        total_prot = user_today_f['Protein'].sum()
        total_carb = user_today_f['Carbs'].sum()
        total_fat = user_today_f['Fats'].sum()
        
        hud_c1, hud_c2, hud_c3, hud_c4 = st.columns(4)
        hud_c1.metric("Total Energy Pool Logged", f"{int(total_cal)} / 2500 kcal")
        hud_c2.metric("Total Active Protein Sub-Matrix", f"{int(total_prot)} / 160 g")
        hud_c3.metric("Total Active Carbohydrates", f"{int(total_carb)} / 250 g")
        hud_c4.metric("Total Lipids/Fats Allocation", f"{int(total_fat)} / 70 g")
    st.markdown("</div>", unsafe_allow_html=True)

# =========================================================================================
# 🤖 AI TRAINER TAB
# =========================================================================================
elif current_selection == "🤖 AI TRAINER":
    st.markdown("<div class='stealth-card'>", unsafe_allow_html=True)
    st.markdown("## 🤖 CORE ARTIFICIAL PERSONAL ASSISTANT WORKSTATION")
    st.write("Ask your Coach anything about sports-science, meal replacements, or technique adjustments.")
    user_query_input = st.text_input("Enter question terminal cue script block:")
    if st.button("Fire Query Tracking Node Pipeline", use_container_width=True):
        if user_query_input.strip() != "":
            st.info(f"**Coach Hanuman AI Response Configuration Output Engine:**\n\nTo optimize your strategy right now, ensure you are tracking your reps accurately across your sets layer inside the workout engine tab. Keep your protein floor above 2.0g per kg of total mass to secure long-term physical recovery balances, bro!")
    st.markdown("</div>", unsafe_allow_html=True)

# =========================================================================================
# 📊 PROGRESS TAB
# =========================================================================================
elif current_selection == "📊 PROGRESS":
    st.markdown("<div class='stealth-card'>", unsafe_allow_html=True)
    st.markdown("## 📊 MASTER STRENGTH PERFORMANCE REGISTER")
    st.write("No automation templates here. Select any gym movement vector, input your figures, and compile your historical PR registry manually.")
    
    # 1. Compile Global Gym Exercises Registry Array Dropdown List options safely
    all_possible_gym_movements_list = []
    for exercise_group in EXERCISE_DICTIONARY.values():
        all_possible_gym_movements_list.extend(exercise_group)
        
    # Manual PR Select fields
    pr_ex = st.selectbox("Select Target Exercise Asset Node:", sorted(list(set(all_possible_gym_movements_list))))
    pr_wt = st.number_input("Absolute Top Working Weight Payload Verified (kg):", min_value=1, max_value=500, value=80)
    
    if st.button("🔒 Lock Performance Metric into Personal Record Registry Ledger", use_container_width=True):
        pr_df = pd.read_csv(pr_ledger_file)
        # Clear duplicate movement records for user profiles to keep file clean
        pr_df = pr_df[~((pr_df['Username'] == st.session_state.active_username) & (pr_df['Exercise'] == pr_ex))]
        new_pr_row = pd.DataFrame([{"Username": st.session_state.active_username, "Exercise": pr_ex, "WeightMax": pr_wt}])
        pd.concat([pr_df, new_pr_row], ignore_index=True).to_csv(pr_ledger_file, index=False)
        st.success(f"Personal Record array profile updated successfully for `{pr_ex}`!")
        st.rerun()
        
    st.write("---")
    st.write("#### 🏆 My Verified Heavy Hitter Standing PR Ledger Matrix")
    if os.path.exists(pr_ledger_file):
        display_pr_df = pd.read_csv(pr_ledger_file)
        user_prs = display_pr_df[display_pr_df['Username'] == st.session_state.active_username].reset_index(drop=True)
        st.dataframe(user_prs[['Exercise', 'WeightMax']], use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

# =========================================================================================
# 💳 PAYMENT TAB
# =========================================================================================
elif current_selection == "💳 PAYMENT":
    st.markdown("<div class='stealth-card'>", unsafe_allow_html=True)
    st.markdown("## 💳 PREMIUM PROCESSING CONTROL EDGE WALLET")
    p_cols = st.columns(3)
    p_cols[0].button("💪 Starter Pass\n\n ₹1,500 / Month", use_container_width=True, key="p1")
    p_cols[1].button("🔥 Quarterly Pack\n\n ₹4,000 / 3 Months", use_container_width=True, key="p2")
    p_cols[2].button("👑 Iron Elite VIP\n\n ₹12,000 / Year", use_container_width=True, key="p3")
    st.markdown("</div>", unsafe_allow_html=True)

# =========================================================================================
# 📍 LOCATION TAB
# =========================================================================================
elif current_selection == "📍 LOCATION":
    st.markdown("<div class='stealth-card'>", unsafe_allow_html=True)
    st.markdown("## 📍 JAI HANUMAN FACILITY BOUNDARIES MAP NODE")
    st.write("• **Central Operational Center Branch:** Emmiganur, Andhra Pradesh, India.")
    st.write("• **Facility Status:** Fully Open Infrastructure Active (05:00 AM - 10:00 PM Scale Windows).")
    st.markdown("</div>", unsafe_allow_html=True)

# =========================================================================================
# 👤 PROFILE TAB
# =========================================================================================
elif current_selection == "👤 PROFILE":
    st.markdown("<div class='stealth-card'>", unsafe_allow_html=True)
    st.markdown("## 👤 SECURITY PROFILE PARAMETERS IDENTIFICATION")
    st.write(f"Identity Handle Node Checked: `{st.session_state.active_username.upper()}`")
    st.write("License Class Level: Active Premium Athlete Strata Tier.")
    st.markdown("</div>", unsafe_allow_html=True)
