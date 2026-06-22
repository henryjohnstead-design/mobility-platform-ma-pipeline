import streamlit as st

st.markdown(
    "<p style='font-size:18px; margin-top:0;'>Queries the Companies House API to map trading names to verified legal entity registration numbers.</p>",
    unsafe_allow_html=True
)

st.code('''

import requests
import json
import pandas as pd

# 1. Configuration & Authentication Setup
API_KEY = "YOUR_COMPANIES_HOUSE_API_KEY"
BASE_URL = "https://api.company-information.service.gov.uk"


target_companies = [
    "ParkingEye Limited",
    "TMA Group (UK) Limited",       
    "Yellow Line Parking Limited",  
    "Ebbon Group Limited",           
    "FleetCheck Limited",
    "Joju Limited"
]

def get_company_number(company_name):
    search_url = f"{BASE_URL}/search/companies"
    response = requests.get(search_url, auth=(API_KEY, ''), params={'q': company_name})
    
    if response.status_code == 200:
        results = response.json().get('items', [])
        if results:
            # Grab the top match from the search results
            top_match = results[0]
            return {
                "name": top_match.get('title'),
                "company_number": top_match.get('company_number'),
                "status": top_match.get('company_status')
            }
    print(f"⚠️ Warning: Could not resolve numbers for {company_name}")
    return None

# Execute the mapping phase
company_registry_map = []
print("Initiating Companies House API Target Mapping...")

for target in target_companies:
    registry_data = get_company_number(target)
    if registry_data:
        company_registry_map.append(registry_data)
        print(f"Resolved: {registry_data['name']} -> ID: {registry_data['company_number']} [{registry_data['status']}]")

# Convert to DataFrame for visualization
registry_df = pd.DataFrame(company_registry_map)
print("\n Verified Target Registry Database:")
print(registry_df)

#  GENERATE THE EXCEL FILE 
registry_df.to_excel("Mobility_Platform_Registry.xlsx", index=False)
print("\n Excel file saved to your working directory.")

# Explanation of code 

# Step 1: Configuration & Authentication Setup

# Step 2: Then we define a function which Queries Companies House API
# to resolve a company name into its official 8-digit registry number

# Step 3: Execute the mapping phase. This takes a list of raw text strings (your 
# human-readable company names) and maps them to a structured list of verified database 
# entities (the official government registry codes) before doing any hard math.

# Step 4: Output to Excel


#%%

#first attempt output file had TMA wrong and Joju wrong too so here is new code

import requests
import pandas as pd
 
 
# =============================================================================
# STEP 1: Configuration & Authentication Setup
# =============================================================================
 
API_KEY  = "614ab5d1-3143-4f97-a1b3-30857aace5d6"
BASE_URL = "https://api.company-information.service.gov.uk"
OUTPUT_PATH = "/Users/henrystead/Desktop/Mobility_Platform_Registry.xlsx"
 
# Target companies for Project Mobility Platform.
# Each entry provides:
#   - trading_name:        the name we know the business by
#   - search_name:         the name to query in Companies House (may differ due to
#                          rebrands, e.g. AppyWay is legally registered as Yellow Line Parking)
#   - incorporated_before: upper bound on incorporation date, used to filter out
#                          recently incorporated companies with similar names from
#                          polluting the search results (e.g. TMAC Group Ltd)
 
TARGET_COMPANIES = [
    {
        "trading_name":        "ParkingEye",
        "search_name":         "ParkingEye Limited",
        "incorporated_before": "2010-01-01",
    },
    {
        "trading_name":        "TMA Group",
        "search_name":         "TMA Group Holdings",
        "incorporated_before": "2022-01-01",
    },
    {
        "trading_name":        "AppyWay",
        "search_name":         "Yellow Line Parking",   # AppyWay's registered legal name pre-rebrand
        "incorporated_before": "2015-01-01",
    },
    {
        "trading_name":        "Ebbon Group",
        "search_name":         "Ebbon Group Limited",
        "incorporated_before": "2000-01-01",
    },
    {
        "trading_name":        "FleetCheck",
        "search_name":         "FleetCheck Limited",
        "incorporated_before": "2010-01-01",
    },
    {
        "trading_name":        "Joju Charging",
        "search_name":         "Joju Charging Network",
        "incorporated_before": "2022-01-01",
    },
]
 
 
# =============================================================================
# STEP 2: Define Search & Validation Functions
# =============================================================================
 
def search_company(search_name, incorporated_before):
    """
    Queries the Companies House search endpoint for a given name and returns
    the best matching active company incorporated before the specified date.
 
    Using items_per_page=10 ensures we scan multiple candidates rather than
    blindly accepting the top result, which may be a recently incorporated
    company with a similar name.
 
    Parameters
    ----------
    search_name        : str  — name to search for on Companies House
    incorporated_before: str  — ISO date string (YYYY-MM-DD); filters out
                                companies incorporated on or after this date
 
    Returns
    -------
    dict with keys: company_number, registered_name, status, date_incorporated
    None if no suitable match is found
    """
    url = f"{BASE_URL}/search/companies"
    response = requests.get(
        url,
        auth=(API_KEY, ''),
        params={'q': search_name, 'items_per_page': 10}
    )
 
    if response.status_code != 200:
        print(f"  ⚠️  API error {response.status_code} for query: '{search_name}'")
        return None
 
    candidates = response.json().get('items', [])
 
    for candidate in candidates:
        # Reject dissolved or inactive entities
        if candidate.get('company_status') != 'active':
            continue
 
        # Reject companies incorporated on or after the cutoff date
        date_of_creation = candidate.get('date_of_creation', '')
        if date_of_creation and date_of_creation >= incorporated_before:
            continue
 
        # First candidate passing both filters is our match
        return {
            "company_number":    candidate.get('company_number'),
            "registered_name":   candidate.get('title'),
            "status":            candidate.get('company_status'),
            "date_incorporated": date_of_creation,
        }
 
    print(f"  ⚠️  No valid match found for: '{search_name}'")
    return None
 
 
def fetch_company_detail(company_number):
    """
    Fetches the full company record directly by company number from Companies
    House. Used to enrich the registry with SIC codes and other metadata that
    the search endpoint does not return.
 
    Parameters
    ----------
    company_number: str — the 8-digit Companies House number
 
    Returns
    -------
    dict with sic_codes key, or empty dict on failure
    """
    url = f"{BASE_URL}/company/{company_number}"
    response = requests.get(url, auth=(API_KEY, ''))
 
    if response.status_code == 200:
        data = response.json()
        return {
            "sic_codes": ", ".join(data.get('sic_codes', []))
        }
 
    return {"sic_codes": "N/A"}
 
 
# =============================================================================
# STEP 3: Execute the Mapping Phase
# =============================================================================
# This phase takes a list of human-readable trading names and maps each one to
# a verified Companies House entity. The search function filters candidates by
# active status and incorporation date, ensuring we resolve to the correct
# legal entity rather than a recently incorporated company with a similar name.
# A second API call then enriches each resolved entity with SIC codes.
# =============================================================================
 
print("=" * 60)
print("  Project Mobility Platform — Company Registry Mapping")
print("=" * 60)
 
registry = []
 
for target in TARGET_COMPANIES:
    print(f"\n  Resolving: {target['trading_name']} ...")
 
    # Step 3a: Search for the company and apply date filter
    match = search_company(target['search_name'], target['incorporated_before'])
 
    if not match:
        print(f"  ❌ Failed to resolve {target['trading_name']} — skipping")
        continue
 
    # Step 3b: Enrich with SIC codes via direct company lookup
    detail = fetch_company_detail(match['company_number'])
 
    print(f"  ✅ Resolved")
    print(f"     Trading name:    {target['trading_name']}")
    print(f"     Registered name: {match['registered_name']}")
    print(f"     Number:          {match['company_number']}")
    print(f"     Status:          {match['status']}")
    print(f"     Incorporated:    {match['date_incorporated']}")
    print(f"     SIC codes:       {detail['sic_codes']}")
 
    registry.append({
        "Trading Name":      target['trading_name'],
        "Registered Name":   match['registered_name'],
        "Company Number":    match['company_number'],
        "Status":            match['status'],
        "Date Incorporated": match['date_incorporated'],
        "SIC Codes":         detail['sic_codes'],
    })
 
 
# =============================================================================
# STEP 4: Output to Excel
# =============================================================================
 
df = pd.DataFrame(registry)
df.to_excel(OUTPUT_PATH, index=False)
 
print("\n" + "=" * 60)
print(f"  Registry saved to: {OUTPUT_PATH}")
print(f"  {len(registry)} of {len(TARGET_COMPANIES)} companies resolved successfully.")
print("=" * 60)

''', language='python')
