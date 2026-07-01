# IssueScout Prediction Engine Documentation

**Version:** 1.0 (Draft)

**Last Updated:** July 2026

---

# Table of Contents

1. Introduction
2. Prediction Engine Overview
3. Prediction Objectives
4. Design Principles
5. Prediction Architecture
6. Package Structure
7. Prediction Components
8. Prediction Service
9. Candidate Generator
10. Prediction Lifecycle
11. Prediction Models
12. Prediction Pipeline
13. Design Summary

---

# 1. Introduction

The Prediction Engine is the core intelligence of IssueScout.

Its responsibility is to determine which pull request most likely resolves a given GitHub issue.

Unlike traditional approaches that rely only on explicit GitHub links, IssueScout combines multiple independent sources of evidence to estimate issue–pull request relationships.

The Prediction Engine consumes repository data collected by the Scanner subsystem and produces ranked predictions with confidence estimates and human-readable explanations.

Prediction remains completely independent from:

- repository scanning
- evaluation
- benchmarking
- presentation

This separation allows prediction algorithms to evolve without affecting other backend components.

---

# 2. Prediction Engine Overview

The prediction workflow consists of several stages.

```
Issue

↓

Candidate Generator

↓

Candidate Pull Requests

↓

Relation Engine

↓

Relation Predictions

↓

Ranker

↓

Best Prediction

↓

Confidence Service

↓

Explanation Service

↓

Prediction Result
```

Each stage performs one focused responsibility.

---

# 3. Prediction Objectives

The Prediction Engine has several major objectives.

## Relationship Prediction

Estimate which pull request resolves an issue.

---

## Ranking

Order candidate pull requests from most likely to least likely.

---

## Explainability

Provide evidence supporting every prediction whenever possible.

---

## Confidence Estimation

Estimate the reliability of the predicted relationship.

---

## Repository Independence

Support prediction across different GitHub repositories without embedding repository-specific logic.

---

## Extensibility

Allow contributors to add:

- relation detectors
- ranking algorithms
- explanation generators
- confidence strategies

without modifying existing prediction components.

---

# 4. Design Principles

The prediction subsystem follows the same engineering principles as the rest of IssueScout.

---

## Single Responsibility

Each prediction component has one clearly defined responsibility.

Examples:

CandidateGenerator

↓

Select promising pull requests

---

RelationEngine

↓

Analyze relationships

---

Ranker

↓

Sort predictions

---

ConfidenceService

↓

Estimate reliability

---

ExplanationService

↓

Generate evidence

---

PredictionService

↓

Coordinate the complete prediction workflow

---

## Separation of Concerns

Prediction is divided into independent stages.

No stage should duplicate the responsibility of another.

---

## Extensibility

New prediction strategies should be introduced through extension rather than modification.

Future contributors should be able to add:

- new detectors
- new ranking algorithms
- new explanation builders

without changing the prediction workflow.

---

## Explainability

Predictions should not consist only of scores.

IssueScout attempts to explain why a prediction was produced.

This improves transparency and contributor trust.

---

# 5. Prediction Architecture

The Prediction Engine coordinates multiple specialized components.

```
                 Prediction Service

                        │

       ┌────────────────┼────────────────┐

       ▼                ▼                ▼

Candidate Generator   Relation Engine   Ranker

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

PredictionService acts as the orchestrator while individual components remain focused.

---

# 6. Package Structure

```
prediction/

├── analysis_service.py

├── candidate_generator.py

├── confidence_service.py

├── explanation_builder.py

├── explanation_service.py

├── prediction_service.py
```

Each module contributes one stage of the prediction process.

---

# 7. Prediction Components

The prediction subsystem consists of the following major components.

| Component | Responsibility |
|------------|----------------|
| PredictionService | Coordinates prediction |
| CandidateGenerator | Filters pull requests |
| AnalysisService | Executes relation analysis |
| RelationEngine | Computes relationship scores |
| Ranker | Sorts predictions |
| ConfidenceService | Computes confidence |
| ExplanationService | Produces explanation items |
| ExplanationBuilder | Formats explanations |

Each component is independently testable.

---

# 8. Prediction Service

PredictionService is the entry point for prediction.

It coordinates all prediction stages.

Typical workflow:

```
Issue

↓

Candidate Generator

↓

Relation Analysis

↓

Ranking

↓

Confidence

↓

Explanation

↓

Prediction Result
```

PredictionService intentionally contains orchestration logic rather than detector implementations.

---

## Responsibilities

PredictionService should:

- generate candidates
- invoke relation analysis
- rank predictions
- compute confidence
- generate explanations
- produce PredictionResult

PredictionService should not:

- communicate with GitHub directly
- perform repository scanning
- benchmark predictions
- evaluate prediction quality

---

# 9. Candidate Generator

Evaluating every pull request in a repository would be computationally expensive.

CandidateGenerator reduces the search space before expensive relation analysis begins.

Current heuristics include:

- shared author
- explicit issue references
- title similarity
- branch naming conventions
- creation timestamps
- shared labels

Only promising pull requests proceed to the Relation Engine.

---

## Benefits

Candidate generation provides:

- lower computation cost
- faster execution
- improved scalability
- reduced detector workload

Future heuristics can be added independently.

---

# 10. Prediction Lifecycle

The complete prediction lifecycle is illustrated below.

```
Issue

↓

Candidate Generator

↓

Candidate Pull Requests

↓

Relation Analysis

↓

Ranking

↓

Confidence

↓

Explanation

↓

Prediction Result
```

Each stage consumes the output of the previous stage.

---

# 11. Prediction Models

Prediction communicates using strongly typed models.

Typical models include:

```
Issue

↓

PullRequest

↓

RelationPrediction

↓

PredictionResult
```

These models provide stable interfaces between prediction components.

---

# 12. Prediction Pipeline

The overall prediction pipeline is summarized below.

```
Issue
   │
   ▼
Candidate Generator
   │
   ▼
Relation Engine
   │
   ▼
Ranker
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

This pipeline forms the foundation of the IssueScout prediction subsystem.

---

# 13. Design Summary

The Prediction Engine has been designed around several core principles:

- modularity
- explainability
- extensibility
- repository independence
- deterministic execution
- strong typing

By separating candidate generation, relation analysis, ranking, confidence estimation, and explanation generation into independent components, IssueScout provides a prediction architecture that is maintainable, testable, and suitable for future enhancements.

---

# 14. Relation Engine

The Relation Engine is responsible for determining how strongly a pull request is related to an issue.

Rather than relying on a single heuristic, the Relation Engine combines evidence from multiple independent detectors.

Each detector contributes a score representing one aspect of the relationship.

The combined evidence forms the final relation score.

---

## High-Level Workflow

```
Issue
   │
   ▼
Candidate Pull Request
   │
   ▼
Relation Engine
   │
   ▼
Relation Detectors
   │
   ▼
Evidence Results
   │
   ▼
Combined Relation Score
```

The Relation Engine itself does not know how evidence is produced.

It delegates that responsibility to registered detectors.

---

# 15. Detector Registry

The Relation Engine uses a detector registry.

The registry manages all available relation detectors.

```
Relation Engine

        │

        ▼

Detector Registry

        │

 ┌──────┼────────┬─────────┐

 ▼      ▼        ▼         ▼

Detector A

Detector B

Detector C

Detector N
```

The engine simply executes every registered detector.

This architecture allows new detectors to be added without modifying the engine.

---

## Advantages

The registry provides:

- modularity
- extensibility
- low coupling
- independent testing

Future contributors only need to register a detector.

The engine remains unchanged.

---

# 16. Relation Detectors

Each detector evaluates one source of evidence.

Examples include:

- Title Similarity
- Body Reference
- Comment Reference
- Commit Reference
- Commit Message Reference
- Commit History Similarity
- Branch Similarity
- Reviewer Similarity
- Label Similarity
- Metadata Similarity
- Timeline Reference
- File Similarity

Each detector returns an independent result.

---

## Detector Responsibilities

A detector should:

- inspect one source of evidence
- compute a score
- provide evidence details
- remain deterministic

A detector should not:

- rank predictions
- estimate confidence
- communicate with GitHub directly
- modify repository models

---

# 17. Detector Execution

For every candidate pull request, detectors execute independently.

```
Candidate Pull Request

        │

        ▼

Detector 1

        │

Detector 2

        │

Detector 3

        │

Detector N

        │

        ▼

Evidence Results
```

Each detector contributes its own score.

No detector depends on another detector.

---

## Failure Isolation

If one detector encounters an unexpected error:

- remaining detectors continue execution
- evidence already collected is preserved
- prediction continues whenever possible

This improves robustness.

---

# 18. Evidence Collection

Evidence produced by detectors is collected into a single prediction.

Typical evidence includes:

- matching issue numbers
- commit references
- reviewer overlap
- branch names
- labels
- timeline events
- title similarity
- commit history

Evidence remains available for explanation generation.

---

# 19. Relation Scoring

After detector execution, the Relation Engine combines detector scores.

```
Detector Results

      │

      ▼

Score Aggregation

      │

      ▼

Relation Score
```

The relation score represents the overall strength of the relationship between an issue and a pull request.

---

## Characteristics

Relation scores should be:

- deterministic
- reproducible
- explainable
- independent of ranking

---

# 20. Ranking

After relation scores are computed, predictions are sorted.

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

Ranking determines ordering only.

It does not modify relation scores.

---

## Responsibilities

The Ranker should:

- sort predictions
- identify the highest ranked prediction
- provide deterministic ordering

The Ranker should not:

- calculate evidence
- estimate confidence
- generate explanations

---

# 21. Confidence Service

Confidence estimation occurs after ranking.

```
Best Prediction

       │

       ▼

Confidence Service

       │

       ▼

Confidence Score
```

Confidence estimates how reliable the prediction appears.

A high-scoring prediction is not necessarily a high-confidence prediction.

Keeping confidence separate improves transparency.

---

# 22. Explanation Service

Predictions should be understandable.

IssueScout therefore produces explanations describing why a prediction was selected.

```
Prediction

      │

      ▼

Evidence

      │

      ▼

Explanation Service

      │

      ▼

Explanation Items
```

Explanation items summarize evidence rather than raw detector output.

---

# 23. Explanation Builder

The Explanation Builder converts explanation items into user-facing output.

```
Explanation Items

        │

        ▼

Explanation Builder

        │

        ▼

Formatted Explanation
```

Future output formats may include:

- Console
- Markdown
- HTML
- PDF

The builder is presentation-focused.

It does not perform relation analysis.

---

# 24. Prediction Result

The final output of the Prediction Engine is a PredictionResult.

A PredictionResult typically contains:

- issue number
- ranked predictions
- best prediction
- confidence
- explanation
- evidence
- acceptance status

This object forms the public interface of the prediction subsystem.

---

# 25. Prediction Execution Sequence

The complete prediction sequence is illustrated below.

```
Issue

↓

Candidate Generator

↓

Candidate Pull Requests

↓

Relation Engine

↓

Relation Detectors

↓

Evidence Results

↓

Relation Score

↓

Ranker

↓

Best Prediction

↓

Confidence Service

↓

Explanation Service

↓

Prediction Result
```

Every stage has one clearly defined responsibility.

---

# 26. Prediction Responsibilities

The Prediction Engine is responsible for:

✔ Selecting candidate pull requests

✔ Evaluating relationships

✔ Ranking predictions

✔ Estimating confidence

✔ Producing explanations

✔ Returning prediction results

The Prediction Engine is **not** responsible for:

✘ Repository scanning

✘ GitHub communication

✘ Benchmarking

✘ Evaluation

✘ Report generation

Those responsibilities belong to other backend subsystems.

---

# 27. Extension Guide

The Prediction Engine has been designed to support long-term evolution without requiring major architectural changes.

Most enhancements should be implemented by extending existing components rather than modifying them.

The primary extension points are:

- Candidate Generation
- Relation Detectors
- Ranking
- Confidence Estimation
- Explanation Generation

---

# 28. Adding a New Relation Detector

New relation detectors are the preferred mechanism for improving prediction quality.

Typical development workflow:

```
Requirement

↓

Design Detector

↓

Implement Detector

↓

Register Detector

↓

Unit Tests

↓

Integration Tests

↓

Documentation
```

Every detector should evaluate one source of evidence only.

Examples of future detectors include:

- Semantic Similarity Detector
- Code Ownership Detector
- Dependency Graph Detector
- Test Coverage Detector
- Release Note Detector

---

## Detector Checklist

A detector should:

✔ Evaluate one evidence source

✔ Return deterministic scores

✔ Provide explanation evidence

✔ Remain independently testable

A detector should not:

✘ Perform ranking

✘ Modify models

✘ Fetch GitHub data directly

✘ Generate explanations

---

# 29. Adding Candidate Generation Rules

Candidate generation is intentionally lightweight.

Future heuristics may include:

- milestone matching
- release matching
- component ownership
- contributor history
- repository conventions

New heuristics should reduce the search space while minimizing false negatives.

---

# 30. Adding a New Ranking Strategy

Ranking algorithms are isolated inside the Ranker.

Possible future implementations include:

- weighted ranking
- learning-to-rank
- graph-based ranking
- semantic ranking
- machine learning ranking

Development steps:

1. Implement ranking algorithm.
2. Add tests.
3. Preserve public Ranker interface.
4. Update documentation.

---

# 31. Extending Confidence Estimation

Confidence should remain independent from relation scoring.

Possible future confidence factors include:

- detector agreement
- evidence diversity
- repository maturity
- historical prediction accuracy
- contributor activity

Confidence should remain explainable and reproducible.

---

# 32. Extending Explanation Generation

Explanations help users understand prediction decisions.

Future explanation improvements may include:

- grouped evidence
- evidence weighting
- visual summaries
- Markdown reports
- HTML reports

Explanation generation should remain presentation-oriented.

---

# 33. Performance Considerations

Prediction performance is important for repositories containing thousands of pull requests.

Current optimization techniques include:

- candidate filtering
- detector independence
- lightweight models
- pipeline separation

Future optimizations may include:

- detector parallelization
- cached similarity calculations
- incremental prediction
- repository caching

Performance improvements should preserve deterministic behavior.

---

# 34. Testing Strategy

Every prediction component should include automated tests.

---

## Unit Tests

Examples:

- CandidateGenerator
- Ranker
- ConfidenceService
- ExplanationService
- Individual relation detectors

Each test should verify one behavior.

---

## Integration Tests

Verify cooperation between:

- PredictionService
- RelationEngine
- Ranker
- ConfidenceService
- ExplanationBuilder

---

## Regression Tests

Whenever a prediction bug is fixed, a regression test should be added.

This prevents future regressions.

---

# 35. Debugging Guide

When prediction results appear incorrect, investigate in the following order:

1. Verify candidate generation.
2. Verify detector execution.
3. Inspect detector scores.
4. Verify score aggregation.
5. Verify ranking.
6. Verify confidence calculation.
7. Verify generated explanation.
8. Verify PredictionResult.

This approach narrows problems efficiently.

---

# 36. Logging Strategy

Useful prediction logs include:

- prediction started
- candidate count
- detector execution
- detector scores
- ranking completed
- confidence calculated
- explanation generated
- prediction completed

Logs should never expose sensitive credentials.

---

# 37. Common Pitfalls

Contributors should avoid:

- bypassing CandidateGenerator
- mixing detector responsibilities
- embedding GitHub requests inside detectors
- combining ranking with scoring
- coupling explanations to detector implementations
- introducing repository-specific logic into generic prediction code

Maintaining separation of concerns keeps the subsystem extensible.

---

# 38. Best Practices

When implementing prediction features:

Prefer:

- small focused detectors
- reusable models
- deterministic algorithms
- clear evidence collection
- extensive automated tests

Avoid:

- duplicated heuristics
- hidden side effects
- unnecessary complexity
- tightly coupled components

---

# 39. Future Enhancements

Potential future improvements include:

## Candidate Generation

- semantic pre-filtering
- repository-specific heuristics
- contributor history

---

## Relation Analysis

- transformer embeddings
- graph-based analysis
- repository knowledge graphs
- code ownership signals

---

## Ranking

- adaptive weighting
- learning-to-rank
- historical accuracy feedback

---

## Explainability

- interactive explanations
- visual evidence graphs
- detector contribution summaries

---

# 40. Prediction Development Workflow

```
Requirement
      │
      ▼
Design
      │
      ▼
Implementation
      │
      ▼
Unit Tests
      │
      ▼
Integration Tests
      │
      ▼
Documentation
      │
      ▼
Ruff Check
      │
      ▼
Pytest
      │
      ▼
Code Review
      │
      ▼
Merge
```

Following this workflow helps maintain reliability and architectural consistency.

---

# 41. Relationship to Other Subsystems

The Prediction Engine operates after repository scanning.

```
GitHub Repository
        │
        ▼
Scanner
        │
        ▼
Prediction Engine
        │
        ▼
Evaluation
        │
        ▼
Benchmark
        │
        ▼
Reports
```

Prediction consumes repository information but remains independent from evaluation and reporting.

---

# 42. Conclusion

The Prediction Engine is the core analytical subsystem of IssueScout.

By separating candidate generation, relation analysis, ranking, confidence estimation, and explanation generation into independent components, the system remains modular, extensible, and maintainable.

This architecture allows future contributors to improve prediction quality through new detectors, ranking strategies, and explanation techniques without disrupting the existing prediction workflow.

---

# References

See also:

- `ARCHITECTURE.md`
- `BACKEND.md`
- `SCANNER.md`
- `EVALUATION.md`
- Source code documentation
- Inline code comments

---

**End of Document**
