"""SheetsFinance catalog fuzzy search."""

from __future__ import annotations

import re
from functools import lru_cache
from typing import Any, Dict, List

from .sf_catalog import OTHER_FUNCTIONS, SF_CATEGORIES

STOPWORDS = {"the", "a", "of", "in", "for"}
_CAMEL_RE = re.compile(r"([a-z0-9])([A-Z])")
_SPLIT_RE = re.compile(r"[^a-z0-9]+")
_SF_CATEGORY_PRIORITY = {
    "income": 0,
    "cashflow": 1,
    "balancesheet": 2,
    "ratios": 3,
    "estimates": 4,
}


def _split_camel(text: str) -> str:
    return _CAMEL_RE.sub(r"\1 \2", text)


def _tokenize(text: str) -> List[str]:
    normalized = _split_camel(text).replace("_", " ").lower()
    tokens = [t for t in _SPLIT_RE.split(normalized) if t and t not in STOPWORDS]
    return tokens


def _build_type_hint(type_values: List[str]) -> str:
    if len(type_values) <= 1:
        return ""

    annual = type_values[0]
    quarterly = next((value for value in type_values if value.endswith("Q")), "")
    trailing = next((value for value in type_values if value.endswith("TTM")), "")
    quarter_specific = [value for value in type_values if re.search(r"Q[1-4]$", value)]

    parts: List[str] = [f"Use '{annual}' for annual"]
    if quarterly:
        parts.append(f"'{quarterly}' for quarterly")
    if trailing:
        parts.append(f"'{trailing}' for trailing")
    if quarter_specific:
        variants = ", ".join(f"'{value}'" for value in quarter_specific)
        parts.append(f"{variants} for quarter-specific data")

    return ", ".join(parts)


@lru_cache(maxsize=1)
def _build_index() -> List[Dict[str, Any]]:
    entries: List[Dict[str, Any]] = []

    for category_name, category in SF_CATEGORIES.items():
        type_hint = _build_type_hint(category.type_values)
        legacy_type_terms = list(category.legacy_types.keys())
        legacy_words = [word for legacy in legacy_type_terms for word in _tokenize(legacy)]
        for metric in category.metrics:
            metric_id = f"SF.{category_name}.{metric.name}"
            alias_words = [a for alias in metric.aliases for a in _tokenize(alias)]
            searchable_parts = [
                metric.name,
                _split_camel(metric.name),
                category_name,
                category.display_name,
                metric.description,
                *metric.aliases,
                *alias_words,
                *legacy_type_terms,
                *legacy_words,
            ]
            entries.append(
                {
                    "metric_id": metric_id,
                    "function": "SF",
                    "category": category_name,
                    "priority": _SF_CATEGORY_PRIORITY.get(category_name, 50),
                    "display_name": category.display_name,
                    "metric": metric.name,
                    "description": metric.description,
                    "type_hint": type_hint,
                    "example": category.example,
                    "searchable_text": " ".join(searchable_parts).lower(),
                    "metric_name_lc": metric.name.lower(),
                    "alias_lc": [a.lower() for a in metric.aliases],
                }
            )

    for function_name, function in OTHER_FUNCTIONS.items():
        for metric in function.metrics:
            metric_id = f"{function_name}.{metric.name}"
            alias_words = [a for alias in metric.aliases for a in _tokenize(alias)]
            searchable_parts = [
                metric.name,
                _split_camel(metric.name),
                function_name,
                metric.description,
                function.notes,
                *metric.aliases,
                *alias_words,
            ]
            entries.append(
                {
                    "metric_id": metric_id,
                    "function": function_name,
                    "category": None,
                    "priority": 100,
                    "display_name": function_name.replace("_", " ").title(),
                    "metric": metric.name,
                    "description": metric.description,
                    "type_hint": "",
                    "example": function.example,
                    "searchable_text": " ".join(searchable_parts).lower(),
                    "metric_name_lc": metric.name.lower(),
                    "alias_lc": [a.lower() for a in metric.aliases],
                }
            )

    return entries


def _score_entry(
    query_normalized: str,
    query_tokens: List[str],
    entry: Dict[str, Any],
) -> int:
    score = 0
    metric_name = entry["metric_name_lc"]
    aliases = entry["alias_lc"]
    searchable_text = entry["searchable_text"]

    if query_normalized == metric_name:
        score += 100
    elif query_normalized and query_normalized in metric_name:
        score += 50

    if query_normalized in aliases:
        score += 80
    elif any(query_normalized and query_normalized in alias for alias in aliases):
        score += 30

    for token in sorted(set(query_tokens)):
        if token in searchable_text:
            score += 10

    return score


def sf_search(query: str, limit: int = 10) -> Dict[str, Any]:
    """Search the SheetsFinance catalog and return ranked metric matches."""
    if not isinstance(query, str) or not query.strip():
        return {"status": "error", "error": "query must be a non-empty string"}

    if not isinstance(limit, int) or limit <= 0:
        return {"status": "error", "error": "limit must be a positive integer"}

    query_normalized = query.strip().lower()
    query_tokens = _tokenize(query)

    ranked: List[Dict[str, Any]] = []
    for entry in _build_index():
        score = _score_entry(query_normalized, query_tokens, entry)
        if score < 10:
            continue
        ranked.append(
            {
                "metric_id": entry["metric_id"],
                "function": entry["function"],
                "metric": entry["metric"],
                "category": entry["category"],
                "priority": entry["priority"],
                "display_name": entry["display_name"],
                "description": entry["description"],
                "type_hint": entry["type_hint"],
                "example": entry["example"],
                "score": score,
            }
        )

    ranked.sort(key=lambda row: (-row["score"], row["priority"], row["metric_id"]))
    results = ranked[:limit]
    for row in results:
        row.pop("priority", None)
    return {"status": "ok", "results": results, "count": len(results)}


__all__ = ["sf_search"]
