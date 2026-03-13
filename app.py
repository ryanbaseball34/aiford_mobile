import streamlit as st
import plotly.graph_objects as go
from openai import OpenAI
import pandas as pd
import webbrowser

# --- AIford 1.0: Monarch Executive Build ---
st.set_page_config(page_title="AIford Wealth", layout="wide", page_icon="🏦")

# MONARCH-LEVEL CUSTOM CSS
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600;800&display=swap');
    
    html, body, [class*="st-"] { font-family: 'Plus Jakarta Sans', sans-serif; }
    .stApp { background-color: #f8fafc; color: #1e293b; }
    
    /* Monarch Header */
    .header-container { background: white; padding: 2rem; border-bottom: 1px solid #e2e8f0; margin-bottom: 2rem; }
    .balance-label { color: #64748b; font-size: 0.875rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; }
    .balance-main { font-size: 3rem; font-weight: 800; color: #0f172a; margin: 0; }
    
    /* Search Bar */
    .search-input {
        width: 100%; padding: 15px 25px; border-radius: 50px; border: 1px solid #e2e8f0;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05); font-size: 16px; outline: none;
    }

    /* Transaction Card */
    .txn-card { background: white; padding: 1rem; border-radius: 12px; border: 1px solid #e2e8f0; margin-bottom: 0.75rem; display: flex; justify-content: space-between; align-items: center; }
    .txn-vendor { font-weight: 600; color: #0f172a; }
    .txn-amt { font-weight: 700; }

    /* Advisor Chat */
    .stChatMessage { border-radius: 12px !important; border: 1px solid #e2e8f0 !important; background: white !important; }
    
    header {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# --- 1. TOP SECTION: THE MONARCH DASHBOARD ---
st.markdown('<div class="header-container">', unsafe_allow_html=True)
col_bal, col_chart = st.columns([1, 2])

with col_bal:
    st.markdown('<p class="balance-label">Total Net Worth</p>', unsafe_allow_html=True)
    balance = 142250.80
    st.markdown(f'<h1 class="balance-main">${balance:,.2f}</h1>', unsafe_allow_html=True)
    st.markdown('<p style="color: #10b981; font-weight: 700; margin:0;">↑ $1,240.50 (Last 30 days)</p>', unsafe_allow_html=True)

with col_chart:
    # Monarch-style area chart
    df = pd.DataFrame({'Month': ['Oct', 'Nov', 'Dec', 'Jan', 'Feb', 'Mar'], 'Val': [130000, 132500, 138000, 135000, 140000, 142250]})
    fig = go.Figure(go.Scatter(x=df['Month'], y=df['Val'], fill='tozeroy', line=dict(color='#3b82f6', width=3), fillcolor='rgba(59, 130, 246, 0.05)'))
    fig.update_layout(height=120, margin=dict(l=0,r=0,t=0,b=0), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', xaxis=dict(visible=False), yaxis=dict(visible=False))
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
st.markdown('</div>', unsafe_allow_html=True)

# --- 2. MAIN INTERFACE ---
col_sidebar, col_main = st.columns([1, 2.5], gap="large")

with col_sidebar:
    st.subheader("Bank Accounts")
    # Simulated Accounts
    accounts = [("Checking", "$12,450.00"), ("Savings", "$50,107.55"), ("Investment", "$79,693.25")]
    for name, amt in accounts:
        st.markdown(f"""
            <div class="txn-card">
                <div><b>{name}</b><br><small style="color:#64748b">Synced 2m ago</small></div>
                <div style="font-weight:700;">{amt}</div>
            </div>
        """, unsafe_allow_html=True)
    
    st.divider()
    st.subheader("Recent Moves")
    txns = [("Apple Store", "-$2,499.00"), ("Whole Foods", "-$82.40"), ("Salary Deposit", "+$4,500.00")]
    for v, a in txns:
        st.markdown(f"""
            <div class="txn-card">
                <span>{v}</span>
                <span style="color: {'#10b981' if '+' in a else '#1e293b'}">{a}</span>
            </div>
        """, unsafe_allow_html=True)

with col_main:
    # Google Search Functionality
    search_query = st.text_input("🔍 Search Market or Ask Advisor...", placeholder="Search Google or analyze wealth...")
    if search_query and not search_query.startswith("Can I"):
        # This opens a new tab for Google results automatically
        st.markdown(f'<meta http-equiv="refresh" content="0; url=https://www.google.com/search?q={search_query}">', unsafe_allow_html=True)

    st.divider()

    # Chatbot Logic
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": "I'm AIford. Your wealth is secure. How can I assist with your March allocations?"}]

    for m in st.session_state.messages:
        with st.chat_message(m["role"]):
            st.markdown(m["content"])

    if prompt := st.chat_input("Analyze my spending..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            try:
                # ACCESSING THE BRAIN
                api_key = st.secrets["GROQ_API_KEY"]
                client = OpenAI(base_url="https://api.groq.com/openai/v1", api_key=api_key)
                
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "user", "content": f"Balance: ${balance}. User: {prompt}"}]
                )
                full_response = response.choices[0].message.content
                st.markdown(full_response)
                st.session_state.messages.append({"role": "assistant", "content": full_response})
            except Exception as e:
                st.error(f"Brain Error: {e}")
                st.info("Check your Streamlit Secrets for 'GROQ_API_KEY'")
