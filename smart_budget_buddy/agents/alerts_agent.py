class AlertsAgent:
    def __init__(self, budget_plan, spending_analysis):
        self.budget = budget_plan
        self.spending = spending_analysis
        self.mapping = {
            'restuarant': 'food', 'coffe': 'food', 'market': 'food',
            'transport': 'transportation', 'taxi': 'transportation', 'travel': 'transportation', 'rent_car': 'transportation',
            'clothing': 'personal_care',
            'phone': 'technology',
            'learning': 'books_supplies',
            'events': 'entertainment', 'film/enjoyment': 'entertainment', 'sport': 'entertainment',
            'health': 'health_wellness',
            'communal': 'miscellaneous', 'other': 'miscellaneous', 'business_lunch': 'food', 'motel': 'miscellaneous'
        }

    def check_alerts(self):
        alerts = []
        category_spending = self.spending['category_breakdown']
        
        # Aggregate actual spending into budget categories
        aggregated_actuals = {}
        for cat, amount in category_spending.items():
            budget_cat = self.mapping.get(cat.lower(), 'miscellaneous')
            aggregated_actuals[budget_cat] = aggregated_actuals.get(budget_cat, 0) + amount
            
        # Compare
        for cat, limit in self.budget['category_limits'].items():
            actual = aggregated_actuals.get(cat, 0)
            if actual > limit:
                alerts.append(f"⚠️ Overspending in {cat}: Spent ${actual:.2f} vs Limit ${limit:.2f}")
            elif actual > limit * 0.9:
                alerts.append(f"⚠️ Near limit in {cat}: Spent ${actual:.2f} vs Limit ${limit:.2f}")
                
        return {
            "alerts": alerts,
            "aggregated_spending": aggregated_actuals
        }
