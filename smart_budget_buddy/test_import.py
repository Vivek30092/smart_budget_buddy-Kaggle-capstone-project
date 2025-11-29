import sys
import os

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

try:
    from smart_budget_buddy.agents.financial_literacy import FinancialLiteracyAgent
    print("Import successful!")
    agent = FinancialLiteracyAgent()
    print("Agent instantiated.")
except ImportError as e:
    print(f"ImportError: {e}")
except Exception as e:
    print(f"Error: {e}")
