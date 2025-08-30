"""
Document generation nodes
"""
from typing import Dict, Any
from datetime import datetime
from backend.app.graphs.state import WorkflowState, DocumentState
from backend.app.core.logging import get_logger

logger = get_logger(__name__)


async def generate_document_node(state: WorkflowState) -> Dict[str, Any]:
    """
    Generate documents using Jinja2 templates
    """
    logger.info("Starting document generation")
    
    try:
        # Extract context for document generation
        client_intel = state.get("client_intel", {})
        analysis = state.get("analysis", {})
        strategy = state.get("strategy", {})
        schedule = state.get("schedule_proposal", [])
        
        # Determine document type based on context
        doc_type = state.get("context", {}).get("doc_type", "visit_report")
        
        # Build Jinja2 context
        jinja_context = {
            "client_name": "Seoul Medical Center",  # Would come from client_intel
            "visit_date": datetime.utcnow().strftime("%Y-%m-%d"),
            "purpose": "Quarterly business review and new product presentation",
            "key_points": [
                "Presented Q3 sales performance",
                "Introduced new product line PROD003",
                "Discussed expansion opportunities",
                "Scheduled follow-up meeting"
            ],
            "next_actions": [
                "Send product samples by next week",
                "Prepare customized pricing proposal",
                "Schedule technical training session"
            ],
            "products": [
                {"code": "PROD001", "name": "Product A", "quantity": 100},
                {"code": "PROD002", "name": "Product B", "quantity": 50}
            ],
            "sales_summary": {
                "total_revenue": analysis.get("kpi_summary", {}).get("total_revenue", 0),
                "growth_rate": 15.5,
                "achievement_rate": 92.3
            }
        }
        
        # TODO: Implement actual Jinja2 template rendering
        # Mock document generation
        
        generated_content = f"""
# Visit Report - {jinja_context['client_name']}

**Date:** {jinja_context['visit_date']}
**Purpose:** {jinja_context['purpose']}

## Key Discussion Points
{chr(10).join(f'- {point}' for point in jinja_context['key_points'])}

## Next Actions
{chr(10).join(f'- {action}' for action in jinja_context['next_actions'])}

## Sales Performance
- Total Revenue: {jinja_context['sales_summary']['total_revenue']:,} KRW
- Growth Rate: {jinja_context['sales_summary']['growth_rate']}%
- Target Achievement: {jinja_context['sales_summary']['achievement_rate']}%
"""
        
        # Create document metadata
        draft_doc = {
            "doc_id": "DOC-2025-001",
            "doc_type": doc_type,
            "content": generated_content,
            "format": "markdown",
            "storage_uri": f"/data/storage/docs/{doc_type}_2025_001.md",
            "version": 1,
            "created_at": datetime.utcnow().isoformat(),
            "context": jinja_context
        }
        
        logger.info(f"Generated {doc_type} document")
        
        return {
            "draft_doc": draft_doc,
            "messages": state["messages"] + [{
                "role": "assistant",
                "content": f"Generated {doc_type} document successfully"
            }]
        }
        
    except Exception as e:
        logger.error(f"Error generating document: {str(e)}")
        return {
            "errors": state.get("errors", []) + [{
                "node": "generate_document",
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }]
        }


async def select_template_node(state: DocumentState) -> Dict[str, Any]:
    """
    Select appropriate template based on document type
    """
    logger.info(f"Selecting template for {state.get('doc_type')}")
    
    template_map = {
        "visit_report": "templates/visit_report.jinja2",
        "proposal": "templates/proposal.jinja2",
        "application": "templates/application.jinja2"
    }
    
    template_name = template_map.get(state.get("doc_type"), "templates/default.jinja2")
    
    return {
        **state,
        "template_name": template_name
    }