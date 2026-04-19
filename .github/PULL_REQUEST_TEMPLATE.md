### Related Issues

- closes #

### Proposed Changes

<!-- What does this PR do and why? Be specific about the implementation approach. -->

### How I tested

- Unit:
  -
- Integration:
  -
- Quality:
  - `pre-commit run --all-files`
  - `make test`
- Regression:
  - All existing tests pass

### Notes for reviewers

<!-- Anything the reviewer should pay extra attention to: tricky logic, security implications, architectural decisions, or known limitations. -->

### Checklist

- [ ] I have read the [coding standards](/.idea/Plan/Architecture/CodingStandards.md) and the [NFRs](/.idea/Plan/Project/NFRs.md)
- [ ] `pre-commit run --all-files` passes locally
- [ ] New code has tests (happy path + at least one failure case)
- [ ] All existing tests still pass
- [ ] No `print()` or `console.log` in production paths
- [ ] No secrets, hardcoded URLs, or `--no-verify` commits
- [ ] Docstrings added for new functions
- [ ] README updated if new setup steps are needed
