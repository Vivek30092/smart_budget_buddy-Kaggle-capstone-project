import streamlit as st
import pandas as pd
import plotly.express as px
import sys
import os
import json

# Add the project root directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from smart_budget_buddy.agents.budget_planner import BudgetPlannerAgent
from smart_budget_buddy.agents.spending_analyzer import SpendingAnalyzerAgent
from smart_budget_buddy.agents.forecasting_agent import ForecastingAgent
from smart_budget_buddy.agents.alerts_agent import AlertsAgent
from smart_budget_buddy.agents.financial_chat import FinancialLiteracyChatBot
from smart_budget_buddy.utils.memory_store import MemoryStore

# Initialize Memory
memory = MemoryStore()

# Page Config
st.set_page_config(page_title="Smart Budget Buddy", page_icon="🎓", layout="wide")

# Title and Header
st.title("🎓 Smart Budget Buddy")
st.markdown("### Your AI-Powered Financial Assistant")

# Sidebar for User Input
st.sidebar.header("📝 Your Financial Profile")

# Manual Input Form
with st.sidebar.form("profile_form"):
    st.markdown("### Income & Fixed Expenses")
    # Load existing profile if available
    existing_profile = memory.get_profile()
    
    monthly_income = st.number_input("Monthly Income ($)", min_value=0.0, value=existing_profile.get('monthly_income', 1000.0), step=50.0)
    financial_aid = st.number_input("Financial Aid ($)", min_value=0.0, value=existing_profile.get('financial_aid', 0.0), step=50.0)
    
    st.markdown("### Fixed Costs (Monthly)")
    housing = st.number_input("Housing/Rent ($)", min_value=0.0, value=existing_profile.get('housing', 400.0), step=50.0)
    tuition = st.number_input("Tuition (Monthly Avg) ($)", min_value=0.0, value=existing_profile.get('tuition', 200.0), step=50.0)
    transportation = st.number_input("Transportation ($)", min_value=0.0, value=existing_profile.get('transportation', 50.0), step=10.0)
    
    submit_button = st.form_submit_button("Generate Budget")

# Construct Profile Dictionary from Inputs
profile = {
    'monthly_income': monthly_income,
    'financial_aid': financial_aid,
    'housing': housing,
    'tuition': tuition,
    'transportation': transportation,
    # Variable categories set to 0 to trigger standard allocation logic in BudgetPlanner
    'food': 0, 'books_supplies': 0, 'entertainment': 0, 
    'personal_care': 0, 'technology': 0, 'health_wellness': 0, 'miscellaneous': 0
}

if submit_button:
    memory.update_profile(profile)
    st.sidebar.success("Profile Updated!")

# --- Main Content ---

# 1. Budget Planner Agent
st.header("1. 📝 Monthly Budget Plan")

if submit_button or profile:
    planner = BudgetPlannerAgent(profile)
    budget = planner.generate_budget()
    
    # Save budget to memory
    memory.save_budget_plan(budget)
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Monthly Income", f"${budget['total_income']:.2f}")
    col2.metric("Fixed Costs", f"${sum(budget['fixed_costs'].values()):.2f}")
    col3.metric("Disposable Income", f"${budget['disposable_income']:.2f}", delta_color="normal")
    
    with st.expander("View Budget Recommendations", expanded=True):
        for rec in budget['recommendations']:
            st.write(f"- {rec}")
            
    st.subheader("Recommended Category Limits")
    limits_df = pd.DataFrame(list(budget['category_limits'].items()), columns=['Category', 'Recommended Limit ($)'])
    st.dataframe(limits_df, use_container_width=True)

    # 2. Transaction Analysis (Requires File Upload)
    st.markdown("---")
    st.header("2. 📊 Transaction Analysis")
    st.info("Upload your bank statement or transaction history (CSV) to analyze spending and get alerts.")
    
    uploaded_file = st.file_uploader("Upload CSV (Columns: date, category, amount)", type=["csv"])
    
    if uploaded_file is not None:
        try:
            # Load and preprocess uploaded file
            transactions = pd.read_csv(uploaded_file)
            # Basic cleaning to match expected format
            transactions.columns = [c.strip().lower().replace(" ", "_") for c in transactions.columns]
            if 'date' in transactions.columns:
                transactions['date'] = pd.to_datetime(transactions['date'])
            
            # Run Agents
            analyzer = SpendingAnalyzerAgent(transactions)
            analysis = analyzer.analyze()
            
            st.subheader("Spending Overview")
            st.metric("Total Spent (Period)", f"${analysis['total_spent']:.2f}")
            
            # Charts
            tab1, tab2 = st.tabs(["Category Breakdown", "Daily Spending Trend"])
            
            with tab1:
                cat_df = pd.DataFrame(list(analysis['category_breakdown'].items()), columns=['Category', 'Amount'])
                fig_pie = px.pie(cat_df, values='Amount', names='Category', title="Spending by Category")
                st.plotly_chart(fig_pie, use_container_width=True)
                
            with tab2:
                if 'date' in transactions.columns:
                    daily_series = transactions.groupby(transactions['date'].dt.date)['amount'].sum()
                    daily_df = daily_series.reset_index()
                    daily_df.columns = ['Date', 'Amount']
                    fig_line = px.line(daily_df, x='Date', y='Amount', title="Daily Spending Trend")
                    st.plotly_chart(fig_line, use_container_width=True)
                else:
                    st.warning("No 'date' column found for trend analysis.")

            # 3. Alerts Agent
            st.header("3. 🚨 Risk Alerts")
            alerts_agent = AlertsAgent(budget, analysis)
            alerts_result = alerts_agent.check_alerts()
            
            if alerts_result['alerts']:
                for alert in alerts_result['alerts']:
                    st.error(alert)
            else:
                st.success("No overspending risks detected based on your budget!")

            # 4. Forecasting Agent
            st.header("4. 🔮 Future Forecast")
            if 'date' in transactions.columns:
                forecaster = ForecastingAgent(transactions)
                forecast = forecaster.predict_next_month()
                
                col_f1, col_f2 = st.columns(2)
                col_f1.metric("Predicted Next Month Spending", f"${forecast['predicted_spending']:.2f}")
                col_f2.metric("Trend", forecast['trend'].title(), delta=forecast['trend'], delta_color="off")
            else:
                st.warning("Forecasting requires a 'date' column.")
                
        except Exception as e:
            st.error(f"Error processing file: {e}")
    else:
        st.markdown("👋 *Don't have a file? The Budget Planner above still works! Upload a CSV to unlock Analysis, Alerts, and Forecasting.*")

# 5. Financial Literacy Chat
st.markdown("---")
st.header("5. 💡 Financial Literacy Chat")
st.markdown("Ask me about **budgeting, saving, or expense tracking**! (I cannot answer about stocks or loans)")

# Initialize Agent in Session State if not present
if 'literacy_agent' not in st.session_state:
    st.session_state.literacy_agent = FinancialLiteracyChatBot()

# API Key Input (Optional)
api_key = st.sidebar.text_input("🔑 Google Gemini API Key (Optional)", type="password", help="Enter your API key for smarter AI responses.")

# Re-initialize agent if API key is provided and not yet set
if api_key and (st.session_state.literacy_agent.api_key != api_key):
    st.session_state.literacy_agent = FinancialLiteracyChatBot(api_key=api_key)
    st.sidebar.success("API Key set! AI mode enabled.")

# Chat Interface
# Display chat history
history = st.session_state.literacy_agent.get_history()
for chat in history:
    with st.chat_message(chat['role']):
        st.write(chat['content'])

# User Input
if prompt := st.chat_input("Ask a question..."):
    # Display user message
    with st.chat_message("user"):
        st.write(prompt)
    
    # Get response
    response = st.session_state.literacy_agent.ask(prompt)
    
    # Display assistant response
    with st.chat_message("assistant"):
        st.write(response)

# Clear History Button
if st.button("Clear Chat History"):
    st.session_state.literacy_agent.clear_history()
    st.rerun()
