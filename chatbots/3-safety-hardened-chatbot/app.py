"""
Main Safety-Hardened Chatbot Application
Built with AWS Bedrock (Claude 3.5 Sonnet) + Safety Guardrails
"""

import logging
import sys
from typing import Optional, List, Dict

import config
from utils.bedrock_client import BedrockClient
from utils import SafetyMetrics
from security.input_validator import InputValidator
from security.output_filter import OutputFilter
from security.pii_detector import PIIDetector
from security.jailbreak_detector import JailbreakDetector
from security import GuardrailsManager

# Configure logging
logging.basicConfig(
    level=config.LOG_LEVEL,
    format=config.LOG_FORMAT,
    handlers=[
        logging.FileHandler(config.LOG_FILE) if config.ENABLE_LOGGING else logging.NullHandler(),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)


class SafetyHardenedChatbot:
    """Safety-focused chatbot with multi-layer protection"""

    def __init__(self):
        """Initialize chatbot with safety components"""
        try:
            self.bedrock_client = BedrockClient()
            self.system_prompt = self._load_system_prompt()
            self.conversation_history: List[Dict[str, str]] = []
            
            # Safety components
            self.input_validator = InputValidator()
            self.output_filter = OutputFilter()
            self.pii_detector = PIIDetector()
            self.jailbreak_detector = JailbreakDetector()
            self.guardrails_manager = GuardrailsManager()
            self.metrics = SafetyMetrics()
            
            logger.info("Safety-Hardened Chatbot initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize chatbot: {e}")
            raise

    def _load_system_prompt(self) -> str:
        """Load system prompt from file"""
        try:
            with open(config.SYSTEM_PROMPT_FILE, "r") as f:
                prompt = f.read().strip()
            logger.info("System prompt loaded successfully")
            return prompt
        except FileNotFoundError:
            logger.warning(f"System prompt file not found: {config.SYSTEM_PROMPT_FILE}")
            return "You are a helpful and safe AI assistant. Always refuse harmful requests."

    def get_response(self, user_message: str) -> Optional[str]:
        """
        Get chatbot response with full safety pipeline
        
        Args:
            user_message: User's message
            
        Returns:
            Chatbot response or None on error
        """
        self.metrics.record_request()
        
        try:
            # Step 1: Input Validation
            user_message = user_message.strip()
            is_valid, error_msg, details = self.input_validator.validate(user_message)
            
            if not is_valid:
                logger.warning(f"Input validation failed: {details}")
                self.metrics.record_blocked()
                return error_msg
            
            # Step 2: PII Detection
            if config.PII_DETECTION_ENABLED:
                pii_findings = self.pii_detector.detect(user_message)
                if pii_findings:
                    self.metrics.record_pii_detection()
                    user_message, _ = self.pii_detector.redact(user_message)
                    logger.warning(f"PII detected and redacted: {pii_findings}")
            
            # Step 3: Jailbreak Detection
            jailbreak_info = self.jailbreak_detector.detect(user_message)
            if jailbreak_info:
                logger.warning(f"Jailbreak attempt detected: {jailbreak_info}")
                self.metrics.record_jailbreak_attempt()
                self.metrics.record_blocked()
                return config.ERROR_MESSAGES["jailbreak_detected"]
            
            # Step 4: Bedrock Guardrails
            guardrail_result = self.guardrails_manager.apply_guardrails(user_message)
            if not guardrail_result.get("safe", True):
                logger.warning(f"Guardrails violation: {guardrail_result}")
                self.metrics.record_safety_violation()
                self.metrics.record_blocked()
                return config.ERROR_MESSAGES["safety_violation"]
            
            # Step 5: Get Bedrock Response
            messages = self.conversation_history.copy()
            messages.append({"role": "user", "content": user_message})
            
            logger.debug(f"Calling Bedrock with {len(messages)} messages")
            assistant_response = self.bedrock_client.invoke_model(
                messages=messages,
                system_prompt=self.system_prompt,
                temperature=config.MODEL_TEMPERATURE,
                max_tokens=config.MODEL_MAX_TOKENS
            )
            
            if not assistant_response:
                logger.warning("Empty response from Bedrock")
                return config.ERROR_MESSAGES["bedrock_error"]
            
            # Step 6: Output Filtering
            is_safe, filtered_response, filter_details = self.output_filter.filter(assistant_response)
            
            if not is_safe:
                logger.warning(f"Output filtering failed: {filter_details}")
                self.metrics.record_safety_violation()
                return config.ERROR_MESSAGES["toxic_output"]
            
            # Step 7: PII Redaction in Output
            if config.REDACT_PII:
                filtered_response, pii_out = self.pii_detector.redact(filtered_response)
                if pii_out:
                    logger.warning(f"PII found in output, redacted: {pii_out}")
                    self.metrics.record_pii_detection()
            
            # Update conversation history
            self.conversation_history.append({"role": "user", "content": user_message})
            self.conversation_history.append({"role": "assistant", "content": filtered_response})
            
            # Trim history if needed
            if len(self.conversation_history) > config.MAX_CONVERSATION_HISTORY:
                self.conversation_history = self.conversation_history[-config.MAX_CONVERSATION_HISTORY:]
            
            self.metrics.record_success()
            logger.info(f"Response generated successfully (safety_score: {self.metrics.calculate_safety_score():.1f}%)")
            
            return filtered_response
            
        except Exception as e:
            logger.error(f"Error getting response: {e}")
            self.metrics.record_safety_violation()
            return config.ERROR_MESSAGES["bedrock_error"]

    def get_safety_status(self) -> Dict:
        """Get current safety metrics"""
        return {
            "metrics": self.metrics.get_metrics(),
            "safety_score": self.metrics.calculate_safety_score(),
            "guardrails_enabled": config.GUARDRAILS_ENABLED,
            "pii_detection_enabled": config.PII_DETECTION_ENABLED,
        }

    def reset_conversation(self) -> None:
        """Reset conversation history"""
        self.conversation_history = []
        logger.info("Conversation history reset")


def main():
    """Main chat loop"""
    print("\n" + "="*60)
    print("🔒 Safety-Hardened Chatbot")
    print("="*60)
    print("With multi-layer protection against jailbreaks & prompt injection")
    print("Type 'exit' to quit, 'safety' for status\n")
    
    try:
        chatbot = SafetyHardenedChatbot()
        print("✓ Chatbot ready!\n")
        
        while True:
            try:
                user_input = input("You: ").strip()
                
                if not user_input:
                    continue
                
                if user_input.lower() in ["exit", "quit", "bye"]:
                    print("\nThank you for using Safety-Hardened Chatbot. Goodbye!")
                    chatbot.metrics.save_metrics()
                    break
                
                if user_input.lower() == "safety":
                    status = chatbot.get_safety_status()
                    print(f"\n🛡️  Safety Status:")
                    print(f"  Safety Score: {status['safety_score']:.1f}%")
                    print(f"  Total Requests: {status['metrics']['total_requests']}")
                    print(f"  Blocked: {status['metrics']['blocked_requests']}")
                    print(f"  Successful: {status['metrics']['successful_responses']}")
                    print(f"  PII Detections: {status['metrics']['pii_detections']}")
                    print(f"  Jailbreak Attempts: {status['metrics']['jailbreak_attempts']}\n")
                    continue
                
                response = chatbot.get_response(user_input)
                if response:
                    print(f"\nChatbot: {response}\n")
                else:
                    print(f"\nChatbot: {config.ERROR_MESSAGES['bedrock_error']}\n")
                    
            except KeyboardInterrupt:
                print("\n\nChatbot interrupted.")
                break
            except Exception as e:
                logger.error(f"Error in chat loop: {e}")
                print(f"\nAn error occurred. Please try again.\n")
    
    except Exception as e:
        logger.error(f"Failed to start chatbot: {e}")
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
