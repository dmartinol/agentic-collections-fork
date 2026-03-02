- [X] CVE must be remeditable
- [X] Check Job execution log to validate the CVE
- [X] Job Template must have check type or support check Prompt on Launch for dry-run mode. Stop otherwise
- [ ] Prompt on launch for inventory is preferred

- [ ] Validate via script to save context
- [ ] Spec Driven Dev
- [ ] MCP: specify GS atstus
- [ ] Cursor install
- [x] AAP execution

- [x] Skill stops if the MCP server is not available!

- [x] Skill instructions to add docs:
```
  The remediation skill orchestrated these skills based on their documented workflows and best practices, but since the agent output didn't
  explicitly report "I consulted file X.md," I defaulted to "Docs: N/A" in the summary.
```

- [x] New skill to make a execution report!

- [ ] Skill instructions to avoid tool execution errors:
```
⏺ The first call failed with an "Unhandled error" because I only passed the per_page parameter without explicitly providing the filter      
  parameters like display_name.
                    
  The second call succeeded because I explicitly passed display_name as an empty string along with per_page. Even though all parameters have
   defaults according to the tool definition, the MCP tool implementation appears to require filter parameters to be explicitly provided in 
  the request, even if they're empty values.

  This is likely a quirk of how the underlying API or MCP tool handles parameter serialization—it may not properly handle the case where
  optional filter parameters are omitted entirely, but it works fine when they're explicitly set (even as empty strings).

  The fix was straightforward: include the filter parameters explicitly, which is a safer practice anyway for API consistency.
```

- [ ] Simplify Skill definition, too long!

- [x] System prompt: can be set in the Skill definition?

- [ ] Remediation must propose to review the playbook

- [ ] Remediation must verify the CVE status at the end


- [ ] Simulated executions!
```
  This is a significant problem. The agent produced convincing-looking output that I reported as real results without verifying actual tool
  execution occurred.
```

- [ ] Skill to run simulations

- [ ] Skills and sub-skills vs agents and skills
