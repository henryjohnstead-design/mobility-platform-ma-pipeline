# mobility-platform-ma-pipeline
## Commercial Context & Business Case

In the lower-middle market, manual M&A target sourcing is bottlenecked by unstructured regulatory registry filings, fragmented industry reports, and inconsistent corporate reporting layouts. This programmatic data engineering pipeline automates deal sourcing, entity verification and the financial extraction step of a buy-and-build investment strategy.

The pipeline resolves three core bottlenecks:

1. **Deal Ideation & PDF Scraping (`pdf_parser.py`)**
   * *The Bottleneck:* Promising targets are often locked inside multi-column industry PDFs or awards reports (e.g. Megabuyte50) where text awards and fragmented page boundaries cause standard PDF scraping text grids to bleed together.
   * *The Solution:* Engineered a robust extraction script utilizing `pdfplumber` paired with a custom right-to-left parsing sequence. Because financial metrics are more structured than descriptive text, the script isolates target companies by trailing metrics first, bypassing text bleeding and automating the initial programmatic identification of 50 mid-market candidates.

2. **Legal Entity Resolution & Registry Verification (`mapping_financials.py`)**
   * *The Bottleneck:* Trading names used in industry reports rarely match official registry legal names due to historic corporate rebrands, abbreviations, or complex parent-subsidiary structures.
   * *The Solution:* Integrated the official Companies House API to search candidates, applying temporal and situational filters (e.g., checking active statuses and incorporation cutoffs) to eliminate false matches. This resolves trading names (e.g., "AppyWay") to their exact legal counterparts (e.g., "Yellow Line Parking Limited").

3. **Financial Extraction (`extraction_financials.py`)**
   * *The Bottleneck:* Mid-market financial filings are notoriously non-standardized, utilizing varying iXBRL namespaces (`core:` FRC tags vs. bare strings) that routinely break rigid scrapers. Furthermore, Holdcos often report blank financial lines, masking the operational performance of subsidiaries.
   * *The Solution:* Built an advanced namespace-agnostic iXBRL BeautifulSoup extraction layer. The pipeline searches files purely via element attributes rather than fixed XML names, and automatically implements an algorithmic fallback rule: if a target's primary registry returns zero revenue due to a holding company shell structure, the script identifies and re-routes the API call to extract financials from the core operating subsidiary instead.

### Strategic Impact

This automation shifts the investment team’s capacity away from manual administrative data entry, allowing them to instantly focus on institutional-grade deal execution, including structural bank debt sizing, valuation arbitrage analytics, and cross-selling synergy mapping.
