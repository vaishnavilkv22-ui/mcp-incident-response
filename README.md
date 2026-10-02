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

Maps the assessed severity to a recommended support action.

| Severity | Recommended action |
|---|---|
| LOW | Monitor application |
| MEDIUM | Investigate incident and review application logs |
| HIGH | Escalate incident and begin detailed investigation |

### `classify_incident_type`

Classifies an incident based on keywords found in an error message.

Supported classifications include:

- AUTHENTICATION
- DATABASE
- PERFORMANCE
- APPLICATION
- UNKNOWN

More specific conditions are evaluated before broader conditions to avoid incorrect classifications.

### `build_incident_profile`

Builds a structured incident profile from investigation results.

The profile contains:

- Severity
- Customer impact
- Primary errors
- Repeated error occurrence counts
- Warnings

Repeated errors are listed first, with their occurrence count. Errors that occur only once are listed without an occurrence count.

The tool also validates that every repeated error exists in the supplied error list before building the profile.

## Cross-MCP Workflow

The Incident Response MCP can work together with the Log Analyzer MCP to support an application incident investigation.

The workflow is:

Application log  
↓  
Log Analyzer MCP  
↓  
Errors / repeated errors / warnings / timeline  
↓  
Incident Response MCP  
↓  
Incident classification  
↓  
Severity + customer impact  
↓  
Structured incident profile  
↓  
Recommended support action

For example, the Log Analyzer identified 3 ERROR entries in a simulated application log.

The repeated error analysis identified:

- Database connection timeout → 2 occurrences
- Failed to process customer request → 1 occurrence

The Incident Response MCP then:

1. Classified the incident types.
2. Assessed severity based on error count and customer impact.
3. Built a structured incident profile.
4. Determined the corresponding support action.

For the same technical evidence:

- 3 errors + no customer impact → MEDIUM → Investigate incident and review application logs
- 3 errors + customer impact → HIGH → Escalate incident and begin detailed investigation

Customer impact in these scenarios was provided as an explicit input to demonstrate how business context can change the operational response.

The workflow does not assume a root cause. Technical evidence, hypotheses, and confirmed conclusions remain separate.

## Testing & Break/Fix

The MCP was tested using direct Python calls and Claude Desktop.

### Functional tests

- 3 errors → MEDIUM
- 5 errors → HIGH
- 3 errors + no customer impact → MEDIUM
- 3 errors + customer impact → HIGH
- Database connection timeout → DATABASE
- Authentication connection failed → AUTHENTICATION
- High memory usage detected → PERFORMANCE
- Failed to process customer request → APPLICATION
- Unknown error message → UNKNOWN
- Structured incident profile generated successfully

### Negative testing

Several deliberate failures were introduced during development.

#### Invalid error count

A negative error count initially produced an incorrect severity result.

Validation was added to reject negative error counts.

#### Incorrect incident classification

The message:

`Authentication connection failed`

was initially classified as `DATABASE` because the generic `connection` condition was evaluated before the more specific authentication condition.

The classification logic was reordered so that more specific conditions are evaluated first.

The test was then repeated and correctly returned:

`AUTHENTICATION`

#### Invalid customer impact

The value:

`customer_impact = "yes"`

was initially accepted because a non-empty string is truthy in Python.

Validation was added to ensure that `customer_impact` must be a Boolean.

The test was then repeated and correctly returned a validation error.

#### Inconsistent incident data

A repeated error was deliberately supplied that did not exist in the main error list.

The initial implementation accepted the inconsistent data and included the error in the incident profile.

Validation was added to reject the profile when a repeated error is missing from the supplied error list.

The test was then repeated and correctly returned a validation error.

### Regression testing

After each fix, the original scenarios were retested successfully.

This followed a practical support-engineering workflow:

**Build → Break → Diagnose → Fix → Retest**

### Cross-MCP testing

The Log Analyzer MCP and Incident Response MCP were tested together using the actual simulated application log.

The workflow successfully:

- Retrieved the application log
- Counted errors
- Identified repeated errors
- Extracted warnings and timeline information
- Classified incident types
- Assessed severity
- Built an incident profile
- Generated a recommended support action

The workflow also demonstrated that the same technical evidence can produce different operational responses when customer impact changes.

Importantly, customer impact was explicitly supplied as test input and was not inferred from the application log.

## What This Demonstrates

This project demonstrates how custom MCP servers can expose application-support-specific capabilities to an AI assistant and combine them into an operational workflow.

Key areas demonstrated:

- Python and FastMCP
- MCP tool development
- Input validation and error handling
- Incident classification
- Severity assessment
- Customer-impact handling
- Structured incident profiles
- Tool chaining and orchestration
- Cross-MCP workflows
- Break/fix debugging
- Regression testing
- Data consistency validation
- AI-assisted incident investigation

The project also demonstrates an important principle for Application Support:

**Technical evidence and business context both matter when determining the appropriate response.**

The goal is not to replace the Application Support Engineer, but to give the engineer better access to structured operational information, reduce manual investigation effort, and assist with incident analysis and decision-making.

Root-cause conclusions are not assumed unless the available evidence supports them.
