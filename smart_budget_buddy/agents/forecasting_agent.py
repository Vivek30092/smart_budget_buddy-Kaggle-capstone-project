import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

class ForecastingAgent:
    def __init__(self, transactions_df):
        self.df = transactions_df

    def predict_next_month(self):
        """
        Predicts next month's spending using Linear Regression on monthly totals.
        """
        monthly_spending = self.df.groupby(self.df['date'].dt.to_period('M'))['amount'].sum().reset_index()
        monthly_spending['month_num'] = np.arange(len(monthly_spending))
        
        if len(monthly_spending) < 2:
            return {"prediction": monthly_spending['amount'].iloc[0] if len(monthly_spending) > 0 else 0, "note": "Not enough data for regression"}

        X = monthly_spending[['month_num']]
        y = monthly_spending['amount']
        
        model = LinearRegression()
        model.fit(X, y)
        
        next_month_num = monthly_spending['month_num'].max() + 1
        prediction = model.predict([[next_month_num]])[0]
        
        return {
            "predicted_spending": round(prediction, 2),
            "trend": "increasing" if model.coef_[0] > 0 else "decreasing"
        }
