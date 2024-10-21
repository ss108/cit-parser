import string
from typing import List

from .types import LabelPrediction


def aggregate_entities(labels: List[LabelPrediction]) -> List[LabelPrediction]:
    """
    Aggregate tokens into entities based on their labels.
    """
    aggregated = []
    current_entity_tokens = []
    current_label = None

    for pair in labels:
        token = pair.token
        label = pair.label

        # Skip special tokens
        if token in ["[CLS]", "[SEP]", "[PAD]"] or label == "O":
            continue

        # Handle 'B-' labels as the start of a new entity
        if label.startswith("B-"):
            label_type = label[2:]

            # Save any existing entity before starting a new one
            if current_entity_tokens and current_label:
                aggregated.append(
                    LabelPrediction(
                        token="".join(current_entity_tokens).replace(" ##", ""),
                        label=current_label,
                    )
                )
                current_entity_tokens = []

            current_label = label_type
            # Add the token, removing '##' if it's a subword.
            current_entity_tokens.append(token.replace("##", ""))
        elif label.startswith("I-") and current_label == label[2:]:
            # If the token is a subword, add it directly.
            if token.startswith("##"):
                current_entity_tokens.append(token[2:])
            elif token in string.punctuation:
                # Attach punctuation directly without space.
                current_entity_tokens[-1] += token
            else:
                # Add a space before non-subword continuation tokens.
                current_entity_tokens.append(" " + token)
        else:
            # Handle 'O' labels or labels not continuing the current entity
            if current_entity_tokens and current_label:
                aggregated.append(
                    LabelPrediction(
                        token="".join(current_entity_tokens).replace(" ##", ""),
                        label=current_label,
                    )
                )
                current_entity_tokens = []
                current_label = None

    # Add any remaining entity
    if current_entity_tokens and current_label:
        aggregated.append(
            LabelPrediction(
                token="".join(current_entity_tokens).replace(" ##", ""),
                label=current_label,
            )
        )

    return aggregated
