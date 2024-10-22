from typing import List

import pytest

from src.cit_parser import (
    CaselawCitation,
    LabelPrediction,
)


@pytest.mark.parametrize(
    ["token_label_pairs", "expected"],
    [
        # Test case: Complete citation with all fields
        (
            [
                LabelPrediction(token="Brown", label="CASE_NAME", start=0, end=5),
                LabelPrediction(token="v.", label="CASE_NAME", start=6, end=7),
                LabelPrediction(token="Board", label="CASE_NAME", start=8, end=13),
                LabelPrediction(token="of", label="CASE_NAME", start=14, end=15),
                LabelPrediction(token="Education", label="CASE_NAME", start=16, end=25),
                LabelPrediction(token="of", label="CASE_NAME", start=26, end=27),
                LabelPrediction(token="Topeka", label="CASE_NAME", start=28, end=34),
                LabelPrediction(token="347", label="VOLUME", start=35, end=38),
                LabelPrediction(token="U.S.", label="REPORTER", start=39, end=43),
                LabelPrediction(token="483", label="PAGE", start=44, end=47),
                LabelPrediction(token="1954", label="YEAR", start=48, end=52),
            ],
            CaselawCitation(
                case_name="Brown v. Board of Education of Topeka",
                volume=347,
                reporter="U.S.",
                starting_page=483,
                year=1954,
                start=0,
                end=52,
            ),
        ),
        # Test case: Citation with no volume
        (
            [
                LabelPrediction(token="Jones", label="CASE_NAME", start=0, end=5),
                LabelPrediction(token="v.", label="CASE_NAME", start=6, end=7),
                LabelPrediction(token="Smith", label="CASE_NAME", start=8, end=13),
                LabelPrediction(token="F.2d", label="REPORTER", start=14, end=18),
                LabelPrediction(token="101", label="PAGE", start=19, end=22),
                LabelPrediction(token="2000", label="YEAR", start=23, end=27),
            ],
            CaselawCitation(
                case_name="Jones v. Smith",
                reporter="F.2d",
                starting_page=101,
                year=2000,
                start=0,
                end=27,
            ),
        ),
        # Test case: Citation with no reporter (e.g., Jones, supra, at 67)
        (
            [
                LabelPrediction(token="Jones", label="CASE_NAME", start=0, end=5),
                LabelPrediction(token="supra", label="CASE_NAME", start=6, end=11),
                LabelPrediction(token="67", label="PAGE", start=12, end=14),
            ],
            CaselawCitation(
                case_name="Jones supra",
                starting_page=67,
                start=0,
                end=14,
            ),
        ),
        # Test case: Citation with only case name (minimal valid citation)
        (
            [
                LabelPrediction(token="Doe", label="CASE_NAME", start=0, end=3),
                LabelPrediction(token="v.", label="CASE_NAME", start=4, end=5),
                LabelPrediction(token="Roe", label="CASE_NAME", start=6, end=9),
            ],
            CaselawCitation(
                case_name="Doe v. Roe",
                start=0,
                end=9,
            ),
        ),
        # Test case: Missing case name (should return None)
        (
            [
                LabelPrediction(token="347", label="VOLUME", start=0, end=3),
                LabelPrediction(token="U.S.", label="REPORTER", start=4, end=8),
                LabelPrediction(token="483", label="PAGE", start=9, end=12),
                LabelPrediction(token="1954", label="YEAR", start=13, end=17),
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


@pytest.mark.parametrize(
    ["cit1", "cit2", "res"],
    [
        (
            CaselawCitation(
                case_name="hi",
                volume=1,
                reporter="some.reporter",
                starting_page=1,
                year=1990,
                start=1,
                end=1,
            ),
            CaselawCitation(
                case_name="case name does not matter",
                volume=1,
                reporter="some.reporter",
                starting_page=1,
                year=1990,
                start=11,
                end=15,
            ),
            True,
        ),
        (
            CaselawCitation(
                case_name="Ppl v. Doe",
                volume=56,
                reporter="Crim. L. Enjoyers",
                starting_page=11,
                year=1991,
                court="NY App. Div.",
                start=1,
                end=1,
            ),
            CaselawCitation(
                case_name="case name does not matter",
                volume=56,
                reporter="Crim. L. Enjoyers",
                starting_page=11,
                year=1991,
                court="NY App. Div.",
                start=11,
                end=15,
            ),
            True,
        ),
        (
            CaselawCitation(
                case_name="year matters",
                volume=56,
                reporter="Crim. L. Enjoyers",
                starting_page=11,
                year=2001,
                court="NY App. Div.",
                start=1,
                end=1,
            ),
            CaselawCitation(
                case_name="case name does not matter",
                volume=56,
                reporter="Crim. L. Enjoyers",
                starting_page=11,
                year=1021,
                court="NY App. Div.",
                start=11,
                end=15,
            ),
            False,
        ),
        (
            CaselawCitation(
                case_name="People v. Wuncler",
                volume=56,
                reporter="Crim. L. Enjoyers",
                starting_page=11,
                year=2001,
                court="U.S.",
                start=1,
                end=1,
            ),
            CaselawCitation(
                case_name="People v. Wuncler",
                volume=56,
                reporter="Crim. L. Enjoyers",
                starting_page=11,
                year=2001,
                court="M.D.",
                start=1,
                end=1,
            ),
            False,
        ),
    ],
)
def test_eq(cit1: CaselawCitation, cit2: CaselawCitation, res: bool):
    assert (cit1 == cit2) == res
