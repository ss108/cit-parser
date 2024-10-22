from __future__ import annotations

from enum import Enum
from itertools import chain
from typing import (
    Annotated,
    Dict,
    List,
    Literal,
    Optional,
    Tuple,
    TypeAlias,
    Union,
)

from pydantic import BaseModel, ConfigDict, Field

PIN_CITE: TypeAlias = Tuple[int, Optional[int]]
SPAN: TypeAlias = Tuple[int, int]


class _Base_(BaseModel):
    model_config = ConfigDict(
        frozen=True,
        arbitrary_types_allowed=True,
        use_enum_values=True,
    )


class CitationType(str, Enum):
    OPINION = "opinion"
    STATUTE = "statute"


class LabelPrediction(_Base_):
    token: str
    label: str
    start: int
    end: int

    @property
    def span(self) -> SPAN:
        return self.start, self.end

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, LabelPrediction):
            return False
        return self.token == other.token and self.label == other.label

    def __str__(self):
        return f"{self.token}: {self.label}"


class CaselawCitation(_Base_):
    citation_type: Literal[CitationType.OPINION] = CitationType.OPINION

    case_name: str
    volume: Optional[int] = None
    reporter: Optional[str] = None
    starting_page: Optional[int] = None
    raw_pin_cite: Optional[str] = None
    raw_court: Optional[str] = None
    year: Optional[int] = None

    start: int
    end: int

    @property
    def span(self) -> SPAN:
        return self.start, self.end

    @property
    def formatted_court(self) -> Optional[str]:
        # handle SCOTUS speshul
        if self.reporter in {"U.S.", "S. Ct."}:
            return "SCOTUS"
        return self.raw_court

    @property
    def is_full(self) -> bool:
        return all(
            [
                self.case_name,
                self.volume,
                self.reporter,
                self.starting_page,
                self.formatted_court,
                self.year,
            ]
        )

    @property
    def full_text(self) -> str:
        components = [f"{self.case_name},"]

        if self.volume:
            components.append(str(self.volume))
        if self.reporter:
            components.append(self.reporter)
        if self.starting_page:
            components.append(str(self.starting_page))

        if self.raw_pin_cite:
            if self.is_full:
                components[-1] += ","
                components.append(self.raw_pin_cite)
            else:
                components.append(f"at {self.raw_pin_cite}")

        if self.raw_court or self.year:
            parens_content = " ".join(
                filter(None, [self.raw_court, str(self.year) if self.year else None])
            )
            components.append(f"({parens_content})")

        return " ".join(components)

    def __str__(self) -> str:
        return self.full_text

    @classmethod
    def from_token_label_pairs(
        cls, token_label_pairs: List[LabelPrediction]
    ) -> Optional[CaselawCitation]:
        case_name = ""
        reporter = ""
        volume = None
        starting_page = None
        raw_pin_cite = None
        court = None
        year = None
        start = 0
        end = 0

        for i, pair in enumerate(token_label_pairs):
            token = pair.token
            label = pair.label

            if i == 0:
                start = pair.start
            if i == len(token_label_pairs) - 1:
                end = pair.end

            if label == "CASE_NAME":
                case_name += token + " "
            elif label == "VOLUME" and token.isdigit():
                volume = int(token)
            elif label == "REPORTER":
                reporter += token + " "
            elif label == "PAGE" and token.isdigit():
                starting_page = int(token)
            elif label == "PIN":
                raw_pin_cite = token
            elif label == "COURT":
                court = token
            elif label == "YEAR" and token.isdigit():
                year = int(token)

        case_name = case_name.strip()
        reporter = reporter.strip()

        if not case_name:
            return None

        return cls(
            case_name=case_name,
            volume=volume,
            reporter=reporter or None,
            starting_page=starting_page,
            raw_pin_cite=raw_pin_cite,
            raw_court=court,
            year=year,
            start=start,
            end=end,
        )

    def __hash__(self) -> int:
        return hash((self.volume, self.reporter, self.starting_page))

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, CaselawCitation):
            return False

        return (
            self.volume == other.volume
            and self.reporter == other.reporter
            and self.starting_page == other.starting_page
            and self.raw_court == other.raw_court
            and self.year == other.year
        )


class StatuteCitation(_Base_):
    citation_type: Literal[CitationType.STATUTE] = CitationType.STATUTE

    title: Optional[str] = None
    code: Optional[str] = None
    section: str
    year: Optional[int] = None

    start: int
    end: int

    @property
    def span(self) -> SPAN:
        return self.start, self.end

    @property
    def is_full(self) -> bool:
        return self.section is not None

    @property
    def full_text(self) -> str:
        components = []
        if self.title:
            components.append(self.title)
        if self.code:
            components.append(self.code)
        if self.section:
            components.append(f"§ {self.section}")
        if self.year:
            components.append(f"({self.year})")

        return " ".join(components)

    def is_fuller_than(self, other: StatuteCitation) -> bool:
        if self.section and not other.section:
            return True
        elif self.title and not other.title:
            return True
        elif self.code and not other.code:
            return True
        elif self.year and not other.year:
            return True

        return False

    def __str__(self) -> str:
        return self.full_text

    def __hash__(self) -> int:
        return hash((self.code, self.section))

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, StatuteCitation):
            return False

        return (
            self.title == other.title
            and self.code == other.code
            and self.section == other.section
            and self.year == other.year
        )

    @classmethod
    def from_token_label_pairs(
        cls, token_label_pairs: List[LabelPrediction]
    ) -> Optional[StatuteCitation]:
        title = ""
        code = ""
        section = ""
        year = None
        start = 0
        end = 0

        for i, pair in enumerate(token_label_pairs):
            token = pair.token
            label = pair.label

            # Set start and end positions based on the first and last token positions
            if i == 0:
                start = pair.start
            if i == len(token_label_pairs) - 1:
                end = pair.end

            if label == "TITLE":
                title += token + " "
            elif label == "CODE":
                # Combine parts for the code field
                if token == ".":
                    code = code.rstrip() + "."
                else:
                    code += token + " "
            elif label == "SECTION":
                section += token + " "
            elif label == "YEAR" and token.isdigit():
                year = int(token)

        title = title.strip() or None
        code = code.strip() or None
        section = section.strip()

        if not section:
            return None

        return cls(
            title=title,
            code=code,
            section=section,
            year=year,
            start=start,
            end=end,
        )


Citation: TypeAlias = Annotated[
    Union[CaselawCitation, StatuteCitation], Field(discriminator="citation_type")
]


class Authorities(BaseModel):
    caselaw: Dict[CaselawCitation, List[CaselawCitation]] = {}
    statutes: Dict[StatuteCitation, List[StatuteCitation]] = {}

    def all(self, full_only: bool = False) -> List[Citation]:
        if full_only:
            return list(self.caselaw.keys()) + list(self.statutes.keys())
        else:
            return list(chain.from_iterable(self.caselaw.values())) + list(
                chain.from_iterable(self.statutes.values())
            )

    @classmethod
    def construct(cls, citations: List[Citation]) -> Authorities:
        caselaw: Dict[CaselawCitation, List[CaselawCitation]] = {}
        statutes: Dict[StatuteCitation, List[StatuteCitation]] = {}

        # Separate full and short citations
        full_citations = [c for c in citations if c.is_full]
        short_citations = [c for c in citations if not c.is_full]

        # Add full citations directly
        for full_citation in full_citations:
            if full_citation.citation_type == CitationType.OPINION:
                caselaw.setdefault(full_citation, []).append(full_citation)
            elif full_citation.citation_type == CitationType.STATUTE:
                # Add or replace the existing statute with a fuller one
                existing_citation = next(
                    (k for k in statutes if k.section == full_citation.section), None
                )
                if existing_citation:
                    if full_citation.is_fuller_than(existing_citation):
                        # Replace the key if the new one is "fuller"
                        citations_list = statutes.pop(existing_citation)
                        statutes[full_citation] = citations_list + [full_citation]
                    else:
                        # Add to the existing citation list
                        statutes[existing_citation].append(full_citation)
                else:
                    statutes[full_citation] = [full_citation]

        # Map short citations to the appropriate full citation.
        for short_citation in short_citations:
            if short_citation.citation_type == CitationType.OPINION:
                for full_citation in caselaw:
                    if (
                        full_citation.volume == short_citation.volume
                        and full_citation.reporter == short_citation.reporter
                    ):
                        caselaw[full_citation].append(short_citation)
                        break
            elif short_citation.citation_type == CitationType.STATUTE:
                # Try to find a matching full citation by section.
                matched = False
                for full_citation in statutes:
                    if full_citation.section == short_citation.section:
                        statutes[full_citation].append(short_citation)
                        matched = True
                        break

                # If no full citation is found, add it as its own key.
                if not matched:
                    statutes.setdefault(short_citation, []).append(short_citation)

        return cls(caselaw=caselaw, statutes=statutes)

    def __str__(self) -> str:
        return f"Statutes: {self.statutes}\nCaselaw: {self.caselaw}"
