# SheetsFinance Formula Catalog

Complete reference for the SheetsFinance Google Sheets add-on custom functions.
Scraped from https://www.sheetsfinance.com/docs/ on 2026-02-20.

---

## Function Signatures

SheetsFinance provides 10 custom functions:

### 1. SF() — Main Data Function
```
=SF(symbol, type, metric, year, options)
```
Used for: realTime, companyInfo, ratios, earnings, esg, score, peers, analysts, ratings, insiders, insiderStats, change, growth, etfInfo, etfHoldings, etfSectors, etfCountries, prePostMarket, historical, owners, income/balancesheet/cashflow statements, estimates, revenue segmentation.

### 2. SF_TIMESERIES() — Time Series
```
=SF_TIMESERIES(symbol, startDate, endDate, period, metric, options)
```

### 3. SF_DIVIDEND() — Dividend History
```
=SF_DIVIDEND(symbol, startDate, endDate, metric, options)
```

### 4. SF_OPTIONS() — Options Chain
```
=SF_OPTIONS(symbol, type, metric, expirationDate, options)
```

### 5. SF_CALENDAR() — Financial Calendars
```
=SF_CALENDAR(searchTerms, type, startDate, endDate, metrics, options)
```

### 6. SF_SPARK() — Sparklines
```
=SF_SPARK(symbol, lastXdays, type)
```

### 7. SF_TECHNICAL() — Technical Analysis
```
=SF_TECHNICAL(symbol, type, timeframe, startDate, endDate, options)
```

### 8. SF_NEWS() — News Feeds
```
=SF_NEWS(symbol(s), type, limit, metrics, site, startDate, endDate, options)
```

### 9. SF_SCREEN() — Stock Screener
```
=SF_SCREEN(filters, metrics, options)
```

### 10. SF_MAP() — ISIN/CUSIP/CIK Mapper
```
=SF_MAP(code, type, filter)
```

---

## Common Options (apply to most functions)

| Option | Description |
|--------|-------------|
| `"NH"` | No header rows |
| `"NLI"` | No line item labels |
| `"-"` | Reverse chronological order |
| `"calYear"` | Calendar years instead of fiscal |
| `"pad"` | Pad missing periods with empty columns |

Options are chained with `&` (e.g., `"NH&NLI&-"`).

Metrics can also be chained with `&` (e.g., `"revenue&netIncome&eps"`).

---

## SF() Categories and Parameters

### 1. realTime
```
=SF(symbol, "realTime", metric, "", options)
```

**Metrics:**
- `all`, `price`, `open`, `previousClose`, `change`, `changesPercentage`
- `dayLow`, `dayHigh`, `volume`, `timestamp`
- `name`, `exchange`, `marketCap`
- `yearHigh`, `yearLow`, `priceAvg50`, `priceAvg200`
- `avgVolume` (3-month average)
- `earningsAnnouncement`
- `pe`, `eps`, `sharesOutstanding`

**Options:** `NH`

---

### 2. companyInfo
```
=SF(symbol, "companyInfo", metric, "", options)
```

**Metrics:**
- `all`, `name`, `exchange`, `exchangeFullName`
- `range`, `lastDividend`, `divYield`, `beta`
- `currency`, `industry`, `sector`, `country`, `state`, `city`, `zip`, `phone`
- `isin`, `cusip`, `cik`
- `fullTimeEmployees`, `ipoDate`, `ceo`, `website`, `description`
- `isEtf`, `isAdr`, `isFund`, `isActivelyTrading`

**Options:** `NH`

---

### 3. Income Statement
```
=SF(symbol, type, metric, year, options)
```

**Type values:**
- `"income"` — Annual
- `"incomeQ"` — All quarters
- `"incomeQ1"`, `"incomeQ2"`, `"incomeQ3"`, `"incomeQ4"` — Specific quarter
- `"incomeTTM"` — Trailing twelve months

**Metrics (39):**
- Metadata: `all`, `date`, `reportedCurrency`, `cik`, `filingDate`, `acceptedDate`, `fiscalYear`, `period`
- Revenue: `revenue`, `costOfRevenue`, `grossProfit`
- Expenses: `researchAndDevelopmentExpenses`, `generalAndAdministrativeExpenses`, `sellingAndMarketingExpenses`, `sellingGeneralAndAdministrativeExpenses`, `otherExpenses`, `operatingExpenses`, `costAndExpenses`
- Interest: `netInterestIncome`, `interestIncome`, `interestExpense`, `depreciationAndAmortization`
- Profitability: `ebitda`, `ebit`, `nonOperatingIncomeExcludingInterest`, `operatingIncome`, `totalOtherIncomeExpensesNet`, `incomeBeforeTax`
- Tax & Net: `incomeTaxExpense`, `netIncomeFromContinuingOperations`, `netIncomeFromDiscontinuedOperations`, `otherAdjustmentsToNetIncome`, `netIncome`, `netIncomeDeductions`, `bottomLineNetIncome`
- Per Share: `eps`, `epsDiluted`, `weightedAverageShsOut`, `weightedAverageShsOutDil`

**Year:** `"2020"`, `"2015-2020"`, `"ttm"`, `"2020-06-30"`, `"2020-03"`

**Options:** `NH`, `NLI`, `-`, `calYear`, `pad`

---

### 4. Balance Sheet
```
=SF(symbol, type, metric, year, options)
```

**Type values:**
- `"balancesheet"` — Annual
- `"balancesheetQ"` — All quarters
- `"balancesheetQ1"`, `"balancesheetQ2"`, `"balancesheetQ3"`, `"balancesheetQ4"` — Specific quarter
- `"balancesheetTTM"` — Trailing twelve months

**Metrics (62):**
- Metadata: `all`, `date`, `symbol`, `reportedCurrency`, `cik`, `filingDate`, `acceptedDate`, `fiscalYear`, `period`
- Current Assets: `cashAndCashEquivalents`, `shortTermInvestments`, `cashAndShortTermInvestments`, `netReceivables`, `accountsReceivables`, `otherReceivables`, `inventory`, `prepaids`, `otherCurrentAssets`, `totalCurrentAssets`
- Non-Current Assets: `propertyPlantEquipmentNet`, `goodwill`, `intangibleAssets`, `goodwillAndIntangibleAssets`, `longTermInvestments`, `taxAssets`, `otherNonCurrentAssets`, `totalNonCurrentAssets`, `otherAssets`, `totalAssets`
- Payables: `totalPayables`, `accountPayables`, `otherPayables`, `accruedExpenses`
- Current Liabilities: `shortTermDebt`, `capitalLeaseObligationsCurrent`, `taxPayables`, `deferredRevenue`, `otherCurrentLiabilities`, `totalCurrentLiabilities`
- Non-Current Liabilities: `longTermDebt`, `capitalLeaseObligationsNonCurrent`, `deferredRevenueNonCurrent`, `deferredTaxLiabilitiesNonCurrent`, `otherNonCurrentLiabilities`, `totalNonCurrentLiabilities`, `otherLiabilities`, `capitalLeaseObligations`, `totalLiabilities`
- Equity: `treasuryStock`, `preferredStock`, `commonStock`, `retainedEarnings`, `additionalPaidInCapital`, `accumulatedOtherComprehensiveIncomeLoss`, `otherTotalStockholdersEquity`, `totalStockholdersEquity`, `totalEquity`, `minorityInterest`
- Composite: `totalLiabilitiesAndTotalEquity`, `totalInvestments`, `totalDebt`, `netDebt`

**Year:** Same as Income Statement

**Options:** `NH`, `NLI`, `-`, `calYear`, `pad`

---

### 5. Cash Flow Statement
```
=SF(symbol, type, metric, year, options)
```

**Type values:**
- `"cashflow"` — Annual
- `"cashflowQ"` — All quarters
- `"cashflowQ1"`, `"cashflowQ2"`, `"cashflowQ3"`, `"cashflowQ4"` — Specific quarter
- `"cashflowTTM"` — Trailing twelve months

**Metrics (48):**
- Metadata: `all`, `date`, `symbol`, `reportedCurrency`, `cik`, `filingDate`, `acceptedDate`, `fiscalYear`, `period`
- Operating: `netIncome`, `depreciationAndAmortization`, `deferredIncomeTax`, `stockBasedCompensation`, `changeInWorkingCapital`, `accountsReceivables`, `inventory`, `accountsPayables`, `otherWorkingCapital`, `otherNonCashItems`, `netCashProvidedByOperatingActivities`
- Investing: `investmentsInPropertyPlantAndEquipment`, `acquisitionsNet`, `purchasesOfInvestments`, `salesMaturitiesOfInvestments`, `otherInvestingActivities`, `netCashProvidedByInvestingActivities`
- Financing: `netDebtIssuance`, `longTermNetDebtIssuance`, `shortTermNetDebtIssuance`, `netStockIssuance`, `netCommonStockIssuance`, `commonStockIssuance`, `commonStockRepurchased`, `netPreferredStockIssuance`, `netDividendsPaid`, `commonDividendsPaid`, `preferredDividendsPaid`, `otherFinancingActivities`, `netCashProvidedByFinancingActivities`
- Summary: `effectOfForexChangesOnCash`, `netChangeInCash`, `cashAtEndOfPeriod`, `cashAtBeginningOfPeriod`, `operatingCashFlow`, `capitalExpenditure`, `freeCashFlow`, `incomeTaxesPaid`, `interestPaid`

**Year:** Same as Income Statement

**Options:** `NH`, `NLI`, `-`, `calYear`, `pad`

---

### 6. Key Ratios
```
=SF(symbol, type, metric, year, options)
```

**Type values:**
- `"ratios"` — Annual
- `"ratiosQ"` — All quarters (use with year range)
- `"ratiosQ1"`, `"ratiosQ2"`, `"ratiosQ3"`, `"ratiosQ4"` — Specific quarter

**Metrics (104):**
- Metadata: `all`, `date`, `fiscalYear`, `period`, `reportedCurrency`
- Margins: `grossProfitMargin`, `ebitMargin`, `ebitdaMargin`, `operatingProfitMargin`, `pretaxProfitMargin`, `continuousOperationsProfitMargin`, `netProfitMargin`, `bottomLineProfitMargin`
- Turnover: `receivablesTurnover`, `payablesTurnover`, `inventoryTurnover`, `fixedAssetTurnover`, `assetTurnover`
- Liquidity: `currentRatio`, `quickRatio`, `solvencyRatio`, `cashRatio`
- Valuation: `priceToEarningsRatio`, `priceToEarningsGrowthRatio`, `forwardPriceToEarningsGrowthRatio`, `priceToBookRatio`, `priceToSalesRatio`, `priceToFreeCashFlowRatio`, `priceToOperatingCashFlowRatio`
- Leverage: `debtToAssetsRatio`, `debtToEquityRatio`, `debtToCapitalRatio`, `longTermDebtToCapitalRatio`, `financialLeverageRatio`
- Cash Flow: `workingCapitalTurnoverRatio`, `operatingCashFlowRatio`, `operatingCashFlowSalesRatio`, `freeCashFlowOperatingCashFlowRatio`, `debtServiceCoverageRatio`, `interestCoverageRatio`, `shortTermOperatingCashFlowCoverageRatio`, `operatingCashFlowCoverageRatio`, `capitalExpenditureCoverageRatio`, `dividendPaidAndCapexCoverageRatio`
- Dividend: `dividendPayoutRatio`, `dividendYield`, `dividendPerShare`
- Enterprise: `enterpriseValue`, `enterpriseValueMultiple`, `evToSales`, `evToOperatingCashFlow`, `evToFreeCashFlow`, `evToEBITDA`, `netDebtToEBITDA`
- Per Share: `revenuePerShare`, `netIncomePerShare`, `interestDebtPerShare`, `cashPerShare`, `bookValuePerShare`, `tangibleBookValuePerShare`, `shareholdersEquityPerShare`, `operatingCashFlowPerShare`, `capexPerShare`, `freeCashFlowPerShare`
- Efficiency: `netIncomePerEbt`, `ebtPerEbit`, `priceToFairValue`, `debtToMarketCap`, `effectiveTaxRate`
- Quality: `incomeQuality`, `grahamNumber`, `grahamNetNet`, `taxBurden`, `interestBurden`
- Working Capital: `workingCapital`, `investedCapital`
- Returns: `returnOnAssets`, `operatingReturnOnAssets`, `returnOnTangibleAssets`, `returnOnEquity`, `returnOnInvestedCapital`, `returnOnCapitalEmployed`
- Yields: `earningsYield`, `freeCashFlowYield`
- CapEx: `capexToOperatingCashFlow`, `capexToDepreciation`, `capexToRevenue`
- Expense Ratios: `salesGeneralAndAdministrativeToRevenue`, `researchAndDevelopementToRevenue`, `stockBasedCompensationToRevenue`, `intangiblesToTotalAssets`
- Working Capital Cycle: `averageReceivables`, `averagePayables`, `averageInventory`, `daysOfSalesOutstanding`, `daysOfPayablesOutstanding`, `daysOfInventoryOutstanding`, `operatingCycle`, `cashConversionCycle`
- Free Cash Flow: `freeCashFlowToEquity`, `freeCashFlowToFirm`
- Asset Value: `tangibleAssetValue`, `netCurrentAssetValue`
- Market: `marketCap`

**Year:** `"2020"`, `"2010-2020"`, `"ttm"`

**Options:** `NH`, `NLI`, `-`, `calYear`, `pad`

---

### 7. Estimates
```
=SF(symbol, type, metric, year, options)
```

**Type values:**
- `"estimates"` — Annual
- `"estimatesQ"` — Quarterly

**Metrics:**
- `all`, `date`
- Revenue: `revenueLow`, `revenueHigh`, `revenueAvg`
- EBITDA: `ebitdaLow`, `ebitdaHigh`, `ebitdaAvg`
- EBIT: `ebitLow`, `ebitHigh`, `ebitAvg`
- Net Income: `netIncomeLow`, `netIncomeHigh`, `netIncomeAvg`
- SGA: `sgaExpenseLow`, `sgaExpenseHigh`, `sgaExpenseAvg`
- EPS: `epsLow`, `epsHigh`, `epsAvg`
- Counts: `numAnalystsRevenue`, `numAnalystsEps`

**Year:** `2025`, `2023-2025`, or quarterly `2024-03`; defaults to next year

**Options:** `NH`, `NLI`, `-`

---

### 8. Earnings
```
=SF(symbol, "earnings", metric, date, options)
```

**Metrics:** `all`, `date`, `eps`, `epsEstimated`, `revenue`, `revenueEstimated`

**Date:** `"ttm"` (default), `2022`, `"2020-2023"`

**Options:** `NH`, `-`

---

### 9. ESG Score
```
=SF(symbol, "esg", metric, year, options)
```

**Metrics:** `all`, `date`, `formType`, `acceptedDate`, `environmentalScore`, `socialScore`, `governanceScore`, `ESGScore`, `url`

**Year:** `2020`, `"2019-2021"`

**Options:** `NH`, `-`

**Note:** US markets only. Score 0-100 (50 = industry average).

---

### 10. Financial Score
```
=SF(symbol, "score", metric, "", options)
```

**Metrics:** `all`, `revenue`, `totalLiabilities`, `marketCap`, `ebit`, `retainedEarnings`, `totalAssets`, `workingCapital`, `piotroskiScore`, `altmanZScore`

**Options:** `NH`, `NLI`

---

### 11. Peers
```
=SF(symbol, "peers", metric)
```

**Metrics:** `all`, `symbol`, `name`, `price`, `marketCap`

---

### 12. Analyst Ratings
```
=SF(symbol, "analysts", metric, date, options)
```

**Metrics:** `all`, `date`, `gradingCompany`, `previousGrade`, `newGrade`

**Date:** `"2020"`, `"2020-01"`, `"2020-01-05"`, `"all"`, `"latestUnique"`

**Options:** `NH`, `-`

---

### 13. Analyst Ratings Totals
```
=SF(symbol, "ratings", metric, date, options)
```

**Metrics:** `all`, `date`, `buy`, `sell`, `hold`, `strongBuy`, `strongSell`

**Date:** `"2020"`, `"2020-01"`, `"latest"`, `"all"`

**Options:** `NH`, `-`

---

### 14. Price Targets
```
=SF(symbol, "priceTargets", metric, timePeriod, options)
```

**Metrics:** `all`, `publishedDate`, `analystCompany`, `analystName`, `priceTarget`, `priceWhenPosted`

**Time Period:** Integer (last X months), `YYYY`, `YYYY-MM`, `YYYY-MM-DD`; default last 12 months

**Options:** `NH`, `-`

**Note:** US markets only.

---

### 15. Company Growth
```
=SF(symbol, type, metric, year, options)
```

**Type values:**
- `"growth"` — Annual
- `"growthQ"` — All quarters
- `"growthQ1"`, `"growthQ2"`, `"growthQ3"`, `"growthQ4"` — Specific quarter

**Metrics (34):**
- `revenueGrowth`, `grossProfitGrowth`, `ebitgrowth`, `operatingIncomeGrowth`, `netIncomeGrowth`
- `epsgrowth`, `epsdilutedGrowth`
- `weightedAverageSharesGrowth`, `weightedAverageSharesDilutedGrowth`
- `dividendsperShareGrowth`
- `operatingCashFlowGrowth`, `freeCashFlowGrowth`
- Multi-year per share: `tenYRevenueGrowthPerShare`, `fiveYRevenueGrowthPerShare`, `threeYRevenueGrowthPerShare`
- `tenYOperatingCFGrowthPerShare`, `fiveYOperatingCFGrowthPerShare`, `threeYOperatingCFGrowthPerShare`
- `tenYNetIncomeGrowthPerShare`, `fiveYNetIncomeGrowthPerShare`, `threeYNetIncomeGrowthPerShare`
- `tenYShareholdersEquityGrowthPerShare`, `fiveYShareholdersEquityGrowthPerShare`, `threeYShareholdersEquityGrowthPerShare`
- `tenYDividendperShareGrowthPerShare`, `fiveYDividendperShareGrowthPerShare`, `threeYDividendperShareGrowthPerShare`
- Balance sheet: `receivablesGrowth`, `inventoryGrowth`, `assetGrowth`, `bookValueperShareGrowth`, `debtGrowth`, `rdexpenseGrowth`, `sgaexpensesGrowth`

**Year:** `"2020"`, `"2010-2020"`

**Options:** `NH`, `NLI`, `-`, `calYear`, `pad`

---

### 16. Price Change
```
=SF(symbol, "change", metric, "", options)
```

**Metrics:** `all`, `1D`, `5D`, `1M`, `3M`, `6M`, `ytd`, `1Y`, `3Y`, `5Y`, `10Y`, `max`

**Options:** `NH`, `decimal` (return as decimal instead of percentage)

---

### 17. Historical EOD
```
=SF(symbol, "historical", metric, date, options)
```

**Metrics:** `all`, `open`, `high`, `low`, `close`, `adjClose`, `volume`, `marketCap`

**Date:** `"YYYY-MM-DD"`

**Options:** `NH`, `includeWeekends` (for FOREX/crypto)

---

### 18. Insider Transactions
```
=SF(symbol, "insiders", metric, year, options)
```

**Metrics:** `all`, `transactionDate`, `reportingName`, `typeOfOwner`, `securitiesOwned`, `securityName`, `transactionType`, `price`, `acquisitionOrDisposition`, `directOrIndirect`, `securitiesTransacted`, `filingDate`, `reportingCik`, `companyCik`, `formType`, `url`

**Year:** `2024`, `"2022-2024"`

**Options:** `NH`, `-`

**Note:** US only. Last 400 transactions max.

---

### 19. Insider Statistics
```
=SF(symbol, "insiderStats", metric, year, options)
```

**Metrics:** `all`, `year`, `quarter`, `acquiredTransactions`, `disposedTransactions`, `acquiredDisposedRatio`, `totalAcquired`, `totalDisposed`, `averageAcquired`, `averageDisposed`, `totalPurchases`, `totalSales`, `cik`

**Year:** `2024`, `"2022-2024"`

**Options:** `NH`, `-`

**Note:** US only. 20+ years quarterly data.

---

### 20. Pre/Post Market
```
=SF(symbol, "prePostMarket", metric, "", options)
```

**Metrics:** `all`, `ask`, `bid`, `askSize`, `bidSize`, `volume`, `timestamp`

**Options:** `NH`

**Note:** US equities only.

---

### 21. Industry PE
```
=SF(industry, "industryPE", "", "", options)
```

**Industry parameter:** One of ~180 industry names (e.g., `"Software - Application"`, `"Biotechnology"`, `"Banks - Regional"`). Chain with `&`.

**Options:** `NH`

---

### 22. Sector PE
```
=SF(sector, "sectorPE", "", "", options)
```

**Sector parameter:** `all`, `Basic Materials`, `Communication Services`, `Consumer Cyclical`, `Consumer Defensive`, `Energy`, `Financial Services`, `Healthcare`, `Industrials`, `Real Estate`, `Technology`, `Utilities`

**Options:** `NH`

---

### 23. Owners Earnings
```
=SF(symbol, "owners", metric, year, options)
```

**Metrics:** `all`, `date`, `averagePPE`, `maintenanceCapex`, `growthCapex`, `ownersEarnings`, `ownersEarningsPerShare`

**Year:** `2020`, `"2019-2021"`

**Options:** `NH`, `-`, `calYear`

---

### 24. Revenue Segmentation — Product
```
=SF(symbol, type, metric, year, options)
```

**Type:** `"revSegProduct"`, `"revSegProductQ"`, `"revSegProductQ1"`..`"revSegProductQ4"`

**Metrics:** `period`, `date`, `fiscalYear`, plus company-specific product segments. Use `"all"`.

**Year:** `2020`, `"2019-2021"`

**Options:** `NH`, `NLI`, `-`, `calYear`

**Note:** US markets only.

---

### 25. Revenue Segmentation — Geography
```
=SF(symbol, type, metric, year, options)
```

**Type:** `"revSegGeo"`, `"revSegGeoQ"`, `"revSegGeoQ1"`..`"revSegGeoQ4"`

**Metrics:** `period`, `date`, `fiscalYear`, plus company-specific geographic segments. Use `"all"`.

**Year:** `2020`, `"2019-2021"`

**Options:** `NH`, `NLI`, `-`, `calYear`

**Note:** US markets only.

---

### 26. ETF Info
```
=SF(ETF, "etfInfo", metric, "", options)
```

**Metrics:** `all`, `name`, `assetClass`, `AUM`, `NAV`, `avgVolume`, `expenseRatio`, `domicile`, `etfCompany`, `inceptionDate`, `isin`, `cusip`, `holdingsCount`, `description`, `website`

**Options:** `NH`, `NLI`

---

### 27. ETF Holdings
```
=SF(ETF, "etfHoldings", metric, "", options)
```

**Metrics:** `all`, `asset`, `name`, `isin`, `cusip`, `sharesNumber`, `weightPercentage`, `marketValue`, `updated`

**Options:** `NH`, `-`, `ob=<metric>`, `limit=X`

---

### 28. ETF Sectors
```
=SF(ETF, "etfSectors", "", "", options)
```

**Options:** `NH`, `-`

---

### 29. ETF Countries
```
=SF(ETF, "etfCountries", "", "", options)
```

**Options:** `NH`, `-`

---

### 30. Institutional Holders
```
=SF(symbol, "instHolders", metric, date, options)
```

**Metrics:** `all`, `holder`, `shares`, `dateReported`, `change`, `dateOptions`

**Date:** Quarterly date recommended; omit for latest

**Options:** `NH`, `-`, `ob=<metric>`, `limit=X`

---

### 31. Historical Market Cap
Single date via SF():
```
=SF(symbol, "historical", "marketCap", "2020-07-24")
```
Time series via SF_TECHNICAL():
```
=SF_TECHNICAL(symbol, "marketCap&all", "", startDate, endDate, options)
```

**Metrics:** `marketCap`, `date`

---

## SF_TIMESERIES() Parameters

```
=SF_TIMESERIES(symbol, startDate, endDate, period, metric, options)
```

**Period values:**
| Period | Code |
|--------|------|
| Daily | `""`, `"daily"`, or omit |
| Daily Dividend Adjusted | `"dailyAdj"` |
| Intra/Inter-day | `"1min"`, `"5min"`, `"15min"`, `"30min"`, `"1hour"`, `"4hour"` |
| Inter-day | `"1week"`, `"1month"`, `"1year"` |
| Outstanding Shares | `"shares"` |

**Intra-day max ranges:** 1min=3d, 5min=7d, 15min=2mo, 30min=1mo, 1hour=3mo, 4hour=3mo

**Daily Metrics:** `all`, `date`, `open`, `high`, `low`, `close`, `adjClose`, `volume`, `unadjustedVolume`, `change`, `changePercent`, `changeOverTime`, `vwap`

**Intra-day Metrics:** `all`, `date`, `open`, `high`, `low`, `close`, `volume`

**Shares Metrics:** `all`, `date`, `outstandingShares`, `floatShares`, `freeFloat`

**Options:** `NH`, `-`

---

## SF_DIVIDEND() Parameters

```
=SF_DIVIDEND(symbol, startDate, endDate, metric, options)
```

**Metrics:** `all`, `date`, `dividend`, `adjDividend`, `recordDate`, `paymentDate`, `declarationDate`, `yield`, `frequency`

**Options:** `NH`, `-`

---

## SF_OPTIONS() Parameters

```
=SF_OPTIONS(symbol, type, metric, expirationDate, options)
```

**Type values:** `"expirationDates"`, `"calls"`, `"puts"`

**Metrics:** `all`, `contractSymbol`, `strike`, `currency`, `lastPrice`, `change`, `percentChange`, `volume`, `openInterest`, `bid`, `ask`, `mid`, `expiration`, `lastTradeDate`, `impliedVolatility`, `intheMoney`

**Options:** `NH`, `-`, `ob=<metric>`, `limit=X`

Can also pass a contract symbol directly (e.g., `"AAPL240920C00160000"`) to get single contract data.

---

## SF_CALENDAR() Parameters

```
=SF_CALENDAR(searchTerms, type, startDate, endDate, metrics, options)
```

**Max date range:** 90 days per call.

**Search terms:** Symbols, exchanges, markets. Use `&` for multiple, `$` for exact match.

### Calendar Types and Metrics:

| Type | Metrics |
|------|---------|
| `"earnings"` | `date`, `symbol`, `eps`, `epsEstimated`, `time`, `revenue`, `revenueEstimated`, `fiscalDateEnding`, `updatedFromDate` |
| `"dividends"` | `date`, `symbol`, `dividend`, `adjDividend`, `recordDate`, `paymentDate`, `declarationDate`, `yield`, `frequency` |
| `"splits"` | `date`, `symbol`, `numerator`, `denominator`, `ratio` |
| `"ipos"` | `date`, `symbol`, `company`, `exchange`, `actions`, `shares`, `priceRange`, `marketCap` |
| `"economic"` | `date`, `country`, `event`, `currency`, `previous`, `estimate`, `actual`, `change`, `changePercentage`, `impact` |
| `"treasury"` | `date`, `month1`, `month2`, `month3`, `month6`, `year1`, `year2`, `year3`, `year5`, `year7`, `year10`, `year20`, `year30` |

**Options:** `NH`, `-`

**Treasury note:** Requires empty first argument: `=SF_CALENDAR("", "treasury", ...)`

---

## SF_TECHNICAL() Parameters

```
=SF_TECHNICAL(symbol, type, timeframe, startDate, endDate, options)
```

**Indicator types** (append period number):
- `sma` — Simple Moving Average (e.g., `sma20`)
- `ema` — Exponential Moving Average (e.g., `ema50`)
- `wma` — Weighted Moving Average
- `dema` — Double Exponential Moving Average
- `tema` — Triple Exponential Moving Average
- `williams` — Williams %R
- `rsi` — Relative Strength Index
- `adx` — Average Directional Index
- `standardDeviation` — Standard Deviation

**Type format:** `[indicator][period]&[display1]&[display2]`
- Display items: `all`, `date`, `open`, `high`, `low`, `close`, `volume`

**Timeframe:** `daily`, `1min`, `5min`, `15min`, `30min`, `1hour`, `4hour`

**Also supports:** `marketCap&all` for historical market cap time series.

**Options:** `NH`, `-`

---

## SF_NEWS() Parameters

```
=SF_NEWS(symbol(s), type, limit, metrics, site, startDate, endDate, options)
```

**Type:** `"stocks"` (default), `"crypto"`, `"forexAndCommodities"`

**Metrics:** `all`, `publishedDate`, `publisher`, `site`, `title`, `text`, `url`

**Site filter:** Domain names (e.g., `"barrons.com"`), chain with `&`

**Options:** `NH`, `-`

---

## SF_SCREEN() Parameters

```
=SF_SCREEN(filters, metrics, options)
```

**Basic Filters (13):**
`marketCap`, `price`, `beta`, `volume`, `averageVolume`, `lastDividend`, `isEtf`, `isActivelyTrading`, `sector`, `industry`, `country`, `exchange`, `ipoDate`

Operators: `>`, `<`, `=`. Multi-value: comma-separated.

**Advanced Filters (98):** All ratios with `TTM` suffix:
`grossProfitMarginTTM`, `ebitMarginTTM`, `ebitdaMarginTTM`, `operatingProfitMarginTTM`, `pretaxProfitMarginTTM`, `continuousOperationsProfitMarginTTM`, `netProfitMarginTTM`, `bottomLineProfitMarginTTM`, `receivablesTurnoverTTM`, `payablesTurnoverTTM`, `inventoryTurnoverTTM`, `fixedAssetTurnoverTTM`, `assetTurnoverTTM`, `currentRatioTTM`, `quickRatioTTM`, `solvencyRatioTTM`, `cashRatioTTM`, `priceToEarningsRatioTTM`, `priceToEarningsGrowthRatioTTM`, `forwardPriceToEarningsGrowthRatioTTM`, `priceToBookRatioTTM`, `priceToSalesRatioTTM`, `priceToFreeCashFlowRatioTTM`, `priceToOperatingCashFlowRatioTTM`, `debtToAssetsRatioTTM`, `debtToEquityRatioTTM`, `debtToCapitalRatioTTM`, `longTermDebtToCapitalRatioTTM`, `financialLeverageRatioTTM`, `workingCapitalTurnoverRatioTTM`, `operatingCashFlowRatioTTM`, `operatingCashFlowSalesRatioTTM`, `freeCashFlowOperatingCashFlowRatioTTM`, `debtServiceCoverageRatioTTM`, `interestCoverageRatioTTM`, `shortTermOperatingCashFlowCoverageRatioTTM`, `operatingCashFlowCoverageRatioTTM`, `capitalExpenditureCoverageRatioTTM`, `dividendPaidAndCapexCoverageRatioTTM`, `dividendPayoutRatioTTM`, `dividendYieldTTM`, `enterpriseValueTTM`, `revenuePerShareTTM`, `netIncomePerShareTTM`, `interestDebtPerShareTTM`, `cashPerShareTTM`, `bookValuePerShareTTM`, `tangibleBookValuePerShareTTM`, `shareholdersEquityPerShareTTM`, `operatingCashFlowPerShareTTM`, `capexPerShareTTM`, `freeCashFlowPerShareTTM`, `netIncomePerEbtTTM`, `ebtPerEbitTTM`, `priceToFairValueTTM`, `debtToMarketCapTTM`, `effectiveTaxRateTTM`, `enterpriseValueMultipleTTM`, `dividendPerShareTTM`, `evToSalesTTM`, `evToOperatingCashFlowTTM`, `evToFreeCashFlowTTM`, `evToEBITDATTM`, `netDebtToEBITDATTM`, `incomeQualityTTM`, `grahamNumberTTM`, `grahamNetNetTTM`, `taxBurdenTTM`, `interestBurdenTTM`, `workingCapitalTTM`, `investedCapitalTTM`, `returnOnAssetsTTM`, `operatingReturnOnAssetsTTM`, `returnOnTangibleAssetsTTM`, `returnOnEquityTTM`, `returnOnInvestedCapitalTTM`, `returnOnCapitalEmployedTTM`, `earningsYieldTTM`, `freeCashFlowYieldTTM`, `capexToOperatingCashFlowTTM`, `capexToDepreciationTTM`, `capexToRevenueTTM`, `salesGeneralAndAdministrativeToRevenueTTM`, `researchAndDevelopementToRevenueTTM`, `stockBasedCompensationToRevenueTTM`, `intangiblesToTotalAssetsTTM`, `averageReceivablesTTM`, `averagePayablesTTM`, `averageInventoryTTM`, `daysOfSalesOutstandingTTM`, `daysOfPayablesOutstandingTTM`, `daysOfInventoryOutstandingTTM`, `operatingCycleTTM`, `cashConversionCycleTTM`, `freeCashFlowToEquityTTM`, `freeCashFlowToFirmTTM`, `tangibleAssetValueTTM`, `netCurrentAssetValueTTM`

**Options:**
- `NH` — No headers
- `ob=<metric>` — Order by (descending); prefix `-` for ascending
- `limit=N` — Limit rows
- `incldNotActive` — Include inactive stocks

---

## SF_SPARK() Parameters

```
=SF_SPARK(symbol, lastXdays, type)
```

**lastXdays:** Integer (e.g., `365` for 1 year)

**type:** `"price"` (default, can omit) or `"volume"`

---

## SF_MAP() Parameters

```
=SF_MAP(code, type, filter)
```

**type:** `"cusip"` (default), `"isin"`, `"cik"`

**filter:** Exchange name (e.g., `"nasdaq"`) or currency code (e.g., `"usd"`). Only for ISIN.

---

## SF_BROKERAGE() Parameters

```
=SF_BROKERAGE(account, type, metrics, startDate, endDate, txnType, options)
```

**Type:** `"holdings"`, `"orders"`, `"balances"`, `"transactions"`, `"optionsPositions"`

**txnType (transactions only):** `"BUY"`, `"SELL"`, `"DIVIDEND"`, `"CONTRIBUTION"`, `"WITHDRAWAL"`, `"REI"`, `"INTEREST"`, `"FEE"`, `"OPTIONEXPIRATION"`, `"OPTIONASSIGNMENT"`, `"OPTIONEXERCISE"`, `"TRANSFER"`

**Options:** `NH`

---

## Legacy Type Names (historicalFinancials*)

The older SF() documentation also references these type names which may still work:

| Legacy Type | Current Equivalent |
|-------------|-------------------|
| `historicalFinancialsIncome` | `income` |
| `historicalFinancialsBalance` | `balancesheet` |
| `historicalFinancialsCash` | `cashflow` |
| `historicalFinancialsIncomeQ1`..`Q4` | `incomeQ1`..`Q4` |
| `historicalFinancialsBalanceQ1`..`Q4` | `balancesheetQ1`..`Q4` |
| `historicalFinancialsCashQ1`..`Q4` | `cashflowQ1`..`Q4` |
| `historicalFinancialsCashQ` | `cashflowQ` |
| `historicalFinancialsIncomeTTM` | `incomeTTM` |
| `historicalFinancialsBalanceTTM` | `balancesheetTTM` |
| `historicalFinancialsCashTTM` | `cashflowTTM` |

---

## Data Coverage Notes

- **Global coverage:** 80,000+ financial assets across 100+ exchanges
- **US only features:** ESG, price targets, insider transactions/stats, pre/post market, revenue segmentation
- **Institutional holders:** Selected major markets only
- **Historical depth:** 30+ years of financial statements
- **FOREX/crypto:** Use `includeWeekends` option for weekend data
