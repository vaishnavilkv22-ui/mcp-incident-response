# Incident Response MCP

A custom MCP server that helps an AI assistant assess application incidents and recommend support actions based on error count and customer impact.

Built with Python, FastMCP, and Claude Desktop.

## Tools

### `assess_incident_severity`

Assesses incident severity based on the number of errors.

| Error count | Severity |
|---|---|
| 0 | LOW |
| 1–3 | MEDIUM |
| 4+ | HIGH |

### `assess_incident_with_impact`

Assesses incident severity using both error count and customer impact.

Customer impact takes priority and results in HIGH severity.

### `recommend_support_action`

Maps the assessed severity to a recommended support action:

| Severity | Recommended action |
|---|---|
| LOW | Monitor application |
| MEDIUM | Investigate incident and review application logs |
| HIGH | Escalate incident and begin detailed investigation |

## Cross-MCP Workflow

The Incident Response MCP can work together with the Log Analyzer MCP to support an application incident investigation.

The workflow is:

Application log  
↓  
Log Analyzer MCP  
↓  
Error count and incident context  
↓  
Incident Response MCP  
↓  
Severity assessment  
↓  
Recommended support action

For example, the Log Analyzer identified 3 ERROR entries in a simulated application log.

The Incident Response MCP then assessed:

- 3 errors + no customer impact → MEDIUM
- 3 errors + customer impact → HIGH

The returned severity was then passed to `recommend_support_action()` to determine the corresponding support action.

## Testing & Break/Fix

The MCP was tested using direct Python calls and Claude Desktop.

### Functional tests

- 3 errors → MEDIUM
- 5 errors → HIGH
- 3 errors + no customer impact → MEDIUM
- 3 errors + customer impact → HIGH

### Negative testing

A negative test was performed using an invalid customer impact value:

`customer_impact = "yes"`

The initial implementation accepted the value because Python treats a non-empty string as truthy.

Validation was added to ensure that `customer_impact` must be a Boolean.

The test was then repeated and correctly returned a validation error.

### Regression testing

After fixing the validation issue, the original severity scenarios were retested successfully.

This followed a practical support-engineering workflow:

**Build → Break → Diagnose → Fix → Retest**

## What This Demonstrates

This project demonstrates how MCP can expose application-support-specific capabilities to an AI assistant.

Key areas demonstrated:

- Python and FastMCP
- MCP tool development
- Input validation and error handling
- Tool chaining and orchestration
- Incident severity assessment
- Customer-impact awareness
- Cross-MCP workflows
- Break/fix debugging
- Regression testing
- AI-assisted operational decision support

The goal is not to replace the Application Support Engineer, but to give the engineer better access to structured operational information and assist with investigation and decision-making.
