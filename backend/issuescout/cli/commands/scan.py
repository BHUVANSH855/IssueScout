from __future__ import annotations

import asyncio

from issuescout.scanner.engine import ScannerEngine


async def _scan(
    owner: str,
    repository: str,
    output_format: str,
) -> None:
    engine = ScannerEngine()

    result = await engine.scan_repository(
        owner,
        repository,
    )

    if output_format == "json":
        print(result.model_dump_json(indent=2))
        return

    print()
    print("=" * 60)
    print("IssueScout Scan")
    print("=" * 60)
    print(f"Repository : {result.repository}")
    print(f"Issues      : {result.available_issues}")
    print()

    if not result.issues:
        print("No candidate issues found.")
        return

    for issue in result.issues:
        print(f"#{issue.number} - {issue.title}")

        if issue.assigned:
            print(f"  Assignee   : {issue.assignee}")

        print(f"  Confidence : {issue.confidence}")

        if issue.linked_pr_number is not None:
            print(f"  Linked PR  : #{issue.linked_pr_number} {issue.linked_pr_title}")

        print()


def run(
    owner: str,
    repository: str,
    output_format: str,
) -> None:
    asyncio.run(
        _scan(
            owner,
            repository,
            output_format,
        )
    )
