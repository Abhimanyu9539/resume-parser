import streamlit as st
import requests
import json

# Configuration
API_BASE_URL = "http://localhost:8000"

st.set_page_config(page_title="Resume Parser", page_icon="📄", layout="wide")

st.title("📄 AI-Powered Resume Parser")
st.markdown(
    "Upload your resume (PDF or DOCX) to extract structured information using AI"
)

# File upload section
st.header("Upload Resume")
uploaded_file = st.file_uploader(
    "Choose a resume file",
    type=["pdf", "docx", "doc"],
    help="Upload a PDF or DOCX resume file",
)

if uploaded_file is not None:
    # Display file info
    st.info(
        f"**File:** {uploaded_file.name} | **Size:** {uploaded_file.size / 1024:.2f} KB"
    )

    # Parse button
    if st.button("🚀 Parse Resume", type="primary"):
        with st.spinner("Parsing resume... This may take a few seconds"):
            try:
                # Send file to API
                files = {"file": (uploaded_file.name, uploaded_file.getvalue())}
                response = requests.post(f"{API_BASE_URL}/api/upload", files=files)

                if response.status_code == 201:
                    data = response.json()

                    # Display success message
                    st.success("✅ Resume parsed successfully!")

                    # Document ID
                    st.markdown(f"**Document ID:** `{data['document_id']}`")
                    st.markdown(f"**Extracted At:** {data['extracted_at']}")

                    # Display extracted data
                    st.header("Extracted Information")

                    resume_data = data["data"]

                    # Contact Information
                    if resume_data.get("contact_information"):
                        st.subheader("👤 Contact Information")
                        contact = resume_data["contact_information"]
                        col1, col2 = st.columns(2)
                        with col1:
                            if contact.get("name"):
                                st.markdown(f"**Name:** {contact['name']}")
                            if contact.get("email"):
                                st.markdown(f"**Email:** {contact['email']}")
                            if contact.get("phone"):
                                st.markdown(f"**Phone:** {contact['phone']}")
                        with col2:
                            if contact.get("location"):
                                st.markdown(f"**Location:** {contact['location']}")
                            if contact.get("linkedin"):
                                st.markdown(f"**LinkedIn:** {contact['linkedin']}")
                            if contact.get("github"):
                                st.markdown(f"**GitHub:** {contact['github']}")

                    # Professional Summary
                    if resume_data.get("professional_summary"):
                        st.subheader("📝 Professional Summary")
                        st.markdown(resume_data["professional_summary"])

                    # Work Experience
                    if resume_data.get("work_experience"):
                        st.subheader("💼 Work Experience")
                        for exp in resume_data["work_experience"]:
                            with st.expander(
                                f"{exp['role']} at {exp['company']}", expanded=True
                            ):
                                st.markdown(f"**Duration:** {exp['duration']}")
                                if exp.get("location"):
                                    st.markdown(f"**Location:** {exp['location']}")
                                if exp.get("responsibilities"):
                                    st.markdown("**Responsibilities:**")
                                    for resp in exp["responsibilities"]:
                                        st.markdown(f"- {resp}")

                    # Projects
                    if resume_data.get("projects"):
                        st.subheader("🚀 Projects")
                        for proj in resume_data["projects"]:
                            with st.expander(
                                f"{proj.get('name', 'Project')}", expanded=False
                            ):
                                if proj.get("description"):
                                    st.markdown(
                                        f"**Description:** {proj['description']}"
                                    )
                                if proj.get("aim"):
                                    st.markdown(f"**Aim:** {proj['aim']}")
                                if proj.get("skills_used"):
                                    st.markdown(
                                        f"**Skills:** {', '.join(proj['skills_used'])}"
                                    )

                    # Education
                    if resume_data.get("education"):
                        st.subheader("🎓 Education")
                        for edu in resume_data["education"]:
                            with st.expander(
                                f"{edu.get('degree', 'Degree')} - {edu.get('institution', 'Institution')}",
                                expanded=True,
                            ):
                                if edu.get("year"):
                                    st.markdown(f"**Year:** {edu['year']}")
                                if edu.get("location"):
                                    st.markdown(f"**Location:** {edu['location']}")

                    # Skills
                    if resume_data.get("skills"):
                        st.subheader("🛠️ Skills")
                        skills = resume_data["skills"]
                        col1, col2 = st.columns(2)
                        with col1:
                            if skills.get("technical"):
                                st.markdown("**Technical Skills:**")
                                st.markdown(", ".join(skills["technical"]))
                        with col2:
                            if skills.get("soft"):
                                st.markdown("**Soft Skills:**")
                                st.markdown(", ".join(skills["soft"]))

                    # Certifications
                    if resume_data.get("certifications"):
                        st.subheader("🏆 Certifications")
                        for cert in resume_data["certifications"]:
                            cert_text = cert["name"]
                            if cert.get("issuer"):
                                cert_text += f" - {cert['issuer']}"
                            if cert.get("date"):
                                cert_text += f" ({cert['date']})"
                            st.markdown(f"- {cert_text}")

                    # Download JSON
                    st.divider()
                    st.download_button(
                        label="📥 Download JSON",
                        data=json.dumps(data, indent=2),
                        file_name=f"resume_{data['document_id']}.json",
                        mime="application/json",
                    )

                else:
                    st.error(
                        f"❌ Error: {response.json().get('detail', 'Unknown error')}"
                    )

            except requests.exceptions.ConnectionError:
                st.error(
                    "❌ Cannot connect to API. Please ensure the FastAPI server is running at http://localhost:8000"
                )
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")

# Sidebar
with st.sidebar:
    st.header("ℹ️ About")
    st.markdown("""
    This AI-powered resume parser extracts structured information from resumes using Large Language Models (LLMs).

    **How to use:**
    1. Upload your resume
    2. Click "Parse Resume"
    3. View extracted data
    4. Download JSON if needed
    """)

    st.header("🔧 API Status")
    try:
        response = requests.get(f"{API_BASE_URL}/", timeout=2)
        if response.status_code == 200:
            st.success("✅ API Connected")
        else:
            st.error("❌ API Error")
    except Exception:
        st.error("❌ API Offline")
