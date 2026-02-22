import json
from config import Config

class FAQRetriever:
    def __init__(self, data_path=None):
        self.data_path = data_path or Config.FAQ_DATA_PATH
        self.faqs = self.load_faqs()

    def load_faqs(self):
        with open(self.data_path, 'r') as f:
            return json.load(f)

    def retrieve(self, question):
        # Simple keyword match; can be replaced with semantic search
        question_lower = question.lower()
        for faq in self.faqs:
            if faq["question"].lower() in question_lower or question_lower in faq["question"].lower():
                return faq["answer"]
        return "Sorry, I couldn't find an answer to your question."
