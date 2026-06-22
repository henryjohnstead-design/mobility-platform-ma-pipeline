import streamlit as st
import pandas as pd
import os

# ==========================================
# MODERN NAVIGATION ROUTING (SOLUTION 1)
# ==========================================
# 1. Define this main file explicitly as a page with your desired sidebar name
overview_page = st.Page(
    "streamlit_app.py", 
    title="Overview", 
    icon="📊", 
    default=True
)

# 2. Define your existing sub-pages so they still appear underneath it in the sidebar
pdf_parser_page = st.Page("pages/1_pdf_parser.py", title="1 PDF Parser")
mapping_financials_page = st.Page("pages/2_mapping_financials.py", title="2 Mapping Financials")
extraction_financials_page = st.Page("pages/3_extraction_financials.py", title="3 Extraction Financials")

# 3. Pass all pages to the navigation manager
pg = st.navigation([overview_page, pdf_parser_page, mapping_financials_page, extraction_financials_page])

# 4. Set global page configuration and execute routing
st.set_page_config(
    page_title="Deal Pipeline",
    layout="wide"
)
pg.run()


# ==========================================
# YOUR EXISTING APPLICATION LOGIC
# ==========================================
def safe_load_excel(filename, sheet_name=0, search_keyword=None):
    try:
        if os.path.exists(filename):
            return pd.read_excel(filename, sheet_name=sheet_name)
        if search_keyword:
            files = os.listdir(".")
            matched = [
                f for f in files
                if search_keyword.lower() in f.lower() and f.endswith(".xlsx")
            ]
            if matched:
                return pd.read_excel(matched[0], sheet_name=sheet_name)
    except Exception as e:
        st.error(f"Could not load '{filename}' (sheet: {sheet_name}): {e}")
    return None

ARROW = "<div style='text-align: center; font-size: 20px; color: black; margin: 4px 0;'>↓</div>"

# Main Title & Subtitle
st.title("UK Mid-Market M&A Tech Sector Roll-Up Strategy and Valuation")
st.markdown("### *An End-to-End Buy-Side Advisory & Data Pipeline Simulation*")
st.caption("Developed by Henry Stead")
st.markdown("---")

# Summary Box
st.info(
    "**Summary:** This dashboard simulates an end-to-end buy-side workflow. "
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
        st.page_link(
            pdf_parser_page, # Updated to use the page object variable
            label="📄 Open Full Python Script →"
        )
    with col2:
        with st.expander("View Sourcing Output Table"):
            df = safe_load_excel(
                "python_PDFparse.xlsx",
                sheet_name="Megabuyte50_Rankings",
                search_keyword="Megabuyte50"
            )
            if df is not None:
                st.dataframe(df, use_container_width=True)
            else:
                st.info("Sourcing output table not found — check the sheet name in python_PDFparse.xlsx.")

# ==========================================
# PHASE 2: Bolt-on Strategy
# ==========================================
st.markdown(ARROW, unsafe_allow_html=True)

with st.container(border=True):
    st.markdown("### Phase 2: Conducting a Bolt-on Strategy")
    st.write(
        "**Objective:** Identified strategic bolt-on targets and synthesised findings into a "
        "formal Investment Committee presentation memo."
    )

    try:
        with open("IC Memo.pdf", "rb") as f:
            pdf_bytes = f.read()
        st.download_button(
            label="Download Full Investment Committee Memo (PDF)",
            data=pdf_bytes,
            file_name="IC_Memo_UK_Tech_RollUp.pdf",
            mime="application/pdf"
        )
    except FileNotFoundError:
        st.warning("Connect your uploaded `IC Memo.pdf` to activate the direct download button.")

# ==========================================
# PHASE 3: Retrieving Financial Data
# ==========================================
st.markdown(ARROW, unsafe_allow_html=True)

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
            st.page_link(
                mapping_financials_page, # Updated to use the page object variable
                label="📄 Open Full Mapping Script →"
            )
        with col_m2:
            with st.expander("View Mapping Targets Table"):
                df_map = safe_load_excel(
                    "Mapping Output.xlsx",
                    sheet_name="Sheet1",
                    search_keyword="Mapping"
                )
                if df_map is not None:
                    st.dataframe(df_map, use_container_width=True)
                else:
                    st.write("Mapping table not found — check the sheet name in Mapping Output.xlsx.")

    with tab2:
        st.write("Parses financial metrics from the companies' iXBRL digital filings")

        col_e1, col_e2 = st.columns(2)
        with col_e1:
            st.page_link(
                extraction_financials_page, # Updated to use the page object variable
                label="📄 Open Full Extraction Script →"
            )
        with col_e2:
            with st.expander("View Extracted Data Table"):
                df_ext = safe_load_excel(
                    "Financials + CCA.xlsx",
                    sheet_name="Target Financials",
                    search_keyword="Financials"
                )
                if df_ext is not None:
                    st.dataframe(df_ext, use_container_width=True)
                else:
                    st.write("Extracted financials table not found — check the sheet name in Financials + CCA.xlsx.")

    st.markdown("---")

    st.info(
        "**Problem:** There were gaps in the financial output data due to companies filing abridged "
        "or simplified accounts.\n\n"
        "**Solution:** Used industry and peer-group averages to estimate missing line items "
        "and complete income statements."
    )

    with st.expander("View Completed & Reconstituted Financial Data (With Industry Estimates)"):
        df_est = safe_load_excel(
            "Mobility_Platform_Financials.xlsx",
            sheet_name="Sheet1",
            search_keyword="Mobility_Platform"
        )
        if df_est is not None:
            st.dataframe(df_est, use_container_width=True)
        else:
            st.caption("Reconstituted financials table not found — check the sheet name in Mobility_Platform_Financials.xlsx.")

# ==========================================
# PHASE 4: Valuation & Institutional Modeling
# ==========================================
st.markdown(ARROW, unsafe_allow_html=True)

with st.container(border=True):
    st.markdown("### Phase 4: Comparable Companies Analysis (CCA) & LBO Model")
    st.write(
        "**Objective:** Validated pricing multiples against public and private peers. "
        "Then I ran a debt sizing framework to see how much bank debt the cash flows could safely service."
    )

    st.markdown("---")

    try:
        with open("Financials + CCA.xlsx", "rb") as f:
            excel_bytes = f.read()
        st.download_button(
            label="Download Complete Financial Model (CCA + LBO Workbook)",
            data=excel_bytes,
            file_name="Automotive_Tech_Sector_CCA_Model.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    except FileNotFoundError:
        st.warning("Connect your master workbook `Financials + CCA.xlsx` to activate model download link.")

st.markdown("---")
st.write("Thank you for reviewing my project. Feel free to explore the technical code structures via the sidebar pages")
