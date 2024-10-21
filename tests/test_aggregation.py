from typing import List

import pytest

from src.postprocess import aggregate_entities
from src.types import LabelPrediction


@pytest.mark.parametrize(
    ["labels", "expected"],
    [
        (
            [
                LabelPrediction(token="h", label="B-CASE_NAME", start=0, end=1),
                LabelPrediction(token="##e", label="I-CASE_NAME", start=1, end=2),
                LabelPrediction(token="##h", label="I-CASE_NAME", start=2, end=3),
            ],
            [LabelPrediction(token="heh", label="CASE_NAME", start=0, end=3)],
        ),
        (
            [
                LabelPrediction(token="Ho", label="B-CASE_NAME", start=0, end=2),
                LabelPrediction(token="##garth", label="I-CASE_NAME", start=2, end=8),
                LabelPrediction(token=",", label="I-CASE_NAME", start=9, end=9),
            ],
            [LabelPrediction(token="Hogarth,", label="CASE_NAME", start=0, end=9)],
        ),
        (
            [
                LabelPrediction(token="Ken", label="B-CASE_NAME", start=0, end=3),
                LabelPrediction(token="##shin", label="I-CASE_NAME", start=3, end=8),
                LabelPrediction(token="##,", label="I-CASE_NAME", start=9, end=9),
            ],
            [LabelPrediction(token="Kenshin,", label="CASE_NAME", start=0, end=9)],
        ),
        (
            [
                LabelPrediction(token="h", label="B-CASE_NAME", start=0, end=1),
                LabelPrediction(token="##e", label="I-CASE_NAME", start=1, end=2),
                LabelPrediction(token="##h", label="I-CASE_NAME", start=2, end=3),
                LabelPrediction(token=",", label="O", start=4, end=4),
                LabelPrediction(token="87", label="B-VOLUME", start=5, end=6),
                LabelPrediction(token="F", label="B-REPORTER", start=7, end=7),
                LabelPrediction(token=".", label="I-REPORTER", start=8, end=8),
                LabelPrediction(token="3d", label="I-REPORTER", start=9, end=11),
                LabelPrediction(token="at", label="O", start=12, end=13),
                LabelPrediction(token="99", label="B-PIN", start=14, end=15),
            ],
            [
                LabelPrediction(token="heh", label="CASE_NAME", start=0, end=3),
                LabelPrediction(token="87", label="VOLUME", start=5, end=6),
                LabelPrediction(token="F. 3d", label="REPORTER", start=7, end=11),
                LabelPrediction(token="99", label="PIN", start=14, end=15),
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
                LabelPrediction(token="18", label="B-TITLE", start=0, end=2),
                LabelPrediction(token="U", label="B-CODE", start=3, end=4),
                LabelPrediction(token=".", label="I-CODE", start=5, end=5),
                LabelPrediction(token="S", label="I-CODE", start=6, end=6),
                LabelPrediction(token=".", label="I-CODE", start=7, end=7),
                LabelPrediction(token="C", label="I-CODE", start=8, end=8),
                LabelPrediction(token=".", label="I-CODE", start=9, end=9),
                LabelPrediction(token="Sec", label="B-SECTION", start=10, end=12),
                LabelPrediction(token="##tion", label="I-SECTION", start=13, end=15),
                LabelPrediction(token="87", label="I-SECTION", start=16, end=17),
            ],
            [
                LabelPrediction(token="18", label="TITLE", start=0, end=2),
                LabelPrediction(token="U.S.C.", label="CODE", start=3, end=9),
                LabelPrediction(token="Section 87", label="SECTION", start=10, end=17),
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
                LabelPrediction(token=",", label="O", start=38, end=38),
                LabelPrediction(token="34", label="B-VOLUME", start=39, end=41),
                LabelPrediction(token="##7", label="I-VOLUME", start=41, end=42),
                LabelPrediction(token="U", label="B-REPORTER", start=43, end=44),
                LabelPrediction(token=".", label="I-REPORTER", start=44, end=44),
                LabelPrediction(token="S", label="I-REPORTER", start=45, end=46),
                LabelPrediction(token=".", label="I-REPORTER", start=46, end=46),
                LabelPrediction(token="4", label="B-PAGE", start=47, end=48),
                LabelPrediction(token="##83", label="I-PAGE", start=48, end=50),
                LabelPrediction(token="(", label="O", start=51, end=51),
                LabelPrediction(token="1954", label="B-YEAR", start=52, end=56),
                LabelPrediction(token=")", label="O", start=57, end=57),
                LabelPrediction(token="[SEP]", label="I-CASE_NAME", start=58, end=58),
            ],
            [
                LabelPrediction(
                    token="Brown v. Board of Education of Topeka",
                    label="CASE_NAME",
                    start=0,
                    end=37,
                ),
                LabelPrediction(token="347", label="VOLUME", start=39, end=42),
                LabelPrediction(token="U.S.", label="REPORTER", start=43, end=46),
                LabelPrediction(token="483", label="PAGE", start=47, end=50),
                LabelPrediction(token="1954", label="YEAR", start=52, end=56),
            ],
        ),
        # (
        #     [
        #         LabelPrediction(token="Doe", label="B-CASE_NAME", start=0, end=3),
        #         LabelPrediction(token="v.", label="I-CASE_NAME", start=4, end=6),
        #         LabelPrediction(token="Smith", label="I-CASE_NAME", start=7, end=12),
        #         LabelPrediction(token=",", label="O", start=13, end=13),
        #         LabelPrediction(token="456", label="B-VOLUME", start=14, end=17),
        #         LabelPrediction(token="F", label="B-REPORTER", start=18, end=19),
        #         LabelPrediction(token=".", label="I-REPORTER", start=19, end=19),
        #         LabelPrediction(token="2", label="I-REPORTER", start=20, end=21),
        #         LabelPrediction(token="d", label="I-REPORTER", start=21, end=22),
        #         LabelPrediction(token="101", label="B-PAGE", start=23, end=26),
        #         LabelPrediction(token="at", label="O", start=27, end=28),
        #         LabelPrediction(token="105", label="B-PIN", start=29, end=32),
        #         LabelPrediction(token="(", label="O", start=33, end=33),
        #         LabelPrediction(token="2009", label="B-YEAR", start=34, end=38),
        #         LabelPrediction(token=")", label="O", start=39, end=39),
        #     ],
        #     [
        #         LabelPrediction(
        #             token="Doe v. Smith", label="CASE_NAME", start=0, end=12
        #         ),
        #         LabelPrediction(token="456", label="VOLUME", start=14, end=17),
        #         LabelPrediction(token="F.2d", label="REPORTER", start=18, end=22),
        #         LabelPrediction(token="101", label="PAGE", start=23, end=26),
        #         LabelPrediction(token="105", label="PIN", start=29, end=32),
        #         LabelPrediction(token="2009", label="YEAR", start=34, end=38),
        #     ],
        # ),
        # (
        #     [
        #         LabelPrediction(token="Smith", label="B-CASE_NAME", start=0, end=5),
        #         LabelPrediction(token="v.", label="I-CASE_NAME", start=6, end=8),
        #         LabelPrediction(token="Jones", label="I-CASE_NAME", start=9, end=14),
        #         LabelPrediction(token=",", label="O", start=15, end=15),
        #         LabelPrediction(token="456", label="B-VOLUME", start=16, end=19),
        #         LabelPrediction(token="F", label="B-REPORTER", start=20, end=21),
        #         LabelPrediction(token=".", label="I-REPORTER", start=21, end=21),
        #         LabelPrediction(token="2", label="I-REPORTER", start=22, end=23),
        #         LabelPrediction(token="d", label="I-REPORTER", start=23, end=24),
        #         LabelPrediction(token="789", label="B-PAGE", start=25, end=28),
        #         LabelPrediction(token=",", label="O", start=29, end=29),
        #         LabelPrediction(token="792", label="B-PIN", start=30, end=33),
        #         LabelPrediction(token="(", label="O", start=34, end=34),
        #         LabelPrediction(token="2d", label="B-COURT", start=35, end=38),
        #         LabelPrediction(token="C", label="I-COURT", start=35, end=38),
        #         LabelPrediction(token="##ir", label="I-COURT", start=35, end=38),
        #         LabelPrediction(token="1983", label="B-YEAR", start=39, end=43),
        #         LabelPrediction(token=")", label="O", start=44, end=44),
        #     ],
        #     [
        #         LabelPrediction(
        #             token="Smith v. Jones", label="CASE_NAME", start=0, end=14
        #         ),
        #         LabelPrediction(token="456", label="VOLUME", start=16, end=19),
        #         LabelPrediction(token="F.2d", label="REPORTER", start=20, end=24),
        #         LabelPrediction(token="789", label="PAGE", start=25, end=28),
        #         LabelPrediction(token="792", label="PIN", start=30, end=33),
        #         LabelPrediction(token="2d Cir", label="COURT", start=35, end=38),
        #         LabelPrediction(token="1983", label="YEAR", start=39, end=43),
        #     ],
        # ),
    ],
)
def test_aggregate_entities_caselaw(
    labels: List[LabelPrediction], expected: List[LabelPrediction]
):
    result = aggregate_entities(labels)
    assert result == expected
