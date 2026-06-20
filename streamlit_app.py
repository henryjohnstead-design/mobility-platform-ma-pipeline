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
                # 1. Try reading the exact filename directly
                sourcing_df = pd.read_csv("python_PDFparse.xlsx - Megabuyte50_Rankings.csv")
                st.dataframe(sourcing_df, use_container_width=True)
            except Exception:
                try:
                    # 2. Flexible fallback: scan directory case-insensitively for 'megabuyte' or 'rankings'
                    import os
                    files = os.listdir(".")
                    matched_files = [f for f in files if "megabuyte" in f.lower() or "rankings" in f.lower()]
                    
                    if matched_files:
                        sourcing_df = pd.read_csv(matched_files[0])
                        st.dataframe(sourcing_df, use_container_width=True)
                    else:
                        st.info("📁 Loading Sourcing Output Table... Please ensure your CSV files are uploaded to the root folder.")
                except Exception:
                    st.info("📁 Sourcing data view ready upon repository refresh.")

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
