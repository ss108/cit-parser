from __future__ import annotations

from typing import List, Optional, Protocol, Tuple, TypeAlias

from pydantic import BaseModel

PIN_CITE: TypeAlias = Tuple[int, Optional[int]]
SPAN: TypeAlias = Tuple[int, int]


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


class CaselawCitation(BaseModel):
    case_name: str
    volume: Optional[int] = None
    reporter: Optional[str] = None
    starting_page: Optional[int] = None
    raw_pin_cite: Optional[str] = None
    court: Optional[str] = None
    year: Optional[int] = None

    start: int
    end: int

    @property
    def span(self) -> SPAN:
        return self.start, self.end

    @property
    def full_text(self) -> str:
        components = [self.case_name]

        if self.volume:
            components.append(str(self.volume))
        if self.reporter:
            components.append(self.reporter)
        if self.starting_page:
            components.append(str(self.starting_page))

        if self.raw_pin_cite:
            components.append(f"at {self.raw_pin_cite}")

        if self.court or self.year:
            parens_content = " ".join(
                filter(None, [self.court, str(self.year) if self.year else None])
            )
            components.append(f"({parens_content})")

        return " ".join(components)

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
            court=court,
            year=year,
            start=start,
            end=end,
        )

    def __hash__(self) -> int:
        return hash((self.case_name, self.volume, self.reporter, self.start, self.end))

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, CaselawCitation):
            return False
        return (
            self.case_name == other.case_name
            and self.volume == other.volume
            and self.reporter == other.reporter
            and self.starting_page == other.starting_page
            and self.raw_pin_cite == other.raw_pin_cite
            and self.court == other.court
            and self.year == other.year
        )


class StatuteCitation(BaseModel):
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
    def full_text(self) -> str:
        components = []
        if self.title:
            components.append(self.title)
        if self.code:
            components.append(self.code)
        if self.section:
            components.append(self.section)
        if self.year:
            components.append(f"({self.year})")

        return " ".join(components)

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

    def __hash__(self) -> int:
        return hash((self.title, self.code, self.section, self.start, self.end))

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, StatuteCitation):
            return False
        return (
            self.title == other.title
            and self.code == other.code
            and self.section == other.section
            and self.year == other.year
        )
