import logging
from config import Config
from utils.faq_retriever import FAQRetriever

LOG_FORMAT = '%(asctime)s %(levelname)s %(name)s: %(message)s'
logging.basicConfig(
    level=Config.LOG_LEVEL,
    format=LOG_FORMAT,
    handlers=[
        logging.FileHandler(f"{Config.LOG_DIR}/faq_chatbot.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("faq_chatbot")

class FAQChatbot:
    def __init__(self):
        self.retriever = FAQRetriever()

    def chat(self, user_input):
        answer = self.retriever.retrieve(user_input)
        logger.info(f"User: {user_input} | Bot: {answer}")
        return answer

if __name__ == "__main__":
    bot = FAQChatbot()
    print("FAQ Retrieval Chatbot. Type 'exit' to quit.")
    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            break
        response = bot.chat(user_input)
        print(f"Bot: {response}")
