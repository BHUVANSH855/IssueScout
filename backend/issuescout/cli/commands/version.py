from __future__ import annotations

import platform

from issuescout.core.config import settings


def run() -> None:
    """
    Display IssueScout version information.
    """

    print(f"{settings.APP_NAME} {settings.API_VERSION}")
    print(f"Python {platform.python_version()}")
