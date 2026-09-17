import os
import httpx
import streamlit as st

API_URL = os.getenv("DANY_API_URL", "http://127.0.0.1:8000")

st.set_page_config(page_title="Dany Super Agent", page_icon="🛡️", layout="wide")
st.title("Dany Super Agent")
st.caption("Local, privacy-first VMware/Broadcom support assistance. Suggestions only; no infrastructure execution. Use synthetic data only. Not affiliated with VMware or Broadcom.")

workflow = st.selectbox("Specialist workflow", ["case", "logs", "email", "automation", "business", "learning", "career", "portfolio", "documents", "tech_devices", "media", "pc_navigation"], format_func=lambda x: {
    "case": "VMware Case Agent", "logs": "Log Analysis Agent", "email": "Customer Email Agent", "automation": "Automation Agent",
    "business": "Business Strategy Agent", "learning": "Learning Coach",
    "career": "Career & Job Application Agent", "documents": "Documents & Forms Agent",
    "tech_devices": "Consumer Tech & Device Troubleshooting Agent", "media": "Media & Creative Task Agent",
    "portfolio": "Project Portfolio Agent",
    "pc_navigation": "PC Navigation (approval-gated instructions only)"
}[x])
col1, col2 = st.columns(2)
product = col1.text_input("Product (recommended)", placeholder="VMware vCenter Server")
version = col2.text_input("Version/build (required for KB applicability)", placeholder="8.0 U3 / build ...")
uploaded = st.file_uploader("Optional UTF-8 log, text, or CSV", type=["log", "txt", "csv"])
text_input = st.text_area("Case description or log excerpt", height=220)
save = st.checkbox("Save redacted analysis to local SQLite memory", value=False)
external_action_approved = st.checkbox("Explicit approval for this single proposed PC action", value=False, disabled=workflow != "pc_navigation")

if st.button("Analyze", type="primary"):
    try:
        combined = text_input
        if uploaded:
            response = httpx.post(f"{API_URL}/upload", files={"file": (uploaded.name, uploaded.getvalue())}, timeout=30)
            response.raise_for_status()
            upload_result = response.json()
            combined = f"{combined}\n{upload_result['redacted_text']}".strip()
            if upload_result["redactions"]:
                st.info("Sensitive upload fields were redacted before analysis: " + ", ".join(upload_result["redactions"]))
        if not combined.strip():
            st.warning("Enter a case description or upload a file.")
        else:
            response = httpx.post(f"{API_URL}/analyze", json={"workflow": workflow, "text": combined, "product": product or None, "version": version or None, "save_to_memory": save, "external_action_approved": external_action_approved}, timeout=30)
            response.raise_for_status()
            result = response.json()
            if result["redactions"]:
                st.warning("Redacted before persistence: " + ", ".join(result["redactions"]))
            st.markdown(result["content"])
            with st.expander("Source/evidence map"):
                st.dataframe(result["evidence"], use_container_width=True)
    except httpx.HTTPError as exc:
        st.error(f"Backend unavailable or request failed: {exc}")
