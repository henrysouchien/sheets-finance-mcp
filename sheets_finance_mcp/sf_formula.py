"""SheetsFinance formula builder and catalog describer."""

from __future__ import annotations

import difflib
from functools import lru_cache
from typing import Any, Dict, Iterable, List, Optional, Tuple

from .sf_catalog import OTHER_FUNCTIONS, SF_CATEGORIES

NON_SF_EXTRA_ARG_ORDER: Dict[str, List[str]] = {
    "SF_TIMESERIES": ["startDate", "endDate", "period"],
    "SF_DIVIDEND": ["startDate", "endDate"],
    "SF_OPTIONS": ["expirationDate"],
    "SF_CALENDAR": ["searchTerms", "startDate", "endDate"],
    "SF_SPARK": ["lastXdays"],
    "SF_TECHNICAL": ["timeframe", "startDate", "endDate"],
    "SF_NEWS": ["limit", "site", "startDate", "endDate"],
    "SF_SCREEN": ["filters", "metrics"],
    "SF_MAP": ["type", "filter"],
}

NON_US_SUFFIXES: Tuple[str, ...] = (
    ".L",
    ".OL",
    ".AS",
    ".MI",
    ".CO",
    ".PA",
    ".DE",
    ".HK",
    ".T",
    ".TO",
    ".SS",
    ".SZ",
    ".KS",
    ".TW",
    ".AX",
    ".SA",
)

NON_US_CURRENCY_NOTE = (
    "Note: Financial data for non-US tickers is reported in local currency (not USD). "
    "Check reporting currency before comparing."
)


def _closest_matches(value: str, candidates: Iterable[str], n: int = 5) -> List[str]:
    return difflib.get_close_matches(value, list(candidates), n=n)


@lru_cache(maxsize=1)
def _legacy_category_map() -> Dict[str, Tuple[str, str]]:
    """Map lowercased legacy type names to canonical category and type."""
    legacy_map: Dict[str, Tuple[str, str]] = {}
    for category_key, category_def in SF_CATEGORIES.items():
        for old_type, new_type in category_def.legacy_types.items():
            legacy_map[old_type.lower()] = (category_key, new_type)
    return legacy_map


def _format_formula_arg(value: Any) -> str:
    if isinstance(value, bool):
        return "TRUE" if value else "FALSE"
    if isinstance(value, (int, float)):
        return str(value)
    text = "" if value is None else str(value)
    escaped = text.replace('"', '\\"')
    return f'"{escaped}"'


def _build_formula(function_name: str, args: List[Any]) -> str:
    trimmed = list(args)
    while trimmed and (trimmed[-1] is None or trimmed[-1] == ""):
        trimmed.pop()
    rendered = ", ".join(_format_formula_arg(v) for v in trimmed)
    return f"={function_name}({rendered})"


def _parse_metric_id(metric_id: str) -> Tuple[str, Optional[str], str]:
    parts = metric_id.split(".")
    if len(parts) == 3 and parts[0] == "SF":
        return "SF", parts[1], parts[2]
    if len(parts) == 2 and parts[0] in OTHER_FUNCTIONS:
        return parts[0], None, parts[1]

    raise ValueError(
        "Invalid metric_id format. Expected 'SF.<category>.<metric>' "
        "or '<FUNCTION>.<metric>' for non-SF functions."
    )


def _parse_symbols(symbol: str) -> List[str]:
    if not isinstance(symbol, str) or not symbol.strip():
        raise ValueError("symbol must be a non-empty string")
    symbols = [item.strip() for item in symbol.split(",") if item.strip()]
    if not symbols:
        raise ValueError("symbol must include at least one ticker")
    return symbols


def _has_non_us_ticker_suffix(symbols: List[str]) -> bool:
    return any(symbol.upper().endswith(NON_US_SUFFIXES) for symbol in symbols)


def _append_note(payload: Dict[str, Any], note: str) -> None:
    existing = payload.get("notes", "")
    payload["notes"] = f"{existing} {note}".strip() if existing else note


def _resolve_category(
    category: str,
) -> Tuple[Optional[Dict[str, Any]], str, Optional[str], Optional[str]]:
    category_def = SF_CATEGORIES.get(category)
    if category_def:
        return None, category, None, None

    resolved = _legacy_category_map().get(category.lower())
    if resolved:
        resolved_category, resolved_type = resolved
        return (
            None,
            resolved_category,
            resolved_type,
            f"'{category}' -> '{resolved_type}'",
        )

    return (
        {
            "status": "error",
            "error": f"Unknown category '{category}'.",
            "available_categories": sorted(SF_CATEGORIES.keys()),
        },
        "",
        None,
        None,
    )


def _validate_sf_metric(
    category: str,
    metric: str,
) -> Tuple[Optional[Dict[str, Any]], str, Optional[str], Optional[str]]:
    resolution_error, resolved_category, resolved_type, migration_note = _resolve_category(category)
    if resolution_error:
        return resolution_error, "", None, None

    category_def = SF_CATEGORIES[resolved_category]

    if metric == "all":
        return None, resolved_category, resolved_type, migration_note

    metrics = [m.name for m in category_def.metrics]
    if metric not in metrics:
        return (
            {
                "status": "error",
                "error": f"Unknown metric '{metric}' in category '{resolved_category}'.",
                "suggestions": _closest_matches(metric, metrics),
            },
            "",
            None,
            None,
        )

    return None, resolved_category, resolved_type, migration_note


def _validate_other_metric(function: str, metric: str) -> Optional[Dict[str, Any]]:
    function_def = OTHER_FUNCTIONS.get(function)
    if not function_def:
        return {
            "status": "error",
            "error": f"Unknown function '{function}'.",
            "available_functions": sorted(OTHER_FUNCTIONS.keys()),
        }

    metrics = [m.name for m in function_def.metrics]
    if metric not in metrics:
        return {
            "status": "error",
            "error": f"Unknown metric '{metric}' in function '{function}'.",
            "suggestions": _closest_matches(metric, metrics),
        }

    return None


def sf_formula(
    symbol: str,
    metric_id: str = "",
    function: str = "SF",
    category: str = "",
    metric: str = "all",
    year: str = "",
    options: str = "",
    extra_args: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """Build and validate a SheetsFinance formula."""
    try:
        symbols = _parse_symbols(symbol)

        parsed_function = function.strip() if isinstance(function, str) else "SF"
        parsed_category = category.strip() if isinstance(category, str) else ""
        parsed_metric = metric.strip() if isinstance(metric, str) else "all"

        if metric_id:
            metric_function, metric_category, metric_name = _parse_metric_id(metric_id.strip())

            if parsed_function not in {"", "SF"} and parsed_function != metric_function:
                return {
                    "status": "error",
                    "error": (
                        f"metric_id conflict: function '{parsed_function}' does not match "
                        f"'{metric_function}' parsed from metric_id."
                    ),
                }

            if parsed_category and metric_category is not None and parsed_category != metric_category:
                return {
                    "status": "error",
                    "error": (
                        f"metric_id conflict: category '{parsed_category}' does not match "
                        f"'{metric_category}' parsed from metric_id."
                    ),
                }

            if parsed_metric not in {"", "all"} and parsed_metric != metric_name:
                return {
                    "status": "error",
                    "error": (
                        f"metric_id conflict: metric '{parsed_metric}' does not match "
                        f"'{metric_name}' parsed from metric_id."
                    ),
                }

            parsed_function = metric_function
            parsed_category = metric_category or ""
            parsed_metric = metric_name

        if parsed_function == "SF":
            if not parsed_category:
                return {
                    "status": "error",
                    "error": "category is required for function SF",
                    "available_categories": sorted(SF_CATEGORIES.keys()),
                }

            validation_error, resolved_category, resolved_type, migration_note = _validate_sf_metric(
                parsed_category,
                parsed_metric,
            )
            if validation_error:
                return validation_error

            category_def = SF_CATEGORIES[resolved_category]
            sf_type = (
                resolved_type
                if resolved_type
                else (category_def.type_values[0] if category_def.type_values else resolved_category)
            )
            sf_args: List[Any] = [None, sf_type, parsed_metric]
            if options:
                sf_args.extend([year, options])
            elif year:
                sf_args.append(year)

            formulas = [_build_formula("SF", [sym, *sf_args[1:]]) for sym in symbols]
            base: Dict[str, Any] = {
                "status": "ok",
                "function": "SF",
                "category": resolved_category,
                "metric": parsed_metric,
                "notes": "",
            }
            if migration_note:
                base["migration_note"] = migration_note
            if len(formulas) == 1:
                base["formula"] = formulas[0]
            else:
                base["formulas"] = formulas
            if _has_non_us_ticker_suffix(symbols):
                _append_note(base, NON_US_CURRENCY_NOTE)
            return base

        validation_error = _validate_other_metric(parsed_function, parsed_metric)
        if validation_error:
            return validation_error

        function_def = OTHER_FUNCTIONS[parsed_function]
        arg_order = NON_SF_EXTRA_ARG_ORDER.get(parsed_function, [])
        extra = extra_args or {}
        if not isinstance(extra, dict):
            return {"status": "error", "error": "extra_args must be an object when provided"}

        formula_values: List[Any] = [None, parsed_metric]
        for key in arg_order:
            formula_values.append(extra.get(key, ""))
        if options:
            formula_values.append(options)

        formulas = [_build_formula(parsed_function, [sym, *formula_values[1:]]) for sym in symbols]
        base = {
            "status": "ok",
            "function": parsed_function,
            "category": None,
            "metric": parsed_metric,
            "notes": function_def.notes,
        }
        if len(formulas) == 1:
            base["formula"] = formulas[0]
        else:
            base["formulas"] = formulas
        return base

    except Exception as exc:
        return {"status": "error", "error": str(exc)}


def sf_describe(target: str) -> Dict[str, Any]:
    """Describe an SF category or non-SF function."""
    if not isinstance(target, str) or not target.strip():
        return {"status": "error", "error": "target must be a non-empty string"}

    normalized = target.strip()

    resolved_category = normalized
    migration_note: Optional[str] = None

    if normalized not in SF_CATEGORIES:
        legacy = _legacy_category_map().get(normalized.lower())
        if legacy:
            resolved_category, resolved_type = legacy
            migration_note = f"'{normalized}' -> '{resolved_type}'"

    if resolved_category in SF_CATEGORIES:
        category = SF_CATEGORIES[resolved_category]
        metrics = [
            {
                "metric_id": f"SF.{resolved_category}.{metric.name}",
                "name": metric.name,
                "description": metric.description,
            }
            for metric in category.metrics
        ]
        payload: Dict[str, Any] = {
            "status": "ok",
            "function": "SF",
            "category": resolved_category,
            "display_name": category.display_name,
            "type_values": category.type_values,
            "metric_count": len(metrics),
            "metrics": metrics,
            "year_syntax": category.year_syntax,
            "options": category.options,
            "example": category.example,
        }
        if migration_note:
            payload["migration_note"] = migration_note
        return payload

    function_name = normalized.upper()
    if function_name in OTHER_FUNCTIONS:
        function_def = OTHER_FUNCTIONS[function_name]
        metrics = [
            {
                "metric_id": f"{function_name}.{metric.name}",
                "name": metric.name,
                "description": metric.description,
            }
            for metric in function_def.metrics
        ]
        payload: Dict[str, Any] = {
            "status": "ok",
            "function": function_name,
            "signature": function_def.signature,
            "metric_count": len(metrics),
            "metrics": metrics,
            "example": function_def.example,
        }
        if function_def.periods:
            payload["periods"] = function_def.periods
        if function_def.types:
            payload["types"] = function_def.types
        if function_def.options:
            payload["options"] = function_def.options
        if function_def.notes:
            payload["notes"] = function_def.notes
        return payload

    return {
        "status": "error",
        "error": f"Unknown target '{target}'.",
        "available_categories": sorted(SF_CATEGORIES.keys()),
        "available_functions": sorted(OTHER_FUNCTIONS.keys()),
    }


__all__ = ["sf_formula", "sf_describe"]
