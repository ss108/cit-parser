from typing import List, Union

import pytest

from src.types import Authorities, CaselawCitation, StatuteCitation


@pytest.mark.parametrize(
    "citations, expected_statutes, expected_caselaw",
    [
        # # Test case: Both statutes and caselaw are present
        (
            [
                StatuteCitation(
                    title="18", code="U.S.C.", section="§ 3553", start=0, end=10
                ),
                StatuteCitation(
                    title="42", code="U.S.C.", section="§ 1983", start=20, end=30
                ),
                CaselawCitation(
                    case_name="Doe v. Smith",
                    volume=456,
                    reporter="F.2d",
                    starting_page=101,
                    court="D. Ct.",
                    year=2000,
                    start=40,
                    end=50,
                ),
            ],
            {},
            # {
            #     StatuteCitation(
            #         title="18", code="U.S.C.", section="§ 3553", start=0, end=10
            #     ): [
            #         StatuteCitation(
            #             title="18", code="U.S.C.", section="§ 3553", start=0, end=10
            #         )
            #     ],
            #     StatuteCitation(
            #         title="42", code="U.S.C.", section="§ 1983", start=20, end=30
            #     ): [
            #         StatuteCitation(
            #             title="42", code="U.S.C.", section="§ 1983", start=20, end=30
            #         )
            #     ],
            # },
            {
                CaselawCitation(
                    case_name="Doe v. Smith",
                    volume=456,
                    reporter="F.2d",
                    starting_page=101,
                    year=2000,
                    court="D. Ct.",
                    start=40,
                    end=50,
                ): [
                    CaselawCitation(
                        case_name="Doe v. Smith",
                        volume=456,
                        reporter="F.2d",
                        starting_page=101,
                        year=2000,
                        court="D. Ct.",
                        start=40,
                        end=50,
                    )
                ],
            },
        ),
        # # Test case: Only caselaw citations
        (
            [
                CaselawCitation(
                    case_name="Roe v. Wade",
                    volume=410,
                    reporter="U.S.",
                    starting_page=113,
                    year=1973,
                    court="SCOTUS",
                    start=0,
                    end=10,
                ),
            ],
            {},
            {
                CaselawCitation(
                    case_name="Roe v. Wade",
                    volume=410,
                    reporter="U.S.",
                    starting_page=113,
                    court="SCOTUS",
                    year=1973,
                    start=0,
                    end=10,
                ): [
                    CaselawCitation(
                        case_name="Roe v. Wade",
                        volume=410,
                        reporter="U.S.",
                        starting_page=113,
                        year=1973,
                        start=0,
                        court="SCOTUS",
                        end=10,
                    )
                ]
            },
        ),
        # # # Test case: Only statute citations
        # (
        #     [
        #         StatuteCitation(
        #             title="28", code="U.S.C.", section="§ 1441", start=0, end=5
        #         ),
        #     ],
        #     {
        #         StatuteCitation(
        #             title="28", code="U.S.C.", section="§ 1441", start=0, end=5
        #         ): [
        #             StatuteCitation(
        #                 title="28", code="U.S.C.", section="§ 1441", start=0, end=5
        #             )
        #         ]
        #     },
        #     {},
        # ),
        # Test case: No citations (empty list)
        (
            [],
            {},
            {},
        ),
    ],
)
def test_authorities_construct(
    citations: List[Union[StatuteCitation, CaselawCitation]],
    expected_statutes,
    expected_caselaw,
):
    result = Authorities.construct(citations)
    assert result.statutes == expected_statutes
    assert result.caselaw == expected_caselaw


@pytest.mark.parametrize(
    "citations, expected_keys",
    [
        # Test case: Full and short citations for caselaw
        (
            [
                CaselawCitation(
                    case_name="Hman v. B",
                    volume=67,
                    reporter="H. Rep.",
                    starting_page=99,
                    court="H. Civ. Ct.",
                    year=1981,
                    start=0,
                    end=10,
                ),
                CaselawCitation(
                    case_name="B",
                    volume=67,
                    reporter="H. Rep.",
                    raw_pin_cite="101",
                    start=20,
                    end=25,
                ),
            ],
            {
                CaselawCitation(
                    case_name="Hman v. B",
                    volume=67,
                    reporter="H. Rep.",
                    starting_page=99,
                    court="H. Civ. Ct.",
                    year=1981,
                    start=0,
                    end=10,
                )
            },
        ),
        # # Test case: Full statute and incomplete statute
        # (
        #     [
        #         StatuteCitation(
        #             title="18",
        #             code="U.S.C.",
        #             section="§ 3553",
        #             year=2002,
        #             start=0,
        #             end=10,
        #         ),
        #         StatuteCitation(
        #             code="U.S.C.",
        #             section="§ 3553",
        #             start=20,
        #             end=30,
        #         ),
        #     ],
        #     {
        #         StatuteCitation(
        #             title="18",
        #             code="U.S.C.",
        #             section="§ 3553",
        #             year=2002,
        #             start=0,
        #             end=10,
        #         )
        #     },
        # ),
        # # Test case: Only short citations, expect empty dicts
        # (
        #     [
        #         CaselawCitation(
        #             case_name="B",
        #             volume=67,
        #             reporter="H. Rep.",
        #             raw_pin_cite="101",
        #             start=20,
        #             end=25,
        #         ),
        #         StatuteCitation(
        #             code="U.S.C.",
        #             section="§ 3553",
        #             start=20,
        #             end=30,
        #         ),
        #     ],
        #     set(),
        # ),
    ],
)
def test_authorities_only_full_citations_as_keys(
    citations: List[Union[StatuteCitation, CaselawCitation]], expected_keys: set
):
    result = Authorities.construct(citations)
    caselaw_keys = set(result.caselaw.keys())
    statute_keys = set(result.statutes.keys())

    full_keys = {k for k in caselaw_keys.union(statute_keys) if k.is_full}

    assert full_keys == expected_keys
