# Security Policy

Thank you for helping keep **post-quantum-studio** and its users safe.

This repository is a demo-safe post-quantum cryptography reference studio aligned to NIST FIPS 203, 204, and 205 concepts. It is **not** a production cryptography implementation. Please treat all findings seriously, especially anything that could cause unsafe reuse, misleading security claims, accidental secret exposure, or insecure copy-paste adoption in real systems.

## Supported Versions

| Version | Supported |
|---------|-----------|
| main | Yes |
| All older commits, tags, and experiments | No |

Security fixes will be applied to the current `main` branch unless explicitly stated otherwise.

## Reporting a Vulnerability

Please **do not** open public GitHub issues or pull requests for suspected security vulnerabilities.

Instead, use GitHub’s private vulnerability reporting flow from the repository’s **Security** tab by clicking **Report a vulnerability**. GitHub documents this as the recommended private reporting path for repositories with private vulnerability reporting enabled. [web:154][web:164]

If private reporting is unavailable for any reason, report privately to the maintainer with:
- A clear description of the issue.
- Impact assessment.
- Steps to reproduce.
- Proof of concept, logs, or screenshots if relevant.
- Any suggested mitigation or fix.

## What to Report

Please report issues such as:
- Cryptographic misuse risks or misleading security guarantees.
- Implementation flaws that could encourage insecure production use.
- Secret exposure, token leakage, or unsafe defaults.
- Dependency vulnerabilities with realistic impact.
- Insecure deserialization, injection, path traversal, or auth/session issues if applicable.
- Supply-chain risks in build, release, or CI/CD workflows.

## Response Expectations

The project aims to follow this response process:
- Acknowledge receipt within 3 business days.
- Perform initial triage within 7 business days.
- Provide status updates for valid reports as investigation continues.
- Coordinate disclosure and remediation before any public discussion.

Response times are goals, not guarantees, but good-faith reports will be handled as quickly as possible.

## Responsible Disclosure

To protect users and downstream adopters:
- Do not disclose the issue publicly before a fix or mitigation is available.
- Do not exploit the issue beyond what is necessary to demonstrate impact.
- Do not access, modify, or destroy data that does not belong to you.
- Give maintainers reasonable time to investigate and remediate.

## Scope Notes

Because this repository is a **reference studio** and not a production cryptography library:
- Findings related to unsafe educational examples, misleading naming, or ambiguous security messaging are in scope.
- Reports should clearly distinguish between demo/reference limitations and exploitable implementation flaws.
- Production deployment of this code without additional hardening is out of scope as a support commitment, but unsafe patterns that could mislead users are still important to report.

## Security Hygiene

Project maintainers may use repository protections such as dependency review, secret scanning, code scanning, and CI-based checks where available. A documented security policy is a recommended repository security practice and helps contributors know how to report issues safely. [web:159][web:160][web:165]

## Disclosure and Credit

After a fix or mitigation is ready, maintainers may publish a GitHub security advisory or other coordinated disclosure notice as appropriate. Reporters may be credited unless they prefer to remain private. [web:154][web:167]
