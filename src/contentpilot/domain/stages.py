"""Pipeline stages and transition rules (pure domain).

The lifecycle of one article, in order:

    idea -> researching -> outlined -> drafted -> reviewing
         -> gated -> approved -> published
"""
from __future__ import annotations

IDEA = "idea"
RESEARCHING = "researching"
OUTLINED = "outlined"
DRAFTED = "drafted"
REVIEWING = "reviewing"
GATED = "gated"
APPROVED = "approved"
PUBLISHED = "published"
# PROMOTED = "promoted"  # Moved to addon

ORDER = [
    IDEA, RESEARCHING, OUTLINED, DRAFTED, REVIEWING,
    GATED, APPROVED, PUBLISHED,
]

# §8 (confirmed 2026-06-13): at most 3 articles in flight at once.
# Overridable via config.yaml → wip_limit field.
DEFAULT_WIP_LIMIT = 3
WIP_LIMIT = DEFAULT_WIP_LIMIT

# Stages that count as "in flight" toward the WIP limit (not yet shipped/dropped).
WIP_STAGES = frozenset({
    RESEARCHING, OUTLINED, DRAFTED, REVIEWING, GATED, APPROVED,
})


def counts_as_wip(stage: str | None) -> bool:
    return stage in WIP_STAGES
