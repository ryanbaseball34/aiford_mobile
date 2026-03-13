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
    
    /* Custom Input Styling */
    .stTextInput input {
        border-radius: 8px !important; border: 1px solid #e4e4e7 !important;
        padding: 12px 16px !important; background: #fafafa !important;
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
    if 'balance' not in st.session_state:
        st.session_state.balance = 687041.79
    
    st.markdown(f'<p class="net-worth-val">${st.session_state.balance:,.2f} <span style="color:#10b981; font-size:16px; margin-left:10px;">↑ 3.5%</span></p>', unsafe_allow_html=True)

with col_btns:
    st.write("## ") # Spacing
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
    # 3. GOOGLE SEARCH BAR
    st.markdown("### 🔍 Global Market Search")
    search_q = st.text_input("Search live prices or market trends...", placeholder="e.g. 2026 Toyota RAV4 Hybrid Price", label_visibility="collapsed")
    
    if search_q:
        # Check if it's an AI question or a Google search
        if any(word in search_q.lower() for word in ["can i", "analyze", "should i"]):
             st.info("💡 Tip: Ask this in the 'Neural Advisor' box below for detailed financial analysis.")
        else:
             st.success(f"Searching Google for: {search_q}")
             st.markdown(f'<meta http-equiv="refresh" content="0; url=https://www.google.com/search?q={search_q}">', unsafe_allow_html=True)

    # 4. PERFORMANCE CHART
    st.markdown('<div class="card"><strong>Net worth performance</strong>', unsafe_allow_html=True)
    df = pd.DataFrame({
        'Date': ['Nov 6', 'Nov 13', 'Nov 20', 'Nov 27', 'Dec 6'],
        'Value': [663000, 668000, 674000, 681000, st.session_state.balance]
    })
    fig = go.Figure(go.Scatter(x=df['Date'], y=df['Value'], fill='tozeroy', line=dict(color='#0ea5e9', width=3), fillcolor='rgba(14, 165, 233, 0.05)'))
    fig.update_layout(height=250, margin=dict(l=0,r=0,t=10,b=0), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', xaxis=dict(showgrid=False), yaxis=dict(side="right", gridcolor="#f4f4f5"))
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    st.markdown('</div>', unsafe_allow_html=True)

    # 5. NEURAL ADVISOR
    st.markdown("### 🤖 Neural Advisor")
    
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": "I'm AIford. Ready to analyze your wealth strategy. Ask me anything."}]

    for m in st.session_state.messages:
        with st.chat_message(m["role"]):
            st.markdown(m["content"])

    if chat_input := st.chat_input("Ask about your finances..."):
        st.session_state.messages.append({"role": "user", "content": chat_input})
        with st.chat_message("user"):
            st.markdown(chat_input)

        with st.chat_message("assistant"):
            try:
                # Use st.secrets to securely access your Groq Key
                client = OpenAI(base_url="https://api.groq.com/openai/v1", api_key=st.secrets["GROQ_API_KEY"])
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "user", "content": f"Balance: ${st.session_state.balance}. Query: {chat_input}"}]
                )
                answer = response.choices[0].message.content
                st.markdown(answer)
                st.session_state.messages.append({"role": "assistant", "content": answer})
            except Exception as e:
                st.error("Brain Connection Pending. Make sure 'GROQ_API_KEY' is set in Streamlit Secrets.")
