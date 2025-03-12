# Contributing to Telegram Bot Framework

Thank you for your interest in contributing to the Telegram Bot Framework! This document provides guidelines and instructions for contributing to this project.

## Code of Conduct

By participating in this project, you agree to abide by our Code of Conduct. Please be respectful, inclusive, and constructive in all interactions.

## How to Contribute

### Reporting Bugs

If you find a bug, please create an issue with the following information:

1. A clear, descriptive title
2. Steps to reproduce the issue
3. Expected behavior
4. Actual behavior
5. Screenshots (if applicable)
6. Environment details (OS, Python version, framework version)

### Suggesting Enhancements

We welcome suggestions for enhancements! When creating an issue for a feature request, please:

1. Provide a clear description of the feature
2. Explain why this feature would be useful
3. Outline how it might be implemented
4. Specify if you're willing to work on implementing it

### Pull Requests

We actively welcome pull requests:

1. Fork the repository
2. Create a new branch (`git checkout -b feature/your-feature-name`)
3. Make your changes
4. Add tests for your changes if applicable
5. Run the test suite to ensure everything passes
6. Commit your changes (`git commit -am 'Add some amazing feature'`)
7. Push to the branch (`git push origin feature/your-feature-name`)
8. Create a new Pull Request

## Development Setup

1. Clone the repository
   ```bash
   git clone https://github.com/yourusername/telegram-bot-framework.git
   cd telegram-bot-framework
   ```

2. Create a virtual environment
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install development dependencies
   ```bash
   pip install -e ".[dev]"
   ```

## Coding Style

Please follow these style guidelines:

- Follow PEP 8 style guidelines
- Use Black for code formatting (`black .`)
- Sort imports with isort (`isort .`)
- Use type hints where appropriate
- Write docstrings for all functions, classes, and modules
- Keep functions small and focused on a single responsibility
- Add comments for complex logic

## Testing

- Write unit tests for all new functionality
- Ensure all tests pass before submitting a pull request
- Run tests with pytest:
  ```bash
  pytest
  ```
- Aim for high test coverage:
  ```bash
  pytest --cov=telegram_bot_framework
  ```

## Documentation

- Update documentation when changing functionality
- Document all new functions, classes, and modules
- Keep README and other documentation up to date
- Use clear, concise language in docstrings and comments

## Git Workflow

- Create a branch from `main` for your changes
- Use descriptive branch names (e.g., `feature/conversation-handler`, `fix/webhook-timeout`)
- Make focused commits with clear commit messages
- Rebase your branch on `main` before submitting a pull request
- Squash commits if necessary to maintain a clean history

## Pull Request Process

1. Ensure your code follows the style guidelines
2. Update the documentation if necessary
3. Add tests for your changes
4. Ensure the test suite passes
5. Make sure your code doesn't introduce any new linting warnings
6. Update the CHANGELOG.md with details of your changes

## Releasing

The project maintainers will handle releases following semantic versioning:

- MAJOR version when making incompatible API changes
- MINOR version when adding functionality in a backward-compatible manner
- PATCH version when making backward-compatible bug fixes

## License

By contributing to this project, you agree that your contributions will be licensed under the project's MIT License. See the [LICENSE](LICENSE) file for details. 