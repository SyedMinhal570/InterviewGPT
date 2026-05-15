import google.generativeai as genai
import os
from dotenv import load_dotenv   # install python-dotenv if not present
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def generate_questions(resume_text: str, job_description: str, num_questions=5) -> list:
    prompt = f"""
    You are an expert technical interviewer. Based on the following resume and job description,
    generate {num_questions} interview questions (mix of technical and behavioral) that an interviewer
    would ask to assess the candidate's fit for the role. Return only the list of questions, numbered.

    Resume:
    {resume_text[:2000]}

    Job Description:
    {job_description[:2000]}

    Questions:
    """
    model = genai.GenerativeModel('gemini-2.5-flash')
    response = model.generate_content(prompt)
    # Parse questions
    import re
    questions = []
    for line in response.text.split('\n'):
        match = re.match(r'^\s*\d+[\.\)]\s*(.*)', line)
        if match:
            questions.append(match.group(1).strip())
    return questions[:num_questions]