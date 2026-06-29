import re


WINDOWS_PATH_PATTERN = re.compile(r"[A-Za-z]:\\(?:[^\\\s]+\\)*[^\\\s]+")

FILE_PATTERN = re.compile(
    r"""
    (?:
        # Repository paths
        (?:[A-Za-z0-9_.-]+/)+
        [A-Za-z0-9_.-]+\.[A-Za-z0-9]+

        |

        # Root-level files
        [A-Za-z0-9_.-]+\.[A-Za-z0-9]+

        |

        # Common extensionless repository files
        README
        |LICENSE
        |COPYING
        |Makefile
        |Dockerfile
    )
    """,
    re.VERBOSE,
)


def extract_file_mentions(
    text: str,
) -> set[str]:

    if not text:
        return set()

    # Ignore Windows filesystem paths
    text = WINDOWS_PATH_PATTERN.sub(
        " ",
        text,
    )

    return {match.group(0) for match in FILE_PATTERN.finditer(text)}
