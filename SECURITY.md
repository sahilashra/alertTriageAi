# Security Policy

## Supported Versions

We release patches for security vulnerabilities for the following versions:

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |
| < 1.0   | :x:                |

## Reporting a Vulnerability

We take security seriously. If you discover a security vulnerability, please follow these steps:

### 1. Do Not Disclose Publicly

Please **DO NOT** open a public GitHub issue for security vulnerabilities.

### 2. Report Privately

Send a detailed report to: [your-email@example.com]

Include:
- Description of the vulnerability
- Steps to reproduce
- Potential impact
- Suggested fix (if any)

### 3. Response Timeline

- **Initial Response**: Within 48 hours
- **Status Update**: Within 7 days
- **Fix Timeline**: Depends on severity
  - Critical: 1-7 days
  - High: 7-14 days
  - Medium: 14-30 days
  - Low: 30-90 days

### 4. Disclosure Policy

- We will work with you to understand and resolve the issue
- Once fixed, we will publicly disclose the vulnerability
- You will be credited for the discovery (unless you prefer to remain anonymous)

## Security Best Practices

### For Users

1. **Never commit `.env` files** with real API keys
2. **Use strong API keys** and rotate them regularly
3. **Run in demo mode** unless you need real execution
4. **Review scripts** before approving execution
5. **Keep dependencies updated**: `pip install --upgrade -r requirements.txt`

### For Contributors

1. **No hardcoded secrets** in code
2. **Use environment variables** for all sensitive data
3. **Validate all inputs** especially for script generation
4. **Follow principle of least privilege**
5. **Run security scanners**: `safety check`, `bandit -r backend/`

## Security Features

### Current Implementation

- ✅ Script safety validation (8-point check)
- ✅ Human-in-the-loop approval required
- ✅ Demo mode for safe testing
- ✅ Input validation with Pydantic
- ✅ CORS configuration
- ✅ Error handling and logging

### Planned Enhancements

- ⏳ Rate limiting
- ⏳ Authentication and authorization
- ⏳ Audit logging
- ⏳ Encrypted credential storage
- ⏳ SOC2 compliance

## Known Security Considerations

### Demo Mode

- Current implementation uses **demo mode** by default
- Real script execution is **disabled** unless explicitly enabled
- Always review generated scripts before approval

### API Keys

- Gemini API keys should be kept **confidential**
- Use environment variables, never hardcode
- Consider using key rotation policies

### Script Execution

- Generated scripts undergo safety validation
- Dangerous command patterns are blocked
- Backup steps are mandatory
- Full audit trail is maintained

## Third-Party Dependencies

We regularly monitor dependencies for known vulnerabilities:

```bash
# Check for vulnerable packages
pip install safety
safety check

# Update dependencies
pip install --upgrade -r requirements.txt
```

## Contact

For security-related questions: [your-email@example.com]

---

**Last Updated:** October 2025  
**Version:** 1.0.0
