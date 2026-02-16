"""
Conversation state management for Multi-Intent Chatbot
"""

import json
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime
import config


class ConversationState:
    """Manages conversation state across multiple intents"""
    
    def __init__(self):
        """Initialize conversation state"""
        self.logger = logging.getLogger(__name__)
        
        # Conversation tracking
        self.conversation_history: List[Dict] = []
        self.turn_count = 0
        
        # Intent tracking
        self.current_intent: Optional[str] = None
        self.intent_history: List[str] = []
        
        # Per-intent state
        self.intent_states: Dict[str, Dict] = {
            "booking": {},
            "cancellation": {},
            "refund": {},
            "information": {},
            "complaint": {}
        }
        
        # Overall conversation context
        self.context: Dict[str, Any] = {
            "started_at": datetime.now().isoformat(),
            "last_intent_switch": None,
            "intent_switches_count": 0
        }
    
    def add_message(self, role: str, content: str) -> None:
        """Add message to conversation history"""
        self.conversation_history.append({
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat()
        })
        self.turn_count += 1
        self.logger.debug(f"Added {role} message (turn {self.turn_count})")
    
    def get_history_for_api(self) -> List[Dict]:
        """Get conversation history in Bedrock format (without timestamps)"""
        return [{"role": m["role"], "content": m["content"]} 
                for m in self.conversation_history[-config.MAX_HISTORY_TURNS * 2:]]
    
    def set_current_intent(self, intent: str) -> bool:
        """
        Set current intent, tracking switches
        
        Returns:
            True if this is a new intent, False if same intent
        """
        if intent != self.current_intent:
            self.logger.info(f"Intent switch: {self.current_intent} → {intent}")
            self.current_intent = intent
            self.intent_history.append(intent)
            self.context["last_intent_switch"] = datetime.now().isoformat()
            self.context["intent_switches_count"] += 1
            return True
        return False
    
    def update_intent_state(self, intent: str, key: str, value: Any) -> None:
        """Update state for specific intent"""
        if intent not in self.intent_states:
            self.logger.warning(f"Unknown intent: {intent}")
            return
        self.intent_states[intent][key] = value
        self.logger.debug(f"Updated {intent} state: {key} = {value}")
    
    def get_intent_state(self, intent: str) -> Dict:
        """Get state for specific intent"""
        return self.intent_states.get(intent, {})
    
    def validate_intent_state(self, intent: str, required_params: List[str]) -> Dict:
        """
        Validate that required parameters are present for intent
        
        Returns:
            Dict with missing and present parameters
        """
        intent_state = self.get_intent_state(intent)
        present = [p for p in required_params if p in intent_state]
        missing = [p for p in required_params if p not in intent_state]
        
        return {
            "present": present,
            "missing": missing,
            "is_valid": len(missing) == 0
        }
    
    def get_summary(self) -> Dict:
        """Get conversation state summary"""
        return {
            "turn_count": self.turn_count,
            "current_intent": self.current_intent,
            "intent_history": self.intent_history,
            "intent_states": self.intent_states,
            "context": self.context
        }
    
    def should_refresh_state(self) -> bool:
        """Check if state should be refreshed (every N turns)"""
        return self.turn_count % config.STATE_REFRESH_FREQUENCY == 0
    
    def clear_intent_state(self, intent: str) -> None:
        """Clear state for specific intent (when user switches away)"""
        if intent in self.intent_states:
            self.intent_states[intent].clear()
            self.logger.debug(f"Cleared state for intent: {intent}")
