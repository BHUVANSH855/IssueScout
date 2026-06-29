# Security Policy

Thank you for helping keep **IssueScout** and its users safe.

We take security issues seriously and appreciate responsible disclosure of vulnerabilities.

---

# Supported Versions

The following table describes which versions of IssueScout currently receive security updates.

| Version | Supported |
| ------- | --------- |
| 0.1.x   | ✅ Yes     |
| < 0.1   | ❌ No      |

---

# Reporting a Vulnerability

If you believe you have discovered a security vulnerability in IssueScout, please report it responsibly.

Please **do not open a public GitHub issue** for security vulnerabilities.

Instead, contact the maintainer directly.

Include as much information as possible:

* Description of the vulnerability
* Steps to reproduce
* Expected behavior
* Actual behavior
* Proof of concept (if available)
* Potential impact
* Suggested mitigation (optional)

---

# What to Expect

After receiving a security report, we will:

1. Acknowledge receipt of the report.
2. Investigate the issue.
3. Determine its severity and impact.
4. Develop and test a fix.
5. Release a security update if necessary.
6. Credit the reporter when appropriate (unless anonymity is requested).

---

# Scope

This policy applies to:

* FastAPI backend
* GitHub API integrations
* Repository scanning engine
* Prediction engine
* Evidence collection modules
* REST API endpoints
* Dependency management

Third-party services such as GitHub itself are outside the scope of this policy.

---

# Security Best Practices

When deploying or using IssueScout:

* Keep dependencies up to date.
* Use the latest supported release.
* Store GitHub Personal Access Tokens securely.
* Never commit secrets or credentials to version control.
* Use environment variables for sensitive configuration.
* Rotate compromised credentials immediately.
* Enable Dependabot and GitHub security alerts.

---

# Supported Reporting Languages

Security reports are accepted in:

* English

---

# Disclosure Policy

Please allow reasonable time for investigation and remediation before publicly disclosing any security vulnerability.

Responsible disclosure helps protect all users of the project.

---

# Acknowledgements

We sincerely appreciate security researchers and community members who responsibly disclose vulnerabilities and help improve the security of IssueScout.

Thank you for helping make the project safer for everyone.
