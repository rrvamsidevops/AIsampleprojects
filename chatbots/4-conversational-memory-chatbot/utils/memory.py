from collections import deque

class MemoryManager:
    def __init__(self, memory_type="short-term", window=5):
        self.memory_type = memory_type
        self.window = window
        self.history = deque(maxlen=window) if memory_type == "short-term" else []

    def update(self, user_input, bot_response):
        entry = {"user": user_input, "bot": bot_response}
        if self.memory_type == "short-term":
            self.history.append(entry)
        else:
            self.history.append(entry)  # For long-term, could be persisted externally

    def get_history(self):
        if self.memory_type == "short-term":
            return list(self.history)
        else:
            return list(self.history)  # Extend for persistent storage
