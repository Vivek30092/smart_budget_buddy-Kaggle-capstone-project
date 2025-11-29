import google.generativeai as genai
import json
import os
from ..utils.memory_store import MemoryStore
from .tools import calculate_budget_tool, expense_classifier_tool, memory_lookup_tool, memory_update_tool, dataset_loader_tool

class FinancialLiteracyChatBot:
    def __init__(self, api_key=None):
        self.memory = MemoryStore()
        self.api_key = api_key
        self.model = None
        
        if self.api_key:
            try:
                genai.configure(api_key=self.api_key)
                self.model = genai.GenerativeModel('gemini-2.5-flash-lite')
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
        
        # Strict Restricted Topics
        self.restricted_topics = [
            "stock", "invest", "crypto", "bitcoin", "loan", "credit card", "borrow", "trading", 
            "mutual fund", "bond", "debt", "gamble", "gambling", "betting", "casino", 
            "politics", "political", "election", "vote", "hack", "hacking", "illegal", 
            "drug", "weapon", "adult", "sex", "porn", "medical", "doctor", "lawyer", "legal"
        ]

    def ask(self, query):
        """
        Processes a user query. Uses LLM if available, otherwise falls back to keyword matching.
        """
        # Save user message to memory
        self.memory.add_chat_message("user", query)
        
        # 1. LLM Response (if API Key is valid)
        if self.model:
            try:
                # System Prompt for Guardrails and Persona
                system_instruction = """
                You are Smart Budget Buddy, an AI financial literacy assistant specifically designed for students.
                Your goal is to teach budgeting, saving, and responsible money habits.
                
                STRICT GUARDRAILS:
                1. You MUST NOT give investment advice (stocks, crypto, trading).
                2. You MUST NOT recommend specific loans, credit cards, or debt products.
                3. You MUST NOT discuss gambling, politics, adult content, hacking, or illegal acts.
                4. You MUST NOT give medical, legal, or mental health advice.
                5. If asked about restricted topics, reply EXACTLY: "I'm here only to help with student budgeting and financial literacy. I cannot assist with that topic."
                6. Keep answers short, crisp, clear, and student-friendly.
                7. Use emojis to be engaging.
                
                AVAILABLE TOOLS:
                - If the user asks to calculate a budget, you can suggest they use the Budget Planner tool in the sidebar.
                - If the user asks about their past data, you can mention you have access to their profile.
                """
                
                # Fetch context from memory
                profile = self.memory.get_profile()
                history = self.memory.get_history()[-5:] # Last 5 messages for context
                
                context_str = f"User Profile: {json.dumps(profile)}\nRecent History: {json.dumps(history)}"
                
                full_prompt = f"{system_instruction}\n\nContext:\n{context_str}\n\nUser Query: {query}"
                
                response_obj = self.model.generate_content(full_prompt)
                response = response_obj.text
                
                # Save assistant response to memory
                self.memory.add_chat_message("assistant", response)
                return response
            except Exception as e:
                return f"⚠️ API Error: {e}. Switching to offline mode."

        # 2. Fallback Logic (Offline Mode)
        query_lower = query.lower()
        
        # Guardrails check for offline mode
        for topic in self.restricted_topics:
            if topic in query_lower:
                response = "I'm here only to help with student budgeting and financial literacy. I cannot assist with that topic."
                self.memory.add_chat_message("assistant", response)
                return response

        response = None
        for key, value in self.knowledge_base.items():
            if key in query_lower:
                response = value
                break
        
        if not response:
            response = "🤔 I can help you with budgeting, saving, and tracking expenses. (Add an API Key for smarter answers!)"

        self.memory.add_chat_message("assistant", response)
        return response

    def get_history(self):
        # Return history formatted for Streamlit
        raw_history = self.memory.get_history()
        return raw_history

    def clear_history(self):
        self.memory.clear_history()
