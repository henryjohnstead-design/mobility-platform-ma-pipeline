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

# Summary Box
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
        with st.expander("View Python Script"):
            try:
                # Dynamically opens your live script file
                with open("pages/pdf_parser.py", "r") as f:
                    pdf_script = f.read()
                st.code(pdf_script, language='python')
            except FileNotFoundError:
                st.warning("🔗 Appending full code... Ensure `pages/pdf_parser.py` is in your repository.")
            
    with col2:
        with st.expander("View Sourcing Output Table"):
            try:
                sourcing_df = pd.read_csv("python_PDFparse.xlsx - Megabuyte50_Rankings.csv")
                st.dataframe(sourcing_df[["Rank", "Company", "Sector", "Ownership", "Revenue (GBPm)", "EBITDA (GBPm)"]].head(10), use_container_width=True)
            except Exception:
                st.write("📁 Sourcing data view ready upon repository refresh.")

# ==========================================
# PHASE 2: Conducting a Bolt-on Strategy
# ==========================================
st.markdown("<div style='text-align: center; font-size: 24px;'>⬇️</div>", unsafe_allow_html=True)

with st.container(border=True):
    st.markdown("### Phase 2: Conducting a Bolt-on Strategy")
    st.write(
        "**Objective:** Identified strategic bolts on targets and synthesised findings into a "
        "formal Investment Committee presentation memo."
    )
    
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
# PHASE 3: Retrieving Financial Data
# ==========================================
st.markdown("<div style='text-align: center; font-size: 24px;'>⬇️</div>", unsafe_allow_html=True)

with st.container(border=True):
    st.markdown("### Phase 3: Retrieving Financial Data")
    st.write(
        "**Objective:** Programmatically harvested financial registry filings from Companies House across "
        "a 2-stage execution pipeline."
    )
    
    tab1, tab2 = st.tabs(["Stage 1", "Stage 2"])
    
    with tab1:
        st.write("Queries the Companies House API to map trading names to verified legal entity registration numbers")
        
        col_m1, col_m2 = st.columns(2)
        with col_m1:
            with st.expander("View Mapping Script"):
                try:
                    # Dynamically opens your mapping script file
                    with open("pages/mapping_financials.py", "r") as f:
                        mapping_script = f.read()
                    st.code(mapping_script, language='python')
                except FileNotFoundError:
                    st.warning("🔗 Appending full code... Ensure `pages/mapping_financials.py` is in your repository.")
        with col_m2:
            with st.expander("View Mapping Targets Table"):
                try:
                    mapping_df = pd.read_csv("Mapping Output.xlsx - Sheet1.csv")
                    st.dataframe(mapping_df, use_container_width=True)
                except Exception:
                    st.write("📁 Mapping file link updating...")
            
    with tab2:
        st.write("Parses financial metrics from the companies' iXBRL digital filings")
        
        col_e1, col_e2 = st.columns(2)
        with col_e1:
            with st.expander("View Extraction Script"):
                try:
                    # Dynamically opens your extraction script file
                    with open("pages/extraction_financials.py", "r") as f:
                        extraction_script = f.read()
                    st.code(extraction_script, language='python')
                except FileNotFoundError:
                    st.warning("🔗 Appending full code... Ensure `pages/extraction_financials.py` is in your repository.")
        with col_e2:
            with st.expander("View Extracted Data Table"):
                try:
                    extracted_financials = pd.read_csv("Financials + CCA.xlsx - Target Financials.csv")
                    st.dataframe(extracted_financials[["Company", "Revenue (£)", "Operating Profit / EBIT (£)", "EBITDA Derived (£)", "Net Debt (£)"]], use_container_width=True)
                except Exception:
                    st.write("📁 Financial statement link updating...")

    # Financial Engineering Gaps Solution Box
    st.info(
        "**Problem:** There were gaps in the financial output data due to small/medium companies filing abridged "
        "or simplified accounts.\n\n"
        "**Solution:** Built top-down predictive industry logic and peer-group averages to estimate missing line items "
        "and reconstitute complete institutional income statements."
    )
    
    with st.expander("📊 View Completed & Reconstituted Financial Data (With Industry Estimates)"):
        try:
            est_financials = pd.read_csv("Mobility_Platform_Financials.xlsx - Sheet1.csv")
            st.dataframe(est_financials, use_container_width=True)
        except Exception:
            st.caption("📁 Financial estimates dataset link updating...")

# ==========================================
# PHASE 4: Valuation & Institutional Modeling
# ==========================================
st.markdown("<div style='text-align: center; font-size: 24px;'>⬇️</div>", unsafe_allow_html=True)

with st.container(border=True):
    st.markdown("### Phase 4: Comparable Companies Analysis (CCA) & LBO Model")
    st.write(
        "**Objective:** Validated pricing multiples against public and private peers. "
        "Then I ran a debt sizing framework to see how much bank debt the cash flows could safely service."
    )
    
    with st.expander("📊 View Valuation & Leverage Summary Dashboard"):
        try:
            val_df = pd.read_csv("Financials + CCA.xlsx - Valuation Summary.csv")
            st.dataframe(val_df, use_container_width=True)
        except Exception:
            st.write("📁 Valuation summary sheet linking...")

    st.markdown("---")
    
    # Download Core Excel Model Asset
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
st.write("Thank you for reviewing my project. Feel free to explore the technical code structures via the sidebar pages")
