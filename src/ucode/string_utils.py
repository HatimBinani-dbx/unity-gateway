"""Shared string helpers."""

from __future__ import annotations


def is_valid_catalog_schema(value: str) -> bool:
    """Return whether value is a safe ``<catalog>.<schema>`` reference."""
    parts = value.split(".")
    return len(parts) == 2 and all(
        part
        and part.isprintable()
        and not any(character.isspace() or character == "/" for character in part)
        for part in parts
    )


_MODEL_LABEL_ACRONYMS = frozenset({"glm", "gpt"})
_MODEL_LABEL_WORDS = {"deepseek": "DeepSeek"}


def model_picker_label(model: str) -> str:
    """A human-friendly picker label for a model id (e.g. ``system.ai.claude-haiku-4-5`` ->
    ``Claude Haiku 4.5``): keep the vendor and name words title-cased, uppercase known acronyms,
    and join a run of numeric segments into a dotted version, also after a word that ends in one
    (``kimi-k3-1-pro`` -> ``Kimi K3.1 Pro``)."""
    stem = model.removeprefix("system.ai.")
    parts: list[str] = []
    version: list[str] = []
    for token in stem.split("-"):
        if token.isdigit():
            if not version and parts and parts[-1][-1].isdigit():
                parts[-1] = f"{parts[-1]}.{token}"
            else:
                version.append(token)
            continue
        if version:
            parts.append(".".join(version))
            version = []
        if token in _MODEL_LABEL_ACRONYMS:
            parts.append(token.upper())
        else:
            parts.append(_MODEL_LABEL_WORDS.get(token, token.title()))
    if version:
        parts.append(".".join(version))
    return " ".join(parts) if parts else stem
