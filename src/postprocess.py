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


def aggregate_entities(
    labels: List[LabelPrediction], original_text: str
) -> List[LabelPrediction]:
    """
    Aggregate tokens into entities based on their labels, handling subwords and punctuation.
    Uses the original text for precise reconstruction of entities.
    """
    aggregated = []
    current_entity_tokens = []
    current_label = None
    current_start: Optional[int] = None
    current_end: Optional[int] = None

    for pair in labels:
        token = pair.token
        label = pair.label

        if token in ["[CLS]", "[SEP]", "[PAD]"] or label == "O":
            continue

        if label.startswith("B-"):
            label_type = label[2:]

            # Save the previous entity if exists and has valid start/end
            if (
                current_entity_tokens
                and current_label
                and current_start is not None
                and current_end is not None
            ):
                # Construct the token from the original text using the spans
                corrected_token = original_text[current_start:current_end].strip()
                aggregated.append(
                    LabelPrediction(
                        token=corrected_token,
                        label=current_label,
                        start=current_start,
                        end=current_end,
                    )
                )
                current_entity_tokens = []
                current_start = None
                current_end = None

            current_label = label_type
            current_entity_tokens.append(token.replace("##", ""))
            current_start = pair.start
            current_end = pair.end
        elif label.startswith("I-") and current_label == label[2:]:
            # if len(current_entity_tokens) == 0:
            #     raise ValueError(
            #         f"Invalid sequence of labels: {current_label} followed by {label}"
            #     )
            # Continuation of the current entity
            if token.startswith("##"):
                current_entity_tokens.append(token[2:])
            else:
                current_entity_tokens.append(token)

            # Update the end position
            current_end = pair.end
        else:
            # Handle any other case, end current entity
            if (
                current_entity_tokens
                and current_label
                and current_start is not None
                and current_end is not None
            ):
                corrected_token = original_text[current_start:current_end].strip()
                aggregated.append(
                    LabelPrediction(
                        token=corrected_token,
                        label=current_label,
                        start=current_start,
                        end=current_end,
                    )
                )
                current_entity_tokens = []
                current_start = None
                current_end = None
                current_label = None

    # Add the last entity if exists and has valid start/end
    if (
        current_entity_tokens
        and current_label
        and current_start is not None
        and current_end is not None
    ):
        corrected_token = original_text[current_start:current_end].strip()
        aggregated.append(
            LabelPrediction(
                token=corrected_token,
                label=current_label,
                start=current_start,
                end=current_end,
            )
        )

    return aggregated


def organize(cits: List[Citation]) -> Authorities:
    print(f"Organizing {cits}")
    return Authorities.construct(cits)
