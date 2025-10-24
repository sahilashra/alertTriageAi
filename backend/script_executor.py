"""
Script execution engine with safety validation
Simulates RMM API execution for demo purposes
"""

import subprocess
import os
import time
import re
from typing import Dict, List


class ScriptSafetyValidator:
    """Validates PowerShell scripts for dangerous patterns"""

    DANGEROUS_PATTERNS = [
        r"rm\s+-rf\s+/",
        r"del\s+/[fF]\s+/[sS]\s+/[qQ]\s+C:\\\\_drive",
        r"DROP\s+DATABASE",
        r"shutdown\s+/[sS]",
        r"format\s+[cC]:",
        r"reg\s+delete.*HKLM",
        r"chmod\s+777\s+/",
        r"> /dev/sda",
        r":(){ :|:& };:",  # Fork bomb
        r"Remove-Item.*-Recurse.*C:\\\\Windows",
    ]

    REQUIRED_SAFETY_PATTERNS = [
        r"Test-Path",  # Path validation
        r"try.*catch",  # Error handling
    ]

    def validate(self, script: str, language: str = "powershell") -> Dict:
        """
        Validate script safety
        Returns: {is_safe: bool, issues: List[str], safety_score: int}
        """
        issues = []

        # Check for dangerous patterns
        for pattern in self.DANGEROUS_PATTERNS:
            if re.search(pattern, script, re.IGNORECASE):
                issues.append(
                    f"CRITICAL: Dangerous command pattern detected: {pattern}"
                )

        # Check for safety measures
        safety_score = 0
        for pattern in self.REQUIRED_SAFETY_PATTERNS:
            if re.search(pattern, script, re.IGNORECASE):
                safety_score += 1

        # Additional checks
        if "backup" not in script.lower() and "Backup" not in script:
            issues.append("WARNING: No backup step detected")

        return {
            "is_safe": len(issues) == 0 or all("WARNING" in issue for issue in issues),
            "issues": issues,
            "safety_score": safety_score,
            "recommendation": (
                "APPROVED"
                if len([i for i in issues if "CRITICAL" in i]) == 0
                else "REJECTED"
            ),
        }


class ScriptExecutor:
    """
    Executes remediation scripts
    For demo: simulates execution with realistic output
    For production: would integrate with RMM APIs
    """

    def __init__(self):
        self.validator = ScriptSafetyValidator()
        self.demo_mode = True  # Set to False for real execution

    def execute_script(
        self, script_content: str, script_language: str = "powershell"
    ) -> Dict:
        """
        Execute remediation script
        Returns: {status, output, exit_code, execution_time}
        """
        start_time = time.time()

        # Validate safety first
        validation = self.validator.validate(script_content, script_language)
        if not validation["is_safe"]:
            return {
                "status": "rejected",
                "output": "Script failed safety validation:\\n"
                + "\\n".join(validation["issues"]),
                "exit_code": 1,
                "execution_time": 0,
            }

        # For demo: simulate execution
        if self.demo_mode:
            if script_language == "powershell":
                result = self._simulate_powershell_execution(script_content)
            else:
                result = self._simulate_bash_execution(script_content)
        else:
            # Real execution (use with caution!)
            result = self._real_execution(script_content, script_language)

        execution_time = time.time() - start_time
        result["execution_time"] = round(execution_time, 2)

        return result

    def _simulate_powershell_execution(self, script: str) -> Dict:
        """Simulate PowerShell execution for demo"""
        # Realistic output based on disk cleanup script
        output = """Starting disk cleanup on C:\
Target: IIS logs older than 30 days
Found 247 files totaling 12.3 GB
Created backup directory: D:\\Backups\\IISLogs
Creating backup...
Deleting old logs...
Cleanup complete. Space freed: 12.3 GB
Current disk usage: 42%
SUCCESS: Disk usage now within acceptable range"""

        return {"status": "success", "output": output, "exit_code": 0}

    def _simulate_bash_execution(self, script: str) -> Dict:
        """Simulate Bash execution for demo"""
        output = """Checking disk usage...
Cleaning /tmp directory
Removed 5.2 GB of temporary files
Disk usage: 38%
Cleanup complete"""

        return {"status": "success", "output": output, "exit_code": 0}

    def _real_execution(self, script: str, language: str) -> Dict:
        """
        Real script execution (disabled in demo)
        WARNING: Only use in controlled environments
        """
        try:
            if language == "powershell":
                # Write script to temp file
                script_path = "temp_script.ps1"
                with open(script_path, "w") as f:
                    f.write(script)

                # Execute PowerShell script
                result = subprocess.run(
                    ["powershell", "-ExecutionPolicy", "Bypass", "-File", script_path],
                    capture_output=True,
                    text=True,
                    timeout=300,  # 5 minute timeout
                )

                # Clean up
                os.remove(script_path)

                return {
                    "status": "success" if result.returncode == 0 else "failed",
                    "output": result.stdout + result.stderr,
                    "exit_code": result.returncode,
                }
            else:
                return {
                    "status": "failed",
                    "output": f"Language {language} not supported for real execution",
                    "exit_code": 1,
                }
        except subprocess.TimeoutExpired:
            return {
                "status": "failed",
                "output": "Script execution timed out after 5 minutes",
                "exit_code": 1,
            }
        except Exception as e:
            return {
                "status": "failed",
                "output": f"Execution error: {str(e)}",
                "exit_code": 1,
            }
