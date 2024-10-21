from typing import List

import pytest

from src.types import (
    LabelPrediction,
    StatuteCitation,
)


@pytest.mark.parametrize(
    ["token_label_pairs", "expected"],
    [
        # Test case: Complete citation with title, code, and section
        (
            [
                LabelPrediction(token="18", label="TITLE", start=0, end=2),
                LabelPrediction(token="U", label="CODE", start=3, end=4),
                LabelPrediction(token=".", label="CODE", start=5, end=5),
                LabelPrediction(token="S", label="CODE", start=6, end=6),
                LabelPrediction(token=".", label="CODE", start=7, end=7),
                LabelPrediction(token="C", label="CODE", start=8, end=8),
                LabelPrediction(token=".", label="CODE", start=9, end=9),
                LabelPrediction(token="§", label="SECTION", start=10, end=10),
                LabelPrediction(token="87", label="SECTION", start=11, end=13),
                LabelPrediction(token="2002", label="YEAR", start=14, end=18),
            ],
            StatuteCitation(
                title="18", code="U.S.C.", section="§ 87", year=2002, start=0, end=18
            ),
        ),
        # Test case: Citation with only code and section
        (
            [
                LabelPrediction(token="U", label="CODE", start=0, end=1),
                LabelPrediction(token=".", label="CODE", start=2, end=2),
                LabelPrediction(token="S", label="CODE", start=3, end=3),
                LabelPrediction(token=".", label="CODE", start=4, end=4),
                LabelPrediction(token="§", label="SECTION", start=5, end=5),
                LabelPrediction(token="3553", label="SECTION", start=6, end=10),
            ],
            StatuteCitation(
                code="U.S.",
                section="§ 3553",
                start=0,
                end=10,
            ),
        ),
        # Test case: Citation with just a section and year
        (
            [
                LabelPrediction(token="Section", label="SECTION", start=0, end=6),
                LabelPrediction(token="87", label="SECTION", start=7, end=8),
                LabelPrediction(token="1999", label="YEAR", start=9, end=13),
            ],
            StatuteCitation(
                section="Section 87",
                year=1999,
                start=0,
                end=13,
            ),
        ),
        # Test case: Citation with only a title
        (
            [
                LabelPrediction(token="Title", label="TITLE", start=0, end=4),
                LabelPrediction(token="42", label="TITLE", start=5, end=7),
            ],
            None,
        ),
        # Test case: Invalid citation with no title, code, or section
        (
            [
                LabelPrediction(token="not", label="O", start=0, end=3),
                LabelPrediction(token="valid", label="O", start=4, end=8),
            ],
            None,
        ),
    ],
)
def test_from_token_label_pairs(
    token_label_pairs: List[LabelPrediction], expected: StatuteCitation
):
    result = StatuteCitation.from_token_label_pairs(token_label_pairs)
    assert result == expected
