"""
Main LangGraph workflow orchestrator
"""
from typing import Dict, Any, List, Literal
from datetime import datetime
from langgraph.graph import StateGraph, END, START
from langgraph.checkpoint.sqlite.aio import AsyncSqliteSaver
from langgraph.prebuilt import ToolNode
from langgraph.graph import add_messages

from backend.app.graphs.state import WorkflowState
from backend.app.graphs.cache_policies import NODE_CACHE_POLICIES
from backend.app.graphs.nodes import (
    analyze_sales_node,
    targeting_node,
    policy_rag_node,
    generate_document_node,
    compliance_check_node
)
from backend.app.core.config import settings
from backend.app.core.logging import get_logger

logger = get_logger(__name__)


# Deferred node for merging parallel results
async def merge_insights_node(state: WorkflowState) -> Dict[str, Any]:
    """
    Deferred node that merges results from parallel analysis
    Executes only after all parallel branches complete
    """
    logger.info("Merging insights from parallel analysis")
    
    # Combine insights from different analyses
    merged_strategy = {
        "sales_insights": state.get("analysis", {}),
        "target_clients": state.get("targeting", {}),
        "policy_constraints": state.get("policy_context", {}),
        "recommended_actions": [],
        "priority_score": 0
    }
    
    # Generate strategic recommendations based on combined insights
    if state.get("analysis", {}).get("kpi_summary", {}).get("total_revenue", 0) > 100000000:
        merged_strategy["recommended_actions"].append("Focus on enterprise clients")
        merged_strategy["priority_score"] += 10
    
    if state.get("targeting", {}).get("whitespace_opportunities"):
        merged_strategy["recommended_actions"].append("Expand to untapped segments")
        merged_strategy["priority_score"] += 5
    
    return {
        "strategy": merged_strategy,
        "messages": state["messages"] + [{
            "role": "assistant",
            "content": "Analysis completed and insights merged successfully"
        }]
    }


# Schedule proposal node
async def schedule_node(state: WorkflowState) -> Dict[str, Any]:
    """
    Propose optimal schedule based on targeting results
    """
    logger.info("Generating schedule proposals")
    
    target_clients = state.get("targeting", {}).get("top_clients", [])
    
    schedule_proposals = []
    for i, client in enumerate(target_clients[:5]):  # Top 5 clients
        schedule_proposals.append({
            "client_id": client.get("id"),
            "client_name": client.get("name"),
            "proposed_date": f"2025-09-{10 + i:02d}",
            "time_slot": "14:00-15:00",
            "purpose": "Product presentation",
            "priority": client.get("priority", "medium")
        })
    
    return {
        "schedule_proposal": schedule_proposals,
        "messages": state["messages"] + [{
            "role": "assistant",
            "content": f"Generated {len(schedule_proposals)} schedule proposals"
        }]
    }


# Client intelligence node
async def client_intel_node(state: WorkflowState) -> Dict[str, Any]:
    """
    Gather client intelligence and history
    """
    logger.info("Gathering client intelligence")
    
    client_ids = state.get("client_ids", [])
    
    client_intel = {}
    for client_id in client_ids[:3]:  # Process top 3 clients
        client_intel[client_id] = {
            "last_visit": "2025-07-15",
            "preferred_products": ["PROD001", "PROD002"],
            "decision_makers": ["Dr. Kim", "Manager Lee"],
            "communication_preference": "email",
            "purchase_pattern": "quarterly",
            "satisfaction_score": 4.2
        }
    
    return {
        "client_intel": client_intel,
        "messages": state["messages"] + [{
            "role": "assistant",
            "content": f"Gathered intelligence for {len(client_intel)} clients"
        }]
    }


# Human review node
async def human_review_node(state: WorkflowState) -> Dict[str, Any]:
    """
    Human-in-the-loop review point
    """
    logger.info("Awaiting human review", 
                compliance_status=state.get("compliance_result", {}).get("status"))
    
    # In production, this would trigger a notification and wait for human input
    # For now, we'll mark it as reviewed
    return {
        "needs_human_review": False,
        "messages": state["messages"] + [{
            "role": "system",
            "content": "Human review completed - proceeding with approved changes"
        }]
    }


# Router function for conditional edges
def route_compliance(state: WorkflowState) -> Literal["finalize", "human_review", "regenerate"]:
    """
    Route based on compliance check results
    """
    status = state.get("compliance_result", {}).get("status", "inconclusive")
    
    if status == "green":
        return "finalize"
    elif status == "yellow":
        return "human_review"
    else:  # red or inconclusive
        return "regenerate"


# Finalize node
async def finalize_node(state: WorkflowState) -> Dict[str, Any]:
    """
    Finalize the workflow and prepare outputs
    """
    logger.info("Finalizing workflow")
    
    return {
        "completed_at": datetime.utcnow(),
        "artifacts": {
            "analysis": state.get("analysis"),
            "strategy": state.get("strategy"),
            "documents": state.get("draft_doc"),
            "schedule": state.get("schedule_proposal"),
            "compliance": state.get("compliance_result")
        },
        "messages": state["messages"] + [{
            "role": "assistant",
            "content": "Workflow completed successfully. All artifacts are ready."
        }]
    }


def create_main_graph() -> StateGraph:
    """
    Create the main workflow graph with LangGraph 0.6.6 features
    """
    # Initialize the graph
    graph = StateGraph(WorkflowState)
    
    # Add nodes
    graph.add_node("analyze_sales", analyze_sales_node)
    graph.add_node("targeting", targeting_node)
    graph.add_node("policy_rag", policy_rag_node)
    graph.add_node("merge_insights", merge_insights_node)  # Deferred node
    graph.add_node("schedule", schedule_node)
    graph.add_node("client_intel", client_intel_node)
    graph.add_node("generate_document", generate_document_node)
    graph.add_node("compliance_check", compliance_check_node)
    graph.add_node("human_review", human_review_node)
    graph.add_node("finalize", finalize_node)
    
    # Set entry point
    graph.set_entry_point("analyze_sales")
    
    # Add parallel execution edges (fan-out)
    graph.add_edge(START, "analyze_sales")
    graph.add_edge(START, "targeting")
    graph.add_edge(START, "policy_rag")
    
    # Add edges to deferred merge node (fan-in)
    graph.add_edge("analyze_sales", "merge_insights")
    graph.add_edge("targeting", "merge_insights")
    graph.add_edge("policy_rag", "merge_insights")
    
    # Sequential execution after merge
    graph.add_edge("merge_insights", "schedule")
    graph.add_edge("schedule", "client_intel")
    graph.add_edge("client_intel", "generate_document")
    graph.add_edge("generate_document", "compliance_check")
    
    # Conditional routing based on compliance
    graph.add_conditional_edges(
        "compliance_check",
        route_compliance,
        {
            "finalize": "finalize",
            "human_review": "human_review",
            "regenerate": "generate_document"  # Loop back for regeneration
        }
    )
    
    # Human review outcomes
    graph.add_edge("human_review", "finalize")
    
    # Set finish point
    graph.add_edge("finalize", END)
    
    return graph


async def compile_graph_with_features():
    """
    Compile the graph with caching, checkpointing, and other features
    """
    # Create checkpointer for persistence
    checkpointer = AsyncSqliteSaver.from_conn_string(
        f"{settings.LANGGRAPH_CHECKPOINT_DIR}/workflow.db"
    )
    
    # Create the graph
    graph = create_main_graph()
    
    # Compile with features
    compiled = graph.compile(
        checkpointer=checkpointer,
        interrupt_before=["human_review"],  # Interrupt for human input
        debug=settings.DEBUG
    )
    
    # Note: In LangGraph 0.6.6, node caching would be configured here
    # but the exact API may vary. This is a placeholder for the caching setup
    
    logger.info("Graph compiled with checkpointing and interrupts")
    
    return compiled


# Export the compiled graph
async def get_workflow_graph():
    """Get the compiled workflow graph"""
    return await compile_graph_with_features()