"""
Bedrock Client Wrapper for Customer Support Chatbot
Handles all interactions with AWS Bedrock
"""

import boto3
import json
import logging
from typing import List, Dict, Optional
from botocore.exceptions import BotoCoreError, ClientError

logger = logging.getLogger(__name__)


class BedrockClient:
    """Wrapper for AWS Bedrock Claude 3.5 Sonnet model"""

    def __init__(self, model_id: str, region: str = "us-east-1", profile: str = "default"):
        """
        Initialize Bedrock client
        
        Args:
            model_id: The model ID to use (e.g., anthropic.claude-3-5-sonnet-20241022-v2:0)
            region: AWS region
            profile: AWS profile name
        """
        self.model_id = model_id
        self.region = region
        
        try:
            # Create Bedrock runtime client
            session = boto3.Session(profile_name=profile, region_name=region)
            self.client = session.client("bedrock-runtime", region_name=region)
            logger.info(f"Bedrock client initialized with model: {model_id}")
        except Exception as e:
            logger.error(f"Failed to initialize Bedrock client: {e}")
            raise

    def invoke_model(
        self,
        messages: List[Dict[str, str]],
        system_prompt: str,
        temperature: float = 0.7,
        max_tokens: int = 1000,
        top_p: float = 0.95,
    ) -> Optional[str]:
        """
        Invoke Claude model with conversation messages
        
        Args:
            messages: List of message dicts with 'role' and 'content'
            system_prompt: System instructions for the model
            temperature: Model temperature (0-1)
            max_tokens: Maximum tokens in response
            top_p: Top-p sampling parameter
            
        Returns:
            Model response text or None on error
        """
        try:
            # Prepare request body for Claude
            request_body = {
                "anthropic_version": "bedrock-2023-05-31",
                
                "max_tokens": max_tokens,
                "system": system_prompt,
                "messages": messages,
                "temperature": temperature,
                "top_p": top_p,
            }

            # Invoke model
            response = self.client.invoke_model(
                modelId=self.model_id,
                body=json.dumps(request_body),
            )

            # Parse response
            response_body = json.loads(response["body"].read())
            
            if response_body.get("content") and len(response_body["content"]) > 0:
                return response_body["content"][0].get("text", "")
            else:
                logger.warning("Empty response from Bedrock")
                return None

        except ClientError as e:
            error_code = e.response.get("Error", {}).get("Code", "")
            error_msg = e.response.get("Error", {}).get("Message", "")
            
            if error_code == "ResourceNotFoundException" and "use case details" in error_msg:
                logger.error(
                    f"Bedrock model access error: {error_msg}\n"
                    "ACTION REQUIRED: Complete the Anthropic use case details form in AWS Console > Bedrock > Model Access"
                )
            else:
                logger.error(f"Bedrock client error: {e}")
            return None
        except BotoCoreError as e:
            logger.error(f"Bedrock boto error: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error invoking Bedrock: {e}")
            return None

    def get_token_count(self, text: str) -> int:
        """
        Estimate token count for text
        (Claude typically uses ~1 token per 4 characters)
        
        Args:
            text: Text to count tokens for
            
        Returns:
            Estimated token count
        """
        # Rough approximation: Claude tokenizer averages ~1 token per 4 characters
        return len(text) // 4

    def format_messages(
        self, 
        conversation_history: List[Dict[str, str]], 
        user_message: str
    ) -> List[Dict[str, str]]:
        """
        Format conversation history for API call
        
        Args:
            conversation_history: List of previous messages
            user_message: Current user message
            
        Returns:
            Formatted messages list
        """
        messages = []
        
        # Add conversation history
        for msg in conversation_history:
            messages.append({
                "role": msg.get("role", "user"),
                "content": msg.get("content", "")
            })
        
        # Add current user message
        messages.append({
            "role": "user",
            "content": user_message
        })
        
        return messages
