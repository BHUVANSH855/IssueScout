from __future__ import annotations

import argparse

from issuescout.cli.commands.evaluate import (
    run as run_evaluate,
)

from issuescout.cli.commands.scan import (
    run as run_scan,
)
from issuescout.cli.commands.version import (
    run as run_version,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="issuescout",
        description="IssueScout Command Line Interface",
    )

    subparsers = parser.add_subparsers(
        dest="command",
    )

    subparsers.add_parser(
        "evaluate",
        help="Run evaluation benchmarks",
    )

    scan_parser = subparsers.add_parser(
        "scan",
        help="Scan a GitHub repository",
    )

    scan_parser.add_argument(
        "owner",
        help="Repository owner",
    )

    scan_parser.add_argument(
        "repository",
        help="Repository name",
    )

    scan_parser.add_argument(
        "--format",
        choices=[
            "console",
            "json",
        ],
        default="console",
        help="Output format",
    )

    subparsers.add_parser(
        "version",
        help="Display version information",
    )

    return parser


def main() -> None:
    parser = build_parser()

    args = parser.parse_args()

    match args.command:
        case "evaluate":
            run_evaluate()

        case "scan":
            run_scan(
                args.owner,
                args.repository,
                args.format,
            )

        case "version":
            run_version()

        case _:
            parser.print_help()


if __name__ == "__main__":
    main()
