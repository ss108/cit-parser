from __future__ import annotations

from typing import Optional, Protocol, Tuple, TypeAlias

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

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, LabelPrediction):
            return False
        return self.token == other.token and self.label == other.label

    def __str__(self):
        return f"{self.token}: {self.label}"


# class CaselawCitation(BaseModel):
#     case_name: str
#     volume: Optional[int] = None
#     reporter: str
#     starting_page: Optional[int] = None
#     raw_pin_cite: Optional[str] = None
#     court: Optional[str] = None
#     year: Optional[int] = None

#     @classmethod
#     def from_token_label_pairs(
#         cls, token_label_pairs: List[LabelPrediction]
#     ) -> Optional[CaselawCitation]:
#         # data = cls()
#         case_name = ""
#         reporter = ""
#         for pair in token_label_pairs:
#             token = pair.token.replace("##", "")
#             label = pair.label

#             if label == "CASE_NAME":
#                 data.case_name += token + " "
#             elif label == "VOLUME":
#                 if token.isdigit():
#                     data.volume = int(token)
#             elif label == "REPORTER":
#                 data.reporter += token + " "
#             elif label == "PAGE":
#                 if token.isdigit():
#                     data.starting_page = int(token)
#             elif label == "PIN":
#                 data.raw_pin_cite = token
#             elif label == "COURT":
#                 data.court = token
#             elif label == "YEAR":
#                 if token.isdigit():
#                     data.year = int(token)

#         # Trim whitespace
#         data.case_name = data.case_name.strip()
#         data.reporter = data.reporter.strip()

#         # Validate required fields
#         if not data.case_name or not data.volume or not data.reporter:
#             return None

#         return data
