import streamlit as st
from openai import OpenAI
import requests
from bs4 import BeautifulSoup
import time

# --- AIford 2.0: Cyber-Aesthetic Edition ---
st.set_page_config(page_title="AIford | Ultra", layout="wide", page_icon="⚡")

# THE "GLOW-UP" CSS
st.markdown("""
    <style>
    /* Global Styles */
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Inter:wght@300;600&display=swap');
    
    .stApp {
        background: radial-gradient(circle at top right, #0d1b2a, #010101);
        color: #e0e0e0;
        font-family: 'Inter', sans-serif;
    }

    /* The Neon Header */
    .neon-card {
        background: rgba(255, 255, 255, 0.03);
        border-radius: 30px;
        padding: 50px;
        text-align: center;
        border: 1px solid rgba(0, 255, 255, 0.2);
        box-shadow: 0 0 20px rgba(0, 255, 255, 0.1), inset 0 0 20px rgba(0, 255, 255, 0.05);
        margin-bottom: 40px;
    }

    .balance-label { font-family: 'Orbitron', sans-serif; color: #00f2ff; text-transform: uppercase; letter-spacing: 3px; font-size: 14px; }
    
    .balance-huge {
        font-family: 'Orbitron', sans-serif;
        font-size: 80px;
        font-weight: 700;
        color: #ffffff;
        text-shadow: 0 0 30px rgba(0, 242, 255, 0.6);
        margin: 10px 0;
    }

    /* Buttons with Glow */
    .stButton>button {
        background: linear-gradient(90deg, #00f2ff, #7000ff);
        color: white;
        border: none;
        border-radius: 15px;
        padding: 15px 30px;
        font-weight: bold;
        transition: 0.3s;
        box-shadow: 0 0 15px rgba(0, 242, 255, 0.4);
    }
    .stButton>button:hover {
        transform: scale(1.05);
        box-shadow: 0 0 25px rgba(0, 242, 255, 0.6);
    }

    /* Glassmorphism Chat */
    .stChatMessage {
        background: rgba(255, 255, 255, 0.05) !important;
        backdrop-filter: blur(15px);
        border-radius: 20px !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        margin-bottom: 15px;
    }

    /* Custom Scrollbar */
    ::-webkit-scrollbar { width: 8px; }
    ::-webkit-scrollbar-track { background: #010101; }
    ::-webkit-scrollbar-thumb { background: #7000ff; border-radius: 10px; }
    </style>
""", unsafe_allow_html=True)

# --- THE VAULT (Top Hero Section) ---
st.markdown('<div class="neon-card">', unsafe_allow_html=True)
balance = st.session_state.get('balance', 2540.80)
st.markdown('<p class="balance-label">Available Wealth</p>', unsafe_allow_html=True)
st.markdown(f'<h1 class="balance-huge">${balance:,.2f}</h1>', unsafe_allow_html=True)

col1, col2, col3 = st.columns([1,1,1])
with col2:
    if st.button("⚡ SYNC NEURAL BANK"):
        with st.status("Accessing Mainframe..."):
            time.sleep(1)
            st.session_state.balance = 15720.45
            st.session_state.sync_glow = True
        st.rerun()
st.markdown('</div>', unsafe_allow_html=True)

# --- MAIN INTERFACE ---
col_chat, col_feed = st.columns([2, 1], gap="large")

with col_chat:
    st.markdown("### 🤖 AIford Neural Advisor")
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": "System Online. Your finances are encrypted and ready for analysis."}]

    for m in st.session_state.messages:
        with st.chat_message(m["role"]):
            st.markdown(m["content"])

    if prompt := st.chat_input("Can I afford a new graphics card?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            # Connection to Local RTX 4070 Ti Super
            client = OpenAI(base_url="http://127.0.0.1:1234/v1", api_key="lm-studio")
            
            with st.spinner("Decoding Market Data..."):
                try:
                    # Logic
                    safe_limit = balance - 1000.0
                    
                    response = client.chat.completions.create(
                        model="local-model",
                        messages=[{"role": "user", "content": f"Balance: ${balance}. Safe to spend: ${safe_limit}. Question: {prompt}. Be a cool, firm AI bodyguard."}],
                        timeout=30
                    )
                    
                    reply = response.choices[0].message.content
                    st.markdown(f"**Advisor:** {reply}")
                    st.session_state.messages.append({"role": "assistant", "content": reply})
                except Exception as e:
                    st.error(f"⚠️ Brain Offline: {e}")

with col_feed:
    st.markdown("### 📡 Live Signal")
    
    # Fraud Alert (Glowing Red)
    if st.session_state.get('sync_glow'):
        st.markdown("""
            <div style="background: rgba(255,0,0,0.1); border: 1px solid #ff0000; padding: 15px; border-radius: 15px; color: #ff4b4b; margin-bottom: 20px;">
                <strong>🚨 THREAT DETECTED</strong><br>
                Suspicious login attempt from: <b>Seoul, KR</b><br>
                <small>Auto-blocking in 3... 2... 1...</small>
            </div>
        """, unsafe_allow_html=True)

    # Activity Feed
    st.markdown('<p style="color:#7000ff; font-weight:bold; font-size:12px;">ENCRYPTED LEDGER</p>', unsafe_allow_html=True)
    txns = [
        ("Nvidia Store", "-$899.00"),
        ("Steam Games", "-$59.99"),
        ("Tesla Supercharger", "-$22.40"),
        ("Monthly Salary", "+$4,200.00")
    ]
    for vendor, price in txns:
        color = "#00ff88" if "+" in price else "#ffffff"
        st.markdown(f"""
            <div style="background: rgba(255,255,255,0.02); padding: 12px; border-radius: 10px; margin-bottom: 8px; border-left: 3px solid #7000ff;">
                <span style="font-size: 14px;">{vendor}</span>
                <span style="float: right; color: {color}; font-weight: bold;">{price}</span>
            </div>
        """, unsafe_allow_html=True)