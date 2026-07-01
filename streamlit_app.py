import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import os

# ==========================================
# HERO HEXAGON GRAPHIC (Key Results Summary)
# ==========================================
def show_hero_hexagons():
    html = """
<html>
<head>
    <style>
    body { margin: 0; padding: 0; }
    .hex-wrap {
        display: flex;
        justify-content: center;
        align-items: stretch;
        gap: 22px;
        flex-wrap: wrap;
        margin: 6px 0 18px 0;
    }
    .hex {
        position: relative;
        width: 178px;
        height: 176px;
        clip-path: polygon(25% 3%, 75% 3%, 100% 50%, 75% 97%, 25% 97%, 0% 50%);
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        text-align: center;
        padding: 14px 20px;
        color: #ffffff;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    }
    .hex-1 { background: linear-gradient(160deg, #1f2a44, #33456e); }
    .hex-2 { background: linear-gradient(160deg, #7a1f2b, #b23a2f); }
    .hex-3 { background: linear-gradient(160deg, #1e4d3a, #2f7d57); }
    .hex-4 { background: linear-gradient(160deg, #3d3560, #6a4c93); width: 210px; }

    .hex-label {
        font-size: 0.62rem;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        opacity: 0.85;
        margin-bottom: 4px;
        font-weight: 600;
    }
    .hex-stat {
        font-size: 1.55rem;
        font-weight: 800;
        line-height: 1.05;
    }
    .hex-substat {
        font-size: 0.68rem;
        opacity: 0.9;
        margin-top: 5px;
        line-height: 1.3;
    }
    .hex-multiline .hex-substat div {
        margin-top: 2px;
    }
    </style>
</head>
<body>

    <div class="hex-wrap">

        <div class="hex hex-1">
            <div class="hex-label">Deal Sourcing</div>
            <div class="hex-stat">50 &rarr; 6</div>
            <div class="hex-substat">50 firms screened (Megabuyte50)<br>3 identified algorithmically<br>+3 sourced manually</div>
        </div>

        <div class="hex hex-2">
            <div class="hex-label">Valuation Arbitrage</div>
            <div class="hex-stat">&pound;79.38m</div>
            <div class="hex-substat">Uplift vs.<br>public peer multiples</div>
        </div>

        <div class="hex hex-3">
            <div class="hex-label">Debt Sizing</div>
            <div class="hex-stat">4.08x</div>
            <div class="hex-substat">Implied DSCR on<br>&pound;143.47m debt capacity</div>
        </div>

        <div class="hex hex-4 hex-multiline">
            <div class="hex-label">Platform Profile</div>
            <div class="hex-stat">&pound;117.65m</div>
            <div class="hex-substat">
                <div>Combined Revenue</div>
                <div>34.9% EBITDA Margin</div>
                <div>&pound;143.47m Debt Capacity</div>
            </div>
        </div>

    </div>

</body>
</html>
    """
    components.html(html, height=210, scrolling=False)


# ==========================================
# DEFINE THE MAIN WRAPPER FUNCTION
# ==========================================
def show_overview():
    """All of your original dashboard content goes inside this function"""

    # Main Title & Subtitle
    st.title("UK Mid-Market M&A Tech Sector Roll-Up Strategy and Valuation")
    st.markdown("### *An End-to-End Buy-Side Advisory & Data Pipeline Simulation*")
    st.caption("Developed by Henry Stead")
    st.markdown("---")

    # Hero hexagon results graphic (sits above the Summary)
    show_hero_hexagons()

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
            with st.expander("Open Full Python Script"):
                if st.button("Go to PDF Parser Script", key="btn_pdf"):
                    st.switch_page(pdf_parser_page)
        with col2:
            try:
                with open("python_PDFparse.xlsx", "rb") as f:
                    sourcing_bytes = f.read()
                st.download_button(
                    label="Download Sourcing Output Table (Excel)",
                    data=sourcing_bytes,
                    file_name="python_PDFparse.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    key="dl_sourcing"
                )
            except FileNotFoundError:
                st.warning("Connect your uploaded `python_PDFparse.xlsx` to activate download link.")

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
                with st.expander("Open Full Mapping Script"):
                    if st.button("Go to Mapping Financials", key="btn_map"):
                        st.switch_page(mapping_financials_page)
            with col_m2:
                try:
                    with open("Mapping Output.xlsx", "rb") as f:
                        mapping_bytes = f.read()
                    st.download_button(
                        label="Download Mapping Targets Table (Excel)",
                        data=mapping_bytes,
                        file_name="Mapping_Output.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        key="dl_mapping"
                    )
                except FileNotFoundError:
                    st.warning("Connect your uploaded `Mapping Output.xlsx` to activate download link.")

        with tab2:
            st.write("Parses financial metrics from the companies' iXBRL digital filings")

            col_e1, col_e2 = st.columns(2)
            with col_e1:
                with st.expander("Open Full Extraction Script"):
                    if st.button("Go to Extraction Financials", key="btn_ext"):
                        st.switch_page(extraction_financials_page)
            with col_e2:
                try:
                    with open("Mobility_Platform_Financials.xlsx", "rb") as f:
                        mobility_bytes = f.read()
                    st.download_button(
                        label="Download Extracted Data Table (Excel)",
                        data=mobility_bytes,
                        file_name="Mobility_Platform_Financials.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        key="dl_mobility"
                    )
                except FileNotFoundError:
                    st.warning("Connect your uploaded `Mobility_Platform_Financials.xlsx` to activate download link.")

        st.markdown("---")

        st.info(
            "**Problem:** There were gaps in the financial output data because of iXBRL tag mismatches, PDF formatting issues and companies filing abridged or simplified accounts.\n\n"
            "**Solution:** I manually filled in the gaps by reading and synthesising the company account. I also used industry and peer-group averages to estimate missing line items."
        )

        try:
            with open("Full_Financials.xlsx", "rb") as f:
                full_financials_bytes = f.read()
            st.download_button(
                label="Download Completed & Reconstituted Financial Data (Excel)",
                data=full_financials_bytes,
                file_name="Full_Financials.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                key="dl_full_financials"
            )
        except FileNotFoundError:
            st.warning("Connect your uploaded `Full_Financials.xlsx` to activate download link.")

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

        try:
            with open("Financials_CCA_LBO.xlsx", "rb") as f:
                excel_bytes = f.read()
            st.download_button(
                label="Download Complete Financial Model (CCA + LBO Workbook)",
                data=excel_bytes,
                file_name="Financials_CCA_LBO.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                key="dl_phase4"
            )
        except FileNotFoundError:
            st.warning("Connect your master workbook `Financials_CCA_LBO.xlsx` to activate model download link.")

    st.markdown("---")
    st.write("Thank you for reviewing my project. Feel free to explore the technical code structures via the sidebar pages")


# ==========================================
# HELPER UTILITIES
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


# ==========================================
# MODERN NAVIGATION ROUTING DEFINITION
# ==========================================
overview_page = st.Page(
    show_overview,
    title="Overview",
    default=True
)

pdf_parser_page = st.Page("pages/1_pdf_parser.py", title="1 PDF Parser")
mapping_financials_page = st.Page("pages/2_mapping_financials.py", title="2 Mapping Financials")
extraction_financials_page = st.Page("pages/3_extraction_financials.py", title="3 Extraction Financials")

pg = st.navigation([overview_page, pdf_parser_page, mapping_financials_page, extraction_financials_page])

st.set_page_config(
    page_title="Deal Pipeline",
    layout="wide"
)
pg.run()
