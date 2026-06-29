from .author_similarity import AuthorSimilarityAnalyzer
from .body_reference import BodyReferenceAnalyzer
from .branch_similarity import BranchSimilarityAnalyzer
from .comment_reference import CommentReferenceAnalyzer
from .commit_history_similarity import (
    CommitHistorySimilarityAnalyzer,
)
from .commit_message_reference import (
    CommitMessageReferenceAnalyzer,
)
from .commit_reference import CommitReferenceAnalyzer
from .file_similarity import FileSimilarityAnalyzer
from .label_similarity import LabelSimilarityAnalyzer
from .reviewer_similarity import ReviewerSimilarityAnalyzer
from .timeline_reference import TimelineReferenceAnalyzer
from .title_similarity import TitleSimilarityAnalyzer
from .metadata_similarity import (
    MetadataSimilarityAnalyzer,
)


def default_analyzers():
    """
    Return the default analyzer pipeline.

    The order matters:
    explicit evidence first,
    heuristic evidence second.
    """

    return [
        TimelineReferenceAnalyzer(),
        CommitReferenceAnalyzer(),
        CommentReferenceAnalyzer(),
        BodyReferenceAnalyzer(),
        CommitMessageReferenceAnalyzer(),
        BranchSimilarityAnalyzer(),
        TitleSimilarityAnalyzer(),
        CommitHistorySimilarityAnalyzer(),
        LabelSimilarityAnalyzer(),
        AuthorSimilarityAnalyzer(),
        MetadataSimilarityAnalyzer(),
        FileSimilarityAnalyzer(),
        ReviewerSimilarityAnalyzer(),
    ]
