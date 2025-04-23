"""Event classes for agent interactions."""
from dataclasses import dataclass
from typing import Dict, Any, Optional, List


@dataclass
class AgentEvent:
    """Base class for all agent events."""
    event_type: str


@dataclass
class UserQueryEvent(AgentEvent):
    """Event representing a user query."""
    query: str

    def __init__(self, query: str):
        super().__init__(event_type="user_query")
        self.query = query


@dataclass
class AgentResponseEvent(AgentEvent):
    """Event representing an agent response."""
    text: str
    
    def __init__(self, text: str):
        super().__init__(event_type="agent_response")
        self.text = text


@dataclass
class ToolCallEvent(AgentEvent):
    """Event representing a tool call."""
    name: str
    args: Dict[str, Any]
    
    def __init__(self, name: str, args: Dict[str, Any]):
        super().__init__(event_type="tool_call")
        self.name = name
        self.args = args


@dataclass
class ToolResponseEvent(AgentEvent):
    """Event representing a tool response."""
    name: str
    response: Any
    
    def __init__(self, name: str, response: Any):
        super().__init__(event_type="tool_response")
        self.name = name
        self.response = response


@dataclass
class FinalResponseEvent(AgentEvent):
    """Event representing the final response from the agent."""
    text: str
    
    def __init__(self, text: str):
        super().__init__(event_type="final_response")
        self.text = text


@dataclass
class ConversationStartEvent(AgentEvent):
    """Event indicating the start of a conversation."""
    
    def __init__(self):
        super().__init__(event_type="conversation_start")


@dataclass
class ConversationEndEvent(AgentEvent):
    """Event indicating the end of a conversation."""
    
    def __init__(self):
        super().__init__(event_type="conversation_end")


@dataclass
class ErrorEvent(AgentEvent):
    """Event representing an error in the agent processing."""
    message: str
    
    def __init__(self, message: str):
        super().__init__(event_type="error")
        self.message = message