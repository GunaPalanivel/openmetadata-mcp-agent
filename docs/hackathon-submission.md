# Hackathon submission (Track T-01)

Checklist for **WeMakeDevs × OpenMetadata — Back to the Metadata** (T-01: MCP Ecosystem & AI Agents). Human steps unless your automation owns them.

## Form (P4-04)

- [ ] **Track**: T-01 (correct paradox).
- [ ] **Repository**: `https://github.com/GunaPalanivel/openmetadata-mcp-agent`
- [ ] **Team**: “The Mavericks” + all GitHub handles.
- [ ] **Related issues**: [#26645](https://github.com/open-metadata/OpenMetadata/issues/26645), [#26608](https://github.com/open-metadata/OpenMetadata/issues/26608)
- [ ] **Demo video URL** (when recorded): link in form as required by organizers.

## After submit

- [ ] Comment on upstream **#26645** and **#26608** with repo + demo link (coordination, not “claim”).
- [ ] GFI: only check if you actually opened an upstream **good-first-issue** PR; otherwise omit.

## Optional CI integration job

Main-branch integration tests need repository variables/secrets configured (`OM_INTEGRATION_TESTS_ENABLED`, bot JWT, OpenAI key). See [.github/workflows/ci.yml](../.github/workflows/ci.yml).

## Innovation pitch alignment

The shipped product’s **primary** differentiators are **HITL-governed writes**, **prompt-injection defenses**, and **deep OM MCP usage**. Optional **GitHub MCP** (`GITHUB_TOKEN`) enables cross-MCP issue creation; if not configured, say so in the narrative rather than implying it runs out of the box.

For operations and recovery during a demo, see [`runbook.md`](runbook.md).
