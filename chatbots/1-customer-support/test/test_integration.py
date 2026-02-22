"""
Integration test for Customer Support Chatbot
Tests actual Bedrock API calls (requires AWS credentials and permissions)
"""

from app import CustomerSupportChatbot

def test_bedrock_integration():
    """Test actual Bedrock API integration"""
    
    print("\n" + "="*60)
    print("🧪 Integration Test: Bedrock API Call")
    print("="*60 + "\n")
    
    try:
        print("Initializing chatbot...")
        chatbot = CustomerSupportChatbot()
        print("✓ Chatbot initialized\n")
        
        print("Testing actual API call to Bedrock...")
        print("Sending test message: 'What is your support email?'\n")
        
        response = chatbot.get_response("What is your support email?")
        
        if response:
            print(f"✓ API call successful!")
            print(f"Response: {response}\n")
            print("="*60)
            print("✅ Integration test PASSED!")
            print("="*60)
            return True
        else:
            print("✗ Empty response from API\n")
            return False
            
    except Exception as e:
        error_msg = str(e)
        print(f"✗ Integration test FAILED!\n")
        print(f"Error: {error_msg}\n")
        
        if "AccessDenied" in error_msg or "not authorized" in error_msg:
            print("🔐 AWS Permission Issue Detected:")
            print("   Your user doesn't have bedrock:InvokeModel permission")
            print("\n   Solution: See AWS_BEDROCK_SETUP.md for instructions")
            print("            to add the required IAM policy\n")
        
        print("="*60)
        print("❌ Integration test FAILED")
        print("="*60 + "\n")
        return False

if __name__ == "__main__":
    success = test_bedrock_integration()
    exit(0 if success else 1)
