"""
AWS Bedrock integration for Multi-Intent Chatbot
"""

import json
import logging
import boto3
from typing import Dict, List, Tuple, Optional
from botocore.exceptions import ClientError
import config


class BedrockClient:
    """Wrapper for AWS Bedrock Claude API with tool calling support"""
    
    def __init__(self):
        """Initialize Bedrock client"""
        try:
            # Create session with proper AWS profile and region
            session = boto3.Session(
                profile_name=config.AWS_PROFILE,
                region_name=config.AWS_REGION
            )
            self.client = session.client("bedrock-runtime", region_name=config.AWS_REGION)
            self.model_id = config.BEDROCK_MODEL_ID
            self.logger = logging.getLogger(__name__)
            self.logger.info(f"Bedrock client initialized with model: {self.model_id}")
        except Exception as e:
            logging.getLogger(__name__).error(f"Failed to initialize Bedrock client: {e}")
            raise
    
    def invoke_model(self, 
                    system_prompt: str, 
                    user_message: str, 
                    conversation_history: List[Dict] = None,
                    temperature: float = None,
                    max_tokens: int = None) -> Tuple[str, int]:
        """
        Call Bedrock Claude model with conversation history
        
        Args:
            system_prompt: System instructions for the model
            user_message: Current user message
            conversation_history: Previous messages (role/content format)
            temperature: Model temperature (0-1)
            max_tokens: Maximum tokens in response
        
        Returns:
            Tuple of (response_text, token_count)
        """
        temperature = temperature or config.MODEL_TEMPERATURE
        max_tokens = max_tokens or config.MODEL_MAX_TOKENS
        
        # Format messages with conversation history
        messages = conversation_history or []
        messages.append({"role": "user", "content": user_message})
        
        try:
            # Build request body according to Bedrock API specification
            request_body = {
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": max_tokens,
                "system": system_prompt,
                "messages": messages,
                "temperature": temperature
            }
            
            response = self.client.invoke_model(
                modelId=self.model_id,
                body=json.dumps(request_body)
            )
            
            # Parse response
            response_body = json.loads(response["body"].read())
            response_text = response_body["content"][0]["text"]
            token_count = response_body.get("usage", {}).get("outputTokens", 0)
            
            self.logger.debug(f"API response: {response_text[:100]}...")
            return response_text, token_count
            
        except ClientError as e:
            error_code = e.response["Error"]["Code"]
            self.logger.error(f"Bedrock error ({error_code}): {e.response['Error']['Message']}")
            raise
        except json.JSONDecodeError as e:
            self.logger.error(f"Failed to parse Bedrock response: {e}")
            raise
        except KeyError as e:
            self.logger.error(f"Unexpected response format: {e}")
            raise
    
    def classify_intent(self, user_message: str, conversation_history: List[Dict]) -> Dict:
        """
        Classify user intent using a specialized prompt
        
        Args:
            user_message: Current user message
            conversation_history: Previous messages
        
        Returns:
            Dict with intent classification results
        """
        classifier_prompt = """You are an intent classification expert. 
Analyze the user message and classify it into one of these intents:
1. booking - User wants to book something
2. cancellation - User wants to cancel something
3. refund - User wants a refund
4. information - User asking for information
5. complaint - User has a complaint

Respond with valid JSON only (no markdown):
{
  "intent": "<intent_name>",
  "confidence": <0.0-1.0>,
  "reasoning": "<brief explanation>",
  "extracted_params": {
    "<param_name>": "<param_value>"
  }
}"""
        
        response, _ = self.invoke_model(classifier_prompt, user_message, conversation_history)
        
        try:
            # Parse JSON response
            result = json.loads(response)
            return result
        except json.JSONDecodeError:
            self.logger.warning(f"Failed to parse intent classification response")
            return {
                "intent": "information",
                "confidence": 0.5,
                "reasoning": "Could not classify, defaulting to information",
                "extracted_params": {}
            }
    
    def extract_parameters(self, 
                          intent_type: str, 
                          user_message: str,
                          conversation_history: List[Dict]) -> Dict:
        """
        Extract parameters for a specific intent
        
        Args:
            intent_type: Type of intent
            user_message: Current message
            conversation_history: Conversation so far
        
        Returns:
            Dict with extracted parameters
        """
        prompt = f"""Extract parameters for a {intent_type} intent.
User message: {user_message}

Respond with valid JSON only (no markdown):
{{
  "extracted": {{"<param_name>": "<value>"}},
  "missing": ["<param_name>"],
  "confidence": <0.0-1.0>
}}"""
        
        response, _ = self.invoke_model(prompt, user_message, conversation_history)
        
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            self.logger.warning(f"Failed to parse parameter extraction")
            return {
                "extracted": {},
                "missing": [],
                "confidence": 0.0
            }
    
    def generate_response(self,
                         system_prompt: str,
                         user_message: str,
                         conversation_history: List[Dict],
                         intent_context: Optional[Dict] = None) -> str:
        """
        Generate a response for the user
        
        Args:
            system_prompt: Intent-specific system prompt
            user_message: User's message
            conversation_history: Previous messages
            intent_context: Context about current intent
        
        Returns:
            Generated response text
        """
        # Enhance system prompt with intent context if provided
        if intent_context:
            system_prompt += f"\n\nCurrent Intent Context:\n{json.dumps(intent_context, indent=2)}"
        
        response, _ = self.invoke_model(system_prompt, user_message, conversation_history)
        return response
