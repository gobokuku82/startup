"""
LangGraph State Definitions
"""
from typing import TypedDict, List, Dict, Any, Optional, Annotated
from datetime import datetime
from langgraph.graph import add_messages


class WorkflowState(TypedDict):
    """Main workflow state for LangGraph"""
    
    # Core context
    user_id: int
    session_id: str
    thread_id: str
    messages: Annotated[List[Dict], add_messages]
    
    # User input
    query: str
    context: Dict[str, Any]
    
    # Business data
    product_codes: List[str]
    client_ids: List[int]
    period: Dict[str, str]  # {"start": "202401", "end": "202412"}
    
    # Analysis results
    analysis: Dict[str, Any]  # KPI, sales metrics
    targeting: Dict[str, Any]  # Target clients, whitespace
    strategy: Dict[str, Any]  # Strategic recommendations
    
    # Policy and compliance
    policy_context: Dict[str, Any]  # Related policies, regulations
    compliance_result: Dict[str, Any]  # Compliance check results
    
    # Schedule and planning
    schedule_proposal: List[Dict[str, Any]]  # Proposed schedule slots
    selected_slots: List[Dict[str, Any]]  # User-selected slots
    
    # Client intelligence
    client_intel: Dict[str, Any]  # Client insights, history
    
    # Document generation
    draft_doc: Dict[str, Any]  # Generated document info
    doc_versions: List[Dict[str, Any]]  # Document version history
    
    # Control flags
    needs_human_review: bool
    is_compliant: bool
    should_retry: bool
    max_retries: int
    current_retry: int
    
    # Artifacts and outputs
    artifacts: Dict[str, Any]  # Files, reports, etc.
    errors: List[Dict[str, Any]]  # Error tracking
    metadata: Dict[str, Any]  # Additional metadata
    
    # Timestamps
    started_at: datetime
    completed_at: Optional[datetime]


class DocumentState(TypedDict):
    """State for document generation subgraph"""
    
    # Context
    user_id: int
    client_id: Optional[int]
    
    # Document specifics
    doc_type: str  # visit_report, proposal, application
    template_name: str
    
    # Content
    context_data: Dict[str, Any]
    jinja_context: Dict[str, Any]
    
    # Generated document
    content: str
    format: str  # docx, pdf, markdown
    storage_uri: Optional[str]
    
    # Versioning
    version: int
    previous_version_uri: Optional[str]
    change_summary: Optional[str]
    
    # Status
    status: str  # draft, generated, reviewed, finalized
    errors: List[str]


class ComplianceState(TypedDict):
    """State for compliance checking subgraph"""
    
    # Input
    document_id: Optional[int]
    content: str
    check_type: str  # pre_submit, final, periodic
    
    # Analysis
    rule_violations: List[Dict[str, Any]]
    policy_citations: List[Dict[str, Any]]
    
    # Results
    status: str  # green, yellow, red, inconclusive
    severity: str  # low, medium, high, critical
    
    # Suggestions
    suggestions: List[Dict[str, Any]]
    auto_fix_available: bool
    auto_fixed_content: Optional[str]
    
    # Metadata
    checked_rules: List[str]
    skipped_rules: List[str]
    check_duration_ms: int


class AnalyticsState(TypedDict):
    """State for analytics and KPI calculation"""
    
    # Parameters
    user_id: int
    product_codes: List[str]
    client_ids: List[int]
    period: Dict[str, str]
    
    # Metrics
    kpi_summary: Dict[str, Any]
    sales_by_client: List[Dict[str, Any]]
    sales_by_product: List[Dict[str, Any]]
    
    # Analysis
    yoy_growth: float
    ytd_achievement: float
    target_achievement_rate: float
    
    # Trends
    trend_analysis: Dict[str, Any]
    seasonality: Dict[str, Any]
    
    # Recommendations
    opportunities: List[Dict[str, Any]]
    risks: List[Dict[str, Any]]


class ScheduleState(TypedDict):
    """State for schedule management"""
    
    # Context
    user_id: int
    client_ids: List[int]
    
    # Time constraints
    date_range: Dict[str, str]
    duration_minutes: int
    preferred_times: List[str]
    
    # Existing schedule
    existing_events: List[Dict[str, Any]]
    conflicts: List[Dict[str, Any]]
    
    # Proposals
    proposed_slots: List[Dict[str, Any]]
    optimization_score: float
    
    # Selected
    confirmed_events: List[Dict[str, Any]]
    calendar_sync_status: Optional[str]