import pandas as pd

class SpendingAnalyzerAgent:
    def __init__(self, transactions_df):
        self.df = transactions_df

    def analyze(self):
        """
        Analyzes spending patterns.
        """
        # Group by category
        category_spending = self.df.groupby('category')['amount'].sum().to_dict()
        
        # Daily spending
        daily_spending = self.df.groupby(self.df['date'].dt.date)['amount'].sum()
        
        # Monthly spending
        monthly_spending = self.df.groupby(self.df['date'].dt.to_period('M'))['amount'].sum()
        
        # Top categories
        top_categories = self.df.groupby('category')['amount'].sum().sort_values(ascending=False).head(5).to_dict()
        
        return {
            "total_spent": self.df['amount'].sum(),
            "category_breakdown": category_spending,
            "average_daily_spending": daily_spending.mean(),
            "monthly_spending": {str(k): v for k, v in monthly_spending.items()},
            "top_categories": top_categories
        }
