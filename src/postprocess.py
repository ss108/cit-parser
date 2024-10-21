import string
from typing import List, Optional

from .types import CaselawCitation, ICitation, LabelPrediction, StatuteCitation


def labels_to_cit(labels: List[LabelPrediction]) -> Optional[ICitation]:
    entities = aggregate_entities(labels)

    if is_caselaw_citation(entities):
        return CaselawCitation.from_token_label_pairs(entities)
    elif is_statute_citation(entities):
        return StatuteCitation.from_token_label_pairs(entities)
    else:
        return None


# Neither of the below seem good, but there is basically no mainstream language that offers a good way of declaratively handling this kind of thing (but I think can be done in Idris?)
def is_caselaw_citation(entities: List[LabelPrediction]) -> bool:
    """
    Determines if the given combination of labels constitute a caselaw citation.
    """
    has_case_name = any(e.label == "CASE_NAME" for e in entities)
    has_volume = any(e.label == "VOLUME" for e in entities)
    has_reporter = any(e.label == "REPORTER" for e in entities)
    return has_case_name and (has_volume or has_reporter)


def is_statute_citation(entities: List[LabelPrediction]) -> bool:
    """
    Determines if the given combination of labels constitute a statute citation.
    """
    has_section = any(e.label == "SECTION" for e in entities)
    return has_section


def aggregate_entities(labels: List[LabelPrediction]) -> List[LabelPrediction]:
    """
    Aggregate tokens into entities based on their labels, handling subwords and punctuation.
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
                aggregated.append(
                    LabelPrediction(
                        token="".join(current_entity_tokens),
                        label=current_label,
                        start=current_start,
                        end=current_end,
                    )
                )
                current_entity_tokens = []
                current_start = None
                current_end = None

            current_label = label_type
            token = token.replace("##", "")
            current_entity_tokens.append(token)
            current_start = pair.start
            current_end = pair.end
        elif label.startswith("I-") and current_label == label[2:]:
            # Continuation of the current entity
            if token.startswith("##"):
                current_entity_tokens.append(token[2:])
            elif token in string.punctuation:
                if current_entity_tokens:
                    current_entity_tokens[-1] += token
            else:
                # Add a space before non-subword continuation tokens if needed
                if not (len(token) == 1 and token.isupper()):
                    if (
                        current_entity_tokens
                        and current_entity_tokens[-1].endswith(".")
                        and token.isdigit()
                    ):
                        current_entity_tokens.append(token)
                    elif (
                        current_entity_tokens
                        and current_entity_tokens[-1].isdigit()
                        and token.islower()
                    ):
                        current_entity_tokens.append(token)
                    else:
                        current_entity_tokens.append(" " + token)
                else:
                    current_entity_tokens.append(token)

            # Update the start and end positions
            if current_start is not None:
                current_start = min(current_start, pair.start)
            if current_end is not None:
                current_end = max(current_end, pair.end)
        else:
            # Handle any other case, end current entity
            if (
                current_entity_tokens
                and current_label
                and current_start is not None
                and current_end is not None
            ):
                aggregated.append(
                    LabelPrediction(
                        token="".join(current_entity_tokens),
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
        aggregated.append(
            LabelPrediction(
                token="".join(current_entity_tokens),
                label=current_label,
                start=current_start,
                end=current_end,
            )
        )

    return aggregated
