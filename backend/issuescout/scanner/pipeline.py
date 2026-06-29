from issuescout.models import (
    Issue,
    RepositoryScanContext,
)


class AnalysisPipeline:
    def __init__(self, analyzers):
        self.analyzers = analyzers

    async def run(
        self,
        context: RepositoryScanContext,
        issue: Issue,
    ):
        results = []

        for analyzer in self.analyzers:
            try:
                result = await analyzer.analyze(
                    context,
                    issue,
                )
            except Exception:
                # Skip failed analyzers and continue with the remaining ones.
                continue

            results.append(result)

        return results
