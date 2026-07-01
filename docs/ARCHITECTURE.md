# IssueScout Architecture

**Version:** 1.0 (Draft)

**Last Updated:** July 2026

---

# Table of Contents

1. Introduction
2. Project Vision
3. Project Goals
4. Design Principles
5. High-Level Architecture
6. System Overview
7. Repository Structure
8. Backend Architecture
9. Frontend Architecture
10. Data Flow
11. Prediction Pipeline
12. Evaluation Pipeline
13. Scanner Pipeline
14. API Layer
15. Future Architecture
16. Scalability
17. Security Considerations
18. Design Decisions
19. Glossary

---

# 1. Introduction

IssueScout is a modern GitHub contribution assistant designed to help contributors discover suitable issues, understand repository activity, analyze pull request relationships, and evaluate prediction quality using measurable metrics.

Unlike traditional issue recommendation tools that rely solely on labels or keyword matching, IssueScout performs multi-stage repository analysis by combining repository metadata, issue history, pull request information, commit history, timeline events, comments, reviewers, labels, and multiple relation detectors.

The project has been designed as a modular and extensible platform so that support for additional repositories, prediction algorithms, ranking strategies, and machine learning models can be added without changing the overall architecture.

---

# 2. Project Vision

The long-term vision of IssueScout is to become a universal open-source contribution assistant capable of supporting contributors across thousands of GitHub repositories.

Rather than being tailored to a single project such as CPython, IssueScout is designed around repository-independent abstractions that allow the same prediction pipeline to operate on any GitHub repository.

The project focuses on three major objectives:

- Helping contributors discover meaningful issues.
- Predicting relationships between issues and pull requests.
- Measuring prediction quality through reproducible evaluation.

---

# 3. Project Goals

The architecture is built around the following goals.

## Universality

IssueScout should support any GitHub repository without requiring repository-specific code whenever possible.

Repository-specific behaviour should be isolated through repository profiles.

---

## Modularity

Every subsystem should have a single responsibility.

Examples include:

- Scanner
- Prediction
- Evaluation
- Ranking
- API
- GitHub Services

Each component should evolve independently.

---

## Extensibility

The architecture should allow developers to add:

- new analyzers
- new relation detectors
- new ranking algorithms
- new confidence calculations
- new exporters
- new evaluation metrics

without modifying existing implementations.

---

## Maintainability

The project emphasizes:

- readable code
- clear package boundaries
- dependency injection
- low coupling
- high cohesion

to simplify future maintenance.

---

## Testability

Every major subsystem is independently testable.

Current testing includes:

- unit tests
- integration tests
- evaluation tests
- scanner tests
- prediction tests
- API tests

The project maintains a comprehensive automated test suite to ensure architectural stability during future development.

---

# 4. Design Principles

IssueScout follows several software engineering principles.

## Single Responsibility Principle

Every class should have one primary responsibility.

Examples include:

- CandidateGenerator generates candidate pull requests.
- Ranker sorts predictions.
- EvaluationRunner compares predictions.
- EvaluationPipeline computes evaluation summaries.

---

## Open/Closed Principle

The architecture encourages extension instead of modification.

Examples:

- New relation detectors can be registered.
- New analyzers can be added.
- New repository profiles can be introduced.

Existing components remain unchanged.

---

## Dependency Injection

Core services receive dependencies through constructors whenever practical.

Benefits include:

- easier testing
- easier mocking
- lower coupling

---

## Separation of Concerns

Different responsibilities are separated into dedicated packages.

For example:

Scanner
→ repository analysis

Prediction
→ relation prediction

Evaluation
→ benchmarking

GitHub
→ API communication

Services
→ GitHub resource access

API
→ REST interface

---

## Repository Independence

The architecture avoids assumptions about any specific repository.

Repository-specific behaviour is isolated into profiles.

Examples include:

- GenericProfile
- CPythonProfile

Future repositories can provide specialized behaviour while preserving the common prediction pipeline.

---

# 5. High-Level Architecture

The system can be viewed as five cooperating layers.

```

                    +-------------------------+
                    |     REST API / CLI      |
                    +-----------+-------------+
                                |
                                v
                    +-------------------------+
                    |     Scanner Engine      |
                    +-----------+-------------+
                                |
                                v
                    +-------------------------+
                    |   Prediction Engine     |
                    +-----------+-------------+
                                |
                                v
                    +-------------------------+
                    | Evaluation & Benchmark  |
                    +-----------+-------------+
                                |
                                v
                    +-------------------------+
                    | GitHub Services Layer   |
                    +-------------------------+

```

Each layer has a dedicated responsibility and communicates through well-defined models.

---

# 6. System Overview

IssueScout consists of several independent subsystems.

## Scanner

Responsible for discovering candidate issues suitable for contributors.

The scanner collects repository information and executes multiple analyzers before assigning confidence scores.

---

## Prediction

Responsible for identifying likely pull request relationships.

The prediction engine combines:

- candidate generation
- relation detection
- ranking
- confidence estimation
- explanation generation

to produce prediction results.

---

## Evaluation

Responsible for measuring prediction quality.

Evaluation includes:

- dataset generation
- ground truth collection
- comparison
- metric computation
- benchmarking

---

## API

Provides REST endpoints that expose IssueScout functionality.

The API is independent of prediction logic and delegates work to backend services.

---

## GitHub Integration

All communication with GitHub occurs through dedicated services.

Examples include:

- IssueService
- PullRequestService
- RepositoryService
- CommitService
- ReviewService

This abstraction isolates external dependencies from business logic.

---

# 7. Repository Structure

The project is organized into clearly separated packages.

```

IssueScout/
│
├── backend/
│
├── frontend/
│
├── docs/
│
├── datasets/
│
├── evaluation/
│
├── scripts/
│
├── README.md
│
├── ROADMAP.md
│
├── CONTRIBUTING.md
│
└── LICENSE

```

The backend contains the implementation while the root repository contains project documentation, datasets, automation scripts, and future frontend assets.

---

# 8. Backend Architecture

The backend is the core of IssueScout. It is responsible for interacting with GitHub, analyzing repositories, predicting issue–pull request relationships, evaluating prediction quality, and exposing functionality through a REST API.

The backend follows a layered, modular architecture where each package has a clearly defined responsibility.

```
                           Backend Architecture

                     +----------------------------+
                     |         FastAPI API        |
                     +-------------+--------------+
                                   |
                                   v
                     +----------------------------+
                     |      Scanner Engine        |
                     +-------------+--------------+
                                   |
                                   v
                     +----------------------------+
                     |    Prediction Services     |
                     +-------------+--------------+
                                   |
                                   v
                     +----------------------------+
                     |  Evaluation & Benchmark    |
                     +-------------+--------------+
                                   |
                                   v
                     +----------------------------+
                     |    GitHub Service Layer    |
                     +-------------+--------------+
                                   |
                                   v
                     +----------------------------+
                     |      GitHub REST API       |
                     +----------------------------+
```

Each package communicates using strongly typed models, minimizing coupling and simplifying testing.

---

# 9. Backend Package Structure

The backend is organized as follows.

```
backend/
│
├── issuescout/
│
│   ├── api/
│   ├── cli/
│   ├── core/
│   ├── evaluation/
│   ├── evidence/
│   ├── github/
│   ├── middleware/
│   ├── models/
│   ├── output/
│   ├── prediction/
│   ├── presentation/
│   ├── profiles/
│   ├── ranking/
│   ├── scanner/
│   ├── services/
│   └── utils/
│
└── tests/
```

Every package has a single responsibility and can evolve independently.

---

# 10. Package Responsibilities

## api/

Provides the REST interface.

Responsibilities include:

- FastAPI routes
- Request validation
- Response models
- Dependency injection
- HTTP endpoints

The API contains no prediction logic.

It delegates work to backend services.

---

## cli/

Provides the command-line interface.

Responsibilities include:

- command parsing
- evaluation commands
- benchmarking
- reporting
- scanning

The CLI acts as a thin wrapper around backend functionality.

---

## core/

Contains application-wide configuration.

Examples include:

- settings
- exception handling
- configuration management

No prediction logic belongs here.

---

## scanner/

Responsible for repository analysis.

Primary responsibilities:

- fetching repository data
- analyzer execution
- linked PR detection
- confidence calculation
- issue filtering

Main classes include:

- ScannerEngine
- Fetcher
- AnalysisPipeline
- ConfidenceCalculator

---

## prediction/

Responsible for pull request prediction.

Components include:

- CandidateGenerator
- AnalysisService
- PredictionService
- ConfidenceService
- ExplanationBuilder
- ExplanationService

This package never communicates directly with GitHub.

Instead, it consumes repository models.

---

## ranking/

Responsible for ordering predictions.

The Ranker determines:

- best prediction
- prediction ordering

Future ranking strategies can be introduced without modifying prediction logic.

---

## evaluation/

Responsible for measuring prediction quality.

Submodules include:

- dataset generation
- exporters
- loaders
- benchmarking
- metrics
- comparison
- report generation

Evaluation is completely independent from prediction.

It consumes prediction outputs.

---

## github/

Contains low-level GitHub communication.

Responsibilities include:

- authentication
- API client
- pagination
- request handling

No business logic exists here.

---

## services/

High-level wrappers around GitHub resources.

Examples:

- RepositoryService
- IssueService
- PullRequestService
- CommitService
- TimelineService
- ReviewService

Services hide HTTP implementation details from the rest of the project.

---

## models/

Defines all shared data structures.

Examples:

- Issue
- PullRequest
- PredictionResult
- RelationPrediction
- RepositoryEvaluation
- EvaluationRecord

Models form the contract between backend components.

---

## evidence/

Responsible for collecting evidence used during prediction.

Evidence includes:

- commits
- comments
- timeline events
- reviewers

Evidence collectors remain independent from prediction algorithms.

---

## profiles/

Supports repository-specific behavior.

Examples:

- GenericProfile
- CPythonProfile

Future repositories may register specialized profiles while preserving common interfaces.

---

## presentation/

Responsible for presenting information to users.

Examples:

- console reporters
- summaries

Presentation is separated from evaluation and prediction.

---

## output/

Contains reusable output formatting utilities.

Supports:

- JSON
- Console
- Explanation formatting

---

## utils/

Contains shared utilities.

Examples:

- text similarity
- issue reference parsing
- helper functions

Utilities should remain generic and reusable.

---

# 11. Dependency Rules

IssueScout follows strict dependency boundaries.

```
API
 │
 ▼
Scanner
 │
 ▼
Prediction
 │
 ▼
Evaluation
 │
 ▼
Models
 │
 ▼
Services
 │
 ▼
GitHub
```

Higher layers may depend on lower layers.

Lower layers must never depend on higher layers.

For example:

✔ Scanner may use Services.

✔ Prediction may use Models.

✔ Evaluation may use Prediction models.

✘ Services must never depend on Prediction.

✘ GitHub must never import Scanner.

---

# 12. Dependency Injection

Whenever practical, dependencies are injected through constructors.

Example:

```
ScannerEngine
    │
    ├── Fetcher
    ├── Detector
    ├── Pipeline
    └── ConfidenceCalculator
```

Benefits include:

- improved testing
- easier mocking
- loose coupling
- future extensibility

---

# 13. Data Models

The project communicates through strongly typed models.

Typical examples include:

```
Issue

↓

PullRequest

↓

RelationPrediction

↓

PredictionResult

↓

EvaluationRecord

↓

RepositoryEvaluation

↓

BenchmarkSuite
```

This minimizes shared mutable state and provides stable interfaces between packages.

---

# 14. Error Handling

Errors are isolated whenever possible.

Examples include:

- failed analyzer execution
- unavailable GitHub resources
- malformed datasets
- missing pull requests

Whenever safe, failures are contained so that processing of unrelated issues can continue.

This improves robustness during large repository scans.

---

# 15. Testing Strategy

Every major backend package is independently tested.

Current test coverage includes:

- API
- Prediction
- Evaluation
- Ranking
- Scanner
- GitHub Services
- Utilities
- Models
- Presentation
- Evidence
- Profiles

The project currently maintains hundreds of automated tests that verify both functionality and architectural integrity.

---

# 16. Internal Execution Pipelines

IssueScout is organized around several independent execution pipelines.

Each pipeline performs one well-defined task while communicating with the others through shared models.

The major execution pipelines are:

- Repository Scanning
- Prediction
- Relation Analysis
- Candidate Generation
- Ranking
- Confidence Estimation
- Explanation Generation
- Evaluation
- Benchmarking

Each pipeline is described below.

---

# 17. Repository Scanning Pipeline

The repository scanner identifies issues that are suitable for contributors.

It coordinates repository fetching, analyzer execution, linked pull request detection, and confidence estimation.

## Workflow

```
Repository
      │
      ▼
Fetcher
      │
      ▼
RepositoryScanContext
      │
      ▼
Issue Collection
      │
      ▼
Linked PR Detection
      │
      ▼
Analysis Pipeline
      │
      ▼
Confidence Calculation
      │
      ▼
Issue Summary
      │
      ▼
Scan Result
```

## Responsibilities

The scanner is responsible for:

- downloading repository metadata
- retrieving issues
- retrieving pull requests
- constructing the repository context
- executing analyzers
- filtering unsuitable issues
- calculating confidence
- returning contributor-friendly summaries

The scanner intentionally avoids prediction logic.

---

# 18. Analysis Pipeline

The analysis pipeline coordinates multiple independent analyzers.

Each analyzer checks one property of an issue.

Current examples include:

- Assignment Analyzer
- Linked Pull Request Analyzer

Future analyzers may include:

- Activity Analyzer
- Complexity Analyzer
- Documentation Analyzer
- First Issue Analyzer
- Repository Health Analyzer

## Workflow

```
Issue
 │
 ▼
Analyzer 1
 │
 ▼
Analyzer 2
 │
 ▼
Analyzer 3
 │
 ▼
Analyzer N
 │
 ▼
Analysis Results
```

Each analyzer returns an independent result.

Failures in one analyzer should not terminate execution of the remaining analyzers.

---

# 19. Prediction Pipeline

Prediction is responsible for identifying which pull request most likely resolves a given issue.

The prediction system is intentionally separated into multiple stages.

## Workflow

```
Issue
 │
 ▼
Candidate Generator
 │
 ▼
Candidate Pull Requests
 │
 ▼
Relation Engine
 │
 ▼
Relation Predictions
 │
 ▼
Ranker
 │
 ▼
Best Prediction
 │
 ▼
Confidence Service
 │
 ▼
Explanation Service
 │
 ▼
Prediction Result
```

Every stage has a single responsibility.

---

# 20. Candidate Generation

Evaluating every pull request in a repository would be computationally expensive.

Candidate generation reduces the search space.

The Candidate Generator applies inexpensive heuristics to identify promising pull requests before invoking the more expensive relation engine.

Current heuristics include:

- shared author
- explicit issue reference
- title similarity
- branch naming conventions
- creation timeline
- shared labels

Only candidate pull requests proceed to the relation engine.

This greatly improves performance.

---

# 21. Relation Engine

The relation engine performs detailed comparison between an issue and each candidate pull request.

Each detector contributes evidence independently.

## Workflow

```
Issue
       │
       ▼
Candidate Pull Request
       │
       ▼
Relation Detector Registry
       │
       ▼
Detector 1
Detector 2
Detector 3
Detector N
       │
       ▼
Evidence Scores
       │
       ▼
Combined Relation Score
```

Current relation detectors include evidence derived from:

- title similarity
- body references
- comments
- commits
- reviewers
- metadata
- labels
- branch names
- timeline events
- commit history

Additional detectors can be registered without modifying the engine.

---

# 22. Ranking Pipeline

Once relation scores have been computed, predictions are ranked.

## Workflow

```
Relation Predictions
        │
        ▼
Ranker
        │
        ▼
Sorted Predictions
        │
        ▼
Best Prediction
```

The ranking algorithm remains independent from relation detection.

Future ranking algorithms may include:

- weighted ranking
- learning-to-rank
- graph-based ranking
- ML-assisted ranking

---

# 23. Confidence Estimation

Confidence estimation provides users with an estimate of prediction reliability.

## Workflow

```
Best Prediction
       │
       ▼
Confidence Service
       │
       ▼
Confidence Score
```

Confidence is intentionally separated from ranking.

A prediction with the highest score may still have relatively low confidence.

Keeping these concepts separate improves explainability.

---

# 24. Explanation Generation

IssueScout attempts to explain every prediction.

Rather than returning only a numerical score, the system provides evidence that contributed to the prediction.

## Workflow

```
Prediction
      │
      ▼
Evidence Collection
      │
      ▼
Explanation Service
      │
      ▼
Explanation Builder
      │
      ▼
Human-readable Explanation
```

Typical explanation items include:

- explicit issue references
- matching commits
- shared reviewers
- similar titles
- matching labels
- timeline evidence

Explainability improves contributor trust and simplifies debugging.

---

# 25. Evaluation Pipeline

Evaluation measures prediction quality using known issue–pull request relationships.

## Workflow

```
Ground Truth Dataset
        │
        ▼
Evaluation Loader
        │
        ▼
Evaluation Runner
        │
        ▼
Comparison Results
        │
        ▼
Evaluation Pipeline
        │
        ▼
Evaluation Summary
```

The evaluation system is completely independent of GitHub.

It operates entirely on datasets.

---

# 26. Dataset Generation Pipeline

Datasets are generated directly from GitHub repositories.

## Workflow

```
Repository
      │
      ▼
Issue Service
      │
      ▼
Closed Issues
      │
      ▼
Ground Truth Collector
      │
      ▼
Repository Collector
      │
      ▼
Repository Evaluation
      │
      ▼
Exporter
      │
      ▼
Dataset
```

Datasets can later be reused for benchmarking without contacting GitHub again.

---

# 27. Benchmark Pipeline

Benchmarking evaluates IssueScout across one or more repositories.

## Workflow

```
Repository Evaluation
         │
         ▼
Evaluation Summary
         │
         ▼
Repository Benchmark
         │
         ▼
Benchmark Engine
         │
         ▼
Benchmark Suite
```

A benchmark suite aggregates results from multiple repositories.

This allows direct comparison of prediction quality across different projects.

---

# 28. Report Generation Pipeline

Evaluation reports provide a repository-wide summary.

## Workflow

```
Evaluation Summary
        │
        ▼
Repository Metrics
        │
        ▼
Evaluation Report
        │
        ▼
Console
JSON
Markdown
HTML (future)
PDF (future)
```

Reports are intentionally independent from presentation formats.

The same report object can be rendered into multiple output formats.

---

# 29. End-to-End System Workflow

The complete IssueScout execution flow is shown below.

```
GitHub Repository
        │
        ▼
GitHub Services
        │
        ▼
Scanner Engine
        │
        ▼
Candidate Generator
        │
        ▼
Relation Engine
        │
        ▼
Ranking
        │
        ▼
Confidence
        │
        ▼
Explanation
        │
        ▼
Prediction Result
        │
        ▼
Evaluation
        │
        ▼
Benchmark
        │
        ▼
Report
```

This pipeline demonstrates how all backend components cooperate while remaining modular and independently testable.

---

# 30. Repository Profiles

IssueScout is designed to operate across a wide variety of GitHub repositories without embedding repository-specific logic into the core prediction engine.

To achieve this, repository-specific behavior is encapsulated within repository profiles.

## Objectives

Repository profiles provide:

- repository metadata
- repository-specific defaults
- optional custom behavior
- future customization hooks

Current implementations include:

```
RepositoryProfile
      │
      ├──────────────┐
      ▼              ▼
GenericProfile   CPythonProfile
```

The `GenericProfile` serves as the default implementation for repositories that do not require custom behavior.

Repository-specific profiles can later customize:

- branch naming conventions
- label mappings
- issue templates
- repository heuristics
- detector weighting

without affecting the common prediction pipeline.

---

# 31. Extension Points

One of IssueScout's primary architectural goals is extensibility.

Developers should be able to introduce new functionality without modifying existing implementations.

## Supported Extension Points

### Repository Profiles

New repositories may provide specialized profiles.

Examples include:

- DjangoProfile
- KubernetesProfile
- RustProfile
- TensorFlowProfile

---

### Relation Detectors

Additional evidence sources can be introduced simply by implementing the detector interface.

Possible future detectors include:

- AI semantic similarity
- code ownership
- dependency graph analysis
- test coverage similarity
- file history similarity

---

### Scanner Analyzers

Additional repository analyzers can be added independently.

Examples:

- stale issue analyzer
- issue complexity analyzer
- newcomer issue analyzer
- documentation analyzer

---

### Evaluation Metrics

The evaluation framework supports adding new metrics without modifying the evaluation pipeline.

Potential additions include:

- F1 Score
- NDCG
- Top-K Accuracy
- Hit Rate
- Coverage

---

### Exporters

Future exporters may include:

- SQLite
- PostgreSQL
- HTML
- PDF
- Excel
- Parquet

---

# 32. Scalability

IssueScout is designed to scale from small repositories to very large projects.

## Candidate Reduction

Instead of comparing every issue against every pull request,

```
Issues × Pull Requests
```

the Candidate Generator reduces the search space before expensive relation analysis.

This significantly reduces computational cost.

---

## Parallel Repository Analysis

Independent issue analyses can execute concurrently.

This architecture allows future versions to leverage:

- asyncio
- multiprocessing
- distributed workers

without redesigning the prediction engine.

---

## Independent Pipelines

Prediction

Evaluation

Scanning

Benchmarking

remain independent.

Each subsystem may be optimized individually.

---

## Repository Independence

Supporting additional repositories does not require architectural changes.

Only repository-specific profiles may be introduced when necessary.

---

# 33. Performance Strategy

Performance is an important design consideration.

IssueScout applies several optimization techniques.

## Candidate Filtering

Only promising pull requests are evaluated.

This avoids unnecessary relation analysis.

---

## Lightweight Models

The project communicates through lightweight dataclasses and models.

Avoiding unnecessary mutable state reduces memory usage.

---

## Independent Relation Detectors

Each detector operates independently.

Future versions may evaluate detectors concurrently.

---

## Pipeline Separation

Scanning

Prediction

Evaluation

Benchmarking

can each be optimized independently.

---

## Future Caching

Future versions may introduce:

```
GitHub API

↓

Cache Layer

↓

Services

↓

Scanner
```

Possible cache implementations include:

- in-memory cache
- filesystem cache
- Redis
- SQLite

This will reduce GitHub API requests and improve performance.

---

# 34. Security Considerations

IssueScout follows several security principles.

## GitHub Authentication

Authentication tokens are supplied through environment variables.

Tokens are never hardcoded.

---

## Configuration

Sensitive configuration belongs in:

```
.env
```

rather than source code.

---

## Input Validation

API endpoints validate incoming requests before processing.

Invalid requests are rejected early.

---

## Error Isolation

Failures during scanning should not terminate unrelated analyses.

Individual component failures remain isolated whenever possible.

---

## Least Privilege

IssueScout primarily requires read-only access to GitHub repositories.

Future integrations should request only the permissions they require.

---

# 35. Configuration Architecture

Configuration is centralized.

```
Environment Variables
          │
          ▼
Settings
          │
          ▼
Services
          │
          ▼
Application Components
```

Examples include:

- GitHub token
- API endpoint
- request timeout
- retry policy
- default repository

Centralized configuration simplifies deployment.

---

# 36. Architectural Decisions

Several key design decisions influenced the architecture.

## Why FastAPI?

FastAPI provides:

- asynchronous request handling
- automatic documentation
- strong typing
- excellent performance

---

## Why Repository Profiles?

Different repositories may adopt different workflows.

Profiles isolate repository-specific behavior while preserving a universal prediction engine.

---

## Why Candidate Generation?

Evaluating every pull request would be computationally expensive.

Candidate generation dramatically reduces the search space.

---

## Why Separate Ranking?

Prediction scoring and ranking represent different responsibilities.

Keeping them independent allows future ranking algorithms without modifying relation analysis.

---

## Why Separate Evaluation?

Evaluation should remain independent of prediction.

This enables benchmarking of multiple prediction strategies using the same datasets.

---

## Why Explanation Generation?

Predictions without explanations are difficult to trust.

IssueScout provides transparent reasoning behind every prediction whenever possible.

---

# 37. Future Evolution

IssueScout is designed for long-term evolution.

## Version 1.x

Focus areas:

- backend stability
- benchmarking
- documentation
- contributor experience

---

## Version 2.x

Potential enhancements:

- machine learning ranking
- semantic embeddings
- advanced explanation engine
- incremental repository indexing

---

## Version 3.x

Long-term vision:

- multi-platform support
- GitLab
- Gitea
- Bitbucket
- enterprise deployments

---

## Research Directions

Potential future work includes:

- graph neural networks
- repository knowledge graphs
- developer recommendation systems
- automated issue assignment
- contributor onboarding

---

# 38. Glossary

## Candidate

A pull request selected for detailed relation analysis.

---

## Confidence

An estimate of prediction reliability.

---

## Evaluation

The process of measuring prediction quality against known ground truth.

---

## Ground Truth

The verified issue–pull request relationship used during evaluation.

---

## Issue

A GitHub issue representing a task, bug, or feature request.

---

## Prediction

The estimated relationship between an issue and a pull request.

---

## Pull Request

A proposed code contribution submitted through GitHub.

---

## Ranker

The component responsible for ordering prediction candidates.

---

## Relation Detector

A component that contributes evidence indicating whether an issue and pull request are related.

---

## Repository Profile

Repository-specific behavior isolated behind a common interface.

---

## Scanner

The subsystem responsible for discovering issues suitable for contributors.

---

# Conclusion

IssueScout has been designed as a modular, extensible, and repository-independent platform for analyzing GitHub repositories and predicting relationships between issues and pull requests.

The architecture emphasizes clear separation of responsibilities, strong typing, extensibility, and comprehensive evaluation. By isolating scanning, prediction, evaluation, benchmarking, and presentation into independent subsystems, the project remains maintainable while providing a solid foundation for future research and production use.

Future versions will continue to build upon this architecture by introducing advanced ranking techniques, richer repository analysis, improved benchmarking capabilities, and broader platform support while preserving the core architectural principles described in this document.
