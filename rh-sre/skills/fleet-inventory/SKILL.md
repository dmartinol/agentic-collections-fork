---
name: fleet-inventory
description: |
  Query and display Red Hat Insights managed system inventory. Use this skill for information-gathering requests about the fleet, registered systems, or inventory queries. This skill focuses on discovery and listing only - for remediation actions, transition to the remediator agent.

  **When to use this skill**:
  - "Show the managed fleet"
  - "List all systems registered in Insights"
  - "What systems are affected by CVE-X?"
  - "How many RHEL 8 systems do we have?"
  - "Show me production systems"

  **When NOT to use this skill** (use remediator agent instead):
  - "Remediate CVE-X on these systems"
  - "Create a playbook for..."
  - "Patch system Y"

  This skill orchestrates MCP tools from insights-mcp to provide comprehensive fleet visibility and system inventory management.
---

# Fleet Inventory Skill

This skill queries Red Hat Insights to retrieve and display information about managed systems, registered hosts, and fleet inventory.

## When to Use This Skill

**Use this skill directly when you need**:
- List all systems registered in Red Hat Insights
- Show systems affected by specific CVEs
- Display system details (OS version, tags, last check-in)
- Filter systems by environment, RHEL version, or tags
- Count systems matching criteria
- Verify system registration status

**Use the remediator agent when you need**:
- Remediate vulnerabilities on systems
- Generate or execute playbooks
- Perform infrastructure changes
- End-to-end CVE remediation workflows

**How they work together**: Use this skill for discovery ("What systems are affected?"), then transition to the remediator agent for action ("Remediate those systems").

## Workflow

### 1. Retrieve System Inventory

**MCP Tool**: `get_host_details` (from insights-mcp)

Query Insights for system information:

```
Input: Optional filters (system_id, hostname pattern, tags)
Tool: get_host_details()

Expected Response:
{
  "systems": [
    {
      "id": "abc-def-123",
      "display_name": "web-server-01.example.com",
      "fqdn": "web-server-01.example.com",
      "rhel_version": "8.9",
      "last_seen": "2024-01-20T10:30:00Z",
      "tags": ["production", "web-tier"],
      "stale": false,
      "satellite_managed": false
    },
    ...
  ],
  "total": 42,
  "count": 10
}

Verification:
✓ Systems list returned with metadata
✓ Total count matches expectation
✓ System details include RHEL version, tags, status
```

**Key Fields to Extract**:
- `id`: Unique system identifier (use for remediation)
- `display_name` / `fqdn`: Human-readable hostname
- `rhel_version`: OS version (important for remediation planning)
- `tags`: Environment labels (production, staging, dev)
- `stale`: Whether system recently checked in
- `last_seen`: Last Insights client run

### 2. Filter and Organize Systems

Apply user-requested filters:

```
Filtering Examples:

By RHEL Version:
→ systems.filter(rhel_version.startswith("8"))
→ Result: All RHEL 8.x systems

By Environment Tag:
→ systems.filter("production" in tags)
→ Result: Production systems only

By Status:
→ systems.filter(stale == false)
→ Result: Active systems (recently checked in)

By Hostname Pattern:
→ systems.filter(fqdn.contains("web-server"))
→ Result: Web server tier systems
```

**Sorting Options**:
- By last_seen (most recent first)
- By rhel_version (group by OS)
- By display_name (alphabetical)
- By tag (environment grouping)

### 3. Query CVE-Affected Systems

**MCP Tool**: `get_cve_systems` (from insights-mcp)

Find systems affected by specific CVEs:

```
Input: CVE ID (e.g., "CVE-2024-1234")
Tool: get_cve_systems(cve_id="CVE-2024-1234")

Expected Response:
{
  "cve_id": "CVE-2024-1234",
  "affected_systems": [
    {
      "system_id": "abc-def-123",
      "display_name": "web-server-01.example.com",
      "status": "Vulnerable",
      "remediation_available": true
    },
    {
      "system_id": "xyz-123-456",
      "display_name": "db-server-02.example.com",
      "status": "Vulnerable",
      "remediation_available": true
    }
  ],
  "total_affected": 15,
  "total_remediated": 3,
  "total_vulnerable": 12
}

Verification:
✓ CVE ID matches request
✓ System list includes remediation status
✓ Counts accurate (affected, remediated, still vulnerable)
```

**Status Interpretation**:
```
Status: Vulnerable
→ CVE affects this system, patch not applied
→ Action: Suggest remediation

Status: Patched
→ CVE previously affected, now remediated
→ Action: No action needed

Status: Not Affected
→ System not vulnerable to this CVE
→ Action: Informational only
```

### 4. Generate Fleet Summary

Create organized output based on query results:

```markdown
# Fleet Inventory Summary

## Overview
**Total Systems**: 42
**Active Systems**: 38 (last seen < 24 hours)
**Stale Systems**: 4 (last seen > 7 days)

## By RHEL Version
- RHEL 9.x: 18 systems (43%)
- RHEL 8.x: 20 systems (48%)
- RHEL 7.x: 4 systems (9%)

## By Environment (Tags)
- Production: 25 systems
- Staging: 10 systems
- Development: 7 systems

## System Details

| Display Name | RHEL Version | Environment | Last Seen | Status |
|--------------|--------------|-------------|-----------|--------|
| web-server-01.example.com | 8.9 | production | 2024-01-20T10:30:00Z | Active |
| web-server-02.example.com | 8.9 | production | 2024-01-20T09:45:00Z | Active |
| db-server-01.example.com | 9.3 | production | 2024-01-20T10:15:00Z | Active |
| ... | ... | ... | ... | ... |

## Stale Systems (Attention Required)
⚠️ The following systems have not checked in recently:
- backup-server-01.example.com (last seen: 8 days ago)
- test-server-05.example.com (last seen: 12 days ago)
```

### 5. Offer Remediation Transition

When appropriate, suggest transitioning to the remediator agent:

```markdown
## Next Steps

**For CVE Remediation**:
If you need to remediate vulnerabilities on any of these systems, I can help with that using the remediator agent:

Examples:
- "Remediate CVE-2024-1234 on web-server-01"
- "Create playbook for all RHEL 8 production systems affected by CVE-2024-5678"
- "Batch remediate critical CVEs on staging environment"

**For System Investigation**:
- "Show CVEs affecting web-server-01"
- "Analyze risk for production systems"
- "List critical vulnerabilities across the fleet"
```

## Output Templates

### Template 1: Full Fleet Listing

**User Request**: "Show the managed fleet"

**Skill Response**:
```markdown
# Managed Fleet Inventory

Retrieved from Red Hat Insights on 2024-01-20T10:30:00Z

## Fleet Overview
- **Total Registered Systems**: 42
- **Active (< 24h)**: 38
- **Stale (> 7 days)**: 4

## RHEL Version Distribution
| Version | Count | Percentage |
|---------|-------|------------|
| RHEL 9.3 | 12 | 29% |
| RHEL 9.2 | 6 | 14% |
| RHEL 8.9 | 15 | 36% |
| RHEL 8.8 | 5 | 12% |
| RHEL 7.9 | 4 | 9% |

## Environment Breakdown
| Environment | Count | Systems |
|-------------|-------|---------|
| Production | 25 | web-*, db-*, app-* |
| Staging | 10 | stg-* |
| Development | 7 | dev-* |

## Top 20 Systems (by last check-in)
[Table with display_name, rhel_version, tags, last_seen]

**Would you like to**:
- Filter by specific environment or RHEL version
- View CVEs affecting these systems
- Create remediation plans for vulnerabilities
```

### Template 2: CVE-Affected Systems

**User Request**: "What systems are affected by CVE-2024-1234?"

**Skill Response**:
```markdown
# CVE-2024-1234 Impact Analysis

## Affected Systems Summary
- **Total Vulnerable**: 12 systems
- **Already Patched**: 3 systems
- **Total Registered**: 42 systems
- **Impact Rate**: 29% of fleet

## Vulnerable Systems

| System Name | RHEL Version | Environment | Remediation Available |
|-------------|--------------|-------------|-----------------------|
| web-server-01.example.com | 8.9 | production | ✓ Yes |
| web-server-02.example.com | 8.9 | production | ✓ Yes |
| app-server-03.example.com | 8.8 | staging | ✓ Yes |
| ... | ... | ... | ... |

**Affected Package**: httpd-2.4.51-7.el8_6.5

## Already Patched (No Action Needed)
- db-server-01.example.com (patched on 2024-01-18)
- cache-server-02.example.com (patched on 2024-01-19)
- lb-server-01.example.com (patched on 2024-01-19)

## Next Steps

**To remediate these systems**, use the remediator agent:
- Single system: "Remediate CVE-2024-1234 on web-server-01"
- Batch production: "Remediate CVE-2024-1234 on all production systems"
- All vulnerable: "Create playbook for CVE-2024-1234 affecting these 12 systems"

**For more analysis**:
- "Show CVSS score and severity for CVE-2024-1234" (use cve-impact skill)
- "What's the risk assessment for this CVE?" (use cve-impact skill)
```

### Template 3: Environment-Filtered View

**User Request**: "Show me production systems"

**Skill Response**:
```markdown
# Production Systems Inventory

Filtered by tag: "production"

## Production Fleet Summary
- **Total Production Systems**: 25
- **RHEL 9.x**: 12 systems
- **RHEL 8.x**: 10 systems
- **RHEL 7.x**: 3 systems
- **Active**: 24 systems
- **Stale**: 1 system ⚠️

## System Tiers
### Web Tier (8 systems)
- web-server-01.example.com (RHEL 8.9)
- web-server-02.example.com (RHEL 8.9)
- web-server-03.example.com (RHEL 9.3)
- ...

### Database Tier (6 systems)
- db-server-01.example.com (RHEL 9.3)
- db-server-02.example.com (RHEL 9.3)
- ...

### Application Tier (11 systems)
- app-server-01.example.com (RHEL 8.9)
- app-server-02.example.com (RHEL 8.9)
- ...

## Stale System Alert ⚠️
- backup-server-01.example.com (last seen: 8 days ago)
  - Action: Investigate Insights client connectivity

## Next Steps
- "Show CVEs affecting production systems"
- "List critical vulnerabilities in production"
- "Remediate CVE-X on production web tier"
```

### Template 4: RHEL Version View

**User Request**: "How many RHEL 8 systems do we have?"

**Skill Response**:
```markdown
# RHEL 8.x Systems Inventory

## RHEL 8 Version Breakdown
- **Total RHEL 8.x Systems**: 20 (48% of fleet)
- **RHEL 8.9**: 15 systems (latest)
- **RHEL 8.8**: 5 systems (upgrade recommended)

## RHEL 8.9 Systems (Latest)
[Table with 15 systems]

## RHEL 8.8 Systems (Upgrade Available)
⚠️ These systems are not on the latest RHEL 8.x minor version:
- legacy-app-01.example.com (RHEL 8.8)
- legacy-app-02.example.com (RHEL 8.8)
- test-server-03.example.com (RHEL 8.8)
- ...

**Recommendation**: Consider upgrading RHEL 8.8 systems to RHEL 8.9 for latest security patches.

## Next Steps
- "Show CVEs affecting RHEL 8 systems"
- "Create upgrade plan for RHEL 8.8 → 8.9"
- "Remediate critical CVEs on RHEL 8 fleet"
```

## Examples

### Example 1: General Fleet Query

**User Request**: "Show the managed fleet"

**Skill Response**:
1. Call `get_host_details()` without filters → retrieve all systems
2. Group by RHEL version, environment tags
3. Calculate totals and percentages
4. Sort by last_seen (most recent first)
5. Generate Template 1 output
6. Offer next step options (CVE analysis, remediation)

### Example 2: CVE Impact Query

**User Request**: "What systems are affected by CVE-2024-1234?"

**Skill Response**:
1. Call `get_cve_systems(cve_id="CVE-2024-1234")`
2. Separate vulnerable vs. patched systems
3. Extract affected package information
4. Generate Template 2 output
5. Suggest remediation agent for next steps

### Example 3: Environment Filter

**User Request**: "Show me staging systems"

**Skill Response**:
1. Call `get_host_details()` → retrieve all systems
2. Filter by tag: "staging" in system.tags
3. Group by tier/function (inferred from hostname)
4. Generate Template 3 output
5. Suggest CVE analysis or remediation options

### Example 4: Version-Specific Query

**User Request**: "List all RHEL 9 systems"

**Skill Response**:
1. Call `get_host_details()` → retrieve all systems
2. Filter: rhel_version starts with "9"
3. Group by minor version (9.3, 9.2, etc.)
4. Generate Template 4 output
5. Suggest upgrade or remediation workflows

## Error Handling

**No Systems Found**:
```
Fleet Inventory Query: No Results

Query: [user's filter criteria]
Result: No systems match the specified criteria

Possible reasons:
1. No systems registered in Red Hat Insights
2. Filter criteria too restrictive
3. Systems not tagged with specified environment

Troubleshooting:
- Verify systems are registered: Check Red Hat Insights console
- Try broader filters: Remove environment/version constraints
- Check tag spelling: Ensure tag names match exactly
```

**Insights API Error**:
```
Fleet Inventory Query: API Error

Error: Unable to retrieve system inventory from Red Hat Insights

Possible causes:
1. insights-mcp server not running
2. Authentication failure (check LIGHTSPEED credentials)
3. Network connectivity issues

Troubleshooting:
1. Verify insights-mcp server is running: Check .mcp.json configuration
2. Check credentials: echo $LIGHTSPEED_CLIENT_ID
3. Test manually: podman run insights-mcp-server
```

**Stale System Warning**:
```
⚠️ Stale Systems Detected

The following systems have not checked in recently (> 7 days):
- system-01.example.com (last seen: 8 days ago)
- system-02.example.com (last seen: 12 days ago)

Impact: Vulnerability data may be outdated for these systems

Recommended Actions:
1. Verify Insights client is running: systemctl status insights-client
2. Check network connectivity from these systems
3. Review Insights client logs: /var/log/insights-client/insights-client.log
4. Re-register if needed: insights-client --register
```

## Best Practices

1. **Start broad, then filter** - Retrieve full inventory first, then apply filters
2. **Group by meaningful categories** - Environment, RHEL version, tier/function
3. **Highlight stale systems** - Warn users about systems with outdated data
4. **Offer remediation transitions** - Always suggest next steps (use remediator agent)
5. **Use clear formatting** - Tables for detailed lists, summaries for overviews
6. **Include percentages** - Help users understand fleet composition
7. **Show last check-in times** - Indicate data freshness
8. **Link to CVE analysis** - Transition to cve-impact skill for vulnerability details

## Tools Reference

This skill primarily uses:
- `get_host_details` (insights-mcp) - Retrieve system inventory
- `get_cve_systems` (insights-mcp) - Find systems affected by specific CVEs

All tools are provided by the insights-mcp MCP server configured in `.mcp.json`.

## Integration with Other Skills

- **cve-impact**: Transition to CVE analysis after identifying affected systems
- **remediator agent**: Transition to remediation workflows after fleet discovery
- **remediation-verifier**: Verify remediation status on specific systems

**Typical Workflow**:
1. User: "Show the managed fleet" → **fleet-inventory skill**
2. Response shows 42 systems, 15 have CVE-2024-1234
3. User: "What's the risk of CVE-2024-1234?" → **cve-impact skill**
4. Response shows CVSS 8.1, Critical severity
5. User: "Remediate CVE-2024-1234 on all affected systems" → **remediator agent**
6. Agent generates playbook, executes, verifies → **Complete workflow**

**Information-First Principle**:
```
Always start with discovery:
1. What systems do we have? (fleet-inventory)
2. What are they vulnerable to? (cve-impact)
3. How do we fix it? (remediator agent)

This ensures informed decisions before taking remediation actions.
```
