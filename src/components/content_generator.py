import google.genai as genai
import os
from dotenv import load_dotenv
from pydantic import BaseModel
from typing import List, Dict
import json
from config import get_secret
load_dotenv()

# class Item(BaseModel):
#     item: str
#     quantity: str

# class RecipeResponse(BaseModel):
#     content: str
#     items: List[Item]


def create_content_generation_prompt(role, work, additional_info=None):
    prompt = f'''
    You are an expert {role}.
    This time you have to do the following:
    {work}
    Generate content based on it. It should be simple, straight forward and easy to implement if implementation is possible.
    If there are any items present in the content generated, please keep a track of it and its quantity (start with smallest possible available).
    Please do not use any filler words and no **highlighted headers and titles**.
    Output should be strictly in the following JSON structure:
    ```json{{
    content : generated content,
    items : [items]
    }}```
    '''
    if additional_info is not None:
        prompt = prompt + '\n' + f'''
        Also, consider this additional details:
        {additional_info}.
        '''
    return prompt


def generate_content(role, work, additional_info=None):
    try:
        client = genai.Client(api_key=get_secret('GEMINI_API_KEY'))
        response = client.models.generate_content(
            model='gemini-2.0-flash',
            contents=create_content_generation_prompt(role, work, additional_info)
        )
        # print(response.candidates[0].content.parts[0].text)
        return response.candidates[0].content.parts[0].text
    except Exception as e:
        print("Error", e)
        return -1


def clean_json_output(raw_text):
    try:
        parsed_json = json.loads(raw_text.strip("```json"))
        parsed_response = json.dumps(parsed_json, indent=4, ensure_ascii=False)
        parsed_list_response = json.loads(parsed_response)
        return parsed_list_response
    except json.JSONDecodeError as e:
        print(f"JSON Decoding Error: {e}")
        return -1
    
def content_generator(role, work, additional_info=None):
        retries, max_retries = 0, 5
        if retries < max_retries:
            try:
                raw_content = generate_content(role, work, additional_info)
                parsed_content = clean_json_output(raw_content)
                return parsed_content
            except Exception as e:
                retries = retries + 1
                print(f"Exception occurred : {e}. Retrying...")
        else:
            print(f"Max retries exceeded. Please try after sometime...")


if __name__ == '__main__':
    jsoned_content = content_generator(
        role='Gigachad',
        work=f'''Motivate someone who is addicted to smoking.''',
        # additional_info='Do not keep track of the items'
    )
    print(jsoned_content)