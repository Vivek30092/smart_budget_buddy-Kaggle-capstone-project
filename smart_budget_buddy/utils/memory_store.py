import json
import os
from datetime import datetime

class MemoryStore:
    def __init__(self, file_path='user_data.json'):
        self.file_path = file_path
        self.data = self._load_data()

    def _load_data(self):
        if os.path.exists(self.file_path):
            try:
                with open(self.file_path, 'r') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                return self._init_structure()
        else:
            return self._init_structure()

    def _init_structure(self):
        return {
            "user_profile": {},
            "conversation_history": [],
            "budget_plans": [],
            "goals": []
        }

    def save_data(self):
        with open(self.file_path, 'w') as f:
            json.dump(self.data, f, indent=4)

    def update_profile(self, profile_data):
        self.data["user_profile"].update(profile_data)
        self.save_data()

    def get_profile(self):
        return self.data.get("user_profile", {})

    def add_chat_message(self, role, content):
        message = {
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat()
        }
        self.data["conversation_history"].append(message)
        self.save_data()

    def get_history(self):
        return self.data.get("conversation_history", [])

    def clear_history(self):
        self.data["conversation_history"] = []
        self.save_data()

    def save_budget_plan(self, plan):
        plan['timestamp'] = datetime.now().isoformat()
        self.data["budget_plans"].append(plan)
        self.save_data()

    def get_latest_budget(self):
        if self.data["budget_plans"]:
            return self.data["budget_plans"][-1]
        return None
