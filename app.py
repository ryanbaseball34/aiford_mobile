import streamlit as st
import plotly.graph_objects as go
from openai import OpenAI
import pandas as pd

# --- AIford 1.0: Monarch Executive Build ---
st.set_page_config(page_title="AIford Wealth", layout="wide", page_icon="🧡")

# MONARCH-LEVEL CUSTOM CSS
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Executive White Aesthetic */
    .stApp { background-color: #ffffff; color: #1a1d21; font-family: 'Inter', sans-serif; }
    
    /* Top Navigation Bar */
    .monarch-header {
        background: white; padding: 15px 30px; border-bottom: 1px solid #f0f0f0;
        display: flex; justify-content: space-between; align-items: center;
        position: sticky; top: 0; z-index: 999;
    }
    
    .net-worth-label { color: #71717a; font-size: 12px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px; }
    .net-worth-val { font-size: 28px; font-weight: 700; color: #18181b; margin: 0; }
    .growth-pill { color: #10b981; background: #f0fdf4; padding: 4px 8px; border-radius: 6px; font-weight: 600; font-size: 13px; }

    /* Cards */
    .card {
        background: white; border: 1px solid #e4e4e7; border-radius: 12px;
        padding: 20px; margin-bottom: 15px; box-shadow: 0 1px 2px rgba(0,0,0,0.03);
    }
    
    /* Account Rows */
    .account-row {
        display: flex; justify-content: space-between; padding: 10px 0;
        border-bottom: 1px solid #f4f4f5; align-items: center;
    }
    .account-name { font-weight: 500; color: #3f3f46; font-size: 14px; }
    .account-bal { font-weight: 600; color: #18181b; font-size: 14px; }

    /* Unified Search Bar */
    .stTextInput input {
        border-radius: 10px !important; border: 1px solid #e4e4e7 !important;
        padding: 12px 16px !important; background: #f9fafb !important; font-size: 16px !important;
    }

    /* Chat Styling */
    .stChatMessage { background: #f9fafb !important; border: 1px solid #f3f4f6 !important; border-radius: 12px !important; }
    
    /* Clean UI Overrides */
    header {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# --- 1. TOP NAV BAR (Sticky) ---
st.markdown("""
    <div class="monarch-header">
        <div>
            <span class="net-worth-label">Net Worth</span>
            <div style="display: flex; align-items: center; gap: 12px;">
                <p class="net-worth-val">$687,041.79</p>
                <span class="growth-pill">↑ $23,542.96 (3.5%)</span>
            </div>
        </div>
        <div style="display:flex; gap:10px;">
            <button style="border: 1px solid #e4e4e7; background:white; padding:8px 14px; border-radius:6px; cursor:pointer; font-size:13px; font-weight:500;">Refresh</button>
            <button style="border: none; background:#ea580c; color:white; padding:8px 14px; border-radius:6px; cursor:pointer; font-size:13px; font-weight:600;">+ Add account</button>
        </div>
    </div>
""", unsafe_allow_html=True)

# --- 2. LAYOUT ---
col_side, col_main = st.columns([1, 2.8], gap="medium")

with col_side:
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Cash Accounts
    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("<p style='font-weight:700; font-size:15px; margin-bottom:10px;'>Cash <span style='float:right; color:#71717a; font-weight:400;'>$65,342.30</span></p>", unsafe_allow_html=True)
        cash_accounts = [("Melanie's Checking", "$15,234.75"), ("Joint Savings", "$50,107.55")]
        for name, amt in cash_accounts:
            st.markdown(f'<div class="account-row"><span class="account-name">{name}</span><span class="account-bal">{amt}</span></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # Investments
    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("<p style='font-weight:700; font-size:15px; margin-bottom:10px;'>Investments <span style='float:right; color:#71717a; font-weight:400;'>$542,301.55</span></p>", unsafe_allow_html=True)
        inv_accounts = [("Jon's 401k", "$180,336.73"), ("Brokerage", "$361,964.82")]
        for name, amt in inv_accounts:
            st.markdown(f'<div class="account-row"><span class="account-name">{name}</span><span class="account-bal">{amt}</span></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

with col_main:
    st.markdown("<br>", unsafe_allow_html=True)
    
    # 3. SEARCH BAR (Top of Feed)
    search_q = st.text_input("", placeholder="Search transactions or ask your neural advisor...", key="main_search")
    
    # Google Search Logic: If they hit enter and it's not a question, go to Google
    if search_q and not any(word in search_q.lower() for word in ["can", "how", "what", "analyze"]):
        st.markdown(f'<meta http-equiv="refresh" content="0; url=https://www.google.com/search?q={search_q}">', unsafe_allow_html=True)

    # 4. MAIN CHART CARD
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("<p style='font-weight:600; color:#18181b; margin-bottom:15px;'>Net worth performance</p>", unsafe_allow_html=True)
    
    df = pd.DataFrame({
        'Date': ['Nov 6', 'Nov 13', 'Nov 20', 'Nov 27', 'Dec 6'],
        'Value': [663000, 668000, 674000, 681000, 687041]
    })
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['Date'], y=df['Value'], fill='tozeroy', 
                             line=dict(color='#0ea5e9', width=3), 
                             fillcolor='rgba(14, 165, 233, 0.04)', mode='lines'))
    fig.update_layout(height=280, margin=dict(l=0,r=0,t=0,b=0), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', 
                      xaxis=dict(showgrid=False, color="#a1a1aa", tickfont=dict(size=10)), 
                      yaxis=dict(side="right", gridcolor="#f4f4f5", color="#a1a1aa", tickfont=dict(size=10)))
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    st.markdown('</div>', unsafe_allow_html=True)

    # 5. NEURAL ADVISOR CHAT (Bottom of Feed)
    st.markdown("### Neural Advisor")
    
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": "Welcome to AIford. I've analyzed your March cash flow. You are tracking $1,200 ahead of your savings goal."}]

    for m in st.session_state.messages:
        with st.chat_message(m["role"]):
            st.markdown(m["content"])

    if chat_input := st.chat_input("Analyze my wealth strategy..."):
        st.session_state.messages.append({"role": "user", "content": chat_input})
        with st.chat_message("user"):
            st.markdown(chat_input)

        with st.chat_message("assistant"):
            try:
                # ACCESSING THE CLOUD BRAIN
                client = OpenAI(base_url="https://api.groq.com/openai/v1", api_key=st.secrets["GROQ_API_KEY"])
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "user", "content": f"Balance: $687,041. Query: {chat_input}"}]
                )
                st.markdown(response.choices[0].message.content)
                st.session_state.messages.append({"role": "assistant", "content": response.choices[0].message.content})
            except Exception as e:
                st.error("Brain Connection Pending. Make sure 'GROQ_API_KEY' is in your Streamlit Secrets.")
