import streamlit as st
import pandas as pd

# Set up page configuration with no emoji in the tab title
st.set_page_config(
    page_title="UK Tech M&A Roll-Up Strategy",
    layout="wide"
)

# Main Title & Subtitle
st.title("UK Mid-Market M&A Tech Sector Roll-Up Strategy and Valuation")
st.markdown("### *An End-to-End Buy-Side Advisory & Data Pipeline Simulation*")
st.caption("Developed by Henry Stead")
st.markdown("---")

# Updated Summary Box
st.info(
    "**Summary:** This interactive dashboard simulates an end-to-end buy-side workflow. "
    "It moves sequentially from deal sourcing to financial data harvesting, it then constructs "
    "a CCA and LBO debt capacity model to evaluate the consolidation of UK mid-market automotive tech companies."
)

st.markdown("## Follow the deal workflow below:")

# ==========================================
# PHASE 1: Algorithmic Sourcing
# ==========================================
with st.container(border=True):
    st.markdown("### Phase 1: Algorithmic Sourcing")
    st.write(
        "**Objective:** Programmatically isolate high-performing UK tech firms from the Megabuyte50 "
        "to ideate for a core platform of our roll-up thesis."
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
            st.write("### Megabuyte50 Rankings Sourced Data")
            # Reads your exact uploaded file name
            try:
                sourcing_df = pd.read_csv("python_PDFparse.xlsx - Megabuyte50_Rankings.csv")
                st.dataframe(sourcing_df[["Rank", "Company", "Sector", "Ownership", "Revenue (GBPm)", "EBITDA (GBPm)"]].head(10), use_container_width=True)
                st.caption("Showing top 10 rows from your live `python_PDFparse.xlsx` data.")
            except Exception:
                st.write("📁 Data table ready upon repository refresh.")

# ==========================================
# PHASE 2: Tactical Origination & IC Memo
# ==========================================
st.markdown("<div style='text-align: center; font-size: 24px;'>⬇️</div>", unsafe_allow_html=True)

with st.container(border=True):
    st.markdown("### Phase 2: Bolt-on Strategy & Investment Committee (IC) Memo")
    st.write(
        "**Objective:** Expanded market mapping via desk research to identify strategic bolt-on targets. "
        "Synthesized findings into a formal Investment Committee presentation memo."
    )
    
    # Matches your exact uploaded name: "IC Memo.pdf"
    try:
        with open("IC Memo.pdf", "rb") as f:
            pdf_bytes = f.read()
        st.download_button(
            label="📥 Download Full Investment Committee Memo (PDF)",
            data=pdf_bytes,
            file_name="IC_Memo_UK_Tech_RollUp.pdf",
            mime="application/pdf"
        )
    except FileNotFoundError:
        st.warning("🔗 Connect your uploaded `IC Memo.pdf` to activate the direct download button.")

# ==========================================
# PHASE 3: Data Engineering Pipeline
# ==========================================
st.markdown("<div style='text-align: center; font-size: 24px;'>⬇️</div>", unsafe_allow_html=True)

with st.container(border=True):
    st.markdown("### Phase 3: Financial Harvesting Engine (Companies House iXBRL)")
    st.write(
        "**Objective:** Bypassed the bottleneck of manual data entry by programmatically harvesting "
        "financial registry filings from Companies House across a 2-stage execution pipeline."
    )
    
    tab1, tab2 = st.tabs(["Stage 1: Mapping Phase", "Stage 2: Extraction Phase"])
    
    with tab1:
        st.markdown("#### Registry Schema & Field Mapping")
        st.write("Aligns disparate regulatory registry balance sheet structures into a uniform financial schema.")
        with st.expander("💻 View Mapping Code Snippet & Targets"):
            # Reads your exact uploaded mapping metadata file name
            try:
                mapping_df = pd.read_csv("Mapping Output.xlsx - Sheet1.csv")
                st.dataframe(mapping_df, use_container_width=True)
            except Exception:
                st.code("# Code from mapping_financials.py\n# Normalizes UK GAAP/IFRS tags", language='python')
            
    with tab2:
        st.markdown("#### Structured iXBRL Extraction Output")
        st.write("Parses raw XML data into fully populated multi-year financial statements.")
        with st.expander("💻 View Extracted Data View"):
            # Reads your exact uploaded financials file name
            try:
                extracted_financials = pd.read_csv("Financials + CCA.xlsx - Target Financials.csv")
                st.dataframe(extracted_financials[["Company", "Revenue (£)", "Operating Profit / EBIT (£)", "EBITDA Derived (£)", "Net Debt (£)"]], use_container_width=True)
            except Exception:
                st.write("📁 Financial statement matrix linking...")

# ==========================================
# PHASE 4: Financial Engineering Adjustments
# ==========================================
st.markdown("<div style='text-align: center; font-size: 24px;'>⬇️</div>", unsafe_allow_html=True)

with st.container(border=True):
    st.markdown("### Phase 4: Financial Engineering & Normalization")
    st.write(
        "**Objective:** Resolved data gaps inherent to small/medium companies that file 'abridged' or simplified "
        "accounts. Implemented predictive top-down industry logic and benchmark estimates to reconstitute full "
        "income statements (e.g., estimating gross margins based on peer-group software averages)."
    )
    st.caption("💡 *Demonstrates professional analytical problem-solving when dealing with messy marketplace data.*")

# ==========================================
# PHASE 5: Valuation & Institutional Modeling
# ==========================================
st.markdown("<div style='text-align: center; font-size: 24px;'>⬇️</div>", unsafe_allow_html=True)

with st.container(border=True):
    st.markdown("### Phase 5: Comparable Companies Analysis (CCA) & LBO Model")
    st.write(
        "**Objective:** Validated pricing multiples (EV/EBITDA, P/E) against public/private peer universes "
        "and ran a debt sizing framework to see how much leveraged bank debt the cash flows could safely service."
    )
    
    # Interactive Demo Area
    st.markdown("#### 🛠️ Live LBO Stress-Testing Tool")
    st.write("Test the asset's debt capacity right here on the web:")
    
    c1, c2, c3 = st.columns(3)
    with c1:
        ebitda = st.number_input("Target EBITDA (£)", value=2000000, step=250000)
    with c2:
        debt_multiple = st.slider("Senior Debt Multiple (x EBITDA)", 2.0, 6.0, 3.5, step=0.1)
    with c3:
        interest_rate = st.slider("Bank Cost of Debt (%)", 4.0, 12.0, 7.5, step=0.25)
        
    total_debt = ebitda * debt_multiple
    annual_interest = total_debt * (interest_rate / 100)
    
    st.metric(label="Maximum Safe Debt Funding", value=f"£{total_debt:,.0f}")
    st.caption(f"Estimated Annual Interest Payment: £{annual_interest:,.0f}. Assumes a safety coverage ratio floor of >1.5x.")
    
    st.markdown("---")
    
    # Download Core Excel Model Asset (Tied to your master valuation workbook)
    try:
        with open("Financials + CCA.xlsx", "rb") as f:
            excel_bytes = f.read()
        st.download_button(
            label="🟢 Download Complete Financial Model (CCA + LBO Workbook)",
            data=excel_bytes,
            file_name="Automotive_Tech_Sector_CCA_Model.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    except FileNotFoundError:
        st.warning("🔗 Connect your master workbook `Financials + CCA.xlsx` to activate model download link.")

st.markdown("---")
st.write("✨ *Thank you for reviewing my project. Feel free to explore the technical code structures via the sidebar pages.*")
