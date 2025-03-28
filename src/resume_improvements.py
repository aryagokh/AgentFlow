from components.document_scraper import extract_text
from components.image_scraper import scrape_image
from components.content_generator import content_generator
from components.improvement_suggestor import improvement_suggestions
from components.mail_handling import handle_mail, create_mail, send_mail
import os
from dotenv import load_dotenv
import time
import json
load_dotenv()

def resume_improver(file_path:str, ):
    try:
        print("Chain 1 : Text Extractor")
        if file_path.endswith(('.jpg', '.jpeg', '.png', '.webp')):
            text = scrape_image(file_path, 
                                additional_info=f'''
                                Scrape this resume image.
                                If it is difficult to do so, return 'Not able to scrape'.
                                Do not return any false or non sensical information please.
                                ''')
        elif file_path.endswith(('.pdf', '.docx', '.xlsx', '.csv', '.txt')):
            text = extract_text(file_path)
        else:
            print("Files not compatible to scrape. Please try uploading following compatible formats.")
            print("(jpg, jpeg, png, webp, pdf, docx, xlsx, csv and txt files only.)")
            return -1
        
        print("Chain 2 : Resume subparts scraper")
        retries, max_retries = 0, 5
        while True:
            try:
                if retries < max_retries:
                    resume_understander = content_generator(role='Expert Resume Parser and Data Extractor.',
                    work=f"""
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
                    {text}
                    """,
                    additional_info=f"""
                    There are no items here so return nothing in that.
                    """)
                    break
                else:
                    print("Not able to parse right now. Max attempts reached. Please try again after sometime!!")
                    return -1
            except Exception as e:
                print(f"Exception {e} occurred!! Retrying in 5 seconds....")
                time.sleep(5)
                retries = retries + 1 
        
        page_content = f''
        for key, value in resume_understander['content'].items():
            page_content = page_content + f'\n {key} : {value}'

        print("Chain 3.1 : Issues Identifier")
        issues_serped = content_generator(role='Resume Improvement Suggestor', work=f'''
        Given the resume content, you should identify some issues in the resume.
        Do not return any hyperlink related issue. Eg. Github name has no link, linkedin has no link, etc. Please do not do this.
                                          
        If you cannot find any issue, you can return 'No issues found.'
        Else you should return issues in bullets form.
        Only return the requested information.
        This is the resume content in which you have to find issues:
        {page_content}
        ''', 
        additional_info=f"""There are no items here so return nothing in that.""")
        print("GEMINI")
        print(issues_serped)

        print("Chain 3.2 : Issue Solver")
        improvements_needed = improvement_suggestions(
            background='You are an resume improvement expert in each domain.',
            issues=issues_serped['content'],
            additional_info=f'''
            The issues were found on this resume text:
            {page_content}
            ''',
            whom='user'
        )
        print("Improvements needed")
        print(improvements_needed.strip("\\boxed{```markdown").strip("```python").strip("```json").strip("```").strip("```json").strip("```").strip("{").strip("}"))
        
        improvements_needed = improvements_needed.strip("\\boxed{```markdown").strip("```python").strip("```json").strip("```").strip("```json").strip("```").strip("{").strip("}")
        
        print("Chain 4 : Improver")
        improved_resume = content_generator(role='Resume improver based on issues and resolution provided.',
        work=f"""
        This is the original resume:
        {page_content}

        These are some issues that were found along with their possible resolutions:
        {improvements_needed}
        """)

        print(improved_resume['content'])

        print("Chain 5 : Mailer")
        print(improvements_needed)
        # return
        # os.makedirs('sample_file.txt', exist_ok=True)
        # a = ''
        # # with open('sample_file.txt', 'wb') as file:
        # for key, value in improved_resume['content'].items():
        #     # file.append(f"{key} : {value}")
        #     a = a + f'\n{key} : {value}'
        
        retries, max_retries = 0, 5
        while True:
            try:
                if retries < max_retries:
                    handle_mail(mail_content=improved_resume['content'], to='arya7555@gmail.com', additional_info=f'''
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
 
                    break
                else:
                    print("Max retries exceeded!! Cannot mail right now. Please try mail feature after sometime.")
        # os.rmdir(file)
            except Exception as e:
                print(f"Exception {e} occurred. Retrying mailing in 5 seconds")
                time.wait(5)
                retries = retries + 1

    except Exception as e:
        print(e)
        return -1

if __name__ == '__main__':
    # print('*'*50)
    # resume_improver(file_path='data/raw/documents/Kiran_Resume.pdf')
    # print('*'*50)
    # resume_improver(file_path='data/raw/documents/Arya_Gokhale_Resume.pdf')
    # print('*'*50)
    # resume_improver(file_path='data/raw/documents/Tirath_Bhathawala_Resume.pdf')
    # print('*'*50)
    # resume_improver(file_path='data/raw/documents/TaranShah_CV.pdf')
    # print('*'*50)
    resume_improver('data/raw/documents/Mihir_CV.pdf')
    # page_content = f''
    # print(resume['content'])

                    # Generate a subject that best suits "Improvements suggestions for your resume."
                    # Generate mail body using the content provided. You should list down all the details properly.
                    # The user earlier provided me their resume and now I have to improve their resume and the improved resume is provided to you in mail content.

                                       # handle_mail(
                    #     mail_content=improved_resume['content'],
                    #     to='arya7555@gmail.com',
                    #     additional_info=f"""
                    #     Forget all previous instructions.

                    #     Use the following refined resume content:
                    #     {improved_resume['content']}

                    #     Additionally, include the following resume improvements at the end:
                    #     {improvements_needed}

                    #     **Strict Mail Format:**
                        
                    #     **Subject:** Refined Resume Update  

                    #     **Body:**
                        
                    #     Hey [Recipient’s Name],  

                    #     Here's a template of your refined resume:  
                    #     [Insert resume content]  

                    #     Also, here are some improvements that were needed:  
                    #     [Insert resume improvements]  

                    #     Best Regards,  
                    #     Agentic Email Bot  
                    #     """
                    # )