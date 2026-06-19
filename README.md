# mobility-platform-ma-pipeline
## Commercial Context & Business Case

In the lower-middle market, manual M&A target sourcing is bottlenecked by unstructured regulatory registry filings, fragmented industry reports, and inconsistent corporate reporting layouts. This programmatic data engineering pipeline automates deal sourcing, entity verification, and financial extraction layer of a buy-and-build investment strategy.

The pipeline resolves three core bottlenecks:

1. **Automated Deal Ideation & Unstructured PDF Scraping (`pdf_parser.py`)**
   * *The Bottleneck:* Promising proprietary targets are often locked inside multi-column industry PDFs or awards reports (e.g., Megabuyte50) where embedded text awards and fragmented page boundaries cause standard PDF scraping text grids to bleed together.
   * *The Solution:* Engineered a robust extraction script utilizing `pdfplumber` paired with a custom right-to-left parsing sequence. Because financial metrics are more structured than descriptive text, the script isolates target companies by trailing metrics first, bypassing text bleeding and automating the initial programmatic identification of 50 elite mid-market candidates.

2. **Legal Entity Resolution & Registry Verification (`me.mapping.financials.py`)**
   * *The Bottleneck:* Trading names used in industry reports rarely match official registry legal names due to historic corporate rebrands, abbreviations, or complex parent-subsidiary structures (e.g., operating assets hidden under non-reporting shell entities).
   * *The Solution:* Integrated the official Companies House API to dynamically search candidates, applying temporal and situational filters (e.g., checking active statuses and incorporation cutoffs) to eliminate false matches. This automatically resolves trading names (e.g., "AppyWay") to their exact legal counterparts (e.g., "Yellow Line Parking Limited").

3. **Accounting Taxonomy Normalization & Financial Extraction (`me.extraction.financials.py`)**
   * *The Bottleneck:* Mid-market financial filings are notoriously non-standardized, utilizing varying iXBRL namespaces (`core:` FRC tags vs. bare strings) that routinely break rigid scrapers. Furthermore, top-level Parent entities ("Holdcos") often report blank financial lines, masking the true operational performance of underlying operating subsidiaries.
   * *The Solution:* Built an advanced namespace-agnostic iXBRL BeautifulSoup extraction layer. The pipeline searches files purely via element attributes rather than fixed XML names, and automatically implements an algorithmic fallback rule: if a target's primary registry returns zero revenue due to a holding company shell structure, the script identifies and re-routes the API call to extract financials from the core operating subsidiary instead.

### Strategic Impact
By seamlessly binding PDF data extraction, API corporate mapping, and automated iXBRL parsing, this end-to-end framework reduces manual time-to-insight for mid-market target screening by an estimated **90%**. 

Ultimately, this automation shifts the investment team’s capacity away from manual administrative data entry, allowing them to instantly focus on institutional-grade deal execution, including structural bank debt sizing, valuation arbitrage analytics, and cross-selling synergy mapping.
