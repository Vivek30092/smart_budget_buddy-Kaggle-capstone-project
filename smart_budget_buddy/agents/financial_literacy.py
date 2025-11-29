import google.generativeai as genai

class FinancialLiteracyAgent:
    def __init__(self, api_key=None):
        self.history = []
        self.api_key = api_key
        self.model = None
        
        if self.api_key:
            try:
                genai.configure(api_key=self.api_key)
                self.model = genai.GenerativeModel('gemini-pro')
            except Exception as e:
                print(f"Error configuring Gemini API: {e}")
                self.model = None

        # Fallback Knowledge Base
        self.knowledge_base = {
            "budget": "💡 **Budgeting** is creating a plan for your money. It helps you balance income and expenses so you don't overspend. Try the 50/30/20 rule: 50% needs, 30% wants, 20% savings!",
            "saving": "💰 **Saving** means setting aside money for future goals. Start small! Even saving $10 a week adds up. Try automating transfers to a savings account.",
            "expense": "📉 **Expense tracking** is recording every purchase. Use apps or a simple notebook. Knowing where your money goes is the first step to controlling it.",
            "goal": "🎯 **Goal-based planning** means saving for specific things (like a laptop or trip). Set a target amount and a deadline, then break it down into monthly savings targets.",
            "emergency": "🚨 An **emergency fund** is money saved for unexpected costs like car repairs or medical bills. Aim for $500-$1000 to start.",
            "student": "🎓 **Student Tip**: Take advantage of student discounts! Always carry your ID. Buy used textbooks, cook at home, and use campus resources."
        }
        self.restricted_topics = ["stock", "invest", "crypto", "bitcoin", "loan", "credit card", "borrow", "trading", "mutual fund", "bond", "debt"]

    def ask(self, query):
        """
        Processes a user query. Uses LLM if available, otherwise falls back to keyword matching.
        """
        self.history.append({"role": "user", "content": query})
        
        # 1. LLM Response (if API Key is valid)
        if self.model:
            try:
                # System Prompt for Guardrails
                system_instruction = """
                You are Smart Budget Buddy, a helpful AI assistant for students.
                Your goal is to teach financial literacy, budgeting, and saving tips.
                
                STRICT GUARDRAILS:
                1. You MUST NOT give investment advice (stocks, crypto, trading).
                2. You MUST NOT recommend specific loans, credit cards, or debt products.
                3. If asked about restricted topics, politely decline and steer back to budgeting/saving.
                4. Keep answers short, encouraging, and student-friendly.
                5. Use emojis to be engaging.
                """
                
                full_prompt = f"{system_instruction}\n\nUser Query: {query}"
                response_obj = self.model.generate_content(full_prompt)
                response = response_obj.text
                
                self.history.append({"role": "assistant", "content": response})
                return response
            except Exception as e:
                return f"⚠️ API Error: {e}. Switching to offline mode."

        # 2. Fallback Logic (Offline Mode)
        query_lower = query.lower()
        
        # Guardrails check for offline mode
        for topic in self.restricted_topics:
            if topic in query_lower:
                response = "🚫 Sorry, I only assist with student budget management. I cannot provide advice on investments or loans."
                self.history.append({"role": "assistant", "content": response})
                return response

        response = None
        for key, value in self.knowledge_base.items():
            if key in query_lower:
                response = value
                break
        
        if not response:
            response = "🤔 I can help you with budgeting, saving, and tracking expenses. (Add an API Key for smarter answers!)"

        self.history.append({"role": "assistant", "content": response})
        return response

    def get_history(self):
        # Convert internal history format to Streamlit chat format if needed, 
        # or just return as is. The app expects [{'user':..., 'buddy':...}] or similar.
        # Let's adapt the return to match the existing app structure for compatibility.
        formatted_history = []
        for i in range(0, len(self.history) - 1, 2):
            if self.history[i]['role'] == 'user' and self.history[i+1]['role'] == 'assistant':
                formatted_history.append({
                    "user": self.history[i]['content'], 
                    "buddy": self.history[i+1]['content']
                })
        return formatted_history

    def clear_history(self):
        self.history = []
