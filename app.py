import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, date

# Local imports
import database as db
import learning_data as ld
import market_data as md
import simulator as sim
import ai_coach as coach

# Page Configuration
st.set_page_config(
    page_title="Finly — Personal Finance & Financial Literacy",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load Custom CSS
def load_css():
    try:
        with open("styles.css", "r", encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except Exception:
        pass

load_css()

# Initialize Database
db.init_db()

# Initialize Session State Variables
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "user" not in st.session_state:
    st.session_state.user = {"email": "demo@finly.app", "name": "Alex Demo"}
if "current_page" not in st.session_state:
    st.session_state.current_page = "Dashboard"
if "quiz_states" not in st.session_state:
    st.session_state.quiz_states = {}
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        {"role": "assistant", "content": "👋 Hi there! I'm your Finly AI Coach. Ask me any question about budgeting, stocks, SIPs, or your expense insights!"}
    ]

# Helper function to return to dashboard
def render_back_to_dashboard():
    col1, col2 = st.columns([1, 6])
    with col1:
        if st.button("← Dashboard", key="btn_back_dash"):
            st.session_state.current_page = "Dashboard"
            st.rerun()

# ----------------------------------------------------
# AUTHENTICATION SCREEN
# ----------------------------------------------------
def render_auth_page():
    st.markdown("<br><br>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 2, 1])
    
    with c2:
        st.markdown("""
        <div style='text-align: center; margin-bottom: 25px;'>
            <h1 style='font-size: 3rem; margin-bottom: 5px; color: #FFFFFF;'>⚡ <span style='color: #FF7A00;'>Finly</span></h1>
            <p style='font-size: 1.1rem; color: #A1A1AA;'>Your Beginner-Friendly Personal Finance & Literacy Coach</p>
        </div>
        """, unsafe_allow_html=True)
        
        tab_login, tab_signup = st.tabs(["🔒 Sign In", "✨ Sign Up"])
        
        with tab_login:
            st.markdown("<div class='finly-card'>", unsafe_allow_html=True)
            email_input = st.text_input("Email Address", value="demo@finly.app", key="login_email")
            pass_input = st.text_input("Password", value="••••••••", type="password", key="login_pass")
            
            col_a, col_b = st.columns(2)
            with col_a:
                if st.button("Sign In", use_container_width=True, key="btn_login"):
                    st.session_state.authenticated = True
                    st.session_state.user = {"email": email_input, "name": email_input.split("@")[0].title()}
                    st.session_state.current_page = "Dashboard"
                    st.rerun()
            with col_b:
                if st.button("Continue as Demo User 🚀", use_container_width=True, key="btn_demo_login"):
                    st.session_state.authenticated = True
                    st.session_state.user = {"email": "demo@finly.app", "name": "Demo Investor"}
                    st.session_state.current_page = "Dashboard"
                    st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)
            
        with tab_signup:
            st.markdown("<div class='finly-card'>", unsafe_allow_html=True)
            su_name = st.text_input("Full Name", value="New Learner", key="su_name")
            su_email = st.text_input("Email Address", value="user@example.com", key="su_email")
            su_pass = st.text_input("Create Password", type="password", key="su_pass")
            
            if st.button("Create Account & Start Learning", use_container_width=True, key="btn_signup"):
                st.session_state.authenticated = True
                st.session_state.user = {"email": su_email, "name": su_name}
                st.session_state.current_page = "Dashboard"
                st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)

# ----------------------------------------------------
# DASHBOARD (MAIN LANDING PAGE)
# ----------------------------------------------------
def render_dashboard():
    st.markdown(f"""
    <div style='margin-bottom: 30px;'>
        <h1 style='font-size: 2.6rem; margin-bottom: 6px; color: #FFFFFF;'>
            Welcome back, {st.session_state.user['name']} 👋
        </h1>
        <p style='font-size: 1.1rem; color: #A1A1AA;'>Understand your money. Learn investing. Build your future.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # 7 Feature Cards in Responsive 3-Column Grid
    row1_c1, row1_c2, row1_c3 = st.columns(3)
    
    with row1_c1:
        st.markdown("""
        <div class='dashboard-card'>
            <div>
                <div class='dashboard-card-title'>💰 Expense Tracker</div>
                <div class='dashboard-card-desc'>Track monthly spending, categorize transactions, view charts & get automatic insights.</div>
            </div>
            <div class='dashboard-card-action'>Explore →</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Open Expense Tracker", key="nav_exp", use_container_width=True):
            st.session_state.current_page = "Expense Tracker"
            st.rerun()

    with row1_c2:
        st.markdown("""
        <div class='dashboard-card'>
            <div>
                <div class='dashboard-card-title'>📚 Learn Investing</div>
                <div class='dashboard-card-desc'>Master 8 essential chapters on stocks, SIPs, mutual funds & compounding with quizzes.</div>
            </div>
            <div class='dashboard-card-action'>Explore →</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Start Learning", key="nav_learn", use_container_width=True):
            st.session_state.current_page = "Learn Investing"
            st.rerun()

    with row1_c3:
        st.markdown("""
        <div class='dashboard-card'>
            <div>
                <div class='dashboard-card-title'>📈 Market Overview</div>
                <div class='dashboard-card-desc'>Explore recent Indian market developments, index trends & economic news simply explained.</div>
            </div>
            <div class='dashboard-card-action'>Explore →</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("View Market Overview", key="nav_mkt", use_container_width=True):
            st.session_state.current_page = "Market Overview"
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)
    row2_c1, row2_c2, row2_c3 = st.columns(3)

    with row2_c1:
        st.markdown("""
        <div class='dashboard-card'>
            <div>
                <div class='dashboard-card-title'>🧪 Investment Simulator</div>
                <div class='dashboard-card-desc'>Test a virtual ₹10,000 portfolio across Bull, Bear & Volatile market scenarios safely.</div>
            </div>
            <div class='dashboard-card-action'>Explore →</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Launch Simulator", key="nav_sim", use_container_width=True):
            st.session_state.current_page = "Investment Simulator"
            st.rerun()

    with row2_c2:
        st.markdown("""
        <div class='dashboard-card'>
            <div>
                <div class='dashboard-card-title'>⚠️ Beginner Mistakes</div>
                <div class='dashboard-card-desc'>Avoid 7 dangerous financial traps like social media hype, panic selling & zero diversification.</div>
            </div>
            <div class='dashboard-card-action'>Explore →</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Explore Mistakes", key="nav_mistakes", use_container_width=True):
            st.session_state.current_page = "Beginner Mistakes"
            st.rerun()

    with row2_c3:
        st.markdown("""
        <div class='dashboard-card'>
            <div>
                <div class='dashboard-card-title'>🎯 Financial Goals</div>
                <div class='dashboard-card-desc'>Set targets for emergency funds or investment goals and calculate monthly required savings.</div>
            </div>
            <div class='dashboard-card-action'>Explore →</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Track Financial Goals", key="nav_goals", use_container_width=True):
            st.session_state.current_page = "Financial Goals"
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)
    row3_c1, row3_c2 = st.columns([2, 1])
    with row3_c1:
        st.markdown("""
        <div class='dashboard-card' style='border-color: #FF7A00;'>
            <div>
                <div class='dashboard-card-title'>🤖 AI Financial Coach (Gemini 2.5 Flash)</div>
                <div class='dashboard-card-desc'>Ask any question about finance concepts, stock terms, or your personal spending patterns!</div>
            </div>
            <div class='dashboard-card-action' style='background:#FF7A00; color:#FFFFFF;'>Chat Now →</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Chat with AI Coach", key="nav_ai", use_container_width=True):
            st.session_state.current_page = "AI Financial Coach"
            st.rerun()

# ----------------------------------------------------
# FEATURE 1: EXPENSE TRACKER
# ----------------------------------------------------
def render_expense_tracker():
    render_back_to_dashboard()
    st.markdown("<h1 style='color:#FFFFFF;'>💰 Personal Expense Tracker</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color:#A1A1AA;'>Manage your daily expenses, track category breakdowns, and receive automated financial insights.</p>", unsafe_allow_html=True)
    
    user_id = st.session_state.user["email"]
    
    # Form to add expense
    with st.expander("➕ Add New Expense", expanded=False):
        with st.form("add_expense_form", clear_on_submit=True):
            col_t, col_a, col_c, col_d = st.columns([3, 2, 2, 2])
            with col_t:
                title = st.text_input("Title / Description", placeholder="e.g. Groceries")
            with col_a:
                amount = st.number_input("Amount (₹)", min_value=1.0, value=500.0, step=50.0)
            with col_c:
                category = st.selectbox("Category", ["Food", "Transport", "Education", "Shopping", "Bills", "Entertainment", "Other"])
            with col_d:
                exp_date = st.date_input("Date", value=date.today())
            notes = st.text_input("Notes (Optional)", placeholder="e.g. Bought at supermarket")
            
            if st.form_submit_button("Save Expense"):
                if title.strip():
                    db.add_expense(user_id, title.strip(), amount, category, str(exp_date), notes.strip())
                    st.success("Expense added successfully!")
                    st.rerun()
                else:
                    st.warning("Please enter a title for the expense.")

    df_expenses = db.get_expenses(user_id)
    
    if df_expenses.empty:
        st.info("No expenses recorded yet. Add your first expense above!")
        return

    # Metrics Summary
    total_spending = df_expenses['amount'].sum()
    
    # Current month calculation
    current_month_str = datetime.now().strftime("%Y-%m")
    df_expenses['month'] = pd.to_datetime(df_expenses['date']).dt.strftime("%Y-%m")
    monthly_spending = df_expenses[df_expenses['month'] == current_month_str]['amount'].sum()
    
    top_cat = df_expenses.groupby('category')['amount'].sum().idxmax()
    top_cat_amount = df_expenses.groupby('category')['amount'].sum().max()
    
    m1, m2, m3 = st.columns(3)
    with m1:
        st.markdown(f"""
        <div class='metric-box'>
            <div class='metric-label'>Total Spending recorded</div>
            <div class='metric-value' style='color: #FF7A00;'>₹{total_spending:,.2f}</div>
        </div>
        """, unsafe_allow_html=True)
    with m2:
        st.markdown(f"""
        <div class='metric-box'>
            <div class='metric-label'>This Month's Spending</div>
            <div class='metric-value' style='color: #FF7A00;'>₹{monthly_spending:,.2f}</div>
        </div>
        """, unsafe_allow_html=True)
    with m3:
        st.markdown(f"""
        <div class='metric-box'>
            <div class='metric-label'>Highest Category</div>
            <div class='metric-value' style='color: #FF7A00;'>{top_cat} (₹{top_cat_amount:,.0f})</div>
        </div>
        """, unsafe_allow_html=True)

    # Automated Insights Box
    st.markdown(f"""
    <div class='finly-insight'>
        💡 <b>Automated Spending Insight</b>:<br>
        • <b>{top_cat}</b> is your highest spending category, representing {top_cat_amount/total_spending*100:.1f}% of all expenses.<br>
        • You have logged <b>{len(df_expenses)} total transactions</b> with an average expense of ₹{df_expenses['amount'].mean():,.2f}.
    </div>
    """, unsafe_allow_html=True)

    # Plotly Charts (Orange palette matching Image 1)
    c_chart1, c_chart2 = st.columns(2)
    orange_palette = ["#FF7A00", "#FF8A00", "#FF9800", "#FFB74D", "#FFE0B2", "#FFAB40", "#E65100"]
    
    with c_chart1:
        cat_df = df_expenses.groupby('category')['amount'].sum().reset_index()
        fig_pie = px.pie(
            cat_df, values='amount', names='category', hole=0.4,
            title="Spending Distribution by Category",
            color_discrete_sequence=orange_palette
        )
        fig_pie.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#FFFFFF'),
            legend=dict(font=dict(color='#FFFFFF'))
        )
        st.plotly_chart(fig_pie, use_container_width=True)
        
    with c_chart2:
        df_expenses_sorted = df_expenses.sort_values('date')
        fig_bar = px.bar(
            df_expenses_sorted, x='date', y='amount', color='category',
            title="Expenses Timeline",
            color_discrete_sequence=orange_palette
        )
        fig_bar.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#FFFFFF'),
            xaxis=dict(gridcolor='#1F222C'),
            yaxis=dict(gridcolor='#1F222C', title="Amount (₹)")
        )
        st.plotly_chart(fig_bar, use_container_width=True)

    # Transactions List & Edit/Delete
    st.markdown("<h3 style='color:#FFFFFF;'>📋 Recent Transactions</h3>", unsafe_allow_html=True)
    
    for idx, row in df_expenses.iterrows():
        with st.container():
            col_info, col_act = st.columns([5, 1])
            with col_info:
                st.markdown(f"""
                <div style='background: #111318; padding: 12px 18px; border-radius: 10px; border: 1px solid #1F222C; margin-bottom: 8px;'>
                    <span style='color:#FF7A00; font-weight:600;'>[{row['category']}]</span> <b style='color:#FFFFFF;'>{row['title']}</b> — 
                    <span style='color:#FFFFFF; font-weight:700;'>₹{row['amount']:,.2f}</span> 
                    <span style='color:#A1A1AA; font-size:0.85rem;'>({row['date']})</span>
                    {f"<br><small style='color:#A1A1AA;'>Note: {row['notes']}</small>" if row['notes'] else ""}
                </div>
                """, unsafe_allow_html=True)
            with col_act:
                if st.button("Delete", key=f"del_{row['id']}"):
                    db.delete_expense(row['id'])
                    st.success("Deleted")
                    st.rerun()

# ----------------------------------------------------
# FEATURE 2: LEARN INVESTING
# ----------------------------------------------------
def render_learn_investing():
    render_back_to_dashboard()
    st.markdown("<h1 style='color:#FFFFFF;'>📚 Learn Investing (8 Chapters)</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color:#A1A1AA;'>Master key stock market principles and test your knowledge with interactive quizzes.</p>", unsafe_allow_html=True)
    
    chapter_titles = [f"{c['id']}. {c['title'].split('. ')[1]}" for c in ld.CHAPTERS]
    selected_ch_title = st.selectbox("Select Chapter to Study:", chapter_titles)
    
    ch_id = int(selected_ch_title.split(".")[0])
    chapter = next(c for c in ld.CHAPTERS if c["id"] == ch_id)
    
    st.markdown("<div class='finly-card'>", unsafe_allow_html=True)
    st.markdown(f"<h2 style='color:#FF7A00;'>{chapter['title']}</h2>", unsafe_allow_html=True)
    st.markdown(f"<div style='color:#FFFFFF;'>{chapter['explanation']}</div>", unsafe_allow_html=True)
    
    st.markdown("<h4 style='color:#FF7A00; margin-top:20px;'>💡 Real-Life Example</h4>", unsafe_allow_html=True)
    st.info(chapter['example'])
    
    st.markdown("<h4 style='color:#FF7A00; margin-top:20px;'>📌 Key Takeaways</h4>", unsafe_allow_html=True)
    for takeaway in chapter['takeaways']:
        st.markdown(f"<p style='color:#FFFFFF;'>• {takeaway}</p>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
    
    # 2 Quizzes per chapter
    st.markdown("<h3 style='color:#FFFFFF;'>✍️ Test Your Knowledge (2 Questions)</h3>", unsafe_allow_html=True)
    
    for q_idx, quiz in enumerate(chapter['quizzes']):
        q_key = f"quiz_{ch_id}_{q_idx}"
        st.markdown(f"""
        <div class='quiz-card'>
            <span class='quiz-badge'>Question {q_idx + 1} of 2</span>
            <h4 style='color:#FFFFFF; margin-bottom:12px;'>{quiz['question']}</h4>
        </div>
        """, unsafe_allow_html=True)
        
        user_choice = st.radio(
            "Choose your answer:",
            quiz['options'],
            key=f"radio_{q_key}"
        )
        
        if st.button(f"Submit Answer Q{q_idx+1}", key=f"btn_{q_key}"):
            selected_idx = quiz['options'].index(user_choice)
            if selected_idx == quiz['correct_index']:
                st.success(f"🎉 Correct! {quiz['explanation']}")
            else:
                correct_opt = quiz['options'][quiz['correct_index']]
                st.error(f"❌ Incorrect. The correct answer is: **{correct_opt}**\n\nExplanation: {quiz['explanation']}")

# ----------------------------------------------------
# FEATURE 3: MARKET OVERVIEW
# ----------------------------------------------------
def render_market_overview():
    render_back_to_dashboard()
    st.markdown("<h1 style='color:#FFFFFF;'>📈 Indian Market Overview</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color:#A1A1AA;'>Stay informed with recent benchmark updates and financial news in plain language.</p>", unsafe_allow_html=True)
    
    st.markdown(md.MARKET_DISCLAIMER)
    st.markdown("<br>", unsafe_allow_html=True)
    
    for item in md.MARKET_UPDATES:
        st.markdown(f"""
        <div class='finly-card'>
            <div style='display:flex; justify-between; align-items:center;'>
                <span style='color:#FF7A00; font-weight:600; font-size:0.85rem;'>📅 Date: {item['date']}</span>
                <span style='color:#A1A1AA; font-size:0.8rem; background:#111318; border:1px solid #1F222C; padding:2px 8px; border-radius:6px;'>Source: {item['source']}</span>
            </div>
            <h3 style='color:#FFFFFF; margin: 10px 0;'>{item['title']}</h3>
            <p style='color:#A1A1AA;'>{item['summary']}</p>
            <div class='finly-insight' style='margin-top:10px;'>
                <b>Impact on Beginners:</b> {item['impact']}
            </div>
        </div>
        """, unsafe_allow_html=True)

# ----------------------------------------------------
# FEATURE 4: INVESTMENT SIMULATOR
# ----------------------------------------------------
def render_simulator():
    render_back_to_dashboard()
    st.markdown("<h1 style='color:#FFFFFF;'>🧪 Investment Simulator (Virtual ₹10,000)</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color:#A1A1AA;'>Experiment with asset allocation and observe outcomes under different market conditions with zero risk.</p>", unsafe_allow_html=True)
    
    st.warning("ℹ️ Virtual Simulation Only: No real money involved, no brokerage integration.")
    
    col_alloc, col_scen = st.columns([1, 1])
    
    with col_alloc:
        st.markdown("<div class='finly-card'>", unsafe_allow_html=True)
        st.markdown("<h3 style='color:#FFFFFF;'>1. Set Asset Allocation (%)</h3>", unsafe_allow_html=True)
        p_stocks = st.slider("Individual Stocks (%)", 0, 100, 40)
        p_mf = st.slider("Mutual Funds (%)", 0, 100, 30)
        p_gold = st.slider("Gold (%)", 0, 100, 20)
        p_cash = st.slider("Cash (%)", 0, 100, 10)
        
        total_p = p_stocks + p_mf + p_gold + p_cash
        
        if total_p != 100:
            st.error(f"⚠️ Total allocation must sum to 100%. Currently: **{total_p}%**")
        else:
            st.success("✅ Total Allocation = 100% (₹10,000 Total)")
        st.markdown("</div>", unsafe_allow_html=True)
        
    with col_scen:
        st.markdown("<div class='finly-card'>", unsafe_allow_html=True)
        st.markdown("<h3 style='color:#FFFFFF;'>2. Choose Market Scenario</h3>", unsafe_allow_html=True)
        scenario_choice = st.selectbox("Select Scenario", list(sim.SCENARIOS.keys()))
        info = sim.SCENARIOS[scenario_choice]
        st.info(f"**Scenario Context:** {info['description']}")
        
        run_sim = st.button("Run Simulation 🚀", disabled=(total_p != 100), use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    if run_sim and total_p == 100:
        allocations = {
            "Stocks": p_stocks,
            "Mutual Funds": p_mf,
            "Gold": p_gold,
            "Cash": p_cash
        }
        res = sim.calculate_simulation(allocations, scenario_choice)
        
        st.markdown("<br><h2 style='text-align:center; color:#FFFFFF;'>📊 Simulation Results</h2>", unsafe_allow_html=True)
        
        res_m1, res_m2, res_m3 = st.columns(3)
        with res_m1:
            st.markdown(f"""
            <div class='metric-box'>
                <div class='metric-label'>Starting Capital</div>
                <div class='metric-value'>₹{res['initial_capital']:,.0f}</div>
            </div>
            """, unsafe_allow_html=True)
        with res_m2:
            st.markdown(f"""
            <div class='metric-box'>
                <div class='metric-label'>Simulated Final Value</div>
                <div class='metric-value' style='color:#FF7A00;'>₹{res['total_final']:,.2f}</div>
            </div>
            """, unsafe_allow_html=True)
        with res_m3:
            color_val = "#FF7A00" if res['net_pl'] >= 0 else "#EF4444"
            st.markdown(f"""
            <div class='metric-box'>
                <div class='metric-label'>Net Profit / Loss</div>
                <div class='metric-value' style='color: {color_val};'>
                    {'+' if res['net_pl']>=0 else ''}₹{res['net_pl']:,.2f} ({res['net_pl_pct']:.1f}%)
                </div>
            </div>
            """, unsafe_allow_html=True)
            
        fig_sim = sim.create_simulation_chart(res)
        st.plotly_chart(fig_sim, use_container_width=True)
        
        st.markdown(f"""
        <div class='finly-insight'>
            💡 <b>What Happened in this Scenario?</b><br>
            {res['scenario_info']['explanation']}
        </div>
        """, unsafe_allow_html=True)

# ----------------------------------------------------
# FEATURE 5: BEGINNER MISTAKES
# ----------------------------------------------------
def render_beginner_mistakes():
    render_back_to_dashboard()
    st.markdown("<h1 style='color:#FFFFFF;'>⚠️ 7 Common Beginner Financial Mistakes</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color:#A1A1AA;'>Learn from the most frequent traps rookie investors fall into and protect your capital.</p>", unsafe_allow_html=True)
    
    for item in ld.BEGINNER_MISTAKES:
        st.markdown(f"""
        <div class='finly-card'>
            <div style='font-size: 1.5rem; margin-bottom: 5px;'>{item['icon']} <span style='color:#FFFFFF; font-weight:700;'>{item['title']}</span></div>
            <p style='color:#FF7A00; font-weight:500;'>{item['summary']}</p>
            <p style='color:#A1A1AA;'>{item['explanation']}</p>
            <div class='finly-warning'>
                <b>Real-World Trap:</b> {item['example']}
            </div>
            <div style='color:#FF7A00; font-weight:600; margin-top:10px;'>
                ✅ Key Lesson: {item['lesson']}
            </div>
        </div>
        """, unsafe_allow_html=True)

# ----------------------------------------------------
# FEATURE 6: FINANCIAL GOALS
# ----------------------------------------------------
def render_financial_goals():
    render_back_to_dashboard()
    st.markdown("<h1 style='color:#FFFFFF;'>🎯 Financial Goals Tracker</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color:#A1A1AA;'>Set financial targets, track saving progress, and calculate your required monthly savings.</p>", unsafe_allow_html=True)
    
    user_id = st.session_state.user["email"]
    
    with st.expander("➕ Add New Financial Goal", expanded=False):
        with st.form("add_goal_form", clear_on_submit=True):
            cg1, cg2 = st.columns(2)
            with cg1:
                g_name = st.text_input("Goal Name", placeholder="e.g. Emergency Fund")
                g_target = st.number_input("Target Amount (₹)", min_value=1000.0, value=50000.0, step=5000.0)
            with cg2:
                g_saved = st.number_input("Current Savings (₹)", min_value=0.0, value=10000.0, step=1000.0)
                g_date = st.date_input("Target Date", value=date(2026, 12, 31))
                
            if st.form_submit_button("Save Goal"):
                if g_name.strip():
                    db.add_goal(user_id, g_name.strip(), g_target, g_saved, str(g_date))
                    st.success("Financial Goal added!")
                    st.rerun()

    df_goals = db.get_goals(user_id)
    
    if df_goals.empty:
        st.info("No financial goals set yet. Click above to add your first goal!")
        return

    for idx, row in df_goals.iterrows():
        pct = min(100.0, (row['current_savings'] / row['target_amount']) * 100.0)
        rem = max(0.0, row['target_amount'] - row['current_savings'])
        
        # Calculate months remaining
        target_d = datetime.strptime(row['target_date'], "%Y-%m-%d").date()
        today_d = date.today()
        months_left = max(1, (target_d.year - today_d.year) * 12 + (target_d.month - today_d.month))
        req_monthly = rem / months_left if rem > 0 else 0.0
        
        st.markdown("<div class='finly-card'>", unsafe_allow_html=True)
        g_c1, g_c2 = st.columns([4, 1])
        with g_c1:
            st.markdown(f"""
            <h3 style='color:#FFFFFF; margin-bottom: 4px;'>🎯 {row['goal_name']}</h3>
            <p style='color:#A1A1AA; font-size:0.9rem;'>Target Date: {row['target_date']} ({months_left} months remaining)</p>
            """, unsafe_allow_html=True)
        with g_c2:
            if st.button("Delete Goal", key=f"del_g_{row['id']}"):
                db.delete_goal(row['id'])
                st.rerun()
                
        st.progress(int(pct))
        
        stat1, stat2, stat3 = st.columns(3)
        with stat1:
            st.markdown(f"<span style='color:#A1A1AA;'>Saved:</span> <b style='color:#FFFFFF;'>₹{row['current_savings']:,.0f}</b> / ₹{row['target_amount']:,.0f}", unsafe_allow_html=True)
        with stat2:
            st.markdown(f"<span style='color:#A1A1AA;'>Progress:</span> <b style='color:#FF7A00;'>{pct:.1f}%</b>", unsafe_allow_html=True)
        with stat3:
            st.markdown(f"<span style='color:#A1A1AA;'>Est. Monthly Saving:</span> <b style='color:#FF7A00;'>₹{req_monthly:,.0f}/mo</b>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

# ----------------------------------------------------
# FEATURE 7: AI FINANCIAL COACH
# ----------------------------------------------------
def render_ai_coach():
    render_back_to_dashboard()
    st.markdown("<h1 style='color:#FFFFFF;'>🤖 Finly AI Financial Coach</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color:#A1A1AA;'>Powered by Google Gemini 2.5 Flash with fallback logic. Ask financial literacy questions!</p>", unsafe_allow_html=True)
    
    # Context helper button prompts
    st.markdown("<h4 style='color:#FFFFFF;'>Quick Prompts:</h4>", unsafe_allow_html=True)
    prompt_cols = st.columns(4)
    p_selected = None
    with prompt_cols[0]:
        if st.button("💡 What is Nifty 50?", key="pr1"):
            p_selected = "What is a Nifty 50 index fund and why is it good for beginners?"
    with prompt_cols[1]:
        if st.button("🛡️ Emergency Fund?", key="pr2"):
            p_selected = "How much money should I keep in an emergency fund?"
    with prompt_cols[2]:
        if st.button("📊 Explain 50/30/20 Rule", key="pr3"):
            p_selected = "Can you explain the 50/30/20 budgeting rule simple language?"
    with prompt_cols[3]:
        if st.button("📈 SIP vs Lump Sum", key="pr4"):
            p_selected = "What is the difference between SIP and Lump Sum investing?"

    # Render Chat History
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # User Input
    user_input = st.chat_input("Ask your financial question here...")
    
    if p_selected:
        user_input = p_selected

    if user_input:
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)
            
        with st.chat_message("assistant"):
            with st.spinner("Finly Coach is thinking..."):
                response_text = coach.ask_ai_coach(user_input)
                st.markdown(response_text)
                st.session_state.chat_history.append({"role": "assistant", "content": response_text})

# ----------------------------------------------------
# SECONDARY SIDEBAR
# ----------------------------------------------------
def render_sidebar():
    with st.sidebar:
        st.markdown("""
        <div style='text-align: left; padding: 10px 0;'>
            <h2 style='font-size: 1.8rem; margin:0; color:#FFFFFF;'>⚡ <span style='color: #FF7A00;'>Finly</span></h2>
            <p style='font-size: 0.8rem; color: #A1A1AA;'>Your money, your future</p>
        </div>
        <hr style='border-color: #1F222C; margin: 10px 0;'>
        """, unsafe_allow_html=True)
        
        # Profile Section
        st.markdown("<h3 style='color:#FFFFFF;'>👤 User Profile</h3>", unsafe_allow_html=True)
        st.markdown(f"**Name:** {st.session_state.user['name']}")
        st.markdown(f"**Email:** `{st.session_state.user['email']}`")
        
        st.markdown("<hr style='border-color: #1F222C; margin: 15px 0;'>", unsafe_allow_html=True)
        
        # Current Page Indicator
        st.markdown(f"📍 **Active Page:** `{st.session_state.current_page}`")
        if st.session_state.current_page != "Dashboard":
            if st.button("🏠 Go to Dashboard", key="sidebar_dash_btn"):
                st.session_state.current_page = "Dashboard"
                st.rerun()

        st.markdown("<hr style='border-color: #1F222C; margin: 15px 0;'>", unsafe_allow_html=True)

        # Settings Expander
        with st.expander("⚙️ Settings"):
            st.selectbox("Currency Display", ["INR (₹)", "USD ($)"])
            st.selectbox("Theme Mode", ["Black & Orange (Default)", "Dark Charcoal"])
            if st.button("Reset Seed Data", key="btn_reset_db"):
                db.init_db()
                st.success("Database re-initialized")

        # About Expander
        with st.expander("ℹ️ About Finly"):
            st.markdown("""
            **Finly Hackathon MVP v1.0**
            • Simple, reliable personal finance platform
            • Streamlit + SQLite + Plotly
            • Google Gemini 2.5 Flash Coach
            """)

        st.markdown("<br><br>", unsafe_allow_html=True)
        if st.button("🚪 Logout", key="btn_logout", use_container_width=True):
            st.session_state.authenticated = False
            st.session_state.current_page = "Dashboard"
            st.rerun()

# ----------------------------------------------------
# MAIN APP ROUTER
# ----------------------------------------------------
def main():
    if not st.session_state.authenticated:
        render_auth_page()
    else:
        render_sidebar()
        
        page = st.session_state.current_page
        if page == "Dashboard":
            render_dashboard()
        elif page == "Expense Tracker":
            render_expense_tracker()
        elif page == "Learn Investing":
            render_learn_investing()
        elif page == "Market Overview":
            render_market_overview()
        elif page == "Investment Simulator":
            render_simulator()
        elif page == "Beginner Mistakes":
            render_beginner_mistakes()
        elif page == "Financial Goals":
            render_financial_goals()
        elif page == "AI Financial Coach":
            render_ai_coach()

if __name__ == "__main__":
    main()
