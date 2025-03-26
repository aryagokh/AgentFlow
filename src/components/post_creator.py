import google.genai as genai
from openai import OpenAI
import os
from dotenv import load_dotenv
from google.genai.types import GenerateContentConfig, Tool, GoogleSearch
from config import get_secret
load_dotenv()


def construct_post_generation_prompt(topic, platform, additional_info=None):
    prompt = f'''
    You are an expert in writing all kinds of social media posts.
    This time you have to write for {platform} platform.
    The topic of the post is {topic}.

    Do not include headers and suggestions.
    Just only do what is asked.
    Strictly, directly start with the post content. No filler words and no filler sentences please.
    Last but not the least, you can use search tool provided for searching if latest topics are to be generated.
    ''' 
    if additional_info is not None:
        prompt = prompt + "\n" + f"Also consider this : {additional_info}."

    return prompt


def create_post(topic, platform, creativity_temperature=0.7, additional_info=None):
    try:
        prompt = construct_post_generation_prompt(topic, platform, additional_info)
        client = genai.Client(api_key=get_secret('GEMINI_API_KEY'))

        google_search_tool = Tool(
            google_search=GoogleSearch()
            )
        
        response = client.models.generate_content(
            model='gemini-2.0-flash',
            contents=prompt,
            config = GenerateContentConfig(
                temperature=creativity_temperature,
                tools=[google_search_tool]
                )
        )
        return_response = ''
        for i, each in enumerate(response.candidates[0].content.parts):
            # print(i, "-->", each.text)
            return_response = return_response + '\n' + each.text
        return return_response
    except Exception as e:
        print(e)
        return -1

# if __name__ == '__main__':
#     post = create_post(
#     topic='Machine Learning in finance markets',
#     platform='LinkedIn',
#     creativity_temperature=1.2,
#     additional_info='I am a financial social media influencer. My target audience is 30-40 age group people who trade in markets.'
#     )

#     print(post)