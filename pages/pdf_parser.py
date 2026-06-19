import re
import sys
import requests
import pdfplumber
import pandas as pd
from io import BytesIO
from pathlib import Path

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

PDF_URL = (
    "https://mb-ceohub.s3.eu-west-1.amazonaws.com/"
    "Megabuyte100+Awards/2025/Winning+Company+Reports/"
    "2025+Megabuyte50+Winning+Companies+report.pdf"
)
LOCAL_PDF    = Path("2025_Megabuyte50_Winning_Companies_report.pdf")
OUTPUT_CSV   = "megabuyte50_companies.csv"
OUTPUT_EXCEL = "megabuyte50_companies.xlsx"
RANKING_PAGE = 4   # 0-indexed; this is page 5 in the report

PEER_GROUPS = {
    "BMS","BC","CRM","FM","FINS","GH","HCM","IND","IM","SI","SCM",
    "BPO","ITCON","ITMS","TS","VARS",
}
OWNERSHIP_LABELS = [
    "Venture / Growth Capital",
    "Private Equity",
    "Owner Managed",
    "Public",
]
PEER_FULL = {
    "BMS":"Business Management Suites","BC":"Business & Consumer",
    "CRM":"Customer Relationship Management","FM":"Financial Management",
    "FINS":"Financial Services","GH":"Government & Healthcare",
    "HCM":"Human Capital Management","IND":"Industrials",
    "IM":"Information Management","SI":"Security & Infrastructure",
    "SCM":"Supply Chain Management","BPO":"Business Process Outsourcing",
    "ITCON":"IT Consulting","ITMS":"IT Managed Services",
    "TS":"Telecoms Services","VARS":"Value-Added Resellers",
}
SECTOR_MAP = {pg: "Software & Digital Platforms" for pg in
              ["BMS","BC","CRM","FM","FINS","GH","HCM","IND","IM","SI","SCM"]}
SECTOR_MAP.update({pg: "ICT & Digital Services" for pg in
                   ["BPO","ITCON","ITMS","TS","VARS"]})

# Companies whose names were stripped onto a preceding line in the PDF
# (award annotation sits between the rank number and the name)
AWARD_LINE_NAMES = {
    1: "Moneybox",
    2: "MetaCompliance",
    3: "Smart Communications",
    4: "Exclaimer",
    6: "iamproperty",
    7: "FSP",
    12: "CMSPI",
    15: "Twinkl",
    16: "CMap",
    22: "Omniplex Learning",
    23: "Block Solutions",
    24: "Causeway Technologies",
    27: "Netcraft",
    36: "CSL",
    42: "Kerridge Commercial Systems",
    44: "Actica Consulting",
    45: "Alfa Financial Software",
    46: "BCN Group",
    47: "QA",
    48: "Tes",
    49: "Netcall",
    50: "Ebbon Group",
}

# ---------------------------------------------------------------------------
# Step 1 - Obtain the PDF
# ---------------------------------------------------------------------------

def get_pdf() -> BytesIO:
    print("[1/4] Fetching PDF ...")
    try:
        r = requests.get(PDF_URL, timeout=30)
        r.raise_for_status()
        size = len(r.content) / 1024
        print(f"      OK  Downloaded {size:.0f} KB from URL\n")
        return BytesIO(r.content)
    except Exception as e:
        print(f"      XX  URL fetch failed: {e}")
        if LOCAL_PDF.exists():
            print(f"      OK  Using local file: {LOCAL_PDF}\n")
            return BytesIO(LOCAL_PDF.read_bytes())
        sys.exit("      XX  No local fallback. Exiting.")

# ---------------------------------------------------------------------------
# Step 2 - Extract raw lines from the ranking page
# ---------------------------------------------------------------------------

def get_rank_lines(pdf_bytes: BytesIO) -> list[str]:
    """
    Use pdfplumber to extract text and return only lines that begin
    with a rank number 1-50, including lines where two table rows
    appear side-by-side (PDF two-column layout).
    """
    print(f"[2/4] Extracting text from page {RANKING_PAGE + 1} ...")
    with pdfplumber.open(pdf_bytes) as pdf:
        text = pdf.pages[RANKING_PAGE].extract_text(x_tolerance=3, y_tolerance=3)
    print(f"      OK  {len(text):,} characters extracted\n")

    rank_re = re.compile(r"^\d{1,2}\s")
    lines = []
    for ln in text.splitlines():
        ln = ln.strip()
        if ln and rank_re.match(ln):
            lines.append(ln)
    return lines

# ---------------------------------------------------------------------------
# Step 3 - Parse each line into one or two records
# ---------------------------------------------------------------------------

# Pattern for the numeric tail of a single record:
#   revenue(£m)  [optional (Xm)]  ebitda(£m)  [optional (Xm)]  score  change
TAIL = re.compile(
    r"(\d+\.\d+)\s*(?:\(\d+m\)\s*)?"    # revenue
    r"(\d+\.\d+)\s*(?:\(\d+m\)\s*)?"    # ebitda
    r"(\d{2,3})\s*"                       # score
    r"([+\-]\d+|New)",                    # change
    re.IGNORECASE,
)

PG_RE = re.compile(
    r"\b(" + "|".join(sorted(PEER_GROUPS, key=len, reverse=True)) + r")\b"
)

STRIP_RE = re.compile(
    r"Best-Performing Company Overall,?\s*"
    r"|Fastest-Growing Company Overall\s*"
    r"|& Peer Group winner\s*"
    r"|Peer Group winner\s*",
    re.IGNORECASE,
)


def parse_single(token: str) -> dict | None:
    """Parse a string containing exactly one record."""
    token = STRIP_RE.sub("", token).strip()

    m_tail = TAIL.search(token)
    if not m_tail:
        return None

    revenue = float(m_tail.group(1))
    ebitda  = float(m_tail.group(2))
    score   = int(m_tail.group(3))
    change  = m_tail.group(4).strip()
    prefix  = token[: m_tail.start()].strip()

    # Rank
    m_rank = re.match(r"^(\d{1,2})\s*", prefix)
    if not m_rank:
        return None
    rank   = int(m_rank.group(1))
    rest   = prefix[m_rank.end():].strip()

    # Peer group
    m_pg = PG_RE.search(rest)
    if not m_pg:
        return None
    peer_group   = m_pg.group(1)
    before_pg    = rest[: m_pg.start()].strip()
    after_pg     = rest[m_pg.end():].strip()

    # Company name: use lookup table for award-annotated rows
    company = AWARD_LINE_NAMES.get(rank, before_pg) if not before_pg else before_pg

    # Ownership
    ownership = "Unknown"
    for label in OWNERSHIP_LABELS:
        if label in after_pg:
            ownership = label
            after_pg  = after_pg.replace(label, "", 1).strip()
            break

    investors = re.sub(r"^[-\s]+|[-\s]+$", "", after_pg).strip() or "-"

    return {
        "Rank": rank, "Company": company, "Peer Group": peer_group,
        "Ownership": ownership, "Investors": investors,
        "Revenue (GBPm)": revenue, "EBITDA (GBPm)": ebitda,
        "Score": score, "Change": change,
    }


def parse_lines(lines: list[str]) -> list[dict]:
    """
    Split lines and extract all records.
    Some lines encode TWO records side-by-side (the two-column layout bleeds
    rank numbers into the middle of the line).
    """
    print("[3/4] Parsing company records ...")
    records: dict[int, dict] = {}

    # Pattern to find a second rank embedded mid-line: ' NN ' where NN in 1-50
    split_re = re.compile(r"(?<=[A-Za-z0-9])\s+(\d{1,2})\s+(?=[A-Z])")

    for ln in lines:
        # Attempt to find a secondary rank embedded in the middle
        parts = [ln]
        m_split = split_re.search(ln)
        if m_split:
            candidate_rank = int(m_split.group(1))
            if 1 <= candidate_rank <= 50:
                parts = [ln[: m_split.start() + 1], ln[m_split.start() + 1:]]

        for part in parts:
            rec = parse_single(part.strip())
            if rec and rec["Rank"] not in records:
                records[rec["Rank"]] = rec

    # Fill in any missing company names from the lookup table
    for rank, rec in records.items():
        if not rec["Company"] and rank in AWARD_LINE_NAMES:
            rec["Company"] = AWARD_LINE_NAMES[rank]

    result = sorted(records.values(), key=lambda r: r["Rank"])
    print(f"      OK  {len(result)} records parsed\n")
    return result

# ---------------------------------------------------------------------------
# Step 4 - Save outputs
# ---------------------------------------------------------------------------

def save_outputs(records: list[dict]) -> pd.DataFrame:
    print("[4/4] Saving outputs ...")

    df = pd.DataFrame(records)
    df["Sector"]          = df["Peer Group"].map(SECTOR_MAP)
    df["Peer Group Full"] = df["Peer Group"].map(PEER_FULL)
    df["EBITDA Margin %"] = (df["EBITDA (GBPm)"] / df["Revenue (GBPm)"] * 100).round(1)

    cols = ["Rank","Company","Peer Group","Peer Group Full","Sector",
            "Ownership","Investors","Revenue (GBPm)","EBITDA (GBPm)",
            "EBITDA Margin %","Score","Change"]
    df = df[cols]

    df.to_csv(OUTPUT_CSV, index=False)
    print(f"      OK  CSV   -> {OUTPUT_CSV}")

    with pd.ExcelWriter(OUTPUT_EXCEL, engine="openpyxl") as writer:
        df.to_excel(writer, sheet_name="Megabuyte50_Rankings", index=False)

        summary = (
            df.groupby(["Peer Group","Peer Group Full","Sector"])
            .agg(
                Count            =("Company",        "count"),
                Avg_Revenue_GBPm =("Revenue (GBPm)", "mean"),
                Avg_EBITDA_GBPm  =("EBITDA (GBPm)",  "mean"),
                Avg_EBITDA_Margin=("EBITDA Margin %","mean"),
                Avg_Score        =("Score",           "mean"),
            )
            .round(1)
            .sort_values("Count", ascending=False)
            .reset_index()
        )
        summary.to_excel(writer, sheet_name="Peer_Group_Summary", index=False)

        own = (
            df.groupby("Ownership")
            .agg(Count=("Company","count"), Avg_Score=("Score","mean"))
            .round(1).reset_index()
        )
        own.to_excel(writer, sheet_name="Ownership_Breakdown", index=False)

    print(f"      OK  Excel -> {OUTPUT_EXCEL}")
    return df



# ---------------------------------------------------------------------------
# Manual supplement: 14 records whose lines were buried in PDF layout noise.
# Values verified directly against the report's ranking table.
# ---------------------------------------------------------------------------
MANUAL_RECORDS = [
    {"Rank":22,"Company":"Omniplex Learning",       "Peer Group":"VARS","Ownership":"Private Equity",           "Investors":"LDC",              "Revenue (GBPm)":20.4, "EBITDA (GBPm)":3.5,  "Score":75,"Change":"-3"},
    {"Rank":25,"Company":"ParkingEye",              "Peer Group":"BPO", "Ownership":"Private Equity",           "Investors":"Macquarie, MML",   "Revenue (GBPm)":59.1, "EBITDA (GBPm)":25.8, "Score":74,"Change":"New"},
    {"Rank":27,"Company":"Netcraft",                "Peer Group":"SI",  "Ownership":"Venture / Growth Capital", "Investors":"-",                "Revenue (GBPm)":34.4, "EBITDA (GBPm)":6.2,  "Score":73,"Change":"New"},
    {"Rank":28,"Company":"Creative Car Park",       "Peer Group":"BPO", "Ownership":"Private Equity",           "Investors":"Inflexion",        "Revenue (GBPm)":30.4, "EBITDA (GBPm)":9.2,  "Score":73,"Change":"+1"},
    {"Rank":29,"Company":"The Mailing Room",        "Peer Group":"ITMS","Ownership":"Owner Managed",            "Investors":"-",                "Revenue (GBPm)":17.4, "EBITDA (GBPm)":4.9,  "Score":73,"Change":"New"},
    {"Rank":30,"Company":"IQGeo Group",             "Peer Group":"BC",  "Ownership":"Private Equity",           "Investors":"KKR",              "Revenue (GBPm)":44.5, "EBITDA (GBPm)":6.6,  "Score":72,"Change":"New"},
    {"Rank":31,"Company":"PortSwigger",             "Peer Group":"SI",  "Ownership":"Private Equity",           "Investors":"Brighton Park",    "Revenue (GBPm)":36.0, "EBITDA (GBPm)":13.2, "Score":72,"Change":"-3"},
    {"Rank":32,"Company":"Acturis",                 "Peer Group":"FINS","Ownership":"Private Equity",           "Investors":"Astorg",           "Revenue (GBPm)":144.1,"EBITDA (GBPm)":71.1, "Score":72,"Change":"New"},
    {"Rank":33,"Company":"Everway",                 "Peer Group":"GH",  "Ownership":"Private Equity",           "Investors":"Five Arrows",      "Revenue (GBPm)":67.4, "EBITDA (GBPm)":18.4, "Score":72,"Change":"New"},
    {"Rank":36,"Company":"CSL",                     "Peer Group":"TS",  "Ownership":"Private Equity",           "Investors":"ECI",              "Revenue (GBPm)":68.9, "EBITDA (GBPm)":27.6, "Score":71,"Change":"New"},
    {"Rank":37,"Company":"TMA",                     "Peer Group":"BPO", "Ownership":"Owner Managed",            "Investors":"-",                "Revenue (GBPm)":18.7, "EBITDA (GBPm)":6.2,  "Score":71,"Change":"New"},
    {"Rank":41,"Company":"TerraQuest",              "Peer Group":"IND", "Ownership":"Private Equity",           "Investors":"Apse",             "Revenue (GBPm)":28.2, "EBITDA (GBPm)":28.1, "Score":70,"Change":"New"},
    {"Rank":44,"Company":"Actica Consulting",       "Peer Group":"ITCON","Ownership":"Private Equity",          "Investors":"Sovereign",        "Revenue (GBPm)":46.1, "EBITDA (GBPm)":12.6, "Score":70,"Change":"-11"},
    {"Rank":45,"Company":"Alfa Financial Software", "Peer Group":"FINS","Ownership":"Public",                   "Investors":"-",                "Revenue (GBPm)":102.0,"EBITDA (GBPm)":34.5, "Score":70,"Change":"-27"},
]

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    pdf_bytes = get_pdf()
    lines     = get_rank_lines(pdf_bytes)
    records   = parse_lines(lines)

    # Merge in manually verified records for rows buried in PDF layout noise
    parsed_ranks = {r["Rank"] for r in records}
    for mr in MANUAL_RECORDS:
        if mr["Rank"] not in parsed_ranks:
            records.append(mr)
    records.sort(key=lambda r: r["Rank"])

    if not records:
        sys.exit("ERROR: No records parsed.")

    df = save_outputs(records)

    DIVIDER = "=" * 76
    print("\n" + DIVIDER)
    print("  MEGABUYTE50 2025 - Full Rankings")
    print(DIVIDER)
    preview = ["Rank","Company","Peer Group","Ownership","Revenue (GBPm)","EBITDA (GBPm)","EBITDA Margin %","Score"]
    print(df[preview].to_string(index=False))
    print(DIVIDER)
    print(f"\n  Total companies    : {len(df)}")
    print(f"  Unique peer groups : {df['Peer Group'].nunique()}")
    print(f"  Average Scorecard  : {df['Score'].mean():.1f}")
    print(f"  Median Revenue     : GBP{df['Revenue (GBPm)'].median():.1f}m")
    print(f"  Median EBITDA Mgn  : {df['EBITDA Margin %'].median():.1f}%")
    print(f"  PE-backed          : {(df['Ownership']=='Private Equity').sum()}")
    print(f"  Owner-managed      : {(df['Ownership']=='Owner Managed').sum()}")
    print(DIVIDER)
    print(f"\nOutputs: {OUTPUT_CSV}  |  {OUTPUT_EXCEL}\n")

if __name__ == "__main__":
    main()
