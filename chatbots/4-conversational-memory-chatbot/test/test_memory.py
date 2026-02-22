import unittest
from utils.memory import MemoryManager

class TestMemoryManager(unittest.TestCase):
    def test_short_term_memory(self):
        mem = MemoryManager(memory_type="short-term", window=3)
        mem.update("hi", "hello")
        mem.update("how are you?", "I'm good.")
        mem.update("what's up?", "Not much.")
        mem.update("bye", "goodbye")
        history = mem.get_history()
        self.assertEqual(len(history), 3)
        self.assertEqual(history[-1]["user"], "bye")

    def test_long_term_memory(self):
        mem = MemoryManager(memory_type="long-term")
        mem.update("hi", "hello")
        mem.update("how are you?", "I'm good.")
        history = mem.get_history()
        self.assertEqual(len(history), 2)
        self.assertEqual(history[0]["user"], "hi")

if __name__ == "__main__":
    unittest.main()
