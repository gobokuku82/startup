"""
SQLAlchemy Database Models
"""
from datetime import datetime
from typing import Optional
from sqlalchemy import (
    Column, Integer, String, Float, Boolean, DateTime, Date, Text,
    ForeignKey, Index, JSON, DECIMAL
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(255), unique=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    role = Column(String(50), nullable=False)  # admin, manager, rep
    department = Column(String(100))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    clients = relationship("Client", back_populates="owner")
    sales = relationship("Sales", back_populates="rep")
    visits = relationship("Visit", back_populates="user")
    events = relationship("Event", back_populates="user")
    documents = relationship("Document", back_populates="user")
    reports = relationship("Report", back_populates="user")


class Client(Base):
    __tablename__ = "clients"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    type = Column(String(50))  # hospital, clinic, pharmacy
    address = Column(Text)
    owner_user_id = Column(Integer, ForeignKey("users.id"))
    tier = Column(String(20))  # platinum, gold, silver
    phone = Column(String(50))
    email = Column(String(255))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    owner = relationship("User", back_populates="clients")
    sales = relationship("Sales", back_populates="client")
    visits = relationship("Visit", back_populates="client")
    events = relationship("Event", back_populates="client")
    documents = relationship("Document", back_populates="client")
    
    # Indexes
    __table_args__ = (
        Index("idx_clients_owner", "owner_user_id"),
        Index("idx_clients_tier", "tier"),
    )


class Product(Base):
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    code = Column(String(50), unique=True, nullable=False)
    name = Column(String(255), nullable=False)
    category = Column(String(100))
    unit_price = Column(DECIMAL(10, 2))
    description = Column(Text)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    sales = relationship("Sales", back_populates="product")


class Sales(Base):
    __tablename__ = "sales"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    rep_user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    yyyymm = Column(String(6), nullable=False)  # 202501
    quantity = Column(Integer, nullable=False)
    revenue = Column(DECIMAL(12, 2), nullable=False)
    target = Column(DECIMAL(12, 2))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    client = relationship("Client", back_populates="sales")
    product = relationship("Product", back_populates="sales")
    rep = relationship("User", back_populates="sales")
    
    # Indexes
    __table_args__ = (
        Index("idx_sales_period", "yyyymm"),
        Index("idx_sales_rep", "rep_user_id"),
        Index("idx_sales_client", "client_id"),
        Index("idx_sales_product", "product_id"),
    )


class Visit(Base):
    __tablename__ = "visits"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    visit_date = Column(Date, nullable=False)
    purpose = Column(String(255))
    notes = Column(Text)
    next_action = Column(Text)
    status = Column(String(50))  # scheduled, completed, cancelled
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    client = relationship("Client", back_populates="visits")
    user = relationship("User", back_populates="visits")
    
    # Indexes
    __table_args__ = (
        Index("idx_visits_date", "visit_date"),
        Index("idx_visits_user", "user_id"),
    )


class Event(Base):
    __tablename__ = "events"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    client_id = Column(Integer, ForeignKey("clients.id"))
    title = Column(String(255), nullable=False)
    starts_at = Column(DateTime, nullable=False)
    ends_at = Column(DateTime, nullable=False)
    location = Column(String(255))
    description = Column(Text)
    source = Column(String(50))  # internal, google, outlook
    external_id = Column(String(255))
    status = Column(String(50))  # confirmed, tentative, cancelled
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="events")
    client = relationship("Client", back_populates="events")
    
    # Indexes
    __table_args__ = (
        Index("idx_events_user_date", "user_id", "starts_at"),
        Index("idx_events_client", "client_id"),
    )


class Document(Base):
    __tablename__ = "documents"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    doc_type = Column(String(50), nullable=False)  # visit_report, proposal, application
    client_id = Column(Integer, ForeignKey("clients.id"))
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    status = Column(String(50), nullable=False)  # draft, reviewing, approved, archived
    current_version = Column(Integer, default=1)
    storage_uri = Column(Text)
    doc_metadata = Column(JSON)  # Additional document metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    client = relationship("Client", back_populates="documents")
    user = relationship("User", back_populates="documents")
    versions = relationship("DocumentVersion", back_populates="document")
    compliance_checks = relationship("ComplianceCheck", back_populates="document")


class DocumentVersion(Base):
    __tablename__ = "document_versions"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    document_id = Column(Integer, ForeignKey("documents.id"), nullable=False)
    version = Column(Integer, nullable=False)
    storage_uri = Column(Text, nullable=False)
    hash = Column(String(64))
    change_summary = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    document = relationship("Document", back_populates="versions")
    
    # Constraints
    __table_args__ = (
        Index("idx_doc_version", "document_id", "version", unique=True),
    )


class ComplianceCheck(Base):
    __tablename__ = "compliance_checks"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    document_id = Column(Integer, ForeignKey("documents.id"), nullable=False)
    version = Column(Integer, nullable=False)
    status = Column(String(20), nullable=False)  # green, yellow, red, inconclusive
    findings_json = Column(JSON)  # Array of violations
    citations_json = Column(JSON)  # Array of policy references
    suggestions_json = Column(JSON)  # Array of improvement suggestions
    checked_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    document = relationship("Document", back_populates="compliance_checks")
    
    # Indexes
    __table_args__ = (
        Index("idx_compliance_doc", "document_id", "version"),
        Index("idx_compliance_status", "status"),
    )


class Report(Base):
    __tablename__ = "reports"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    report_date = Column(Date, nullable=False)
    report_type = Column(String(50))  # daily, weekly, monthly
    storage_uri = Column(Text, nullable=False)
    summary = Column(Text)
    tags = Column(JSON)  # Array of tags
    metrics = Column(JSON)  # KPI metrics snapshot
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="reports")
    
    # Indexes
    __table_args__ = (
        Index("idx_reports_user_date", "user_id", "report_date"),
    )


class AuditLog(Base):
    __tablename__ = "audit_logs"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, nullable=False)
    action = Column(String(100), nullable=False)
    resource_type = Column(String(50))
    resource_id = Column(Integer)
    ip_address = Column(String(45))
    user_agent = Column(Text)
    request_body = Column(JSON)
    response_status = Column(Integer)
    details = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Indexes
    __table_args__ = (
        Index("idx_audit_user", "user_id"),
        Index("idx_audit_action", "action"),
        Index("idx_audit_created", "created_at"),
    )