"""
Pre/Post Model Hooks for LangGraph
"""
from typing import List, Dict, Any, Optional
import json
from datetime import datetime
from backend.app.core.logging import get_logger

logger = get_logger(__name__)


class PreModelHook:
    """Pre-model execution hooks for context management"""
    
    @staticmethod
    async def summarize_messages(messages: List[Dict[str, Any]], max_messages: int = 10) -> List[Dict[str, Any]]:
        """
        Summarize messages if they exceed the threshold
        Helps with context window management
        """
        if len(messages) <= max_messages:
            return messages
        
        # Keep system message and first few messages
        system_msgs = [m for m in messages if m.get("role") == "system"]
        user_msgs = [m for m in messages if m.get("role") == "user"]
        assistant_msgs = [m for m in messages if m.get("role") == "assistant"]
        
        # Create summary of middle messages
        middle_msgs = messages[3:-3]
        if middle_msgs:
            summary = {
                "role": "system",
                "content": f"[Summary of {len(middle_msgs)} previous messages omitted for brevity]"
            }
            
            # Reconstruct message list
            result = system_msgs[:1]  # Keep system message
            result.extend(user_msgs[:2])  # Keep first 2 user messages
            result.append(summary)  # Add summary
            result.extend(messages[-3:])  # Keep last 3 messages
            
            logger.info(f"Summarized {len(messages)} messages to {len(result)}")
            return result
        
        return messages
    
    @staticmethod
    async def inject_context(messages: List[Dict[str, Any]], context: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Inject additional context into messages
        """
        if not context:
            return messages
        
        # Create context message
        context_msg = {
            "role": "system",
            "content": f"Current context: {json.dumps(context, ensure_ascii=False)}"
        }
        
        # Insert after first system message
        result = messages[:1]
        result.append(context_msg)
        result.extend(messages[1:])
        
        return result
    
    @staticmethod
    async def filter_sensitive_data(messages: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Remove sensitive information from messages
        """
        sensitive_patterns = [
            "password", "pwd", "secret", "token", "api_key",
            "주민등록번호", "계좌번호", "카드번호"
        ]
        
        filtered = []
        for msg in messages:
            content = msg.get("content", "")
            
            # Check for sensitive patterns
            for pattern in sensitive_patterns:
                if pattern.lower() in content.lower():
                    logger.warning(f"Sensitive data detected and filtered: {pattern}")
                    content = content.replace(pattern, "[REDACTED]")
            
            filtered.append({**msg, "content": content})
        
        return filtered


class PostModelHook:
    """Post-model execution hooks for validation and guardrails"""
    
    @staticmethod
    async def compliance_check(response: Dict[str, Any], rules: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Check response for compliance violations
        """
        if not rules:
            rules = [
                "no_financial_advice",
                "no_medical_diagnosis",
                "no_legal_counsel",
                "respect_data_privacy"
            ]
        
        violations = []
        content = response.get("content", "")
        
        # Simple rule checks (can be enhanced with ML models)
        rule_patterns = {
            "no_financial_advice": ["투자 추천", "매수", "매도", "수익 보장"],
            "no_medical_diagnosis": ["진단", "처방", "치료법", "의학적 조언"],
            "no_legal_counsel": ["법적 조언", "소송", "계약서 작성"],
            "respect_data_privacy": ["개인정보", "주민번호", "신용카드"]
        }
        
        for rule, patterns in rule_patterns.items():
            if rule in rules:
                for pattern in patterns:
                    if pattern in content:
                        violations.append({
                            "rule": rule,
                            "pattern": pattern,
                            "severity": "high"
                        })
        
        if violations:
            logger.warning(f"Compliance violations detected: {violations}")
            return {
                "needs_review": True,
                "violations": violations,
                "original_response": response,
                "status": "blocked"
            }
        
        return response
    
    @staticmethod
    async def add_metadata(response: Dict[str, Any], metadata: Dict[str, Any]) -> Dict[str, Any]:
        """
        Add metadata to response
        """
        return {
            **response,
            "metadata": {
                **metadata,
                "processed_at": datetime.utcnow().isoformat(),
                "hook_applied": "post_model"
            }
        }
    
    @staticmethod
    async def human_review_gate(response: Dict[str, Any], criteria: Dict[str, Any]) -> Dict[str, Any]:
        """
        Determine if human review is needed
        """
        needs_review = False
        review_reasons = []
        
        # Check confidence score
        confidence = response.get("confidence", 1.0)
        if confidence < criteria.get("min_confidence", 0.7):
            needs_review = True
            review_reasons.append(f"Low confidence: {confidence}")
        
        # Check for specific keywords that require review
        review_keywords = criteria.get("review_keywords", ["urgent", "critical", "법적", "소송"])
        content = response.get("content", "")
        
        for keyword in review_keywords:
            if keyword in content:
                needs_review = True
                review_reasons.append(f"Keyword detected: {keyword}")
        
        # Check amount thresholds
        if "amount" in response:
            amount = response.get("amount", 0)
            threshold = criteria.get("amount_threshold", 10000000)  # 10M KRW
            if amount > threshold:
                needs_review = True
                review_reasons.append(f"Amount exceeds threshold: {amount:,}")
        
        if needs_review:
            logger.info(f"Human review required: {review_reasons}")
            return {
                **response,
                "needs_human_review": True,
                "review_reasons": review_reasons,
                "status": "pending_review"
            }
        
        return response
    
    @staticmethod
    async def format_response(response: Dict[str, Any], format_spec: Dict[str, Any]) -> Dict[str, Any]:
        """
        Format response according to specification
        """
        if format_spec.get("type") == "structured":
            # Ensure response has required fields
            required_fields = format_spec.get("required_fields", [])
            for field in required_fields:
                if field not in response:
                    response[field] = None
                    logger.warning(f"Missing required field: {field}")
        
        if format_spec.get("type") == "markdown":
            # Convert to markdown if needed
            content = response.get("content", "")
            if not content.startswith("#"):
                response["content"] = f"## Response\n\n{content}"
        
        return response


# Hook compositions for different node types
NODE_HOOKS = {
    "analyze_sales": {
        "pre": [PreModelHook.inject_context],
        "post": [PostModelHook.add_metadata]
    },
    "generate_document": {
        "pre": [PreModelHook.filter_sensitive_data],
        "post": [PostModelHook.compliance_check, PostModelHook.format_response]
    },
    "compliance_check": {
        "pre": [PreModelHook.inject_context],
        "post": [PostModelHook.human_review_gate]
    },
    "chat": {
        "pre": [PreModelHook.summarize_messages, PreModelHook.filter_sensitive_data],
        "post": [PostModelHook.compliance_check, PostModelHook.add_metadata]
    }
}


async def apply_pre_hooks(node_name: str, messages: List[Dict[str, Any]], state: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Apply pre-model hooks for a specific node"""
    hooks = NODE_HOOKS.get(node_name, {}).get("pre", [])
    
    result = messages
    for hook in hooks:
        if hook == PreModelHook.inject_context:
            result = await hook(result, state.get("context", {}))
        else:
            result = await hook(result)
    
    return result


async def apply_post_hooks(node_name: str, response: Dict[str, Any], state: Dict[str, Any]) -> Dict[str, Any]:
    """Apply post-model hooks for a specific node"""
    hooks = NODE_HOOKS.get(node_name, {}).get("post", [])
    
    result = response
    for hook in hooks:
        if hook == PostModelHook.human_review_gate:
            criteria = state.get("context", {}).get("review_criteria", {})
            result = await hook(result, criteria)
        elif hook == PostModelHook.format_response:
            format_spec = state.get("context", {}).get("format_spec", {"type": "structured"})
            result = await hook(result, format_spec)
        elif hook == PostModelHook.add_metadata:
            metadata = {"node": node_name, "session_id": state.get("session_id")}
            result = await hook(result, metadata)
        else:
            result = await hook(result)
    
    return result