import string
from typing import List

from .types import LabelPrediction


def aggregate_entities(labels: List[LabelPrediction]) -> List[LabelPrediction]:
    """
    Aggregate tokens into entities based on their labels, handling subwords and punctuation.
    """
    aggregated = []
    current_entity_tokens = []
    current_label = None

    for pair in labels:
        token = pair.token
        label = pair.label

        # Skip special tokens and 'O' labels
        if token in ["[CLS]", "[SEP]", "[PAD]"] or label == "O":
            continue

        if label.startswith("B-"):
            # Start of a new entity
            label_type = label[2:]

            # Save the previous entity if exists
            if current_entity_tokens and current_label:
                aggregated.append(
                    LabelPrediction(
                        token="".join(current_entity_tokens),
                        label=current_label,
                    )
                )
                current_entity_tokens = []

            # Initialize new entity
            current_label = label_type
            token = token.replace("##", "")
            current_entity_tokens.append(token)
        elif label.startswith("I-") and current_label == label[2:]:
            # Continuation of the current entity
            if token.startswith("##"):
                # Subword token: concatenate directly
                current_entity_tokens.append(token[2:])
            elif token in string.punctuation:
                # Punctuation: attach directly to the last token
                if current_entity_tokens:
                    current_entity_tokens[-1] += token
            else:
                # Non-subword, non-punctuation: add with a space unless single uppercase
                if not (len(token) == 1 and token.isupper()):
                    # Check for special cases where space should not be added
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
        else:
            # Any other case, end current entity
            if current_entity_tokens and current_label:
                aggregated.append(
                    LabelPrediction(
                        token="".join(current_entity_tokens),
                        label=current_label,
                    )
                )
                current_entity_tokens = []
                current_label = None

    # Append the last entity if exists
    if current_entity_tokens and current_label:
        aggregated.append(
            LabelPrediction(
                token="".join(current_entity_tokens),
                label=current_label,
            )
        )

    return aggregated
