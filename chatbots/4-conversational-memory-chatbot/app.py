import logging
from config import Config
from utils.memory import MemoryManager
# from utils.bedrock_client import BedrockClient  # Uncomment if using Bedrock

LOG_FORMAT = '%(asctime)s %(levelname)s %(name)s: %(message)s'
logging.basicConfig(
    level=Config.LOG_LEVEL,
    format=LOG_FORMAT,
    handlers=[
        logging.FileHandler(f"{Config.LOG_DIR}/chatbot.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("chatbot")

class Chatbot:
    def __init__(self):
        self.memory = MemoryManager(memory_type=Config.MEMORY_TYPE, window=Config.MEMORY_WINDOW)
        # self.llm = BedrockClient(...)

    def chat(self, user_input):
        history = self.memory.get_history()
        prompt = self.compose_prompt(user_input, history)
        # response = self.llm.generate(prompt)
        response = f"[MOCK RESPONSE] {user_input} (context: {history})"
        self.memory.update(user_input, response)
        logger.info(f"User: {user_input} | Bot: {response}")
        return response

    def compose_prompt(self, user_input, history):
        # Load prompt template and inject memory/context
        return f"User: {user_input}\nHistory: {history}"

if __name__ == "__main__":
    bot = Chatbot()
    print("Conversational Memory Chatbot. Type 'exit' to quit.")
    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            break
        response = bot.chat(user_input)
        print(f"Bot: {response}")
