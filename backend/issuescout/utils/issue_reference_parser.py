import re


REFERENCE_PATTERNS = (
    r"\bfix(?:es|ed)?\s+#?(\d+)",
    r"\bclose(?:s|d)?\s+#?(\d+)",
    r"\bresolve(?:s|d)?\s+#?(\d+)",
    r"\brefs?\s+#?(\d+)",
    r"\brelated\s+to\s+#?(\d+)",
    r"\bgh-(\d+)",
    r"\b[\w.-]+/[\w.-]+#(\d+)",
    r"github\.com/[\w.-]+/[\w.-]+/issues/(\d+)",
    r"#(\d+)",
)


def extract_issue_references(
    body: str,
) -> set[int]:
    """
    Extract referenced GitHub issue numbers from text.

    Supports:
    - Fixes #123
    - Closes #123
    - Resolves #123
    - Refs #123
    - Related to #123
    - gh-123
    - python/cpython#123
    - https://github.com/python/cpython/issues/123
    - #123
    """

    if not body:
        return set()

    issues: set[int] = set()

    for pattern in REFERENCE_PATTERNS:
        for match in re.findall(
            pattern,
            body,
            flags=re.IGNORECASE,
        ):
            issues.add(int(match))

    return issues
