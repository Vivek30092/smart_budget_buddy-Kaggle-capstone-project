import json
import pandas as pd
from .budget_planner import BudgetPlannerAgent
from .spending_analyzer import SpendingAnalyzerAgent
from ..utils.memory_store import MemoryStore
from ..utils.data_loader import DataLoader

# Initialize Memory Store
memory = MemoryStore()

def calculate_budget_tool(income, fixed_expenses, variable_expenses=None):
    """
    Calculates a budget based on income and expenses.
    Args:
        income (float): Monthly income.
        fixed_expenses (dict): Dictionary of fixed expenses (e.g., {'rent': 500}).
        variable_expenses (dict, optional): Dictionary of variable expenses.
    Returns:
        str: JSON string of the budget plan.
    """
    profile = {
        'monthly_income': income,
        'financial_aid': 0, # Simplified for tool
        'housing': fixed_expenses.get('housing', 0),
        'tuition': fixed_expenses.get('tuition', 0),
        'transportation': fixed_expenses.get('transportation', 0),
    }
    # Add other fixed expenses if any
    
    planner = BudgetPlannerAgent(profile)
    budget = planner.generate_budget()
    return json.dumps(budget, indent=2)

def expense_classifier_tool(transactions_csv_path):
    """
    Categorizes user spending and detects patterns.
    Args:
        transactions_csv_path (str): Path to the transactions CSV file.
    Returns:
        str: JSON string of the analysis.
    """
    try:
        df = pd.read_csv(transactions_csv_path)
        # Basic preprocessing
        df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]
        if 'date' in df.columns:
            df['date'] = pd.to_datetime(df['date'])
            
        analyzer = SpendingAnalyzerAgent(df)
        analysis = analyzer.analyze()
        return json.dumps(analysis, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e)})

def memory_lookup_tool(key):
    """
    Fetches stored user data.
    Args:
        key (str): The key to lookup (e.g., 'user_profile', 'budget_plans').
    Returns:
        str: JSON string of the data.
    """
    if key == 'user_profile':
        return json.dumps(memory.get_profile(), indent=2)
    elif key == 'history':
        return json.dumps(memory.get_history(), indent=2)
    elif key == 'latest_budget':
        return json.dumps(memory.get_latest_budget(), indent=2)
    else:
        return json.dumps({"error": "Key not found"})

def memory_update_tool(key, data):
    """
    Updates conversation history or user profile.
    Args:
        key (str): 'user_profile' or 'history'.
        data (dict): Data to update.
    Returns:
        str: Status message.
    """
    if key == 'user_profile':
        memory.update_profile(data)
        return "Profile updated."
    else:
        return "Update not supported for this key via tool."

def dataset_loader_tool(directory_path):
    """
    Reads files in the project folder.
    Args:
        directory_path (str): Path to the directory.
    Returns:
        str: Summary of files found.
    """
    try:
        loader = DataLoader(directory_path)
        # Assuming DataLoader has a method to list or load files. 
        # If not, we'll just list files for now as a simple implementation.
        import os
        files = os.listdir(directory_path)
        return json.dumps({"files": files}, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e)})
