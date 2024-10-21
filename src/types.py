from __future__ import annotations

from typing import List, Optional, Protocol, Tuple, TypeAlias

from pydantic import BaseModel

PIN_CITE: TypeAlias = Tuple[int, Optional[int]]
SPAN: TypeAlias = Tuple[int, int]


class ICitation(Protocol):
    start: int
    end: int

    @classmethod
    def from_token_label_pairs(
        cls, token_label_pairs: list[LabelPrediction]
    ) -> Optional[ICitation]: ...

    @property
    def full_text(self) -> str: ...

    @property
    def span(self) -> SPAN: ...

    def __hash__(self) -> int: ...

    def __eq__(self, other: object) -> bool: ...


class LabelPrediction(BaseModel):
    token: str
    label: str
    start: int
    end: int

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, LabelPrediction):
            return False
        return self.token == other.token and self.label == other.label

    def __str__(self):
        return f"{self.token}: {self.label}"


class CaselawCitation(BaseModel):
    case_name: str
    volume: Optional[int] = None
    reporter: Optional[str] = None
    starting_page: Optional[int] = None
    raw_pin_cite: Optional[str] = None
    court: Optional[str] = None
    year: Optional[int] = None

    @classmethod
    def from_token_label_pairs(
        cls, token_label_pairs: List[LabelPrediction]
    ) -> Optional[CaselawCitation]:
        # Initialize fields
        case_name = ""
        reporter = ""
        volume = None
        starting_page = None
        raw_pin_cite = None
        court = None
        year = None

        for pair in token_label_pairs:
            token = pair.token
            label = pair.label

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
            court=court,
            year=year,
        )


class StatuteCitation(BaseModel):
    title: Optional[str] = None
    code: Optional[str] = None
    section: Optional[str] = None
    year: Optional[int] = None

    @classmethod
    def from_token_label_pairs(
        cls, token_label_pairs: List[LabelPrediction]
    ) -> Optional[StatuteCitation]:
        title = ""
        code = ""
        section = ""
        year = None

        for pair in token_label_pairs:
            token = pair.token
            label = pair.label

            if label == "TITLE":
                title += token + " "
            elif label == "CODE":
                code += token + " "
            elif label == "SECTION":
                section += token + " "
            elif label == "YEAR" and token.isdigit():
                year = int(token)

        # Trim whitespace
        title = title.strip() or None
        code = code.strip() or None
        section = section.strip() or None

        # Validate required fields
        if not title and not code and not section:
            return None

        return cls(
            title=title,
            code=code,
            section=section,
            year=year,
        )
