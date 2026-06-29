from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class AnalyzerExplanation:
    """
    Human-friendly metadata describing an analyzer.
    """

    title: str

    category: str

    description: str


EXPLANATION_METADATA = {
    "timeline_reference": AnalyzerExplanation(
        title="Timeline Reference",
        category="Explicit Evidence",
        description="The issue timeline explicitly references the pull request.",
    ),
    "commit_reference": AnalyzerExplanation(
        title="Commit Reference",
        category="Explicit Evidence",
        description="A commit associated with the pull request references the issue.",
    ),
    "comment_reference": AnalyzerExplanation(
        title="Comment Reference",
        category="Explicit Evidence",
        description="Issue comments reference the pull request.",
    ),
    "body_reference": AnalyzerExplanation(
        title="Body Reference",
        category="Explicit Evidence",
        description="The pull request description references the issue.",
    ),
    "commit_message_reference": AnalyzerExplanation(
        title="Commit Message",
        category="Explicit Evidence",
        description="A commit message references the issue.",
    ),
    "branch_similarity": AnalyzerExplanation(
        title="Branch Name",
        category="Strong Signal",
        description="The branch name contains the issue identifier.",
    ),
    "title_similarity": AnalyzerExplanation(
        title="Title Similarity",
        category="Similarity",
        description="Issue and pull request titles are similar.",
    ),
    "commit_history_similarity": AnalyzerExplanation(
        title="Commit History",
        category="Similarity",
        description="Historical commit messages resemble the issue title.",
    ),
    "label_similarity": AnalyzerExplanation(
        title="Label Similarity",
        category="Similarity",
        description="Issue and pull request share labels.",
    ),
    "author_similarity": AnalyzerExplanation(
        title="Author Match",
        category="Metadata",
        description="The issue and pull request have the same author.",
    ),
    "metadata_similarity": AnalyzerExplanation(
        title="Metadata",
        category="Metadata",
        description="Issue and pull request metadata are related.",
    ),
    "file_similarity": AnalyzerExplanation(
        title="Changed Files",
        category="Similarity",
        description="Files mentioned in the issue overlap with files changed by the pull request.",
    ),
    "reviewer_similarity": AnalyzerExplanation(
        title="Reviewer Match",
        category="Metadata",
        description="The same reviewers are involved.",
    ),
}
