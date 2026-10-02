from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Incident Response")

@mcp.tool()
def assess_incident_severity(error_count: int):
    """Assess incident severity based on the number of errors."""
    if error_count < 0:
        return {
            "error": "Error count cannot be negative."
        }
    if error_count == 0:
        severity = "LOW"
    elif error_count <= 3:
        severity = "MEDIUM"
    else:
        severity = "HIGH"

    return {
        "error_count": error_count,
        "severity": severity
    }

@mcp.tool()
def recommend_support_action(severity: str):
    """Recommend a support action based on incident severity."""

    severity = severity.upper()

    if severity == "LOW":
        action = "Monitor application"
    elif severity == "MEDIUM":
        action = "Investigate incident and review application logs"
    elif severity == "HIGH":
        action = "Escalate incident and begin detailed investigation"
    else:
        return {
            "error": "Invalid severity. Use LOW, MEDIUM, or HIGH."
        }

    return {
        "severity": severity,
        "recommended_action": action
    }

@mcp.tool()
def assess_incident_with_impact(error_count: int, customer_impact: bool):
    """Assess incident severity using error count and customer impact."""

    if error_count < 0:
        return {
            "error": "Error count cannot be negative."
        }

    if not isinstance(customer_impact, bool):
        return {
            "error": "Customer impact must be True or False."
        }

    if customer_impact:
        severity = "HIGH"
    elif error_count == 0:
        severity = "LOW"
    elif error_count <= 3:
        severity = "MEDIUM"
    else:
        severity = "HIGH"

    return {
        "error_count": error_count,
        "customer_impact": customer_impact,
        "severity": severity
    }

@mcp.tool()
def classify_incident_type(error_message: str):
    """Classify an incident based on its error message."""

    message = error_message.lower()

    if "authentication" in message or "login" in message:
        incident_type = "AUTHENTICATION"
    elif "database" in message or "connection" in message:
        incident_type = "DATABASE"
    elif "memory" in message or "response time" in message:
        incident_type = "PERFORMANCE"
    elif "customer request" in message or "application" in message:
        incident_type = "APPLICATION"
    else:
        incident_type = "UNKNOWN"

    return {
        "error_message": error_message,
        "incident_type": incident_type
    }

@mcp.tool()
def build_incident_profile(
    severity: str,
    customer_impact: bool,
    errors: list,
    repeated_errors: dict,
    warnings: list
):
    """Build a structured incident profile from investigation results."""

    severity = severity.upper()

    if severity not in ["LOW", "MEDIUM", "HIGH"]:
        return {
            "error": "Invalid severity. Use LOW, MEDIUM, or HIGH."
        }

    if not isinstance(customer_impact, bool):
        return {
            "error": "Customer impact must be True or False."
        }

    if not isinstance(errors, list):
        return {
            "error": "Errors must be provided as a list."
        }

    if not isinstance(repeated_errors, dict):
        return {
            "error": "Repeated errors must be provided as a dictionary."
        }
    
    for error in repeated_errors:
        if error not in errors:
            return {
                "error": f"Repeated error '{error}' was not found in the error list."
            }

    if not isinstance(warnings, list):
        return {
            "error": "Warnings must be provided as a list."
        }

    primary_errors = []

    for error, count in repeated_errors.items():
        primary_errors.append({
            "error": error,
            "occurrences": count
        })

    for error in errors:
        if error not in repeated_errors:
            primary_errors.append({
                "error": error
            })

    return {
        "severity": severity,
        "impact": "CUSTOMER_IMPACT" if customer_impact else "NO_CUSTOMER_IMPACT",
        "primary_errors": primary_errors,
        "warnings": warnings
    }

if __name__ == "__main__":
    mcp.run()
