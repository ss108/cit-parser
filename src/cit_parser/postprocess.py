from typing import List, Optional

from .types import (
    Authorities,
    CaselawCitation,
    Citation,
    LabelPrediction,
    StatuteCitation,
)


def labels_to_cit(
    labels: List[LabelPrediction], original_text: str
) -> Optional[Citation]:
    entities = aggregate_entities(labels, original_text)

    if _is_caselaw_citation(entities):
        return CaselawCitation.from_token_label_pairs(entities)
    elif _is_statute_citation(entities):
        return StatuteCitation.from_token_label_pairs(entities)
    else:
        return None


# Neither of the below seem good, but there is basically no mainstream language that offers a good way of declaratively and succinctly handling this kind of thing
def _is_caselaw_citation(entities: List[LabelPrediction]) -> bool:
    """
    Determines if the given combination of labels constitute a caselaw citation.
    """
    has_case_name = any(e.label == "CASE_NAME" for e in entities)
    has_volume = any(e.label == "VOLUME" for e in entities)
    has_reporter = any(e.label == "REPORTER" for e in entities)
    return has_case_name and (has_volume or has_reporter)


def _is_statute_citation(entities: List[LabelPrediction]) -> bool:
    """
    Determines if the given combination of labels constitute a statute citation.
    """
    has_section = any(e.label == "SECTION" for e in entities)
    return has_section


# def _construct_label(start: int) -> LabelPrediction:
#     return LabelPrediction(token="", label="", start=start, end=start)


# def _combine_labels(
#     labels: List[LabelPrediction], original_text: str
# ) -> Optional[LabelPrediction]:
#     """
#     Squash the labels to remove subword tokens and combine them into a single token.
#     """
#     if len(labels) == 0:
#         return None

#     conbine_label: LabelPrediction = labels[0]

#     for x in labels[1:]:
#         combine_label

#         if token.startswith("##"):
#             current_label.token += token[2:]
#             current_label.end = end
#         else:
#             if current_label.token:
#                 squashed.append(current_label)
#             current_label = LabelPrediction(token=token, label=x, start=start, end=end)

#     if current_label.token:
#         squashed.append(current_label)

#     return squashed


def aggregate_entities(
    labels: List[LabelPrediction], original_text: str
) -> List[LabelPrediction]:
    """
    Aggregate tokens into entities based on their labels, handling subwords and punctuation.
    Uses the original text for precise reconstruction of entities.
    """
    current_start: int = 0
    current_end: int = 0
    VALID_CLASSIFICATIONS = {
        "CASE_NAME",
        "VOLUME",
        "REPORTER",
        "PAGE",
        "COURT",
        "SECTION",
        "PIN",
        "TITLE",
        "CODE",
        "YEAR",
    }

    res: List[LabelPrediction] = []

    current_label: Optional[str] = None

    for i, pair in enumerate(labels):
        label = pair.label
        token = pair.token

        if token in ["[CLS]", "[SEP]", "[PAD]"] or label == "O":
            if current_label:
                res.append(
                    LabelPrediction(
                        token=original_text[current_start:current_end].strip(),
                        label=current_label,
                        start=current_start,
                        end=current_end,
                    )
                )
            current_label = None
            continue

        if label.startswith("B-"):
            classification = label[2:]

            if classification not in VALID_CLASSIFICATIONS:
                continue

            if current_label:
                res.append(
                    LabelPrediction(
                        token=original_text[current_start:current_end].strip(),
                        label=current_label,
                        start=current_start,
                        end=current_end,
                    )
                )

            current_label = classification
            current_start = pair.start
            current_end = pair.end

        elif label.startswith("I-"):
            if not current_label or label[2:] != current_label:
                continue

            current_end = pair.end
        else:
            if current_label:
                res.append(
                    LabelPrediction(
                        token=original_text[current_start:current_end].strip(),
                        label=current_label,
                        start=current_start,
                        end=current_end,
                    )
                )

        if i == len(labels) - 1 and current_label is not None:
            res.append(
                LabelPrediction(
                    token=original_text[current_start:current_end].strip(),
                    label=current_label,
                    start=current_start,
                    end=current_end,
                )
            )

    return res


def organize(cits: List[Citation]) -> Authorities:
    return Authorities.construct(cits)
