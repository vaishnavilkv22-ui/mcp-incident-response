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

if __name__ == "__main__":
    mcp.run()