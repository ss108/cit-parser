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
                LabelPrediction(token="18", label="TITLE"),
                LabelPrediction(token="U", label="CODE"),
                LabelPrediction(token=".", label="CODE"),
                LabelPrediction(token="S", label="CODE"),
                LabelPrediction(token=".", label="CODE"),
                LabelPrediction(token="C", label="CODE"),
                LabelPrediction(token=".", label="CODE"),
                LabelPrediction(token="§", label="SECTION"),
                LabelPrediction(token="87", label="SECTION"),
                LabelPrediction(token="2002", label="YEAR"),
            ],
            StatuteCitation(title="18", code="U.S.C.", section="§ 87", year=2002),
        ),
        # Test case: Citation with only code and section
        (
            [
                LabelPrediction(token="U", label="CODE"),
                LabelPrediction(token=".", label="CODE"),
                LabelPrediction(token="S", label="CODE"),
                LabelPrediction(token=".", label="CODE"),
                LabelPrediction(token="§", label="SECTION"),
                LabelPrediction(token="3553", label="SECTION"),
            ],
            StatuteCitation(
                code="U.S.",
                section="§ 3553",
            ),
        ),
        # Test case: Citation with just a section and year
        (
            [
                LabelPrediction(token="Section", label="SECTION"),
                LabelPrediction(token="87", label="SECTION"),
                LabelPrediction(token="1999", label="YEAR"),
            ],
            StatuteCitation(section="Section 87", year=1999),
        ),
        # Test case: Citation with only a title
        (
            [
                LabelPrediction(token="Title", label="TITLE"),
                LabelPrediction(token="42", label="TITLE"),
            ],
            StatuteCitation(
                title="Title 42",
            ),
        ),
        # Test case: Invalid citation with no title, code, or section
        (
            [
                LabelPrediction(token="not", label="O"),
                LabelPrediction(token="valid", label="O"),
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
