'''
FastAPI main application
API endpoints for alert triage and remediation
'''
from fastapi import FastAPI, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from backend.models import Alert, RemediationPlan, ExecutionResult, HealthCheck
from backend.aws_bedrock_service import BedrockService
from backend.script_executor import ScriptExecutor
from dotenv import load_dotenv
import os
from datetime import datetime

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="Agentic Alert Triage API",
    description="AI-powered alert analysis and remediation",
    version="1.0.0"
)

# CORS middleware for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production: specify frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
try:
    bedrock_service = BedrockService()
    ai_service_configured = True
    print("[OK] AWS Bedrock service initialized successfully")
except Exception as e:
    print(f"WARNING: Bedrock service initialization failed: {e}")
    ai_service_configured = False

script_executor = ScriptExecutor()

# In-memory storage (replace with database in production)
alerts_db = []
plans_db = {}
executions_db = {}

# Auto-load demo alert on startup
import json
try:
    with open("data/alerts.json", "r") as f:
        demo_alert = json.load(f)
        alerts_db.append(demo_alert)
        print(f"[OK] Auto-loaded demo alert: {demo_alert['id']}")
except Exception as e:
    print(f"[WARN] Could not auto-load demo alert: {e}")

@app.get("/api/health", response_model=HealthCheck)
def health_check():
    '''API health check'''
    return {
        "status": "healthy",
        "service": "Alert Triage AI (AWS Bedrock)",
        "version": "1.0.0",
        "bedrock_configured": ai_service_configured
    }

@app.get("/")
async def serve_frontend():
    '''Serve the frontend HTML'''
    frontend_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend", "index.html")
    if os.path.exists(frontend_path):
        return FileResponse(frontend_path)
    return {"message": "Frontend not found. Visit /docs for API documentation."}

@app.post("/alerts/ingest")
async def ingest_alert(alert: Alert):
    '''
    Ingest new alert from monitoring system
    Stores alert and returns acknowledgment
    '''
    alerts_db.append(alert.dict())
    return {
        "message": "Alert received successfully",
        "alert_id": alert.id,
        "timestamp": datetime.utcnow().isoformat()
    }

@app.get("/alerts")
async def list_alerts():
    '''List all alerts'''
    return {
        "count": len(alerts_db),
        "alerts": alerts_db
    }

@app.get("/alerts/{alert_id}")
async def get_alert(alert_id: str):
    '''Get specific alert by ID'''
    alert = next((a for a in alerts_db if a["id"] == alert_id), None)
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    return alert

@app.post("/alerts/{alert_id}/analyze")
async def analyze_alert(alert_id: str):
    '''
    Analyze alert with AWS Bedrock (Amazon Nova Pro)
    Generates remediation plan with safety checks
    '''
    # Find alert
    alert_data = next((a for a in alerts_db if a["id"] == alert_id), None)
    if not alert_data:
        raise HTTPException(status_code=404, detail="Alert not found")
    
    # Convert to Alert model
    alert = Alert(**alert_data)
    
    # Check if AI service is configured
    if not ai_service_configured:
        raise HTTPException(
            status_code=503,
            detail="AWS Bedrock service not configured. Please set AWS credentials in .env file"
        )

    # Analyze with AWS Bedrock
    try:
        plan = bedrock_service.analyze_alert(alert)
        plans_db[alert_id] = plan.dict()
        
        return {
            "status": "completed",
            "alert_id": alert_id,
            "plan": plan.dict(),
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Analysis failed: {str(e)}"
        )

@app.get("/alerts/{alert_id}/plan")
async def get_remediation_plan(alert_id: str):
    '''Get remediation plan for alert'''
    if alert_id not in plans_db:
        raise HTTPException(status_code=404, detail="Remediation plan not found")
    return plans_db[alert_id]

@app.post("/alerts/{alert_id}/execute")
async def execute_remediation(
    alert_id: str,
    approved: bool = True,
    request_body: dict = Body(None)
):
    '''
    Execute approved remediation script
    Requires human approval
    Accepts plan in request body to handle multi-worker deployments
    '''
    if not approved:
        return {
            "status": "cancelled",
            "message": "Execution cancelled by technician",
            "alert_id": alert_id
        }

    # Get remediation plan from request body or memory
    plan = None
    if request_body and "plan" in request_body:
        plan = request_body["plan"]
    if not plan:
        plan = plans_db.get(alert_id)
    if not plan:
        raise HTTPException(status_code=404, detail="Remediation plan not found")
    
    # Validate script safety
    validation = script_executor.validator.validate(plan["script"], plan["script_language"])
    if validation["recommendation"] == "REJECTED":
        return {
            "status": "rejected",
            "message": "Script failed safety validation",
            "issues": validation["issues"],
            "alert_id": alert_id
        }
    
    # Execute script
    try:
        result = script_executor.execute_script(
            plan["script"],
            plan["script_language"]
        )
        
        # Calculate MTTR (mock for demo)
        mttr = 4  # 4 minutes for demo
        
        execution_result = {
            "alert_id": alert_id,
            "status": result["status"],
            "output": result["output"],
            "execution_time": result["execution_time"],
            "mttr_minutes": mttr,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        executions_db[alert_id] = execution_result
        
        return execution_result
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Execution failed: {str(e)}"
        )

@app.get("/alerts/{alert_id}/result")
async def get_execution_result(alert_id: str):
    '''Get execution result for alert'''
    if alert_id not in executions_db:
        raise HTTPException(status_code=404, detail="Execution result not found")
    return executions_db[alert_id]

@app.get("/stats")
async def get_statistics():
    '''Get system statistics'''
    total_alerts = len(alerts_db)
    analyzed = len(plans_db)
    executed = len(executions_db)
    
    return {
        "total_alerts": total_alerts,
        "analyzed": analyzed,
        "executed": executed,
        "success_rate": (executed / analyzed * 100) if analyzed > 0 else 0
    }

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
