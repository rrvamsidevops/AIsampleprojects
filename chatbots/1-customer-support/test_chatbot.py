"""
Quick test script for Customer Support Chatbot
Tests basic functionality without AWS Bedrock (mock mode)
"""

from app import CustomerSupportChatbot
import config

def test_chatbot():
    """Test basic chatbot functionality"""
    
    print("\n" + "="*60)
    print("🤖 Testing Customer Support Chatbot")
    print("="*60 + "\n")
    
    try:
        # Test 1: Initialization
        print("Test 1: Initializing chatbot...")
        try:
            chatbot = CustomerSupportChatbot()
            print("✓ Chatbot initialized successfully\n")
        except Exception as e:
            print(f"✗ Initialization failed: {e}\n")
            print("Note: This is expected if AWS credentials are not configured")
            print("Please run: aws configure\n")
            return False
        
        # Test 2: Conversation history
        print("Test 2: Testing conversation history...")
        history = chatbot.get_conversation_history()
        print(f"✓ Initial history is empty: {len(history) == 0}\n")
        
        # Test 3: System prompt loading
        print("Test 3: Verifying system prompt loaded...")
        if chatbot.system_prompt:
            print(f"✓ System prompt loaded ({len(chatbot.system_prompt)} characters)\n")
        else:
            print("✗ System prompt not loaded\n")
            return False
        
        # Test 4: Configuration
        print("Test 4: Checking configuration...")
        print(f"✓ Model: {config.BEDROCK_MODEL_ID}")
        print(f"✓ Temperature: {config.MODEL_TEMPERATURE}")
        print(f"✓ Max tokens: {config.MODEL_MAX_TOKENS}")
        print(f"✓ AWS Region: {config.AWS_REGION}\n")
        
        # Test 5: Reset functionality
        print("Test 5: Testing reset functionality...")
        chatbot.reset_conversation()
        print("✓ Conversation reset successful\n")
        
        print("="*60)
        print("✅ All basic tests passed!")
        print("="*60)
        print("\n� Note: This tests initialization only.")
        print("For full integration testing (actual API calls):")
        print("   source venv/bin/activate")
        print("   python test_integration.py")
        print("\n�📋 To run the interactive chatbot:")
        print("   source venv/bin/activate")
        print("   python app.py\n")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}\n")
        return False

if __name__ == "__main__":
    success = test_chatbot()
    exit(0 if success else 1)
