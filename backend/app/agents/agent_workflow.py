from typing import TypedDict, Annotated, Any, Dict, List
from langchain_core.messages import BaseMessage, AIMessage, HumanMessage, ToolMessage
import operator
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode


class AgentState(TypedDict):
    """
    State definition for the agent workflow.
    """
    messages: Annotated[List[BaseMessage], operator.add]
    user_input: str
    tool_results: List[Dict[str, Any]]
    final_output: str
    iteration_count: int


def create_agent_workflow(llm: Any, tools: Dict[str, Any], system_prompt: str, max_iterations: int = 10):
    """
    Create a LangGraph StateGraph workflow for the agent.
    
    Args:
        llm: The language model instance (e.g., ChatAnthropic)
        tools: Dictionary of available tools
        system_prompt: The system prompt for the agent
        max_iterations: Maximum number of agent loop iterations
        
    Returns:
        Compiled LangGraph application
    """
    from langgraph.graph import StateGraph, END
    
    # Bind tools to LLM
    llm_with_tools = llm.bind_tools(list(tools.values()))
    
    def should_continue(state: AgentState) -> str:
        """
        Determine if the agent should continue or end.
        """
        messages = state["messages"]
        last_message = messages[-1]
        
        # Check if max iterations reached
        if state.get("iteration_count", 0) >= max_iterations:
            return "end"
        
        # If there are no tool calls, end
        if not hasattr(last_message, "tool_calls") or not last_message.tool_calls:
            return "end"
        
        # Otherwise continue to tools
        return "continue"
    
    def call_model(state: AgentState) -> Dict[str, Any]:
        """
        Call the LLM with current state.
        """
        messages = state["messages"]
        
        # Add system prompt if this is the first call
        if len(messages) == 1:
            messages = [
                {"role": "system", "content": system_prompt},
                *messages
            ]
        
        response = llm_with_tools.invoke(messages)
        
        return {
            "messages": [response],
            "iteration_count": state.get("iteration_count", 0) + 1
        }
    
    def call_tools(state: AgentState) -> Dict[str, Any]:
        """
        Execute tools based on the model's tool calls.
        """
        messages = state["messages"]
        last_message = messages[-1]
        
        tool_results = []
        
        # Execute each tool call
        if hasattr(last_message, "tool_calls"):
            for tool_call in last_message.tool_calls:
                tool_name = tool_call["name"]
                tool_args = tool_call["args"]
                
                # Execute the tool
                try:
                    if tool_name in tools:
                        tool_output = tools[tool_name].invoke(tool_args)
                    else:
                        tool_output = f"Error: Tool '{tool_name}' not found in available tools"
                except Exception as e:
                    tool_output = f"Error executing tool '{tool_name}': {str(e)}"
                
                tool_results.append({
                    "tool_name": tool_name,
                    "output": tool_output
                })
                
                # Create tool message
                tool_message = ToolMessage(
                    content=str(tool_output),
                    tool_call_id=tool_call["id"]
                )
                messages.append(tool_message)
        
        return {
            "tool_results": tool_results,
            "messages": messages
        }
    
    # Build the graph
    workflow = StateGraph(AgentState)
    
    # Add nodes
    workflow.add_node("agent", call_model)
    workflow.add_node("tools", call_tools)
    
    # Set entry point
    workflow.set_entry_point("agent")
    
    # Add conditional edges
    workflow.add_conditional_edges(
        "agent",
        should_continue,
        {
            "continue": "tools",
            "end": END
        }
    )
    
    # Add edge from tools back to agent
    workflow.add_edge("tools", "agent")
    
    # Compile and return
    return workflow.compile()
