# import streamlit as st
# import os
# from dotenv import load_dotenv
# from google import genai
# from firecrawl import FirecrawlApp

# # ----------------------------
# # 1. Load environment variables
# # ----------------------------
# load_dotenv()

# GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
# FIRECRAWL_API_KEY = os.getenv("FIRECRAWL_API_KEY")

# if not GOOGLE_API_KEY:
#     st.error("❌ Missing GOOGLE_API_KEY in .env")
#     st.stop()

# if not FIRECRAWL_API_KEY:
#     st.error("❌ Missing FIRECRAWL_API_KEY in .env")
#     st.stop()

# # ----------------------------
# # 2. Initialize clients
# # ----------------------------
# genai_client = genai.Client(
#     api_key=GOOGLE_API_KEY,
#     http_options={"api_version": "v1"}
# )

# firecrawl = FirecrawlApp(api_key=FIRECRAWL_API_KEY)

# # ----------------------------
# # 3. Streamlit UI
# # ----------------------------
# st.set_page_config(page_title="Resume Agent", page_icon="🤖")
# st.title("🤖 Your Agentic Resume Tailor")

# job_url = st.text_input("🔗 Paste a Job Link (LinkedIn supported via manual JD):")

# job_desc_manual = ""

# # ----------------------------
# # 4. Action
# # ----------------------------
# if st.button("🚀 Tailor My Resume"):

#     if not job_url:
#         st.warning("Please paste a job link first!")
#         st.stop()

#     with st.spinner("Tailoring your resume..."):

#         # ----------------------------
#         # Read resume
#         # ----------------------------
#         if not os.path.exists("master_resume.txt"):
#             st.error("❌ master_resume.txt file not found!")
#             st.stop()

#         with open("master_resume.txt", "r", encoding="utf-8") as f:
#             my_resume = f.read()

#         # ----------------------------
#         # Job Description Extraction
#         # ----------------------------
#         job_desc = ""

#         # LinkedIn & protected sites → manual fallback
#         if "linkedin.com" in job_url:
#             st.warning("⚠️ LinkedIn jobs cannot be scraped. Please paste the Job Description below.")
#             job_desc = st.text_area(
#                 "📋 Paste Job Description here:",
#                 height=300
#             )
#         else:
#             try:
#                 scraped = firecrawl.scrape_url(job_url)

#                 if isinstance(scraped, dict):
#                     job_desc = scraped.get("markdown") or scraped.get("content", "")
#                 else:
#                     job_desc = getattr(scraped, "markdown", "") or getattr(scraped, "content", "")

#             except Exception:
#                 st.warning(
#                     "⚠️ This website cannot be scraped automatically.\n\n"
#                     "Please copy-paste the Job Description below."
#                 )
#                 job_desc = st.text_area(
#                     "📋 Paste Job Description here:",
#                     height=300
#                 )
#                 if not st.button("✅ Generate Tailored Resume"):
#                     st.stop()

#         if not job_desc.strip():
#             st.error("❌ Job Description is required to proceed.")
#             st.stop()

#         # ----------------------------
#         # Prompt
#         # ----------------------------
#         prompt = f"""
# You are an expert resume writer and ATS optimization specialist.

# Rewrite the resume to strongly match the job description.

# Rules:
# - Use concise, impact-driven bullet points (XYZ or STAR format)
# - Optimize for ATS keywords
# - Preserve truth (DO NOT hallucinate experience)
# - Keep formatting clean and professional

# RESUME:
# {my_resume}

# JOB DESCRIPTION:
# {job_desc}
# """

#         # ----------------------------
#         # Gemini call (STABLE MODEL)
#         # ----------------------------
#         response = genai_client.models.generate_content(
#             model="gemini-2.5-flash",
#             contents=prompt
#         )

#         # ----------------------------
#         # Output
#         # ----------------------------
#         st.success("✅ Tailored Resume Ready!")
#         st.markdown("---")
#         st.markdown(response.text)

# import streamlit as st
# import os
# from dotenv import load_dotenv
# from google import genai
# from firecrawl import FirecrawlApp

# # ----------------------------
# # 1. Load environment variables
# # ----------------------------
# load_dotenv()

# GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
# FIRECRAWL_API_KEY = os.getenv("FIRECRAWL_API_KEY")

# if not GOOGLE_API_KEY:
#     st.error("❌ Missing GOOGLE_API_KEY in .env")
#     st.stop()

# if not FIRECRAWL_API_KEY:
#     st.error("❌ Missing FIRECRAWL_API_KEY in .env")
#     st.stop()

# # ----------------------------
# # 2. Initialize clients
# # ----------------------------
# genai_client = genai.Client(
#     api_key=GOOGLE_API_KEY,
#     http_options={"api_version": "v1"}
# )

# firecrawl = FirecrawlApp(api_key=FIRECRAWL_API_KEY)

# # ----------------------------
# # 3. ATS Score Function
# # ----------------------------
# def calculate_ats_score(resume_text, job_desc):
#     prompt = f"""
# You are an ATS (Applicant Tracking System).

# Analyze the resume against the job description and return:
# 1. ATS Match Score (0–100)
# 2. Missing important keywords
# 3. 3 improvement suggestions

# Respond ONLY in this format:

# ATS_SCORE: <number>
# MISSING_KEYWORDS: keyword1, keyword2, keyword3
# SUGGESTIONS:
# - suggestion 1
# - suggestion 2
# - suggestion 3

# RESUME:
# {resume_text}

# JOB DESCRIPTION:
# {job_desc}
# """

#     response = genai_client.models.generate_content(
#         model="gemini-2.5-flash",
#         contents=prompt
#     )

#     return response.text

# # ----------------------------
# # 4. Streamlit UI
# # ----------------------------
# st.set_page_config(page_title="Resume Agent", page_icon="🤖")
# st.title("🤖 Your Agentic Resume Tailor")

# job_url = st.text_input("🔗 Paste Job Link (LinkedIn supported)")
# job_desc_manual = st.text_area(
#     "📋 If LinkedIn or scraping fails, paste Job Description here (optional)",
#     height=250
# )

# # ----------------------------
# # 5. Action
# # ----------------------------
# if st.button("🚀 Tailor My Resume"):

#     with st.spinner("Tailoring your resume..."):

#         # Read resume
#         if not os.path.exists("master_resume.txt"):
#             st.error("❌ master_resume.txt file not found!")
#             st.stop()

#         with open("master_resume.txt", "r", encoding="utf-8") as f:
#             my_resume = f.read()

#         # ----------------------------
#         # Job Description Resolution
#         # ----------------------------
#         job_desc = ""

#         if job_desc_manual.strip():
#             job_desc = job_desc_manual
#         elif job_url:
#             try:
#                 scraped = firecrawl.scrape_url(job_url)

#                 if isinstance(scraped, dict):
#                     job_desc = scraped.get("markdown") or scraped.get("content", "")
#                 else:
#                     job_desc = getattr(scraped, "markdown", "") or getattr(scraped, "content", "")

#             except Exception:
#                 st.error(
#                     "❌ Failed to scrape job link.\n\n"
#                     "Please paste the Job Description manually."
#                 )
#                 st.stop()
#         else:
#             st.error("❌ Please provide a Job Link or paste Job Description.")
#             st.stop()

#         if not job_desc.strip():
#             st.error("❌ Job Description is required.")
#             st.stop()

#         # ----------------------------
#         # Resume Tailoring Prompt
#         # ----------------------------
#         resume_prompt = f"""
# You are an expert resume writer and ATS optimization specialist.

# Rewrite the resume to strongly match the job description.

# Rules:
# - Use concise, impact-driven bullet points (XYZ or STAR)
# - Optimize for ATS keywords
# - Preserve truth (DO NOT hallucinate experience)
# - Keep formatting clean and professional

# RESUME:
# {my_resume}

# JOB DESCRIPTION:
# {job_desc}
# """

#         resume_response = genai_client.models.generate_content(
#             model="gemini-2.5-flash",
#             contents=resume_prompt
#         )

#         tailored_resume = resume_response.text

#         # ----------------------------
#         # Output: Resume
#         # ----------------------------
#         st.success("✅ Tailored Resume Ready!")
#         st.markdown("## 📄 Tailored Resume")
#         st.markdown(tailored_resume)

#         # ----------------------------
#         # Output: ATS Score
#         # ----------------------------
#         st.markdown("---")
#         st.markdown("## 📊 ATS Match Score")

#         ats_result = calculate_ats_score(tailored_resume, job_desc)
#         st.markdown(ats_result)

# import streamlit as st
# import os
# from dotenv import load_dotenv
# from google import genai
# from firecrawl import FirecrawlApp

# # ----------------------------
# # 1. Load environment variables
# # ----------------------------
# load_dotenv()

# GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
# FIRECRAWL_API_KEY = os.getenv("FIRECRAWL_API_KEY")

# if not GOOGLE_API_KEY:
#     st.error("❌ Missing GOOGLE_API_KEY in .env")
#     st.stop()

# if not FIRECRAWL_API_KEY:
#     st.error("❌ Missing FIRECRAWL_API_KEY in .env")
#     st.stop()

# # ----------------------------
# # 2. Initialize clients
# # ----------------------------
# genai_client = genai.Client(
#     api_key=GOOGLE_API_KEY,
#     http_options={"api_version": "v1"}
# )

# firecrawl = FirecrawlApp(api_key=FIRECRAWL_API_KEY)

# # ----------------------------
# # 3. ATS Score Function
# # ----------------------------
# def calculate_ats_score(resume_text, job_desc):
#     prompt = f"""
# You are an ATS (Applicant Tracking System).

# Analyze the resume against the job description and return:
# 1. ATS Match Score (0–100)
# 2. Missing important keywords
# 3. 3 improvement suggestions

# Respond ONLY in this format:

# ATS_SCORE: <number>
# MISSING_KEYWORDS: keyword1, keyword2, keyword3
# SUGGESTIONS:
# - suggestion 1
# - suggestion 2
# - suggestion 3

# RESUME:
# {resume_text}

# JOB DESCRIPTION:
# {job_desc}
# """

#     response = genai_client.models.generate_content(
#         model="gemini-2.5-flash",
#         contents=prompt
#     )

#     return response.text

# ----------------------------
# 4. Streamlit UI
# ----------------------------
# st.set_page_config(page_title="Resume Agent", page_icon="🤖")
# st.title("🤖 Your Agentic Resume Tailor")

# job_url = st.text_input("🔗 Paste Job Link")
# job_desc_manual = st.text_area(
#     "📋 Paste Job Description here (only if auto-extraction fails)",
#     height=250
# )

# st.caption("💡 The app will automatically extract the Job Description when possible.")

# # ----------------------------
# # 5. Action
# # ----------------------------
# if st.button("🚀 Tailor My Resume"):

#     with st.spinner("Tailoring your resume..."):

#         # ----------------------------
#         # Read Resume
#         # ----------------------------
#         if not os.path.exists("master_resume.txt"):
#             st.error("❌ master_resume.txt file not found!")
#             st.stop()

#         with open("master_resume.txt", "r", encoding="utf-8") as f:
#             my_resume = f.read()

#         # ----------------------------
#         # Job Description Resolution (FINAL LOGIC)
#         # ----------------------------
#         job_desc = ""

#         if job_url:
#             try:
#                 scraped = firecrawl.scrape_url(job_url)

#                 if isinstance(scraped, dict):
#                     job_desc = scraped.get("markdown") or scraped.get("content", "")
#                 else:
#                     job_desc = getattr(scraped, "markdown", "") or getattr(scraped, "content", "")

#                 if not job_desc.strip():
#                     raise Exception("Empty scrape result")

#             except Exception:
#                 if not job_desc_manual.strip():
#                     st.error(
#                         "❌ Unable to extract Job Description automatically.\n\n"
#                         "Please paste the Job Description manually."
#                     )
#                     st.stop()

#                 job_desc = job_desc_manual

#         else:
#             st.error("❌ Please provide a Job Link.")
#             st.stop()

#         # ----------------------------
#         # Resume Tailoring Prompt
#         # ----------------------------
#         resume_prompt = f"""
# You are an expert resume writer and ATS optimization specialist.

# Rewrite the resume to strongly match the job description.

# Rules:
# - Use concise, impact-driven bullet points (XYZ or STAR)
# - Optimize for ATS keywords
# - Preserve truth (DO NOT hallucinate experience)
# - Keep formatting clean and professional

# RESUME:
# {my_resume}

# JOB DESCRIPTION:
# {job_desc}
# """

#         resume_response = genai_client.models.generate_content(
#             model="gemini-2.5-flash",
#             contents=resume_prompt
#         )

#         tailored_resume = resume_response.text

#         # ----------------------------
#         # Output: Resume
#         # ----------------------------
#         st.success("✅ Tailored Resume Ready!")
#         st.markdown("## 📄 Tailored Resume")
#         st.markdown(tailored_resume)

#         # ----------------------------
#         # Output: ATS Score
#         # ----------------------------
#         st.markdown("---")
#         st.markdown("## 📊 ATS Match Score")

#         ats_result = calculate_ats_score(tailored_resume, job_desc)
#         st.markdown(ats_result)


# import streamlit as st
# import os
# from dotenv import load_dotenv
# from google import genai
# from firecrawl import FirecrawlApp

# # ----------------------------
# # 1. Load environment variables
# # ----------------------------
# load_dotenv()

# GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
# FIRECRAWL_API_KEY = os.getenv("FIRECRAWL_API_KEY")

# if not GOOGLE_API_KEY:
#     st.error("❌ Missing GOOGLE_API_KEY in .env")
#     st.stop()

# if not FIRECRAWL_API_KEY:
#     st.error("❌ Missing FIRECRAWL_API_KEY in .env")
#     st.stop()

# # ----------------------------
# # 2. Initialize clients
# # ----------------------------
# genai_client = genai.Client(
#     api_key=GOOGLE_API_KEY,
#     http_options={"api_version": "v1"}
# )

# firecrawl = FirecrawlApp(api_key=FIRECRAWL_API_KEY)

# # ----------------------------
# # 3. ATS Score Function
# # ----------------------------
# def calculate_ats_score(resume_text, job_desc):
#     prompt = f"""
# You are an ATS (Applicant Tracking System).

# Analyze the resume against the job description and return:
# 1. ATS Match Score (0–100)
# 2. Missing important keywords
# 3. 3 improvement suggestions

# Respond ONLY in this format:

# ATS_SCORE: <number>
# MISSING_KEYWORDS: keyword1, keyword2, keyword3
# SUGGESTIONS:
# - suggestion 1
# - suggestion 2
# - suggestion 3

# RESUME:
# {resume_text}

# JOB DESCRIPTION:
# {job_desc}
# """

#     response = genai_client.models.generate_content(
#         model="gemini-2.5-flash",
#         contents=prompt
#     )

#     return response.text

# # ----------------------------
# # 4. Streamlit UI
# # ----------------------------
# st.set_page_config(page_title="Resume Agent", page_icon="🤖")
# st.title("🤖 Your Agentic Resume Tailor")

# job_url = st.text_input("🔗 Paste Job Link (optional)")
# job_desc_manual = st.text_area(
#     "📋 Paste Job Description here (optional)",
#     height=250
# )

# st.caption("💡 You can paste either a Job Link OR the Job Description.")

# # ----------------------------
# # 5. Action
# # ----------------------------
# if st.button("🚀 Tailor My Resume"):

#     with st.spinner("Tailoring your resume..."):

#         # ----------------------------
#         # Read Resume
#         # ----------------------------
#         if not os.path.exists("master_resume.txt"):
#             st.error("❌ master_resume.txt file not found!")
#             st.stop()

#         with open("master_resume.txt", "r", encoding="utf-8") as f:
#             my_resume = f.read()

#         # ----------------------------
#         # Job Description Resolution (FINAL FIXED FLOW)
#         # ----------------------------
#         job_desc = ""

#         # 1️⃣ Manual JD takes full priority
#         if job_desc_manual.strip():
#             job_desc = job_desc_manual

#         # 2️⃣ Else try scraping if link is provided
#         elif job_url.strip():
#             try:
#                 scraped = firecrawl.scrape_url(job_url)

#                 if isinstance(scraped, dict):
#                     job_desc = scraped.get("markdown") or scraped.get("content", "")
#                 else:
#                     job_desc = getattr(scraped, "markdown", "") or getattr(scraped, "content", "")

#                 if not job_desc.strip():
#                     raise Exception("Empty scrape result")

#             except Exception:
#                 st.error(
#                     "❌ Unable to auto-extract Job Description.\n\n"
#                     "Please paste the Job Description manually and click again."
#                 )
#                 st.stop()

#         # 3️⃣ Neither provided
#         else:
#             st.error("❌ Please paste a Job Link or Job Description.")
#             st.stop()

#         # ----------------------------
#         # Resume Tailoring Prompt
#         # ----------------------------
#         resume_prompt = f"""
# You are an expert resume writer and ATS optimization specialist.

# Rewrite the resume to strongly match the job description.

# Rules:
# - Use concise, impact-driven bullet points (XYZ or STAR)
# - Optimize for ATS keywords
# - Preserve truth (DO NOT hallucinate experience)
# - Keep formatting clean and professional

# RESUME:
# {my_resume}

# JOB DESCRIPTION:
# {job_desc}
# """

#         resume_response = genai_client.models.generate_content(
#             model="gemini-2.5-flash",
#             contents=resume_prompt
#         )

#         tailored_resume = resume_response.text

#         # ----------------------------
#         # Output: Resume
#         # ----------------------------
#         st.success("✅ Tailored Resume Ready!")
#         st.markdown("## 📄 Tailored Resume")
#         st.markdown(tailored_resume)

#         # ----------------------------
#         # Output: ATS Score
#         # ----------------------------
#         st.markdown("---")
#         st.markdown("## 📊 ATS Match Score")

#         ats_result = calculate_ats_score(tailored_resume, job_desc)
#         st.markdown(ats_result)

# import streamlit as st
# import os
# from dotenv import load_dotenv
# from google import genai
# from firecrawl import FirecrawlApp

# # ----------------------------
# # 1. Load environment variables
# # ----------------------------
# load_dotenv()

# GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
# FIRECRAWL_API_KEY = os.getenv("FIRECRAWL_API_KEY")

# if not GOOGLE_API_KEY:
#     st.error("❌ Missing GOOGLE_API_KEY in .env")
#     st.stop()

# if not FIRECRAWL_API_KEY:
#     st.error("❌ Missing FIRECRAWL_API_KEY in .env")
#     st.stop()

# # ----------------------------
# # 2. Initialize clients
# # ----------------------------
# genai_client = genai.Client(
#     api_key=GOOGLE_API_KEY,
#     http_options={"api_version": "v1"}
# )

# firecrawl = FirecrawlApp(api_key=FIRECRAWL_API_KEY)

# # ----------------------------
# # 3. ATS Score Function
# # ----------------------------
# def calculate_ats_score(resume_text, job_desc):
#     prompt = f"""
# You are an ATS (Applicant Tracking System).

# Analyze the resume against the job description and return:
# 1. ATS Match Score (0–100)
# 2. Missing important keywords
# 3. 3 improvement suggestions

# Respond ONLY in this format:

# ATS_SCORE: <number>
# MISSING_KEYWORDS: keyword1, keyword2, keyword3
# SUGGESTIONS:
# - suggestion 1
# - suggestion 2
# - suggestion 3

# RESUME:
# {resume_text}

# JOB DESCRIPTION:
# {job_desc}
# """

#     response = genai_client.models.generate_content(
#         model="gemini-2.5-flash",
#         contents=prompt
#     )

#     return response.text


# def extract_ats_score(ats_text):
#     for line in ats_text.splitlines():
#         if line.startswith("ATS_SCORE"):
#             return int(line.split(":")[1].strip())
#     return 0


# # ----------------------------
# # 4. Improve Resume Function
# # ----------------------------
# def improve_resume_to_90(resume_text, job_desc, ats_feedback):
#     prompt = f"""
# You are an elite ATS optimization expert.

# Goal:
# Improve the resume so that it achieves an ATS score ABOVE 90.

# Rules:
# - Fix missing keywords
# - Improve bullet strength
# - Align more closely to JD
# - DO NOT add fake experience
# - Keep content truthful and concise

# CURRENT RESUME:
# {resume_text}

# ATS FEEDBACK:
# {ats_feedback}

# JOB DESCRIPTION:
# {job_desc}

# Return ONLY the improved resume.
# """

#     response = genai_client.models.generate_content(
#         model="gemini-2.5-flash",
#         contents=prompt
#     )

#     return response.text


# # ----------------------------
# # 5. Streamlit UI
# # ----------------------------
# st.set_page_config(page_title="Resume Agent", page_icon="🤖")
# st.title("🤖 Your Agentic Resume Tailor")

# job_url = st.text_input("🔗 Paste Job Link ")
# job_desc_manual = st.text_area(
#     "📋 Paste Job Description here (if Job Link don't work)",
#     height=250
# )

# st.caption("💡 Paste the Job Description")

# # ----------------------------
# # 6. Action Button
# # ----------------------------
# if st.button("🚀 Tailor My Resume"):

#     with st.spinner("Tailoring your resume..."):

#         # ----------------------------
#         # Read Resume
#         # ----------------------------
#         if not os.path.exists("master_resume.txt"):
#             st.error("❌ master_resume.txt not found")
#             st.stop()

#         with open("master_resume.txt", "r", encoding="utf-8") as f:
#             my_resume = f.read()

#         # ----------------------------
#         # Job Description Resolution
#         # ----------------------------
#         job_desc = ""

#         # Priority 1: Manual JD
#         if job_desc_manual.strip():
#             job_desc = job_desc_manual.strip()

#         # Priority 2: Scrape link
#         elif job_url.strip():
#             try:
#                 scraped = firecrawl.scrape_url(job_url)

#                 if isinstance(scraped, dict):
#                     job_desc = scraped.get("markdown") or scraped.get("content", "")
#                 else:
#                     job_desc = getattr(scraped, "markdown", "") or getattr(scraped, "content", "")

#                 if not job_desc.strip():
#                     raise Exception("Empty scrape")

#             except Exception:
#                 st.error(
#                     "❌ Could not extract Job Description from link.\n\n"
#                     "Please paste the Job Description manually."
#                 )
#                 st.stop()

#         # Neither provided
#         else:
#             st.error("❌ Please paste a Job Link or Job Description")
#             st.stop()

#         # ----------------------------
#         # Resume Tailoring
#         # ----------------------------
#         resume_prompt = f"""
# You are an expert resume writer and ATS optimization specialist.

# Rewrite the resume to strongly match the job description.

# Rules:
# - Use impact-driven bullet points
# - Optimize for ATS keywords
# - Preserve truth (no hallucination)
# - Keep formatting professional

# RESUME:
# {my_resume}

# JOB DESCRIPTION:
# {job_desc}
# """

#         resume_response = genai_client.models.generate_content(
#             model="gemini-2.5-flash",
#             contents=resume_prompt
#         )

#         tailored_resume = resume_response.text

#         # ----------------------------
#         # Output: Tailored Resume
#         # ----------------------------
#         st.success("✅ Tailored Resume Ready!")
#         st.markdown("## 📄 Tailored Resume")
#         st.markdown(tailored_resume)

#         # ----------------------------
#         # ATS Score
#         # ----------------------------
#         st.markdown("---")
#         st.markdown("## 📊 ATS Match Score")

#         ats_result = calculate_ats_score(tailored_resume, job_desc)
#         st.markdown(ats_result)

#         ats_score = extract_ats_score(ats_result)

#         # ----------------------------
#         # Improve Resume Button
#         # ----------------------------
#         if ats_score < 90:
#             st.warning(f"⚠️ ATS Score is {ats_score}. Improve to 90+?")

#             if st.button("🚀 Improve Resume to 90+ ATS"):
#                 with st.spinner("Improving resume..."):

#                     improved_resume = improve_resume_to_90(
#                         tailored_resume,
#                         job_desc,
#                         ats_result
#                     )

#                     st.markdown("---")
#                     st.success("🔥 Improved Resume")
#                     st.markdown("## 📄 Improved Resume")
#                     st.markdown(improved_resume)

#                     st.markdown("---")
#                     st.markdown("## 📊 Updated ATS Score")
#                     improved_ats = calculate_ats_score(improved_resume, job_desc)
#                     st.markdown(improved_ats)

#         else:
#             st.success("🎉 ATS Score already 90+ — excellent match!")

# import streamlit as st
# import os
# import re
# from dotenv import load_dotenv
# from google import genai
# from firecrawl import FirecrawlApp

# # ----------------------------
# # 1. Load environment variables
# # ----------------------------
# load_dotenv()

# GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
# FIRECRAWL_API_KEY = os.getenv("FIRECRAWL_API_KEY")

# if not GOOGLE_API_KEY:
#     st.error("❌ Missing GOOGLE_API_KEY in .env")
#     st.stop()

# if not FIRECRAWL_API_KEY:
#     st.error("❌ Missing FIRECRAWL_API_KEY in .env")
#     st.stop()

# ----------------------------
# 2. Initialize clients
# ----------------------------
# genai_client = genai.Client(
#     api_key=GOOGLE_API_KEY,
#     http_options={"api_version": "v1"}
# )

# firecrawl = FirecrawlApp(api_key=FIRECRAWL_API_KEY)

# # ----------------------------
# # 3. Session State Init
# # ----------------------------
# for key in [
#     "tailored_resume",
#     "ats_score",
#     "ats_feedback",
#     "job_desc"
# ]:
#     if key not in st.session_state:
#         st.session_state[key] = None

# # ----------------------------
# # 4. ATS Score Function
# # ----------------------------
# def calculate_ats_score(resume_text, job_desc):
#     prompt = f"""
# You are an ATS (Applicant Tracking System).

# Analyze the resume against the job description and return:
# 1. ATS Match Score (0–100)
# 2. Missing important keywords
# 3. 3 improvement suggestions

# Respond ONLY in this format:

# ATS_SCORE: <number>
# MISSING_KEYWORDS: keyword1, keyword2, keyword3
# SUGGESTIONS:
# - suggestion 1
# - suggestion 2
# - suggestion 3

# RESUME:
# {resume_text}

# JOB DESCRIPTION:
# {job_desc}
# """

#     response = genai_client.models.generate_content(
#         model="gemini-2.5-flash",
#         contents=prompt
#     )

#     text = response.text
#     match = re.search(r"ATS_SCORE:\s*(\d+)", text)
#     score = int(match.group(1)) if match else 0

#     return score, text

# # ----------------------------
# # 5. Streamlit UI
# # ----------------------------
# st.set_page_config(page_title="Resume Agent", page_icon="🤖")
# st.title("🤖 Your Agentic Resume Tailor")

# job_url = st.text_input("🔗 Paste Job Link (optional)")
# job_desc_manual = st.text_area(
#     "📋 Paste Job Description here (optional)",
#     height=250
# )

# st.caption("💡 Paste **either** Job Link **or** Job Description")

# # ----------------------------
# # 6. Tailor Resume
# # ----------------------------
# if st.button("🚀 Tailor My Resume"):

#     with st.spinner("Tailoring your resume..."):

#         if not os.path.exists("master_resume.txt"):
#             st.error("❌ master_resume.txt file not found!")
#             st.stop()

#         with open("master_resume.txt", "r", encoding="utf-8") as f:
#             base_resume = f.read()

#         # -------- Job Description Resolution --------
#         job_desc = ""

#         if job_desc_manual.strip():
#             job_desc = job_desc_manual

#         elif job_url.strip():
#             try:
#                 scraped = firecrawl.scrape_url(job_url)

#                 if isinstance(scraped, dict):
#                     job_desc = scraped.get("markdown") or scraped.get("content", "")
#                 else:
#                     job_desc = getattr(scraped, "markdown", "") or getattr(scraped, "content", "")

#                 if not job_desc.strip():
#                     raise Exception("Empty JD")

#             except Exception:
#                 st.error("❌ Auto-extraction failed. Please paste Job Description manually.")
#                 st.stop()
#         else:
#             st.error("❌ Please provide a Job Link or Job Description.")
#             st.stop()

#         st.session_state.job_desc = job_desc

#         # -------- Resume Tailoring --------
#         resume_prompt = f"""
# You are an expert resume writer and ATS optimization specialist.

# Rewrite the resume to strongly match the job description.

# Rules:
# - Use concise, impact-driven bullet points (XYZ / STAR)
# - Optimize for ATS keywords
# - Preserve truth (NO hallucination)
# - Keep formatting clean and professional

# RESUME:
# {base_resume}

# JOB DESCRIPTION:
# {job_desc}
# """

#         resume_response = genai_client.models.generate_content(
#             model="gemini-2.5-flash",
#             contents=resume_prompt
#         )

#         st.session_state.tailored_resume = resume_response.text

#         # -------- ATS Evaluation --------
#         score, feedback = calculate_ats_score(
#             st.session_state.tailored_resume,
#             job_desc
#         )

#         st.session_state.ats_score = score
#         st.session_state.ats_feedback = feedback

# # ----------------------------
# # 7. Display Results
# # ----------------------------
# if st.session_state.tailored_resume:

#     st.success("✅ Tailored Resume Ready")
#     st.markdown("## 📄 Tailored Resume")
#     st.markdown(st.session_state.tailored_resume)

#     st.markdown("---")
#     st.markdown("## 📊 ATS Match Score")

#     st.progress(min(st.session_state.ats_score / 100, 1.0))
#     st.markdown(f"### 🎯 ATS Score: **{st.session_state.ats_score}/100**")
#     st.markdown(st.session_state.ats_feedback)

# # ----------------------------
# # 8. Improve Resume Loop (ATS < 90)
# # ----------------------------
# if st.session_state.ats_score and st.session_state.ats_score < 90:

#     if st.button("🔥 Improve Resume to Reach ATS > 90"):

#         with st.spinner("Improving resume for higher ATS score..."):

#             improve_prompt = f"""
# You are an ATS optimization expert.

# Improve the resume to achieve an ATS score above 90.

# Rules:
# - Use ATS feedback strictly
# - Improve keyword density and phrasing
# - Do NOT add fake experience
# - Keep formatting ATS-friendly

# CURRENT RESUME:
# {st.session_state.tailored_resume}

# ATS FEEDBACK:
# {st.session_state.ats_feedback}

# JOB DESCRIPTION:
# {st.session_state.job_desc}
# """

#             improved_response = genai_client.models.generate_content(
#                 model="gemini-2.5-flash",
#                 contents=improve_prompt
#             )

#             st.session_state.tailored_resume = improved_response.text

#             score, feedback = calculate_ats_score(
#                 st.session_state.tailored_resume,
#                 st.session_state.job_desc
#             )

#             st.session_state.ats_score = score
#             st.session_state.ats_feedback = feedback

#             st.rerun()

# import streamlit as st
# import os
# import re
# from dotenv import load_dotenv
# from google import genai
# from firecrawl import FirecrawlApp

# # ----------------------------
# # 1. Load environment variables
# # ----------------------------
# load_dotenv()

# GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
# FIRECRAWL_API_KEY = os.getenv("FIRECRAWL_API_KEY")

# if not GOOGLE_API_KEY or not FIRECRAWL_API_KEY:
#     st.error("❌ Missing API keys in .env")
#     st.stop()

# # ----------------------------
# # 2. Initialize clients
# # ----------------------------
# genai_client = genai.Client(
#     api_key=GOOGLE_API_KEY,
#     http_options={"api_version": "v1"}
# )

# firecrawl = FirecrawlApp(api_key=FIRECRAWL_API_KEY)

# # ----------------------------
# # 3. Helper Functions
# # ----------------------------
# def extract_ats_score(text):
#     match = re.search(r"ATS_SCORE:\s*(\d+)", text)
#     return int(match.group(1)) if match else 0


# def calculate_ats_score(resume, jd):
#     prompt = f"""
# You are an ATS system.

# Return:
# ATS_SCORE (0–100)
# MISSING_KEYWORDS
# 3 SUGGESTIONS

# FORMAT ONLY:

# ATS_SCORE: <number>
# MISSING_KEYWORDS: x, y, z
# SUGGESTIONS:
# - ...
# - ...
# - ...

# RESUME:
# {resume}

# JOB DESCRIPTION:
# {jd}
# """
#     return genai_client.models.generate_content(
#         model="gemini-2.5-flash",
#         contents=prompt
#     ).text


# def skill_gap_intelligence(resume, jd):
#     prompt = f"""
# You are a skill gap intelligence engine.

# Compare resume vs job description.

# Return ONLY this format:

# MISSING_SKILLS:
# - skill
# - skill

# WEAK_SKILLS:
# - skill (reason)

# STRONG_SKILLS:
# - skill

# RESUME:
# {resume}

# JOB DESCRIPTION:
# {jd}
# """
#     return genai_client.models.generate_content(
#         model="gemini-2.5-flash",
#         contents=prompt
#     ).text


# def improve_resume(resume, jd, ats_feedback, skill_gap):
#     prompt = f"""
# Improve the resume to achieve ATS score above 90.

# Use:
# - ATS feedback
# - Skill gaps

# Rules:
# - Do NOT hallucinate
# - Strengthen weak skills
# - Address missing skills carefully (only if plausible)
# - Add metrics where possible

# CURRENT RESUME:
# {resume}

# ATS FEEDBACK:
# {ats_feedback}

# SKILL GAP INTELLIGENCE:
# {skill_gap}

# JOB DESCRIPTION:
# {jd}
# """
#     return genai_client.models.generate_content(
#         model="gemini-2.5-flash",
#         contents=prompt
#     ).text


# # ----------------------------
# # 4. UI
# # ----------------------------
# st.set_page_config("Resume Agent", "🤖")
# st.title("🤖 Agentic Resume Tailor + Skill Intelligence")

# job_url = st.text_input("🔗 Job Link (optional)")
# job_desc_manual = st.text_area("📋 Paste Job Description (optional)", height=250)

# st.caption("💡 Provide either Job Link or Job Description")

# # ----------------------------
# # 5. State Init
# # ----------------------------
# for key in ["resume", "jd", "ats", "ats_score", "skill_gap"]:
#     st.session_state.setdefault(key, None)

# # ----------------------------
# # 6. Tailor Resume
# # ----------------------------
# if st.button("🚀 Tailor My Resume"):

#     if not os.path.exists("master_resume.txt"):
#         st.error("❌ master_resume.txt not found")
#         st.stop()

#     with open("master_resume.txt", "r", encoding="utf-8") as f:
#         resume = f.read()

#     # JD resolution
#     jd = ""
#     if job_desc_manual.strip():
#         jd = job_desc_manual
#     elif job_url.strip():
#         try:
#             scraped = firecrawl.scrape_url(job_url)
#             jd = scraped.get("markdown") or scraped.get("content", "")
#             if not jd.strip():
#                 raise Exception()
#         except Exception:
#             st.error("❌ Auto extraction failed. Paste JD manually.")
#             st.stop()
#     else:
#         st.error("❌ Provide Job Link or Job Description")
#         st.stop()

#     resume_prompt = f"""
# Rewrite resume to match job description.
# Use ATS-optimized bullets.
# No hallucination.

# RESUME:
# {resume}

# JOB DESCRIPTION:
# {jd}
# """
#     tailored = genai_client.models.generate_content(
#         model="gemini-2.5-flash",
#         contents=resume_prompt
#     ).text

#     ats = calculate_ats_score(tailored, jd)
#     ats_score = extract_ats_score(ats)
#     skill_gap = skill_gap_intelligence(tailored, jd)

#     st.session_state.update({
#         "resume": tailored,
#         "jd": jd,
#         "ats": ats,
#         "ats_score": ats_score,
#         "skill_gap": skill_gap
#     })

# # ----------------------------
# # 7. Output
# # ----------------------------
# if st.session_state.resume:

#     st.markdown("## 📄 Tailored Resume")
#     st.markdown(st.session_state.resume)

#     st.markdown("## 📊 ATS Result")
#     st.markdown(st.session_state.ats)
#     st.progress(st.session_state.ats_score / 100)

#     st.markdown("## 🧠 Skill Gap Intelligence")
#     st.markdown(st.session_state.skill_gap)

#     # ----------------------------
#     # 8. Improve Loop
#     # ----------------------------
#     if st.session_state.ats_score < 90:
#         if st.button("🔁 Improve Resume to Reach ATS > 90"):
#             improved = improve_resume(
#                 st.session_state.resume,
#                 st.session_state.jd,
#                 st.session_state.ats,
#                 st.session_state.skill_gap
#             )

#             new_ats = calculate_ats_score(improved, st.session_state.jd)
#             new_score = extract_ats_score(new_ats)
#             new_skill_gap = skill_gap_intelligence(improved, st.session_state.jd)

#             st.session_state.update({
#                 "resume": improved,
#                 "ats": new_ats,
#                 "ats_score": new_score,
#                 "skill_gap": new_skill_gap
#             })

#             st.rerun()
#     else:
#         st.success("🎯 ATS Score ≥ 90 achieved!")
# import streamlit as st
# import os
# import re
# from dotenv import load_dotenv
# from google import genai
# from firecrawl import FirecrawlApp

# # ============================
# # Load ENV
# # ============================
# load_dotenv()

# GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
# FIRECRAWL_API_KEY = os.getenv("FIRECRAWL_API_KEY")

# if not GOOGLE_API_KEY or not FIRECRAWL_API_KEY:
#     st.error("Missing API keys in .env")
#     st.stop()

# # ============================
# # Clients
# # ============================
# genai_client = genai.Client(api_key=GOOGLE_API_KEY)
# firecrawl = FirecrawlApp(api_key=FIRECRAWL_API_KEY)

# # ============================
# # Helpers
# # ============================
# def extract_ats_score(text):
#     match = re.search(r"ATS_SCORE:\s*(\d+)", text)
#     return int(match.group(1)) if match else 0

# def gemini(prompt):
#     return genai_client.models.generate_content(
#         model="gemini-2.5-flash",
#         contents=prompt
#     ).text

# # ============================
# # Page
# # ============================
# st.set_page_config("Agentic Resume Tailor", "🤖")
# st.title("🤖 Agentic Resume Tailor")

# job_url = st.text_input("Job URL (optional)")
# job_desc = st.text_area("Paste Job Description", height=250)

# # ============================
# # Session State
# # ============================
# defaults = {
#     "has_run": False,
#     "resume": "",
#     "ats": "",
#     "ats_score": 0,
#     "skill_gap": "",
#     "jd": ""
# }

# for k, v in defaults.items():
#     if k not in st.session_state:
#         st.session_state[k] = v

# # ============================
# # Button (ONLY sets state)
# # ============================
# if st.button("🚀 Tailor My Resume"):
#     st.session_state.has_run = True

# # ============================
# # Main Logic (runs ONCE)
# # ============================
# if st.session_state.has_run and not st.session_state.resume:

#     with st.spinner("Analyzing job & tailoring resume..."):

#         if not os.path.exists("master_resume.txt"):
#             st.error("master_resume.txt not found")
#             st.stop()

#         with open("master_resume.txt", "r", encoding="utf-8") as f:
#             master_resume = f.read()

#         # Resolve JD
#         if job_desc.strip():
#             jd = job_desc
#         elif job_url.strip():
#             scraped = firecrawl.scrape_url(job_url)
#             jd = scraped.get("markdown", "")
#         else:
#             st.error("Provide JD or URL")
#             st.stop()

#         st.session_state.jd = jd

#         # Tailor resume
#         tailored_resume = gemini(f"""
# Rewrite resume for ATS.
# No hallucination.

# RESUME:
# {master_resume}

# JOB DESCRIPTION:
# {jd}
# """)

#         ats = gemini(f"""
# ATS_SCORE: <number>
# MISSING_KEYWORDS:
# SUGGESTIONS:

# RESUME:
# {tailored_resume}

# JOB DESCRIPTION:
# {jd}
# """)

#         skill_gap = gemini(f"""
# MISSING_SKILLS:
# WEAK_SKILLS:
# STRONG_SKILLS:

# RESUME:
# {tailored_resume}

# JOB DESCRIPTION:
# {jd}
# """)

#         st.session_state.resume = tailored_resume
#         st.session_state.ats = ats
#         st.session_state.ats_score = extract_ats_score(ats)
#         st.session_state.skill_gap = skill_gap

# # ============================
# # Render (ALWAYS SAFE)
# # ============================
# if st.session_state.resume:

#     st.subheader("📄 Tailored Resume")
#     st.markdown(st.session_state.resume)

#     st.subheader("📊 ATS Score")
#     st.markdown(st.session_state.ats)
#     st.progress(st.session_state.ats_score / 100)

#     st.subheader("🧠 Skill Gap Intelligence")
#     st.markdown(st.session_state.skill_gap)

#     if st.session_state.ats_score < 90:
#         if st.button("🔁 Improve Resume"):
#             improved = gemini(f"""
# Improve resume to reach ATS > 90.

# RESUME:
# {st.session_state.resume}

# JOB DESCRIPTION:
# {st.session_state.jd}
# """)
#             st.session_state.resume = improved
#             st.session_state.ats = gemini(improved)
#             st.session_state.ats_score = extract_ats_score(st.session_state.ats)
#             st.session_state.skill_gap = gemini(improved)
# import streamlit as st
# import os
# import re
# from dotenv import load_dotenv
# from google import genai
# from firecrawl import FirecrawlApp

# # ----------------------------
# # 1. ENV SETUP
# # ----------------------------
# load_dotenv()

# GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
# FIRECRAWL_API_KEY = os.getenv("FIRECRAWL_API_KEY")

# if not GOOGLE_API_KEY or not FIRECRAWL_API_KEY:
#     st.error("❌ Missing API keys in .env")
#     st.stop()

# # ----------------------------
# # 2. CLIENTS
# # ----------------------------
# genai_client = genai.Client(
#     api_key=GOOGLE_API_KEY,
#     http_options={"api_version": "v1"}
# )

# firecrawl = FirecrawlApp(api_key=FIRECRAWL_API_KEY)

# # ----------------------------
# # 3. HELPERS
# # ----------------------------
# def gemini(prompt):
#     return genai_client.models.generate_content(
#         model="gemini-2.5-flash",
#         contents=prompt
#     ).text.strip()

# def extract_ats_score(text):
#     match = re.search(r"ATS_SCORE:\s*(\d+)", text)
#     return int(match.group(1)) if match else 0

# def calculate_ats(resume, jd):
#     return gemini(f"""
# You are an ATS system.

# Return ONLY:

# ATS_SCORE: <0-100>
# MISSING_KEYWORDS: comma-separated
# SUGGESTIONS:
# - suggestion 1
# - suggestion 2
# - suggestion 3

# RESUME:
# {resume}

# JOB DESCRIPTION:
# {jd}
# """)

# # ----------------------------
# # 4. UI
# # ----------------------------
# st.set_page_config("Resume Agent", "🤖")
# st.title("🤖 Agentic Resume Tailor (ATS Optimized)")

# job_url = st.text_input("🔗 Job Link (optional)")
# job_desc_manual = st.text_area("📋 Paste Job Description (recommended)", height=250)

# st.caption("💡 Manual JD always takes priority")

# # ----------------------------
# # 5. STATE
# # ----------------------------
# if "resume" not in st.session_state:
#     st.session_state.resume = None
# if "ats" not in st.session_state:
#     st.session_state.ats = None
# if "score" not in st.session_state:
#     st.session_state.score = None
# if "jd" not in st.session_state:
#     st.session_state.jd = None

# # ----------------------------
# # 6. TAILOR BUTTON
# # ----------------------------
# if st.button("🚀 Tailor Resume"):

#     if not os.path.exists("master_resume.txt"):
#         st.error("❌ master_resume.txt not found")
#         st.stop()

#     with open("master_resume.txt", "r", encoding="utf-8") as f:
#         master_resume = f.read()

#     # Resolve JD
#     if job_desc_manual.strip():
#         jd = job_desc_manual.strip()
#     elif job_url.strip():
#         try:
#             scraped = firecrawl.scrape_url(job_url)
#             jd = scraped.get("markdown") or scraped.get("content", "")
#         except Exception:
#             st.error("❌ Scraping failed. Paste JD manually.")
#             st.stop()
#     else:
#         st.error("❌ Paste JD or provide link")
#         st.stop()

#     st.session_state.jd = jd

#     with st.spinner("Optimizing resume..."):
#         tailored = gemini(f"""
# You are an expert ATS resume writer.

# GOAL:
# Create a 1–2 PAGE resume (MAX 700 words).

# RULES:
# - Keep ONLY experience relevant to the job
# - Internally score bullets: High / Medium / Low relevance
# - Keep High, limited Medium, drop Low
# - Max 4–5 bullets per role
# - Compress older roles
# - Do NOT hallucinate
# - Preserve company, title, dates

# RESUME:
# {master_resume}

# JOB DESCRIPTION:
# {jd}

# OUTPUT:
# Final optimized resume only.
# """)

#     # Safety compression
#     if len(tailored.split()) > 720:
#         tailored = gemini(f"""
# Compress this resume to under 700 words
# without losing ATS keywords.

# RESUME:
# {tailored}
# """)

#     ats = calculate_ats(tailored, jd)
#     score = extract_ats_score(ats)

#     st.session_state.resume = tailored
#     st.session_state.ats = ats
#     st.session_state.score = score

# # ----------------------------
# # 7. OUTPUT
# # ----------------------------
# if st.session_state.resume:
#     st.success("✅ Resume Generated")

#     st.markdown("## 📄 Tailored Resume")
#     st.markdown(st.session_state.resume)

#     st.markdown("---")
#     st.markdown("## 📊 ATS Match")
#     st.markdown(st.session_state.ats)
#     st.metric("ATS Score", f"{st.session_state.score}/100")

# # ----------------------------
# # 8. IMPROVE BUTTON
# # ----------------------------
# if st.session_state.score and st.session_state.score < 90:
#     if st.button("🔥 Improve ATS to 90+"):

#         with st.spinner("Improving resume further..."):
#             improved = gemini(f"""
# Improve this resume to achieve ATS score above 90.

# RULES:
# - Stay under 700 words
# - Add missing keywords naturally
# - Strengthen impact bullets
# - Do NOT hallucinate experience

# RESUME:
# {st.session_state.resume}

# JOB DESCRIPTION:
# {st.session_state.jd}
# """)

#             ats2 = calculate_ats(improved, st.session_state.jd)
#             score2 = extract_ats_score(ats2)

#             st.session_state.resume = improved
#             st.session_state.ats = ats2
#             st.session_state.score = score2

#             st.success("🎯 Resume Improved")

# import streamlit as st
# from dotenv import load_dotenv
# import os
# from google import genai
# from firecrawl import FirecrawlApp

# # ----------------------------
# # 1. Load environment variables
# # ----------------------------
# load_dotenv()

# GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
# FIRECRAWL_API_KEY = os.getenv("FIRECRAWL_API_KEY")

# if not GOOGLE_API_KEY or not FIRECRAWL_API_KEY:
#     st.error("❌ API keys missing. Check environment variables.")
#     st.stop()

# # ----------------------------
# # 2. Initialize clients
# # ----------------------------
# genai_client = genai.Client(
#     api_key=GOOGLE_API_KEY,
#     http_options={"api_version": "v1"}
# )

# firecrawl = FirecrawlApp(api_key=FIRECRAWL_API_KEY)

# # ----------------------------
# # 3. Helper: ATS + Skill Gap
# # ----------------------------
# def calculate_ats_and_skill_gap(resume_text, job_desc):
#     prompt = f"""
# You are an ATS and Hiring Manager.

# Return:
# 1. ATS Match Score (0–100)
# 2. Missing skills / gaps
# 3. 3 concrete improvement actions

# FORMAT STRICTLY AS:

# ATS_SCORE: <number>
# SKILL_GAPS:
# - gap 1
# - gap 2
# - gap 3
# IMPROVEMENTS:
# - improvement 1
# - improvement 2
# - improvement 3

# RESUME:
# {resume_text}

# JOB DESCRIPTION:
# {job_desc}
# """
#     response = genai_client.models.generate_content(
#         model="gemini-2.5-flash",
#         contents=prompt
#     )
#     return response.text

# # ----------------------------
# # 4. Streamlit UI
# # ----------------------------
# st.set_page_config(page_title="Agentic Resume Tailor", page_icon="🤖")
# st.title("🤖 Agentic Resume Tailor (Public Version)")

# resume_text = st.text_area(
#     "📄 Paste Your Resume",
#     height=350,
#     placeholder="Paste your resume content here..."
# )

# job_url = st.text_input("🔗 Job Link (optional)")
# job_desc_manual = st.text_area(
#     "📋 Or paste Job Description",
#     height=250
# )

# st.caption("You can provide **either** a job link **or** paste the job description.")

# # ----------------------------
# # 5. Tailor Resume
# # ----------------------------
# if st.button("🚀 Tailor Resume"):

#     if not resume_text.strip():
#         st.error("❌ Resume is required.")
#         st.stop()

#     my_resume = resume_text

#     # Resolve Job Description
#     job_desc = ""

#     if job_desc_manual.strip():
#         job_desc = job_desc_manual

#     elif job_url.strip():
#         try:
#             scraped = firecrawl.scrape_url(job_url)
#             job_desc = (
#                 scraped.get("markdown") or scraped.get("content")
#                 if isinstance(scraped, dict)
#                 else getattr(scraped, "markdown", "") or getattr(scraped, "content", "")
#             )
#             if not job_desc.strip():
#                 raise Exception("Empty JD")

#         except Exception:
#             st.error("❌ Unable to extract Job Description. Please paste it manually.")
#             st.stop()
#     else:
#         st.error("❌ Provide Job Link or Job Description.")
#         st.stop()

#     # Resume Tailoring
#     with st.spinner("Tailoring resume..."):
#         resume_prompt = f"""
# You are a senior resume strategist.

# Rewrite the resume to match the job description.
# Rules:
# - Max 1–2 pages
# - Only relevant experience
# - ATS optimized
# - No hallucination

# RESUME:
# {my_resume}

# JOB DESCRIPTION:
# {job_desc}
# """
#         resume_response = genai_client.models.generate_content(
#             model="gemini-2.5-flash",
#             contents=resume_prompt
#         )

#         tailored_resume = resume_response.text

#     st.success("✅ Tailored Resume Ready")
#     st.markdown("## 📄 Tailored Resume")
#     st.markdown(tailored_resume)

#     # ATS + Skill Gap
#     st.markdown("---")
#     st.markdown("## 📊 ATS Score & Skill Gap")

#     ats_output = calculate_ats_and_skill_gap(tailored_resume, job_desc)
#     st.markdown(ats_output)

# import streamlit as st
# from dotenv import load_dotenv
# import os
# from google import genai
# from firecrawl import FirecrawlApp

# # ----------------------------
# # 1. Load environment variables
# # ----------------------------
# load_dotenv()

# GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
# FIRECRAWL_API_KEY = os.getenv("FIRECRAWL_API_KEY")

# if not GOOGLE_API_KEY or not FIRECRAWL_API_KEY:
#     st.error("❌ API keys missing. Check environment variables.")
#     st.stop()

# # ----------------------------
# # 2. Initialize clients
# # ----------------------------
# genai_client = genai.Client(
#     api_key=GOOGLE_API_KEY,
#     http_options={"api_version": "v1"}
# )

# firecrawl = FirecrawlApp(api_key=FIRECRAWL_API_KEY)

# # ----------------------------
# # 3. Safety Helpers
# # ----------------------------
# def truncate_text(text, max_chars=6000):
#     if len(text) <= max_chars:
#         return text
#     return text[:max_chars] + "\n\n[TRUNCATED FOR SAFETY]"

# # ----------------------------
# # 4. ATS + Skill Gap Function
# # ----------------------------
# def calculate_ats_and_skill_gap(resume_text, job_desc):
#     safe_resume = truncate_text(resume_text, 5000)
#     safe_jd = truncate_text(job_desc, 5000)

#     prompt = f"""
# You are an ATS system.

# Evaluate the resume against the job description.

# Respond STRICTLY in this format:

# ATS_SCORE: <number 0-100>
# SKILL_GAPS:
# - gap 1
# - gap 2
# - gap 3
# IMPROVEMENTS:
# - improvement 1
# - improvement 2
# - improvement 3

# RESUME:
# {safe_resume}

# JOB DESCRIPTION:
# {safe_jd}
# """

#     response = genai_client.models.generate_content(
#         model="gemini-2.5-flash",
#         contents=prompt,
#         config={"max_output_tokens": 400}
#     )

#     return response.text

# # ----------------------------
# # 5. Streamlit UI
# # ----------------------------
# st.set_page_config(page_title="Agentic Resume Tailor", page_icon="🤖")
# st.title("🤖 Agentic Resume Tailor")

# st.markdown("### 📄 Paste Your Resume")
# resume_text = st.text_area(
#     "Resume Content",
#     height=350,
#     placeholder="Paste your resume here (experience, skills, education, etc.)"
# )

# st.markdown("### 🎯 Job Information")
# job_url = st.text_input("Job Link (optional)")
# job_desc_manual = st.text_area(
#     "Or paste Job Description",
#     height=250
# )

# st.caption("💡 Provide either a Job Link or paste the Job Description")

# # ----------------------------
# # 6. Main Action
# # ----------------------------
# if st.button("🚀 Tailor Resume"):

#     # Validate resume
#     if not resume_text.strip():
#         st.error("❌ Please paste your resume.")
#         st.stop()

#     # Resolve Job Description
#     job_desc = ""

#     if job_desc_manual.strip():
#         job_desc = job_desc_manual

#     elif job_url.strip():
#         try:
#             scraped = firecrawl.scrape_url(job_url)
#             job_desc = (
#                 scraped.get("markdown") or scraped.get("content")
#                 if isinstance(scraped, dict)
#                 else getattr(scraped, "markdown", "") or getattr(scraped, "content", "")
#             )
#             if not job_desc.strip():
#                 raise Exception("Empty JD")

#         except Exception:
#             st.error("❌ Unable to extract job description. Please paste it manually.")
#             st.stop()
#     else:
#         st.error("❌ Provide a job link or job description.")
#         st.stop()

#     # Truncate safely before LLM
#     safe_resume = truncate_text(resume_text, 7000)
#     safe_jd = truncate_text(job_desc, 7000)

#     # ----------------------------
#     # Resume Tailoring
#     # ----------------------------
#     with st.spinner("✍️ Tailoring your resume..."):
#         resume_prompt = f"""
# You are a senior resume strategist.

# Rewrite the resume to match the job description.

# Rules:
# - Limit to 1–2 pages
# - Keep ONLY relevant experience
# - Use ATS-optimized keywords
# - No hallucination
# - Clean professional formatting

# RESUME:
# {safe_resume}

# JOB DESCRIPTION:
# {safe_jd}
# """
#         resume_response = genai_client.models.generate_content(
#             model="gemini-2.5-flash",
#             contents=resume_prompt,
#             config={"max_output_tokens": 1200}
#         )

#         tailored_resume = resume_response.text

#     st.success("✅ Tailored Resume Ready")
#     st.markdown("## 📄 Tailored Resume")
#     st.markdown(tailored_resume)

#     # ----------------------------
#     # ATS + Skill Gap
#     # ----------------------------
#     st.markdown("---")
#     st.markdown("## 📊 ATS Score & Skill Gap")

#     with st.spinner("📊 Evaluating ATS match..."):
#         ats_output = calculate_ats_and_skill_gap(tailored_resume, job_desc)

#     st.markdown(ats_output)

# import streamlit as st
# import os
# from dotenv import load_dotenv
# from google import genai
# from firecrawl import FirecrawlApp

# # ----------------------------
# # ENV SETUP
# # ----------------------------
# load_dotenv()

# GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
# FIRECRAWL_API_KEY = os.getenv("FIRECRAWL_API_KEY")

# if not GOOGLE_API_KEY or not FIRECRAWL_API_KEY:
#     st.error("❌ Missing API keys in environment variables")
#     st.stop()

# # ----------------------------
# # CLIENTS
# # ----------------------------
# genai_client = genai.Client(api_key=GOOGLE_API_KEY)
# firecrawl = FirecrawlApp(api_key=FIRECRAWL_API_KEY)

# # ----------------------------
# # HELPERS
# # ----------------------------
# def truncate_text(text, max_chars=4000):
#     return text[:max_chars] if len(text) > max_chars else text


# def generate_tailored_resume(resume_text, job_desc):
#     resume_text = truncate_text(resume_text)
#     job_desc = truncate_text(job_desc)

#     try:
#         response = genai_client.models.generate_content(
#             model="gemini-2.5-flash",
#             contents=[
#                 {
#                     "role": "user",
#                     "parts": [
#                         {"text": "You are a senior ATS resume strategist."},
#                         {"text": "Rewrite the resume to best match the job description."},
#                         {"text": "Rules:"},
#                         {"text": "- STRICTLY 1–2 pages"},
#                         {"text": "- Include ONLY relevant experience"},
#                         {"text": "- Use ATS keywords"},
#                         {"text": "- No false experience"},
#                         {"text": "- Professional bullet format"},
#                         {"text": f"\nRESUME:\n{resume_text}"},
#                         {"text": f"\nJOB DESCRIPTION:\n{job_desc}"}
#                     ]
#                 }
#             ],
#             config={
#                 "max_output_tokens": 800,
#                 "temperature": 0.4
#             }
#         )
#         return response.text

#     except Exception as e:
#         return f"❌ Resume generation failed.\n\n{e}"


# def calculate_ats_and_skill_gap(resume_text, job_desc):
#     resume_text = truncate_text(resume_text)
#     job_desc = truncate_text(job_desc)

#     try:
#         response = genai_client.models.generate_content(
#             model="gemini-2.5-flash",
#             contents=[
#                 {
#                     "role": "user",
#                     "parts": [
#                         {"text": "You are an ATS system and career coach."},
#                         {"text": "Analyze the resume against the job description."},
#                         {"text": "Return ONLY this format:"},
#                         {"text": "ATS_SCORE: <0-100>"},
#                         {"text": "MISSING_SKILLS: skill1, skill2"},
#                         {"text": "SKILL_GAP_INTELLIGENCE:"},
#                         {"text": "- skill → how to close gap"},
#                         {"text": f"\nRESUME:\n{resume_text}"},
#                         {"text": f"\nJOB DESCRIPTION:\n{job_desc}"}
#                     ]
#                 }
#             ],
#             config={
#                 "max_output_tokens": 500,
#                 "temperature": 0.3
#             }
#         )
#         return response.text

#     except Exception as e:
#         return f"❌ ATS analysis failed.\n\n{e}"


# # ----------------------------
# # STREAMLIT UI
# # ----------------------------
# st.set_page_config(page_title="Agentic Resume Tailor", page_icon="🤖")
# st.title("🤖 Agentic Resume Tailor (ATS-First)")

# resume_input = st.text_area(
#     "📄 Paste your Resume",
#     height=300,
#     placeholder="Paste your full resume here"
# )

# job_url = st.text_input("🔗 Job Link (optional)")
# job_desc_manual = st.text_area(
#     "📋 Job Description (optional)",
#     height=250
# )

# st.caption("💡 Paste either Job Link or Job Description")

# # ----------------------------
# # ACTION
# # ----------------------------
# if st.button("🚀 Tailor Resume"):
#     if not resume_input.strip():
#         st.error("❌ Please paste your resume")
#         st.stop()

#     # Resolve JD
#     job_desc = ""
#     if job_desc_manual.strip():
#         job_desc = job_desc_manual
#     elif job_url.strip():
#         try:
#             scraped = firecrawl.scrape_url(job_url)
#             job_desc = scraped.get("markdown") or scraped.get("content", "")
#             if not job_desc.strip():
#                 raise Exception("Empty JD")
#         except Exception:
#             st.error("❌ Failed to extract JD. Paste manually.")
#             st.stop()
#     else:
#         st.error("❌ Provide Job Link or Description")
#         st.stop()

#     # Resume Tailoring
#     with st.spinner("✍️ Tailoring resume..."):
#         tailored_resume = generate_tailored_resume(resume_input, job_desc)

#     st.success("✅ Tailored Resume Ready")
#     st.markdown("## 📄 Tailored Resume")
#     st.markdown(tailored_resume)

#     # ATS + Skill Gap
#     with st.spinner("📊 Analyzing ATS & Skill Gaps..."):
#         ats_output = calculate_ats_and_skill_gap(tailored_resume, job_desc)

#     st.markdown("---")
#     st.markdown("## 📊 ATS & Skill Gap Intelligence")
#     st.markdown(ats_output)

# import streamlit as st
# import os
# from dotenv import load_dotenv
# from google import genai
# from firecrawl import FirecrawlApp
# import re

# # ----------------------------
# # PAGE CONFIG (SaaS Style)
# # ----------------------------
# st.set_page_config(page_title="AI Resume ATS Optimizer", page_icon="🚀", layout="wide")

# st.markdown("""
# <style>
# .block-container {padding-top: 2rem;}
# h1, h2, h3 {font-weight: 600;}
# textarea {font-size: 14px !important;}
# </style>
# """, unsafe_allow_html=True)

# # ----------------------------
# # LOAD API KEYS
# # ----------------------------
# load_dotenv()
# GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
# FIRECRAWL_API_KEY = os.getenv("FIRECRAWL_API_KEY")

# if not GOOGLE_API_KEY:
#     st.error("Missing GOOGLE_API_KEY")
#     st.stop()

# genai_client = genai.Client(api_key=GOOGLE_API_KEY, http_options={"api_version": "v1"})

# firecrawl = None
# if FIRECRAWL_API_KEY:
#     firecrawl = FirecrawlApp(api_key=FIRECRAWL_API_KEY)

# # ----------------------------
# # HELPERS
# # ----------------------------
# def extract_score(text):
#     match = re.search(r"ATS_SCORE:\s*(\d+)", text)
#     return int(match.group(1)) if match else 0

# def tailor_resume(resume, jd):
#     prompt = f"""
# You are an elite resume strategist.

# Create a highly targeted resume tailored to the job description.

# RULES:
# • Keep resume within 1–2 pages
# • Only include relevant experience
# • Use strong bullet points (XYZ format)
# • Insert ATS keywords naturally
# • Do NOT hallucinate

# RESUME:
# {resume}

# JOB DESCRIPTION:
# {jd}
# """
#     response = genai_client.models.generate_content(
#         model="gemini-2.5-flash",
#         contents=prompt,
#         config={"max_output_tokens": 1200}
#     )
#     return response.text

# def ats_analysis(resume, jd):
#     prompt = f"""
# You are an ATS system.

# Return:
# ATS_SCORE: <number>
# MISSING_KEYWORDS: <comma list>
# SKILL_GAPS: <comma list>
# SUGGESTIONS:
# - suggestion 1
# - suggestion 2
# - suggestion 3

# RESUME:
# {resume}

# JOB DESCRIPTION:
# {jd}
# """
#     response = genai_client.models.generate_content(
#         model="gemini-2.5-flash",
#         contents=prompt,
#         config={"max_output_tokens": 600}
#     )
#     return response.text

# def improve_resume(resume, jd, missing):
#     prompt = f"""
# Improve this resume to reach ATS score above 90.

# Focus on adding these missing keywords:
# {missing}

# Keep it truthful and 1–2 pages.

# RESUME:
# {resume}

# JOB DESCRIPTION:
# {jd}
# """
#     response = genai_client.models.generate_content(
#         model="gemini-2.5-flash",
#         contents=prompt,
#         config={"max_output_tokens": 1200}
#     )
#     return response.text

# # ----------------------------
# # HEADER
# # ----------------------------
# st.title("🚀 AI-Powered Resume ATS Optimizer")
# st.caption("Tailor your resume. Beat ATS. Land interviews.")

# st.markdown("---")

# # ----------------------------
# # INPUT SECTION (2 Columns)
# # ----------------------------
# col1, col2 = st.columns(2)

# with col1:
#     st.subheader("📄 Your Resume")
#     resume_text = st.text_area("Paste your full resume here", height=350)

# with col2:
#     st.subheader("🎯 Job Description")
#     job_url = st.text_input("Paste Job Link (optional)")
#     job_desc_manual = st.text_area("Or paste Job Description manually", height=300)

# st.markdown("---")

# # ----------------------------
# # MAIN ACTION BUTTON
# # ----------------------------
# if st.button("✨ Tailor Resume for This Job", use_container_width=True):

#     if not resume_text.strip():
#         st.warning("Please paste your resume.")
#         st.stop()

#     if not job_desc_manual.strip() and not job_url.strip():
#         st.warning("Please paste a job description or link.")
#         st.stop()

#     with st.spinner("Analyzing job and tailoring resume..."):

#         job_desc = job_desc_manual

#         if not job_desc and firecrawl and job_url:
#             try:
#                 scraped = firecrawl.scrape_url(job_url)
#                 job_desc = scraped.get("markdown") or scraped.get("content", "")
#             except:
#                 st.error("Could not extract job description. Please paste manually.")
#                 st.stop()

#         # Generate tailored resume
#         tailored_resume = tailor_resume(resume_text, job_desc)

#         # ATS Analysis
#         ats_output = ats_analysis(tailored_resume, job_desc)
#         score = extract_score(ats_output)

#         st.session_state.tailored_resume = tailored_resume
#         st.session_state.job_desc = job_desc
#         st.session_state.ats_output = ats_output
#         st.session_state.ats_score = score

# # ----------------------------
# # OUTPUT SECTION
# # ----------------------------
# if "tailored_resume" in st.session_state:

#     st.subheader("🤖 Tailored Resume")
#     st.text_area("Optimized Resume", st.session_state.tailored_resume, height=400)

#     st.download_button("📥 Download Resume", st.session_state.tailored_resume, "tailored_resume.txt")

#     st.markdown("---")

#     st.subheader("📊 ATS Match Score")
#     score = st.session_state.ats_score

#     color = "red" if score < 60 else "orange" if score < 80 else "green"
#     st.markdown(f"<h2 style='color:{color}'>Score: {score}/100</h2>", unsafe_allow_html=True)

#     st.markdown("### 🧠 ATS Insights")
#     st.text_area("ATS Feedback", st.session_state.ats_output, height=200)

#     # Improve Button
#     if score < 90:
#         if st.button("🚀 Improve Resume to 90+ Score"):
#             with st.spinner("Boosting resume score..."):
#                 missing = re.search(r"MISSING_KEYWORDS:(.*)", st.session_state.ats_output)
#                 missing = missing.group(1) if missing else ""
#                 improved = improve_resume(st.session_state.tailored_resume, st.session_state.job_desc, missing)

#                 st.session_state.tailored_resume = improved
#                 new_ats = ats_analysis(improved, st.session_state.job_desc)
#                 st.session_state.ats_output = new_ats
#                 st.session_state.ats_score = extract_score(new_ats)
#                 st.rerun()

# import streamlit as st
# import os
# from dotenv import load_dotenv
# from google import genai
# from firecrawl import FirecrawlApp
# import re

# # ----------------------------
# # PAGE CONFIG
# # ----------------------------
# st.set_page_config(page_title="AI Resume ATS Optimizer", page_icon="🚀", layout="wide")

# st.markdown("""
# <style>
# .block-container {padding-top: 2rem;}
# h1, h2, h3 {font-weight: 600;}
# textarea {font-size: 14px !important;}
# </style>
# """, unsafe_allow_html=True)

# # ----------------------------
# # LOAD API KEYS
# # ----------------------------
# load_dotenv()
# GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
# FIRECRAWL_API_KEY = os.getenv("FIRECRAWL_API_KEY")

# if not GOOGLE_API_KEY:
#     st.error("Missing GOOGLE_API_KEY")
#     st.stop()

# genai_client = genai.Client(api_key=GOOGLE_API_KEY, http_options={"api_version": "v1"})

# firecrawl = FirecrawlApp(api_key=FIRECRAWL_API_KEY) if FIRECRAWL_API_KEY else None

# # ----------------------------
# # HELPERS
# # ----------------------------
# def extract_score(text):
#     match = re.search(r"ATS_SCORE:\s*(\d+)", text)
#     return int(match.group(1)) if match else 0

# def safe_truncate(text, limit=12000):
#     return text[:limit]

# def tailor_resume(resume, jd):
#     prompt = f"""
# You are an elite resume strategist.

# Create a highly targeted resume tailored to the job description.

# RULES:
# • Keep resume within 1–2 pages
# • Only include relevant experience
# • Use strong bullet points (XYZ format)
# • Insert ATS keywords naturally
# • Do NOT hallucinate

# RESUME:
# {resume}

# JOB DESCRIPTION:
# {jd}
# """
#     response = genai_client.models.generate_content(
#         model="gemini-2.5-flash",
#         contents=prompt,
#         config={"max_output_tokens": 1000}
#     )
#     return response.text

# def ats_analysis(resume, jd):
#     prompt = f"""
# You are an ATS system.

# Return:
# ATS_SCORE: <number>
# MISSING_KEYWORDS: <comma list>
# SKILL_GAPS: <comma list>
# SUGGESTIONS:
# - suggestion 1
# - suggestion 2
# - suggestion 3

# RESUME:
# {resume}

# JOB DESCRIPTION:
# {jd}
# """
#     response = genai_client.models.generate_content(
#         model="gemini-2.5-flash",
#         contents=prompt,
#         config={"max_output_tokens": 500}
#     )
#     return response.text

# def improve_resume(resume, jd, missing):
#     prompt = f"""
# Improve this resume to reach ATS score above 90.

# Focus on adding these missing keywords:
# {missing}

# Keep it truthful and 1–2 pages.

# RESUME:
# {resume}

# JOB DESCRIPTION:
# {jd}
# """
#     response = genai_client.models.generate_content(
#         model="gemini-2.5-flash",
#         contents=prompt,
#         config={"max_output_tokens": 1000}
#     )
#     return response.text

# # ----------------------------
# # HEADER
# # ----------------------------
# st.title("🚀 AI-Powered Resume ATS Optimizer")
# st.caption("Tailor your resume. Beat ATS. Land interviews.")
# st.markdown("---")

# # ----------------------------
# # INPUTS
# # ----------------------------
# col1, col2 = st.columns(2)

# with col1:
#     st.subheader("📄 Your Resume")
#     resume_text = st.text_area("Paste your full resume here", height=350)

# with col2:
#     st.subheader("🎯 Job Description")
#     job_url = st.text_input("Paste Job Link (optional)")
#     job_desc_manual = st.text_area("Or paste Job Description manually", height=300)

# st.markdown("---")

# # ----------------------------
# # MAIN BUTTON
# # ----------------------------
# if st.button("✨ Tailor Resume for This Job", use_container_width=True):

#     if not resume_text.strip():
#         st.warning("Please paste your resume.")
#         st.stop()

#     job_desc = ""

#     # 1️⃣ Manual JD takes priority
#     if job_desc_manual.strip():
#         job_desc = job_desc_manual.strip()

#     # 2️⃣ Else try scraping
#     elif job_url.strip() and firecrawl:
#         try:
#             scraped = firecrawl.scrape_url(job_url)

#             if isinstance(scraped, dict):
#                 job_desc = scraped.get("markdown") or scraped.get("content", "")
#             else:
#                 job_desc = getattr(scraped, "markdown", "") or getattr(scraped, "content", "")

#         except Exception:
#             st.error("Could not extract job description. Please paste manually.")
#             st.stop()

#     if not job_desc.strip():
#         st.error("Job description is required.")
#         st.stop()

#     with st.spinner("AI is tailoring your resume..."):

#         resume_text = safe_truncate(resume_text)
#         job_desc = safe_truncate(job_desc)

#         tailored_resume = tailor_resume(resume_text, job_desc)
#         ats_output = ats_analysis(tailored_resume, job_desc)
#         score = extract_score(ats_output)

#         st.session_state.tailored_resume = tailored_resume
#         st.session_state.job_desc = job_desc
#         st.session_state.ats_output = ats_output
#         st.session_state.ats_score = score

# # ----------------------------
# # OUTPUT
# # ----------------------------
# if "tailored_resume" in st.session_state:

#     st.subheader("🤖 Tailored Resume")
#     st.text_area("Optimized Resume", st.session_state.tailored_resume, height=400)
#     st.download_button("📥 Download Resume", st.session_state.tailored_resume, "tailored_resume.txt")

#     st.markdown("---")
#     st.subheader("📊 ATS Match Score")

#     score = st.session_state.ats_score
#     color = "red" if score < 60 else "orange" if score < 80 else "green"
#     st.markdown(f"<h2 style='color:{color}'>Score: {score}/100</h2>", unsafe_allow_html=True)

#     st.markdown("### 🧠 ATS Insights")
#     st.text_area("ATS Feedback", st.session_state.ats_output, height=200)

#     if score < 90:
#         if st.button("🚀 Improve Resume to 90+ Score"):
#             with st.spinner("Boosting resume score..."):
#                 missing = re.search(r"MISSING_KEYWORDS:(.*)", st.session_state.ats_output)
#                 missing = missing.group(1) if missing else ""
#                 improved = improve_resume(st.session_state.tailored_resume, st.session_state.job_desc, missing)

#                 st.session_state.tailored_resume = improved
#                 new_ats = ats_analysis(improved, st.session_state.job_desc)
#                 st.session_state.ats_output = new_ats
#                 st.session_state.ats_score = extract_score(new_ats)
#                 st.rerun()

# ----------------------------------

import streamlit as st
import os
from dotenv import load_dotenv
from google import genai
from firecrawl import FirecrawlApp
import re

# ----------------------------
# PAGE CONFIG (SaaS Style)
# ----------------------------
st.set_page_config(page_title="AI Resume ATS Optimizer", page_icon="🚀", layout="wide")

st.markdown("""
<style>
.block-container {padding-top: 2rem;}
h1, h2, h3 {font-weight: 600;}
textarea {font-size: 14px !important;}
.stButton>button {height: 3em; font-weight: 600;}
</style>
""", unsafe_allow_html=True)

# ----------------------------
# LOAD API KEYS
# ----------------------------
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
FIRECRAWL_API_KEY = os.getenv("FIRECRAWL_API_KEY")

if not GOOGLE_API_KEY:
    st.error("Missing GOOGLE_API_KEY in Streamlit secrets or .env file")
    st.stop()

genai_client = genai.Client(api_key=GOOGLE_API_KEY, http_options={"api_version": "v1"})

firecrawl = FirecrawlApp(api_key=FIRECRAWL_API_KEY) if FIRECRAWL_API_KEY else None

# ----------------------------
# HELPERS
# ----------------------------
def extract_score(text):
    match = re.search(r"ATS_SCORE:\s*(\d+)", text)
    return int(match.group(1)) if match else 0

def safe_truncate(text, limit=20000):  # Large enough to keep full resume
    return text[:limit]

# ----------------------------
# AI FUNCTIONS
# ----------------------------
def tailor_resume(resume, jd):
    prompt = f"""
Tailor this resume to match the job description.

Keep it ATS optimized, achievement-focused, and within 1–2 pages.
Do NOT add fake experience.

RESUME:
{resume}

JOB DESCRIPTION:
{jd}
"""
    response = genai_client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config={"max_output_tokens": 2500}
    )
    return response.text


def ats_analysis(resume, jd):
    prompt = f"""
You are an ATS scanner.

Return EXACTLY in this format:

ATS_SCORE: <number>
MISSING_KEYWORDS: <comma separated>
SKILL_GAPS: <comma separated>
SUGGESTIONS:
- suggestion
- suggestion
- suggestion

RESUME:
{resume}

JOB DESCRIPTION:
{jd}
"""
    response = genai_client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config={"max_output_tokens": 800}
    )
    return response.text


def improve_resume(resume, jd, missing):
    prompt = f"""
Improve this resume using the missing keywords below.

Keep it truthful, ATS optimized, and under 2 pages.

MISSING KEYWORDS:
{missing}

RESUME:
{resume}

JOB DESCRIPTION:
{jd}
"""
    response = genai_client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config={"max_output_tokens": 2500}
    )
    return response.text


# ----------------------------
# HEADER
# ----------------------------
st.title("🚀 AI-Powered Resume ATS Optimizer")
st.caption("Tailor your resume. Beat ATS. Land interviews.")

st.markdown("---")

# ----------------------------
# INPUT SECTION
# ----------------------------
col1, col2 = st.columns(2)

with col1:
    st.subheader("📄 Your Resume")
    resume_text = st.text_area("Paste your full resume here", height=400)

with col2:
    st.subheader("🎯 Job Description")
    job_url = st.text_input("Paste Job Link (optional)")
    job_desc_manual = st.text_area("Or paste Job Description manually", height=350)

st.markdown("---")

# ----------------------------
# MAIN BUTTON
# ----------------------------
if st.button("✨ Tailor Resume for This Job", use_container_width=True):

    if not resume_text.strip():
        st.warning("Please paste your resume.")
        st.stop()

    if not job_desc_manual.strip() and not job_url.strip():
        st.warning("Please paste a job description or link.")
        st.stop()

    with st.spinner("Analyzing job and tailoring resume..."):

        job_desc = job_desc_manual.strip()

        # Scrape job description if URL provided
        if not job_desc and firecrawl and job_url:
            try:
                scraped = firecrawl.scrape_url(job_url)
                job_desc = scraped.get("markdown") or scraped.get("content", "")
            except:
                st.error("Could not extract job description. Please paste manually.")
                st.stop()

        resume_text = safe_truncate(resume_text)
        job_desc = safe_truncate(job_desc)

        tailored_resume = tailor_resume(resume_text, job_desc)
        ats_output = ats_analysis(tailored_resume, job_desc)
        score = extract_score(ats_output)

        st.session_state.tailored_resume = tailored_resume
        st.session_state.job_desc = job_desc
        st.session_state.ats_output = ats_output
        st.session_state.ats_score = score

# ----------------------------
# OUTPUT SECTION
# ----------------------------
if "tailored_resume" in st.session_state:

    st.subheader("🤖 Tailored Resume")
    st.text_area("Optimized Resume", st.session_state.tailored_resume, height=450)
    st.download_button("📥 Download Resume", st.session_state.tailored_resume, "tailored_resume.txt")

    st.markdown("---")

    st.subheader("📊 ATS Match Score")
    score = st.session_state.ats_score
    color = "red" if score < 60 else "orange" if score < 80 else "green"
    st.markdown(f"<h2 style='color:{color}'>Score: {score}/100</h2>", unsafe_allow_html=True)

    st.markdown("### 🧠 ATS Insights")
    st.text_area("ATS Feedback", st.session_state.ats_output, height=220)

    # ----------------------------
    # IMPROVE BUTTON
    # ----------------------------
    if score < 90:
        if st.button("🚀 Improve Resume to 90+ Score"):
            with st.spinner("Boosting resume score..."):
                missing_match = re.search(r"MISSING_KEYWORDS:(.*)", st.session_state.ats_output)
                missing = missing_match.group(1) if missing_match else ""

                improved_resume = improve_resume(
                    st.session_state.tailored_resume,
                    st.session_state.job_desc,
                    missing
                )

                new_ats = ats_analysis(improved_resume, st.session_state.job_desc)

                st.session_state.tailored_resume = improved_resume
                st.session_state.ats_output = new_ats
                st.session_state.ats_score = extract_score(new_ats)

                st.rerun()
