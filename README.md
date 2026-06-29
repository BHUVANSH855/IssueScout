# 🚀 IssueScout

<div align="center">

# Intelligent GitHub Contribution Assistant

Analyze GitHub repositories, discover contribution opportunities, and understand issue–pull request relationships using evidence-driven analysis.

<p>

![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-009688?logo=fastapi)
![License](https://img.shields.io/badge/License-MIT-green)
![Tests](https://img.shields.io/badge/Tests-260%2B-success)
![Coverage](https://img.shields.io/badge/Coverage-98%25-brightgreen)
![Ruff](https://img.shields.io/badge/Lint-Ruff-orange)
![GitHub Actions](https://img.shields.io/badge/CI-GitHub_Actions-blue?logo=githubactions)

</p>

</div>

---

# 📖 Overview

IssueScout is an intelligent GitHub contribution assistant designed to help developers discover meaningful open-source contribution opportunities.

Rather than relying solely on labels such as **good first issue** or **help wanted**, IssueScout analyzes multiple signals across a repository to identify relationships between issues and pull requests.

The project combines GitHub repository metadata, issue timelines, commits, comments, reviews, and multiple similarity algorithms to produce explainable predictions about issue activity.

---

# ✨ Features

## 🔍 Repository Analysis

- Repository scanning
- Open issue discovery
- Repository metadata analysis
- Contribution insights

## 📝 Evidence Collection

- Issue comments
- Timeline events
- Commit history
- Pull request metadata
- Review information

## 🧠 Relation Engine

IssueScout combines multiple independent detectors including:

- Author similarity
- Title similarity
- Body references
- Timeline references
- Commit references
- Commit message references
- Branch similarity
- Reviewer similarity
- File similarity
- Label similarity
- Repository metadata similarity

## 🤖 Prediction Engine

- Intelligent pull request prediction
- Confidence scoring
- Explainable results
- Candidate ranking
- JSON output
- Console reports

## ⚡ REST API

- FastAPI REST API
- Interactive Swagger documentation
- OpenAPI specification
- Structured response models

## 🛠️ Developer Experience

- GitHub Actions CI
- Ruff linting & formatting
- Pre-commit hooks
- Dependabot updates
- Structured logging
- Global exception handling
- Comprehensive automated testing

---

# 🏗️ High-Level Architecture

```text
                GitHub Repository
                        │
                        ▼
               GitHub REST API
                        │
        ┌───────────────┴───────────────┐
        │                               │
        ▼                               ▼
 Repository Services            API Endpoints
        │
        ▼
 Evidence Collection
 ├── Timeline
 ├── Comments
 ├── Commits
 ├── Reviews
 └── Metadata
        │
        ▼
 Relation Engine
 ├── Author Similarity
 ├── Title Similarity
 ├── Body References
 ├── Timeline References
 ├── Commit References
 ├── Commit Message References
 ├── Branch Similarity
 ├── Reviewer Similarity
 ├── File Similarity
 ├── Label Similarity
 └── Metadata Similarity
        │
        ▼
 Prediction Engine
        │
        ▼
 Ranking Engine
        │
        ▼
 FastAPI REST API
```

---

# 📂 Project Structure

```text
IssueScout/
│
├── .github/
│   ├── workflows/
│   ├── ISSUE_TEMPLATE/
│   └── dependabot.yml
│
├── backend/
│   ├── issuescout/
│   │   ├── api/
│   │   ├── core/
│   │   ├── evidence/
│   │   ├── github/
│   │   ├── middleware/
│   │   ├── models/
│   │   ├── output/
│   │   ├── prediction/
│   │   ├── presentation/
│   │   ├── ranking/
│   │   ├── scanner/
│   │   ├── services/
│   │   └── utils/
│   │
│   ├── tests/
│   └── pyproject.toml
│
├── docs/
├── frontend/
│
├── CHANGELOG.md
├── CONTRIBUTING.md
├── ROADMAP.md
├── LICENSE
└── README.md
```

---

# 💡 Why IssueScout?

Traditional GitHub searches depend heavily on repository labels and manual inspection.

IssueScout improves this process by combining evidence from multiple GitHub resources into a unified prediction engine that helps contributors understand:

- Which issues are likely already linked to pull requests.
- How issues relate to commits and discussions.
- The confidence of each prediction.
- Why a prediction was made.

This makes repository exploration faster, more transparent, and easier to understand.

---

# ⚡ Installation

## Prerequisites

Before getting started, ensure you have:

- Python 3.12 or later
- Git
- A GitHub Personal Access Token (recommended to avoid rate limits)

---

## Clone the Repository

```bash
git clone https://github.com/BHUVANSH855/IssueScout.git

cd IssueScout/backend
```

---

## Create a Virtual Environment

```bash
python -m venv .venv
```

### Windows

```bash
.venv\Scripts\activate
```

### Linux / macOS

```bash
source .venv/bin/activate
```

---

## Install Dependencies

Install IssueScout in editable mode:

```bash
pip install -e .
```

Install development tools:

```bash
pip install pytest pytest-cov ruff pre-commit
```

Enable Git hooks:

```bash
pre-commit install
```

---

# ⚙️ Configuration

Create a `.env` file inside the `backend` directory.

```env
GITHUB_TOKEN=your_github_personal_access_token
```

### Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `GITHUB_TOKEN` | Recommended | GitHub Personal Access Token |
| `GITHUB_API` | Optional | GitHub REST API endpoint |

---

# ▶️ Running the Application

Start the development server:

```bash
uvicorn issuescout.main:app --reload
```

The API will be available at:

```
http://127.0.0.1:8000
```

---

# 📚 API Documentation

FastAPI automatically generates interactive documentation.

Swagger UI

```
http://127.0.0.1:8000/docs
```

ReDoc

```
http://127.0.0.1:8000/redoc
```

OpenAPI Schema

```
http://127.0.0.1:8000/openapi.json
```

---

# 📡 Available Endpoints

| Method | Endpoint | Description |
|---------|----------|-------------|
| GET | `/` | Welcome endpoint |
| GET | `/health` | Health check |
| GET | `/github` | Repository information |
| GET | `/issues` | List repository issues |
| GET | `/scan/{owner}/{repo}` | Scan a GitHub repository |

---

# 🧪 Testing

Run the complete test suite:

```bash
pytest
```

Run tests with coverage:

```bash
pytest --cov=issuescout
```

Run a specific test:

```bash
pytest tests/github/test_client.py
```

Run all GitHub-related tests:

```bash
pytest tests/github
```

Current status:

- ✅ 260 automated tests
- ✅ High test coverage
- ✅ Fast test execution
- ✅ GitHub Actions CI

---

# 🧹 Code Quality

Lint the project:

```bash
ruff check .
```

Automatically format code:

```bash
ruff format .
```

Run all pre-commit hooks:

```bash
pre-commit run --all-files
```

---

# 🔄 Continuous Integration

IssueScout uses GitHub Actions for continuous integration.

Every push and pull request automatically runs:

- Ruff linting
- Ruff formatting checks
- Complete test suite
- Coverage reporting

Dependabot automatically keeps:

- Python dependencies updated
- GitHub Actions updated

---

# 🛠️ Technology Stack

## Backend

- Python 3.12
- FastAPI
- Pydantic
- HTTPX

## Testing

- Pytest
- Pytest-Cov

## Code Quality

- Ruff
- Pre-commit

## Automation

- GitHub Actions
- Dependabot

## APIs

- GitHub REST API

---

# 📦 Project Highlights

- Modular architecture
- Asynchronous GitHub client
- Evidence-based repository analysis
- Intelligent relation engine
- Explainable prediction system
- Structured logging
- Global exception handling
- Request logging middleware
- Response models
- Pagination utilities
- Automated testing
- Continuous integration
- Production-ready project structure

---

# 📈 Project Status

IssueScout is actively developed and maintained.

Current project status:

| Component | Status |
|-----------|--------|
| FastAPI Backend | ✅ Stable |
| GitHub REST Client | ✅ Stable |
| Repository Scanner | ✅ Stable |
| Evidence Collection | ✅ Stable |
| Relation Engine | ✅ Stable |
| Prediction Engine | ✅ Stable |
| Ranking Engine | ✅ Stable |
| REST API | ✅ Stable |
| Automated Tests | ✅ 260 Passing |
| GitHub Actions | ✅ Enabled |
| Ruff Linting | ✅ Enabled |
| Pre-commit Hooks | ✅ Enabled |
| Dependabot | ✅ Enabled |
| Documentation | ✅ Up to Date |

---

# 🗺️ Roadmap

## Version 0.2.0

### Planned Features

- GitHub GraphQL integration
- Improved repository scanning performance
- Advanced repository filters
- Better relation detection
- Concurrent GitHub requests

---

## Version 0.3.0

### CLI

- `issuescout scan`
- `issuescout analyze`
- `issuescout repo`

### Backend

- Request caching
- Rate-limit management
- Background scanning
- Persistent scan history

---

## Version 0.4.0

### Dashboard

- Repository overview
- Contribution analytics
- Pull request visualization
- Scan history
- Interactive reports

---

## Version 1.0.0

### Stable Release

- Stable public API
- GraphQL support
- AI-assisted issue recommendations
- Production deployment
- Complete documentation
- Plugin architecture

---

# 🤝 Contributing

Contributions are always welcome!

Whether you'd like to:

- Report a bug
- Suggest a feature
- Improve documentation
- Write tests
- Refactor existing code
- Improve performance

your contributions are appreciated.

Please read the project's **CONTRIBUTING.md** before opening a pull request.

Typical workflow:

1. Fork the repository.
2. Create a new branch.
3. Make your changes.
4. Run Ruff and the test suite.
5. Commit your work.
6. Open a Pull Request.

---

# 🧪 Development Workflow

Install pre-commit hooks:

```bash
pre-commit install
```

Before committing:

```bash
ruff check .
ruff format .
pytest
```

If all checks pass, commit your changes.

---

# 📄 License

This project is licensed under the **MIT License**.

See the **LICENSE** file for details.

---

# 🙏 Acknowledgements

IssueScout is built using several excellent open-source projects.

Special thanks to the communities behind:

- Python
- FastAPI
- Pydantic
- HTTPX
- Pytest
- Ruff
- GitHub REST API
- GitHub Actions

Their work makes projects like IssueScout possible.

---

# 👨‍💻 Author

**Bhuvansh Kataria**

Computer Science Engineering Student

GitHub:

**https://github.com/BHUVANSH855**

---

# ⭐ Support the Project

If you find IssueScout useful, consider:

- ⭐ Starring the repository
- 🍴 Forking the project
- 🐛 Reporting bugs
- 💡 Suggesting new features
- 🤝 Contributing code
- 📢 Sharing the project with others

Every contribution—big or small—helps improve IssueScout.

---

<div align="center">

## 🚀 Happy Contributing!

Made with ❤️ for the open-source community.

**IssueScout — Helping developers discover meaningful GitHub contributions.**

</div>
