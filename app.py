import streamlit as st
import plotly.graph_objects as go
from openai import OpenAI
import pandas as pd
import time

# --- AIford 1.0: Monarch Executive Edition ---
st.set_page_config(page_title="AIford Wealth", layout="wide", page_icon="🏦")

# CLEAN EXECUTIVE CSS
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    .stApp { background-color: #ffffff; color: #1a1d21; font-family: 'Inter', sans-serif; }
    
    /* Top Header */
    .header-bar {
        padding: 20px 0; border-bottom: 1px solid #f0f0f0; margin-bottom: 30px;
        display: flex; justify-content: space-between; align-items: flex-end;
    }
    
    .net-worth-label { color: #71717a; font-size: 12px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px; }
    .net-worth-val { font-size: 36px; font-weight: 700; color: #18181b; margin: 0; }
    
    /* Content Cards */
    .card {
        background: white; border: 1px solid #e4e4e7; border-radius: 12px;
        padding: 24px; margin-bottom: 20px;
    }
    
    .account-row {
        display: flex; justify-content: space-between; padding: 12px 0;
        border-bottom: 1px solid #f4f4f5; font-size: 14px;
    }
    
    /* Buttons */
    .stButton>button {
        border-radius: 8px !important; font-weight: 600 !important;
    }

    /* Hide UI noise */
    header {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# --- 1. THE TOP SECTION ---
col_net, col_btns = st.columns([2, 1])

with col_net:
    st.markdown('<p class="net-worth-label">Net Worth</p>', unsafe_allow_html=True)
    # Using a state-based balance so "Add Account" can change it
    if 'balance' not in st.session_state:
        st.session_state.balance = 687041.79
    
    st.markdown(f'<p class="net-worth-val">${st.session_state.balance:,.2f} <span style="color:#10b981; font-size:16px; margin-left:10px;">↑ 3.5%</span></p>', unsafe_allow_html=True)

with col_btns:
    st.write("## ") # Padding
    sub_col1, sub_col2 = st.columns(2)
    with sub_col1:
        if st.button("Refresh All", use_container_width=True):
            st.toast("Syncing accounts...")
    with sub_col2:
        if st.button("＋ Add Account", type="primary", use_container_width=True):
            with st.status("Connecting to Financial Institution..."):
                time.sleep(1.5)
                st.session_state.balance += 12500.00
                st.session_state.new_account = True
            st.success("New Account Linked!")
            st.rerun()

st.divider()

# --- 2. MAIN LAYOUT ---
col_side, col_main = st.columns([1, 2.5], gap="large")

with col_side:
    st.subheader("Accounts")
    
    # Cash Section
    st.markdown("""<div class="card"><strong>Cash</strong><span style="float:right; color:#71717a;">$65,342.30</span>""", unsafe_allow_html=True)
    st.markdown('<div class="account-row"><span>Melanie\'s Checking</span><b>$15,234.75</b></div>', unsafe_allow_html=True)
    st.markdown('<div class="account-row"><span>Joint Savings</span><b>$50,107.55</b></div>', unsafe_allow_html=True)
    if st.session_state.get('new_account'):
         st.markdown('<div class="account-row" style="background:#f0fdf4;"><span>New Connected Account</span><b>$12,500.00</b></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Investments Section
    st.markdown("""<div class="card"><strong>Investments</strong><span style="float:right; color:#71717a;">$542,301.55</span>""", unsafe_allow_html=True)
    st.markdown('<div class="account-row"><span>Jon\'s 401k</span><b>$180,336.73</b></div>', unsafe_allow_html=True)
    st.markdown('<div class="account-row"><span>Brokerage</span><b>$361,964.82</b></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col_main:
    # 3. GOOGLE SEARCH (Centered & Prominent)
    st.markdown("### 🔍 Global Market Search")
    search_q = st.text_input("Search Google for live prices, models, or trends...", placeholder="e.g. 2026 Toyota RAV4 Hybrid Price", label_visibility="collapsed")
    
    if search_q:
        # Check if it's a question for the AI or a search for Google
        if any(word in search_q.lower() for word in ["can i", "analyze", "should i"]):
             st.info("💡 Tip: Ask this in the 'Neural Advisor' box below for a
