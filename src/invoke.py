from functools import lru_cache
from typing import Dict, List, Optional

import spacy
import torch
from transformers import (
    AutoModelForTokenClassification,
    AutoTokenizer,
    PreTrainedTokenizerFast,
)
from wasabi import msg

from src.config import Config
from src.constants import ALL_LABELS
from src.postprocess import labels_to_cit

from .types import Citation, LabelPrediction


def _get_device() -> torch.device:
    """
    Detects if CUDA or MPS is available and returns the appropriate device.
    Defaults to CPU if neither is available.
    """
    if torch.cuda.is_available():
        device = torch.device("cuda")
        msg.info("CUDA is available; using GPU for inference.")
    elif torch.backends.mps.is_available() and torch.backends.mps.is_built():
        device = torch.device("mps")
        msg.info("MPS is available; using MPS for inference.")
    else:
        device = torch.device("cpu")
        msg.warn("No GPU found :(\nUsing CPU for inference.")
    return device


DEVICE = _get_device()


@lru_cache(maxsize=1)
def _nlp():
    try:
        return spacy.load("en_core_web_sm")
    except OSError:
        msg.fail(
            "SpaCy model 'en_core_web_sm' not found. Please run `python -m spacy download en_core_web_sm`."
        )
        raise


@lru_cache(maxsize=1)
def _get_model() -> AutoModelForTokenClassification:
    """
    Loads the model from the pretrained Hugging Face repository and moves it to the appropriate device.
    """
    model = AutoModelForTokenClassification.from_pretrained(Config.HF_MODEL_NAME)
    model.to(DEVICE)
    model.eval()
    msg.info(f"Model '{Config.HF_MODEL_NAME}' loaded and moved to {DEVICE}.")
    return model


@lru_cache(maxsize=1)
def _get_tokenizer() -> PreTrainedTokenizerFast:
    """
    Loads the tokenizer from the pretrained Hugging Face repository.
    """
    tokenizer = AutoTokenizer.from_pretrained(Config.HF_MODEL_NAME)
    assert isinstance(
        tokenizer, PreTrainedTokenizerFast
    ), "Tokenizer is not a PreTrainedTokenizerFast instance."
    msg.info(f"Tokenizer for '{Config.HF_MODEL_NAME}' loaded.")
    return tokenizer


def split_text(text: str) -> List[str]:
    """
    Splits the input text into sentences using spaCy.
    """
    nlp = _nlp()
    doc = nlp(text)
    sentences: List[str] = [sent.text for sent in doc.sents]
    msg.info(f"Text split into {len(sentences)} sentence(s).")
    return sentences


def invoke(text: str) -> List[Citation]:
    model = _get_model()
    sentences = split_text(text)
    res = []
    for sentence in sentences:
        predictions = infer_labels(sentence, model)
        cit: Optional[Citation] = labels_to_cit(predictions, sentence)
        if cit:
            res.append(cit)
    return res


def tokenize(s: str) -> Dict[str, torch.Tensor]:
    tokenizer: PreTrainedTokenizerFast = _get_tokenizer()
    tokenized_input = tokenizer(
        s,
        return_tensors="pt",
        padding=True,
    )  # pyright: ignore
    tokenized_input: Dict[str, torch.Tensor] = {
        k: v.to(DEVICE) for k, v in tokenized_input.items()
    }

    # tokens = tokenizer.convert_ids_to_tokens(tokenized_input["input_ids"][0])  # pyright: ignore
    # msg.info(f"Tokenized input: {tokens}")
    return tokenized_input


def infer_labels(
    text: str, model: AutoModelForTokenClassification
) -> List[LabelPrediction]:
    """
    Tokenizes the text, performs inference with the model, and returns predicted labels
    along with their character spans using offset mapping.
    """
    tokenizer: PreTrainedTokenizerFast = _get_tokenizer()

    # Tokenize with offset mapping to keep track of token positions
    tokenized_input = tokenizer(
        text, return_offsets_mapping=True, truncation=True, return_tensors="pt"
    )

    # Extract offset mapping before moving tensors to device
    offset_mapping = tokenized_input.pop("offset_mapping")[0].tolist()

    tokenized_input = {k: v.to(DEVICE) for k, v in tokenized_input.items()}

    model.to(DEVICE)  # pyright: ignore
    model.eval()  # pyright: ignore

    with torch.no_grad():
        outputs = model(**tokenized_input)  # pyright: ignore
        logits = outputs.logits
        predictions = torch.argmax(logits, dim=-1)

    predicted_labels = [ALL_LABELS[p] for p in predictions[0].tolist()]
    tokens = tokenizer.convert_ids_to_tokens(tokenized_input["input_ids"][0])

    res = []
    raw_pairs = []

    for token, label, (start, end) in zip(tokens, predicted_labels, offset_mapping):
        if token in ["[CLS]", "[SEP]", "[PAD]"] or label == "O" or start == end:
            continue

        token = token.replace("##", "")

        p = LabelPrediction(token=token, label=label, start=start, end=end)
        res.append(p)
        raw_pairs.append((token, label, start, end))

    msg.info(f"Token-label pairs with spans: {raw_pairs}")

    return res
