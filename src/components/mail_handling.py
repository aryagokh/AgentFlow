import smtplib
from email.mime.text import MIMEText
import os
import google.genai as genai
from dotenv import load_dotenv
import json
from config import get_secret
load_dotenv()

def create_mail_prompt(mail_content, additional_info=None):
    prompt = f'''
    You are expert in writing emails.
    You go thoroughly through the content provided.
    The content is as follows:
    {mail_content}

    Think about a suitable subject for this email.
    Now think about perfect body that covers all the mail content.
    If mail content is any set of instructions/summary, provide the body in forms of bullets.
    If not, write a simple body that covers all aspects of the mail content provided.

    Always remember, no additional information from your side. No filler words and **highlighted headers**.
    Just return json as follows:
    subject:
    body:
    '''
    if additional_info is not None:
        prompt = prompt + '\n' + f"Here is some additional information about the content : {additional_info}"

    return prompt


def create_mail(mail_content, additional_info=None):
    try:
        client = genai.Client(api_key=get_secret('GEMINI_API_KEY'))
        prompt = create_mail_prompt(mail_content, additional_info)
        response = client.models.generate_content(
            model='gemini-2.0-flash-lite',
            contents=prompt
        )
        subject = client.models.generate_content(
            model='gemini-2.0-flash-lite',
            contents=[f'Extract only the subject from the following. No additional information please and no fillers please: {response.candidates[0].content.parts[0].text}']
        )
        body = client.models.generate_content(
            model='gemini-2.0-flash-lite',
            contents=[f'Extract only the body from the following. Add salutation. No additional information please and no fillers please: {response.candidates[0].content.parts[0].text}']
        )
        return {
            'subject': subject.candidates[0].content.parts[0].text,
            'body':body.candidates[0].content.parts[0].text
        }
    except Exception as e:
        print(e)
        return -1


def send_mail(to, mail_content:json):
    try:
        sender_email = get_secret('GOOGLE_MAIL_SENDER')
        password = get_secret('GOOGLE_APP_PASSWORD')

        msg =  MIMEText(mail_content['body'])
        subject = mail_content['subject']
        msg["Subject"] = subject
        msg["From"] = get_secret('GOOGLE_MAIL_SENDER')
        msg["To"] = to
        try:
            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
                server.login(sender_email, password)
                server.sendmail(sender_email, to, msg.as_string())
                print("Email sent successfully!")
        except Exception as e:
            print(f"Coudn't send email : {e}")
            return -1
    except Exception as e:
        print(e)
        return -1


def handle_mail(mail_content, to, additional_info=None):
    response_json = create_mail(mail_content, additional_info)
    send_mail(to, response_json)
    return 0

