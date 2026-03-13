import streamlit as st
import plotly.graph_objects as go
from openai import OpenAI
import pandas as pd

# --- AIford 1.0: Origin/Monarch Executive Build ---
st.set_page_config(page_title="AIford | Wealth", layout="wide", page_icon="🧡")

# THE "CLEAN TECH" CSS Re-build
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Force white background and clean typography */
    .stApp { background-color: #ffffff; color: #1a1d21; font-family: 'Inter', sans-serif; }
    
    /* Clean Top Header */
    .monarch-header {
        background: white; padding: 20px 40px; border-bottom: 1px solid #f0f0f0;
        display: flex; justify-content: space-between; align-items: center;
    }
    
    .net-worth-label { color: #71717a; font-size: 13px; font-weight: 500; text-transform: uppercase; letter-spacing: 0.5px; }
    .net-worth-val { font-size: 32px; font-weight: 700; color: #18181b; margin: 0; }
    .growth-pill { color: #10b981; background: #f0fdf4; padding: 4px 10px; border-radius: 6px; font-weight: 600; font-size: 14px; }

    /* Cards & Containers */
    .card {
        background: white; border: 1px solid #e4e4e7; border-radius: 12px;
        padding: 24px; margin-bottom: 20px; box-shadow: 0 1px 3px rgba(0,0,0,0.02);
    }
    
    /* Sidebar / Account List */
    .account-row {
        display: flex; justify-content: space-between; padding: 12px 0;
        border-bottom: 1px solid #f4f4f5; align-items: center;
    }
    .account-name { font-weight: 500; color: #27272a; }
    .account-bal { font-weight: 600; color: #18181b; }

    /* The Search Bar (Origin Style) */
    .stTextInput input {
        border-radius: 8px !important; border: 1px solid #e4e4e7 !important;
        padding: 12px 16px !important; background: #fafafa !important;
    }

    /* Advisor Chat (Simplified) */
    .stChatMessage { background: #f9fafb !important; border: none !important; border-radius: 12px !important; }
    
    /* Hide Default Elements */
    header {visibility: hidden;}
    footer {visibility: hidden;}
    #MainMenu {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# --- 1. TOP NAVIGATION BAR ---
st.markdown("""
    <div class="monarch-header">
        <div>
            <span class="net-worth-label">Net Worth</span>
            <div style="display: flex; align-items: center; gap: 15px;">
                <p class="net-worth-val">$687,041.79</p>
                <span class="growth-pill">↑ $23,542.96 (3.5%)</span>
            </div>
        </div>
        <div style="display:flex; gap:10px;">
            <button style="border: 1px solid #e4e4e7; background:white; padding:8px 16px; border-radius:6px; cursor:pointer; font-weight:500;">Refresh all</button>
            <button style="border: none; background:#ea580c; color:white; padding:8px 16px; border-radius:6px; cursor:pointer; font-weight:500;">+ Add account</button>
        </div>
    </div>
""", unsafe_allow_html=True)

# --- 2. MAIN DASHBOARD LAYOUT ---
col_sidebar, col_main = st.columns([1, 2.8], gap="large")

with col_sidebar:
    st.markdown("### Accounts")
    
    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("**Cash** <span style='float:right; color:#71717a;'>$65,342.30</span>", unsafe_allow_html=True)
        accounts = [("Chase Checking", "$15,234.75"), ("Joint Savings", "$50,107.55")]
        for name, amt in accounts:
            st.markdown(f'<div class="account-row"><span class="account-name">{name}</span><span class="account-bal">{amt}</span></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("**Credit Cards** <span style='float:right; color:#71717a;'>$2,828.99</span>", unsafe_allow_html=True)
        cards = [("Amex Gold", "$2,104.50"), ("Chase Sapphire", "$724.49")]
        for name, amt in cards:
            st.markdown(f'<div class="account-row"><span class="account-name">{name}</span><span class="account-bal">{amt}</span></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

with col_main:
    # 3. GOOGLE SEARCH HUB
    search_query = st.text_input("", placeholder="Search Google or ask your neural advisor...", key="main_search")
    if search_query and not (search_query.lower().startswith("can i") or search_query.lower().startswith("how")):
        st.markdown(f'<meta http-equiv="refresh" content="0; url=https://www.google.com/search?q={search_query}">', unsafe_allow_html=True)

    # 4. CHARTING (Monarch Performance Style)
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("**Net worth performance**", unsafe_allow_html=True)
    
    df = pd.DataFrame({
        'Day': ['Nov 6', 'Nov 14', 'Nov 22', 'Nov 30', 'Dec 6'],
        'Value': [663000, 672000, 675000, 680000, 687041]
    })
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['Day'], y=df['Value'], fill='tozeroy', line=dict(color='#0ea5e9', width=3), fillcolor='rgba(14, 165, 233, 0.05)', mode='lines'))
    fig.update_layout(height=250, margin=dict(l=0,r=0,t=10,b=0), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', 
                      xaxis=dict(showgrid=False, color="#a1a1aa"), yaxis=dict(side="right", gridcolor="#f4f4f5", color="#a1a1aa"))
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    st.markdown('</div>', unsafe_allow_html=True)

    # 5. ADVISOR CHATBOT
    st.markdown("### Neural Advisor")
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": "Welcome. I've analyzed your cash flow. You're tracking 3% ahead of your March goal."}]

    for m in st.session_state.messages:
        with st.chat_message(m["role"]):
            st.markdown(m["content"])

    if prompt := st.chat_input("Analyze my wealth strategy..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            try:
                # Using Groq for the Cloud Build
                client = OpenAI(base_url="https://api.groq.com/openai/v1", api_key=st.secrets["GROQ_API_KEY"])
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "user", "content": f"Balance: $687,041. User query: {prompt}"}]
                )
                full_reply = response.choices[0].message.content
                st.markdown(full_reply)
                st.session_state.messages.append({"role": "assistant", "content": full_reply})
            except Exception as e:
                st.error("Brain Connection Pending. Ensure your GROQ_API_KEY is in Secrets.")
