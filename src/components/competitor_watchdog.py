import os
import google.genai as genai
from dotenv import load_dotenv
from google.genai.types import Tool, GenerateContentConfig, GoogleSearch

load_dotenv()

client = genai.Client(api_key=os.getenv('GEMINI_API_KEY'))
google_search_tool = Tool(google_search = GoogleSearch())

def construct_watchdog_prompt(content, goal, additional_info=None):
    prompt = f'''
    You are an expert analyzer for competitor watchdog.
    The output should not include filler texts and strictly no **headers like this**.
    You can use Google Search tool provided to monitor recent competitor activities too.

    The content is as follows:
    {content}

    The goal is as follows:
    {goal}

    Identify domain on your own and work based on it. Focus on competitors too which is our main goal.
    Output in this manner each seprately:
    - Who competitors are ?
    ** What have competitors done/are doing which is different?
    ** Why is that is good/bad approach?
    Do not include filler words and stricly output only what is asked. No **headers** please.
    '''
    
    if additional_info is not None:
        prompt = prompt + '\n' + f'''
        Keep in mind about also the additional information which is provided here as follows:
        {additional_info}.
        '''
    return prompt

def competitor_watchdog(content, goal, additional_info=None):
    try:
        prompt = construct_watchdog_prompt(content, goal, additional_info)
        client = genai.Client(api_key=os.getenv('GEMINI_API_KEY'))
        response = client.models.generate_content(
            model='gemini-2.0-flash',
            contents=prompt,
            config=GenerateContentConfig(
                tools=[google_search_tool],
                response_modalities=["TEXT"]
            )
        )
        return response.candidates[0].content.parts[0].text
    except Exception as e:
        print(e)
        return -1


# if __name__ == '__main__':
#     print(competitor_watchdog(
#         content='AI ML',
#         goal='How are companies analyzing Big Data Analysis smoothely?',
#         additional_info='The company is struggling with paid apis as their cost is very high.'
#     ))