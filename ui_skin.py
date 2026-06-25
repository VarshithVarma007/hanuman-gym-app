import streamlit as st

def inject_premium_skin():
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
