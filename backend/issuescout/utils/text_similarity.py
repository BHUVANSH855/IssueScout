from difflib import SequenceMatcher


def similarity_percentage(
    left: str,
    right: str,
) -> int:
    """
    Returns the similarity between two strings
    as a percentage from 0 to 100.
    """

    left = (left or "").strip()
    right = (right or "").strip()

    if not left and not right:
        return 100

    if not left or not right:
        return 0

    return int(
        SequenceMatcher(
            None,
            left.lower(),
            right.lower(),
        ).ratio()
        * 100
    )
