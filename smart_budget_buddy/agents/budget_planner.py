class BudgetPlannerAgent:
    def __init__(self, profile):
        self.profile = profile

    def generate_budget(self):
        """
        Generates a monthly budget based on the student profile.
        """
        income = self.profile.get('monthly_income', 0) + self.profile.get('financial_aid', 0)
        
        # Fixed expenses (assuming these are monthly for the sake of the budget, 
        # though tuition might be semesterly. We'll treat them as allocated monthly costs)
        # Actually, tuition is usually large. Let's assume the user wants to budget for *variable* spending
        # given their income and fixed costs.
        
        fixed_costs = {
            'tuition': self.profile.get('tuition', 0) / 6, # Assuming semester
            'housing': self.profile.get('housing', 0),
            'transportation': self.profile.get('transportation', 0)
        }
        
        total_fixed = sum(fixed_costs.values())
        disposable_income = income - total_fixed
        
        # Recommended allocation for variable categories (50/30/20 rule adaptation)
        # We'll just allocate remaining income to categories based on their historical spending in the profile
        # or set reasonable limits.
        
        # Categories for variable spending
        categories = ['food', 'books_supplies', 'entertainment', 'personal_care', 'technology', 'health_wellness', 'miscellaneous']
        
        # Calculate total historical spending in these categories (if available)
        current_spending = sum(self.profile.get(c, 0) for c in categories)
        
        budget_plan = {
            "total_income": income,
            "fixed_costs": fixed_costs,
            "disposable_income": disposable_income,
            "category_limits": {},
            "recommendations": []
        }
        
        # Standard allocation percentages for variable spending (sum = 1.0)
        allocations = {
            'food': 0.35,
            'books_supplies': 0.15,
            'entertainment': 0.10,
            'personal_care': 0.10,
            'technology': 0.10,
            'health_wellness': 0.10,
            'miscellaneous': 0.10
        }

        if disposable_income < 0:
            budget_plan['recommendations'].append("⚠️ Critical: Your fixed expenses exceed your income. Seek financial aid or reduce housing costs.")
            # Set strict limits (minimal survival budget)
            for cat in categories:
                budget_plan['category_limits'][cat] = 0
        else:
            budget_plan['recommendations'].append("✅ Income covers fixed costs.")
            
            if current_spending > 0:
                # Use historical data logic
                if disposable_income > current_spending:
                     budget_plan['recommendations'].append("You are saving money! Great job.")
                     factor = 1.0 
                else:
                     budget_plan['recommendations'].append("⚠️ You are overspending your disposable income. Reducing variable spending is advised.")
                     factor = disposable_income / current_spending
                
                for cat in categories:
                    limit = self.profile.get(cat, 0) * factor
                    budget_plan['category_limits'][cat] = round(limit, 2)
            else:
                # Use standard allocation logic (New User / Manual Input)
                budget_plan['recommendations'].append("ℹ️ Using standard student budget allocation rules.")
                for cat in categories:
                    limit = disposable_income * allocations.get(cat, 0.1)
                    budget_plan['category_limits'][cat] = round(limit, 2)
            
        return budget_plan
