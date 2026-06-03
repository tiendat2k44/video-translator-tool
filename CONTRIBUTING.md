# Contributing Guide

Thank you for interest in contributing to Video Translator Tool!

## Code of Conduct

Please be respectful and inclusive in all interactions.

## Getting Started

1. **Fork the repository**
   ```bash
   git clone https://github.com/YOUR_USERNAME/video-translator-tool.git
   cd video-translator-tool
   ```

2. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Set up development environment**
   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   pip install -r requirements-dev.txt  # Development dependencies
   ```

## Development Guidelines

### Code Style
- Follow PEP 8 conventions
- Use type hints where possible
- Document functions with docstrings
- Max line length: 100 characters

### Commit Messages
- Use present tense ("Add feature" not "Added feature")
- Be descriptive and concise
- Reference issues when relevant: "Fix #123"

### Testing
```bash
# Run tests
pytest

# Check code quality
flake8 modules/ utils/
black --check modules/ utils/
```

### Documentation
- Update README.md if adding features
- Add docstrings to functions
- Update EXAMPLES.md with new examples
- Update ARCHITECTURE.md if changing structure

## Types of Contributions

### Bug Reports
- Check if issue already exists
- Include Python version and OS
- Provide reproducible example
- Include error logs

### Feature Requests
- Describe use case clearly
- Provide example usage
- Consider performance impact
- Check for conflicts with existing features

### Code Contributions
1. Make your changes
2. Add tests for new functionality
3. Update documentation
4. Run quality checks
5. Submit pull request with clear description

### Documentation
- Improve README clarity
- Add missing examples
- Fix typos and errors
- Improve code comments

## Pull Request Process

1. **Update documentation**
   - README.md (if needed)
   - EXAMPLES.md (if adding features)
   - ARCHITECTURE.md (if changing structure)

2. **Add tests**
   ```bash
   pytest tests/
   ```

3. **Run quality checks**
   ```bash
   flake8 modules/ utils/
   black modules/ utils/
   mypy modules/ utils/
   ```

4. **Create pull request**
   - Clear description of changes
   - Reference related issues
   - Include before/after examples if applicable

5. **Wait for review**
   - Maintainers will review
   - Address feedback
   - Update as requested

## Areas for Contribution

### High Priority
- [ ] Add support for more video platforms
- [ ] Improve translation accuracy
- [ ] Add GPU acceleration
- [ ] Create web UI

### Medium Priority
- [ ] Add more language support
- [ ] Improve documentation
- [ ] Add more test coverage
- [ ] Performance optimization

### Low Priority
- [ ] UI/UX improvements
- [ ] Code refactoring
- [ ] Minor bug fixes
- [ ] Documentation improvements

## Development Setup

### Install Development Dependencies
```bash
pip install pytest pytest-cov flake8 black mypy
```

### Project Structure
```
video-translator-tool/
├── modules/           # Core modules
├── utils/            # Utility functions
├── tests/            # Test files
├── config.py         # Configuration
├── main.py           # CLI entry point
└── quickstart.py     # Setup script
```

### Running Tests
```bash
pytest                           # Run all tests
pytest tests/test_module.py     # Run specific test
pytest --cov=modules            # With coverage
pytest -v                       # Verbose output
```

## Reporting Issues

**Security Issues:** Please email privately instead of using issues tracker.

**Bug Reports:** Include:
- Python version
- OS and version
- Steps to reproduce
- Expected vs actual behavior
- Error logs

**Feature Requests:** Include:
- Use case description
- Example usage
- Any implementation ideas
- Potential challenges

## Questions?

- Check existing issues and discussions
- Read documentation
- Ask in GitHub discussions

## Code Review Checklist

Before submitting PR:
- [ ] Code follows PEP 8
- [ ] All tests pass
- [ ] Documentation updated
- [ ] No breaking changes (or documented)
- [ ] Commit messages are clear
- [ ] No debug code left
- [ ] Performance acceptable

## License

By contributing, you agree that your contributions will be licensed under MIT License.

---

Thank you for contributing! 🎉
