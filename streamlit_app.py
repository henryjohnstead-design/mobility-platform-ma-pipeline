import streamlit as st
import pandas as pd

# Set up page configuration for a professional finance look
st.set_page_config(
    page_title="UK Tech M&A Roll-Up Strategy",
    page_icon="💼",
    layout="wide"
)

# Main Title & Subtitle
st.title("UK Mid-Market M&A Tech Sector Roll-Up Strategy & Valuation")
st.markdown("### *An End-to-End Buy-Side Advisory & Data Pipeline Simulation*")
st.caption("Developed by Henry Johnstead | Role Focus: Corporate Finance, Deals & Consulting")
st.markdown("---")

# Quick Executive Summary Callout Box
st.info(
    "**Project Thesis:** This interactive dashboard simulates the exact programmatic workflow of an M&A analyst. "
    "It demonstrates automated deal sourcing, registry financial harvesting, and institutional valuation modeling "
    "for a UK IT Services consolidation strategy."
)

st.markdown("## 📊 Strategic Transaction Pipeline")
st.write("Follow the deal workflow sequentially below:")

# ==========================================
# PHASE 1: Automated Deal Sourcing
# ==========================================
with st.container(border=True):
    st.markdown("### 🔍 Phase 1: Algorithmic Sourcing (Megabuyte50)")
    st.write(
        "**Objective:** Programmatically isolate high-performing UK tech firms to anchor the core platform "
        "of our roll-up thesis."
    )
    
    col1, col2 = st.columns(2)
    with col1:
        with st.expander("🛠️ View Sourcing Methodology & Python Script"):
            st.code('''
# Snippet from your pdf_parser.py
import pdfplumber
import pandas as pd

def extract_megabuyte_targets(pdf_path):
    # Extracts text, identifies target columns, and handles tables
    with pdfplumber.open(pdf_path) as pdf:
        # Programmatic parsing logic
        pass
            ''', language='python')
            st.caption("Full code accessible in your `pages/pdf_parser.py` tab.")
            
    with col2:
        with st.expander("📈 View Sourcing Output Table"):
            st.write("### Extracted Target Long-List")
            # Mock Dataframe representation (Replace with your actual CSV file read if desired)
            mock_data = pd.DataFrame({
                "Company Name": ["Target Alpha Tech", "Beta Cloud UK", "Gamma Systems"],
                "Sector": ["IT Services", "Managed Services", "SaaS Solutions"],
                "Source": ["Megabuyte50", "Megabuyte50", "Megabuyte50"]
            })
            st.dataframe(mock_data, use_container_width=True)

# ==========================================
# PHASE 2: Tactical Origination & IC Memo
# ==========================================
st.markdown("<div style='text-align: center; font-size: 24px;'>⬇️</div>", unsafe_allow_html=True)

with st.container(border=True):
    st.markdown("### 📄 Phase 2: Bolt-on Strategy & Investment Committee (IC) Memo")
    st.write(
        "**Objective:** Expanded market mapping via desk research to identify strategic bolt-on targets. "
        "Synthesized findings into a formal Investment Committee presentation memo."
    )
    
    # Provide a direct download for your IC Memo PDF
    # (Assumes 'ic_memo.pdf' is in your repo or generated)
    try:
        with open("ic_memo.pdf", "rb") as f:
            pdf_bytes = f.read()
        st.download_button(
            label="📥 Download Full Investment Committee Memo (PDF)",
            data=pdf_bytes,
            file_name="IC_Memo_UK_Tech_RollUp.pdf",
            mime="application/pdf"
        )
    except FileNotFoundError:
        st.warning("🔗 [IC Memo Placeholder] Upload your `ic_memo.pdf` to your repository root to enable immediate download.")

# ==========================================
# PHASE 3: Data Engineering Pipeline
# ==========================================
st.markdown("<div style='text-align: center; font-size: 24px;'>⬇️</div>", unsafe_allow_html=True)

with st.container(border=True):
    st.markdown("### ⚙️ Phase 3: Financial Harvesting Engine (Companies House iXBRL)")
    st.write(
        "**Objective:** Bypassed the bottleneck of manual data entry by programmatically harvesting "
        "financial registry filings from Companies House across a 2-stage execution pipeline."
    )
    
    tab1, tab2 = st.tabs(["Stage 1: Mapping Phase", "Stage 2: Extraction Phase"])
    
    with tab1:
        st.markdown("#### Registry Schema & Field Mapping")
        st.write("Aligns disparate regulatory registry balance sheet structures into a uniform financial schema.")
        with st.expander("💻 View Mapping Code Snippet"):
            st.code("# Code from mapping_financials.py\n# Normalizes UK GAAP/IFRS tag names to standardised variables", language='python')
            
    with tab2:
        st.markdown("#### Structured iXBRL Extraction Output")
        st.write("Parses raw XML data into fully populated multi-year financial statements.")
        with st.expander("💻 View Extraction Code Snippet & Cleaned Data"):
            st.code("# Code from extraction_financials.py\n# Executes regulatory API calls and extracts numerical tables", language='python')
            # Mock extracted data frame
            extracted_financials = pd.DataFrame({
                "Company": ["Target Alpha", "Target Alpha", "Beta Cloud"],
                "Year": [2024, 2025, 2025],
                "Turnover (£)": ["12,450,000", "14,100,000", "8,900,000"],
                "Operating Profit (£)": ["1,850,000", "2,100,000", "950,000"]
            })
            st.dataframe(extracted_financials, use_container_width=True)

# ==========================================
# PHASE 4: Financial Engineering Adjustments
# ==========================================
st.markdown("<div style='text-align: center; font-size: 24px;'>⬇️</div>", unsafe_allow_html=True)

with st.container(border=True):
    st.markdown("### 🧠 Phase 4: Financial Engineering & Normalization")
    st.write(
        "**Objective:** Resolved data gaps inherent to small/medium companies that file 'abridged' or simplified "
        "accounts. Implemented predictive top-down industry logic and benchmark estimates to reconstitute full "
        "income statements (e.g., estimating gross margins based on peer-group software averages)."
    )
    st.caption("💡 *Demonstrates professional commercial judgment when dealing with messy middle-market data.*")

# ==========================================
# PHASE 5: Valuation & Institutional Modeling
# ==========================================
st.markdown("<div style='text-align: center; font-size: 24px;'>⬇️</div>", unsafe_allow_html=True)

with st.container(border=True):
    st.markdown("### 📈 Phase 5: Comparable Companies Analysis (CCA) & LBO Model")
    st.write(
        "**Objective:** Validated pricing multiples (EV/EBITDA, P/E) against public/private peer universes "
        "and ran a debt sizing framework to see how much leveraged bank debt the cash flows could safely service."
    )
    
    # Interactive Demo Area
    st.markdown("#### 🛠️ Live LBO Stress-Testing Tool")
    st.write("Test the deal's debt capacity right here on the web:")
    
    c1, c2, c3 = st.columns(3)
    with c1:
        ebitda = st.number_input("Target EBITDA (£)", value=2000000, step=250000)
    with c2:
        debt_multiple = st.slider("Senior Debt Multiple (x EBITDA)", 2.0, 6.0, 3.5, step=0.1)
    with c3:
        interest_rate = st.slider("Bank Cost of Debt (%)", 4.0, 12.0, 7.5, step=0.25)
        
    total_debt = ebitda * debt_multiple
    annual_interest = total_debt * (interest_rate / 100)
    
    # Metric Callouts
    st.metric(label="Maximum Safe Debt Funding", value=f"£{total_debt:,.0f}")
    st.caption(f"Estimated Annual Interest Payment: £{annual_interest:,.0f}. Assumes a DSCR safety floor of >1.5x.")
    
    st.markdown("---")
    
    # Download Core Excel Model Asset
    try:
        with open("cca_lbo_model.xlsx", "rb") as f:
            excel_bytes = f.read()
        st.download_button(
            label="🟢 Download Complete Institutional Excel Model (CCA + LBO)",
            data=excel_bytes,
            file_name="Tech_Sector_CCA_LBO_Model.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    except FileNotFoundError:
        st.warning("🔗 [Excel Model Placeholder] Upload your financial `.xlsx` file to your repository root to enable download.")

st.markdown("---")
st.center = st.write("✨ *Thank you for reviewing my project. Feel free to pivot through the technical file breakdowns in the sidebar.*")
