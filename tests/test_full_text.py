import pytest

from src.cit_parser import CaselawCitation, StatuteCitation


@pytest.mark.parametrize(
    "citation, expected",
    [
        (
            CaselawCitation(
                case_name="Brown v. Board of Education",
                volume=347,
                reporter="U.S.",
                starting_page=483,
                raw_pin_cite="484",
                raw_court=None,
                year=1954,
                start=0,
                end=37,
            ),
            "Brown v. Board of Education, 347 U.S. 483, 484 (1954)",
        ),
        (
            CaselawCitation(
                case_name="T v. B.",
                volume=300,
                reporter="F.3d",
                starting_page=87,
                raw_court="2d Cir.",
                year=1989,
                start=0,
                end=37,
            ),
            "T v. B., 300 F.3d 87 (2d Cir. 1989)",
        ),
    ],
)
def test_caselaw_citation_full_text(citation, expected):
    assert citation.full_text == expected


@pytest.mark.parametrize(
    "citation, expected",
    [
        (
            StatuteCitation(
                title="California Civil Code",
                code="Cal. Civ. Code",
                section="1080",
                year=2021,
                start=0,
                end=27,
            ),
            "California Civil Code Cal. Civ. Code § 1080 (2021)",
        ),
        (
            StatuteCitation(
                code="Cal. Civ. Code",
                section="1080",
                year=2021,
                start=0,
                end=27,
            ),
            "Cal. Civ. Code § 1080 (2021)",
        ),
        (
            StatuteCitation(
                code="Gov't Code",
                section="1080",
                start=0,
                end=27,
            ),
            "Gov't Code § 1080",
        ),
        (
            StatuteCitation(
                section="1080",
                start=0,
                end=27,
            ),
            "§ 1080",
        ),
    ],
)
def test_statute_citation_full_text(citation, expected):
    assert citation.full_text == expected
