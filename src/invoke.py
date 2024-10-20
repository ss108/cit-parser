from functools import lru_cache

import spacy
import torch
from transformers import AutoModelForTokenClassification, BertTokenizerFast
from wasabi import msg

from src.config import Config
from src.constants import ALL_LABELS


@lru_cache(maxsize=1)
def _nlp():
    return spacy.load("en_core_web_sm")


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


@lru_cache(maxsize=1)
def _get_model() -> AutoModelForTokenClassification:
    model = AutoModelForTokenClassification.from_pretrained(Config.HF_MODEL_NAME)
    device = _get_device()
    model.to(device)
    model.eval()
    return model


def split_text(text: str) -> list[str]:
    """
    Split text into sentences using spaCy.
    """
    nlp = _nlp()
    doc = nlp(text)
    sentences: list[str] = [sent.text for sent in doc.sents]
    return sentences


def tokenize(text: str) -> dict[str, torch.Tensor]:
    tokenizer = BertTokenizerFast.from_pretrained(Config.HF_MODEL_NAME)
    return tokenizer(
        text,
        add_special_tokens=True,
        padding="max_length",
        truncation=True,
        max_length=512,
        return_attention_mask=True,
        return_tensors="pt",
    )


async def invoke(text: str):
    if Config.MODEL_URL:
        ...

    msg.info("No URL configured; using model locally")
    text_chunks = split_text(text)
    tokenized = [tokenize(chunk) for chunk in text_chunks]
    print(tokenized)


def get_labels(tokenized_text: dict[str, torch.Tensor]) -> list[str]:
    model = _get_model()

    with torch.no_grad():
        output = model(**tokenized_text)  # pyright: ignore

    logits = output.logits
    predictions = logits.argmax(dim=-1)
    predicted_labels = [ALL_LABELS[p] for p in predictions[0].tolist()]
    return predicted_labels

    # tokens = tokenizer.convert_ids_to_tokens(tokenized_input["input_ids"][0])  # pyright: ignore
