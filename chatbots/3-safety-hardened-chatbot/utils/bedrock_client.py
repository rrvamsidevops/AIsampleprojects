"""
Bedrock Client Wrapper for Safety-Hardened Chatbot
"""

import boto3
import json
import logging
from typing import List, Dict, Optional
from botocore.exceptions import ClientError, BotoCoreError

import config

logger = logging.getLogger(__name__)


class BedrockClient:
    """Wrapper for AWS Bedrock Claude 3.5 Sonnet model"""

    def __init__(self):
        """Initialize Bedrock client"""
        try:
            session = boto3.Session(
                profile_name=config.AWS_PROFILE,
                region_name=config.AWS_REGION
            )
            self.client = session.client("bedrock-runtime", region_name=config.AWS_REGION)
            self.model_id = config.BEDROCK_MODEL_ID
            logger.info(f"Bedrock client initialized with model: {self.model_id}")
        except Exception as e:
            logger.error(f"Failed to initialize Bedrock client: {e}")
            raise

    def invoke_model(
        self,
        messages: List[Dict[str, str]],
        system_prompt: str,
        temperature: float = 0.3,
        max_tokens: int = 1000,
    ) -> Optional[str]:
        """
        Invoke Claude model with conversation messages
        
        Args:
            messages: List of message dicts with 'role' and 'content'
            system_prompt: System instructions for the model
            temperature: Model temperature (0-1)
            max_tokens: Maximum tokens in response
            
        Returns:
            Model response text or None on error
        """
        try:
            # Prepare request body
            request_body = {
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": max_tokens,
                "system": system_prompt,
                "messages": messages,
                "temperature": temperature
            }

            # Invoke model
            response = self.client.invoke_model(
                modelId=self.model_id,
                body=json.dumps(request_body)
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
