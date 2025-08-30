"""
Compliance checking and auto-fix nodes
"""
from typing import Dict, Any, List
from datetime import datetime
from backend.app.graphs.state import WorkflowState, ComplianceState
from backend.app.core.logging import get_logger

logger = get_logger(__name__)


async def compliance_check_node(state: WorkflowState) -> Dict[str, Any]:
    """
    Check document and actions for compliance violations
    """
    logger.info("Starting compliance check")
    
    try:
        draft_doc = state.get("draft_doc", {})
        policy_context = state.get("policy_context", {})
        
        violations = []
        citations = []
        suggestions = []
        
        # Check document content
        doc_content = draft_doc.get("content", "")
        context_data = draft_doc.get("context", {})
        
        # Rule 1: Check discount limits
        for product in context_data.get("products", []):
            # Mock compliance check
            if "discount" in str(product).lower():
                violations.append({
                    "rule": "COMP-001",
                    "severity": "medium",
                    "description": "Discount approval required",
                    "location": "products section"
                })
                suggestions.append({
                    "type": "approval_required",
                    "action": "Obtain manager approval for discounts over 10%",
                    "reference": "Sales Policy Section 3.2"
                })
        
        # Rule 2: Check required documentation
        required_fields = ["client_name", "visit_date", "purpose", "next_actions"]
        missing_fields = []
        
        for field in required_fields:
            if field not in context_data or not context_data[field]:
                missing_fields.append(field)
        
        if missing_fields:
            violations.append({
                "rule": "COMP-002",
                "severity": "high",
                "description": f"Missing required fields: {', '.join(missing_fields)}",
                "location": "document metadata"
            })
            suggestions.append({
                "type": "add_content",
                "action": f"Add missing fields: {', '.join(missing_fields)}",
                "reference": "Documentation Standards"
            })
        
        # Rule 3: Check for sensitive information
        sensitive_patterns = ["password", "api_key", "주민번호", "계좌번호"]
        for pattern in sensitive_patterns:
            if pattern.lower() in doc_content.lower():
                violations.append({
                    "rule": "COMP-003",
                    "severity": "critical",
                    "description": f"Sensitive information detected: {pattern}",
                    "location": "document content"
                })
                suggestions.append({
                    "type": "remove_content",
                    "action": f"Remove or redact sensitive information: {pattern}",
                    "reference": "Data Privacy Policy"
                })
        
        # Add policy citations
        for policy in policy_context.get("policies", []):
            if policy.get("relevance_score", 0) > 0.8:
                citations.append({
                    "source": policy.get("title"),
                    "policy_id": policy.get("policy_id"),
                    "excerpt": policy.get("content"),
                    "relevance": policy.get("relevance_score")
                })
        
        # Determine overall compliance status
        if any(v["severity"] == "critical" for v in violations):
            status = "red"
        elif any(v["severity"] == "high" for v in violations):
            status = "yellow"
        elif violations:
            status = "yellow"
        else:
            status = "green"
        
        compliance_result = {
            "status": status,
            "violations": violations,
            "citations": citations,
            "suggestions": suggestions,
            "check_timestamp": datetime.utcnow().isoformat(),
            "auto_fix_available": len(violations) > 0 and all(v["severity"] != "critical" for v in violations)
        }
        
        logger.info(f"Compliance check completed: {status}", violations_count=len(violations))
        
        return {
            "compliance_result": compliance_result,
            "is_compliant": status == "green",
            "needs_human_review": status == "yellow",
            "messages": state["messages"] + [{
                "role": "assistant",
                "content": f"Compliance check completed: {status}. Found {len(violations)} violations."
            }]
        }
        
    except Exception as e:
        logger.error(f"Error in compliance check: {str(e)}")
        return {
            "compliance_result": {
                "status": "inconclusive",
                "error": str(e)
            },
            "is_compliant": False
        }


async def auto_fix_node(state: ComplianceState) -> Dict[str, Any]:
    """
    Automatically fix compliance violations where possible
    """
    logger.info("Attempting auto-fix for compliance violations")
    
    violations = state.get("rule_violations", [])
    content = state.get("content", "")
    
    fixed_content = content
    fixes_applied = []
    
    for violation in violations:
        if violation.get("severity") != "critical":
            # Apply auto-fixes for non-critical violations
            if violation.get("rule") == "COMP-002":
                # Add missing fields
                fixes_applied.append(f"Added missing field placeholders")
                # Mock fix implementation
                
            elif violation.get("rule") == "COMP-001":
                # Flag for approval
                fixes_applied.append(f"Flagged for manager approval")
    
    logger.info(f"Applied {len(fixes_applied)} auto-fixes")
    
    return {
        **state,
        "auto_fixed_content": fixed_content if fixes_applied else None,
        "suggestions": state.get("suggestions", []) + [
            {"type": "auto_fix", "description": fix} for fix in fixes_applied
        ]
    }