import unittest
from utils.faq_retriever import FAQRetriever

class TestFAQRetriever(unittest.TestCase):
    def setUp(self):
        self.retriever = FAQRetriever("data/faq.json")

    def test_exact_match(self):
        self.assertEqual(
            self.retriever.retrieve("What is your return policy?"),
            "You can return any item within 30 days of purchase."
        )

    def test_partial_match(self):
        self.assertIn(
            self.retriever.retrieve("return policy"),
            [
                "You can return any item within 30 days of purchase.",
                "Sorry, I couldn't find an answer to your question."
            ]
        )

    def test_no_match(self):
        self.assertEqual(
            self.retriever.retrieve("How do I cancel my subscription?"),
            "Sorry, I couldn't find an answer to your question."
        )

if __name__ == "__main__":
    unittest.main()
