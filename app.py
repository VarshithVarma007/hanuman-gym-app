import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import os
from datetime import datetime, date, timedelta

# Premium Global Page Matrix Configuration
st.set_page_config(page_title="Hanuman Gym OS - Elite Edition", page_icon="🏋️‍♂️", layout="wide")

# 🎨 HIGH-FIDELITY CYBERPUNK PREMIUM INTERFACE SKIN (CUSTOM EMBEDDED CSS)
premium_skin_css = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Inter:wght@300;400;600&display=swap');
    
    .stApp {
        background-color: #050508 !important;
        color: #E2E8F0 !important;
        font-family: 'Inter', sans-serif;
    }
    
    h1, h2, h3, h4 {
        font-family: 'Orbitron', sans-serif !important;
        letter-spacing: 3px;
        color: #FFFFFF !important;
        text-transform: uppercase;
        text-shadow: 0 0 10px rgba(149, 7, 64, 0.3);
    }
    
    .premium-card {
        background: linear-gradient(145deg, #111625, #070913) !important;
        border: 1px solid rgba(69, 162, 158, 0.15) !important;
        border-radius: 16px !important;
        padding: 26px !important;
        margin-bottom: 24px !important;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.6) !important;
        transition: all 0.3s ease;
    }
    
    .premium-card:hover {
        border-color: #950740 !important;
        box-shadow: 0 8px 32px rgba(149, 7, 64, 0.2) !important;
    }
    
    .hud-metric-label {
        font-size: 11px;
        text-transform: uppercase;
        color: #8A99AD;
        letter-spacing: 2px;
    }
    
    .hud-metric-val {
        font-family: 'Orbitron', sans-serif;
        font-size: 26px;
        font-weight: 700;
        color: #FFFFFF;
    }
</style>
"""
st.markdown(premium_skin_css, unsafe_allow_html=True)

# 💾 ROBUST SEAMLESS FILES DATABASE TRACKING NODES
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

# Global Static Reference Libraries
EXERCISE_DICTIONARY = {
    "Chest": ["Flat Barbell Bench Press", "Incline Dumbbell Press", "Dumbbell Flyes", "Pec Dec Machine", "Cable Crossover"],
    "Back": ["Conventional Deadlift", "Barbell Bent-Over Rows", "Lat Pulldown", "Seated Cable Rows", "Pull-Ups"],
    "Legs": ["Barbell Back Squat", "Leg Press", "Romanian Deadlift", "Seated Leg Extensions", "Standing Calf Raises"],
    "Shoulders": ["Seated Overhead Barbell Press", "Dumbbell Lateral Raises", "Rear Delt Face Pulls", "Front Raises"],
    "Arms": ["Barbell Bicep Curls", "Hammer Curls", "Tricep Rope Pushdowns", "Close-Grip Bench Press", "Preacher Curls"]
}

FOOD_NUTRITION_DATABASE = [
    {"Name": "Chicken Breast 🥩", "Protein": 31, "Carbs": 0, "Fats": 3, "Type": "Non-Veg", "Tier": "Standard"},
    {"Name": "Whole Eggs 🥚", "Protein": 6, "Carbs": 0, "Fats": 5, "Type": "Non-Veg", "Tier": "Affordable Budget"},
    {"Name": "Egg Whites 🥚", "Protein": 4, "Carbs": 0, "Fats": 0, "Type": "Non-Veg", "Tier": "Affordable Budget"},
    {"Name": "Premium Paneer 🧀", "Protein": 18, "Carbs": 1, "Fats": 20, "Type": "Veg", "Tier": "Standard"},
    {"Name": "Soya Chunks 🫘", "Protein": 52, "Carbs": 33, "Fats": 1, "Type": "Veg", "Tier": "Affordable Budget"},
    {"Name": "Greek Yogurt (Curd) 🥛", "Protein": 10, "Carbs": 4, "Fats": 0, "Type": "Veg", "Tier": "Standard"},
    {"Name": "Lentils / Dal 🥣", "Protein": 9, "Carbs": 20, "Fats": 0, "Type": "Veg", "Tier": "Affordable Budget"},
    {"Name": "White Rice 🍚", "Protein": 3, "Carbs": 28, "Fats": 0, "Type": "Veg", "Tier": "Affordable Budget"},
    {"Name": "Peanut Butter 🥜", "Protein": 25, "Carbs": 20, "Fats": 50, "Type": "Veg", "Tier": "Affordable Budget"}
]

# Session State Pipeline Initialization
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'username' not in st.session_state: st.session_state.username = None

def get_user_databases():
    df = pd.read_csv(users_file)
    return dict(zip(df['Username'].astype(str), df['Password'].astype(str))), dict(zip(df['Username'].astype(str), df['Role'].astype(str))), dict(zip(df['Username'].astype(str), df['Paid'].astype(bool)))

user_pass, user_role, user_paid = get_user_databases()

# 🔒 CENTRAL GATEWAY LOCK INTERFACE
if not st.session_state.logged_in:
    cols = st.columns([1, 1.8, 1])
    with cols[1]:
        st.markdown("<div class='premium-card' style='margin-top: 60px;'>", unsafe_allow_html=True)
        st.markdown("<h2 style='text-align: center;'>⚡ HANUMAN INTELLIGENT PORTAL</h2>", unsafe_allow_html=True)
        
        mode = st.radio("Access Node Router:", ["Client Authorization Sign-In", "New Corporate Registration Matrix"], horizontal=True)
        u = st.text_input("User ID String").strip().lower()
        p = st.text_input("Security Pass Token", type="password").strip()
        
        if mode == "Client Authorization Sign-In":
            if st.button("Unshackle Command Terminal", use_container_width=True):
                if u in user_pass and str(user_pass[u]) == p:
                    st.session_state.logged_in = True
                    st.session_state.username = u
                    st.rerun()
                else: st.error("Verification Refused. Invalid credentials signature.")
        else:
            if st.button("Deploy New Account Infrastructure", use_container_width=True):
                if u == "" or p == "": st.error("Parameters cannot be empty strings.")
                elif u in user_pass: st.error("User identity space already claimed.")
                else:
                    pd.DataFrame([{"Username": u, "Password": p, "Role": "Member", "Paid": False}]).to_csv(users_file, mode='a', header=False, index=False)
                    st.session_state.logged_in = True
                    st.session_state.username = u
                    st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# Role Mapping Coordinates
is_owner = (user_role.get(st.session_state.username, "Member") == "Owner")

# 🎛️ PLATFORM MASTER TOP PANEL HEADLINE
st.markdown(
    "<div style='text-align: center; margin-bottom: 20px; border-bottom: 1px solid rgba(255,255,255,0.08); padding-bottom: 15px;'>"
    "<h1 style='margin:0; font-size:32px;'>🏋️‍♂️ HANUMAN AUTOMATED SAAST ENGINE</h1>"
    f"<p style='color:#45A29E; letter-spacing:4px; font-size:12px; font-weight:bold; margin:5px 0 0 0;'>ACTIVE OPERATOR: {st.session_state.username.upper()} | ROLE MATRICES VERIFIED</p>"
    "</div>", unsafe_allow_html=True
)

if st.sidebar.button("🔒 Terminate System Handshake", use_container_width=True):
    st.session_state.logged_in = False
    st.session_state.username = None
    st.rerun()

# Dynamic Tab Router Generation
if is_owner:
    t_admin, t_plan, t_fin = st.tabs(["👑 Central Command HQ", "📋 Global Routine Deployments", "💳 Revenue Ledger Audits"])
else:
    t_profile, t_coach, t_meals, t_pay = st.tabs(["🏥 Medical & Biometric Intake", "🤖 AI Certified Coach HUD", "🍳 Daily Intake Log Workstation", "💳 Premium Gateway Access"])

# =========================================================================================
# 👑 GYM OWNER BACKEND COMMAND CONTROLS
# =========================================================================================
if is_owner:
    with t_admin:
        st.markdown("<div class='premium-card'>", unsafe_allow_html=True)
        st.markdown("### 📡 Global Facility Command Center")
        
        # Real-Time Operational Counts
        u_df = pd.read_csv(users_file)
        hp_df = pd.read_csv(health_profiles_file)
        
        m_c1, m_c2, m_c3 = st.columns(3)
        m_c1.metric("Registered Cohorts Base", f"{len(u_df)} Accounts")
        m_c2.metric("Premium Active Accounts", f"{len(u_df[u_df['Paid'] == True])} Members")
        m_c3.metric("Evaluated Medical Intake Profiles", f"{len(hp_df)} Completed")
        
        st.write("---")
        st.write("#### 🔍 Granular Client Profile Deep-Dive Auditor")
        if not hp_df.empty:
            target_user = st.selectbox("Select Target Client Account Node to Review:", hp_df['Username'].tolist())
            client_file = hp_df[hp_df['Username'] == target_user].iloc[0]
            
            aud_c1, aud_c2, aud_c3 = st.columns(3)
            aud_c1.markdown(f"**Age:** {client_file['Age']} Yrs<br>**Weight:** {client_file['Weight']} kg<br>**Height:** {client_file['Height']} cm", unsafe_allow_html=True)
            aud_c2.markdown(f"**Target Direction:** {client_file['Goal']}<br>**Diet Filter:** {client_file['DietaryPreference']}", unsafe_allow_html=True)
            aud_c3.markdown(f"**Medical Constraints:** <span style='color:#FF4B4B;'>{client_file['MedicalIssues']}</span><br>**Allergies Registry:** {client_file['Allergies']}", unsafe_allow_html=True)
        else:
            st.info("No clients have completed their biometric medical forms yet.")
        st.markdown("</div>", unsafe_allow_html=True)

    with t_plan:
        st.markdown("<div class='premium-card'>", unsafe_allow_html=True)
        st.markdown("### 📋 Active Operational Training Directories")
        st.write("Review the exercise structures integrated across your database layers.")
        for k, v in EXERCISE_DICTIONARY.items():
            st.markdown(f"**{k} Strategy Protocols:** {', '.join(v)}")
        st.markdown("</div>", unsafe_allow_html=True)

    with t_fin:
        st.markdown("<div class='premium-card'>", unsafe_allow_html=True)
        st.markdown("### 💳 Corporate Ledger Audit Infrastructure")
        u_df = pd.read_csv(users_file)
        
        st.write("#### 🛡️ License Activation Control Desk")
        st.dataframe(u_df, use_container_width=True)
        
        pending_activation_users = u_df[u_df['Paid'] == False]['Username'].tolist()
        if pending_activation_users:
            t_user = st.selectbox("Select Target Account to Unblock Premium Modules:", pending_activation_users)
            if st.button("Authorize License Token and Grant Access Key", use_container_width=True):
                u_df.loc[u_df['Username'] == t_user, 'Paid'] = True
                u_df.to_csv(users_file, index=False)
                st.success(f"Premium activation sequence complete for account: `{t_user.upper()}`")
                st.rerun()
        else:
            st.success("All registered accounts are currently activated with premium licenses.")
        st.markdown("</div>", unsafe_allow_html=True)

# =========================================================================================
# 🏋️‍♂️ STANDARD MEMBER FRONTEND SAAS EXPERIENCE
# =========================================================================================
else:
    # CLIENT TAB 1: BIOMETRIC & HEALTH PRE-REQUISITE INTAKE FORM
    with t_profile:
        st.markdown("<div class='premium-card'>", unsafe_allow_html=True)
        st.markdown("### 🏥 Clinical Intake & Target Configuration Node")
        st.write("Before generating any workout or diet structures, our system must register your current physical and health baseline.")
        
        with st.form("medical_intake_form"):
            col1, col2, col3 = st.columns(3)
            with col1:
                age = col1.number_input("Biological Age (Years):", min_value=12, max_value=90, value=22)
                weight = col1.number_input("Current Body Weight Scale (kg):", min_value=30.0, max_value=200.0, value=75.0, step=0.1)
                height = col1.number_input("Absolute Height Matrix (cm):", min_value=100.0, max_value=250.0, value=175.0, step=0.1)
            with col2:
                gender = col2.selectbox("Biological Sex Profile:", ["Male", "Female"])
                bf = col2.number_input("Current Body Fat Percentage (%):", min_value=3.0, max_value=50.0, value=15.0, step=0.1)
                goal = col2.selectbox("Select Precision Transformation Target:", ["Getting Shredded Abs 🔥", "Dense Muscle Building 💪", "Rapid Fat Loss ⚡", "Lean Bulk Strategy ⚖️", "Aggressive Mass Bulk 📈"])
            with col3:
                diet_pref = col3.selectbox("Dietary Class Specification:", ["Vegetarian 🥦", "Non-Vegetarian 🍗"])
                med_issues = col3.text_input("Injuries or Medical Conditions (e.g. Lower back pain, None):", value="None")
                allergies = col3.text_input("Allergies List (e.g. Peanut, Dairy, None):", value="None")
                
            duration_w = st.select_slider("Target Transformation Duration Commitment Scale:", options=[6, 8, 12, 16, 24], value=12)
            
            submit_profile = st.form_submit_button("🔒 LOCK VARIABLES AND EXECUTE AI COACH INITIALIZATION")
            
        if submit_profile:
            # Sports Science Matrix Calculations
            bmr = (10 * weight) + (6.25 * height) - (5 * age) + (5 if gender == "Male" else -161)
            tdee = bmr * 1.45 # Moderate Baseline Activity Coefficient
            
            if "Loss" in goal or "Shredded" in goal:
                cal_target = int(tdee - 500)
                prot_multiplier = 2.4
            elif "Bulk" in goal or "Building" in goal:
                cal_target = int(tdee + 400)
                prot_multiplier = 2.0
            else:
                cal_target = int(tdee)
                prot_multiplier = 2.2
                
            protein_target = int(weight * prot_multiplier)
            fats_target = int((cal_target * 0.25) / 9)
            carbs_target = int((cal_target - ((protein_target * 4) + (fats_target * 9))) / 4)
            target_deadline = date.today() + timedelta(weeks=duration_w)
            
            # Flush out old user profile instances to maintain clean files
            hp_raw = pd.read_csv(health_profiles_file)
            hp_raw = hp_raw[hp_raw['Username'] != st.session_state.username]
            
            new_profile = pd.DataFrame([{
                "Username": st.session_state.username, "Age": age, "Weight": weight, "Height": height,
                "Gender": gender, "BodyFat": bf, "Goal": goal, "DietaryPreference": diet_pref,
                "MedicalIssues": med_issues, "Allergies": allergies, "TargetCalories": cal_target,
                "TargetProtein": protein_target, "TargetCarbs": carbs_target, "TargetFats": fats_target,
                "Deadline": target_deadline.strftime("%Y-%m-%d")
            }])
            
            pd.concat([hp_raw, new_profile], ignore_index=True).to_csv(health_profiles_file, index=False)
            st.success("🎉 Sports-science variables compiled and locked into database matrices cleanly! Jump to the AI Coach Tab.")
        st.markdown("</div>", unsafe_allow_html=True)

    # RE-EVALUATE ACCESS RESTRICTIONS FOR CLIENT EXPERIENCES
    hp_df = pd.read_csv(health_profiles_file)
    has_profile = (st.session_state.username in hp_df['Username'].tolist())
    is_premium = user_paid.get(st.session_state.username, False)
    
    if not has_profile:
        st.warning("⚠️ Access Gateway Engaged: Complete your Medical & Biometric Intake profile form setup first above to proceed.")
        st.stop()

    user_profile = hp_df[hp_df['Username'] == st.session_state.username].iloc[0]

    # CLIENT TAB 2: PERSONAL CERTIFIED AI TRAINER & NUTRITIONAL ASSISTANT
    with t_coach:
        st.markdown("<div class='premium-card' style='border-left: 4px solid #45A29E !important;'>", unsafe_allow_html=True)
        st.markdown(f"### 🤖 Certified AI Dashboard Workstation")
        st.write(f"**Target Vector:** `{user_profile['Goal']}` | **Calculated Timeline Horizon Target End Date:** `{user_profile['Deadline']}`")
        
        # Load any existing logs for today
        logs_df = pd.read_csv(daily_logs_file)
        today_str = date.today().strftime("%Y-%m-%d")
        today_logs = logs_df[(logs_df['Date'] == today_str) & (logs_df['Username'] == st.session_state.username)]
        
        c_p = int(today_logs['MealProtein'].sum()) if not today_logs.empty else 0
        c_c = int(today_logs['MealCarbs'].sum()) if not today_logs.empty else 0
        c_f = int(today_logs['MealFats'].sum()) if not today_logs.empty else 0
        c_cal = int(today_logs['MealCalories'].sum()) if not today_logs.empty else 0
        
        # Premium HUD Layout Panel
        st.markdown("#### 🔋 Live Daily Energy Balance Status")
        hud_cols = st.columns(4)
        hud_cols[0].markdown(f"<div class='premium-card'><span class='hud-metric-label'>Calories consumed</span><br><span class='hud-metric-val'>{c_cal}</span> <span style='color:#45A29E; font-size:11px;'>/ {user_profile['TargetCalories']} kcal</span></div>", unsafe_allow_html=True)
        hud_cols[1].markdown(f"<div class='premium-card'><span class='hud-metric-label'>Protein Input</span><br><span class='hud-metric-val'>{c_p}</span> <span style='color:#950740; font-size:11px;'>/ {user_profile['TargetProtein']} g</span></div>", unsafe_allow_html=True)
        hud_cols[2].markdown(f"<div style='opacity:{'1.0' if is_premium else '0.25'};'><div class='premium-card'><span class='hud-metric-label'>Carbohydrates</span><br><span class='hud-metric-val'>{c_c}</span> <span style='color:#45A29E; font-size:11px;'>/ {user_profile['TargetCarbs']} g</span></div></div>", unsafe_allow_html=True)
        hud_cols[3].markdown(f"<div style='opacity:{'1.0' if is_premium else '0.25'};'><div class='premium-card'><span class='hud-metric-label'>Fats Tracker</span><br><span class='hud-metric-val'>{c_f}</span> <span style='color:#8A99AD; font-size:11px;'>/ {user_profile['TargetFats']} g</span></div></div>", unsafe_allow_html=True)
        
        if not is_premium:
            st.warning("🔒 Carbohydrate and Fat tracking grids are locked under Premium Membership. Complete registration below to unblock.")
        
        # 🚨 AI NOTIFICATION AND REAL-TIME SHORTFALL RECOVERY RECOMMENDATIONS
        st.write("---")
        st.markdown("#### 📢 Automated Coach Intelligence Feedback Logs")
        
        protein_shortfall = int(user_profile['TargetProtein']) - c_p
        
        if protein_shortfall > 0:
            st.error(f"⚠️ **MACRONUTRIENT INTAKE DEFICIT DETECTED:** You are currently trailing behind your muscle recovery pace by **{protein_shortfall}g of pure protein** today!")
            
            st.markdown("##### **💡 Actionable Recovery Options Tailored To Your Profile Preferences:**")
            pref_type = "Veg" if "Veg" in user_profile['DietaryPreference'] else "Non-Veg"
            
            # Dynamic filter mapping matching dietary boundaries
            matching_rec_foods = [f for f in FOOD_NUTRITION_DATABASE if f['Type'] == pref_type or f['Name'] == "Peanut Butter 🥜"]
            
            rec_cols = st.columns(len(matching_rec_foods[:3]))
            for idx, food in enumerate(matching_rec_foods[:3]):
                required_grams = int((protein_shortfall / food['Protein']) * 100)
                with rec_cols[idx]:
                    st.markdown(f"""
                    <div style='background:#111625; padding:15px; border-radius:10px; border:1px solid #950740;'>
                        <span style='font-weight:bold; color:#FFFFFF;'>{food['Name']}</span><br>
                        <span style='font-size:12px; color:#8A99AD;'>Consume: <b>{required_grams}g</b> to clear deficit.<br>
                        Class: <b>{food['Tier']}</b></span>
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.success("🟢 **OPTIMAL PERFORMANCE RATING:** Target protein intake values satisfied for the day. Keep driving consistency.")
            
        # 📅 DYNAMIC SCIENTIFIC DAILY TRAINING SPLIT GENERATION ENGINE
        st.write("---")
        st.markdown("#### 🏋️‍♂️ Prescribed Daily Training Split Architecture")
        
        # Determine tracking split selection automatically using modern calendar date logic
        day_index = datetime.now().weekday()
        split_mapping = {0: "Chest", 1: "Back", 2: "Legs", 3: "Shoulders", 4: "Arms", 5: "Rest Day", 6: "Rest Day"}
        target_group = split_mapping.get(day_index, "Rest Day")
        
        st.info(f"📅 Today is **{datetime.now().strftime('%A')}**. Your Biological Recovery Schedule Dictates: **{target_group.upper()} SPLIT**")
        
        if target_group != "Rest Day":
            prescribed_exercises = EXERCISE_DICTIONARY[target_group]
            for idx, ex in enumerate(prescribed_exercises):
                st.markdown(f"**Exercise {idx+1}:** {ex} | `4 Sets x 8-12 Reps` (Focus on progressive load updates)")
        else:
            st.success("🧘 Today is a strategic neural rest and adaptation recovery day. Focus explicitly on hydration and recovery sleep architectures.")
        st.markdown("</div>", unsafe_allow_html=True)

    # CLIENT TAB 3: HOURLY LOG WORKSTATION (MEAL AND EXERCISE COMPLETION LOGS)
    with t_meals:
        st.markdown("<div class='premium-card'>", unsafe_allow_html=True)
        st.markdown("### 🍳 Live Daily Telemetry Input Station")
        st.write("Commit items consumed or completed on the floor to update your dashboard tracking logs.")
        
        m_col1, m_col2 = st.columns(2)
        
        with m_col1:
            st.markdown("#### **🥗 Quick Log Diet Intake**")
            selected_food_item = st.selectbox("Select Eaten Item from Matrix:", [f['Name'] for f in FOOD_NUTRITION_DATABASE])
            consumed_weight_g = st.number_input("Portion Serving Weight Mass Scale (Grams):", min_value=10, max_value=1000, value=100, step=10)
            
            if st.button("Log Meal Entry to Core Registry", use_container_width=True):
                food_profile = next(f for f in FOOD_NUTRITION_DATABASE if f['Name'] == selected_food_item)
                factor = consumed_weight_g / 100.0
                
                f_p = food_profile['Protein'] * factor
                f_c = food_profile['Carbs'] * factor
                f_f = food_profile['Fats'] * factor
                f_cal = ((f_p * 4) + (f_c * 4) + (f_f * 9))
                
                pd.DataFrame([{
                    "Date": date.today().strftime("%Y-%m-%d"), "Username": st.session_state.username,
                    "MealProtein": f_p, "MealCarbs": f_c, "MealFats": f_f, "MealCalories": f_cal,
                    "ExercisesExecuted": "None"
                }]).to_csv(daily_logs_file, mode='a', header=False, index=False)
                st.success("Meal matrix tracked successfully!")
                st.rerun()
                
        with m_col2:
            st.markdown("#### **🏋️‍♂️ Track Performed Exercise**")
            all_possible_exercises = []
            for v in EXERCISE_DICTIONARY.values(): all_possible_exercises.extend(v)
            
            ex_logged = st.selectbox("Select Executed Movement:", all_possible_exercises)
            sets_done = st.number_input("Sets Completed Successfully:", min_value=1, max_value=10, value=4)
            weight_used = st.number_input("Top Set Working Weight Load (kg):", min_value=1, max_value=300, value=60)
            
            if st.button("Log Workout Completion Set", use_container_width=True):
                pd.DataFrame([{
                    "Date": date.today().strftime("%Y-%m-%d"), "Username": st.session_state.username,
                    "MealProtein": 0, "MealCarbs": 0, "MealFats": 0, "MealCalories": 0,
                    "ExercisesExecuted": f"{ex_logged} ({sets_done}x{weight_used}kg)"
                }]).to_csv(daily_logs_file, mode='a', header=False, index=False)
                st.success("Performance payload written to disk database logs successfully!")
                st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    # CLIENT TAB 4: TRANSACTION ACTIVATION MODULE
    with t_pay:
        st.markdown("<div class='premium-card'>", unsafe_allow_html=True)
        st.markdown("### 💳 Premium Network Activation Hub")
        if is_premium:
            st.success("👑 MASTER LICENSE SIGNATURE DETECTED: All premium AI tracking parameters and macronutrient algorithms are completely unblocked.")
        else:
            st.warning("🔒 YOUR CURRENT ACCOUNT IS OPERATING ON THE DEMO LICENSE STRATA. Carb/Fat visualizations and advanced coaching panels are currently restricted.")
            st.write("Scan the merchant point token details below to initiate activation:")
            
            pay_cols = st.columns([1.2, 1])
            with pay_cols[0]:
                st.markdown("#### **UPI Clearance Directives**\n1. Launch phone financial payment nodes (GPay, PhonePe, Bhim, Paytm).\n2. Remit structural package licensing fees to merchant handle: `hanumangym@ybl`.\n3. Present validation codes to Coach Varshith to toggle your license flag.")
            with pay_cols[1]:
                qr_html = """
                <div style='border: 2px solid #950740; padding: 20px; border-radius: 10px; background-color: #ffffff; text-align: center; width: 200px; margin: auto;'>
                    <h5 style='color: #111111; margin-top: 0; font-family: sans-serif;'>HANUMAN MERCH</h5>
                    <div style='background-color: #0B0C10; width: 140px; height: 140px; margin: auto; border-radius: 6px; display: flex; align-items: center; justify-content: center;'>
                        <span style='color: #45A29E; font-size: 10px; font-weight: bold; font-family: monospace;'>[ UPI CODE ]</span>
                    </div>
                </div>
                """
                st.markdown(qr_html, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
