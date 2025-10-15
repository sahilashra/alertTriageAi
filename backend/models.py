'''
Data models for Alert Triage AI
Uses Pydantic for validation and serialization
'''
from pydantic import BaseModel, Field
from typing import Optional, List, Dict
from datetime import datetime

class Alert(BaseModel):
    '''Incoming alert from monitoring system'''
    id: str = Field(..., description="Unique alert identifier")
    timestamp: str = Field(..., description="ISO 8601 timestamp")
    severity: str = Field(..., description="critical, high, medium, low")
    system: str = Field(..., description="Affected system name")
    alert_type: str = Field(..., description="Type of alert (disk_space, cpu, memory, etc)")
    description: str = Field(..., description="Human-readable alert description")
    metrics: Dict = Field(default_factory=dict, description="Alert-specific metrics")
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": "INC0012345",
                "timestamp": "2025-10-11T02:17:00Z",
                "severity": "critical",
                "system": "PROD-DB-01",
                "alert_type": "disk_space",
                "description": "Disk space critical on C:\\ drive - 95% full",
                "metrics": {
                    "disk_used_percent": 95,
                    "disk_used_gb": 456,
                    "disk_total_gb": 480,
                    "partition": "C:\\"
                }
            }
        }

class RemediationPlan(BaseModel):
    '''AI-generated remediation plan'''
    alert_id: str
    root_cause: str
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence score 0-1")
    reasoning: str
    steps: List[str]
    script: str
    script_language: str = "powershell"
    safety_checks: List[str]
    estimated_time: str
    rollback_plan: str

class ExecutionResult(BaseModel):
    '''Result of script execution'''
    alert_id: str
    status: str  # success, failed, cancelled
    output: str
    execution_time: float
    mttr_minutes: int
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat())

class HealthCheck(BaseModel):
    '''API health check response'''
    status: str
    service: str
    version: str = "1.0.0"
    gemini_configured: bool
