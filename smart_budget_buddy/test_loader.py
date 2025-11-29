from smart_budget_buddy.utils.data_loader import load_profiles, load_transactions
import pandas as pd
import traceback

with open("test_output.txt", "w") as f:
    f.write("Starting test...\n")
    try:
        print("Loading profiles...")
        profiles = load_profiles()
        f.write(f"Profiles loaded: {len(profiles)} rows\n")
        f.write(str(profiles.head()) + "\n")
    except Exception as e:
        f.write(f"Error loading profiles: {e}\n")
        f.write(traceback.format_exc() + "\n")

    try:
        print("Loading transactions...")
        transactions = load_transactions()
        f.write(f"Transactions loaded: {len(transactions)} rows\n")
        f.write(str(transactions.head()) + "\n")
    except Exception as e:
        f.write(f"Error loading transactions: {e}\n")
        f.write(traceback.format_exc() + "\n")
