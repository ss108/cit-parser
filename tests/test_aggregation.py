from typing import List

import pytest

from src.postprocess import aggregate_entities
from src.types import LabelPrediction


@pytest.mark.parametrize(
    ["labels", "expected"],
    [
        (
            [
                LabelPrediction(token="h", label="B-CASE_NAME"),
                LabelPrediction(token="##e", label="I-CASE_NAME"),
                LabelPrediction(token="##h", label="I-CASE_NAME"),
            ],
            [LabelPrediction(token="heh", label="CASE_NAME")],
        ),
        (
            [
                LabelPrediction(token="Ho", label="B-CASE_NAME"),
                LabelPrediction(token="##garth", label="I-CASE_NAME"),
                LabelPrediction(token=",", label="I-CASE_NAME"),
            ],
            [LabelPrediction(token="Hogarth,", label="CASE_NAME")],
        ),
        (
            [
                LabelPrediction(token="Ken", label="B-CASE_NAME"),
                LabelPrediction(token="##shin", label="I-CASE_NAME"),
                LabelPrediction(token="##,", label="I-CASE_NAME"),
            ],
            [LabelPrediction(token="Kenshin,", label="CASE_NAME")],
        ),
        (
            [
                LabelPrediction(token="h", label="B-CASE_NAME"),
                LabelPrediction(token="##e", label="I-CASE_NAME"),
                LabelPrediction(token="##h", label="I-CASE_NAME"),
                LabelPrediction(token=",", label="O"),
                LabelPrediction(token="87", label="B-VOLUME"),
                LabelPrediction(token="F", label="B-REPORTER"),
                LabelPrediction(token=".", label="I-REPORTER"),
                LabelPrediction(token="3d", label="I-REPORTER"),
                LabelPrediction(token="at", label="O"),
                LabelPrediction(token="99", label="B-PIN"),
            ],
            [
                LabelPrediction(token="heh", label="CASE_NAME"),
                LabelPrediction(token="87", label="VOLUME"),
                LabelPrediction(token="F. 3d", label="REPORTER"),
                LabelPrediction(token="99", label="PIN"),
            ],
        ),
    ],
)
def test_aggregate_entities_short_cite(
    labels: List[LabelPrediction], expected: List[LabelPrediction]
):
    result = aggregate_entities(labels)
    assert result == expected


@pytest.mark.parametrize(
    ["labels", "expected"],
    [
        (
            [
                LabelPrediction(token="18", label="B-TITLE"),
                LabelPrediction(token="U", label="B-CODE"),
                LabelPrediction(token=".", label="I-CODE"),
                LabelPrediction(token="S", label="I-CODE"),
                LabelPrediction(token=".", label="I-CODE"),
                LabelPrediction(token="C", label="I-CODE"),
                LabelPrediction(token=".", label="I-CODE"),
                LabelPrediction(token="Sec", label="B-SECTION"),
                LabelPrediction(token="##tion", label="I-SECTION"),
                LabelPrediction(token="87", label="I-SECTION"),
            ],
            [
                LabelPrediction(token="18", label="TITLE"),
                LabelPrediction(token="U.S.C.", label="CODE"),
                LabelPrediction(token="Section 87", label="SECTION"),
            ],
        ),
    ],
)
def test_aggregate_entities_statute(
    labels: List[LabelPrediction], expected: List[LabelPrediction]
):
    result = aggregate_entities(labels)
    assert result == expected


@pytest.mark.parametrize(
    ["labels", "expected"],
    [
        (
            [
                LabelPrediction(token="Brown", label="B-CASE_NAME"),
                LabelPrediction(token="v", label="I-CASE_NAME"),
                LabelPrediction(token=".", label="I-CASE_NAME"),
                LabelPrediction(token="Board", label="I-CASE_NAME"),
                LabelPrediction(token="of", label="I-CASE_NAME"),
                LabelPrediction(token="Education", label="I-CASE_NAME"),
                LabelPrediction(token="of", label="I-CASE_NAME"),
                LabelPrediction(token="Topeka", label="I-CASE_NAME"),
                LabelPrediction(token=",", label="O"),
                LabelPrediction(token="34", label="B-VOLUME"),
                LabelPrediction(token="##7", label="I-VOLUME"),
                LabelPrediction(token="U", label="B-REPORTER"),
                LabelPrediction(token=".", label="I-REPORTER"),
                LabelPrediction(token="S", label="I-REPORTER"),
                LabelPrediction(token=".", label="I-REPORTER"),
                LabelPrediction(token="4", label="B-PAGE"),
                LabelPrediction(token="##83", label="I-PAGE"),
                LabelPrediction(token="(", label="O"),
                LabelPrediction(token="1954", label="B-YEAR"),
                LabelPrediction(token=")", label="O"),
                LabelPrediction(token="[SEP]", label="I-CASE_NAME"),
            ],
            [
                LabelPrediction(
                    token="Brown v. Board of Education of Topeka", label="CASE_NAME"
                ),
                LabelPrediction(token="347", label="VOLUME"),
                LabelPrediction(token="U.S.", label="REPORTER"),
                LabelPrediction(token="483", label="PAGE"),
                LabelPrediction(token="1954", label="YEAR"),
            ],
        ),
        (
            [
                LabelPrediction(token="Doe", label="B-CASE_NAME"),
                LabelPrediction(token="v.", label="I-CASE_NAME"),
                LabelPrediction(token="Smith", label="I-CASE_NAME"),
                LabelPrediction(token=",", label="O"),
                LabelPrediction(token="456", label="B-VOLUME"),
                LabelPrediction(token="F", label="B-REPORTER"),
                LabelPrediction(token=".", label="I-REPORTER"),
                LabelPrediction(token="2", label="I-REPORTER"),
                LabelPrediction(token="d", label="I-REPORTER"),
                LabelPrediction(token="101", label="B-PAGE"),
                LabelPrediction(token="at", label="O"),
                LabelPrediction(token="105", label="B-PIN"),
                LabelPrediction(token="(", label="O"),
                LabelPrediction(token="2009", label="B-YEAR"),
                LabelPrediction(token=")", label="O"),
            ],
            [
                LabelPrediction(token="Doe v. Smith", label="CASE_NAME"),
                LabelPrediction(token="456", label="VOLUME"),
                LabelPrediction(token="F.2d", label="REPORTER"),
                LabelPrediction(token="101", label="PAGE"),
                LabelPrediction(token="105", label="PIN"),
                LabelPrediction(token="2009", label="YEAR"),
            ],
        ),
    ],
)
def test_aggregate_entities_caselaw(
    labels: List[LabelPrediction], expected: List[LabelPrediction]
):
    result = aggregate_entities(labels)
    assert result == expected
