# Smart Budget Buddy 🎓

Smart Budget Buddy is an AI-powered financial literacy assistant designed specifically for students. It helps users manage their budget, analyze spending habits, and learn financial concepts while enforcing strict guardrails to ensure safe and relevant advice.

## 🏗️ Multi-Agent Architecture

The system is built using a modular multi-agent architecture:

1.  **Main Conversational Agent (`FinancialLiteracyChatBot`)**:
    *   **Role**: Handles user interaction, maintains context, and enforces guardrails.
    *   **Logic**: Uses Google Gemini (if API key provided) or a fallback knowledge base.
    *   **Memory**: Persists conversation history and user profile via `MemoryStore`.
    *   **Guardrails**: Strictly declines requests related to investing, gambling, illegal activities, etc.

2.  **Budget Calculation Agent (`BudgetPlannerAgent`)**:
    *   **Role**: Calculates a monthly budget based on income and fixed expenses.
    *   **Logic**: Applies the 50/30/20 rule and custom student-specific adjustments.

3.  **Data Interpretation Agent (`SpendingAnalyzerAgent`)**:
    *   **Role**: Analyzes uploaded transaction data (CSV).
    *   **Logic**: Categorizes spending, calculates totals, and identifies trends.

4.  **Forecasting Agent (`ForecastingAgent`)**:
    *   **Role**: Predicts future spending based on historical data.

5.  **Alerts Agent (`AlertsAgent`)**:
    *   **Role**: Detects overspending risks and generates alerts.

## 🛠️ Tools & API Binding

The system defines specific tools in `agents/tools.py` that can be invoked by the agents or the system:

*   `calculate_budget_tool(income, fixed_expenses)`: Generates a budget plan JSON.
*   `expense_classifier_tool(csv_path)`: Analyzes spending patterns.
*   `memory_lookup_tool(key)`: Retrieves stored user data.
*   `memory_update_tool(key, data)`: Updates user profile or history.
*   `dataset_loader_tool(path)`: Lists available datasets.

## 🔒 Guardrails & Safety Policy

Smart Budget Buddy is strictly limited to **student financial literacy**.

**Restricted Topics (Declined Instantly):**
*   Stock market, crypto, trading, investments.
*   Loans, credit cards, debt products.
*   Gambling, betting, casinos.
*   Politics, adult content, illegal activities.
*   Medical, legal, or mental health advice.

**Response Policy:**
*   "I'm here only to help with student budgeting and financial literacy. I cannot assist with that topic."

## 💾 Memory Schema

User data is stored in `user_data.json` with the following structure:

```json
{
    "user_profile": {
        "monthly_income": 1000,
        "housing": 400,
        ...
    },
    "conversation_history": [
        {"role": "user", "content": "...", "timestamp": "..."},
        {"role": "assistant", "content": "...", "timestamp": "..."}
    ],
    "budget_plans": [...],
    "goals": []
}
```

## 🚀 Deployment Instructions

### Prerequisites
*   Python 3.8+
*   Google Gemini API Key (Optional, for AI features)

### Installation

1.  Clone the repository.
2.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

### Running the App

Run the Streamlit application:

```bash
streamlit run streamlit_app.py
```

The app will open in your browser at `http://localhost:8501`.

### Deployment Options
*   **Streamlit Cloud**: Connect your GitHub repo and deploy directly.
*   **AWS EC2/Lightsail**: Provision a server, install Python/Pip, run the app with `streamlit run`.

## 📂 Project Structure

*   `agents/`: Contains agent logic and tools.
*   `utils/`: Utility functions and memory management.
*   `pipeline/`: Workflow orchestration (if applicable).
*   `streamlit_app.py`: Main application entry point.
*   `requirements.txt`: Python dependencies.
