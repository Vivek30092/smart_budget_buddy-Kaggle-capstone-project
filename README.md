# Smart Budget Buddy - Kaggle Capstone Project 🎓

**Smart Budget Buddy** is an AI-powered financial literacy assistant designed specifically for students. It helps users manage their budgets, analyze spending habits, and learn financial concepts while enforcing strict guardrails to ensure safe and relevant advice.

This project was developed as a Kaggle Capstone Project.

## 🚀 Features

*   **AI Financial Chatbot**: A conversational agent powered by Google Gemini (optional) to answer student finance questions.
*   **Budget Planner**: Automatically calculates a monthly budget based on income and fixed expenses using the 50/30/20 rule.
*   **Spending Analysis**: Upload your transaction history (CSV) to visualize spending breakdowns and trends.
*   **Risk Alerts**: Detects potential overspending and provides actionable warnings.
*   **Forecasting**: Predicts future spending based on historical data.
*   **Strict Guardrails**: Ensures the AI focuses solely on financial literacy and avoids restricted topics like gambling or stock trading.

## 📂 Project Structure

```
smart_budget_buddy-Kaggle-capstone-project/
├── smart_budget_buddy/     # Main application source code
│   ├── agents/             # AI Agents (Budget, Analysis, Chat, etc.)
│   ├── utils/              # Utility functions (Memory, etc.)
│   ├── pipeline/           # Pipeline for data processing
│   ├── streamlit_app.py    # Main Streamlit application
│   └── README.md           # Detailed technical documentation
└── README.md               # This file
```

## 🛠️ Quick Start

### Prerequisites

*   Python 3.8 or higher
*   [Optional] Google Gemini API Key for full AI chat capabilities.

### Installation

1.  **Clone the repository** (if you haven't already):
    ```bash
    git clone <repository-url>
    cd smart_budget_buddy-Kaggle-capstone-project
    ```

2.  **Navigate to the application directory**:
    ```bash
    cd smart_budget_buddy
    ```

3.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

### Running the Application

Run the Streamlit app from the `smart_budget_buddy` directory:

```bash
streamlit run streamlit_app.py
```

The application will launch in your default web browser at `http://localhost:8501`.

## 📖 Documentation

For more detailed information about the **Multi-Agent Architecture**, **Memory Schema**, and **Guardrails**, please refer to the [Technical README](smart_budget_buddy/README.md) located in the `smart_budget_buddy` directory.

## 📝 Usage

1.  **Profile Setup**: Enter your monthly income and fixed expenses in the sidebar to generate a budget.
2.  **Upload Data**: Upload a CSV file of your transactions to unlock analysis and forecasting features.
3.  **Chat**: Use the "Financial Literacy Chat" section to ask questions about budgeting and saving.
