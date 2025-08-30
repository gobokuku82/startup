"""
LangGraph Node Caching Policies
"""
import hashlib
import json
from typing import Any, Dict, Optional
from datetime import timedelta
from backend.app.core.config import settings


class CachePolicy:
    """Base cache policy for LangGraph nodes"""
    
    def __init__(
        self,
        ttl: Optional[int] = None,
        key_func: Optional[callable] = None,
        enabled: bool = True
    ):
        self.ttl = ttl or settings.LANGGRAPH_CACHE_TTL
        self.key_func = key_func or self.default_key_func
        self.enabled = enabled
    
    @staticmethod
    def default_key_func(state: Dict[str, Any]) -> str:
        """Default cache key generation"""
        # Create a stable hash from relevant state fields
        cache_data = {
            "user_id": state.get("user_id"),
            "product_codes": sorted(state.get("product_codes", [])),
            "client_ids": sorted(state.get("client_ids", [])),
            "period": state.get("period"),
            "query": state.get("query")
        }
        
        # Convert to JSON and hash
        cache_str = json.dumps(cache_data, sort_keys=True)
        return hashlib.md5(cache_str.encode()).hexdigest()
    
    def should_cache(self, state: Dict[str, Any]) -> bool:
        """Determine if this state should be cached"""
        if not self.enabled:
            return False
        
        # Don't cache if there are errors
        if state.get("errors"):
            return False
        
        # Don't cache if human review is needed
        if state.get("needs_human_review"):
            return False
        
        return True


class AnalyticsCachePolicy(CachePolicy):
    """Cache policy for analytics nodes"""
    
    def __init__(self):
        super().__init__(
            ttl=3600,  # 1 hour
            enabled=True
        )
    
    def default_key_func(self, state: Dict[str, Any]) -> str:
        """Analytics-specific cache key"""
        cache_data = {
            "user_id": state.get("user_id"),
            "product_codes": sorted(state.get("product_codes", [])),
            "period": state.get("period"),
            "aggregation": state.get("context", {}).get("aggregation", "monthly")
        }
        cache_str = json.dumps(cache_data, sort_keys=True)
        return f"analytics_{hashlib.md5(cache_str.encode()).hexdigest()}"


class PolicyRAGCachePolicy(CachePolicy):
    """Cache policy for policy RAG nodes"""
    
    def __init__(self):
        super().__init__(
            ttl=7200,  # 2 hours - policies don't change often
            enabled=True
        )
    
    def default_key_func(self, state: Dict[str, Any]) -> str:
        """Policy RAG cache key"""
        cache_data = {
            "product_codes": sorted(state.get("product_codes", [])),
            "query_type": state.get("context", {}).get("compliance_type", "general"),
            "policy_version": state.get("context", {}).get("policy_version", "latest")
        }
        cache_str = json.dumps(cache_data, sort_keys=True)
        return f"policy_{hashlib.md5(cache_str.encode()).hexdigest()}"


class TargetingCachePolicy(CachePolicy):
    """Cache policy for targeting nodes"""
    
    def __init__(self):
        super().__init__(
            ttl=1800,  # 30 minutes
            enabled=True
        )
    
    def default_key_func(self, state: Dict[str, Any]) -> str:
        """Targeting cache key"""
        cache_data = {
            "user_id": state.get("user_id"),
            "analysis": state.get("analysis", {}).get("kpi_summary", {}),
            "strategy_type": state.get("context", {}).get("strategy_type", "standard")
        }
        cache_str = json.dumps(cache_data, sort_keys=True)
        return f"targeting_{hashlib.md5(cache_str.encode()).hexdigest()}"


class DocumentGenerationCachePolicy(CachePolicy):
    """Cache policy for document generation - usually not cached"""
    
    def __init__(self):
        super().__init__(
            ttl=300,  # 5 minutes - very short
            enabled=False  # Disabled by default for documents
        )
    
    def should_cache(self, state: Dict[str, Any]) -> bool:
        """Documents are rarely cached unless it's a template preview"""
        if not self.enabled:
            return False
        
        # Only cache template previews
        if state.get("context", {}).get("is_preview"):
            return True
        
        return False


# Node-specific cache policies
NODE_CACHE_POLICIES = {
    "analyze_sales": AnalyticsCachePolicy(),
    "calculate_kpi": AnalyticsCachePolicy(),
    "policy_rag": PolicyRAGCachePolicy(),
    "targeting": TargetingCachePolicy(),
    "generate_document": DocumentGenerationCachePolicy(),
    "client_intel": CachePolicy(ttl=1800),  # 30 minutes
    "schedule_proposal": CachePolicy(ttl=600),  # 10 minutes
}


def get_cache_policy(node_name: str) -> Optional[CachePolicy]:
    """Get cache policy for a specific node"""
    return NODE_CACHE_POLICIES.get(node_name)


def create_redis_cache_key(node_name: str, cache_key: str) -> str:
    """Create a Redis-compatible cache key"""
    return f"langgraph:cache:{node_name}:{cache_key}"