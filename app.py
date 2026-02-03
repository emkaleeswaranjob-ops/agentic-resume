import streamlit as st
import os
import re
from dotenv import load_dotenv
from google import genai
from firecrawl import FirecrawlApp

# ----------------------------
# 1. Load environment variables
# ----------------------------
load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
FIRECRAWL_API_KEY = os.getenv("FIRECRAWL_API_KEY")

if not GOOGLE_API_KEY or not FIRECRAWL_API_KEY:
    st.error("❌ Missing API keys in .env")
    st.stop()

# ----------------------------
# 2. Initialize clients
# ----------------------------
genai_client = genai.Client(
    api_key=GOOGLE_API_KEY,
    http_options={"api_version": "v1"}
)

firecrawl = FirecrawlApp(api_key=FIRECRAWL_API_KEY)

# ----------------------------
# 3. Helper Functions
# ----------------------------
def extract_ats_score(text):
    match = re.search(r"ATS_SCORE:\s*(\d+)", text)
    return int(match.group(1)) if match else 0


def calculate_ats_score(resume, jd):
    prompt = f"""
You are an ATS system.

Return:
ATS_SCORE (0–100)
MISSING_KEYWORDS
3 SUGGESTIONS

FORMAT ONLY:

ATS_SCORE: <number>
MISSING_KEYWORDS: x, y, z
SUGGESTIONS:
- ...
- ...
- ...

RESUME:
{resume}

JOB DESCRIPTION:
{jd}
"""
    return genai_client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    ).text


def skill_gap_intelligence(resume, jd):
    prompt = f"""
You are a skill gap intelligence engine.

Compare resume vs job description.

Return ONLY this format:

MISSING_SKILLS:
- skill
- skill

WEAK_SKILLS:
- skill (reason)

STRONG_SKILLS:
- skill

RESUME:
{resume}

JOB DESCRIPTION:
{jd}
"""
    return genai_client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    ).text


def improve_resume(resume, jd, ats_feedback, skill_gap):
    prompt = f"""
Improve the resume to achieve ATS score above 90.

Use:
- ATS feedback
- Skill gaps

Rules:
- Do NOT hallucinate
- Strengthen weak skills
- Address missing skills carefully (only if plausible)
- Add metrics where possible

CURRENT RESUME:
{resume}

ATS FEEDBACK:
{ats_feedback}

SKILL GAP INTELLIGENCE:
{skill_gap}

JOB DESCRIPTION:
{jd}
"""
    return genai_client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    ).text


# ----------------------------
# 4. UI
# ----------------------------
st.set_page_config("Resume Agent", "🤖")
st.title("🤖 Agentic Resume Tailor + Skill Intelligence")

job_url = st.text_input("🔗 Job Link (optional)")
job_desc_manual = st.text_area("📋 Paste Job Description (optional)", height=250)

st.caption("💡 Provide either Job Link or Job Description")

# ----------------------------
# 5. State Init
# ----------------------------
for key in ["resume", "jd", "ats", "ats_score", "skill_gap"]:
    st.session_state.setdefault(key, None)

# ----------------------------
# 6. Tailor Resume
# ----------------------------
if st.button("🚀 Tailor My Resume"):

    if not os.path.exists("master_resume.txt"):
        st.error("❌ master_resume.txt not found")
        st.stop()

    with open("master_resume.txt", "r", encoding="utf-8") as f:
        resume = f.read()

    # JD resolution
    jd = ""
    if job_desc_manual.strip():
        jd = job_desc_manual
    elif job_url.strip():
        try:
            scraped = firecrawl.scrape_url(job_url)
            jd = scraped.get("markdown") or scraped.get("content", "")
            if not jd.strip():
                raise Exception()
        except Exception:
            st.error("❌ Auto extraction failed. Paste JD manually.")
            st.stop()
    else:
        st.error("❌ Provide Job Link or Job Description")
        st.stop()

    resume_prompt = f"""
Rewrite resume to match job description.
Use ATS-optimized bullets.
No hallucination.

RESUME:
{resume}

JOB DESCRIPTION:
{jd}
"""
    tailored = genai_client.models.generate_content(
        model="gemini-2.5-flash",
        contents=resume_prompt
    ).text

    ats = calculate_ats_score(tailored, jd)
    ats_score = extract_ats_score(ats)
    skill_gap = skill_gap_intelligence(tailored, jd)

    st.session_state.update({
        "resume": tailored,
        "jd": jd,
        "ats": ats,
        "ats_score": ats_score,
        "skill_gap": skill_gap
    })

# ----------------------------
# 7. Output
# ----------------------------
if st.session_state.resume:

    st.markdown("## 📄 Tailored Resume")
    st.markdown(st.session_state.resume)

    st.markdown("## 📊 ATS Result")
    st.markdown(st.session_state.ats)
    st.progress(st.session_state.ats_score / 100)

    st.markdown("## 🧠 Skill Gap Intelligence")
    st.markdown(st.session_state.skill_gap)

    # ----------------------------
    # 8. Improve Loop
    # ----------------------------
    if st.session_state.ats_score < 90:
        if st.button("🔁 Improve Resume to Reach ATS > 90"):
            improved = improve_resume(
                st.session_state.resume,
                st.session_state.jd,
                st.session_state.ats,
                st.session_state.skill_gap
            )

            new_ats = calculate_ats_score(improved, st.session_state.jd)
            new_score = extract_ats_score(new_ats)
            new_skill_gap = skill_gap_intelligence(improved, st.session_state.jd)

            st.session_state.update({
                "resume": improved,
                "ats": new_ats,
                "ats_score": new_score,
                "skill_gap": new_skill_gap
            })

            st.rerun()
    else:
        st.success("🎯 ATS Score ≥ 90 achieved!")
