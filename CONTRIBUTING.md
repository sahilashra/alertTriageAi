# Contributing to Agentic Alert Triage AI

First off, thank you for considering contributing to this project! 🎉

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check the existing issues to avoid duplicates. When you create a bug report, include as many details as possible:

- **Use a clear and descriptive title**
- **Describe the exact steps to reproduce the problem**
- **Provide specific examples**
- **Describe the behavior you observed and what you expected**
- **Include screenshots if applicable**
- **Mention your environment** (OS, Python version, etc.)

### Suggesting Enhancements

Enhancement suggestions are welcome! Please provide:

- **Use a clear and descriptive title**
- **Provide a step-by-step description of the suggested enhancement**
- **Explain why this enhancement would be useful**
- **List any similar features in other tools**

### Pull Requests

1. Fork the repo and create your branch from `main`
2. If you've added code that should be tested, add tests
3. Ensure the test suite passes
4. Make sure your code follows the existing style
5. Write a clear commit message

## Development Setup

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/alert-triage-ai.git
cd alert-triage-ai

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up pre-commit hooks (optional but recommended)
pip install pre-commit
pre-commit install

# Create your .env file
cp .env.example .env
# Edit .env and add your Gemini API key

# Run the application
.\START.ps1
```

## Coding Standards

### Python

- Follow [PEP 8](https://pep8.org/)
- Use type hints where appropriate
- Write docstrings for functions and classes
- Keep functions focused and small
- Maximum line length: 100 characters

### JavaScript

- Use ES6+ features
- Follow existing naming conventions
- Comment complex logic
- Keep functions pure when possible

### Commit Messages

Follow the [Conventional Commits](https://www.conventionalcommits.org/) specification:

```
feat: add new alert type support
fix: resolve Gemini API timeout issue
docs: update README with deployment instructions
refactor: simplify script validation logic
test: add unit tests for gemini_service
chore: update dependencies
```

## Project Structure

```
alert-triage-ai/
├── backend/           # FastAPI backend
│   ├── app.py        # Main application
│   ├── models.py     # Pydantic models
│   ├── gemini_service.py  # AI service
│   └── script_executor.py # Script execution
├── frontend/         # Web UI
│   └── index.html    # Single-page app
├── data/            # Demo data and knowledge base
├── scripts/         # Sample remediation scripts
└── tests/           # Test suite (to be added)
```

## Testing

```bash
# Run tests (when available)
pytest

# Run with coverage
pytest --cov=backend

# Run specific test file
pytest tests/test_gemini_service.py
```

## Documentation

- Update README.md if you change functionality
- Add docstrings to new functions
- Update API documentation if you modify endpoints
- Keep comments up-to-date

## Code of Conduct

### Our Pledge

We are committed to providing a welcoming and inspiring community for all.

### Our Standards

Examples of behavior that contributes to a positive environment:

- Using welcoming and inclusive language
- Being respectful of differing viewpoints
- Gracefully accepting constructive criticism
- Focusing on what is best for the community
- Showing empathy towards other community members

Examples of unacceptable behavior:

- Trolling, insulting/derogatory comments, and personal attacks
- Public or private harassment
- Publishing others' private information without permission
- Other conduct which could reasonably be considered inappropriate

### Enforcement

Instances of abusive, harassing, or otherwise unacceptable behavior may be reported to the project team. All complaints will be reviewed and investigated promptly and fairly.

## Questions?

Feel free to:
- Open an issue for discussion
- Reach out via email (see README for contact info)
- Join our community discussions

## Recognition

Contributors will be recognized in:
- README.md contributors section
- Release notes for their contributions
- GitHub contributors page

Thank you for contributing! 🚀

---

**Happy Coding!**  
Team Integrator
