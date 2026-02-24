# sheets-finance-mcp

MCP server for the SheetsFinance formula catalog.

This package exposes three tools:

- `sf_search`: search metrics/functions and get ranked `metric_id` candidates.
- `sf_formula`: build validated SheetsFinance formulas from a `metric_id` or explicit function/category/metric fields.
- `sf_describe`: inspect category/function metadata, metric lists, and examples.

## What Is SheetsFinance?

SheetsFinance is a Google Sheets add-on for financial market/company data retrieval using spreadsheet formulas.

## Installation

From this package directory:

```bash
pip install -e .
```

Run as a module:

```bash
python -m sheets_finance_mcp
```

Or via console script (installed by `pyproject.toml`):

```bash
sheets-finance-mcp
```

## Claude Code MCP Config

```json
{
  "mcpServers": {
    "sheetsfinance": {
      "command": "python",
      "args": ["-m", "sheets_finance_mcp"]
    }
  }
}
```

## Tool Reference

| Tool | Purpose | Typical Next Step |
|---|---|---|
| `sf_search(query, limit=10)` | Find matching metrics/functions | Use returned `metric_id` with `sf_formula` |
| `sf_formula(...)` | Construct a formula string (single or multi-symbol) | Paste formula in Sheets |
| `sf_describe(target)` | Inspect category/function metrics and options | Pick a metric/function for `sf_formula` |

## Example Workflow

1. Search for a metric:

   ```text
   sf_search(query="gross margin")
   ```

2. Build a formula from the selected metric id:

   ```text
   sf_formula(symbol="AAPL", metric_id="SF.ratios.grossProfitMargin")
   ```

3. Inspect a category/function when needed:

   ```text
   sf_describe(target="income")
   ```

