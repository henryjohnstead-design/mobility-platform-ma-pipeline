import requests
import pandas as pd
from bs4 import BeautifulSoup
import warnings
warnings.filterwarnings("ignore")


# =============================================================================
# STEP 1: Configuration & Authentication Setup
# =============================================================================

API_KEY      = "YOUR_COMPANIES_HOUSE_API_KEY"
BASE_URL     = "https://api.company-information.service.gov.uk"
OUTPUT_PATH  = "Mobility_Platform_Financials.xlsx"

# Registry from the mapping phase.
# Where the filing company is a holdco (e.g. TMA Group Holdings), the
# operating subsidiary is listed as fallback_number — this is where revenue
# and P&L data actually lives.
REGISTRY = [
    {
        "trading_name":    "ParkingEye",
        "company_number":  "05134454",
        "fallback_number": None,         # PDF filer — manual input needed
    },
    {
        "trading_name":    "TMA Group",
        "company_number":  "12604248",   # Holdco — no revenue tagged here
        "fallback_number": "09863398",   # TMA Group (UK) Ltd — operating sub
    },
    {
        "trading_name":    "AppyWay",
        "company_number":  "08584086",
        "fallback_number": None,
    },
    {
        "trading_name":    "Ebbon Group",
        "company_number":  "00722865",
        "fallback_number": None,
    },
    {
        "trading_name":    "FleetCheck",
        "company_number":  "05674824",
        "fallback_number": None,
    },
    {
        "trading_name":    "Joju Charging",
        "company_number":  "11476928",
        "fallback_number": None,
    },
]

# Verified XBRL tag names from inspecting TMA Group's actual iXBRL filing.
# All tags use the FRC 2025 core: taxonomy namespace.
# The parser strips the namespace prefix, so we search both with and without
# the "core:" prefix to handle both parser behaviours.
XBRL_TAGS = {
    "revenue": [
        "core:Turnover", "Turnover",
        "core:Revenue", "Revenue",
        "core:TurnoverRevenue", "TurnoverRevenue",
        "core:TurnoverGrossOperatingRevenue", "TurnoverGrossOperatingRevenue",
    ],
    "cost_of_sales": [
        "core:CostSales", "CostSales",
    ],
    "gross_profit": [
        "core:GrossProfitLoss", "GrossProfitLoss",
    ],
    "admin_expenses": [
        "core:AdministrativeExpenses", "AdministrativeExpenses",
    ],
    "operating_profit": [
        "core:OperatingProfit", "OperatingProfit",
        "core:OperatingProfitLoss", "OperatingProfitLoss",
        "core:ProfitLossFromOperatingActivities", "ProfitLossFromOperatingActivities",
    ],
    "depreciation_amortisation": [
        "core:IncreaseFromDepreciationChargeForYearPropertyPlantEquipment",
        "IncreaseFromDepreciationChargeForYearPropertyPlantEquipment",
        "core:DepreciationAmortisationImpairmentAndOtherMovements",
        "DepreciationAmortisationImpairmentAndOtherMovements",
    ],
    "amortisation": [
        "core:IncreaseFromAmortisationChargeForYearIntangibleAssets",
        "IncreaseFromAmortisationChargeForYearIntangibleAssets",
    ],
    "interest_expense": [
        "core:InterestPayableSimilarChargesFinanceCosts", "InterestPayableSimilarChargesFinanceCosts",
        "core:InterestPaidClassifiedAsOperatingActivities", "InterestPaidClassifiedAsOperatingActivities",
    ],
    "interest_income": [
        "core:OtherInterestReceivableSimilarIncomeFinanceIncome", "OtherInterestReceivableSimilarIncomeFinanceIncome",
        "core:InterestIncomeOnBankDeposits", "InterestIncomeOnBankDeposits",
    ],
    "profit_before_tax": [
        "core:ProfitLossOnOrdinaryActivitiesBeforeTax", "ProfitLossOnOrdinaryActivitiesBeforeTax",
    ],
    "tax": [
        "core:TaxTaxCreditOnProfitOrLossOnOrdinaryActivities", "TaxTaxCreditOnProfitOrLossOnOrdinaryActivities",
        "core:CurrentTaxForPeriod", "CurrentTaxForPeriod",
    ],
    "profit_after_tax": [
        "core:ProfitLoss", "ProfitLoss",
        "core:ProfitLossForPeriod", "ProfitLossForPeriod",
    ],
    "intangible_assets": [
        "core:IntangibleAssets", "IntangibleAssets",
    ],
    "fixed_assets": [
        "core:PropertyPlantEquipment", "PropertyPlantEquipment",
    ],
    "total_assets_less_current_liabilities": [
        "core:TotalAssetsLessCurrentLiabilities", "TotalAssetsLessCurrentLiabilities",
    ],
    "cash": [
        "core:CashCashEquivalents", "CashCashEquivalents",
        "core:CashBankOnHand", "CashBankOnHand",
    ],
    "total_borrowings": [
        "core:TotalBorrowings", "TotalBorrowings",
        "core:OtherRemainingBorrowings", "OtherRemainingBorrowings",
    ],
    "total_equity": [
        "core:Equity", "Equity",
        "core:NetAssetsLiabilities", "NetAssetsLiabilities",
    ],
    "net_assets": [
        "core:NetAssetsLiabilities", "NetAssetsLiabilities",
    ],
    "employees": [
        "core:AverageNumberEmployeesDuringPeriod", "AverageNumberEmployeesDuringPeriod",
    ],
}


# =============================================================================
# STEP 2: Define Extraction Functions
# =============================================================================

def get_latest_full_accounts_url(company_number):
    """
    Queries the Companies House filing history API and returns the document
    metadata URL for the most recent full annual accounts (type AA).
    Skips dormant, micro-entity, and amended filings.
    """
    url = f"{BASE_URL}/company/{company_number}/filing-history"
    response = requests.get(
        url,
        auth=(API_KEY, ''),
        params={'category': 'accounts', 'items_per_page': 20}
    )
    if response.status_code != 200:
        print(f"    ⚠️  Filing history error {response.status_code}")
        return None

    for filing in response.json().get('items', []):
        if filing.get('type') != 'AA':
            continue
        desc = filing.get('description', '').lower()
        if any(s in desc for s in ['dormant', 'micro', 'amended']):
            continue
        doc_url = filing.get('links', {}).get('document_metadata')
        if doc_url:
            print(f"    Filing found: {filing.get('date')} — {filing.get('description')}")
            return doc_url

    print("    ⚠️  No full annual accounts found")
    return None


def get_ixbrl_document(metadata_url):
    """
    Two-step download via the Companies House Document API:
      Step A: Fetch metadata to confirm iXBRL is available
      Step B: Follow the AWS redirect WITHOUT the API key to get the content
    Returns raw iXBRL content string, or None if unavailable.
    """
    meta = requests.get(metadata_url, auth=(API_KEY, '')).json()
    resources = meta.get('resources', {})
    print(f"    Available formats: {list(resources.keys())}")

    if 'application/xhtml+xml' not in resources:
        print("    ⚠️  iXBRL not available for this filing (PDF only)")
        return None

    content_url = metadata_url + "/content"
    r = requests.get(
        content_url,
        auth=(API_KEY, ''),
        headers={'Accept': 'application/xhtml+xml'},
        allow_redirects=False
    )
    if r.status_code == 302:
        return requests.get(r.headers.get('Location')).text
    return r.text if r.status_code == 200 else None


def parse_ixbrl_financials(ixbrl_content, trading_name):
    """
    Parses the iXBRL document to extract tagged numeric facts.

    Uses two complementary strategies to handle namespace stripping by
    different XML/HTML parsers:

    Strategy A — find_all with string match on the 'name' attribute:
      Searches all tags that have a 'name' attribute containing our target
      tag names. This works regardless of whether the parser preserves the
      ix:nonfraction element name, because we are matching on the attribute
      value (e.g. 'core:ProfitLoss') rather than the element name itself.

    Strategy B — find_all by element name variants:
      Tries both 'ix:nonfraction' and 'nonfraction' as element names to
      handle parsers that do and don't preserve the namespace prefix.

    Takes the first occurrence of each tag (current year figure), ignoring
    prior year comparatives which appear as subsequent duplicates.
    """
    soup = BeautifulSoup(ixbrl_content, 'lxml')
    
    all_named = soup.find_all(attrs={"name": True})
    print(f"    DEBUG — elements with name attr: {len(all_named)}")
    if all_named:
        print(f"    DEBUG — first element name: {all_named[0].get('name')}")
    else:
        print(f"    DEBUG — total tags in doc: {len(soup.find_all())}")
        print(f"    DEBUG — first 3 tags: {[t.name for t in soup.find_all()[:3]]}")

    tag_values = {}

    # Strategy A: match on name attribute value — most reliable
    all_named = soup.find_all(attrs={"name": True})
    print(f"    Elements with 'name' attribute: {len(all_named)}")

    for el in all_named:
        tag_name = el.get('name', '')
        if not tag_name:
            continue
        if tag_name in tag_values:
            continue  # Keep first occurrence (current year)
        raw = el.get_text(strip=True).replace(',', '').replace('(', '-').replace(')', '')
        try:
            tag_values[tag_name] = float(raw)
        except ValueError:
            continue

    # Strategy B: fallback — try element name variants if Strategy A found nothing
    if not tag_values:
        print("    Strategy A found nothing — trying element name search...")
        for element_name in ['ix:nonfraction', 'nonfraction', 'ix:nonFraction']:
            elements = soup.find_all(element_name)
            if elements:
                print(f"    Found {len(elements)} elements as '{element_name}'")
                for el in elements:
                    tag_name = el.get('name', '')
                    if not tag_name or tag_name in tag_values:
                        continue
                    raw = el.get_text(strip=True).replace(',', '').replace('(', '-').replace(')', '')
                    try:
                        tag_values[tag_name] = float(raw)
                    except ValueError:
                        continue
                break

    print(f"    Unique XBRL tags extracted: {len(tag_values)}")

    # Map our metric names to extracted values using the tag priority lists
    financials = {"trading_name": trading_name}
    for metric, tag_list in XBRL_TAGS.items():
        value = None
        for tag in tag_list:
            if tag in tag_values:
                value = tag_values[tag]
                break
        financials[metric] = value

    # Derive EBITDA = Operating Profit + PPE Depreciation + Intangible Amortisation
    op   = financials.get('operating_profit')
    dep  = financials.get('depreciation_amortisation') or 0
    amor = financials.get('amortisation') or 0
    if op is not None and (dep + amor) > 0:
        financials['ebitda_derived'] = op + dep + amor
    else:
        financials['ebitda_derived'] = None

    # Derive Net Debt = Total Borrowings - Cash
    debt = financials.get('total_borrowings')
    cash = financials.get('cash')
    financials['net_debt'] = (debt - cash) if (debt is not None and cash is not None) else None

    # Derive EBITDA Margin = EBITDA / Revenue
    rev    = financials.get('revenue')
    ebitda = financials.get('ebitda_derived')
    financials['ebitda_margin'] = round(ebitda / rev, 4) if (rev and ebitda) else None

    return financials


# =============================================================================
# STEP 3: Execute the Extraction Phase
# =============================================================================

print("=" * 65)
print("  Project Mobility Platform — Financial Data Extraction")
print("=" * 65)

all_financials = []

for company in REGISTRY:
    trading_name = company['trading_name']
    print(f"\n  [{trading_name}]")

    financials = None

    for attempt, number in enumerate([company['company_number'], company.get('fallback_number')]):
        if not number:
            continue
        label = "primary" if attempt == 0 else "fallback subsidiary"
        print(f"    Trying {label}: {number}")

        meta_url = get_latest_full_accounts_url(number)
        if not meta_url:
            continue

        ixbrl = get_ixbrl_document(meta_url)
        if not ixbrl:
            continue

        result = parse_ixbrl_financials(ixbrl, trading_name)

        # If primary had no revenue, try fallback subsidiary
        if result.get('revenue') is None and attempt == 0 and company.get('fallback_number'):
            print(f"    ⚠️  No revenue in primary — trying subsidiary...")
            continue

        financials = result
        break

    if financials is None:
        print(f"  ❌ No iXBRL data — manual input required")
        financials = {"trading_name": trading_name}

    def fmt(v): return f"£{v:>14,.0f}" if v is not None else "            N/A"
    print(f"  ✅ Result:")
    print(f"     Revenue:           {fmt(financials.get('revenue'))}")
    print(f"     Gross Profit:      {fmt(financials.get('gross_profit'))}")
    print(f"     Operating Profit:  {fmt(financials.get('operating_profit'))}")
    print(f"     D&A (PPE):         {fmt(financials.get('depreciation_amortisation'))}")
    print(f"     Amortisation:      {fmt(financials.get('amortisation'))}")
    print(f"     EBITDA (derived):  {fmt(financials.get('ebitda_derived'))}")
    print(f"     EBITDA Margin:     {str(round(financials['ebitda_margin']*100,1))+'%' if financials.get('ebitda_margin') else 'N/A'}")
    print(f"     Interest Expense:  {fmt(financials.get('interest_expense'))}")
    print(f"     Profit Before Tax: {fmt(financials.get('profit_before_tax'))}")
    print(f"     Profit After Tax:  {fmt(financials.get('profit_after_tax'))}")
    print(f"     Cash:              {fmt(financials.get('cash'))}")
    print(f"     Total Borrowings:  {fmt(financials.get('total_borrowings'))}")
    print(f"     Net Debt:          {fmt(financials.get('net_debt'))}")
    print(f"     Total Equity:      {fmt(financials.get('total_equity'))}")
    print(f"     Employees:         {int(financials['employees']) if financials.get('employees') else 'N/A'}")

    all_financials.append(financials)


# =============================================================================
# STEP 4: Output to Excel
# =============================================================================

COLUMN_ORDER = [
    "trading_name", "revenue", "cost_of_sales", "gross_profit",
    "admin_expenses", "operating_profit", "depreciation_amortisation",
    "amortisation", "ebitda_derived", "ebitda_margin", "interest_expense",
    "interest_income", "profit_before_tax", "tax", "profit_after_tax",
    "intangible_assets", "fixed_assets", "cash", "total_borrowings",
    "net_debt", "total_assets_less_current_liabilities",
    "total_equity", "net_assets", "employees",
]

COLUMN_LABELS = {
    "trading_name":                          "Company",
    "revenue":                               "Revenue (£)",
    "cost_of_sales":                         "Cost of Sales (£)",
    "gross_profit":                          "Gross Profit (£)",
    "admin_expenses":                        "Admin Expenses (£)",
    "operating_profit":                      "Operating Profit / EBIT (£)",
    "depreciation_amortisation":             "Depreciation — PPE (£)",
    "amortisation":                          "Amortisation — Intangibles (£)",
    "ebitda_derived":                        "EBITDA Derived (£)",
    "ebitda_margin":                         "EBITDA Margin (%)",
    "interest_expense":                      "Interest Expense (£)",
    "interest_income":                       "Interest Income (£)",
    "profit_before_tax":                     "Profit Before Tax (£)",
    "tax":                                   "Tax (£)",
    "profit_after_tax":                      "Profit After Tax (£)",
    "intangible_assets":                     "Intangible Assets (£)",
    "fixed_assets":                          "Property Plant & Equipment (£)",
    "cash":                                  "Cash & Equivalents (£)",
    "total_borrowings":                      "Total Borrowings (£)",
    "net_debt":                              "Net Debt (£)",
    "total_assets_less_current_liabilities": "Total Assets Less Current Liabilities (£)",
    "total_equity":                          "Total Equity (£)",
    "net_assets":                            "Net Assets (£)",
    "employees":                             "Average Employees",
}

df = pd.DataFrame(all_financials)
for col in COLUMN_ORDER:
    if col not in df.columns:
        df[col] = None
df = df[COLUMN_ORDER].rename(columns=COLUMN_LABELS)
df.to_excel(OUTPUT_PATH, index=False)

print("\n" + "=" * 65)
print(f"  Saved to: {OUTPUT_PATH}")
print(f"  {len(all_financials)} companies processed.")
print("  NOTE: Companies showing N/A require manual input from")
print("  their PDF accounts on the Companies House website.")
print("=" * 65)
