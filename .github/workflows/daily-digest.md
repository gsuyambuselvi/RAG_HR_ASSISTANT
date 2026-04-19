---
# Trigger - run every weekday morning
on:
  schedule: daily

# Permissions - read issues and PRs
permissions:
  contents: read
  issues: read
  pull-requests: read

# Tools - GitHub API access
tools:
  github:
    toolsets: [default]

# Network access
network: defaults

# Safe outputs - create issues with automatic cleanup
safe-outputs:
  create-issue:
    title-prefix: "Daily Digest"
    labels: [report, digest]
    close-older-issues: true
    expires: 7

source: gsuyambuselvi/library/.github/workflows/daily-digest.md@e62927d310b581969cc857b24762a0c7dc53b7b1
---

# Daily Digest Report

Every weekday morning, analyze all open issues and pull requests in the repository.

## Instructions

Use the GitHub API to fetch all open issues and pull requests.

For each item, collect:
- Title
- Author (GitHub username)
- Label(s)
- Time since opened (human-readable format like "2 days", "3 weeks")

Group all items by label. For items with multiple labels, include them in each label group.

Generate a GitHub issue with:

**Title**: "Daily Digest – YYYY-MM-DD" (use today's date)

**Content structure**:

### Summary

Include total counts in this format:
- Total Issues: N
- Total Pull Requests: M
- Total Items: N+M

### Items by Label

For each label with open items, create a section:

#### [Label Name] (N items)

List items in this format:

- **[Title](link)** - @author, open for X days

For items with no labels, create a section called "#### Unlabeled (N items)".

Replace this section with specific instructions for the AI. For example:

1. Read the issue description and comments
2. Analyze the request and gather relevant information
3. Provide a helpful response or take appropriate action

Be clear and specific about what the AI should accomplish.

## Notes

- Run `gh aw compile` to generate the GitHub Actions workflow
- See https://github.github.com/gh-aw/ for complete configuration options and tools documentation
