import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
from src.components.document_scraper import extract_text
from src.components.image_scraper import scrape_image
from src.components.content_generator import content_generator
from src.components.improvement_suggestor import improvement_suggestions
from src.components.mail_handling import handle_mail
import time

def resume_improver(file_path: str, email_id:str=None):
    try:
        st.write("### Processing Resume...")
        with st.spinner("Extracting text...."):
            if file_path.endswith(('.jpg', '.jpeg', '.png', '.webp')):
                text = scrape_image(file_path, additional_info='''Scrape this resume image.
                                    If it is difficult to do so, return 'Not able to scrape'.
                                    Do not return any false or non sensical information please.''')
            elif file_path.endswith(('.pdf', '.docx', '.xlsx', '.csv', '.txt')):
                text = extract_text(file_path)
            else:
                st.error("Unsupported file format! Please upload a valid resume format.")
                return
            
            st.success("Text Extracted Successfully!")
        
        st.write("### Understanding Resume Structure")
        with st.spinner("Structuring extracted data..."):
            resume_understander = content_generator(role='Expert Resume Parser and data extractor.', work=f"""
                Scrape a given text which is a resume extracted and I would like you to extract the following:
                        * Full Name
                        * Contact Information (Phone number, Email, LinkedIn, etc.)
                        * Skills (e.g., programming languages, software proficiency, etc.)
                        * Professional Experience (Company names, job titles, duration, responsibilities)
                        * Education (Degree, University, Graduation Year)
                        * Certifications (if available)
                        * Languages spoken (if available)
                        * Other relevant sections (projects, awards, or references)
                        This is the resume text that is provided to you:
                        {text}""",
                        additional_info=f"""
                        There are no items here so return nothing in that.
                        """)
            st.success("Resume parsed successfully!")
            page_content = '\n'.join([f'{key}: {value}' for key, value in resume_understander['content'].items()])
        
        st.write("### Identifying Issues")
        with st.spinner('Identifying issues....'):
            issues_serped = content_generator(role='Resume Improvement Suggestor', work=f'''
            Given the resume content, you should identify some issues in the resume.
            Do not return any hyperlink related issue. Eg. Github name has no link, linkedin has no link, etc. Please do not do this.
                                            
            If you cannot find any issue, you can return 'No issues found.'
            Else you should return issues strictly in bullets form.
            Only return the requested information.
            This is the resume content in which you have to find issues:
            {page_content}
            ''', 
            additional_info=f"""There are no items here so return nothing in that.""")
            st.success("Issues identified successfully!")
            try:
                text = ''
                for a in issues_serped['content']:
                    text = text + '\n' + f'* {a}'
            except Exception as e:
                text = issues_serped['content']
            st.text_area("Identified Issues", text, height=200)
        
        st.write("### Suggesting Improvements.")
        with st.spinner("Generating improvement suggestions (This takes time...)"):
            improvements_needed = improvement_suggestions(
                background='You are a resume improvement expert in each domain.',
                issues=issues_serped['content'],
                additional_info=f'''
                The issues were found on this resume text:
                {page_content}
                ''',
                whom='user'
            )
            st.success("Improvements generation succeesssfull!")
        
        st.write("### Generating Improved Resume")
        with st.spinner('Restructuring your resume, please wait....'):
            improved_resume = content_generator(role='Resume improver based on issues and resolution provided.',
            work=f"""
            This is the original resume:
            {page_content}

            These are some issues that were found along with their possible resolutions:
            {improvements_needed}
            """)
            st.success("Generation successful!")
            try:
                op = improved_resume['content']
                try:
                    if improved_resume['content'].startswith("```"):
                        first_newline = improvements_needed.find("\n")  
                        last_newline = improvements_needed.rfind("\n") 

                        if first_newline != -1 and last_newline != -1 and first_newline < last_newline:
                            op = improved_resume[first_newline + 1:last_newline]
                except Exception:
                    pass
            except:
                pass

            st.text_area("Improvements : ", op, height=200)
        
        if email_id == None or email_id == '':
            return
        else:
            st.info(f"""⚠️ Email feature is still under development and is available for testing purposes currently.
                        Please don't judge the developer based on this feature! 🥲😎""")
            try:
                with st.spinner('Generating email....'):
                    handle_mail(mail_content=improved_resume['content'], to=email_id, additional_info=f'''
                            Forget all the things said earlier.
                            The formal new prompt starts here:
                            Take this mail content:
                            {improved_resume['content']}
                            Also include this following information:
                            It is the improvements that are needed in the resume. If formatting is wrong, please correct it and send at the last of the mail body:
                            {improvements_needed}.
                            Please ensure proper mail formatting.
                            Strictly,
                            The final mail format should be:
                                Hey ...,
                                Here's a template of your refined resume:
                                ...
                                Also, here are some improvements that were needed:
                                ...
                                Best Regards,
                                Agentic Email Bot.
                            Action!!
                            ''')
                    st.success("Email Sent Successfully!")
            except Exception as e:
                st.error(f'Error sending email : {e}')

    except Exception as e:
        st.error(f"Error: {e}")

st.set_page_config(page_title="Resume Improver", layout="wide")
st.title("🚀 AI Resume Improver")
st.write("Upload your resume to extract, analyze, improve, and get suggestions instantly!")

st.sidebar.markdown("<h3 style='text-align: center;'>⬇️ Upload your Resume ⬇️</h3>", unsafe_allow_html=True)
uploaded_file = st.sidebar.file_uploader('', type=["pdf", "docx", "png", "jpg", "jpeg", "webp"], accept_multiple_files=False)

if uploaded_file:
    email_id = st.text_input('Enter email id (optional): ', placeholder='Get emailed suggestions.')
    os.makedirs('temp', exist_ok=True)
    file_path = f"temp/{uploaded_file.name}"
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    button = st.button('Click to Process!')
    if button:
            resume_improver(file_path, email_id)