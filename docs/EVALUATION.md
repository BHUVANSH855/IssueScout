# IssueScout Evaluation Documentation

**Version:** 1.0 (Draft)

**Last Updated:** July 2026

---

# Table of Contents

1. Introduction
2. Evaluation Overview
3. Objectives
4. Design Principles
5. Evaluation Architecture
6. Package Structure
7. Core Components
8. Dataset Generation
9. Dataset Builder
10. Dataset Models
11. Evaluation Pipeline
12. Design Summary

---

# 1. Introduction

The Evaluation subsystem measures the quality of IssueScout's prediction engine.

Unlike the Scanner and Prediction Engine, which operate on live GitHub repositories, the Evaluation subsystem operates on datasets containing verified issue–pull request relationships.

Evaluation allows developers to measure prediction quality objectively using reproducible benchmark datasets and standardized metrics.

The Evaluation subsystem has been designed to remain independent from prediction algorithms, allowing different prediction strategies to be evaluated using the same datasets.

---

# 2. Evaluation Overview

The Evaluation subsystem transforms repository data into measurable benchmark results.

```
GitHub Repository

↓

Dataset Generator

↓

Ground Truth Collection

↓

Repository Evaluation

↓

Evaluation Runner

↓

Comparison Results

↓

Metrics

↓

Benchmark

↓

Evaluation Report
```

Each stage performs a dedicated responsibility.

---

# 3. Evaluation Objectives

The Evaluation subsystem has several objectives.

## Prediction Validation

Measure how accurately IssueScout predicts issue–pull request relationships.

---

## Reproducibility

Ensure evaluation results can be reproduced using the same dataset.

---

## Benchmarking

Compare IssueScout performance across multiple repositories.

---

## Explainability

Produce measurable metrics rather than subjective observations.

---

## Repository Independence

Support evaluation for any GitHub repository.

---

## Extensibility

Allow future contributors to add:

- metrics
- exporters
- benchmark formats
- dataset formats

without modifying the evaluation pipeline.

---

# 4. Design Principles

The Evaluation subsystem follows several engineering principles.

---

## Separation of Concerns

Evaluation does not perform prediction.

Prediction produces results.

Evaluation measures those results.

---

## Reproducibility

Given the same dataset, IssueScout should always produce identical evaluation metrics.

---

## Modularity

Dataset generation

↓

Evaluation

↓

Benchmarking

↓

Reporting

are independent subsystems.

---

## Extensibility

Future metrics and benchmark formats should require extension rather than modification.

---

## Strong Typing

Evaluation communicates using shared models.

Examples include:

- EvaluationRecord

- RepositoryEvaluation

- PredictionCandidate

- GroundTruthRecord

---

# 5. Evaluation Architecture

```
              Evaluation

                    │

      ┌─────────────┼──────────────┐

      ▼             ▼              ▼

 Dataset      Evaluation      Benchmark

 Generator       Runner         Engine

      │             │

      └─────────────┼──────────────┐

                    ▼

             Evaluation Metrics

                    │

                    ▼

             Evaluation Report
```

Each subsystem performs one responsibility.

---

# 6. Package Structure

```
evaluation/

├── benchmark/

├── collector/

├── comparison/

├── dataset/

├── metrics/

├── exporter.py

├── loader.py

├── pipeline.py

├── report.py

├── runner.py
```

The package is organized around the evaluation workflow.

---

# 7. Core Components

| Component | Responsibility |
|-----------|----------------|
| DatasetGenerator | Build datasets |
| DatasetBuilder | Construct repository datasets |
| GroundTruthCollector | Collect verified relationships |
| EvaluationLoader | Load datasets |
| EvaluationRunner | Compare predictions |
| EvaluationPipeline | Compute metrics |
| EvaluationSummaryMetric | Aggregate metrics |
| BenchmarkEngine | Build benchmark suites |
| EvaluationExporter | Export evaluation data |
| EvaluationReport | Store benchmark results |

---

# 8. Dataset Generation

Datasets are generated directly from GitHub repositories.

Workflow:

```
Repository

↓

Closed Issues

↓

Ground Truth Collector

↓

Repository Collector

↓

Repository Evaluation
```

Only verified issue–pull request relationships become part of the dataset.

This ensures reliable evaluation.

---

## Responsibilities

Dataset generation should:

- retrieve closed issues
- identify linked pull requests
- construct ground truth
- build repository datasets

Dataset generation should not:

- predict relationships
- benchmark results
- rank pull requests

---

# 9. Dataset Builder

DatasetBuilder constructs RepositoryEvaluation objects incrementally.

Responsibilities include:

- storing evaluation records
- maintaining repository information
- producing completed datasets

The builder isolates dataset construction from collection.

---

# 10. Dataset Models

Evaluation communicates through strongly typed models.

Typical workflow:

```
GroundTruthRecord

↓

PredictionCandidate

↓

EvaluationRecord

↓

RepositoryEvaluation

↓

BenchmarkSuite
```

These models provide stable interfaces across the Evaluation subsystem.

---

# 11. Evaluation Pipeline

The overall evaluation workflow is summarized below.

```
Dataset

↓

Evaluation Loader

↓

Evaluation Runner

↓

Comparison Results

↓

Metrics

↓

Evaluation Summary

↓

Benchmark

↓

Report
```

This pipeline transforms datasets into measurable benchmark statistics.

---

# 12. Design Summary

The Evaluation subsystem emphasizes:

- reproducibility
- modularity
- extensibility
- benchmarking
- deterministic execution

By separating dataset generation, evaluation, benchmarking, and reporting into independent components, IssueScout provides a robust framework for measuring prediction quality.

---

# 13. Ground Truth Collection

Ground truth represents the verified relationship between an issue and the pull request that resolved it.

Ground truth forms the foundation of every evaluation dataset.

Without reliable ground truth, evaluation metrics become meaningless.

---

## Workflow

```
Closed Issue

↓

Timeline Events

↓

Linked Pull Request

↓

GroundTruthRecord
```

Ground truth should only contain verified relationships.

---

## Responsibilities

The Ground Truth Collector should:

- retrieve timeline events
- identify linked pull requests
- determine linkage method
- build GroundTruthRecord objects

It should never perform prediction.

---

# 14. Repository Collector

RepositoryCollector converts multiple ground truth records into a repository-level evaluation dataset.

```
GroundTruthRecord

↓

RepositoryCollector

↓

RepositoryEvaluation
```

Responsibilities include:

- collecting evaluation records
- storing repository metadata
- constructing RepositoryEvaluation

---

# 15. Evaluation Loader

EvaluationLoader reads datasets from storage.

Current supported format:

- JSON

Future formats may include:

- CSV
- SQLite
- PostgreSQL
- Remote APIs

The loader converts external formats into internal models.

---

## Benefits

Keeping loading separate provides:

- reusable datasets
- format independence
- easier testing

---

# 16. Evaluation Runner

EvaluationRunner compares predictions against ground truth.

```
EvaluationRecord

↓

EvaluationComparator

↓

ComparisonResult
```

Responsibilities include:

- executing comparisons
- collecting comparison results
- remaining independent from metric computation

The runner should not compute statistics.

---

# 17. Comparison Engine

The Comparison Engine determines whether IssueScout's predictions match the verified solution.

Typical comparison considers:

- predicted pull request
- actual pull request
- prediction rank
- prediction score

The output is a ComparisonResult.

---

## Responsibilities

The Comparison Engine should:

- compare predictions
- determine matches
- preserve ranking information
- remain deterministic

---

# 18. Metric Computation

Metrics transform comparison results into measurable statistics.

```
Comparison Results

↓

Metric

↓

Numerical Score
```

Each metric evaluates one aspect of prediction quality.

Metrics remain completely independent.

---

# 19. Current Metrics

IssueScout currently computes:

---

## Accuracy

Measures the percentage of correct predictions.

---

## Precision

Measures prediction correctness among returned results.

---

## Recall

Measures how many true relationships were successfully identified.

---

## Mean Reciprocal Rank (MRR)

Measures how highly the correct prediction appears within ranked results.

---

## Mean Average Precision (MAP)

Measures ranking quality across all evaluated issues.

---

## Evaluation Summary

EvaluationSummary aggregates all metrics into one object.

Typical contents include:

- issue count
- accuracy
- precision
- recall
- MRR
- MAP

---

# 20. Evaluation Pipeline

EvaluationPipeline coordinates metric computation.

```
Comparison Results

↓

Accuracy

↓

Precision

↓

Recall

↓

MRR

↓

MAP

↓

Evaluation Summary
```

The pipeline itself contains minimal business logic.

Metric implementations remain independent.

---

# 21. Benchmark Engine

BenchmarkEngine aggregates evaluation results from multiple repositories.

```
Repository Benchmark

↓

Benchmark Engine

↓

Benchmark Suite
```

Benchmarking enables repository-to-repository comparisons.

---

## Responsibilities

BenchmarkEngine should:

- aggregate repository benchmarks
- build benchmark suites
- remain independent from evaluation

---

# 22. Benchmark Suite

BenchmarkSuite stores evaluation results for multiple repositories.

Typical contents include:

- repository benchmarks
- summary statistics
- aggregate metrics

Future versions may support benchmark history.

---

# 23. Exporters

EvaluationExporter converts evaluation results into external formats.

Current supported formats:

- CSV
- JSON

Future exporters may include:

- Markdown
- HTML
- PDF
- Excel

Exporters should never modify evaluation data.

---

# 24. Evaluation Report

EvaluationReport stores the final benchmark information.

Typical contents include:

- repository
- metrics
- failures
- metadata

The report remains independent from presentation.

---

# 25. Repository Metrics

RepositoryMetrics summarizes evaluation quality for one repository.

Typical metrics include:

- Top-1 Accuracy
- Top-3 Accuracy
- Top-5 Accuracy
- Precision@1
- Precision@3
- Precision@5
- Recall@1
- Recall@3
- Recall@5
- Mean Reciprocal Rank
- Mean Average Precision
- F1 Score
- Average Prediction Score

These metrics provide a comprehensive view of prediction quality.

---

# 26. Evaluation Failures

EvaluationFailure records incorrect predictions.

Typical information includes:

- issue number
- expected pull request
- predicted pull request
- prediction rank
- prediction score
- failure reason

Failure analysis helps identify weaknesses in prediction algorithms.

---

# 27. Evaluation Execution Sequence

The complete evaluation workflow is illustrated below.

```
Repository

↓

Dataset Generator

↓

Ground Truth

↓

Repository Evaluation

↓

Evaluation Runner

↓

Comparison Results

↓

Metrics

↓

Evaluation Summary

↓

Benchmark

↓

Report
```

Each stage performs one clearly defined responsibility.

---

# 28. Evaluation Responsibilities

The Evaluation subsystem is responsible for:

✔ Building datasets

✔ Loading datasets

✔ Comparing predictions

✔ Computing metrics

✔ Benchmarking repositories

✔ Exporting evaluation results

✔ Producing evaluation reports

The Evaluation subsystem is **not** responsible for:

✘ Repository scanning

✘ Pull request prediction

✘ GitHub communication

✘ REST API handling

Those responsibilities belong to other backend subsystems.

---

# 29. Extension Guide

The Evaluation subsystem has been designed to evolve independently of the prediction engine.

Most future improvements should be implemented by extending existing components rather than modifying the evaluation workflow.

Primary extension points include:

- Dataset Generation
- Dataset Formats
- Metrics
- Benchmarking
- Exporters
- Reports

This approach preserves backward compatibility while encouraging experimentation.

---

# 30. Adding a New Metric

Evaluation metrics should remain independent.

Typical implementation workflow:

```
Requirement

↓

Design Metric

↓

Implement Metric

↓

Unit Tests

↓

Register Metric

↓

Documentation
```

Each metric should compute one measurable statistic.

---

## Examples of Future Metrics

Potential additions include:

- Normalized Discounted Cumulative Gain (NDCG)
- Hit Rate
- Coverage
- Success Rate
- Top-K Recall
- Ranking Consistency
- Confidence Calibration

Adding a metric should not require modifications to existing metric implementations.

---

# 31. Adding a New Dataset Format

Datasets are intentionally separated from evaluation logic.

Current format:

- JSON

Possible future formats:

- CSV
- SQLite
- PostgreSQL
- Apache Parquet
- Remote Dataset Service

Only the EvaluationLoader should require extension.

The remainder of the evaluation pipeline should remain unchanged.

---

# 32. Extending Benchmarking

Benchmarking is responsible for comparing repository-level performance.

Future benchmark capabilities may include:

- repository groups
- historical benchmark tracking
- benchmark trends
- cross-version comparisons
- leaderboard generation

BenchmarkEngine should remain independent from metric computation.

---

# 33. Extending Exporters

EvaluationExporter converts evaluation data into external formats.

Current exporters include:

- CSV
- JSON

Future exporters may include:

- Markdown
- HTML
- PDF
- Microsoft Excel
- Interactive dashboards

Exporters should never modify evaluation results.

They should only transform data into presentation formats.

---

# 34. Performance Considerations

Evaluation datasets can become large when benchmarking multiple repositories.

Performance recommendations include:

- reuse loaded datasets
- avoid repeated comparisons
- minimize unnecessary allocations
- keep metrics independent
- reuse shared models

Future optimization opportunities include:

- parallel metric computation
- incremental benchmarking
- cached datasets

Performance improvements should preserve deterministic evaluation.

---

# 35. Testing Strategy

Every evaluation component should include automated tests.

---

## Unit Tests

Examples include:

- DatasetBuilder
- DatasetGenerator
- EvaluationLoader
- EvaluationRunner
- EvaluationPipeline
- BenchmarkEngine
- EvaluationExporter
- Individual metrics

Each test should verify one behavior.

---

## Integration Tests

Integration tests verify cooperation between:

- Dataset Generation
- Evaluation Runner
- Metric Pipeline
- Benchmark Engine
- Exporters

---

## Regression Tests

Whenever an evaluation bug is corrected, a regression test should be added.

Regression tests prevent previously resolved issues from reappearing.

---

# 36. Debugging Guide

When evaluation results appear incorrect, investigate in the following order:

1. Verify dataset generation.
2. Verify ground truth.
3. Verify EvaluationLoader.
4. Verify EvaluationRunner.
5. Verify ComparisonResult.
6. Verify metric computation.
7. Verify benchmark generation.
8. Verify exported report.

This progression isolates problems efficiently.

---

# 37. Logging Strategy

Recommended evaluation log events include:

- dataset generation started
- dataset loaded
- repository evaluated
- comparison completed
- metric computed
- benchmark generated
- exporter completed
- evaluation finished

Logs should emphasize operational information.

Sensitive credentials should never appear in logs.

---

# 38. Common Pitfalls

Contributors should avoid:

- modifying datasets during evaluation
- embedding prediction logic inside evaluation
- combining multiple metrics into one implementation
- duplicating comparison logic
- bypassing shared evaluation models

Maintaining subsystem boundaries improves maintainability.

---

# 39. Best Practices

When extending the Evaluation subsystem:

Prefer:

- small focused metrics
- reusable models
- deterministic algorithms
- isolated benchmark logic
- comprehensive automated tests

Avoid:

- hidden side effects
- duplicated calculations
- unnecessary coupling
- repository-specific evaluation behavior

---

# 40. Future Enhancements

Potential future improvements include:

## Dataset Generation

- incremental dataset updates
- scheduled dataset refresh
- dataset versioning

---

## Evaluation

- confidence calibration analysis
- error categorization
- detector contribution analysis

---

## Benchmarking

- historical comparisons
- repository leaderboards
- benchmark dashboards

---

## Reporting

- HTML reports
- PDF reports
- interactive visualizations
- trend analysis

---

# 41. Evaluation Development Workflow

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

Following this workflow helps ensure reliable and reproducible evaluation results.

---

# 42. Relationship to Other Subsystems

The Evaluation subsystem operates after prediction.

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

Evaluation consumes prediction outputs but remains independent from prediction implementation.

---

# 43. Maintenance Guidelines

Long-term maintenance should focus on:

- improving dataset quality
- expanding metric coverage
- increasing benchmark reliability
- improving exporter support
- maintaining deterministic behavior
- updating documentation

Changes should preserve compatibility whenever practical.

---

# 44. Conclusion

The Evaluation subsystem provides an objective framework for measuring the effectiveness of IssueScout's prediction engine.

By separating dataset generation, comparison, metric computation, benchmarking, exporting, and reporting into independent components, the subsystem remains modular, extensible, and reproducible.

This architecture enables future contributors to introduce new metrics, benchmark strategies, and reporting formats without disrupting existing evaluation workflows.

---

# References

See also:

- `ARCHITECTURE.md`
- `BACKEND.md`
- `SCANNER.md`
- `PREDICTION_ENGINE.md`
- Source code documentation
- Inline code comments

---

**End of Document**
