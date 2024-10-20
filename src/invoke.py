from functools import lru_cache

import spacy
from transformers import BertTokenizerFast

# import torch
from src.config import Config


@lru_cache(maxsize=1)
def _nlp():
    return spacy.load("en_core_web_sm")


def split_text(text: str) -> list[str]:
    """
    Split text into sentences using spaCy.
    """
    nlp = _nlp()
    doc = nlp(text)
    sentences: list[str] = [sent.text for sent in doc.sents]
    return sentences


def tokenize(text: str) -> dict:
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
    text_chunks = split_text(text)
    tokenized = [tokenize(chunk) for chunk in text_chunks]
