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


# @pytest.mark.parametrize(
#     ["labels", "expected"],
#     [
#         (
#             [
#                 LabelPrediction(token="18", label="B-TITLE"),
#                 LabelPrediction(token="U", label="B-CODE"),
#                 LabelPrediction(token=".", label="I-CODE"),
#                 LabelPrediction(token="S", label="I-CODE"),
#                 LabelPrediction(token=".", label="I-CODE"),
#                 LabelPrediction(token="C", label="I-CODE"),
#                 LabelPrediction(token=".", label="I-CODE"),
#                 LabelPrediction(token="Sec", label="B-SECTION"),
#                 LabelPrediction(token="##tion", label="I-SECTION"),
#                 LabelPrediction(token="87", label="I-SECTION"),
#             ],
#             [
#                 LabelPrediction(token="18", label="TITLE"),
#                 LabelPrediction(token="U . S . C .", label="CODE"),
#                 LabelPrediction(token="Sec ##tion 87", label="SECTION"),
#             ],
#         ),
#     ],
# )
# def test_aggregate_entities_statute(
#     labels: List[LabelPrediction], expected: List[LabelPrediction]
# ):
#     result = aggregate_entities(labels)
#     assert result == expected
