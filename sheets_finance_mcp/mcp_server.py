#!/usr/bin/env python3
"""SheetsFinance MCP server."""

import sys
from dataclasses import dataclass
from typing import Any, Dict, Optional

from fastmcp import FastMCP

_real_stdout = sys.stdout
sys.stdout = sys.stderr

from .sf_formula import sf_describe as _sf_describe  # noqa: E402
from .sf_formula import sf_formula as _sf_formula  # noqa: E402
from .sf_search import sf_search as _sf_search  # noqa: E402

sys.stdout = _real_stdout

mcp = FastMCP(
    "sheetsfinance",
    instructions=(
        "SheetsFinance formula catalog and builder. "
        "Use sf_search to find metric_ids, sf_formula to construct formulas, "
        "and sf_describe to inspect categories/functions. "
        "For Google Sheets read/write/list/search operations, prefer gsheets-mcp tools."
    ),
)


@dataclass
class ToolError(Exception):
    error_class: str
    message: str
    names_correction: dict[str, Any] | None = None
    suggested_tool_calls: list[dict[str, Any]] | None = None
    recoverable: bool = True

    def __str__(self) -> str:
        return self.message

    def to_envelope(self) -> dict[str, Any]:
        return {
            "status": "error",
            "error": self.message,
            "error_class": self.error_class,
            "message": self.message,
            "names_correction": self.names_correction or {},
            "suggested_tool_calls": self.suggested_tool_calls or [],
            "recoverable": self.recoverable,
        }


def _suggested_tool_calls(tool_name: str, payload: dict[str, Any]) -> list[dict[str, Any]]:
    if tool_name == "sf_search":
        return [{"name": "sf_describe", "args": {"target": "income"}}]
    if tool_name == "sf_formula":
        calls = [{"name": "sf_search", "args": {"query": payload.get("metric") or payload.get("metric_id") or ""}}]
        target = payload.get("category") or payload.get("function") or "income"
        calls.append({"name": "sf_describe", "args": {"target": target}})
        return calls
    return [{"name": "sf_search", "args": {"query": payload.get("target") or "revenue"}}]


def _normalize_error_result(tool_name: str, result: dict[str, Any], **kwargs: Any) -> dict[str, Any]:
    if result.get("status") != "error":
        return result
    if "error_class" in result and "message" in result and "suggested_tool_calls" in result:
        return result

    message = str(result.get("error") or result.get("message") or "Tool returned an error")
    envelope = ToolError(
        error_class="ToolReturnedError",
        message=message,
        names_correction={
            "tool": tool_name,
            "received_arguments": sorted(kwargs),
        },
        suggested_tool_calls=_suggested_tool_calls(tool_name, kwargs),
    ).to_envelope()
    merged = dict(result)
    for key, value in envelope.items():
        merged.setdefault(key, value)
    return merged


def _exception_envelope(tool_name: str, exc: Exception, **kwargs: Any) -> dict[str, Any]:
    message = str(exc) or exc.__class__.__name__
    return ToolError(
        error_class=exc.__class__.__name__,
        message=message,
        names_correction={
            "tool": tool_name,
            "received_arguments": sorted(kwargs),
        },
        suggested_tool_calls=_suggested_tool_calls(tool_name, kwargs),
    ).to_envelope()


@mcp.tool()
def sf_search(query: str, limit: int = 10) -> dict:
    """Search SheetsFinance metrics/functions and return ranked metric matches.

    Discovery: use this first when an agent knows a plain-English metric name
    such as revenue, EBITDA, dividends, or SMA but not the exact metric_id,
    category, or function. Results include identifiers and match context for
    sf_formula.

    Sibling tools: use sf_describe to browse all metrics in one category or
    non-SF function, and sf_formula after selecting a metric_id/function.

    Common mistake: this searches the formula catalog only. It does not read or
    write Google Sheets cells; use gsheets-mcp for spreadsheet operations.
    """
    try:
        return _normalize_error_result(
            "sf_search",
            _sf_search(query=query, limit=limit),
            query=query,
            limit=limit,
        )
    except Exception as exc:
        return _exception_envelope("sf_search", exc, query=query, limit=limit)


@mcp.tool()
def sf_formula(
    symbol: str,
    metric_id: str = "",
    function: str = "SF",
    category: str = "",
    metric: str = "all",
    year: str = "",
    options: str = "",
    extra_args: Optional[Dict[str, Any]] = None,
) -> dict:
    """Build and validate a SheetsFinance formula for SF() or non-SF functions.

    Discovery: run sf_search to choose an exact metric_id or run sf_describe to
    inspect a category/function before building the formula. For SF metrics,
    pass symbol plus either metric_id or category/metric; for non-SF functions,
    pass function and the required function-specific options.

    Sibling tools: use sf_search for fuzzy lookup and sf_describe for the full
    metric/function menu. Use gsheets-mcp tools only after this returns a
    formula that should be written to a spreadsheet.

    Common mistake: symbol is a market ticker, not a spreadsheet cell. This
    tool returns formula text and validation details; it does not update a
    sheet.
    """
    try:
        return _normalize_error_result(
            "sf_formula",
            _sf_formula(
                symbol=symbol,
                metric_id=metric_id,
                function=function,
                category=category,
                metric=metric,
                year=year,
                options=options,
                extra_args=extra_args,
            ),
            symbol=symbol,
            metric_id=metric_id,
            function=function,
            category=category,
            metric=metric,
            year=year,
            options=options,
            extra_args=extra_args,
        )
    except Exception as exc:
        return _exception_envelope(
            "sf_formula",
            exc,
            symbol=symbol,
            metric_id=metric_id,
            function=function,
            category=category,
            metric=metric,
            year=year,
            options=options,
            extra_args=extra_args,
        )


@mcp.tool()
def sf_describe(target: str) -> dict:
    """Describe all metrics for a category or non-SF function.

    Discovery: run sf_search when the target category/function is unknown, or
    pass a known category such as income or a non-SF function such as
    sf_technical. The response lists valid metrics and options that can feed
    sf_formula.

    Sibling tools: use sf_formula after choosing a metric/function from this
    response. Use sf_search for fuzzy lookup when target is misspelled or only
    partly known.

    Common mistake: target is a catalog category or function, not a ticker,
    metric_id, or spreadsheet range. This tool describes formulas; it does not
    fetch market data or write Sheets cells.
    """
    try:
        return _normalize_error_result("sf_describe", _sf_describe(target=target), target=target)
    except Exception as exc:
        return _exception_envelope("sf_describe", exc, target=target)


def main() -> None:
    mcp.run()


if __name__ == "__main__":
    main()
