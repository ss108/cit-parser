from typing import List

import pytest

from src.cit_parser import aggregate_entities
from src.cit_parser.types import LabelPrediction


@pytest.mark.parametrize(
    ["labels", "original_text", "expected"],
    [
        (
            [
                LabelPrediction(token="h", label="B-CASE_NAME", start=0, end=1),
                LabelPrediction(token="##e", label="I-CASE_NAME", start=1, end=2),
                LabelPrediction(token="##h", label="I-CASE_NAME", start=2, end=3),
            ],
            "heh",
            [LabelPrediction(token="heh", label="CASE_NAME", start=0, end=3)],
        ),
        (
            [
                LabelPrediction(token="Ho", label="B-CASE_NAME", start=0, end=2),
                LabelPrediction(token="##garth", label="I-CASE_NAME", start=2, end=8),
                LabelPrediction(token=",", label="I-CASE_NAME", start=9, end=9),
            ],
            "Hogarth,",
            [LabelPrediction(token="Hogarth,", label="CASE_NAME", start=0, end=9)],
        ),
        (
            [
                LabelPrediction(token="Ken", label="B-CASE_NAME", start=0, end=3),
                LabelPrediction(token="##shin", label="I-CASE_NAME", start=3, end=8),
                LabelPrediction(token="##,", label="I-CASE_NAME", start=9, end=9),
            ],
            "Kenshin,",
            [LabelPrediction(token="Kenshin,", label="CASE_NAME", start=0, end=9)],
        ),
        (
            [
                LabelPrediction(token="h", label="B-CASE_NAME", start=0, end=1),
                LabelPrediction(token="##e", label="I-CASE_NAME", start=1, end=2),
                LabelPrediction(token="##h", label="I-CASE_NAME", start=2, end=3),
                LabelPrediction(token=",", label="O", start=4, end=4),
                LabelPrediction(token="87", label="B-VOLUME", start=5, end=7),
                LabelPrediction(token="F", label="B-REPORTER", start=8, end=9),
                LabelPrediction(token=".", label="I-REPORTER", start=9, end=10),
                LabelPrediction(token="3d", label="I-REPORTER", start=11, end=13),
                LabelPrediction(token="at", label="O", start=14, end=16),
                LabelPrediction(token="99", label="B-PIN", start=17, end=19),
            ],
            "heh, 87 F. 3d at 99",
            [
                LabelPrediction(token="heh", label="CASE_NAME", start=0, end=3),
                LabelPrediction(token="87", label="VOLUME", start=5, end=7),
                LabelPrediction(token="F. 3d", label="REPORTER", start=8, end=13),
                LabelPrediction(token="99", label="PIN", start=17, end=19),
            ],
        ),
    ],
)
def test_aggregate_entities_short_cite(
    labels: List[LabelPrediction], original_text: str, expected: List[LabelPrediction]
):
    result = aggregate_entities(labels, original_text)
    assert result == expected


@pytest.mark.parametrize(
    ["labels", "original_text", "expected"],
    [
        (
            [
                LabelPrediction(token="18", label="B-TITLE", start=0, end=2),
                LabelPrediction(token="U", label="B-CODE", start=3, end=4),
                LabelPrediction(token=".", label="I-CODE", start=5, end=5),
                LabelPrediction(token="S", label="I-CODE", start=6, end=6),
                LabelPrediction(token=".", label="I-CODE", start=7, end=7),
                LabelPrediction(token="C", label="I-CODE", start=8, end=8),
                LabelPrediction(token=".", label="I-CODE", start=9, end=9),
                LabelPrediction(token="Sec", label="B-SECTION", start=10, end=13),
                LabelPrediction(token="##tion", label="I-SECTION", start=13, end=17),
                LabelPrediction(token="87", label="I-SECTION", start=18, end=20),
            ],
            "18 U.S.C. Section 87",
            [
                LabelPrediction(token="18", label="TITLE", start=0, end=2),
                LabelPrediction(token="U.S.C.", label="CODE", start=3, end=9),
                LabelPrediction(token="Section 87", label="SECTION", start=10, end=20),
            ],
        ),
    ],
)
def test_aggregate_entities_statute(
    labels: List[LabelPrediction], original_text: str, expected: List[LabelPrediction]
):
    result = aggregate_entities(labels, original_text)
    assert result == expected


@pytest.mark.parametrize(
    ["labels", "original_text", "expected"],
    [
        (
            [
                LabelPrediction(token="Brown", label="B-CASE_NAME", start=0, end=5),
                LabelPrediction(token="v", label="I-CASE_NAME", start=6, end=7),
                LabelPrediction(token=".", label="I-CASE_NAME", start=7, end=8),
                LabelPrediction(token="Board", label="I-CASE_NAME", start=9, end=14),
                LabelPrediction(token="of", label="I-CASE_NAME", start=15, end=17),
                LabelPrediction(
                    token="Education", label="I-CASE_NAME", start=18, end=27
                ),
                LabelPrediction(token="of", label="I-CASE_NAME", start=28, end=30),
                LabelPrediction(token="Topeka", label="I-CASE_NAME", start=31, end=37),
                LabelPrediction(token=",", label="O", start=37, end=38),
                LabelPrediction(token="34", label="B-VOLUME", start=39, end=41),
                LabelPrediction(token="##7", label="I-VOLUME", start=41, end=42),
                LabelPrediction(token="U", label="B-REPORTER", start=43, end=44),
                LabelPrediction(token=".", label="I-REPORTER", start=44, end=45),
                LabelPrediction(token="S", label="I-REPORTER", start=45, end=46),
                LabelPrediction(token=".", label="I-REPORTER", start=46, end=47),
                LabelPrediction(token="4", label="B-PAGE", start=48, end=49),
                LabelPrediction(token="##83", label="I-PAGE", start=49, end=51),
                LabelPrediction(token="(", label="O", start=51, end=52),
                LabelPrediction(token="1954", label="B-YEAR", start=53, end=57),
                LabelPrediction(token=")", label="O", start=57, end=58),
            ],
            "Brown v. Board of Education of Topeka, 347 U.S. 483 (1954)",
            [
                LabelPrediction(
                    token="Brown v. Board of Education of Topeka",
                    label="CASE_NAME",
                    start=0,
                    end=37,
                ),
                LabelPrediction(token="347", label="VOLUME", start=39, end=42),
                LabelPrediction(token="U.S.", label="REPORTER", start=43, end=47),
                LabelPrediction(token="483", label="PAGE", start=48, end=51),
                LabelPrediction(token="1954", label="YEAR", start=53, end=57),
            ],
        ),
    ],
)
def test_aggregate_entities_caselaw(
    labels: List[LabelPrediction], original_text: str, expected: List[LabelPrediction]
):
    result = aggregate_entities(labels, original_text)
    assert result == expected
