from typing import List

import pytest

from src.types import (
    CaselawCitation,
    LabelPrediction,
)


@pytest.mark.parametrize(
    ["token_label_pairs", "expected"],
    [
        (
            [
                LabelPrediction(token="Brown", label="CASE_NAME"),
                LabelPrediction(token="v.", label="CASE_NAME"),
                LabelPrediction(token="Board", label="CASE_NAME"),
                LabelPrediction(token="of", label="CASE_NAME"),
                LabelPrediction(token="Education", label="CASE_NAME"),
                LabelPrediction(token="of", label="CASE_NAME"),
                LabelPrediction(token="Topeka", label="CASE_NAME"),
                LabelPrediction(token="347", label="VOLUME"),
                LabelPrediction(token="U.S.", label="REPORTER"),
                LabelPrediction(token="483", label="PAGE"),
                LabelPrediction(token="1954", label="YEAR"),
            ],
            CaselawCitation(
                case_name="Brown v. Board of Education of Topeka",
                volume=347,
                reporter="U.S.",
                starting_page=483,
                year=1954,
            ),
        ),
        # Test case: Citation with no volume
        (
            [
                LabelPrediction(token="Jones", label="CASE_NAME"),
                LabelPrediction(token="v.", label="CASE_NAME"),
                LabelPrediction(token="Smith", label="CASE_NAME"),
                LabelPrediction(token="F.2d", label="REPORTER"),
                LabelPrediction(token="101", label="PAGE"),
                LabelPrediction(token="2000", label="YEAR"),
            ],
            CaselawCitation(
                case_name="Jones v. Smith",
                reporter="F.2d",
                starting_page=101,
                year=2000,
            ),
        ),
        # Test case: Citation with no reporter (e.g., Jones, supra, at 67)
        (
            [
                LabelPrediction(token="Jones", label="CASE_NAME"),
                LabelPrediction(token="supra", label="CASE_NAME"),
                LabelPrediction(token="67", label="PAGE"),
            ],
            CaselawCitation(case_name="Jones supra", starting_page=67),
        ),
        # Test case: Citation with only case name (minimal valid citation)
        (
            [
                LabelPrediction(token="Doe", label="CASE_NAME"),
                LabelPrediction(token="v.", label="CASE_NAME"),
                LabelPrediction(token="Roe", label="CASE_NAME"),
            ],
            CaselawCitation(case_name="Doe v. Roe"),
        ),
        # Test case: Missing case name (should return None)
        (
            [
                LabelPrediction(token="347", label="VOLUME"),
                LabelPrediction(token="U.S.", label="REPORTER"),
                LabelPrediction(token="483", label="PAGE"),
                LabelPrediction(token="1954", label="YEAR"),
            ],
            None,
        ),
    ],
)
def test_from_token_label_pairs(
    token_label_pairs: List[LabelPrediction], expected: CaselawCitation
):
    result = CaselawCitation.from_token_label_pairs(token_label_pairs)
    assert result == expected
