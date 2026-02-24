#!/usr/bin/env python3
"""SheetsFinance MCP server."""

import sys
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


@mcp.tool()
def sf_search(query: str, limit: int = 10) -> dict:
    """Search SheetsFinance metrics/functions and return ranked metric matches."""
    try:
        return _sf_search(query=query, limit=limit)
    except Exception as exc:
        return {"status": "error", "error": str(exc)}


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
    """Build and validate a SheetsFinance formula for SF() or non-SF functions."""
    try:
        return _sf_formula(
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
        return {"status": "error", "error": str(exc)}


@mcp.tool()
def sf_describe(target: str) -> dict:
    """Describe all metrics for a category or non-SF function."""
    try:
        return _sf_describe(target=target)
    except Exception as exc:
        return {"status": "error", "error": str(exc)}


def main() -> None:
    mcp.run()


if __name__ == "__main__":
    main()
