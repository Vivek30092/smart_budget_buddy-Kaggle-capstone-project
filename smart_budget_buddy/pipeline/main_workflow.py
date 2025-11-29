# from smart_budget_buddy.utils.data_loader import load_profiles, load_transactions, get_student_profile
from smart_budget_buddy.agents.budget_planner import BudgetPlannerAgent
from smart_budget_buddy.agents.spending_analyzer import SpendingAnalyzerAgent
from smart_budget_buddy.agents.forecasting_agent import ForecastingAgent
from smart_budget_buddy.agents.alerts_agent import AlertsAgent
from smart_budget_buddy.agents.financial_literacy import FinancialLiteracyAgent
import json

def run_pipeline(student_id=0):
    print(f"--- Running Smart Budget Buddy (Manual Mode) ---")
    
    # 1. Define Manual Profile (Mock Data for CLI)
    profile = {
        'monthly_income': 1000,
        'financial_aid': 0,
        'housing': 400,
        'tuition': 200,
        'transportation': 50,
        'food': 0, 'books_supplies': 0, 'entertainment': 0, 
        'personal_care': 0, 'technology': 0, 'health_wellness': 0, 'miscellaneous': 0
    }
    
    # 2. Budget Planner
    planner = BudgetPlannerAgent(profile)
    budget = planner.generate_budget()
    print("\n--- Budget Plan ---")
    print(json.dumps(budget, indent=2, default=str))

    # 3. Spending Analyzer (Skipped in CLI Manual Mode or Mocked)
    print("\n--- Spending Analysis ---")
    print("(Transaction analysis requires CSV upload in Streamlit app)")
    analysis = {
        "total_spent": 0,
        "category_breakdown": {},
        "average_daily_spending": 0,
        "monthly_spending": {},
        "top_categories": {}
    }

    # 4. Alerts
    alerts_agent = AlertsAgent(budget, analysis)
    alerts = alerts_agent.check_alerts()
    print("\n--- Alerts ---")
    print(json.dumps(alerts, indent=2))

    # 5. Forecasting
    print("\n--- Forecast ---")
    print("(Forecasting requires transaction history)")
    forecast = {}

    # 6. Financial Literacy
    literacy = FinancialLiteracyAgent()
    tip = literacy.ask("How do I start saving?")
    print("\n--- Financial Tip ---")
    print(tip)
    
    return {
        "budget": budget,
        "analysis": analysis,
        "alerts": alerts,
        "forecast": forecast,
        "tip": tip
    }


if __name__ == "__main__":
    run_pipeline()
