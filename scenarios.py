
"""
FitFindr evaluation scenarios.

Each scenario runs five times through run_eval.py.
The criterion number corresponds to criteria.md.
"""

SCENARIOS = [
    {
        # Criterion 1: Successful query completes all three tools.
        "name": "matching query completes",
        "query": "vintage graphic tee under $30",
        "wardrobe": "example",
        "criterion": 1,
    },
    {
        # Criterion 2: Impossible query stops before outfit generation.
        "name": "impossible query stops early",
        "query": "designer ballgown size XXS under $5",
        "wardrobe": "example",
        "criterion": 2,
    },
    {
        # Criterion 3: Selected item remains consistent across tools.
        "name": "selected item state consistency",
        "query": "denim jacket under $50",
        "wardrobe": "example",
        "criterion": 3,
    },
    {
        # Criterion 4: Fit card contains accurate price and platform.
        "name": "fit card listing accuracy",
        "query": "vintage graphic tee under $30",
        "wardrobe": "example",
        "criterion": 4,
    },
    {
        # Criterion 5: Empty wardrobe produces usable outfits.
        "name": "empty wardrobe outfit suggestions",
        "query": "denim jacket under $50",
        "wardrobe": "empty",
        "criterion": 5,
    },
]

WARDROBES = ("example", "empty")


def validate() -> list[str]:
    """Validate evaluation scenarios before running tests."""
    problems = []

    for i, scenario in enumerate(SCENARIOS, 1):
        if not scenario.get("query", "").strip():
            problems.append(f"scenario {i} has no query")

        if scenario.get("wardrobe") not in WARDROBES:
            problems.append(
                f"scenario {i} has wardrobe "
                f"{scenario.get('wardrobe')!r} — "
                f"it should be one of {WARDROBES}"
            )

    return problems
