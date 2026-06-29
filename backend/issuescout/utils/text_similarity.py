import re
from difflib import SequenceMatcher


def _normalize(text: str) -> str:
    return re.sub(
        r"\s+",
        " ",
        (text or "").strip().lower(),
    )


def _token_similarity(
    left: str,
    right: str,
) -> float:
    left_tokens = set(left.split())
    right_tokens = set(right.split())

    if not left_tokens and not right_tokens:
        return 1.0

    if not left_tokens or not right_tokens:
        return 0.0

    intersection = len(left_tokens & right_tokens)
    union = len(left_tokens | right_tokens)

    return intersection / union


def similarity_percentage(
    left: str,
    right: str,
) -> int:
    """
    Returns the similarity between two strings
    as a percentage from 0 to 100.

    Combines:
    - Sequence similarity
    - Token overlap similarity
    """

    left = _normalize(left)
    right = _normalize(right)

    if not left and not right:
        return 100

    if not left or not right:
        return 0

    sequence_score = SequenceMatcher(
        None,
        left,
        right,
    ).ratio()

    token_score = _token_similarity(
        left,
        right,
    )

    similarity = sequence_score * 0.7 + token_score * 0.3

    return round(similarity * 100)
